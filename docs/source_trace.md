# Source trace and changes

The development notebook `notebooks/02_tax_notes_exploration.ipynb` (152 cells)
is the code source. The latest HTML was inspected only as a saved-output reference;
none of its code was used to reconstruct or replace the notebook. Input hashes are
in `evidence/input_manifest.json`; paths there are relative to the original project.
`evidence/cell_provenance.json` maps every submission code cell to its development
cell (zero-based), or marks it new.

The actual `cash_tax_current` chain is development cell 37 (expanded extraction),
38 (iprx selection), 48/50 (original 10-K, FY, qtrs=4), 79/80/82 (standardized period
classification), 96/97/99/100 (category/current table), then 104/105 and 113–124
(DIM and jurisdiction diagnostics). Strict pivot/reconciliation is cell 130;
seven exceptions are exposed in 132. CAL is read in 136; positive Other adjustment
was coded in 145; geographic candidates in 150–151.

`filing_universe`, `coverage_10k`, `partial_scopes` and `total_eligibility` are not
defined in the latest development notebook. The HTML contains additional saved
coverage/export cells and the 1,159/2,340 result, absent from the supplied .ipynb.
These were inspected as a reference; the HTML did not reconstruct or replace the
source notebook. The existing Pilot CSV directory contains the first three
products, but their complete export/build code is absent from that notebook.
The submission implements explicit, visible construction/export calls
and reusable helpers. It does not claim that absent development definitions were
already reproducible. The supplied Pilot ZIP path does not exist; the unpacked
current Pilot files are fingerprinted individually.

The original 1,159 is independently reproduced from `cash_tax_current` by numeric
core Total, USD, dimn=0. This matches the saved filing-level coverage flag for every
accession. All four coverage flags, complete-four flag and coverage groups match;
`n_base_scopes` counts scopes with any core tag, including missing values. It is
written as an integer, with an explicit count of zero where no scope exists
(the prior export left that absent group blank).
It does not mean all any-period numeric Totals or all dimensioned Totals.

Submission changes: configurable relative paths; one chunked NUM extraction for the
selected concepts; independent duplicate assertions and metadata preservation;
retained final period/dimension/jurisdiction logic; removal of superseded previews;
complete output-generation code; signed CAL review; original Strict parity checks;
filing-level eligibility and amendment links; English methodology and documentation.
No mechanical notebook-to-script conversion was used.

The prior two `OTHER_RECONCILED` classifications are corrected to
`OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW` because their exact CAL arcs have negative=1.
Only the extended acceptance interpretation changes. The original 184 Strict rows,
four reported amounts, component sum and difference are verified unchanged.
Frozen reference values and prior decisions are retained, with their historical
claims explicitly separated from this freeze's accepted interpretations.

The prior iWallet precision-source flag is retained as a review item. `dcml=128`
is not a missing sentinel and is not rejected by the Decimal interval function.
The public filing page was readable through browser text extraction, but raw HTML
retrieval returned HTTP 403; its original decimals attribute remains unverified.
No additional source-confirmation claim is made.
