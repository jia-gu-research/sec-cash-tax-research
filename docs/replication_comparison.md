# Comparison with Edwards, Kubata and Shevlin (2026)

Source: *Tax Payments in Loss Firms*, Contemporary Accounting Research 43,
1338–1375, [published paper](https://doi.org/10.1111/1911-3846.70064).
Definitions checked against the supplied published PDF, Section 4.1, Table 2,
Table 5 and Appendix 2 (PDF pages 15, 21, 35–36; printed pages 1352, 1358, 1372–1373).

**Classification: preliminary analogous extensive-margin analysis / partial
empirical exercise. This is not a reproduction of Table 5 or the paper's model.**

| Item | Published paper | Stage 2 operational definition | Reason / implication |
|---|---|---|---|
| Data and sample | Compustat North America; 1988–2023; 117,638 firm-years, including 36,989 losses | March 2026 SEC submission cohort; final realized counts in sample_selection_report.csv | Single filing vintage with disclosure and filing-timing selection; not a balanced annual population |
| Country/industry/size | US-incorporated, nonfinancial/nonutility, assets around USD10m minimum, excludes REIT/LP via descriptions | Broad provisional SEC sample; separate paper-screen proxy using countryinc, SIC, assets>=10m and names | Stage 1 did not impose the paper's population screen; names cannot reproduce business-description review |
| Pretax income PI | Compustat PI; PI=0 excluded | Standard US-GAAP continuing-operations pretax income including equity-method earnings; primary loss sample requires <0 | SEC standard tag is an approximation, not proven Compustat equivalence |
| TXPD | Compustat cash taxes paid; refunds are non-taxpaying | Stage 1 IncomeTaxesPaidNet in USD, unchanged | Known semantic/precision cases excluded; remaining semantic status provisional |
| D_TXPD | Among PI<0: 1 for TXPD>0, 0 otherwise | PositiveCashTax, same sign rule among matched losses | Closest replicated definition; missing observations remain missing |
| Assets TA | Compustat AT in millions | Matched end-period Assets in dollars | Stock at year end; monetary scale explicitly different |
| SIZE | -TA/PI, winsorized then standardized for regressions | LogAssets=ln(USD Assets) | Deliberate parsimonious adaptation requested for preliminary analysis; coefficients are not comparable to paper SIZE=0.057 |
| Revenue | No revenue regressor in main Table 5 | LogRevenue=ln(strict Revenues); supplementary customer-contract revenue proxy | Additional scale/operating-activity correlate, not an original-paper control |
| Other determinants | Multinational status, state tax, consolidation differences, impairments/write-downs, extraordinary/discontinued items, CAPX, loss frequency/magnitude | Not estimated | Three financial variables and one vintage cannot reproduce the mechanisms and lag structure. Missing tax components are not coded zero |
| Logit | Panel logistic model with FF49 industry and year FE | Cross-sectional Logit with one or two log variables and intercept | Few controls and limited vintage; no FE or temporal mechanism claims |
| Inference | Table 5 clusters SE by firm | HC0 robust SE if one row per firm; company clustering if repeated CIKs | No repeated-firm panel in the intended design; diagnostics record actual covariance |
| Outliers/scaling | Continuous variables winsorized at 1/99 percentiles by year and standardized | Unwinsorized natural logs, reported monetary levels preserved | Keep transformations teachable and observable; inference not matched to paper |
| Extensive-margin benchmark | 25,146/36,989 taxpaying loss firm-years, about 68% | Actual rates by our sample in sample_selection_report.csv | A difference is descriptive, not a rejection or confirmation of the paper |
| Marginal effects | Table 5 reports probability effects | Average marginal effects with robust delta-method intervals | Functional scale and sample differ, so magnitudes cannot be directly compared |
| Intensive margin and causality | Paper separately studies tax amounts via cash-ETR framework | Not implemented; no causal identification | This deliverable is limited to extensive-margin association |

The paper's prose refers to assets of at least USD10m, whereas Table 2 says
greater than USD10m. Our supplementary screen explicitly uses >=USD10m;
it is not advertised as exact sample replication.

The primary regression's total-revenue restriction can materially select the
sample by reporting practice. M1 uses assets on all available loss observations;
M2 uses assets on the primary complete-case sample; M3 adds strict revenue on that
same sample. S1 expands to the separately labeled revenue proxy. S2 applies the
paper-screen proxy to the strict primary sample. These planned comparisons are
diagnostics of sample/measurement sensitivity, not specification search for a
significant result.
