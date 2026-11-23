# Data and inputs

## Public SEC input (not redistributed)

Download the SEC Financial Statement and Notes Data Sets release **2026 03** from:

https://www.sec.gov/data-research/sec-markets-data/financial-statement-notes-data-sets

Save the file as:

`data/raw/2026_03_notes.zip`

Expected file size: **307,533,198 bytes**  
Expected SHA-256:

`d1c1711e6cee2f197fb91879521da178329d1c1ed369f9086aa501aff45f83d4`

Both notebooks check this hash and stop if a different release is supplied. The SEC ZIP is intentionally excluded from this repository because it is large; it is a public SEC source and should be downloaded directly from the SEC.

## Frozen Stage 1 bridge (included)

`data/frozen_inputs/stage1_bridge.zip` is a small, frozen input used by Stage 2. It contains only these two Stage 1 output files, at the original archive member paths expected by the extraction code:

- `P1_Stage1_Coding_Sample/outputs/total_eligibility_audit.csv`
- `P1_Stage1_Coding_Sample/outputs/amendment_relationships.csv`

SHA-256:

`c7f288f5b8b0ed74ded0e2f17042ff63718a371bf18b3e8313a18c08d798b9d1`

This is a minimal data bridge, not the full Stage 1 project archive. It is included so Stage 2 can be inspected and rerun without distributing duplicate intermediate audit files.

## Derived outputs

The selected research sample and summary tables under `outputs/` are derived from public SEC filings. They are supplied to make the executed analysis inspectable. Missing values, refunds, and provisional eligibility statuses are retained rather than silently converted to zero or treated as confirmed observations.
