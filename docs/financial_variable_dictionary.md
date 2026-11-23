# Financial variables and selection rules

This is a March 2026 filing-vintage analysis, not a panel of all fiscal-2025 firms.
Dollar values are nominal USD. No exchange conversion, inflation adjustment,
winsorization, missing-value imputation, or component summation is performed.

## Approved financial concepts

| Research field | US-GAAP XBRL concept | Meaning and restrictions |
|---|---|---|
| PretaxIncome | IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest | Continuing operations before income taxes and noncontrolling interests, **including** equity-method income. Not claimed identical to Compustat PI in every filing. |
| TotalAssets | Assets | Consolidated stock at the matched reporting-period end; qtrs=0. |
| TotalRevenue | Revenues | Broad consolidated revenue; only this tag supplies TotalRevenue and the primary LogRevenue. |
| RevenueIncludingProxy | Revenues; otherwise RevenueFromContractWithCustomerExcludingAssessedTax or RevenueFromContractWithCustomerIncludingAssessedTax | Supplementary measure. Customer-contract revenue may exclude leasing, interest or other activities; gross/net assessed-tax treatment also differs. Never presented as verified total revenue. |

The narrower concept
`IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments`
excludes equity-method earnings. It is extracted for audit but **not substituted** for PretaxIncome.
No reconstruction from net income plus tax expense is attempted.

Actual `(variable, tag, version)` frequencies are in `audit/selected_tag_versions.csv`;
full taxonomy descriptions are in `audit/tag_metadata.csv`. Standard US-GAAP
versions are retained explicitly, never averaged or collapsed. IFRS and custom
versions are not automatically mapped into these variables.

## Fact matching and provenance

The raw identity is `adsh, tag, version, ddate, qtrs, uom, dimh, iprx`.
Duplicate groups omit iprx from this key. Within a group, coreg, datp, durp and
dimn must agree; there must be exactly one iprx=0 and no repeated iprx.
Numeric facts must have intersecting Decimal round-to-nearest precision intervals
and equal values at equal declared precision. Mixed missing/numeric, context
conflicts or unknown precision are review cases, not values to average. All-nil
groups remain missing. Footnotes from all representations are preserved.
Finite dcml=128 is not automatically invalid; 32767 gives a point interval,
and -32768 is not exponentiated. The prior Stage 1 iWallet source flag remains an
exclusion even though its numeric zero is preserved.

Financial flows must match the selected cash tax's accession, standardized end
date, qtrs=4, USD, dimension hash 0x00000000, dimn=0 and empty coreg. Numeric
datp and durp must match exactly; no period tolerance joins. Assets require
qtrs=0 and matching datp/end date. All three must appear in PRE's non-parenthetical
primary statement (IS or BS). These are conservative checks using flattened SEC
metadata; exact original context dates and consolidation semantics are not
universally source-verified. Zero dimension hash is a necessary screen, not a
proof that every cash-tax note and income-statement figure has identical economic scope.

When broad Revenues is present it takes priority over customer-contract concepts;
a missing broad amount does not trigger a narrower fallback. Otherwise exactly
one numeric customer-contract tag/version can be used in the supplementary proxy.
Multiple numeric candidates or raw versions are held for review, even if equal.
Custom monetary tags matching income-before-tax, revenue or total-assets patterns
are preserved in `audit/custom_tag_candidates_not_used.csv`, without automatic
selection. This is a discovery list, not exhaustive semantic classification of
all company-specific tags. Missing custom-only observations require manual mapping.

`audit/financial_selection.csv` has one row per accession and candidate variable,
with status, value, definition, candidate counts and candidate JSON. Its
TotalRevenue candidate rows include clearly flagged customer-contract proxies;
`research_sample.csv` separates actual TotalRevenue from RevenueIncludingProxy.
Candidate lineage columns `TotalRevenue_tag`, `_definition`, etc. describe that
candidate even where strict TotalRevenue is blank. `_status=SELECTED` certifies
candidate selection, not total-revenue equivalence. Read `_definition` as well.
`NO_UNIQUE_STAGE1_TAX_CONTEXT` means no target cash-tax context was available;
it does not establish that the filing contains no financial statement data.

## Derived fields

| Field | Formula / treatment |
|---|---|
| CashTaxAmount | Stage 1 reported_total_usd unchanged, including reported zero and refunds; audit rows retained even if ineligible |
| PretaxLoss | 1 if PretaxIncome<0, 0 otherwise; NA if PretaxIncome missing |
| PositiveCashTax | 1 if CashTaxAmount>0, 0 for zero/refund; NA if cash tax missing |
| LogAssets | Natural log of TotalAssets in USD only when strictly positive |
| LogRevenue | Natural log of strict TotalRevenue in USD only when strictly positive |
| LogRevenueIncludingProxy | Natural log of RevenueIncludingProxy when strictly positive; supplementary model only |
| Stage1Eligible | Stage 1 analysis_eligible=True (ELIGIBLE_PROVISIONAL) |
| base_eligible | Stage1Eligible, unique CIK/period, nonmissing reported tax |
| loss_sample | base_eligible and PretaxIncome<0 |
| size_sample | loss_sample and valid LogAssets |
| regression_sample | size_sample and valid strict LogRevenue; primary final sample |
| proxy_regression_sample | size_sample and valid LogRevenueIncludingProxy |
| paper_screen_proxy | US incorporation, known SIC excluding 4900–4999/6000–6999, assets>=USD10m, name screening for REIT/trust/LP |
| exclusion_stage2 | First failed primary-sample condition; blank iff included |

`paper_screen_proxy` is supplementary. Company names are an incomplete substitute
for the paper's Compustat business-description legal-form screen. It does not
certify corporate tax status. The broad primary sample intentionally retains
financials/utilities, small firms and non-US-incorporated SEC registrants, making
it different from the original paper.

`research_sample.csv` retains all 2,340 original filings, not just regression
observations. Filing merges use adsh with one-to-one assertions; the analytical
key is `(cik, period)`. All members of repeated original company-period groups are
excluded rather than selecting first/latest. Amendments are linked for review,
never silently substituted. CIK is an SEC registrant identifier, not a guaranteed
ultimate corporate-group identifier.

## Statistical output definitions

`regression_results.csv` contains model, term, coefficient (log odds), robust_se,
two-sided normal p_value, 95% ci_lower/ci_upper, n, McFadden pseudo R-squared
`1 - llf/llnull`, and covariance method. `marginal_effects.csv` reports average
derivatives over each model's observed covariates, with delta-method inference
using the same robust coefficient covariance. Effects for log-dollar regressors
are per one natural-log unit, not per dollar or a one-percentage-point increase.
No causal interpretation. Empty correlation entries for constant variables are
intentional. Descriptive statistics are nonmissing, unweighted and untrimmed;
correlations use the complete primary regression sample, without significance stars.
