# Data dictionary

This dictionary covers **every column in every generated output CSV**. Original
reported facts, SEC-standardized representations, derived calculations, diagnostic
candidates and provisional analytical variables have distinct classes. The same
field name has the same core meaning across files; table-specific scope is stated below.

## Core concepts and conventions

`TOTAL` = `IncomeTaxesPaidNet`; `FEDERAL` = `IncomeTaxPaidFederalAfterRefundReceived`;
`STATE_LOCAL` = `IncomeTaxPaidStateAndLocalAfterRefundReceived`;
`FOREIGN` = `IncomeTaxPaidForeignAfterRefundReceived`. Other concepts remain
`OTHER_CUSTOM::<tag>`. Preserve taxonomy version; diagnostic sums never overwrite facts.

Fact identity: `adsh, tag, version, ddate, qtrs, uom, dimh, iprx`.
Strict scope: `adsh, ddate, qtrs, uom, dimh`. Current pilot: original 10-K,
`fp=FY`, `qtrs=4`, `ddate=SUB.period`. Exact original context dates are available
only where preserved evidence exists. Filing rows are unique by accession.

Amounts ending in `_usd` are USD calculations/projections in their table. Raw
`value`, `value_num` and duplicate intervals use row `uom`, which can be non-USD.
Blank monetary values mean missing/not selected, never zero. Explicit numeric zero
is retained. A derived zero residual is arithmetic equality; a zero accepted
adjustment means no adjustment approved. Neither establishes an economic fact.

`segt` is SEC DIM metadata, not a region label. `durp` is a fraction and `datp`
is days in the pinned ZIP. `verified_other_tag` retains a historical field name:
the current signed-CAL interpretation is in `other_relationship_status`, not that name.

## Output grains and complete schemas

### `amendment_relationships.csv`

Grain: one 10-K/A accession, outside the original 10-K universe.

`amendment_adsh`, `cik`, `period`, `filed`, `original_accessions_json`, `link_status`, `replacement_applied`

### `cal_arcs_seven_filings.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `grp`, `arc`, `negative`, `ptag`, `pversion`, `ctag`, `cversion`

### `cash_tax_comparative_facts.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`, `form`, `period`, `fy`, `fp`, `ddate_month`, `period_month`, `period_relation`, `period_date`, `ddate_date`, `gap_days`, `period_type`, `cik`, `ddate_year`, `fy_num`, `fy_offset`, `fye`, `tax_type`

### `cash_tax_exception_log.csv`

Grain: one accession/date/duration/unit/complete dimension scope (seven exceptions are a subset).

`adsh`, `ddate`, `qtrs`, `uom`, `dimh`, `reported_total_usd`, `federal_usd`, `state_local_usd`, `foreign_usd`, `strict_component_sum`, `strict_difference`, `other_adjustment_usd`, `other_candidate_amount_usd`, `other_cal_weight`, `other_relationship_status`, `verified_other_tag`, `verified_other_version`, `difference_after_other`, `other_candidate_difference`, `n_geo_facts`, `n_geo_numeric`, `geo_candidate_sum`, `geo_accepted_sum`, `geo_review_status`, `extended_difference`, `geo_candidate_closes_gap`, `rounding_tolerance`, `rounding_compatible`, `rounding_tested`, `rounding_confirmed`, `reported_total_fact_status`, `analytical_total_usd`, `total_semantic_status`, `source_10k_url`, `evidence_note`, `qa_status`, `source_accession`, `source_dataset`

### `cash_tax_facts_current_long.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`, `form`, `period`, `fy`, `fp`, `ddate_month`, `period_month`, `period_relation`, `period_date`, `ddate_date`, `gap_days`, `period_type`, `cik`, `ddate_year`, `fy_num`, `fy_offset`, `fye`, `tax_type`, `dimhash`, `segments`, `segt`, `dim_match`, `income_tax_authority_member`, `geographical_member`, `has_segments`, `has_income_tax_authority`, `has_geographical`, `authority_class`, `authority_name_member`, `jurisdiction_id`, `jurisdiction_source`, `countryba`, `countryinc`, `stprba`, `stprinc`, `_sub_match`, `inferred_country_id`

### `cash_tax_qa_summary.csv`

Grain: one named coverage measure, eligibility class, QA class or cumulative bridge stage.

`qa_status`, `n_scopes`

### `cash_tax_raw_selected_concepts.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`

### `cash_tax_reconciliation_184.csv`

Grain: one accession/date/duration/unit/complete dimension scope (seven exceptions are a subset).

`adsh`, `ddate`, `qtrs`, `uom`, `dimh`, `reported_total_usd`, `federal_usd`, `state_local_usd`, `foreign_usd`, `strict_component_sum`, `strict_difference`, `other_adjustment_usd`, `other_candidate_amount_usd`, `other_cal_weight`, `other_relationship_status`, `verified_other_tag`, `verified_other_version`, `difference_after_other`, `other_candidate_difference`, `n_geo_facts`, `n_geo_numeric`, `geo_candidate_sum`, `geo_accepted_sum`, `geo_review_status`, `extended_difference`, `geo_candidate_closes_gap`, `rounding_tolerance`, `rounding_compatible`, `rounding_tested`, `rounding_confirmed`, `reported_total_fact_status`, `analytical_total_usd`, `total_semantic_status`, `source_10k_url`, `evidence_note`, `qa_status`, `source_accession`, `source_dataset`

### `cash_tax_selected_all_periods.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`

### `cash_tax_special_period_facts.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`, `form`, `period`, `fy`, `fp`, `ddate_month`, `period_month`, `period_relation`, `period_date`, `ddate_date`, `gap_days`, `period_type`, `cik`, `ddate_year`, `fy_num`, `fy_offset`, `fye`, `tax_type`

### `coverage_summary.csv`

Grain: one named coverage measure, eligibility class, QA class or cumulative bridge stage.

`measure`, `n_filings`, `denominator`, `coverage_rate`

### `duplicate_fact_audit.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `amount_status`, `decision`, `selected_iprx0`

### `duplicate_group_qa.csv`

Grain: one seven-key duplicate group.

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `n_records`, `iprx_distribution`, `amount_status`, `decision`, `intersection_low`, `intersection_high`, `group_footnotes_json`, `values_json`, `dcml_json`

### `filing_coverage_10k.csv`

Grain: one original 10-K accession (exclusion log is a subset).

`adsh`, `cik`, `name`, `sic`, `fy`, `fp`, `period`, `filed`, `form`, `has_total`, `has_federal`, `has_state_local`, `has_foreign`, `has_complete_four`, `n_base_scopes`, `coverage_group`

### `geographic_all_candidates.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`, `form`, `period`, `fy`, `fp`, `ddate_month`, `period_month`, `period_relation`, `period_date`, `ddate_date`, `gap_days`, `period_type`, `cik`, `ddate_year`, `fy_num`, `fy_offset`, `fye`, `tax_type`, `dimhash`, `segments`, `segt`, `dim_match`, `income_tax_authority_member`, `geographical_member`, `has_segments`, `has_income_tax_authority`, `has_geographical`, `authority_class`, `authority_name_member`, `jurisdiction_id`, `jurisdiction_source`, `countryba`, `countryinc`, `stprba`, `stprinc`, `_sub_match`, `inferred_country_id`, `axis_key`, `dimension_class`

### `geographic_gap_candidates.csv`

Grain: exception accession/date/duration/unit/axis signature.

`adsh`, `ddate`, `qtrs`, `uom`, `axis_key`, `n_components`, `n_numeric_components`, `component_sum_usd`, `difference_after_other`, `numeric_gap_match`, `review_status`

### `geographic_relations.csv`

Grain: accession/date/duration/unit/category/tag/version/complete axis signature.

`adsh`, `ddate`, `qtrs`, `uom`, `tax_type`, `tag`, `version`, `axis_key`, `n_geo_facts`, `n_geo_numeric`, `geo_sum_usd`, `parent_value_usd`, `parent_fact_match`, `relation_status`, `accounting_relationship_confirmed`, `interpretation`

### `march_pilot_exception_register.csv`

Grain: one accession/date/duration/unit/complete dimension scope (seven exceptions are a subset).

`adsh`, `ddate`, `qtrs`, `uom`, `dimh`, `reported_total_usd`, `federal_usd`, `state_local_usd`, `foreign_usd`, `strict_component_sum`, `strict_difference`, `other_adjustment_usd`, `other_candidate_amount_usd`, `other_cal_weight`, `other_relationship_status`, `verified_other_tag`, `verified_other_version`, `difference_after_other`, `other_candidate_difference`, `n_geo_facts`, `n_geo_numeric`, `geographic_candidate_amount`, `geo_accepted_sum`, `geo_review_status`, `extended_difference`, `geo_candidate_closes_gap`, `rounding_tolerance`, `rounding_compatible`, `rounding_tested`, `rounding_confirmed`, `reported_total_fact_status`, `analytical_total_usd`, `semantic_status`, `source_10k_url`, `evidence_note`, `final_classification`, `source_accession`, `source_dataset`, `company`, `rounding_status`, `evidence_source`, `unresolved_issue`, `accounting_geo_relationship_confirmed`

### `other_cal_relations.csv`

Grain: one NUM representation with source identity; see selection suffix (raw/selected/current/comparative/special).

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`, `form`, `period`, `fy`, `fp`, `ddate_month`, `period_month`, `period_relation`, `period_date`, `ddate_date`, `gap_days`, `period_type`, `cik`, `ddate_year`, `fy_num`, `fy_offset`, `fye`, `tax_type`, `dimhash`, `segments`, `segt`, `dim_match`, `income_tax_authority_member`, `geographical_member`, `has_segments`, `has_income_tax_authority`, `has_geographical`, `authority_class`, `authority_name_member`, `jurisdiction_id`, `jurisdiction_source`, `countryba`, `countryinc`, `stprba`, `stprinc`, `_sub_match`, `inferred_country_id`, `n_cal_arcs`, `cal_weight`, `cal_status`, `pilot_verified`

### `partial_disclosure_scopes.csv`

Grain: one accession/date/duration/unit/complete dimension scope (seven exceptions are a subset).

`adsh`, `ddate`, `qtrs`, `uom`, `dimh`, `total_usd`, `total_status`, `federal_usd`, `federal_status`, `state_local_usd`, `state_local_status`, `foreign_usd`, `foreign_status`, `n_core_tags`, `n_core_numeric`, `disclosure_class`

### `total_eligibility_audit.csv`

Grain: one original 10-K accession (exclusion log is a subset).

`adsh`, `cik`, `company`, `form`, `filed`, `fy`, `fp`, `period`, `fye`, `total_tag_present`, `numeric_total_any_period`, `raw_numeric_total_coverage`, `total_fact_count`, `total_raw_num_count`, `annual_current_numeric_count`, `usd_current_numeric_count`, `target_total_candidate_count`, `reported_total_usd`, `reported_zero`, `total_tag`, `period_status`, `currency_status`, `dimension_status`, `duplicate_status`, `semantic_status`, `eligibility_status`, `analysis_eligible`, `analytical_total_usd`, `exclusion_reason`, `amendment_status`, `related_amendments_json`, `same_cik_period_originals_json`, `original_context_start`, `original_context_end`, `source_10k_url`, `context_verification_status`, `fy_calendar_label_mismatch`, `all_total_fact_identities_json`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `dcml`, `dimn`, `coreg`, `durp`, `datp`, `footnote`, `duplicate_footnotes_json`, `duplicate_interval_low`, `duplicate_interval_high`

### `total_eligibility_count_bridge.csv`

Grain: one named coverage measure, eligibility class, QA class or cumulative bridge stage.

`stage`, `n_filings`, `reduction_from_previous`, `definition`

### `total_eligibility_summary.csv`

Grain: one named coverage measure, eligibility class, QA class or cumulative bridge stage.

`eligibility_status`, `n_filings`, `n_reported_zero`, `share_of_original_10k`

### `total_exclusion_log.csv`

Grain: one original 10-K accession (exclusion log is a subset).

`adsh`, `cik`, `company`, `form`, `filed`, `fy`, `fp`, `period`, `fye`, `total_tag_present`, `numeric_total_any_period`, `raw_numeric_total_coverage`, `total_fact_count`, `total_raw_num_count`, `annual_current_numeric_count`, `usd_current_numeric_count`, `target_total_candidate_count`, `reported_total_usd`, `reported_zero`, `total_tag`, `period_status`, `currency_status`, `dimension_status`, `duplicate_status`, `semantic_status`, `eligibility_status`, `analysis_eligible`, `analytical_total_usd`, `exclusion_reason`, `amendment_status`, `related_amendments_json`, `same_cik_period_originals_json`, `original_context_start`, `original_context_end`, `source_10k_url`, `context_verification_status`, `fy_calendar_label_mismatch`, `all_total_fact_identities_json`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `dcml`, `dimn`, `coreg`, `durp`, `datp`, `footnote`, `duplicate_footnotes_json`, `duplicate_interval_low`, `duplicate_interval_high`

### `total_fact_candidates.csv`

Grain: one selected seven-key Total fact across all periods/scopes.

`adsh`, `tag`, `version`, `ddate`, `qtrs`, `uom`, `dimh`, `iprx`, `value`, `footnote`, `footlen`, `dimn`, `coreg`, `durp`, `datp`, `dcml`, `duplicate_interval_low`, `duplicate_interval_high`, `duplicate_footnotes_json`, `value_num`, `period`, `fp`, `form`, `is_current_annual`, `is_usd`, `is_dimensionless`, `decision`, `amount_status`

## Field definitions

Each row provides economic meaning, tags, source, unit, formula and QA. The period
and dimension conventions above apply to each field unless its definition explicitly
narrows them. Missing and zero conventions apply to every row. A machine-readable
version repeats all these dimensions for every variable in
`evidence/output_variable_dictionary.csv` (including the files where it appears).

| Variable | Class; economic meaning | Tags; source; unit | Formula / QA |
|---|---|---|---|
| `_sub_match` | Derived diagnostic: SUB address-information merge status | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Many-to-one merge indicator. QA: Retain provenance; no inference beyond stated definition |
| `accounting_geo_relationship_confirmed` | Derived indicator: Economic geographic hierarchy source-confirmed; False throughout | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `accounting_relationship_confirmed` | Derived indicator: Economic parent/children hierarchy source-confirmed; False throughout | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `adsh` | Original filing metadata: SEC filing accession, retained as text including leading zeros | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB/NUM accession; filing join key. QA: Retain provenance; no inference beyond stated definition |
| `all_total_fact_identities_json` | Derived filing QA: Source identities of every selected Total representation in the filing | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | JSON list of seven-key fields plus iprx; amounts in total_fact_candidates.csv. QA: Retain provenance; no inference beyond stated definition |
| `amendment_adsh` | Derived filing QA: Accession of an original 10-K/A SUB record, not part of 2,340 universe | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Direct SUB accession for form 10-K/A. QA: Retain provenance; no inference beyond stated definition |
| `amendment_status` | Derived filing QA: Relationship to same-CIK/period 10-K/A in this monthly ZIP | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Link retained for review; never substitutes amendment values. QA: Retain provenance; no inference beyond stated definition |
| `amount_status` | Derived duplicate QA: Numerical relationship between repeated representations | row tag/version or selected core concept family; NUM; row uom / JSON / category | SAME_VALUE, PRECISION_COMPATIBLE, ALL_MISSING or SINGLETON. QA: Retain provenance; no inference beyond stated definition |
| `analysis_eligible` | Derived indicator: Final status is ELIGIBLE_PROVISIONAL, not universal economic confirmation | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `analytical_total_usd` | Provisional analytical variable: Total retained only after the table-specific eligibility/semantic screen; still provisional | IncomeTaxesPaidNet; NUM + conditional QA / review; USD | Eligibility audit: reported Total if analysis_eligible else blank; reconciliation table: blank for known BigBear ambiguity. QA: Retain provenance; no inference beyond stated definition |
| `annual_current_numeric_count` | Derived count: Numeric Total facts with fp FY, qtrs4 and standardized current period | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `arc` | Standardized calculation relationship: Sequential arc number within calculation group | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL arc. QA: Retain provenance; no inference beyond stated definition |
| `authority_class` | Derived diagnostic: Broad jurisdiction or CA-context candidate label | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Final development cell 120 rules; not confirmed economic geography. QA: Retain provenance; no inference beyond stated definition |
| `authority_name_member` | Derived diagnostic: Named tax authority member, distinct from authority axis | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Regex extract IncomeTaxAuthorityName=([^;]+). QA: Retain provenance; no inference beyond stated definition |
| `axis_key` | Derived diagnostic: Sorted signature of all flattened dimension axis names | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Split segments by semicolon, collect names before equals, sort/join. QA: Retain provenance; no inference beyond stated definition |
| `cal_status` | QA classification / source evidence: Signed CAL review status for candidate Other facts | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Exact tag/version/scope match plus sign review. QA: Retain provenance; no inference beyond stated definition |
| `cal_weight` | QA classification / source evidence: Signed CAL weight for a preserved Other fact | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | negative=1 -> -1; negative=0 -> +1. QA: Retain provenance; no inference beyond stated definition |
| `cik` | Original filing metadata: SEC registrant identifier; not a unique fiscal-period observation | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB cik. QA: Retain provenance; no inference beyond stated definition |
| `company` | Original filing metadata: Registrant name attached to an audit or exception | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | SUB name joined by adsh. QA: Retain provenance; no inference beyond stated definition |
| `component_sum_usd` | Diagnostic candidate: Geographic component sum within an exception and axis signature | dimensioned core concepts; NUM + conditional QA / review; USD | Sum min_count=1; numeric match requires every component numeric. QA: Retain provenance; no inference beyond stated definition |
| `context_verification_status` | Derived filing QA: Whether exact context evidence is available in this package | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | PRESERVED_ORIGINAL_INLINE_EVIDENCE for two filings; otherwise not available in flat NUM. QA: Retain provenance; no inference beyond stated definition |
| `coreg` | Standardized SEC fact: Co-registrant/entity qualifier; not a tax jurisdiction | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM coreg; primary Total requires blank. QA: Retain provenance; no inference beyond stated definition |
| `countryba` | Original filing metadata: Business-address country; not economic tax domicile | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB countryba. QA: Retain provenance; no inference beyond stated definition |
| `countryinc` | Original filing metadata: Country of incorporation; not proof of tax residence | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB countryinc. QA: Retain provenance; no inference beyond stated definition |
| `coverage_group` | Derived filing QA: Mutually exclusive filing coverage label, distinct from research eligibility | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | COMPLETE_FOUR > TOTAL_AVAILABLE > COMPONENTS_WITHOUT_TOTAL > NO_BASE_CORE_NUMERIC. QA: Retain provenance; no inference beyond stated definition |
| `coverage_rate` | Derived ratio: n_filings / denominator for a coverage measure | row tag/version or selected core concept family; SUB + grouped counts; fraction | n_filings / denominator for a coverage measure. QA: 0 to 1; disjoint final eligibility shares sum to 1 |
| `ctag` | Standardized calculation relationship: Calculation arc child concept name | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL ctag. QA: Retain provenance; no inference beyond stated definition |
| `currency_status` | Derived filing QA: Whether current annual numeric Total is in USD | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | USD_AVAILABLE, non-USD/missing unit, or no numeric current candidate. QA: Retain provenance; no inference beyond stated definition |
| `cversion` | Standardized calculation relationship: Calculation arc child concept version | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL cversion; match NUM version exactly. QA: Retain provenance; no inference beyond stated definition |
| `datp` | Standardized SEC fact: SEC date proximity in days in this ZIP | row tag/version or selected core concept family; NUM; days | Direct NUM datp; not an exact context date. QA: Retain provenance; no inference beyond stated definition |
| `dcml` | Standardized SEC fact: XBRL decimals precision; 32767 means INF; finite 128 is not intrinsically invalid | row tag/version or selected core concept family; NUM; decimal-place exponent; 32767=INF | Direct NUM dcml; -32768 or absent metadata is not exponentiated. QA: Retain provenance; no inference beyond stated definition |
| `dcml_json` | Derived duplicate QA: All original decimal metadata in the duplicate group | row tag/version or selected core concept family; NUM; row uom / JSON / category | JSON list of dcml strings. QA: Retain provenance; no inference beyond stated definition |
| `ddate` | Standardized SEC fact: SEC standardized fact end date; not exact original context end | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM ddate. QA: Retain provenance; no inference beyond stated definition |
| `ddate_date` | Derived diagnostic: Parsed standardized NUM end timestamp | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | to_datetime(ddate, format=%Y%m%d). QA: Retain provenance; no inference beyond stated definition |
| `ddate_month` | Derived diagnostic: Year/month portion of standardized fact end date | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | ddate[:6]. QA: Retain provenance; no inference beyond stated definition |
| `ddate_year` | Derived diagnostic: Calendar-year portion of standardized NUM end | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Numeric ddate[:4]. QA: Retain provenance; no inference beyond stated definition |
| `decision` | Derived duplicate QA: Conditional default-representation selection and preservation rule | row tag/version or selected core concept family; NUM; row uom / JSON / category | Numeric pass, preserve annotations, preserve interval, all-missing marker, or singleton. QA: Retain provenance; no inference beyond stated definition |
| `definition` | Derived filing QA: Plain-language bridge inclusion rule | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Written description of the stage's cumulative selection. QA: Retain provenance; no inference beyond stated definition |
| `denominator` | Derived count: Original 10-K universe size, 2,340 | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `difference_after_other` | Derived diagnostic: Residual after accepted Other adjustments only | core + accepted Other; NUM + conditional QA / review; USD | strict_difference - other_adjustment_usd. QA: Retain provenance; no inference beyond stated definition |
| `dim_match` | Derived diagnostic: DIM merge cardinality/status diagnostic | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Many-to-one merge indicator. QA: Retain provenance; no inference beyond stated definition |
| `dimension_class` | Derived diagnostic: Diagnostic dimension classification | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | DIMENSIONED_CANDIDATE; no acceptance of economic hierarchy. QA: Retain provenance; no inference beyond stated definition |
| `dimension_status` | Derived filing QA: Whether a dimensionless entity-unqualified target Total exists | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | No candidate, dimensioned/coreg-only or dimensionless available. QA: Retain provenance; no inference beyond stated definition |
| `dimh` | Standardized SEC fact: SEC dimension hash identifying the complete flattened dimension scope | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM dimh; join DIM dimhash. QA: Retain provenance; no inference beyond stated definition |
| `dimhash` | Standardized dimension metadata: DIM key describing an observed complete dimension scope | Dimension metadata for the fact tag/version; no separate cash-tax concept; DIM; hash/text/boolean | Direct DIM dimhash; many-to-one join from dimh. QA: Retain provenance; no inference beyond stated definition |
| `dimn` | Standardized SEC fact: Count of reported dimensions | row tag/version or selected core concept family; NUM; dimension count | Direct NUM dimn; zero required for primary Total. QA: Retain provenance; no inference beyond stated definition |
| `disclosure_class` | Derived scope classification: Number of numeric core categories; separate from tag count and eligibility | row tag/version or selected core concept family; NUM; category | NUMERIC_ + n_core_numeric. QA: Numeric categories counted from four core concepts only |
| `duplicate_footnotes_json` | Derived duplicate QA: Footnotes retained from all representations when annotation preservation is needed | row tag/version or selected core concept family; NUM; row uom / JSON / category | Distinct group footnotes in preservation groups; original footnote retained separately. QA: Retain provenance; no inference beyond stated definition |
| `duplicate_interval_high` | Derived duplicate QA: Upper bound of preserved narrower joint precision interval | row tag/version or selected core concept family; NUM; original row uom | Min of all duplicate fact interval upper bounds for interval-preservation groups. QA: Retain provenance; no inference beyond stated definition |
| `duplicate_interval_low` | Derived duplicate QA: Lower bound of preserved narrower joint precision interval | row tag/version or selected core concept family; NUM; original row uom | max of all duplicate fact interval lower bounds for interval-preservation groups. QA: Retain provenance; no inference beyond stated definition |
| `duplicate_status` | Derived filing QA: Selected Total representation duplicate-QA decision | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Prior recomputed decision if duplicate; SINGLETON otherwise; no fact if none selected. QA: Retain provenance; no inference beyond stated definition |
| `durp` | Standardized SEC fact: SEC duration proximity fraction relative to whole-quarter duration | row tag/version or selected core concept family; NUM; fraction of standardized duration | Direct NUM durp; do not treat it as days. QA: Retain provenance; no inference beyond stated definition |
| `eligibility_status` | Derived filing QA: Mutually exclusive filing-level final eligibility/review/exclusion status | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Priority order in rulebook; only ELIGIBLE_PROVISIONAL sets analysis_eligible. QA: Retain provenance; no inference beyond stated definition |
| `evidence_note` | QA classification / source evidence: Plain-language record of preserved evidence and limitations | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Original review note; corrected Other sign interpretation where necessary. QA: Retain provenance; no inference beyond stated definition |
| `evidence_source` | QA classification / source evidence: Evidence locator for exception decision | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Original 10-K URL or SEC ZIP CAL/NUM/README locator. QA: Retain provenance; no inference beyond stated definition |
| `exclusion_reason` | Derived filing QA: Understandable reason for each noneligible or review filing | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Status-specific reason; blank only for provisional eligible. QA: Retain provenance; no inference beyond stated definition |
| `extended_difference` | Derived diagnostic: Residual after accepted Other and geographic adjustments | core + accepted extensions; NUM + conditional QA / review; USD | strict_difference - other_adjustment_usd - geo_accepted_sum. QA: Retain provenance; no inference beyond stated definition |
| `federal_status` | Derived disclosure classification: ABSENT_TAG, PRESENT_MISSING, REPORTED_ZERO or REPORTED_NONZERO for the named core category | row tag/version or selected core concept family; NUM; category | Check tag presence first, then raw numeric missingness, then exact zero. QA: Absent/missing never relabeled as zero |
| `federal_usd` | Reported fact projection: USD net federal/national income taxes paid | IncomeTaxPaidFederalAfterRefundReceived; NUM + conditional QA / review; USD | Selected federal fact. QA: Retain provenance; no inference beyond stated definition |
| `filed` | Original filing metadata: SEC filing date | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB filed. QA: Retain provenance; no inference beyond stated definition |
| `final_classification` | QA classification / source evidence: Exception-register alias of qa_status | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Same signed-CAL-aware classification. QA: Retain provenance; no inference beyond stated definition |
| `footlen` | Standardized SEC fact: Length of original linked footnote metadata | row tag/version or selected core concept family; NUM; text length | Direct NUM footlen. QA: Retain provenance; no inference beyond stated definition |
| `footnote` | Standardized SEC fact: Original NUM linked footnote text | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM footnote; keep alongside consolidated duplicate notes. QA: Retain provenance; no inference beyond stated definition |
| `foreign_status` | Derived disclosure classification: ABSENT_TAG, PRESENT_MISSING, REPORTED_ZERO or REPORTED_NONZERO for the named core category | row tag/version or selected core concept family; NUM; category | Check tag presence first, then raw numeric missingness, then exact zero. QA: Absent/missing never relabeled as zero |
| `foreign_usd` | Reported fact projection: USD net foreign income taxes paid | IncomeTaxPaidForeignAfterRefundReceived; NUM + conditional QA / review; USD | Selected foreign fact. QA: Retain provenance; no inference beyond stated definition |
| `form` | Original filing metadata: Original SEC submission form; exact 10-K defines the original universe | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB form. QA: Retain provenance; no inference beyond stated definition |
| `fp` | Original filing metadata: Filer fiscal period label; FY required by pilot annual filter | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB fp. QA: Retain provenance; no inference beyond stated definition |
| `fy` | Original filing metadata: Filer fiscal-year label, not calendar year of NUM end date | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB fy. QA: Retain provenance; no inference beyond stated definition |
| `fy_calendar_label_mismatch` | Derived indicator: Fiscal-year label differs from SUB period calendar year; flag only, not exclusion | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `fy_num` | Derived diagnostic: Numeric representation of SUB fiscal-year label | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | to_numeric(fy). QA: Retain provenance; no inference beyond stated definition |
| `fy_offset` | Derived diagnostic: Fiscal-year label less standardized fact calendar year; diagnostic only | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | fy_num - ddate_year. QA: Retain provenance; no inference beyond stated definition |
| `fye` | Original filing metadata: Filer fiscal year-end month/day metadata | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB fye. QA: Retain provenance; no inference beyond stated definition |
| `gap_days` | Derived diagnostic: Difference between standardized SUB period and NUM end | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; days | period_date - ddate_date, in days. QA: Retain provenance; no inference beyond stated definition |
| `geo_accepted_sum` | Derived accepted adjustment: Source/hierarchy-accepted geographic addition; none accepted in this freeze | dimensioned selected cash-tax concepts; NUM + conditional QA / review; USD | 0 under frozen review decisions. QA: Retain provenance; no inference beyond stated definition |
| `geo_candidate_closes_gap` | Derived indicator: Unaccepted geographic sum equals nonzero residual after accepted Other adjustment | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `geo_candidate_sum` | Diagnostic candidate: Unaccepted sum of dimensioned USD candidates for the same filing/period/currency | dimensioned selected core concepts; NUM + conditional QA / review; USD | Sum across candidate dimension hashes, min_count=1; can overlap economically. QA: Retain provenance; no inference beyond stated definition |
| `geo_review_status` | QA classification / source evidence: Status of candidate geographic hierarchy review | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | PENDING_HIERARCHY_REVIEW or NO_GEO_CANDIDATES. QA: Retain provenance; no inference beyond stated definition |
| `geo_sum_usd` | Diagnostic candidate: Sum of geographic candidates by exact tag/version and axis signature | row tag/version; NUM + conditional QA / review; USD | Group sum with min_count=1; incomplete values flagged. QA: Retain provenance; no inference beyond stated definition |
| `geographic_candidate_amount` | Diagnostic candidate: Exception-register alias of geo_candidate_sum | dimensioned selected core concepts; NUM + conditional QA / review; USD | Same unaccepted candidate sum. QA: Retain provenance; no inference beyond stated definition |
| `geographical_member` | Derived diagnostic: Flattened Geographical axis member candidate | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Regex extract Geographical=([^;]+). QA: Retain provenance; no inference beyond stated definition |
| `group_footnotes_json` | Derived duplicate QA: Distinct original group footnotes; absence is not a statement that disclosure has no mechanism | row tag/version or selected core concept family; NUM; row uom / JSON / category | JSON list from all raw duplicate representations. QA: Retain provenance; no inference beyond stated definition |
| `grp` | Standardized calculation relationship: SEC calculation relationship group within the accession | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL grp. QA: Retain provenance; no inference beyond stated definition |
| `has_complete_four` | Derived indicator: All four dimensionless USD numeric core categories available in the filing | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_federal` | Derived indicator: At least one current annual dimensionless USD numeric Federal fact | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_foreign` | Derived indicator: At least one current annual dimensionless USD numeric Foreign fact | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_geographical` | Derived indicator: Geographical axis member was extracted | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_income_tax_authority` | Derived indicator: IncomeTaxAuthority axis member was extracted | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_segments` | Derived indicator: DIM segments is nonmissing; not proof of a geographic axis | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_state_local` | Derived indicator: At least one current annual dimensionless USD numeric State/Local fact | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `has_total` | Derived indicator: At least one current annual dimensionless USD numeric Total under original coverage rule | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `income_tax_authority_member` | Derived diagnostic: Flattened IncomeTaxAuthority axis member candidate | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Regex extract IncomeTaxAuthority=([^;]+). QA: Retain provenance; no inference beyond stated definition |
| `inferred_country_id` | Derived diagnostic: Auxiliary country inference for DomesticCountry only | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Business and incorporation country must both be present and equal. QA: Retain provenance; no inference beyond stated definition |
| `interpretation` | QA classification / source evidence: Conservative interpretation of geographic relation output | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Candidate only; overlap and scope require original source review. QA: Retain provenance; no inference beyond stated definition |
| `intersection_high` | Derived duplicate QA: Joint duplicate precision interval upper bound | row tag/version or selected core concept family; NUM; original row uom | min(interval upper bounds) using Decimal. QA: Retain provenance; no inference beyond stated definition |
| `intersection_low` | Derived duplicate QA: Joint duplicate precision interval lower bound | row tag/version or selected core concept family; NUM; original row uom | max(interval lower bounds) using Decimal. QA: Retain provenance; no inference beyond stated definition |
| `iprx` | Standardized SEC fact: SEC priority/disambiguation index within otherwise repeated seven-key facts | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM iprx; default zero selected only after group QA. QA: Retain provenance; no inference beyond stated definition |
| `iprx_distribution` | Derived duplicate QA: All disambiguation indices observed in a duplicate group | row tag/version or selected core concept family; NUM; row uom / JSON / category | JSON list of group iprx values. QA: Retain provenance; no inference beyond stated definition |
| `is_current_annual` | Derived indicator: fp=FY, qtrs=4 and standardized NUM ddate equals SUB.period | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `is_dimensionless` | Derived indicator: dimn=0 and dimh=0x00000000 and coreg missing | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `is_usd` | Derived indicator: Original NUM uom exactly USD | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `jurisdiction_id` | Derived diagnostic: Tag-context geographic identifier candidate | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | State code with STATE_LOCAL -> US-code; country code with FOREIGN -> code; named California authority fallback. QA: Retain provenance; no inference beyond stated definition |
| `jurisdiction_source` | Derived diagnostic: Rule supplying jurisdiction_id; retains uncertainty | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | TAG_CONTEXT or NAMED_AUTHORITY_CANDIDATE; UNRESOLVED otherwise. QA: Retain provenance; no inference beyond stated definition |
| `link_status` | Derived filing QA: Amendment link diagnostic, not replacement confirmation | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | SAME_CIK_PERIOD_REVIEW or ORIGINAL_NOT_IN_MONTH. QA: Retain provenance; no inference beyond stated definition |
| `measure` | Derived filing QA: Coverage indicator being summarized | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | One of four core availability flags or complete-four flag. QA: Retain provenance; no inference beyond stated definition |
| `n_base_scopes` | Derived count: Distinct current annual USD dimensionless scopes with any core tag present, including missing amounts; zero means no such scope | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_cal_arcs` | Derived count: Exact parent/child concept-version CAL arc count for Other candidate | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_components` | Derived count: Rows in a geographic gap candidate group, including missing values | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_core_numeric` | Derived count: Number of core categories with numeric amounts; absence/missing do not count | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_core_tags` | Derived count: Number of core concept categories present in a USD scope, including missing values | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_filings` | Derived count: Distinct filing count for stated coverage/status/bridge; these populations differ | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_geo_facts` | Derived count: Number of geographic candidate fact rows, not proven distinct economic components | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_geo_numeric` | Derived count: Geographic candidate rows with nonmissing numeric amounts | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_numeric_components` | Derived count: Nonmissing numeric rows in the same geographic gap candidate group | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_records` | Derived count: Raw records in a seven-key duplicate group | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_reported_zero` | Derived count: Count of unique target reported zeros within a final eligibility class | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `n_scopes` | Derived count: Count of complete four-core scopes in the stated QA classification | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `name` | Original filing metadata: Registrant name as supplied in SUB | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB name. QA: Retain provenance; no inference beyond stated definition |
| `negative` | Standardized calculation relationship: CAL negative-weight flag, not the sign of the NUM amount | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL negative; 1 means weight -1, 0 means +1. QA: Retain provenance; no inference beyond stated definition |
| `numeric_gap_match` | Derived indicator: Geographic candidate sum equals gap and all components are numeric; no accounting confirmation | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `numeric_total_any_period` | Derived indicator: At least one selected Total amount numeric in any period/unit/dimension | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `original_accessions_json` | Derived filing QA: Candidate original accessions linked to an amendment | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Same cik and period within this monthly ZIP. QA: Retain provenance; no inference beyond stated definition |
| `original_context_end` | Derived filing QA: Exact original XBRL end date, distinct from standardized ddate | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Preserved original context c-1; blank otherwise. QA: Retain provenance; no inference beyond stated definition |
| `original_context_start` | Derived filing QA: Exact original XBRL start date where preserved source evidence exists | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Preserved Smithfield/BigBear context c-1; blank otherwise. QA: Retain provenance; no inference beyond stated definition |
| `other_adjustment_usd` | Derived accepted adjustment: Accepted Other adjustment, separate from numerical candidates; zero throughout this freeze | verified_other_tag; NUM + conditional QA / review; USD | Only accepted positive-sign, exact-scope Other relationship; neither observed negative arc accepted. QA: Retain provenance; no inference beyond stated definition |
| `other_cal_weight` | QA classification / source evidence: CAL weight of the reviewed Other arc | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | negative=1 -> -1; negative=0 -> +1. QA: Retain provenance; no inference beyond stated definition |
| `other_candidate_amount_usd` | Diagnostic candidate: Other NUM amount that closes an arithmetic gap but lacks accepted additive CAL interpretation | verified_other_tag; NUM + conditional QA / review; USD | Exact filing/tag/version/scope Other NUM amount. QA: Retain provenance; no inference beyond stated definition |
| `other_candidate_difference` | Diagnostic candidate: Difference after hypothetical positive Other addition; not an accepted reconciliation | core + extension Other; NUM + conditional QA / review; USD | strict_difference - other_candidate_amount_usd. QA: Retain provenance; no inference beyond stated definition |
| `other_relationship_status` | QA classification / source evidence: Whether the Other relation passes signed interpretation checks | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Negative observed arcs flagged ADDITIVE_INTERPRETATION_UNVERIFIED. QA: Retain provenance; no inference beyond stated definition |
| `parent_fact_match` | QA classification / source evidence: Whether a dimensionless parent NUM fact was joined | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Merge indicator; both does not prove an accounting hierarchy. QA: Retain provenance; no inference beyond stated definition |
| `parent_value_usd` | Reported parent candidate: Dimensionless same-concept/version USD parent candidate | row tag/version; NUM + conditional QA / review; USD | Many-to-one merge on filing/date/duration/unit/category/tag/version. QA: Retain provenance; no inference beyond stated definition |
| `period` | Original filing metadata: SUB reporting period used for standardized current-period comparison | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB period. QA: Retain provenance; no inference beyond stated definition |
| `period_date` | Derived diagnostic: Parsed SUB reporting period timestamp | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | to_datetime(period, format=%Y%m%d). QA: Retain provenance; no inference beyond stated definition |
| `period_month` | Derived diagnostic: Year/month portion of SUB reporting period | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | period[:6]. QA: Retain provenance; no inference beyond stated definition |
| `period_relation` | Derived diagnostic: Earlier, same or later standardized reporting month | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Compare ddate_month and period_month. QA: Retain provenance; no inference beyond stated definition |
| `period_status` | Derived filing QA: Filing-level availability of current annual standardized Total context | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | No fact, prior-only, special-review or current annual standardized candidate. QA: Retain provenance; no inference beyond stated definition |
| `period_type` | Derived diagnostic: Pilot current/comparative/special-review partition | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | gap=0 current; gap=365/731 comparative; all other nonzero gaps special review. QA: Retain provenance; no inference beyond stated definition |
| `pilot_verified` | Derived indicator: Signed Other additive relationship accepted, not merely existence of a CAL arc; False for observed two | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `ptag` | Standardized calculation relationship: Calculation arc parent concept name | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL ptag. QA: Retain provenance; no inference beyond stated definition |
| `pversion` | Standardized calculation relationship: Calculation arc parent concept version | ptag/pversion -> ctag/cversion as filed; CAL; identifier/boolean/concept version | Direct CAL pversion; match NUM version exactly. QA: Retain provenance; no inference beyond stated definition |
| `qa_status` | QA classification / source evidence: Complete-scope QA outcome | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Strict exact, precision-compatible, geographic review, Other CAL-sign review or Total semantic review. QA: Retain provenance; no inference beyond stated definition |
| `qtrs` | Standardized SEC fact: SEC rounded whole-quarter duration, not exact start/end interval | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM qtrs. QA: Retain provenance; no inference beyond stated definition |
| `raw_numeric_total_coverage` | Derived indicator: Original current annual dimensionless USD numeric Total coverage, before eligibility exclusions | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `reduction_from_previous` | Derived count: Previous bridge count minus current cumulative count | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `related_amendments_json` | Derived filing QA: List of same-CIK/period amendment accessions | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Group SUB 10-K/A by cik,period. QA: Retain provenance; no inference beyond stated definition |
| `relation_status` | QA classification / source evidence: Diagnostic relation of candidate geography sum to parent | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | No parent, unresolved, numerical equality or incomplete numeric values. QA: Retain provenance; no inference beyond stated definition |
| `replacement_applied` | Derived indicator: An amendment replaces original amounts; False throughout this freeze | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `reported_total_fact_status` | QA classification / source evidence: Numeric selected Total zero/nonzero class | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | ZERO if reported_total_usd == 0 else VALUE. QA: Retain provenance; no inference beyond stated definition |
| `reported_total_usd` | Reported fact projection: Original selected Total, including reported zero; blank when no unique target exists | IncomeTaxesPaidNet; NUM + conditional QA / review; USD | Selected IncomeTaxesPaidNet; no component imputation. QA: Retain provenance; no inference beyond stated definition |
| `reported_zero` | Derived indicator: Unique target USD Total is explicitly reported as numeric zero; raw amount preserved | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `review_status` | QA classification / source evidence: Geographic gap candidate review decision | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | CANDIDATE_ONLY_HIERARCHY_UNVERIFIED in this freeze. QA: Retain provenance; no inference beyond stated definition |
| `rounding_compatible` | Derived indicator: Reported Strict gap falls within declared precision tolerance under round-to-nearest | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `rounding_confirmed` | Derived indicator: Actual rounding cause confirmed; False for every observation in this freeze | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `rounding_status` | QA classification / source evidence: Compatibility classification, not confirmed explanation | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | ROUNDING_COMPATIBLE or PRECISION_INCOMPATIBLE under closed round intervals. QA: Retain provenance; no inference beyond stated definition |
| `rounding_tested` | Derived indicator: Precision check was executed; only original seven nonzero Strict scopes tested | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `rounding_tolerance` | Derived precision diagnostic: Precision-derived round-to-nearest tolerance for four core facts | four core concepts; NUM + conditional QA / review; USD | Sum of four half widths; INF contributes zero; only seven mismatches tested. QA: Retain provenance; no inference beyond stated definition |
| `same_cik_period_originals_json` | Derived filing QA: All original 10-K accessions with same CIK/reporting period | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Group original universe by cik,period; repeated filings require review. QA: Retain provenance; no inference beyond stated definition |
| `segments` | Standardized dimension metadata: SEC flattened axis=member pairs; preserve full original string | Dimension metadata for the fact tag/version; no separate cash-tax concept; DIM; hash/text/boolean | Direct DIM segments. QA: Retain provenance; no inference beyond stated definition |
| `segt` | Standardized dimension metadata: SEC DIM flag indicating segments text was truncated beyond 1024 characters | Dimension metadata for the fact tag/version; no separate cash-tax concept; DIM; hash/text/boolean | Direct DIM segt; not a type map or geography label. QA: Retain provenance; no inference beyond stated definition |
| `selected_iprx0` | Derived indicator: Raw record has iprx exactly zero; numerical use remains conditional on decision | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `semantic_status` | QA classification / source evidence: Filing/exception semantic review status | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Known BigBear ambiguity, Smithfield source-reviewed compatibility, or not individually verified. QA: Retain provenance; no inference beyond stated definition |
| `share_of_original_10k` | Derived ratio: eligibility class n_filings / 2340 | row tag/version or selected core concept family; SUB + grouped counts; fraction | eligibility class n_filings / 2340. QA: 0 to 1; disjoint final eligibility shares sum to 1 |
| `sic` | Original filing metadata: SEC Standard Industrial Classification | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB sic. QA: Retain provenance; no inference beyond stated definition |
| `source_10k_url` | QA classification / source evidence: Original SEC filing URL where available | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Preserved source evidence; blank means not available in this package. QA: Retain provenance; no inference beyond stated definition |
| `source_accession` | QA classification / source evidence: Original NUM accession for traceability | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | adsh retained without replacement. QA: Retain provenance; no inference beyond stated definition |
| `source_dataset` | QA classification / source evidence: Public ZIP release supplying source facts | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | 2026_03_notes.zip. QA: Retain provenance; no inference beyond stated definition |
| `stage` | Derived filing QA: Ordered sequential eligibility bridge stage | row tag/version or selected core concept family; SUB + selected NUM + review evidence; category/date/JSON | Cumulative masks; see count-bridge definition. QA: Retain provenance; no inference beyond stated definition |
| `state_local_status` | Derived disclosure classification: ABSENT_TAG, PRESENT_MISSING, REPORTED_ZERO or REPORTED_NONZERO for the named core category | row tag/version or selected core concept family; NUM; category | Check tag presence first, then raw numeric missingness, then exact zero. QA: Absent/missing never relabeled as zero |
| `state_local_usd` | Reported fact projection: USD net state/local income taxes paid | IncomeTaxPaidStateAndLocalAfterRefundReceived; NUM + conditional QA / review; USD | Selected state/local fact. QA: Retain provenance; no inference beyond stated definition |
| `stprba` | Original filing metadata: Business-address state/province | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB stprba. QA: Retain provenance; no inference beyond stated definition |
| `stprinc` | Original filing metadata: Incorporation state/province | Not applicable; filing metadata rather than an XBRL monetary concept; SUB; identifier/date/text | Direct SUB stprinc. QA: Retain provenance; no inference beyond stated definition |
| `strict_component_sum` | Derived arithmetic: Sum of the three core category amounts within identical scope | three core component concepts; NUM + conditional QA / review; USD | Federal + StateLocal + Foreign. QA: Retain provenance; no inference beyond stated definition |
| `strict_difference` | Derived diagnostic: Strict Total-to-components difference; not automatically an accounting error | four core concepts; NUM + conditional QA / review; USD | Reported Total - strict_component_sum. QA: Retain provenance; no inference beyond stated definition |
| `tag` | Standardized SEC fact: Original XBRL concept local name; interpretation also requires version | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM tag. QA: Retain provenance; no inference beyond stated definition |
| `target_total_candidate_count` | Derived count: Current annual numeric USD Total facts that are dimensionless and without coreg | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `tax_type` | Derived diagnostic: Core economic category or separate extension tag category | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; category/text | Four exact core tags mapped to TOTAL/FEDERAL/STATE_LOCAL/FOREIGN; Other retained as OTHER_CUSTOM::tag. QA: Retain provenance; no inference beyond stated definition |
| `total_fact_count` | Derived count: Selected Total facts in any period/dimension of a filing | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `total_raw_num_count` | Derived count: Raw pre-iprx Total NUM records in a filing | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `total_semantic_status` | QA classification / source evidence: Known semantic review status in reconciliation table | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | NO_SPECIAL_FLAG_IN_PILOT or LEGACY_ROW_SCOPE_AMBIGUOUS; absence of flag is not confirmation. QA: Retain provenance; no inference beyond stated definition |
| `total_status` | Derived disclosure classification: ABSENT_TAG, PRESENT_MISSING, REPORTED_ZERO or REPORTED_NONZERO for the named core category | row tag/version or selected core concept family; NUM; category | Check tag presence first, then raw numeric missingness, then exact zero. QA: Absent/missing never relabeled as zero |
| `total_tag` | QA classification / source evidence: Standard Total concept present in the filing; not evidence of numeric availability | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | IncomeTaxesPaidNet when any selected Total fact exists, blank otherwise. QA: Retain provenance; no inference beyond stated definition |
| `total_tag_present` | Derived indicator: Selected standard Total concept exists in any period/dimension, even when amount missing | row tag/version or selected core concept family; NUM/SUB/DIM + conditional review; boolean | Evaluate stated condition; never infer missing amount as zero. QA: Retain provenance; no inference beyond stated definition |
| `total_usd` | Reported fact projection: USD Total amount in a reporting scope | IncomeTaxesPaidNet; NUM + conditional QA / review; USD | Selected IncomeTaxesPaidNet. QA: Retain provenance; no inference beyond stated definition |
| `unresolved_issue` | QA classification / source evidence: Remaining accounting/context question or lack of global verification | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Human review note; no automatic resolution from a numerical match. QA: Retain provenance; no inference beyond stated definition |
| `uom` | Standardized SEC fact: Original reported unit/currency; controls monetary interpretation | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM uom. QA: Retain provenance; no inference beyond stated definition |
| `usd_current_numeric_count` | Derived count: Current annual numeric Total facts reported in USD, including dimensions | row tag/version or selected core concept family; NUM/SUB or grouped QA; count | Count stated set without imputing missing amounts. QA: Nonnegative integer; numerator no greater than relevant denominator |
| `value` | Standardized SEC fact: Original SEC standardized NUM amount string; unchanged source representation | row tag/version or selected core concept family; NUM; Original NUM uom, not necessarily USD | Direct NUM value; no imputation. QA: Retain provenance; no inference beyond stated definition |
| `value_num` | Derived numeric representation of standardized fact: Numeric conversion of raw value without filling missing amounts | row tag/version or selected core concept family; NUM + SUB/DIM or review evidence; Original NUM uom | pd.to_numeric(value, errors=coerce); assert no nonmissing conversion failures. QA: Retain provenance; no inference beyond stated definition |
| `values_json` | Derived duplicate QA: All raw reported amount strings in a duplicate group | row tag/version or selected core concept family; NUM; row uom / JSON / category | JSON list retaining nulls. QA: Retain provenance; no inference beyond stated definition |
| `verified_other_tag` | QA classification / source evidence: Historically reviewed Other candidate concept name; does not assert accepted addition | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Exact source Other tag retained; see other_relationship_status and CAL sign. QA: Retain provenance; no inference beyond stated definition |
| `verified_other_version` | QA classification / source evidence: Exact taxonomy version of the Other candidate | row tag/version or selected core concept family; NUM/CAL + preserved evidence; category/text/signed weight | Original NUM version matched to CAL cversion. QA: Retain provenance; no inference beyond stated definition |
| `version` | Standardized SEC fact: Standard taxonomy release or extension accession | row tag/version or selected core concept family; NUM; row uom / field-specific metadata | Direct NUM version; retained in seven-key identity. QA: Retain provenance; no inference beyond stated definition |
