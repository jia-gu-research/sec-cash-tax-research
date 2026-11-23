"""Transparent sample construction, feasibility checks, and noncausal Logit."""
import json
import warnings
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.optimize import linprog


def construct_sample(tax, universe, financial):
    sample = tax.copy()
    assert sample.adsh.is_unique
    sample = sample.merge(universe[['adsh', 'sic', 'countryinc']], on='adsh', validate='one_to_one')
    for variable in ['PretaxIncome', 'TotalAssets', 'TotalRevenue']:
        part = financial.loc[financial.variable.eq(variable)].drop(columns='variable')
        part = part.rename(columns={c: variable if c == 'value' else variable+'_'+c for c in part if c != 'adsh'})
        sample = sample.merge(part, on='adsh', how='left', validate='one_to_one')
    sample['CashTaxAmount'] = pd.to_numeric(sample.reported_total_usd)
    sample['PretaxLoss'] = sample.PretaxIncome.lt(0).where(sample.PretaxIncome.notna()).astype('Int64')
    sample['PositiveCashTax'] = sample.CashTaxAmount.gt(0).where(sample.CashTaxAmount.notna()).astype('Int64')
    # Keep customer-contract revenue separate: it is not certified total revenue.
    sample['RevenueIncludingProxy'] = sample.TotalRevenue
    sample['TotalRevenue'] = sample.TotalRevenue.where(sample.TotalRevenue_tag.eq('Revenues'))
    for var, log in [('TotalAssets', 'LogAssets'), ('TotalRevenue', 'LogRevenue'),
                     ('RevenueIncludingProxy', 'LogRevenueIncludingProxy')]:
        sample[log] = np.log(sample[var].where(sample[var].gt(0)))
    # Keep all accessions in audit; reject every member of a repeated company-period group.
    sample['duplicate_company_period'] = sample.duplicated(['cik', 'period'], keep=False)
    sample['Stage1Eligible'] = sample.analysis_eligible.eq('True')
    sample['base_eligible'] = sample.Stage1Eligible & ~sample.duplicate_company_period & sample.CashTaxAmount.notna()
    sample['loss_sample'] = sample.base_eligible & sample.PretaxIncome.lt(0)
    sample['size_sample'] = sample.loss_sample & sample.LogAssets.notna()
    sample['regression_sample'] = sample.size_sample & sample.LogRevenue.notna()
    sample['proxy_regression_sample'] = sample.size_sample & sample.LogRevenueIncludingProxy.notna()
    sic = pd.to_numeric(sample.sic, errors='coerce')
    sample['paper_screen_proxy'] = (sample.countryinc.eq('US') & sic.notna()
        & ~sic.between(4900, 4999) & ~sic.between(6000, 6999) & sample.TotalAssets.ge(10_000_000)
        & ~sample.company.str.contains(r'\bREIT\b|\bTRUST\b|LIMITED PARTNERSHIP|\bL\.?P\.?$', case=False, na=False))
    sample['strict_revenue_sample'] = sample.regression_sample & sample.TotalRevenue_tag.eq('Revenues')
    sample['exclusion_stage2'] = ''
    stages = [(~sample.Stage1Eligible, 'STAGE1_NOT_ELIGIBLE'),
              (sample.duplicate_company_period, 'DUPLICATE_COMPANY_PERIOD'),
              (sample.PretaxIncome.isna(), 'PRETAX_UNAVAILABLE_OR_UNRESOLVED'),
              (~sample.PretaxIncome.lt(0), 'NOT_PRETAX_LOSS'),
              (sample.LogAssets.isna(), 'ASSETS_MISSING_OR_NONPOSITIVE'),
              (sample.LogRevenue.isna(), 'REVENUE_MISSING_OR_NONPOSITIVE')]
    for mask, reason in stages:
        sample.loc[mask & sample.exclusion_stage2.eq(''), 'exclusion_stage2'] = reason
    assert sample.loc[sample.regression_sample, ['cik', 'period']].duplicated().sum() == 0
    assert not sample.loc[sample.adsh.eq('0001836981-26-000018'), 'base_eligible'].any()
    assert np.array_equal(sample.CashTaxAmount.isna(), pd.to_numeric(tax.reported_total_usd).isna())
    assert sample.loc[sample.regression_sample, 'exclusion_stage2'].eq('').all()
    return sample


def sample_report(s):
    rows = []
    sequential = [('01_original_10k', pd.Series(True, index=s.index)),
        ('02_stage1_provisional', s.Stage1Eligible), ('03_unique_company_period_valid_tax', s.base_eligible),
        ('04_matched_pretax', s.base_eligible & s.PretaxIncome.notna()),
        ('05_pretax_losses', s.loss_sample), ('06_positive_assets', s.size_sample),
        ('07_positive_revenue_final', s.regression_sample)]
    previous = len(s)
    for name, mask in sequential:
        rows.append(dict(section='sequential', measure=name, n=int(mask.sum()),
                         removed_from_previous=previous-int(mask.sum()), denominator='previous_step'))
        previous = int(mask.sum())
    for label, mask in [('original_10k', pd.Series(True,index=s.index)), ('stage1_provisional', s.Stage1Eligible),
                        ('matched_pretax', s.base_eligible & s.PretaxIncome.notna()),
                        ('loss_firms', s.loss_sample), ('final_regression', s.regression_sample)]:
        g = s.loc[mask]
        metrics = {'total':len(g), 'pretax_available':g.PretaxIncome.notna().sum(),
            'pretax_missing':g.PretaxIncome.isna().sum(), 'loss':g.PretaxIncome.lt(0).sum(),
            'profitable':g.PretaxIncome.gt(0).sum(), 'pretax_zero':g.PretaxIncome.eq(0).sum(),
            'cash_tax_valid_numeric':g.CashTaxAmount.notna().sum(), 'cash_tax_positive':g.CashTaxAmount.gt(0).sum(),
            'cash_tax_zero':g.CashTaxAmount.eq(0).sum(), 'cash_tax_negative_refund':g.CashTaxAmount.lt(0).sum(),
            'cash_tax_missing':g.CashTaxAmount.isna().sum(), 'assets_missing':g.TotalAssets.isna().sum(),
            'assets_nonpositive':g.TotalAssets.le(0).sum(), 'revenue_missing':g.TotalRevenue.isna().sum(),
            'revenue_nonpositive':g.TotalRevenue.le(0).sum(),
            'revenue_including_proxy_available':g.RevenueIncludingProxy.notna().sum(),
            'revenue_proxy':g.TotalRevenue_definition.eq('CUSTOMER_CONTRACT_REVENUE_PROXY_NOT_VERIFIED_TOTAL').sum()}
        rows.extend(dict(section=label, measure=k, n=int(v), removed_from_previous=None, denominator=label) for k,v in metrics.items())
    return pd.DataFrame(rows)


VARIABLES = ['PretaxIncome','TotalAssets','TotalRevenue','RevenueIncludingProxy','CashTaxAmount','PretaxLoss','PositiveCashTax','LogAssets','LogRevenue','LogRevenueIncludingProxy']


def descriptive(s):
    parts=[]
    for label, mask in [('eligible',s.base_eligible), ('loss',s.loss_sample), ('regression',s.regression_sample)]:
        g=s.loc[mask, VARIABLES].astype(float)
        d=g.describe(percentiles=[.25,.5,.75]).T.reset_index(names='variable')
        d['sample']=label
        d['missing']=g.isna().sum().values
        parts.append(d)
    corr=s.loc[s.regression_sample, VARIABLES].astype(float).corr()
    return pd.concat(parts,ignore_index=True), corr


def fit_logit(s, mask, predictors, name):
    """Gate sample and detect complete/quasi separation BEFORE fitting.

    Threshold (>=50 rows, >=20 per outcome) is a disclosed project heuristic,
    not a theorem. Exact separation feasibility uses standardized predictors.
    """
    g=s.loc[mask].copy()
    y=g.PositiveCashTax.astype(float)
    info={'model':name,'n':len(g),'positive':int(y.sum()),'nonpositive':int((y==0).sum()),
          'predictors':predictors,'status':'NOT_ESTIMATED'}
    if len(g)<50 or y.nunique()!=2 or y.value_counts().min()<20:
        return pd.DataFrame(), pd.DataFrame(), dict(info,reason='INSUFFICIENT_SAMPLE_OR_OUTCOME_VARIATION')
    X=sm.add_constant(g[predictors].astype(float), has_constant='add')
    if np.linalg.matrix_rank(X)!=X.shape[1]:
        return pd.DataFrame(),pd.DataFrame(),dict(info,reason='RANK_DEFICIENT')
    Z=X.copy()
    for p in predictors: Z[p]=(Z[p]-Z[p].mean())/Z[p].std()
    signed=Z.to_numpy()*(2*y.to_numpy()-1)[:,None]
    # Feasible iff all margins nonnegative and at least one strictly positive.
    lp=linprog(np.zeros(Z.shape[1]),A_ub=np.vstack([-signed,-signed.sum(axis=0)]),
               b_ub=np.r_[np.zeros(len(g)),-1.],bounds=[(None,None)]*Z.shape[1],method='highs')
    if lp.success:
        return pd.DataFrame(),pd.DataFrame(),dict(info,reason='COMPLETE_OR_QUASI_SEPARATION')
    if lp.status != 2:
        return pd.DataFrame(),pd.DataFrame(),dict(info,reason='SEPARATION_TEST_INDETERMINATE')
    # One observation per firm is expected; otherwise use firm clustering.
    clustered=g.cik.duplicated().any()
    cov_type='cluster' if clustered else 'HC0'
    cov_kwds={'groups':g.cik} if clustered else {}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        fit_options={'cov_type':cov_type}
        if clustered:
            fit_options['cov_kwds']=cov_kwds
        result=sm.Logit(y,X).fit(disp=False,maxiter=200,**fit_options)
    if not result.mle_retvals['converged'] or not np.isfinite(result.bse).all():
        return pd.DataFrame(),pd.DataFrame(),dict(info,reason='NONCONVERGENCE_OR_INVALID_SE')
    assert result.cov_type == cov_type
    if not clustered:
        # Independent sandwich check guards against a mislabeled robust covariance.
        bread=np.linalg.inv(-result.model.hessian(result.params))
        scores=result.model.score_obs(result.params)
        sandwich=bread @ (scores.T @ scores) @ bread
        np.testing.assert_allclose(result.cov_params(),sandwich,rtol=1e-7,atol=1e-9)
    ci=result.conf_int()
    table=pd.DataFrame({'term':X.columns,'coefficient':result.params.values,'robust_se':result.bse.values,
        'p_value':result.pvalues.values,'ci_lower':ci[0].values,'ci_upper':ci[1].values})
    table['model']=name;table['n']=len(g);table['pseudo_r2_mcfadden']=result.prsquared;table['covariance']=cov_type
    margins=result.get_margeff(at='overall',method='dydx').summary_frame().reset_index(names='term')
    margins['model']=name;margins['n']=len(g);margins['covariance']=cov_type
    info.update(status='ESTIMATED',converged=True,covariance=cov_type,pseudo_r2_mcfadden=float(result.prsquared),
        log_likelihood=float(result.llf),null_log_likelihood=float(result.llnull),
        condition_number_standardized=float(np.linalg.cond(Z)),
        max_abs_score=float(np.max(np.abs(result.model.score(result.params)))),
        warnings=[str(w.message) for w in caught],separation='NONE_DETECTED',
        revenue_proxy_n=int(g.TotalRevenue_definition.eq('CUSTOMER_CONTRACT_REVENUE_PROXY_NOT_VERIFIED_TOTAL').sum()))
    return table,margins,info
