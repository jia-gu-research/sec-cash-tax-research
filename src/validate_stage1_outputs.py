"""Independent frozen-output acceptance checks; run from the submission root."""
from pathlib import Path
import json, hashlib
import pandas as pd
import nbformat

root=Path(__file__).resolve().parents[1]
out=root/'outputs'/'stage1'
checks={}
def read(name): return pd.read_csv(out/name,dtype='string')
audit=read('total_eligibility_audit.csv')
excluded=read('total_exclusion_log.csv')
cov=read('filing_coverage_10k.csv')
rec=read('cash_tax_reconciliation_184.csv')
register=read('march_pilot_exception_register.csv')
reference=pd.read_csv(root/'evidence/pilot_reconciliation_reference.csv',dtype='string')
checks['one_row_per_original_10k']=audit.adsh.is_unique and len(audit)==2340
checks['eligibility_universe_equals_coverage']=set(audit.adsh)==set(cov.adsh)
checks['exclusions_complete']=set(excluded.adsh)==set(audit.loc[audit.analysis_eligible.eq('False'),'adsh'])
checks['exclusion_reasons_complete']=excluded.exclusion_reason.notna().all()
checks['provisional_label_only']=audit.loc[audit.analysis_eligible.eq('True'),'eligibility_status'].eq('ELIGIBLE_PROVISIONAL').all()
checks['ineligible_analytical_values_missing']=audit.loc[audit.analysis_eligible.eq('False'),'analytical_total_usd'].isna().all()
checks['reported_values_not_imputed']=pd.to_numeric(audit.reported_total_usd).equals(pd.to_numeric(audit.value))
checks['zero_retention']=int(audit.reported_zero.eq('True').sum())==125 and int(audit.loc[audit.analysis_eligible.eq('True'),'reported_zero'].eq('True').sum())==123
bb=audit.set_index('adsh').loc['0001836981-26-000018']
checks['bigbear_zero_preserved']=float(bb.reported_total_usd)==0 and bb.analysis_eligible=='False' and bb.semantic_status=='LEGACY_ROW_SCOPE_AMBIGUOUS'
sm=register.set_index('adsh').loc['0000091388-26-000014']
checks['smithfield_precision_only']=sm.rounding_status=='ROUNDING_COMPATIBLE' and sm.rounding_confirmed=='False' and float(sm.geo_accepted_sum)==0
other=register.loc[register.other_candidate_amount_usd.astype(float).ne(0)]
checks['cal_sign_not_ignored']=len(other)==2 and pd.to_numeric(other.other_cal_weight).eq(-1).all() and pd.to_numeric(other.other_adjustment_usd).eq(0).all() and other.final_classification.eq('OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW').all()
keys=['adsh','ddate','qtrs','uom','dimh']
left=reference.set_index(keys).sort_index()
right=rec.set_index(keys).sort_index()
assert left.index.equals(right.index)
for field in ['reported_total_usd','federal_usd','state_local_usd','foreign_usd','strict_component_sum','strict_difference']:
    pd.testing.assert_series_equal(pd.to_numeric(left[field]),pd.to_numeric(right[field]),check_dtype=False)
checks['all_original_strict_amounts_and_differences_unchanged']=True
checks['seven_original_exceptions_retained']=set(register.adsh)==set(reference.loc[pd.to_numeric(reference.strict_difference).ne(0),'adsh']) and len(register)==7
raw=read('cash_tax_raw_selected_concepts.csv')
key=['adsh','tag','version','ddate','qtrs','uom','dimh']
dups=raw.loc[raw.duplicated(key,False)].groupby(key,dropna=False)
checks['all_duplicate_context_qualifiers_agree']=all(not dups[c].nunique(dropna=False).gt(1).any() for c in ['coreg','datp','durp','dimn'])
checks['iprx_zero_unique_even_singletons']=raw.groupby(key,dropna=False).iprx.agg(lambda s:s.eq('0').sum()).eq(1).all()
checks['geographic_relationships_not_confirmed']=read('geographic_relations.csv').accounting_relationship_confirmed.eq('False').all()
checks['fiscal_label_mismatches_not_blanket_excluded']=int(audit.loc[audit.analysis_eligible.eq('True'),'fy_calendar_label_mismatch'].eq('True').sum())==46
dictionary=pd.read_csv(root/'evidence/output_variable_dictionary.csv',dtype='string')
all_fields=set().union(*(set(pd.read_csv(p,nrows=0).columns) for p in out.glob('*.csv')))
checks['all_output_variables_documented']=all_fields==set(dictionary.variable)
nb=nbformat.read(root/'notebooks/01_data_construction_QA.ipynb',as_version=4)
nbformat.validate(nb)
code=[c for c in nb.cells if c.cell_type=='code']
checks['all_notebook_code_cells_executed']=all(c.execution_count is not None for c in code)
checks['no_notebook_error_outputs']=all(o.output_type!='error' for c in code for o in c.outputs)
required=['README.md','requirements-stage1.txt','docs/stage1_data_dictionary.md','docs/march_pilot_processing_rules.md']
checks['required_documents_present']=all((root/p).is_file() for p in required)
raw_input=root/'data/raw/2026_03_notes.zip'
raw_hash_status='NOT_CHECKED_RAW_INPUT_NOT_PRESENT'
if raw_input.is_file():
    raw_hash_status='MATCH' if hashlib.file_digest(raw_input.open('rb'),'sha256').hexdigest()=='d1c1711e6cee2f197fb91879521da178329d1c1ed369f9086aa501aff45f83d4' else 'MISMATCH'
    checks['raw_sec_input_hash_matches']=raw_hash_status=='MATCH'
required_evidence=['exception_review.csv','inline_xbrl_evidence.json',
                   'prior_singleton_anomalies.csv','pilot_reconciliation_reference.csv',
                   'output_variable_dictionary.csv']
checks['required_evidence_present']=all((root/'evidence'/name).is_file() for name in required_evidence)
assert all(bool(v) for v in checks.values()), {k:bool(v) for k,v in checks.items() if not v}
result={'all_checks_passed':True,'checks':{k:bool(v) for k,v in checks.items()},
        'evidence_files_checked':len(required_evidence),'raw_sec_input_hash_status':raw_hash_status,
        'code_cells_executed':len(code),'documented_variables':len(all_fields)}
(out/'final_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='original_file_preservation'},indent=2))
