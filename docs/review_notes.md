# Review notes and interpretation boundaries

These notes are a portfolio-level companion. They do not revise the frozen
Stage 1 or Stage 2 files, numbers, code, dictionaries or original audit records.

## Stage 1 — why the result remains CONDITIONAL PASS

The reviewed package supports data-construction and QA claims: 2,340 original
10-Ks; 1,159 raw Total coverage; 1,157 provisionally eligible Totals; 184 Strict
scopes with 177 exact matches and seven exceptions. The provisional count must
not be described as a fully source-confirmed final research sample.

- Aveanna and Tecnoglass retain unaccepted Other candidates. The source CAL flag
  is `negative=1`, corresponding to a weight of **-1**. The accepted Other
  adjustment is zero in both cases.
- A wording clarification is necessary when reading the frozen README's phrase
  about “subtracting” the Other amount: the candidate residual is
  `Strict difference - positive Other amount`. This is equivalent to hypothetically
  adding Other to the component sum; it is **not** evidence that applying the
  negative CAL weight reconciles the components. The frozen rulebook and code
  preserve this distinction. No sign issue is treated as resolved here.
- Smithfield is rounding-compatible, not rounding-confirmed; California is not
  added again to State. The three geographic gap matches remain candidates.
- BigBear.ai's reported zero is retained with a semantic exclusion. iWallet's
  reported zero is retained while its precision-source verification remains open.
- Exact original context and economic scope are not verified for all observations.

Saved execution counters and JSON reports support the historical execution claim;
they are distinct from a fresh independent run. New working-copy execution and
CSV parity evidence, when supplied in `verification/`, are labeled separately.

## Stage 2 — what has and has not been replicated

This is an **analogous, preliminary extensive-margin regression**, inspired by
the paper's question. It is not a reproduction of Table 5, a complete empirical
replication, or a causal test of why loss firms pay taxes.

The matching and sample construction retain the Stage 1 reported values and
exclusions. Standardized date and duration proximity fields, zero dimensions and
primary-statement checks reduce incompatible matches, but do not establish
universal original-context equivalence.

The 141-observation primary model uses strict broad total revenue. Its sample is
selected by disclosure and successful matching; the larger customer-contract
revenue proxy sample is supplementary. The paper-aligned screening exercise is
only partial and its 79-observation model is not estimated under the declared
outcome-count rule.

The original paper uses a multi-year Compustat sample, additional tax-accounting
determinants, industry/year effects, and a different SIZE measure. The present
log-variable coefficients and taxpaying shares cannot be claimed to reproduce
the original estimates. See Stage 2's `replication_comparison.md` for the detailed
definition-by-definition comparison.

## What changed during portfolio assembly

Only the outer presentation and integration layer was added: the project README,
offline review entry point, reading/reproduction instructions, these notes,
cross-stage verification, and working-copy runners. The two stage snapshots are
byte-identical to their input archives. Stage 2's original ZIP is represented by
its unpacked files and source hash; Stage 1's ZIP is additionally retained because
Stage 2 requires its exact bytes as an input.

The final package contains neither private credentials nor runtime environments,
machine-specific kernel registrations, test working copies, or the large raw SEC
ZIP. Historical file paths remain inside the preserved audit material as provenance.
