"""Independent output checks and alternate GLM verification of primary Logit."""
from pathlib import Path
import hashlib
import json
import unittest
import numpy as np
import pandas as pd
import statsmodels.api as sm
import nbformat

root=Path(__file__).resolve().parents[1]
s=pd.read_csv(root/'outputs/stage2/research_sample.csv',dtype={'adsh':'string','cik':'string','period':'string'})
r=pd.read_csv(root/'outputs/stage2/regression_results.csv')
checks={}
checks['audit_population_unique']=len(s)==2340 and s.adsh.is_unique
g=s.loc[s.regression_sample]
checks['strict_total_revenue_only']=g.TotalRevenue_tag.eq('Revenues').all()
checks['primary_unique_company_period']=not g.duplicated(['cik','period']).any()
checks['primary_all_valid_losses']=g.PretaxIncome.lt(0).all() and g.Stage1Eligible.all()
checks['outcome_reconstructed']=g.PositiveCashTax.eq(g.CashTaxAmount.gt(0).astype(int)).all()
checks['refunds_not_removed']=g.CashTaxAmount.lt(0).sum()==9
checks['logs_reconstructed']=np.allclose(g.LogAssets,np.log(g.TotalAssets)) and np.allclose(g.LogRevenue,np.log(g.TotalRevenue))
checks['no_proxy_mislabeled_total']=s.loc[s.TotalRevenue_tag.ne('Revenues'),'TotalRevenue'].isna().all()
# GLM uses a different fitting algorithm (IRLS) for the same binomial logit likelihood.
X=sm.add_constant(g[['LogAssets','LogRevenue']],has_constant='add')
glm=sm.GLM(g.PositiveCashTax,X,family=sm.families.Binomial()).fit(cov_type='HC0')
primary=r.loc[r.model.eq('M3_assets_revenue_primary')].set_index('term').loc[X.columns]
checks['alternate_irls_coefficients']=np.allclose(glm.params,primary.coefficient,rtol=1e-7,atol=1e-7)
checks['alternate_irls_robust_se']=np.allclose(glm.bse,primary.robust_se,rtol=1e-7,atol=1e-7)
diag=json.loads((root/'outputs/stage2_audit/model_diagnostics.json').read_text())
stopped=[d for d in diag if d['model']=='S2_paper_screen_proxy'][0]
checks['inadequate_model_not_estimated']=stopped['status']=='NOT_ESTIMATED' and 'S2_paper_screen_proxy' not in set(r.model)
nb=nbformat.read(root/'notebooks/02_preliminary_empirical_analysis.ipynb',as_version=4)
nbformat.validate(nb)
code=[c for c in nb.cells if c.cell_type=='code']
checks['notebook_sequential_execution']=[c.execution_count for c in code]==list(range(1,len(code)+1))
checks['notebook_no_error_outputs']=all(o.output_type!='error' for c in code for o in c.outputs)
manifest=json.loads((root/'outputs/stage2_audit/input_hashes_before.json').read_text())
tracked={
    'raw_sec_zip_sha256':root/'data/raw/2026_03_notes.zip',
    'stage1_bridge_sha256':root/'data/frozen_inputs/stage1_bridge.zip'
}
checks['frozen_bridge_matches_pin']=tracked['stage1_bridge_sha256'].is_file() and hashlib.sha256(tracked['stage1_bridge_sha256'].read_bytes()).hexdigest()==manifest['stage1_bridge_sha256']
raw_input=tracked['raw_sec_zip_sha256']
raw_hash_status='NOT_CHECKED_RAW_INPUT_NOT_PRESENT'
if raw_input.is_file():
    raw_hash_status='MATCH' if hashlib.sha256(raw_input.read_bytes()).hexdigest()==manifest['raw_sec_zip_sha256'] else 'MISMATCH'
    checks['source_raw_sec_input_matches_pin']=raw_hash_status=='MATCH'
required=[
    'README.md','notebooks/02_preliminary_empirical_analysis.ipynb',
    'docs/financial_variable_dictionary.md','outputs/stage2/research_sample.csv',
    'outputs/stage2/descriptive_statistics.csv','outputs/stage2/correlation_matrix.csv',
    'outputs/stage2/regression_results.csv','outputs/stage2/sample_selection_report.csv',
    'docs/replication_comparison.md'
]
checks['all_requested_deliverables_present']=all((root/f).is_file() for f in required)
suite=unittest.defaultTestLoader.discover(str(root/'tests'))
test_result=unittest.TextTestRunner(verbosity=1).run(suite)
checks['adversarial_guardrails']=test_result.wasSuccessful()
assert all(checks.values()),{k:bool(v) for k,v in checks.items() if not v}
result={'checks':{k:bool(v) for k,v in checks.items()},'checks_passed':len(checks),
    'guardrail_tests_run':test_result.testsRun,'protected_inputs_rechecked':1+int(raw_input.is_file()),'raw_sec_input_hash_status':raw_hash_status,
    'primary_n':len(g),'alternate_glm_max_coefficient_difference':float(np.max(np.abs(glm.params-primary.coefficient)))}
(root/'outputs/stage2_audit/independent_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
