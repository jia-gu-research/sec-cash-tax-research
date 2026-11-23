# A1.8 — March Pilot Processing Rules

**Frozen 2026-11-11.** This rulebook applies to the pinned March ZIP and the
accompanying submission notebook. It is not evidence that another monthly dataset
satisfies the same duplicate or coverage conditions.

1. **Source and universe.** Use the public SEC Financial Statement and Notes Data
   Set, March 2026. Original filing universe: exact SUB `form == "10-K"`, 2,340
   unique accessions. A filing is the unit, not a unique firm-year across all EDGAR.
   Retain 10-K/A separately; do not select a later filing merely by date.
2. **Tables.** SUB supplies identity, form, period and metadata; NUM supplies
   reported standardized facts; TAG supplies `(tag, version)` definitions; DIM
   supplies `dimhash -> segments, segt`; CAL supplies parent/child tag-version arcs,
   group and weight. PRE/REN/TXT are not required to regenerate this frozen pilot.
   The two original-source snippet sets supplement flattened context information.
3. **Concepts.** Core tags are `IncomeTaxesPaidNet`,
   `IncomeTaxPaidFederalAfterRefundReceived`,
   `IncomeTaxPaidStateAndLocalAfterRefundReceived`, and
   `IncomeTaxPaidForeignAfterRefundReceived`. Discover `IncomeTaxPaidOther` tag names
   through TAG. Preserve four Other extension names as separate categories.
   The four names are `IncomeTaxPaidOther`, `IncomeTaxPaidOtherAfterRefundReceived`,
   `IncomeTaxPaidOtherAfterRefundReceivedTotal` and
   `IncomeTaxPaidOtherStateAndLocalAfterRefundReceived`.
4. **Versions.** Keep `version` in fact identity. Standard concept versions are
   retained; extensions remain filing-specific. Match CAL using parent and child
   versions. Never average or sum taxonomy versions; an ambiguous target selection
   receives review status. Eight concepts yield 11,860 raw records, including nine
   additional Other records beyond the 11,851 core records.
5. **Duplicates.** Seven-field candidate key: `adsh, tag, version, ddate, qtrs, uom,
   dimh`; NUM identity additionally includes `iprx`. Recompute all duplicate groups.
   Every observed group and singleton must have exactly one `iprx=0`. For numeric
   duplicates, require all declared-precision intervals to intersect and equal
   amounts at equal precision. Reject mixed missing/numeric or conflicting groups
   for review; do not choose an amount on proximity alone. Here 919 groups comprise
   894 direct selections, eight note-preservation cases, two joint-interval cases
   and 15 all-missing cases. Selected core facts: 10,917; all eight concepts: 10,926.
   Original NUM records remain separately exportable. The iprx rule is conditional
   pilot validation, not a universal SEC assertion.
6. **Periods.** Preserve the development pilot's rule: exact `form=10-K`, `fp=FY`,
   `qtrs=4`; current candidates require standardized `ddate=SUB.period`.
   Standardized gaps 365/731 days are comparative candidates; other nonzero gaps
   receive special review rather than being silently discarded. This historical
   gap classification is a pilot convention, not an exhaustive calendar model.
   Never exclude only because `fy` differs from the calendar year. Keep `datp` and
   `durp`. Original context dates are not reconstructed from them. In this ZIP,
   `datp` is measured in days and `durp` is a duration-proximity fraction.
7. **Units.** Retain original `uom`; do not infer geography from currency or apply
   exchange rates. Primary coverage and reconciliation summaries use USD. Long
   fact tables retain non-USD amounts and must be read with `uom`.
8. **Dimensions.** Join on `dimh=dimhash` with many-to-one validation. Strict scope
   includes the complete dimension hash. Primary filing-level Total additionally
   requires `dimn=0`, `dimh=0x00000000` and no `coreg` value. Dimensioned facts are
   retained, not automatically collapsed. DIM `segt` flags truncation of segments
   beyond 1024 characters; all 5,548 current rows have segt=0, asserted before
   geographic classification. `CA` geography is only a tag-context
   candidate; DomesticCountry address agreement is auxiliary inference.
9. **Missing and zero.** Preserve blank raw `value`; numeric conversion must have
   zero nonmissing conversion failures. Distinguish absent tag, present missing,
   explicit numeric zero and numeric nonzero. A reported zero or negative net
   payment is not automatically excluded. No component-based imputation.
10. **A — Strict reconciliation.** Same `adsh, ddate, qtrs, uom, dimh`, one fact per
    category, four numeric categories. Calculate
    `strict_difference = Total - Federal - StateLocal - Foreign`. The original 184
    scopes and all original amounts/differences remain unchanged: 177 exact, seven
    nonzero. Arithmetic equality does not certify universal semantic comparability.
11. **Extended reconciliation.** Consider separately disclosed Other concepts and
    appropriate geographic relationships with source support. Extended is not
    synonymous with rounding compatibility. Preserve Strict values independently;
    no diagnostic candidate changes reported Total. Accepted residual is
    `extended_difference = strict_difference - other_adjustment_usd - geo_accepted_sum`.
12. **CAL-guided Other.** Match filing, parent/child tags AND versions, exact NUM
    scope and reported value; inspect CAL sign and the full calculation group.
    `negative=1` means weight -1. Aveanna 3,444,000 and Tecnoglass 52,000 close the
    gaps if added positively, but both exact CAL arcs have weight -1. Register
    `OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW`; keep `other_adjustment_usd=0` and store
    `other_candidate_amount_usd`/`other_candidate_difference` separately. The prior
    `OTHER_RECONCILED` designation is preserved only in the frozen evidence record.
    Do not infer a valid additive accounting relationship from an arc's existence.
13. **B — Geographic component diagnostics.** Compare dimensioned candidate sums
    with a parent/core category or with a remaining gap within the same filing,
    standardized period and currency. Preserve concept/version/axis signature.
    Mixed axes, nested jurisdictions, Other buckets and entity scope can overlap.
    All resulting matches are numerical candidates: accepted geographic sum is
    zero throughout this freeze. ONE Group 726,000, Zumiez 1,287,000 and American
    Shared 679,000 are gap matches under source/hierarchy review. Smithfield's
    California 7m is detail of its State 19m, not an additional component.
    Partial disclosure is separate from both A and B.
14. **Decimals and precision.** For finite integer `d`, the closed round-to-nearest
    interval is `[v - 0.5*10**(-d), v + 0.5*10**(-d)]`. SEC `32767` represents INF
    and yields a point; `-32768` or absent metadata is not exponentiated. Finite
    `128` is mathematically valid. Preserve the prior iWallet source-verification
    flag until the original decimals attribute can be checked. Use Decimal
    arithmetic; never an arbitrary relative or dollar tolerance. A Total/components
    check compares Total's interval to the sum of the component intervals.
    This freeze implements the round-to-nearest diagnostic; it does not claim an
    actual rounding mode or full Calculations 1.1 validation. Smithfield is
    round-compatible, but truncation intervals `[124,125)` versus `[125,128)` million
    do not overlap. All six other original mismatches fail the round interval test.
15. **Exceptions.** Seven rows remain registered: Smithfield precision-compatible;
    ONE Group/Zumiez/American Shared geographic candidates; Aveanna/Tecnoglass
    Other/CAL-sign candidates; BigBear.ai semantic ambiguity. Numerical explanations
    are not confirmed causes. No exception is deleted or forced to reconcile.
16. **Research eligibility.** Audit all original 10-Ks. Priority of mutually exclusive
    statuses: no Total tag; all Total values missing; no current annual numeric
    Total; no USD candidate; dimensioned/entity-only; multiple target candidates;
    unsupported precision; unresolved prior precision-source flag; multiple original
    company-period filings; known semantic ambiguity; `ELIGIBLE_PROVISIONAL`.
    BigBear.ai is explicitly semantically ineligible while its zero is preserved.
    The 1,157 observations are provisional; no universal source verification is
    implied. Amendment links are diagnostic and not automatic exclusions.
17. **Limitations.** Flattened periods and dimensions do not establish exact context
    equality; retained nil/zero values need economic interpretation; threshold
    disclosures are incomplete; Other extensions and CAL directions can be
    ambiguous. Context evidence covers Smithfield and BigBear.ai, not every filing.
    No final research sample, regression, causal inference, paper replication or
    geographic-map extension is delivered in Stage 1.

## Definitions versus project choices

SEC supplies identities, standardized dates/durations, precision metadata, dimension
hashes and signed CAL relationships. XBRL supplies numerical duplicate and precision
concepts. Choosing four concepts, USD coverage, current-period filters, review flags,
provisional eligibility and diagnostic classifications are project rules, tested
for this snapshot. They are not SEC- or FASB-certified research eligibility rules.

## Methodological sources

- [SEC data and download page](https://www.sec.gov/data-research/sec-markets-data/financial-statement-notes-data-sets),
  its linked documentation, and the pinned ZIP's `readme.htm` (preferred for current field units).
- [XBRL Open Information Model 1.0, consistent duplicates](https://www.xbrl.org/Specification/oim/REC-2021-10-13/oim-REC-2021-10-13.html).
- [XBRL duplicate-fact Working Group Note, 2025](https://www.xbrl.org/WGN/xbrl-duplicates/WGN-2025-01-14/xbrl-duplicates-2025-01-14.html).
- [XBRL Calculations 1.1](https://www.xbrl.org/Specification/calculation-1.1/REC-2023-02-22%2Bcorrected-errata-2024-02-14/calculation-1.1-REC-2023-02-22%2Bcorrected-errata-2024-02-14.html).
- [FASB ASU 2023-09](https://storage.fasb.org/ASU%202023-09.pdf) and
  [FASB Income Taxes Taxonomy Implementation Guide, Example 2](https://xbrl.fasb.org/impdocs/IT_TIG/incometaxes.htm).
  The Implementation Guide is nonauthoritative modeling guidance.
