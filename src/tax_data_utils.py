"""Stable audit helpers; substantive construction remains visible in the notebook."""
import json
from decimal import Decimal, localcontext
import xml.etree.ElementTree as ET
import pandas as pd

CORE = {
    'IncomeTaxesPaidNet': 'TOTAL',
    'IncomeTaxPaidFederalAfterRefundReceived': 'FEDERAL',
    'IncomeTaxPaidStateAndLocalAfterRefundReceived': 'STATE_LOCAL',
    'IncomeTaxPaidForeignAfterRefundReceived': 'FOREIGN',
}
SCOPE = ['adsh','ddate','qtrs','uom','dimh']
KEY = ['adsh','tag','version','ddate','qtrs','uom','dimh']
TYPES = list(CORE.values())
PARTS = ['FEDERAL','STATE_LOCAL','FOREIGN']


def interval(value, dcml):
    """Closed precision interval (round-to-nearest); None means indeterminate."""
    if pd.isna(value) or pd.isna(dcml):
        return None
    v = Decimal(str(value))
    d = int(dcml)
    if d == 32767:
        return v, v
    if d == -32768:
        return None  # Missing/unsupported marker; never exponentiate it.
    with localcontext() as ctx:
        ctx.prec = max(50, len(v.as_tuple().digits)+abs(d)+10)
        h = Decimal('0.5') * Decimal(10) ** (-d)
        return v-h, v+h


def audit_duplicates(raw, key):
    results = []
    counts = raw.groupby(key, dropna=False)['iprx'].agg(list)
    assert counts.map(lambda x: x.count('0') == 1).all(), 'Missing/nonunique iprx=0'
    assert not raw.duplicated(key+['iprx']).any(), 'Repeated SEC NUM identity'
    for identity, g in raw.loc[raw.duplicated(key, keep=False)].groupby(key, dropna=False):
        for field in ['coreg','datp','durp','dimn']:
            assert g[field].nunique(dropna=False)==1, f'Duplicate context qualifier differs: {field}; review original contexts'
        z = g.loc[g.iprx.eq('0')].iloc[0]
        numeric = g.loc[g.value.notna()]
        notes = list(dict.fromkeys(g.footnote.dropna().astype(str)))
        decision = 'KEEP_0_NUMERIC_PASS'
        lo = hi = None
        if numeric.empty:
            status = 'ALL_MISSING'
            decision = 'KEEP_0_MISSING_NO_NUMERIC_CLAIM'
        else:
            assert len(numeric) == len(g), 'Mixed missing/numeric duplicate needs review'
            vals = [Decimal(v) for v in numeric.value]
            intervals = [interval(r.value, r.dcml) for r in numeric.itertuples()]
            # OIM additionally requires equal values at the same declared precision.
            equal_precision = all(h.value.map(Decimal).nunique() == 1
                                  for _, h in numeric.groupby('dcml', dropna=False))
            assert all(x is not None for x in intervals), 'Indeterminate duplicate precision'
            lo, hi = max(x[0] for x in intervals), min(x[1] for x in intervals)
            assert equal_precision and lo <= hi, 'Inconsistent duplicate amounts'
            status = 'SAME_VALUE' if len(set(vals)) == 1 else 'PRECISION_COMPATIBLE'
            if notes:
                decision = 'KEEP_0_PRESERVE_ANNOTATIONS'
            if (lo, hi) != interval(z.value, z.dcml):
                assert not notes, 'Both note and interval exception: add explicit handling'
                decision = 'KEEP_0_PRESERVE_INTERVAL'
        results.append(dict(zip(key, identity), n_records=len(g),
            iprx_distribution=json.dumps(g.iprx.tolist()), amount_status=status,
            decision=decision, intersection_low=str(lo) if lo is not None else None,
            intersection_high=str(hi) if hi is not None else None,
            group_footnotes_json=json.dumps(notes, ensure_ascii=False) if notes else None,
            values_json=json.dumps(g.value.astype(object).where(g.value.notna(), None).tolist()),
            dcml_json=json.dumps(g.dcml.tolist())))
    qa = pd.DataFrame(results)
    for c in key: qa[c] = qa[c].astype('string')
    detail = raw.merge(qa[key+['amount_status','decision']], on=key, how='left', validate='many_to_one')
    detail['amount_status'] = detail.amount_status.fillna('SINGLETON')
    detail['decision'] = detail.decision.fillna('KEEP_0_SINGLETON')
    detail['selected_iprx0'] = detail.iprx.eq('0')
    return qa, detail


def _write(df, path):
    df.to_csv(path, index=False, encoding='utf-8-sig')


def _axes(s):
    if pd.isna(s): return ''
    return ';'.join(sorted(x.split('=',1)[0] for x in str(s).split(';') if '=' in x))


def build_pilot_outputs(current, sub, raw, cal7, qa, root, output):
    f = current.copy()
    universe = sub.loc[sub.form.eq('10-K')].copy()
    assert universe.adsh.is_unique
    core = f.loc[f.tax_type.isin(TYPES)].copy()
    assert not core.duplicated(SCOPE+['tax_type']).any()
    # Coverage is the historical dimensionless-USD numeric definition, not tag presence.
    base = core.loc[core.uom.eq('USD') & core.dimn.eq('0') & core.value_num.notna()]
    flags = base.assign(present=True).pivot(index='adsh',columns='tax_type',values='present')
    cov = universe[['adsh','cik','name','sic','fy','fp','period','filed','form']].copy()
    for t, name in [('TOTAL','has_total'),('FEDERAL','has_federal'),('STATE_LOCAL','has_state_local'),('FOREIGN','has_foreign')]:
        cov[name] = cov.adsh.isin(flags.index[flags.get(t,pd.Series(False,index=flags.index)).fillna(False)])
    cov['has_complete_four'] = cov[['has_total','has_federal','has_state_local','has_foreign']].all(axis=1)
    base_present=core.loc[core.uom.eq('USD') & core.dimn.eq('0')]
    cov['n_base_scopes'] = cov.adsh.map(base_present[SCOPE].drop_duplicates().groupby('adsh').size()).fillna(0).astype(int)
    cov['coverage_group'] = 'NO_BASE_CORE_NUMERIC'
    cov.loc[cov[['has_federal','has_state_local','has_foreign']].any(axis=1),'coverage_group'] = 'COMPONENTS_WITHOUT_TOTAL'
    cov.loc[cov.has_total,'coverage_group'] = 'TOTAL_AVAILABLE'
    cov.loc[cov.has_complete_four,'coverage_group'] = 'COMPLETE_FOUR'
    summary = pd.DataFrame([{'measure':c,'n_filings':int(cov[c].sum()),'denominator':len(cov),
            'coverage_rate':cov[c].mean()} for c in ['has_total','has_federal','has_state_local','has_foreign','has_complete_four']])
    _write(cov,output/'filing_coverage_10k.csv'); _write(summary,output/'coverage_summary.csv')

    # Missing/zero/absence are represented independently for each USD reporting scope.
    usd = core.loc[core.uom.eq('USD')]
    wide = usd.pivot(index=SCOPE,columns='tax_type',values='value_num').reindex(columns=TYPES)
    present = usd.assign(exists=True).pivot(index=SCOPE,columns='tax_type',values='exists').reindex(columns=TYPES).fillna(False)
    partial = pd.DataFrame(index=wide.index)
    labels = {'TOTAL':'total','FEDERAL':'federal','STATE_LOCAL':'state_local','FOREIGN':'foreign'}
    for t,n in labels.items():
        partial[n+'_usd'] = wide[t]
        partial[n+'_status'] = 'ABSENT_TAG'
        partial.loc[present[t],n+'_status'] = 'PRESENT_MISSING'
        partial.loc[wide[t].notna(),n+'_status'] = 'REPORTED_NONZERO'
        partial.loc[wide[t].eq(0),n+'_status'] = 'REPORTED_ZERO'
    partial['n_core_tags'] = present.sum(axis=1)
    partial['n_core_numeric'] = wide.notna().sum(axis=1)
    partial['disclosure_class'] = 'NUMERIC_'+partial.n_core_numeric.astype(str)
    _write(partial.reset_index(),output/'partial_disclosure_scopes.csv')

    # Geographic output: sums are diagnostics across distinct hashes; no hierarchy acceptance.
    geo = usd.loc[usd.segments.notna()].copy()
    geo['axis_key'] = geo.segments.map(_axes)
    geo['dimension_class'] = 'DIMENSIONED_CANDIDATE'
    _write(geo, output/'geographic_all_candidates.csv')
    relkeys = ['adsh','ddate','qtrs','uom','tax_type','tag','version','axis_key']
    rel = geo.groupby(relkeys,dropna=False).agg(n_geo_facts=('value_num','size'),
        n_geo_numeric=('value_num','count'),geo_sum_usd=('value_num',lambda s:s.sum(min_count=1))).reset_index()
    parent = usd.loc[usd.dimn.eq('0'),['adsh','ddate','qtrs','uom','tax_type','tag','version','value_num']]
    rel = rel.merge(parent.rename(columns={'value_num':'parent_value_usd'}),
        on=relkeys[:-1], how='left', validate='many_to_one',indicator='parent_fact_match')
    rel['relation_status'] = 'NUMERIC_RELATION_UNRESOLVED'
    rel.loc[rel.parent_fact_match.eq('left_only'),'relation_status'] = 'NO_UNDIM_PARENT'
    rel.loc[rel.parent_value_usd.notna() & rel.geo_sum_usd.eq(rel.parent_value_usd),'relation_status'] = 'NUMERIC_SUM_MATCHES_PARENT'
    rel.loc[rel.n_geo_numeric.ne(rel.n_geo_facts),'relation_status'] = 'INCOMPLETE_GEO_VALUES'
    rel['accounting_relationship_confirmed'] = False
    rel['interpretation'] = 'Candidate only: overlapping axes, nested jurisdictions and residual entity scopes require source review'
    _write(rel,output/'geographic_relations.csv')

    rec = wide.dropna(subset=TYPES).reset_index().rename(columns={t:n+'_usd' for t,n in labels.items()})
    rec = rec.rename(columns={'total_usd':'reported_total_usd'})
    rec['strict_component_sum'] = rec[['federal_usd','state_local_usd','foreign_usd']].sum(axis=1)
    rec['strict_difference'] = rec.reported_total_usd-rec.strict_component_sum
    review = pd.read_csv(root/'evidence/exception_review.csv',dtype='string')
    rmap = review.set_index('adsh')
    other_rows=[]
    rec['other_adjustment_usd'] = 0.0
    rec['other_candidate_amount_usd'] = 0.0
    rec['other_cal_weight'] = float('nan')
    rec['other_relationship_status'] = 'NO_OTHER_CANDIDATE'
    rec['verified_other_tag'] = pd.NA
    rec['verified_other_version'] = pd.NA
    for i,r in rec.iterrows():
        if r.adsh not in rmap.index or pd.isna(rmap.loc[r.adsh,'verified_other_tag']): continue
        row = rmap.loc[r.adsh]
        match = f.tag.eq(row.verified_other_tag) & f.version.eq(row.verified_other_version)
        for c in SCOPE: match &= f[c].eq(r[c])
        candidate = f.loc[match]
        assert len(candidate)==1 and candidate.value_num.notna().all()
        candidate = candidate.iloc[0]
        arcs = cal7.loc[cal7.adsh.eq(r.adsh) & cal7.ptag.eq('IncomeTaxesPaidNet')
            & cal7.ctag.eq(candidate.tag) & cal7.cversion.eq(candidate.version)
            & cal7.pversion.eq(f.loc[f.adsh.eq(r.adsh)&f.tax_type.eq('TOTAL')&f.dimh.eq(r.dimh),'version'].iloc[0])]
        assert len(arcs)>0, 'Missing exact CAL tag/version relationship'
        weights=pd.to_numeric(arcs.negative).map({0:1,1:-1})
        assert weights.notna().all() and weights.nunique()==1
        rec.loc[i,'other_candidate_amount_usd']=candidate.value_num
        rec.loc[i,'other_cal_weight']=int(weights.iloc[0])
        if weights.eq(1).all():
            rec.loc[i,'other_adjustment_usd']=candidate.value_num
            rec.loc[i,'other_relationship_status']='POSITIVE_CAL_SCOPE_MATCH'
        else:
            rec.loc[i,'other_relationship_status']='NEGATIVE_CAL_ARC_ADDITIVE_INTERPRETATION_UNVERIFIED'
        rec.loc[i,'verified_other_tag']=candidate.tag
        rec.loc[i,'verified_other_version']=candidate.version
        other_rows.append({**candidate.to_dict(),'n_cal_arcs':len(arcs),'cal_weight':int(weights.iloc[0]),
            'cal_status':rec.loc[i,'other_relationship_status'],'pilot_verified':bool(weights.eq(1).all())})
    rec['difference_after_other'] = rec.strict_difference-rec.other_adjustment_usd
    rec['other_candidate_difference'] = rec.strict_difference-rec.other_candidate_amount_usd
    gkeys = ['adsh','ddate','qtrs','uom']
    ga = geo.groupby(gkeys,dropna=False).agg(n_geo_facts=('value_num','size'),n_geo_numeric=('value_num','count'),geo_candidate_sum=('value_num',lambda s:s.sum(min_count=1))).reset_index()
    rec = rec.merge(ga,on=gkeys,how='left',validate='many_to_one')
    for c in ['n_geo_facts','n_geo_numeric','geo_candidate_sum']: rec[c]=rec[c].fillna(0)
    rec['geo_accepted_sum']=0.0
    rec['geo_review_status']=rec.n_geo_facts.map(lambda n:'PENDING_HIERARCHY_REVIEW' if n else 'NO_GEO_CANDIDATES')
    rec['extended_difference']=rec.difference_after_other # No geographic amount accepted.
    rec['geo_candidate_closes_gap']=rec.difference_after_other.ne(0)&rec.geo_candidate_sum.eq(rec.difference_after_other)
    rec['rounding_tolerance']=float('nan');rec['rounding_compatible']=False
    rec['rounding_tested']=False;rec['rounding_confirmed']=False
    rec['reported_total_fact_status']=rec.reported_total_usd.map(lambda x:'ZERO' if x==0 else 'VALUE')
    rec['analytical_total_usd']=rec.reported_total_usd
    rec['total_semantic_status']='NO_SPECIAL_FLAG_IN_PILOT'
    rec['source_10k_url']='';rec['evidence_note']=''
    rec['qa_status']='STRICT_EXACT'
    for i,r in rec.loc[rec.strict_difference.ne(0)].iterrows():
        mask = f.tax_type.isin(TYPES)
        for c in SCOPE: mask &= f[c].eq(r[c])
        group = f.loc[mask]
        assert len(group)==4
        bounds={x.tax_type:interval(x.value,x.dcml) for x in group.itertuples()}
        assert all(b is not None for b in bounds.values())
        tolerance=sum((b[1]-b[0])/2 for b in bounds.values())
        compatible=abs(Decimal(str(r.strict_difference)))<=tolerance
        rec.loc[i,['rounding_tolerance','rounding_compatible','rounding_tested']]=[float(tolerance),bool(compatible),True]
        assert r.adsh in rmap.index, 'New reconciliation exception: manual source review required'
        for c in ['source_10k_url','evidence_note','total_semantic_status','qa_status']:
            rec.loc[i,c] = rmap.loc[r.adsh,c] if pd.notna(rmap.loc[r.adsh,c]) else ''
        if rec.loc[i,'other_cal_weight']==-1:
            rec.loc[i,'qa_status']='OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW'
            rec.loc[i,'evidence_note']='Prior pilot called Other reconciled. Exact CAL arc has negative=1 (weight -1); subtracting the positive NUM amount closes the gap numerically but is not accepted as a CAL-confirmed additive relationship.'
        if rmap.loc[r.adsh,'total_semantic_status']=='LEGACY_ROW_SCOPE_AMBIGUOUS':
            rec.loc[i,'analytical_total_usd']=float('nan')
    rec['source_accession']=rec.adsh
    rec['source_dataset']='2026_03_notes.zip'
    _write(rec,output/'cash_tax_reconciliation_184.csv')
    ex=rec.loc[rec.strict_difference.ne(0)].copy()
    _write(ex,output/'cash_tax_exception_log.csv')
    _write(pd.DataFrame(other_rows),output/'other_cal_relations.csv')
    register = ex.merge(sub[['adsh','name']],on='adsh',validate='one_to_one')
    register=register.rename(columns={'name':'company','geo_candidate_sum':'geographic_candidate_amount',
                                    'total_semantic_status':'semantic_status','qa_status':'final_classification'})
    register['rounding_status']=register.rounding_compatible.map({True:'ROUNDING_COMPATIBLE',False:'PRECISION_INCOMPATIBLE'})
    register['evidence_source']=register.source_10k_url
    register.loc[register.other_candidate_amount_usd.ne(0),'evidence_source']='SEC ZIP cal.tsv + exact NUM tag/version/scope; CAL negative=1; ZIP readme defines weight -1'
    register['unresolved_issue']=register.evidence_note
    register.loc[register.final_classification.eq('OTHER_RECONCILED'),'unresolved_issue']='No remaining arithmetic gap under verified Other extension; universal semantic verification not claimed'
    register['accounting_geo_relationship_confirmed']=False
    _write(register,output/'march_pilot_exception_register.csv')
    gaps = geo.merge(ex[gkeys+['difference_after_other']],on=gkeys,how='inner',validate='many_to_one')
    gaps=gaps.groupby(gkeys+['axis_key'],dropna=False).agg(n_components=('value_num','size'),
        n_numeric_components=('value_num','count'),component_sum_usd=('value_num',lambda s:s.sum(min_count=1)),difference_after_other=('difference_after_other','first')).reset_index()
    gaps['numeric_gap_match']=gaps.component_sum_usd.eq(gaps.difference_after_other)&gaps.n_components.eq(gaps.n_numeric_components)
    gaps['review_status']='CANDIDATE_ONLY_HIERARCHY_UNVERIFIED'
    _write(gaps,output/'geographic_gap_candidates.csv')
    _write(rec.groupby('qa_status').size().reset_index(name='n_scopes'),output/'cash_tax_qa_summary.csv')
    return {'filing_universe':universe,'coverage_10k':cov,'coverage_summary':summary,
            'partial_scopes':partial.reset_index(),'exception_register':register}


def _context_evidence(root):
    data=json.loads((root/'evidence/inline_xbrl_evidence.json').read_text(encoding='utf-8'))
    result={}
    for source in data['sources']:
        context=source['contexts'][0]
        # The evidence contains namespaced snippets rather than a standalone XML document.
        import re
        start=re.search(r'<xbrli:startDate>(.*?)</xbrli:startDate>',context).group(1)
        end=re.search(r'<xbrli:endDate>(.*?)</xbrli:endDate>',context).group(1)
        adsh= '0000091388-26-000014' if 'Smithfield' in source['company'] else '0001836981-26-000018'
        result[adsh]=(start,end,source['url'])
    return result


def audit_total_eligibility(sub, raw, selected, qa, root, output):
    universe=sub.loc[sub.form.eq('10-K')].copy()
    totals=selected.loc[selected.tag.eq('IncomeTaxesPaidNet')].copy()
    totals['value_num']=pd.to_numeric(totals.value,errors='coerce')
    totals=totals.merge(sub[['adsh','period','fp','form']],on='adsh',validate='many_to_one')
    totals['is_current_annual']=totals.fp.eq('FY')&totals.qtrs.eq('4')&totals.ddate.eq(totals.period)
    totals['is_usd']=totals.uom.eq('USD')
    totals['is_dimensionless']=totals.dimn.eq('0')&totals.dimh.eq('0x00000000')&totals.coreg.isna()
    totals=totals.merge(qa[KEY+['decision','amount_status']],on=KEY,how='left',validate='one_to_one')
    _write(totals,output/'total_fact_candidates.csv')
    grouped=dict(tuple(totals.groupby('adsh',dropna=False)))
    raw_counts=raw.loc[raw.tag.eq('IncomeTaxesPaidNet')].groupby('adsh').size()
    company_period=universe.groupby(['cik','period'],dropna=False).adsh.agg(list).to_dict()
    amendments=sub.loc[sub.form.eq('10-K/A')].copy()
    amap=amendments.groupby(['cik','period'],dropna=False).adsh.agg(list).to_dict()
    amendment_links=[]
    for r in amendments.itertuples():
        originals=company_period.get((r.cik,r.period),[])
        amendment_links.append({'amendment_adsh':r.adsh,'cik':r.cik,'period':r.period,'filed':r.filed,
            'original_accessions_json':json.dumps(originals),'link_status':'SAME_CIK_PERIOD_REVIEW' if originals else 'ORIGINAL_NOT_IN_MONTH',
            'replacement_applied':False})
    _write(pd.DataFrame(amendment_links,columns=['amendment_adsh','cik','period','filed','original_accessions_json','link_status','replacement_applied']),output/'amendment_relationships.csv')
    contexts=_context_evidence(root)
    prior_precision=pd.read_csv(root/'evidence/prior_singleton_anomalies.csv',dtype='string')
    prior_precision=prior_precision.loc[prior_precision.risk.str.contains('UNVERIFIED_PRECISION',na=False)]
    precision_review_keys=set(prior_precision[KEY+['iprx']].itertuples(index=False,name=None))
    records=[]
    for filing in universe.itertuples():
        g=grouped.get(filing.adsh,totals.iloc[:0])
        n=g.loc[g.value_num.notna()]
        annual=n.loc[n.is_current_annual]
        usd=annual.loc[annual.is_usd]
        main=usd.loc[usd.is_dimensionless]
        peers=company_period[(filing.cik,filing.period)]
        amends=amap.get((filing.cik,filing.period),[])
        status='ELIGIBLE_PROVISIONAL';reason=''
        semantic='NOT_INDIVIDUALLY_VERIFIED'
        period_status='NO_TOTAL_FACT'; currency_status='NO_NUMERIC_CURRENT_CANDIDATE';dimension_status='NO_NUMERIC_USD_CURRENT_CANDIDATE'
        if len(g): period_status='PRIOR_COMPARATIVE_ONLY' if (g.ddate<g.period).all() else 'NONCURRENT_OR_NONANNUAL_REVIEW'
        if g.is_current_annual.any(): period_status='CURRENT_ANNUAL_STANDARDIZED'
        if len(annual): currency_status='USD_AVAILABLE' if len(usd) else 'NON_USD_OR_MISSING_UNIT'
        if len(usd): dimension_status='DIMENSIONLESS_AVAILABLE' if len(main) else 'DIMENSIONED_OR_COREG_ONLY'
        duplicate_status='NO_SELECTED_TOTAL'
        chosen=main.iloc[0] if len(main)==1 else None
        if chosen is not None:
            duplicate_status=chosen.decision if pd.notna(chosen.decision) else 'SINGLETON'
        if g.empty: status='EXCLUDED_NO_TOTAL_TAG';reason='No selected standard Total concept in this filing'
        elif n.empty: status='EXCLUDED_TOTAL_VALUE_MISSING';reason='Total concept present; all reported amounts missing'
        elif annual.empty: status='REVIEW_NO_CURRENT_ANNUAL_NUMERIC';reason='No numeric Total with fp=FY, qtrs=4 and standardized ddate=SUB.period'
        elif usd.empty: status='REVIEW_NON_USD_CURRENT_TOTAL';reason='No current annual USD Total; no exchange-rate conversion applied'
        elif main.empty: status='REVIEW_DIMENSIONED_TOTAL_ONLY';reason='Current annual USD Total exists only with dimensional/entity scope'
        elif len(main)>1: status='REVIEW_MULTIPLE_TOTAL_CANDIDATES';reason='Multiple tag/version candidates in the target scope; no automatic summation'
        elif interval(chosen.value,chosen.dcml) is None: status='REVIEW_UNINTERPRETABLE_PRECISION';reason='Special or missing precision marker requires original XBRL review'
        elif tuple(chosen[c] for c in KEY+['iprx']) in precision_review_keys:
            status='REVIEW_UNVERIFIED_PRECISION_SOURCE';reason='Prior duplicate audit flagged this singleton precision (dcml=128); original decimals attribute not independently verified. Finite 128 is mathematically valid, not treated as a missing marker.'
        elif len(peers)>1: status='REVIEW_MULTIPLE_ORIGINAL_FILINGS';reason='Multiple original accessions for CIK/reporting period; do not delete automatically'
        if filing.adsh=='0001836981-26-000018':
            semantic='LEGACY_ROW_SCOPE_AMBIGUOUS'
            status='EXCLUDED_SEMANTIC_AMBIGUITY';reason='Actual XBRL zero in legacy row; current-period analytical comparability unverified'
        elif filing.adsh=='0000091388-26-000014': semantic='SOURCE_REVIEWED_ROUNDING_COMPATIBLE'
        eligible=status=='ELIGIBLE_PROVISIONAL'
        val=float(chosen.value_num) if chosen is not None else float('nan')
        start,end,url=contexts.get(filing.adsh,('','',''))
        rec={'adsh':filing.adsh,'cik':filing.cik,'company':filing.name,'form':filing.form,'filed':filing.filed,
            'fy':filing.fy,'fp':filing.fp,'period':filing.period,'fye':filing.fye,
            'total_tag_present':not g.empty,'numeric_total_any_period':not n.empty,
            'raw_numeric_total_coverage':bool(len(usd.loc[usd.dimn.eq('0')])),
            'total_fact_count':len(g),'total_raw_num_count':int(raw_counts.get(filing.adsh,0)),
            'annual_current_numeric_count':len(annual),'usd_current_numeric_count':len(usd),'target_total_candidate_count':len(main),
            'reported_total_usd':val,'reported_zero':bool(pd.notna(val) and val==0),
            'total_tag':'IncomeTaxesPaidNet' if len(g) else '',
            'period_status':period_status,'currency_status':currency_status,'dimension_status':dimension_status,
            'duplicate_status':duplicate_status,'semantic_status':semantic,'eligibility_status':status,
            'analysis_eligible':eligible,'analytical_total_usd':val if eligible else float('nan'),
            'exclusion_reason':reason,'amendment_status':'LINKED_AMENDMENT_NOT_SUBSTITUTED' if amends else 'NO_LINKED_AMENDMENT_IN_MONTH',
            'related_amendments_json':json.dumps(amends),'same_cik_period_originals_json':json.dumps(peers),
            'original_context_start':start,'original_context_end':end,'source_10k_url':url,
            'context_verification_status':'PRESERVED_ORIGINAL_INLINE_EVIDENCE' if url else 'NOT_AVAILABLE_IN_SEC_FLAT_NUM',
            'fy_calendar_label_mismatch':str(filing.fy)!=str(filing.period)[:4],
            'all_total_fact_identities_json':g[KEY+['iprx']].to_json(orient='records')}
        for c in ['version','ddate','qtrs','uom','dimh','iprx','value','dcml','dimn','coreg','durp','datp','footnote','duplicate_footnotes_json','duplicate_interval_low','duplicate_interval_high']:
            rec[c]=chosen.get(c,pd.NA) if chosen is not None else pd.NA
        records.append(rec)
    audit=pd.DataFrame(records)
    assert len(audit)==len(universe) and audit.adsh.is_unique
    summary=audit.groupby('eligibility_status',dropna=False).agg(n_filings=('adsh','size'),n_reported_zero=('reported_zero','sum')).reset_index()
    summary['share_of_original_10k']=summary.n_filings/len(universe)
    excluded=audit.loc[~audit.analysis_eligible].copy()
    stage_masks=[('01_ORIGINAL_10K',pd.Series(True,index=audit.index),'Original 10-K, not 10-K/A'),
      ('02_TOTAL_TAG_ANY_PERIOD',audit.total_tag_present,'Standard Total tag present in any period/scope'),
      ('03_NUMERIC_TOTAL_ANY_PERIOD',audit.numeric_total_any_period,'At least one nonmissing numeric Total'),
      ('04_CURRENT_ANNUAL_NUMERIC',audit.annual_current_numeric_count.gt(0),'fp FY, qtrs 4, standardized ddate equals period'),
      ('05_DIMENSIONLESS_USD_CURRENT',audit.raw_numeric_total_coverage,'Original 1,159 coverage definition'),
      ('06_UNIQUE_DUPLICATE_REVIEWED',audit.target_total_candidate_count.eq(1)&~audit.eligibility_status.isin(['REVIEW_UNINTERPRETABLE_PRECISION','REVIEW_UNVERIFIED_PRECISION_SOURCE','REVIEW_MULTIPLE_ORIGINAL_FILINGS']),'Unique target fact; duplicate audit; prior precision-source flags cleared'),
      ('07_SEMANTIC_EXCLUSIONS_APPLIED',audit.semantic_status.ne('LEGACY_ROW_SCOPE_AMBIGUOUS'),'Exclude known legacy-row ambiguity; no universal semantic verification'),
      ('08_ELIGIBLE_PROVISIONAL',audit.analysis_eligible,'Mechanical checks pass; semantic validity provisional')]
    running=pd.Series(True,index=audit.index);prev=len(audit);bridge=[]
    for stage,mask,definition in stage_masks:
        running &= mask
        count=int(running.sum())
        bridge.append({'stage':stage,'n_filings':count,'reduction_from_previous':prev-count,'definition':definition})
        prev=count
    bridge=pd.DataFrame(bridge)
    assert bridge.iloc[-1].n_filings==audit.analysis_eligible.sum()
    _write(audit,output/'total_eligibility_audit.csv');_write(summary,output/'total_eligibility_summary.csv')
    _write(excluded,output/'total_exclusion_log.csv');_write(bridge,output/'total_eligibility_count_bridge.csv')
    return audit,summary,bridge
