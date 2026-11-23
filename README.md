# SEC Cash-Tax Research

**Accounting data construction, quality assurance, and preliminary empirical analysis**

This repository is an accounting research coding sample built from the SEC Financial Statement and Notes Data Sets. It demonstrates an end-to-end workflow from XBRL-based cash-tax fact extraction and accounting-aware quality assurance to sample construction and a preliminary Logit analysis.

> **Research-status note:** This is a coding sample and preliminary empirical exercise, not a completed paper, a full replication of the parent study, or a causal design. The project deliberately preserves provisional classifications, missing values, refunds, and unresolved accounting exceptions.

## Project overview

### Stage 1 — SEC cash-tax data construction and QA

The Stage 1 notebook processes a March 2026 SEC filing cohort containing **2,340 original 10-K filings**.

| Check | Result |
|---|---:|
| Original 10-K filings | 2,340 |
| Current annual, dimensionless USD Total coverage | 1,159 |
| Provisionally eligible filing-level Totals | 1,157 |
| Complete four-category Strict reconciliation scopes | 184 |
| Exact Strict reconciliations | 177 |
| Registered exceptions | 7 |

The Stage 1 result is **CONDITIONAL PASS**, not universal semantic validation. The 1,157 observations are provisionally eligible under the documented mechanical rules. Several issues remain explicitly open, including CAL-sign interpretation for two `Other` candidates, geographic reconciliation candidates, and filing-specific semantic or precision-source questions.

The extraction and QA workflow includes:
- extracting standard cash-tax concepts and separately identifying `IncomeTaxPaidOther` candidates;
- preserving XBRL context, period, unit, dimensions, footnotes, and duplicate representations;
- reviewing duplicate facts before selecting the `iprx=0` representation;
- distinguishing reported zeros, missing amounts, and analytical exclusions;
- reconciling reported Total against Federal, State/Local, and Foreign components only within identical reporting scopes;
- recording unresolved exceptions instead of forcing arithmetic matches.

### Stage 2 — preliminary empirical analysis

Stage 2 links the Stage 1 cash-tax observations to selected financial statement variables and studies the extensive margin of positive cash-tax payments among firms reporting pretax accounting losses.

| Sample construction | Observations |
|---|---:|
| Original 10-K filing cohort | 2,340 |
| Stage 1 provisionally eligible | 1,157 |
| Matched pretax-income observations | 946 |
| Pretax-loss observations | 520 |
| Loss observations with positive assets | 519 |
| Primary complete-case Logit sample | 141 |

Among the 520 loss observations with matched pretax income, 405 have positive cash-tax payments, 60 report zero, and 55 report refunds. The primary 141-observation sample contains 108 positive, 24 zero, and 9 refund outcomes.

The primary specification is:

`PositiveCashTax ~ LogAssets + LogRevenue`

with HC0 heteroskedasticity-robust standard errors.

| Variable | Coefficient | HC0 robust SE | p-value |
|---|---:|---:|---:|
| LogAssets | 0.1544 | 0.1139 | 0.1750 |
| LogRevenue | 0.2954 | 0.1196 | 0.0135 |

The primary model has **N = 141** and McFadden pseudo-R² = **0.1952**. These estimates are conditional associations in a selected complete-case sample. They do not establish why loss firms pay cash taxes and should not be interpreted causally.

A supplementary model uses explicitly labeled customer-contract revenue proxies. A smaller paper-screened model is not estimated because it does not meet the project's predeclared minimum outcome-count rule. The exercise is inspired by Edwards, Kubata and Shevlin (2026), *Tax Payments in Loss Firms*, but is **not a full replication** of that paper or its Table 5.

## Repository structure

```text
sec-cash-tax-research/
├── README.md
├── notebooks/
│   ├── 01_data_construction_QA.ipynb
│   └── 02_preliminary_empirical_analysis.ipynb
├── src/
│   ├── tax_data_utils.py
│   ├── extraction.py
│   ├── analysis.py
│   ├── validate_stage1_outputs.py
│   └── validate_stage2_outputs.py
├── tests/
│   └── test_guardrails.py
├── data/
│   ├── README.md
│   ├── raw/                 # SEC ZIP downloaded by the user; not committed
│   └── frozen_inputs/       # small Stage 1 bridge used by Stage 2
├── evidence/                # source-linked review evidence used by Stage 1
├── outputs/
│   ├── stage1/
│   ├── stage2/
│   └── stage2_audit/
├── docs/
├── requirements.txt
├── requirements-stage1.txt
├── requirements-stage2.txt
├── .gitignore
└── LICENSE
```

## Audit trail and size

The project includes the frozen Stage 1 QA tables as well as the Stage 2 candidate-selection, duplicate-fact, and financial-variable selection audits. These included audit tables are much larger when uncompressed than the notebooks themselves, but are highly compressible CSV files. The SEC source ZIP is **not** included.

The `outputs/stage2_audit/` files document the recorded extraction decisions; they are not independently audited by the repository maintainer as part of this repack. The original uploaded portfolio was reorganized into a single repository, so filenames and notebook path initialization changed; **the repacked notebooks have not been rerun against the raw SEC source**. The included analysis tables and notebook outputs are previously generated results, not new runs.

## Reproduction

See [`docs/reproduction.md`](docs/reproduction.md) and [`data/README.md`](data/README.md).

The raw SEC March 2026 ZIP (307 MB) is not redistributed. Download it directly from the SEC, save it as `data/raw/2026_03_notes.zip`, and verify the SHA-256 listed in `data/README.md`.

**Use separate Python environments for Stage 1 and Stage 2.** Their pinned dependency versions differ; do not install both requirement files into the same environment.

## Important interpretation and scope limits

1. **Filing-cohort scope:** March 2026 is a monthly filing cohort, not a population of all firms with fiscal year 2025.
2. **Provisional Stage 1 eligibility:** mechanically eligible observations are not all semantically verified. The project retains documented exceptions.
3. **Disclosure and matching selection:** only 946 provisional observations have a selected pretax-income match; only 141 enter the primary complete-case Logit because broad standard revenue is unavailable for many filings.
4. **Revenue definitions:** the primary model uses the standard `Revenues` tag. Customer-contract revenue is retained as a proxy only in a supplementary specification.
5. **No missing-to-zero conversion:** missing tax amounts and missing financial variables remain missing; refunds are retained as negative cash-tax amounts.
6. **No causal claim:** the Logit is descriptive/associational. It does not identify a causal mechanism.
7. **No full replication claim:** the parent paper uses a multi-year Compustat sample, additional tax-accounting determinants, industry/year effects, and a different SIZE construction.

## Citation and use

The Stage 2 question is inspired by Edwards, Kubata and Shevlin (2026), *Tax Payments in Loss Firms*. The exact paper-to-project definition differences are documented in [`docs/replication_comparison.md`](docs/replication_comparison.md).

The SEC dataset is a public source. The repository's code and documentation are provided for review; see `LICENSE` before reusing or redistributing them.
