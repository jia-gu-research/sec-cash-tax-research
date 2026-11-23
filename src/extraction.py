"""Read-only SEC extraction and conservative fact selection. No Stage 1 imports/writes."""
from decimal import Decimal, localcontext
import json
import zipfile
import pandas as pd

PI = 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest'
PI_NARROW = 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments'
REVENUE_TAGS = ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax',
                'RevenueFromContractWithCustomerIncludingAssessedTax']
APPROVED = [PI, 'Assets'] + REVENUE_TAGS
KEY = ['adsh', 'tag', 'version', 'ddate', 'qtrs', 'uom', 'dimh']


def read_sources(raw_path, stage1_zip):
    """Whitelist standard concepts; discover custom candidates for review only."""
    with zipfile.ZipFile(raw_path) as z:
        sub = pd.read_csv(z.open('sub.tsv'), sep='\t', dtype='string')
        tags = pd.read_csv(z.open('tag.tsv'), sep='\t', dtype='string')
        pre = pd.read_csv(z.open('pre.tsv'), sep='\t', dtype='string')
        universe = sub.loc[sub.form.eq('10-K')].copy()
        assert universe.adsh.is_unique and len(universe) == 2340
        custom = tags.custom.eq('1') & tags.datatype.eq('monetary') & tags.tag.str.contains(
            r'Income.*Before.*Tax|Pretax|PreTax|Revenue|TotalAssets', case=False, na=False)
        discovered = tags.loc[custom].copy()
        wanted = set(APPROVED + [PI_NARROW]) | set(discovered.tag)
        pieces = []
        for chunk in pd.read_csv(z.open('num.tsv'), sep='\t', dtype='string', chunksize=250000):
            pieces.append(chunk.loc[chunk.adsh.isin(universe.adsh) & chunk.tag.isin(wanted)])
        raw = pd.concat(pieces, ignore_index=True)
    assert not tags.duplicated(['tag', 'version']).any()
    raw = raw.merge(tags, on=['tag', 'version'], how='left', validate='many_to_one')
    with zipfile.ZipFile(stage1_zip) as z:
        tax = pd.read_csv(z.open('P1_Stage1_Coding_Sample/outputs/total_eligibility_audit.csv'), dtype='string')
        amendments = pd.read_csv(z.open('P1_Stage1_Coding_Sample/outputs/amendment_relationships.csv'), dtype='string')
    return universe, raw, pre, tax, amendments


def precision_interval(value, dcml):
    if pd.isna(value) or pd.isna(dcml):
        return None
    v, d = Decimal(str(value)), int(dcml)
    if d == 32767:
        return v, v
    if d == -32768:
        return None
    with localcontext() as ctx:
        ctx.prec = max(50, len(v.as_tuple().digits) + abs(d) + 10)
        half = Decimal('0.5') * Decimal(10) ** (-d)
        return v-half, v+half


def deduplicate(raw):
    """Check all candidates, not only default rows. Conflicts stay in the audit."""
    rows, selected = [], []
    for key, g in raw.groupby(KEY, dropna=False, sort=False):
        status = 'PASS'
        zeros = g.loc[g.iprx.eq('0')]
        if len(zeros) != 1 or g.iprx.duplicated().any():
            status = 'REVIEW_IPRX_IDENTITY'
        elif any(g[c].nunique(dropna=False) != 1 for c in ['coreg', 'datp', 'durp', 'dimn']):
            status = 'REVIEW_CONTEXT_CONFLICT'
        elif g.value.isna().all():
            status = 'ALL_MISSING'
        elif g.value.isna().any():
            status = 'REVIEW_MIXED_NIL_NUMERIC'
        else:
            bounds = [precision_interval(r.value, r.dcml) for r in g.itertuples()]
            if any(b is None for b in bounds):
                status = 'REVIEW_PRECISION'
            elif (max(b[0] for b in bounds) > min(b[1] for b in bounds)
                  or any(h.value.map(Decimal).nunique() != 1 for _, h in g.groupby('dcml'))):
                status = 'REVIEW_INCONSISTENT_VALUES'
        entry = dict(zip(KEY, key), n_records=len(g), duplicate_status=status,
                     values_json=json.dumps(g.value.fillna('').tolist()),
                     footnotes_json=json.dumps(g.footnote.dropna().unique().tolist()))
        rows.append(entry)
        if status in ['PASS', 'ALL_MISSING']:
            row = zeros.iloc[0].to_dict()
            row.update(duplicate_status=status, duplicate_n=len(g), footnotes_json=entry['footnotes_json'])
            selected.append(row)
    selected = pd.DataFrame(selected) if selected else raw.iloc[:0].copy()
    selected['value_num'] = pd.to_numeric(selected.value, errors='coerce')
    assert not (selected.value.notna() & selected.value_num.isna()).any()
    return selected, pd.DataFrame(rows)


def select_financials(selected, raw, pre, tax):
    """One accession-variable record, with all versions inspected before selection.

    Flow facts must match cash-tax ddate/qtrs/dimh/uom and datp/durp.
    Stocks match the cash-tax end-date offset (datp), but qtrs=0.
    SEC proximity metadata is a conservative proxy, not original XBRL context proof.
    """
    records = []
    selected_groups = dict(tuple(selected.groupby('adsh')))
    raw_groups = dict(tuple(raw.groupby('adsh')))
    primary = pre.loc[pre.inpth.eq('0') & pre.stmt.isin(['IS', 'BS'])]
    presentation = set(primary[['adsh', 'tag', 'version', 'stmt']].itertuples(index=False, name=None))
    for t in tax.itertuples():
        g = selected_groups.get(t.adsh, selected.iloc[:0])
        raw_g = raw_groups.get(t.adsh, raw.iloc[:0])
        for variable, names, qtrs, stmt in [('PretaxIncome', [PI], '4', 'IS'),
                                           ('TotalAssets', ['Assets'], '0', 'BS'),
                                           ('TotalRevenue', REVENUE_TAGS, '4', 'IS')]:
            out = dict(adsh=t.adsh, variable=variable, value=None, status='NO_APPROVED_FACT',
                       tag=None, version=None, ddate=None, qtrs=None, uom=None, dimh=None,
                       datp=None, durp=None, dcml=None, iprx=None, definition=None,
                       target_candidates=0, candidate_tags_json='[]')
            if pd.isna(t.reported_total_usd):
                out['status'] = 'NO_UNIQUE_STAGE1_TAX_CONTEXT'
                records.append(out)
                continue
            eligible = g.loc[g.tag.isin(names) & g.custom.eq('0') & g.version.str.startswith('us-gaap/')]
            if not eligible.empty:
                out['status'] = 'NO_MATCHED_SCOPE_PERIOD_CURRENCY'
            h = eligible.loc[eligible.ddate.eq(t.ddate) & eligible.qtrs.eq(qtrs)
                             & eligible.uom.eq('USD') & eligible.dimh.eq('0x00000000')
                             & eligible.dimn.eq('0') & eligible.coreg.isna()].copy()
            # Equality is exact after numeric conversion, with no tolerance to merge durations.
            h = h.loc[pd.to_numeric(h.datp).eq(float(t.datp))]
            if qtrs == '4':
                h = h.loc[pd.to_numeric(h.durp).eq(float(t.durp))]
            h = h.loc[[tuple([r.adsh, r.tag, r.version, stmt]) in presentation for r in h.itertuples()]]
            out['target_candidates'] = len(h)
            out['candidate_tags_json'] = json.dumps(h[['tag', 'version', 'value']].fillna('').to_dict('records'))
            if h.empty:
                records.append(out)
                continue
            out['status'] = 'PRESENT_MISSING'
            numeric = h.loc[h.value_num.notna()]
            if numeric.empty:
                records.append(out)
                continue
            # Broad Revenues takes precedence over customer-contract revenue, which may be partial.
            if variable == 'TotalRevenue' and h.tag.eq('Revenues').any():
                numeric = h.loc[h.tag.eq('Revenues') & h.value_num.notna()]
            if numeric.empty:
                records.append(out)
                continue
            # Even equal numbers from different versions/tags do not establish identical semantics.
            if len(numeric) != 1:
                out['status'] = 'REVIEW_MULTIPLE_TAG_VERSION_CANDIDATES'
                records.append(out)
                continue
            r = numeric.iloc[0]
            # A rejected duplicate version at this target must not be hidden by a passing version.
            target_raw = raw_g.loc[raw_g.tag.eq(r.tag) & raw_g.ddate.eq(r.ddate)
                                  & raw_g.qtrs.eq(qtrs) & raw_g.uom.eq('USD')
                                  & raw_g.dimh.eq('0x00000000') & raw_g.coreg.isna()]
            if target_raw.version.nunique() != 1:
                out['status'] = 'REVIEW_RAW_MULTIPLE_VERSIONS'
                records.append(out)
                continue
            for c in ['tag', 'version', 'ddate', 'qtrs', 'uom', 'dimh', 'datp', 'durp', 'dcml', 'iprx']:
                out[c] = r[c]
            out.update(value=float(r.value_num), status='SELECTED',
                       definition='STANDARD_CONSOLIDATED_TOTAL')
            if variable == 'TotalRevenue' and r.tag != 'Revenues':
                out['definition'] = 'CUSTOMER_CONTRACT_REVENUE_PROXY_NOT_VERIFIED_TOTAL'
            if variable == 'PretaxIncome':
                out['definition'] = 'CONTINUING_OPERATIONS_PRETAX_INCLUDING_EQUITY_METHOD'
            records.append(out)
    result = pd.DataFrame(records)
    assert not result.duplicated(['adsh', 'variable']).any()
    return result
