<div class="title-block"><h1 class="doc-title">[Title]</h1><div class="subtitle">Supplementary Information</div></div>

# 1 About these tables

This document describes the 49 supplementary tables ([S1](#S1) to [S49](#S49)) and the seven data tables of the Results (T5 to T11) of the paper. It does not reprint them. Every one of these tables is released as a CSV file (Tables 1 to 4, in the Methods, are descriptive and are not released as files); each entry below gives the path, the number of rows and columns, what a row is, what the key columns mean, a three-row excerpt, the places in the paper that cite the table, and caveats. Supplementary tables are numbered in the order in which the Methods and Results first cite them.

```
README.md          what is released, what was changed, licence
INDEX.csv          one row per table: id, file, title, rows, columns, licence flag, sha256
main/              T5 ... T11    Tables 5 to 11 of the paper
supplementary/     S1 ... S49    supplementary tables, one CSV per table
```

**How to read an entry.** *File* is the path of the CSV, its size and its licence flag. *Supports* is the part of the paper the table backs. *Cited in* lists the sections of the Methods, Results and Discussion that cite it (a link opens the paper at that section). *A row is* says what one row represents. *Key columns* explains the columns that matter; the shared provenance block (below) is not repeated. The *excerpt* shows real rows from the file.

# 2 Conventions shared by the tables

**Shared provenance columns.** The result tables (T5 to T11 and the supplementary tables whose entry says so) carry the same block of up to 12 columns, so that a row can be traced to its denominator: `claim_type`, `unit` and `n_units` (what was counted and how many), `n_clusters` and `cluster_def` (the resampling unit: enzyme sub-subclass for natural enzymes, campaign and plate well or backbone cluster for designs, position for BglB), `k`, `N` and `k_of_N` (a count with its denominator), `denominator_def`, `headline_ok` (1 if the row may be quoted as a headline result; 0 for per-metric detail, descriptive analyses, reference rows and wrong-ligand AUROCs), `status` and `licence_flag`.

**Claim types.** `detection` (can the metric see damage), `specificity` (catalytic against matched control), `equivalence` (panel ratio against 1), `discrimination` (a real contrast, dead against active), `ranking` (against a measured label), `enrichment`, `baseline` (a reference row), `design`, `audit`, `not_measurable`.

**Applicability status** (in [S3](#S3), [S4](#S4) and the `applicability_status` columns). `OK` can be tested; `OK-KNOCKON` tested but reported as displacement of the other catalytic residues, with no specificity verdict; `OK-PROVISIONAL` the raw status of the interface terms in the re-predicted ladder, resolved by testability; `GLOBAL` tested but has no site input, so it is a comparator; `REF` a fixed reference row; `X-BOOKKEEP` a counter or constant; `X-NOINPUT` the input cannot reach the changed quantity; `X-ARM` the metric belongs to the other kind (structure space or prediction) than the test; `X-UNDEF-COV` defined on too few units; `X-WITHDRAWN` the test was withdrawn; `X-NOCTRL` no matched control exists; `X-CONFOUND` the control is confounded; `NOT-RUN`; `DUP` identical to another test and read once.

**Verdicts in the specificity tables.** `specific` (response significant, interval of the specificity ratio above 1, control adequate); `non_specific` (responds, not more than the control); `blind` (does not respond); `invariant` (does not change); and counts-floor labels for cells with too few units.

**Why some metrics are not in the main set.** A metric with no residue-set input (whole-protein energies, sequence composition, whole-prediction confidence) cannot respond *specifically* to catalytic residues, and a metric whose input cannot reach the changed quantity cannot register the lesion at all (sequence composition under a rotamer change, for example); such metrics are kept as comparators. One further quantity passes these tests but is kept out of the main set: the Chai-1 combined score, which Chai-1 uses to rank its own models and which equals 0.2 × pTM + 0.8 × ipTM − 100 × (inter-chain clash flag), so that it is a rescaled ipTM and not an independent metric. It is still scored, and its role and reason are in [S1](#S1).

**Names that recur.** `canonical_key` is the distinct metric after literal aliases are merged (`metric_name` may be an alias); `in_main_set` is 1 for the 33 reported metrics; `role` is `main`, `reference` or a supplement role (see [S1](#S1)); `source` is structure-space, prediction-based, PLACER, baseline, natural or denovo as the table says; `lesion_test` is the catalytic lesion or the second-shell lesion; `level` or `lesion_step` is the lesion step (isosteric 15.3, non-isosteric 36.4, Ala 53.2, Gly 80.5 Å³ median side-chain volume change; `second_shell_1/2/4` is the second-shell dose); `ame_flavour` is `crystal` (against the deposited structure) or `self_design` (against a design's own model) and the two are never pooled; `sr_*` is a specificity ratio with its interval; `auroc` is direction-free unless a column says `signed` or `directed`; `rho` is a Spearman correlation.

**Test names.** Tables that refer to a test use the names of [S6](#S6), a name followed by its class in square brackets, for example `main set [catalytic lesion, structure-space]`.

**Licence.** Tables flagged `D2DCure_aggregate` in `INDEX.csv` are built from the D2DCure BglB data, whose licence is unstated; they hold metric-level aggregates only, no per-variant row. All other tables are `public`.

**Reproducibility.** The tables were generated by script from result files with seeds and input hashes recorded; `INDEX.csv` gives the sha256 of every released file.


# 3 Where do I find ...?

::: {.defs}

| I want to know | Go to |
|------------------------------------------------------------|--------------------------------------------------|
| Which 33 metrics are reported, and why the rest are not | [S1](#S1), [S2](#S2); then [S3](#S3) and [S4](#S4) for the reason in each test |
| What a metric reads, and over which residues it is scored | [S2](#S2) |
| The 30 tests, with comparator, control type and role | [S6](#S6) |
| The specificity ratio of one metric at one lesion step | [S33](#S33) (comparators: [S34](#S34)) |
| Whether the controls were good | [S26](#S26), [S27](#S27) (structure space); [S37](#S37), [S39](#S39), [S40](#S40), [S41](#S41), [S38](#S38) (predictor ladder) |
| How fragile the structure-space specificity result is | [S31](#S31), [S42](#S42), [S29](#S29) |
| How a metric responds to the substrate swap, and the role of ligand size | Table 7, [S14](#S14), [S15](#S15) |
| The distance control for the interface terms | Table 10, [S30](#S30), [S37](#S37), [S39](#S39), [S40](#S40), [S41](#S41) |
| Every metric on the 21-pair evaluation set (complete Table 5) | [S11](#S11) |
| Every metric on the 192 plated designs, active against no active (complete Table 6) | [S13](#S13) |
| Every quantity analysed on the 432 BglB variants (complete Table 8) | [S16](#S16) |
| Every metric on the 16 plated designs with a measured activity (complete Table 9) | [S21](#S21) |
| Hits per plate when a metric fills a 96-well plate | [S20](#S20) |
| The wider set of 49 pairs, the 28 re-predicted pairs, the pair-set definitions | [S7](#S7), [S8](#S8), [S9](#S9) |
| BglB: every metric, prediction-based metrics, sensitivity analyses | [S17](#S17), [S19](#S19), [S18](#S18) |
| Plated designs: enrichment and ordering for every metric | [S23](#S23), [S24](#S24), [S22](#S22) |
| The reference rows (resolution, length, tyrosine fraction, distance) | [S12](#S12) |
| Experiments that could not be made | [S48](#S48), [S49](#S49) |

:::


# 4 Table of contents

::: {.defs .toc}

| Table | Title | Topic | Rows × cols | Page |
|---------|--------------------------------------------------------------|------------------------|---------------|-------|
| [S1](#S1) | Main metric set: the role of every distinct metric, and why | Metric audit | 191 × 16 | 4 |
| [S2](#S2) | Metric contracts: what each named quantity reads, over which residues, and where it is valid | Metric audit | 216 × 19 | 4 |
| [S3](#S3) | Applicability of every metric in every test (long format) | Metric audit | 6,480 × 11 | 5 |
| [S4](#S4) | Applicability by class of metric and test | Metric audit | 340 × 5 | 6 |
| [S5](#S5) | Counts restated on the eligible metrics (denominators before and after the audit) | Metric audit | 58 × 14 | 6 |
| [S6](#S6) | Test inventory: the 30 tests, with comparator, control type, role and caveats | Metric audit | 30 × 14 | 7 |
| [S7](#S7) | Wider set of 49 zymogen-mature pairs: all 136 scored metrics, with the same-state null | Activity discrimination (3.1) | 136 × 25 | 7 |
| [S8](#S8) | Zymogen pairs re-predicted with Chai-1, restated with the definedness gate | Activity discrimination (3.1) | 33 × 22 | 8 |
| [S9](#S9) | Definitions of the pair sets | Activity discrimination (3.1) | 6 × 4 | 9 |
| [S10](#S10) | Substrate-trapping mutants checked against the literature (tier retired) | Activity discrimination (3.1) | 6 × 4 | 9 |
| [S11](#S11) | Zymogen-mature evaluation set: all 158 metrics ranked by AUROC (complete Table 5) | Activity discrimination (3.1) | 158 × 27 | 9 |
| [S12](#S12) | Reference rows in full, across the activity tests | Activity discrimination (3.1) | 35 × 9 | 10 |
| [S13](#S13) | Plated designs: all 128 metrics ranked by the AUROC of active against no active designs (complete Table 6) | Activity discrimination (3.1) | 128 × 29 | 11 |
| [S14](#S14) | Substrate swap on all systems: all 33 prediction-based quantities, natural enzymes and de novo designs | Substrate discrimination (3.2) | 242 × 17 | 11 |
| [S15](#S15) | Substrate swap stratified by ligand size and charge | Substrate discrimination (3.2) | 1,136 × 27 | 12 |
| [S16](#S16) | BglB: every analysed quantity ranked by rank correlation with the measured impairment (complete Table 8) | Activity ranking (3.3) | 114 × 35 | 13 |
| [S17](#S17) | BglB: all 84 structure-space and comparator metrics | Activity ranking (3.3) | 84 × 29 | 14 |
| [S18](#S18) | BglB: sensitivity analyses | Activity ranking (3.3) | 11 × 22 | 14 |
| [S19](#S19) | BglB: prediction-based metrics (Chai-1 with the assay substrate) | Activity ranking (3.3) | 28 × 29 | 15 |
| [S20](#S20) | Plated designs: hits per 96-well plate for every metric (filter-style analysis) | Activity ranking (3.3) | 128 × 37 | 16 |
| [S21](#S21) | Plated designs: every metric ranked by correlation with kcat/KM among the 16 designs that have a value (complete Table 9) | Activity ranking (3.3) | 106 × 29 | 16 |
| [S22](#S22) | Plated designs: ordering among the 16 active designs, structure-space metrics and comparators | Activity ranking (3.3) | 81 × 23 | 17 |
| [S23](#S23) | Plated designs: enrichment at every keep fraction, structure-space metrics | Activity ranking (3.3) | 816 × 27 | 17 |
| [S24](#S24) | Plated designs: enrichment for prediction-based metrics | Activity ranking (3.3) | 232 × 27 | 18 |
| [S25](#S25) | Sanity floors by class of metric | Detection ability (3.4) | 53 × 8 | 19 |
| [S26](#S26) | Control matching: the loosest tier needed | Detection ability (3.4) | 81 × 6 | 19 |
| [S27](#S27) | Control matching: balance of residues changed in the two arms | Detection ability (3.4) | 15 × 9 | 20 |
| [S28](#S28) | Catalytic lesion: every metric scored (Table 10 plus supplementary comparators and per-step flags) | Detection ability (3.4) | 43 × 73 | 20 |
| [S29](#S29) | Structure-space specificity by metric family and lesion step, with the panel statistic and sensitivity sets | Detection ability (3.4) | 20 × 27 | 21 |
| [S30](#S30) | Re-predicted catalytic lesion: the prediction-based metrics under three successive controls and the pre-specified rule | Detection ability (3.4) | 6 × 23 | 22 |
| [S31](#S31) | Sensitivity of the specificity-ratio counts to motif size, packing matching and count gating | Detection ability (3.4) | 20 × 7 | 22 |
| [S32](#S32) | Re-predicted ladder: seed-noise context | Detection ability (3.4) | 56 × 12 | 23 |
| [S33](#S33) | Specificity ratio of every eligible metric at every step | Detection ability (3.4) | 256 × 29 | 23 |
| [S34](#S34) | Specificity ratio of whole-protein and sequence-only comparators at every step | Detection ability (3.4) | 308 × 29 | 24 |
| [S35](#S35) | The specific cells that survive the controls | Detection ability (3.4) | 97 × 10 | 24 |
| [S36](#S36) | Rank statistic R per lesion step on the 143 main enzymes | Detection ability (3.4) | 313 × 14 | 25 |
| [S37](#S37) | Re-predicted ladder: distance of the substituted and control residues to the ligand | Detection ability (3.4) | 312 × 34 | 25 |
| [S38](#S38) | Re-predicted ladder: candidates for a new distance-matched control | Detection ability (3.4) | 291 × 17 | 26 |
| [S39](#S39) | Re-predicted ladder: specificity ratio in strata of the distance to the ligand | Detection ability (3.4) | 203 × 27 | 27 |
| [S40](#S40) | Re-predicted ladder: caliper-matched subsets and the rule labels | Detection ability (3.4) | 348 × 25 | 27 |
| [S41](#S41) | Re-predicted ladder: regression-adjusted ratios | Detection ability (3.4) | 116 × 28 | 28 |
| [S42](#S42) | Panel equivalence statistic: earlier whole panel against the main-set metrics | Detection ability (3.4) | 6 × 10 | 28 |
| [S43](#S43) | Re-predicted ladder: specificity ratio per step for all metrics | Detection ability (3.4) | 231 × 16 | 29 |
| [S44](#S44) | Second-shell lesion: every metric scored (Table 11 plus supplementary comparators and per-dose flags) | Detection ability (3.4) | 37 × 59 | 29 |
| [S45](#S45) | Drift of the current Chai-1 engine against the earlier predictions | Substrate discrimination (3.2) | 176 × 5 | 30 |
| [S46](#S46) | Effective dimensionality of the panel | Detection ability (3.4) | 4 × 10 | 30 |
| [S47](#S47) | De novo designs: burial equivalence of the created-site control | Detection ability (3.4) | 5 × 11 | 31 |
| [S48](#S48) | Experiments that could not be made or were retired | Detection ability (3.4) | 9 × 4 | 31 |
| [S49](#S49) | PLACER ensemble metrics on the isosteric step (not interpretable) | Detection ability (3.4) | 50 × 12 | 32 |

:::


# 5 Supplementary tables


### Table S1. Main metric set: the role of every distinct metric, and why {#S1}

::: {.tmeta}

**File.** `supplementary/S1_main_metric_set.csv` · 191 rows × 16 columns · public

**Supports.** Methods, Table 1 and 'Which metrics are reported'; the main set of 33 metrics used in Tables 5 to 11. **Cited in.** Methods [2.1](https://pdflink.invalid/paper.pdf#page=1).

**A row is** one distinct metric (a canonical key; literal aliases are merged), 191 in all.

:::

The audit that fixes which metrics the paper reports. For each distinct metric it gives the applicability status in the detection test of the catalytic lesion, in the dead-against-active tests and in the activity-ranking tests, and the resulting role: main (33, valid and tested in the deliberate-change tests and in the tests on real proteins), reference (6, comparators chosen before any result was seen), excluded_bookkeeping (63 counters and constants) or one of the supplement roles (supp_global 44, supp_placer 25, supp_excluded 10, supp_aggregate 4, supp_partial 3, supp_real_protein_tests_only 2, and supp_derived 1, the Chai-1 combined score, a rescaled ipTM). The reason for each role is in the last column. The status is decided from what a metric reads, whether it is defined and the design of the experiment, never from a result.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `canonical_key` / `members` / `rep_metric` | the distinct metric, the names merged into it and the representative one |
| `mode` / `input_class` / `subfamily` / `aggregator` | structure-space or prediction-based, what the metric reads, its family and how it is summarised |
| `status_detection_test` / `fraction_detection_test` | applicability status in the detection test of the catalytic lesion and the share of units on which the metric is defined |
| `status_dead_vs_active_tests` / `fraction_dead_vs_active_tests` / `partial_dead_vs_active_tests` | the same for the dead-against-active tests |
| `status_ranking_tests` / `ranking_tests_ok` | status in each activity-ranking test (BglB variants, plated designs) and the tests in which the metric is OK |
| `role` | main, reference, excluded_bookkeeping, supp_global, supp_placer, supp_excluded, supp_aggregate, supp_partial, supp_real_protein_tests_only or supp_derived |
| `reason` | why the metric has that role |

:::

**Excerpt** (first 3 rows where role = main).

::: {.excerpt}

| `canonical_key` | `input_class` | `status_detection_test` | `status_dead_vs_active_tests` | `role` |
|----------|----------|----------|----------|----------|
| `ame_crystal_clash_max` | `pred_interface` | `OK-PROVISIONAL` | `OK` | `main` |
| `ame_crystal_rmsd` | `ame` | `OK-KNOCKON` | `OK` | `main` |
| `catalytic_frac_buried` | `struct_site` | `OK` | `OK` | `main` |

:::

**Notes.**

- The status vocabulary is in the Conventions.
- NOT-RUN in status_ranking_tests marks the PLACER metrics, which were not computed in the BglB and plated-design analyses.


### Table S2. Metric contracts: what each named quantity reads, over which residues, and where it is valid {#S2}

::: {.tmeta}

**File.** `supplementary/S2_metric_contracts.csv` · 216 rows × 19 columns · public

**Supports.** Methods, Table 1 and 'Which metrics are reported'. **Cited in.** Methods [2.1](https://pdflink.invalid/paper.pdf#page=1).

**A row is** one named quantity (216 in all; an alias is a separate row linked by alias_of and canonical_key).

:::

The input contract of every quantity in the panel: what it reads (sequence only, whole-protein structure, site-scoped structure, predictor output, active-site accuracy, PLACER output, deposit metadata or bookkeeping), over which residues it is scored in the catalytic arm and in the two kinds of control arm, which inputs it needs, which kinds of metric it is valid for and which changes it cannot respond to.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_name` / `canonical_key` / `alias_of` / `alias_kind` | the quantity, the distinct metric after aliases are merged, and the kind of alias |
| `aggregator` / `metric_family` / `subfamily` | how it is summarised, and its family and subfamily |
| `input_class` | sequence-only, whole-protein structure, site-scoped structure, prediction, active-site accuracy (AME), PLACER, deposit metadata or bookkeeping |
| `scope_catalytic_arm` / `scope_control_arm_catalytic_lesion` / `scope_control_arm_second_shell` | the residues the metric is scored over in the catalytic arm, in the control arm of the catalytic lesion and in the control arm of the second-shell lesion |
| `needs_cat_residue` / `needs_ligand` / `needs_reference` / `needs_predictor` | the inputs the metric needs |
| `valid_modes` | structure-space, prediction-based, PLACER, any or deposit metadata |
| `invariant_under` | changes the metric cannot register (for example sequence composition under a rotamer change) |
| `ame_flavour` / `note` | for active-site accuracy, the reference it is measured against; remarks on the metric, including where the metric as computed differs from its earlier description |

:::

**Excerpt** (first 3 rows where input_class = struct_site).

::: {.excerpt}

| `metric_name` | `input_class` | `scope_catalytic_arm` | `valid_modes` |
|----------|----------|----------|----------|
| `catalytic_frac_buried` | `struct_site` | `scored_residue_set` | `structure-space` |
| `catalytic_ligand_min_dist` | `struct_site` | `scored_residue_set+ligand_within_…` | `structure-space` |
| `catalytic_pairwise_dist_max` | `struct_site` | `scored_residue_set` | `structure-space` |

:::


### Table S3. Applicability of every metric in every test (long format) {#S3}

::: {.tmeta}

**File.** `supplementary/S3_applicability.csv` · 6,480 rows × 11 columns · public

**Supports.** Methods, 'Which metrics are reported'; every Results subsection. **Cited in.** Methods [2.1](https://pdflink.invalid/paper.pdf#page=1).

**A row is** one named quantity in one test (216 quantities x 30 tests = 6,480 rows).

:::

Whether each quantity can be tested in each of the 30 tests, and if not why. Status counts: OK 468, GLOBAL 339, REF 15, OK-KNOCKON 6, OK-PROVISIONAL 10 (testable); X-ARM 2,296, X-BOOKKEEP 1,920, X-NOINPUT 576, X-WITHDRAWN 381, X-UNDEF-COV 203, X-NOCTRL 118, X-CONFOUND 10, NOT-RUN 79, DUP 59 (not testable, with the reason). The reason and the coverage (defined_k of defined_N units) are given. Decided from inputs, definedness and design only, never from results.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_name` / `canonical_key` / `input_class` | the quantity, the distinct metric and its class |
| `test` / `test_class` | the test (its name and class as in [S6](#S6)) and the class alone, for example 'dead against active, prediction-based' |
| `status` / `reason` | the applicability status and the reason in words |
| `defined_k` / `defined_N` / `fraction` / `partial` | number of units on which the metric is defined, of how many, their ratio, and whether coverage is partial |

:::

**Excerpt** (first 3 rows where status = OK).

::: {.excerpt}

| `metric_name` | `test` | `status` | `reason` |
|----------|----------|----------|----------|
| `ame_crystal_clash_max` | `BglB single-point variants (predi…` | `OK` | `eligible and scored` |
| `ame_crystal_clash_max` | `zymogen-mature pairs re-predicted…` | `OK` | `eligible and scored` |
| `ame_crystal_clash_max` | `substrate swap, natural enzymes […` | `OK` | `eligible and scored` |

:::

**Notes.**

- Released as a CSV only: with 6,480 rows it is not printed. [S25](#S25) is its summary by class of metric.
- Of the 79 cells with status NOT-RUN, 50 are PLACER metrics that were not computed in the BglB and plated-design analyses. The other 29 are prediction-based metrics in the ladder with ligand-distance-matched controls: this analysis was carried out (results in [S40](#S40) and [S41](#S41)) but its cells keep the label NOT-RUN.


### Table S4. Applicability by class of metric and test {#S4}

::: {.tmeta}

**File.** `supplementary/S4_applicability_by_class.csv` · 340 rows × 5 columns · public

**Supports.** Methods, 'Which metrics are reported' (summary of [S3](#S3)). **Cited in.** Methods [2.1](https://pdflink.invalid/paper.pdf#page=1).

**A row is** one class of metric in one test with one status (340 rows).

:::

A summary of [S3](#S3): for each input class and test, how many metrics receive each status. The quickest way to see why a whole class of metrics is absent from a result.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `input_class` | class of metric (ame, bookkeeping, pred_global, pred_interface, seq_only, struct_site, struct_whole, ...) |
| `test` / `test_class` | the test and its class |
| `status` | applicability status |
| `n_metrics` | number of metrics of that class with that status in that test |

:::

**Excerpt** (first 3 rows where status = OK).

::: {.excerpt}

| `input_class` | `test_class` | `status` | `n_metrics` |
|----------|----------|----------|----------|
| `ame` | `activity ranking, prediction-based` | `OK` | `5` |
| `ame` | `dead against active, prediction-b…` | `OK` | `6` |
| `ame` | `substrate swap` | `OK` | `6` |

:::


### Table S5. Counts restated on the eligible metrics (denominators before and after the audit) {#S5}

::: {.tmeta}

**File.** `supplementary/S5_denominator_restatement.csv` · 58 rows × 14 columns · public

**Supports.** Methods, 'Which metrics are reported'. **Cited in.** Methods [2.1](https://pdflink.invalid/paper.pdf#page=1).

**A row is** one headline count of the earlier whole-panel analysis (58 in all).

:::

The counts of responding and specific metrics of the earlier analysis (original_k of original_N, over every metric with a testable cell) restated on the eligible metrics only (eligible_k of eligible_N, also as distinct metrics and for the whole-protein comparators), with the breakdown of what was excluded and why. It shows how much of the earlier denominators were metrics that could not respond.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis` / `level` / `statistic` | the earlier analysis (data set and lesion), the lesion step and the statistic ('responds' or 'specific') |
| `original_k` / `original_N` | count and denominator of the earlier analysis |
| `eligible_k` / `eligible_N` / `eligible_distinct_k` / `eligible_distinct_N` | the same on eligible metrics, and as distinct metrics |
| `global_k` / `global_N` | the count among whole-protein comparators |
| `excluded_breakdown` / `recompute_kind` / `note` | which statuses were excluded and how many, how the recount was done, and a note |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `analysis` | `level` | `statistic` | `original_k` | `original_N` | `eligible_k` | `eligible_N` |
|----------|----------|----------|----------|----------|----------|----------|
| `main set, packing-matched control…` | `ala` | `responds` | `55` | `102` | `25` | `37` |
| `main set, packing-matched control…` | `ala` | `specific` | `11` | `102` | `10` | `37` |
| `main set, packing-matched control…` | `gly` | `responds` | `58` | `98` | `25` | `34` |

:::


### Table S6. Test inventory: the 30 tests, with comparator, control type, role and caveats {#S6}

::: {.tmeta}

**File.** `supplementary/S6_test_inventory.csv` · 30 rows × 14 columns · public

**Supports.** Methods 2.2 to 2.5; the key to the test names in [S3](#S3) and [S4](#S4). **Cited in.** Methods [2.1](https://pdflink.invalid/paper.pdf#page=1).

**A row is** one test: an experiment on a data set with one kind of metric (30 in all).

:::

Every test with its name and class, the kind of metric (structure-space or prediction-based), the unit and the number of units, the resampling unit, the changes applied, the comparator and control type, the role (primary, sensitivity, sanity, retired, not_measurable or dup) and the caveats. [S3](#S3) and [S4](#S4) use the test names of this table.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `test` / `reader_name` / `test_class` / `mode` | the test (name with its class), the name alone, the class, and structure-space or prediction-based |
| `unit` / `n_units` / `n_clusters` / `cluster_def` | what is counted, how many, and the resampling unit |
| `levels` / `comparator` / `control_type` | what is changed or contrasted, what the metric is compared with and how the control is built |
| `claim_type` / `role` | the kind of claim and the role: primary, sensitivity, sanity, retired, not_measurable or dup |
| `caveats` | limits of the test |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `reader_name` | `test_class` | `mode` | `claim_type` | `role` |
|----------|----------|----------|----------|----------|
| `main set, packing-matched controls` | `catalytic lesion, structure-space` | `structure-space` | `specificity` | `primary` |
| `sanity floor: all catalytic resid…` | `detection floor (duplicate of the…` | `structure-space` | `detection` | `dup` |
| `sanity floor: permuted sequence o…` | `sanity floor` | `structure-space` | `detection` | `sanity` |

:::


### Table S7. Wider set of 49 zymogen-mature pairs: all 136 scored metrics, with the same-state null {#S7}

::: {.tmeta}

**File.** `supplementary/S7_zymogen_all_metrics.csv` · 136 rows × 25 columns · public

**Supports.** Results 3.1.1 (wider set); Methods 2.2.1. **Cited in.** Methods [2.2.1](https://pdflink.invalid/paper.pdf#page=2); Results [3.1.1](https://pdflink.invalid/paper.pdf#page=13).

**A row is** one scored metric (136 in all).

:::

The analysis on the 49 pairs for which structure-space metrics were scored (before the evaluation set of 21 pairs that share a ligand was fixed): the direction-free AUROC of dead against active with interval, the directed AUROC, the number of pairs, and the AUROC of the same metric on 96 same-state null pairs, which shows how much separation arises without any dead/active difference.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_name` / `canonical_key` / `input_class` / `in_main_set` | the metric, its class and whether it is a main-set metric |
| `n_pairs` | pairs with a value (49 at most) |
| `auroc` / `auroc_lo` / `auroc_hi` / `auroc_directed` | direction-free AUROC with 95% interval over pairs, and the directed value |
| `auroc_vs_same_state_null` / `n_zymogen_pairs` / `n_same_state_null_pairs` | AUROC of zymogens against the same-state null pairs and the numbers in each group |
| `applicability_status` | applicability status |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `metric_name` | `in_main_set` | `n_pairs` | `auroc` | `auroc_lo` | `auroc_hi` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_frac_buried` | `1` | `49` | `0.5321` | `0.5019` | `0.6112` |
| `catalytic_hydration_count` | `0` | `48` | `0.5686` | `0.505` | `0.6604` |
| `catalytic_ligand_min_dist` | `0` | `25` | `0.5264` | `0.5024` | `0.6464` |

:::

**Notes.**

- Structure-space and PLACER metrics only; the 4 prediction-based metrics were scored on the 28 re-predicted pairs ([S8](#S8)).
- Results are descriptive of a wider set; the evaluation set is the 21 pairs of [S36](#S36).


### Table S8. Zymogen pairs re-predicted with Chai-1, restated with the definedness gate {#S8}

::: {.tmeta}

**File.** `supplementary/S8_zymogen_re_predicted_restated.csv` · 33 rows × 22 columns · public

**Supports.** Results 3.1.1 (wider-set check for the prediction-based metrics). **Cited in.** Methods [2.2.1](https://pdflink.invalid/paper.pdf#page=2); Results [3.1.1](https://pdflink.invalid/paper.pdf#page=13).

**A row is** one prediction-based metric (33 in all).

:::

The 28 zymogen-mature pairs re-predicted with Chai-1: the AUROC of each metric with interval, the number of pairs reported against the number on which the metric is defined, and a note where the earlier value was not interpretable. Active-site accuracy is relabelled as measured against each form's own deposited structure.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_name` / `metric_reported_as` | the metric and the name it carried in the earlier report |
| `input_class` | class of metric |
| `n_pairs_reported` / `n_pairs_defined_restated` | pairs in the earlier report and pairs on which the metric is defined |
| `auroc` / `auroc_lo` / `auroc_hi` | direction-free AUROC with 95% interval |
| `applicability_status` / `restatement_note` | applicability status and what was restated |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where applicability_status = OK).

::: {.excerpt}

| `metric_name` | `n_pairs_reported` | `n_pairs_defined_restated` | `auroc` | `applicability_status` |
|----------|----------|----------|----------|----------|
| `ame_crystal_clash_max` | `21` | `21` | `0.5351` | `OK` |
| `ame_crystal_pass` | `28` | `28` | `0.5045` | `OK` |
| `ame_crystal_rmsd_max` | `28` | `28` | `0.5332` | `OK` |

:::

**Notes.**

- 28 pairs include the 7 apo pairs that are not in the 21-pair evaluation set.


### Table S9. Definitions of the pair sets {#S9}

::: {.tmeta}

**File.** `supplementary/S9_pair_set_definitions.csv` · 6 rows × 4 columns · public

**Supports.** Methods 2.2.1; Results 3.1.1. **Cited in.** Methods [2.2.1](https://pdflink.invalid/paper.pdf#page=2); Results [3.1.1](https://pdflink.invalid/paper.pdf#page=13).

**A row is** one set of zymogen-mature pairs (6 in all).

:::

The six sets used in 3.1 with their size and definition: 55 candidate rows, 49 scored pairs, 45 with PLACER, 28 re-predicted pairs, the 21-pair evaluation set (pairs that share a ligand) and the 96 same-state null pairs, and which table uses each.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `pair_set` / `n` | the set and its size |
| `definition` | how the set is defined |
| `used_for` | the table that uses it |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `pair_set` | `n` | `used_for` |
|----------|----------|----------|
| `zymogen candidate rows` | `55` | `candidate list` |
| `scored pairs (wider set)` | `49` | `S7 (49 = max n_pairs)` |
| `pairs with PLACER` | `45` | `S49` |

:::


### Table S10. Substrate-trapping mutants checked against the literature (tier retired) {#S10}

::: {.tmeta}

**File.** `supplementary/S10_trapping_verification.csv` · 6 rows × 4 columns · public

**Supports.** Results 3.1.1 (retired tier); Methods 2.2.1. **Cited in.** Methods [2.2.1](https://pdflink.invalid/paper.pdf#page=2); Results [3.1.1](https://pdflink.invalid/paper.pdf#page=13).

**A row is** one verdict category (6 rows).

:::

The 30 trapping-mutant pairs verified against the primary literature: 15 confirmed reduced, 4 confirmed inactive, 4 active and 7 not stated; 26 of the 30 (86.7%, 95% interval 70.3 to 94.7%) are not confirmed dead. Every deposited construct carries an engineered substitution; the failure is the inference from substitution to dead enzyme. The tier is retired.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `verdict` | confirmed_reduced, confirmed_inactive, active, not_stated, and the summary rows |
| `n_pairs` / `denominator` | number of pairs and the total (30) |
| `note` | interval of the mislabelling rate |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `verdict` | `n_pairs` | `denominator` | `note` |
|----------|----------|----------|----------|
| `confirmed_reduced` | `15` | `30` | ` ` |
| `not_stated` | `7` | `30` | ` ` |
| `confirmed_inactive` | `4` | `30` | ` ` |

:::


### Table S11. Zymogen-mature evaluation set: all 158 metrics ranked by AUROC (complete Table 5) {#S11}

::: {.tmeta}

**File.** `supplementary/S11_zymogen_21pair_all_metrics.csv` · 158 rows × 27 columns · public

**Supports.** Results 3.1.1; the complete version of Table 5. **Cited in.** Methods [2.2.1](https://pdflink.invalid/paper.pdf#page=2); Results [3.1.1](https://pdflink.invalid/paper.pdf#page=13).

**A row is** one metric scored on the 21 pairs (158 in all).

:::

Every metric scored on the 21 pairs that share a ligand: structure-space, PLACER and prediction-based metrics, including whole-protein and sequence-only comparators, ranked by direction-free AUROC of dead against active. The best-of-158 threshold (95th percentile of the best AUROC among 158 unrelated metrics in label-swap simulations) is marked: seven metrics exceed it, all summaries of whole-prediction confidence (pLDDT and per-chain pTM), which are comparators and not main-set metrics.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `rank` / `rank_in_table_5` | rank among all 158 and rank among the 39 items of Table 5 |
| `metric_name` / `canonical_key` / `source` / `input_class` | the metric, the distinct metric, structure-space / PLACER / prediction-based, and class |
| `role` | main, reference or a supplement role (43 rows carry main because aliases of the 33 main-set metrics are separate rows) |
| `n_pairs` / `auroc` / `auroc_ci_lo` / `auroc_ci_hi` | pairs (21) and AUROC with 95% interval over pairs |
| `higher_in` / `auroc_directed` | the form (dead or active) in which the metric is larger, and the directed AUROC |
| `above_best_of_158_threshold` / `applicability_status` | 1 if above the threshold; applicability status |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `rank` | `metric_name` | `role` | `auroc` | `auroc_ci_lo` | `auroc_ci_hi` |
|----------|----------|----------|----------|----------|----------|
| `1` | `chai_plddt_min` | `supp_global` | `0.8821` | `0.7483` | `0.9932` |
| `2` | `chai_plddt_best_model` | `supp_global` | `0.7914` | `0.6757` | `0.9025` |
| `3` | `chai_plddt_mean` | `reference` | `0.7914` | `0.6757` | `0.9025` |

:::


### Table S12. Reference rows in full, across the activity tests {#S12}

::: {.tmeta}

**File.** `supplementary/S12_reference_rows.csv` · 35 rows × 9 columns · D2DCure aggregate (licence of the source data unstated; aggregates only, no per-variant rows)

**Supports.** Results 3.1 and 3.3; Tables 5, 6, 8 and 9; Methods 2.2 and 2.4. **Cited in.** Methods [2.2.1](https://pdflink.invalid/paper.pdf#page=2), [2.4.1](https://pdflink.invalid/paper.pdf#page=6); Results [3.1.1](https://pdflink.invalid/paper.pdf#page=13), [3.1.2](https://pdflink.invalid/paper.pdf#page=14), [3.3.1](https://pdflink.invalid/paper.pdf#page=17).

**A row is** one reference item for one measure (35 in all).

:::

The rows that need no catalytic information, reported in full with intervals: crystallographic resolution, sequence length, net charge and tyrosine fraction (AUROC on the 49 zymogen pairs) and pLDDT and pTM (AUROC on the 28 re-predicted pairs); the five declared BglB baselines (side-chain volume change, negative distance to the catalytic residues, burial, BLOSUM62 and the Rosetta score of the BglB data; signed AUROC on 432 variants); and expected hits per 96-well plate at each keep fraction for tyrosine fraction, net charge and sequence length on the plates.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `reference_item` / `metric` | the reference row (and the end kept for plate rows) |
| `measure` | AUROC (direction-free), AUROC (signed, pre-directed) or expected hits per 96-well plate |
| `keep_fraction` | fraction of designs kept (plate rows only) |
| `estimate` / `ci_lo` / `ci_hi` / `n` | the value, its interval and the number of units |

:::

**Excerpt** (first 3 rows where measure = AUROC (signed, pre-directed)).

::: {.excerpt}

| `reference_item` | `measure` | `estimate` | `ci_lo` | `ci_hi` | `n` |
|----------|----------|----------|----------|----------|----------|
| `abs_dvol_A3` | `AUROC (signed, pre-directed)` | `0.5513` | `0.4728` | `0.6278` | `432` |
| `neg_d_cat` | `AUROC (signed, pre-directed)` | `0.7633` | `0.6872` | `0.8243` | `432` |
| `neg_rel_sasa` | `AUROC (signed, pre-directed)` | `0.6831` | `0.6058` | `0.748` | `432` |

:::

**Notes.**

- Contains aggregates of D2DCure data (licence unstated); no per-variant rows.


### Table S13. Plated designs: all 128 metrics ranked by the AUROC of active against no active designs (complete Table 6) {#S13}

::: {.tmeta}

**File.** `supplementary/S13_plates_all_metrics_auroc.csv` · 128 rows × 29 columns · public

**Supports.** Results 3.1.2; the complete version of Table 6. **Cited in.** Methods [2.2.2](https://pdflink.invalid/paper.pdf#page=4); Results [3.1.2](https://pdflink.invalid/paper.pdf#page=14).

**A row is** one metric scored on the 192 designs (128 in all).

:::

Every metric scored on the 192 plated designs, ranked by the direction-free AUROC of the 16 active designs against the 176 no active designs, with 95% interval over the 136 backbone clusters. The best-of-128 threshold (permuting labels among designs) is marked: ten metrics exceed it. They are two main-set metrics (the intra-residue repulsion, 0.80, and the repulsion of the catalytic residues, 0.78), an alias of the latter, and sequence-composition and whole-protein comparators.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `rank` / `rank_in_table_6` / `in_table_6` | rank among 128, rank among the 36 items of Table 6 and membership of Table 6 |
| `metric_name` / `canonical_key` / `source` / `input_class` / `role` | the metric, its source, class and role |
| `n_designs` / `n_active` | 192 and 16 |
| `auroc` / `auroc_ci_lo` / `auroc_ci_hi` / `auroc_directed` / `higher_in` | AUROC, interval, directed AUROC and the group in which the metric is larger |
| `above_best_of_all_metrics_threshold` / `applicability_status` | 1 if above the best-of-128 threshold; applicability status |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `rank` | `metric_name` | `role` | `auroc` | `auroc_ci_lo` | `auroc_ci_hi` |
|----------|----------|----------|----------|----------|----------|
| `1` | `rosetta_cat_fa_intra_rep` | `main` | `0.8018` | `0.6385` | `0.8929` |
| `2` | `frac_G` | `supp_global` | `0.7926` | `0.6157` | `0.8698` |
| `3` | `rosetta_ref` | `excluded_bookkeeping` | `0.7876` | `0.6708` | `0.8914` |

:::

**Notes.**

- Designs are not exchangeable (10 of the 16 active designs lie in two backbone clusters), so the threshold understates the chance range.


### Table S14. Substrate swap on all systems: all 33 prediction-based quantities, natural enzymes and de novo designs {#S14}

::: {.tmeta}

**File.** `supplementary/S14_substrate_swap_per_metric.csv` · 242 rows × 17 columns · public

**Supports.** Results 3.2; the all-system analysis behind Table 7. **Cited in.** Methods [2.3](https://pdflink.invalid/paper.pdf#page=4); Results [3.2](https://pdflink.invalid/paper.pdf#page=15).

**A row is** one prediction-based quantity under one wrong-ligand condition, for one source (natural enzymes or de novo designs).

:::

The substrate swap before the 55-enzyme evaluation set was fixed: all 59 natural enzymes (cognate value averaged over five seeds) and all 30 de novo designs, for every one of the 33 prediction-based quantities that were scored, including the Chai-1 combined score (a rescaled ipTM) that Table 7 leaves out. For each quantity and each wrong ligand (same enzyme class, different class, decoy; apo for the quantities that are defined without a ligand) it gives the mean under the cognate and under the other condition, the paired change, the change in units of seed noise, and the direction-free AUROC with its interval.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` | natural or denovo |
| `metric_name` / `canonical_key` / `input_class` | the quantity, the distinct metric it belongs to and its class |
| `ame_flavour` | crystal = active-site accuracy against the deposited structure; self_design = against the design's own model (never pooled) |
| `in_main_set` | 1 for the four main-set metrics (each appears several times: mean, maximum and spread over the five predicted models are separate rows) |
| `condition` | same_ec, diff_ec, decoy or apo |
| `n_systems` | systems with a value (59 natural, 30 de novo) |
| `mean_cognate` / `mean_condition` / `mean_delta` | mean value under the cognate ligand, under the condition, and the paired difference |
| `median_delta_over_sigma` / `frac_beyond_1sigma` | median change in units of the seed-to-seed standard deviation, and the share of systems that move by more than one |
| `auroc` / `auroc_lo` / `auroc_hi` | direction-free AUROC of cognate against the condition, 95% interval over systems |

:::

**Excerpt** (first 3 rows where source = natural, condition = diff_ec, in_main_set = 1).

::: {.excerpt}

| `source` | `metric_name` | `condition` | `n_systems` | `mean_cognate` | `mean_condition` | `auroc` |
|----------|----------|----------|----------|----------|----------|----------|
| `natural` | `ame_crystal_clash_max` | `diff_ec` | `58` | `3.2826` | `3.6103` | `0.6564` |
| `natural` | `ame_crystal_rmsd_max` | `diff_ec` | `59` | `1.4469` | `1.5572` | `0.5395` |
| `natural` | `ame_crystal_rmsd_mean` | `diff_ec` | `59` | `1.2516` | `1.2895` | `0.5306` |

:::

**Notes.**

- n is 59 natural enzymes here and 55 in Table 7, whose evaluation set drops four enzymes whose ligand could not be built.
- Per-metric results of this table are descriptive; the ranking and the best-of-30 threshold are in Table 7.


### Table S15. Substrate swap stratified by ligand size and charge {#S15}

::: {.tmeta}

**File.** `supplementary/S15_substrate_swap_size_strata.csv` · 1,136 rows × 27 columns · public

**Supports.** Results 3.2; Methods 2.3 (size check, Eq. 10). **Cited in.** Methods [2.3](https://pdflink.invalid/paper.pdf#page=4); Results [3.2](https://pdflink.invalid/paper.pdf#page=15).

**A row is** one quantity, source, wrong-ligand condition and stratum of the difference in ligand size or charge, for one analysis variant.

:::

The check of whether ligand size or charge explains the discrimination. For each headline quantity (ipTM, per-chain pTM minimum, the combined score, ligand clearance), comparator (pTM, pLDDT, AME RMSD) and the two baselines (ligand heavy-atom count and formal charge), the cells (an enzyme and one wrong ligand) are stratified by the difference in heavy-atom count (smaller, matched, larger), by the charge difference (same, different) and jointly. For each stratum it gives the paired win fraction, the AUROC of the absolute value, the Spearman correlation of the size difference with the change, intervals over systems and clusters, and whether the effect survives.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `variant` | natural or denovo; primary or the variant that excludes ipTM = 0 cells (excl_iptm0) |
| `metric_name` / `role` | the quantity and headline, comparator or baseline |
| `stratum_family` / `stratum` | all, size (smaller, matched, larger), charge (q_same, q_diff) or joint, and the stratum |
| `condition` | same_ec, diff_ec, decoy or the three pooled (pooled_3) |
| `k_cells` / `N_cells` / `k_systems` / `N_systems` | cells and systems in the stratum |
| `win_frac` / `win_lo95` / `win_hi95` | paired win fraction (cognate higher than wrong ligand) with 95% interval |
| `auroc_abs` / `spearman_dn_vs_change` / `survives` | AUROC of absolute value, Spearman correlation of size difference with the change, and 1 / 0 / 'n<10, not estimated' |

:::

**Excerpt** (first 3 rows where variant = primary, source = natural, stratum_family = size).

::: {.excerpt}

| `metric_name` | `stratum` | `condition` | `k_cells` | `N_cells` | `win_frac` |
|----------|----------|----------|----------|----------|----------|
| `chai_iptm_mean` | `smaller` | `same_ec` | `18` | `177` | `1.0` |
| `chai_aggregate_score_mean` | `smaller` | `same_ec` | `18` | `177` | `1.0` |
| `chai_per_chain_ptm_min_mean` | `smaller` | `same_ec` | `18` | `177` | `0.8333` |

:::

**Notes.**

- Released as a CSV only for the full 1,136 rows; the excerpt shows the structure.


### Table S16. BglB: every analysed quantity ranked by rank correlation with the measured impairment (complete Table 8) {#S16}

::: {.tmeta}

**File.** `supplementary/S16_bglb_all_quantities_ranked.csv` · 114 rows × 35 columns · D2DCure aggregate (licence of the source data unstated; aggregates only, no per-variant rows)

**Supports.** Results 3.3.1; the complete version of Table 8. **Cited in.** Methods [2.4](https://pdflink.invalid/paper.pdf#page=6), [2.4.1](https://pdflink.invalid/paper.pdf#page=6); Results [3.3.1](https://pdflink.invalid/paper.pdf#page=17).

**A row is** one quantity analysed on the 432 BglB variants (114 in all).

:::

Every quantity analysed on the 432-variant evaluation set: 84 structure-space metrics, 25 prediction-based metrics and the five declared baselines, ranked by the Spearman correlation of the size of its change with the measured impairment, with 95% interval over the 175 positions. It carries the best-of-114 threshold, whether the quantity beats the distance baseline, the correlation of the signed change, and beside them the AUROC of the binary contrast (impaired against wild-type-like variants) with its interval, threshold and beats-the-distance flag. No quantity beats the distance baseline; 34 exceed the best-of-114 threshold.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `rank` / `rank_in_table_8` / `in_table_8` | rank among 114, rank among the 41 items of Table 8 and membership of Table 8 |
| `metric_name` / `canonical_key` / `source` / `input_class` / `role` | the quantity, its source (structure-space, prediction-based or baseline), class and role |
| `n_variants` | variants with a value (431 or 432; 248 for the Rosetta score of the BglB data) |
| `rho` / `rho_ci_lo` / `rho_ci_hi` | Spearman correlation and 95% interval over positions |
| `above_best_of_all_quantities_threshold` / `beats_distance_baseline` / `diff_vs_distance_baseline_ci_lo` | threshold flag, beats-the-distance flag and the lower end of the difference in correlation |
| `rho_signed_delta` | correlation of the signed change |
| `auroc` / `auroc_ci_lo` / `auroc_ci_hi` | AUROC of the binary contrast with 95% interval; the columns that follow (threshold, beats-the-distance flag and difference against the distance baseline) are for the AUROC |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `rank` | `metric_name` | `role` | `rho` | `rho_ci_lo` | `rho_ci_hi` |
|----------|----------|----------|----------|----------|----------|
| `1` | `propka_catalytic_pka_range` | `main` | `0.48` | `0.3474` | `0.592` |
| `2` | `propka_catalytic_pka_min` | `main` | `0.4622` | `0.3224` | `0.5748` |
| `3` | `propka_catalytic_shift_absmax` | `main` | `0.4587` | `0.319` | `0.5782` |

:::

**Notes.**

- Aggregates of D2DCure data (licence unstated); no per-variant rows.


### Table S17. BglB: all 84 structure-space and comparator metrics {#S17}

::: {.tmeta}

**File.** `supplementary/S17_bglb_all_metrics.csv` · 84 rows × 29 columns · D2DCure aggregate (licence of the source data unstated; aggregates only, no per-variant rows)

**Supports.** Results 3.3.1; Methods 2.4.1. **Cited in.** Methods [2.4.1](https://pdflink.invalid/paper.pdf#page=6); Results [3.3.1](https://pdflink.invalid/paper.pdf#page=17).

**A row is** one metric analysed on the 432 BglB variants (84 in all).

:::

Spearman correlation, signed, direction-free and magnitude AUROC with intervals, the paired difference against the distance baseline and whether the metric beats all baselines, for every structure-space metric and comparator (36 site-scoped, 28 sequence-only, 15 whole-protein, 5 bookkeeping). None beats all baselines.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric` / `canonical_key` / `input_class` / `in_main_set` | the metric, its class and main-set membership |
| `rho` / `rho_lo` / `rho_hi` | Spearman correlation with 95% interval over positions |
| `auc_signed` / `auc_dirfree` / auc_mag (+ _lo, _hi) | AUROC of the binary contrast using the signed change, the direction-free form and the magnitude, with intervals |
| `diff_vs_neg_d_cat_lo` / `beats_all_baselines` | lower end of the difference against the distance baseline; whether the metric beats all five baselines |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where in_main_set = 1).

::: {.excerpt}

| `metric` | `in_main_set` | `rho` | `rho_lo` | `rho_hi` | `beats_all_baselines` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_frac_buried` | `1` | `-0.1909` | `-0.3048` | `-0.057` | `0` |
| `catalytic_pairwise_dist_max` | `1` | `0.0431` | `-0.1841` | `0.2709` | `0` |
| `catalytic_pairwise_dist_mean` | `1` | `0.09` | `-0.074` | `0.2468` | `0` |

:::

**Notes.**

- Aggregates of D2DCure data (licence unstated); no per-variant rows.


### Table S18. BglB: sensitivity analyses {#S18}

::: {.tmeta}

**File.** `supplementary/S18_bglb_sensitivities.csv` · 11 rows × 22 columns · D2DCure aggregate (licence of the source data unstated; aggregates only, no per-variant rows)

**Supports.** Results 3.3.1. **Cited in.** Methods [2.4.1](https://pdflink.invalid/paper.pdf#page=6); Results [3.3.1](https://pdflink.invalid/paper.pdf#page=17).

**A row is** the main analysis and one of ten sensitivity analyses (11 rows).

:::

The main analysis and ten sensitivity analyses with their sizes, the number of metrics with an interval above 0.5, the number that beat the distance baseline and the AUROC of the distance baseline. The analyses are: the main analysis (432 variants); variants near to and distal from the catalytic residues (144 and 288); variants with a measured stability (292); each institution left out in turn (FIU, MiraCosta, UC Davis); other thresholds for the impaired label (1 and 3 standard deviations, with 173 and 139 impaired variants); responding metrics only (70 metrics analysed); and without the variants at catalytic positions (431 variants, one position removed). In every analysis no metric beats the distance baseline.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis` | the analysis |
| `n_variants` / `n_positions` / `n_impaired` / `n_wtlike` | size of the analysis |
| `n_metrics_analysed` / `n_auc_mag_ci_above_half` | metrics analysed and metrics whose AUROC interval lies above 0.5 |
| `n_beats_neg_d_cat` / `n_beats_all_baselines` | metrics that beat the distance baseline and all baselines |
| `auc_neg_d_cat_baseline` | AUROC of the distance baseline |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `analysis` | `n_variants` | `n_positions` | `n_impaired` | `n_wtlike` | `n_beats_neg_d_cat` |
|----------|----------|----------|----------|----------|----------|
| `main analysis` | `432` | `175` | `166` | `254` | `0` |
| `variants distal from the catalyti…` | `288` | `136` | `71` | `207` | `0` |
| `variants near the catalytic resid…` | `144` | `39` | `95` | `47` | `0` |

:::

**Notes.**

- Aggregates of D2DCure data (licence unstated); no per-variant rows.


### Table S19. BglB: prediction-based metrics (Chai-1 with the assay substrate) {#S19}

::: {.tmeta}

**File.** `supplementary/S19_bglb_prediction_based_all_metrics.csv` · 28 rows × 29 columns · D2DCure aggregate (licence of the source data unstated; aggregates only, no per-variant rows)

**Supports.** Results 3.3.1; Methods 2.4.1. **Cited in.** Methods [2.4.1](https://pdflink.invalid/paper.pdf#page=6); Results [3.3.1](https://pdflink.invalid/paper.pdf#page=17).

**A row is** one prediction-based metric analysed on the 432 BglB variants (28 in all).

:::

The same columns as [S17](#S17) for the metrics computed from Chai-1 predictions of each variant with the assay substrate (pNPG, no metal); active-site accuracy is measured against the wild-type crystal, which carries a covalent glucosyl intermediate. Twelve rows are main-set metrics; the largest correlation is 0.17.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric` / `canonical_key` / `input_class` / `in_main_set` | the metric, its class and main-set membership |
| `rho` / `rho_lo` / `rho_hi` | Spearman correlation with 95% interval over positions |
| `auc_signed` / `auc_dirfree` / auc_mag (+ _lo, _hi) | AUROC of the binary contrast |
| `beats_all_baselines` | whether the metric beats all five baselines |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where in_main_set = 1).

::: {.excerpt}

| `metric` | `in_main_set` | `rho` | `rho_lo` | `rho_hi` |
|----------|----------|----------|----------|----------|
| `ame_crystal_clash_max` | `1` | `0.0828` | `-0.0534` | `0.2162` |
| `ame_crystal_rmsd_max` | `1` | `0.0632` | `-0.0622` | `0.1849` |
| `ame_crystal_rmsd_mean` | `1` | `0.1213` | `-0.0079` | `0.259` |

:::

**Notes.**

- Aggregates of D2DCure data (licence unstated); no per-variant rows.


### Table S20. Plated designs: hits per 96-well plate for every metric (filter-style analysis) {#S20}

::: {.tmeta}

**File.** `supplementary/S20_plates_hits_per_plate_ranked.csv` · 128 rows × 37 columns · public

**Supports.** Results 3.3.2; Methods 2.4.2 (Eqs. 16 and 17). **Cited in.** Methods [2.4.2](https://pdflink.invalid/paper.pdf#page=8); Results [3.3.2](https://pdflink.invalid/paper.pdf#page=18).

**A row is** one metric scored on the 192 designs (128 in all).

:::

The filter-style analysis, for every metric: the expected hits per 96-well plate and the actives among the 48 designs kept when the quarter of designs that the metric ranks highest, or lowest, fills the plate (8.0 hits when unfiltered), each with a 90% interval over designs, ranked by the better end. 30 metrics exceed the random-filter band (14.0 hits).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `rank` / `rank_among_ranked_items` / `ranked_item` | rank among 128, rank among the 36 items of Table 9 and whether the metric is one of them |
| `metric_name` / `canonical_key` / `source` / `input_class` / `role` | the metric and its class |
| `n_designs` / `n_active` / `n_kept_highest` / `n_kept_lowest` | 192, 16 and the number kept (fewer than 48 when designs tie at the cut) |
| `hits_highest_quarter` / `hits_highest_ci_lo90` / `hits_highest_ci_hi90` / `actives_in_highest_quarter` | hits per plate for the highest quarter, 90% interval and actives kept |
| `hits_lowest_quarter` / `hits_lowest_ci_lo90` / `hits_lowest_ci_hi90` / `actives_in_lowest_quarter` | the same for the lowest quarter |
| `better_end` / `best_hits_per_plate` / `above_random_band` | the better end, its hits per plate and whether it exceeds the random band |
| `note` | for example a tie at the cut |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `rank` | `metric_name` | `role` | `better_end` | `best_hits_per_plate` | `above_random_band` |
|----------|----------|----------|----------|----------|----------|
| `1` | `frac_Y` | `reference` | `highest` | `24.0` | `1` |
| `2` | `frac_G` | `supp_global` | `lowest` | `22.0` | `1` |
| `3` | `rosetta_cat_fa_intra_rep` | `main` | `lowest` | `22.0` | `1` |

:::

**Notes.**

- Descriptive only: no hypothesis test.


### Table S21. Plated designs: every metric ranked by correlation with kcat/KM among the 16 designs that have a value (complete Table 9) {#S21}

::: {.tmeta}

**File.** `supplementary/S21_plates_all_metrics_ranked.csv` · 106 rows × 29 columns · public

**Supports.** Results 3.3.2; the complete version of Table 9. **Cited in.** Methods [2.4.2](https://pdflink.invalid/paper.pdf#page=8); Results [3.3.2](https://pdflink.invalid/paper.pdf#page=18).

**A row is** one metric with a rank correlation on the 16 designs with a reported kcat/KM (106 in all).

:::

Every metric that has a correlation, ranked by the size of the Spearman correlation with log10 kcat/KM, with a 90% interval over designs, whether the interval excludes 0 (33 do), the direction, and the correlation with the sequence length partialled out and whether it survives that control.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `rank` / `rank_in_table_9` / `in_table_9` | rank among 106, rank among the 36 items of Table 9 and membership of Table 9 |
| `metric_name` / `canonical_key` / `source` / `input_class` / `role` | the metric and its class |
| `n_designs` / `rho` / `rho_ci_lo90` / `rho_ci_hi90` | 16 designs, Spearman correlation and 90% interval over designs |
| `interval_excludes_zero` / `higher_value_means` | whether the interval excludes 0 and whether a larger value means higher or lower activity |
| `rho_given_length` / `survives_length_control` | correlation with the sequence length partialled out of both sides, and whether it survives |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `rank` | `metric_name` | `rho` | `rho_ci_lo90` | `rho_ci_hi90` | `higher_value_means` |
|----------|----------|----------|----------|----------|----------|
| `1` | `frac_I` | `-0.7821` | `-0.9494` | `-0.5042` | `lower activity` |
| `2` | `frac_A` | `0.776` | `0.4627` | `0.9348` | `higher activity` |
| `3` | `rosetta_omega` | `-0.7756` | `-0.8904` | `-0.5` | `lower activity` |

:::

**Notes.**

- Descriptive only; about 10% of unrelated metrics are expected to have an interval that excludes 0.


### Table S22. Plated designs: ordering among the 16 active designs, structure-space metrics and comparators {#S22}

::: {.tmeta}

**File.** `supplementary/S22_plates_ordering.csv` · 81 rows × 23 columns · public

**Supports.** Results 3.3.2; Methods 2.4.2 (Eq. 15). **Cited in.** Methods [2.4.2](https://pdflink.invalid/paper.pdf#page=8); Results [3.3.2](https://pdflink.invalid/paper.pdf#page=18).

**A row is** one metric of the structure-space panel or a comparator (81 in all).

:::

The Spearman correlation with log kcat/KM among the 16 active designs with and without the sequence length partialled out, with 90% intervals and whether the interval excludes 0 (24 do).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_name` / `canonical_key` / `input_class` / `in_main_set` | the metric and its class |
| `spearman_rho` / `rho_lo90` / `rho_hi90` / `excludes_zero` | correlation, 90% interval and whether it excludes 0 |
| `rho_given_length` / `survives_length_control` | correlation with length partialled out and whether it survives |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where in_main_set = 1).

::: {.excerpt}

| `metric_name` | `in_main_set` | `spearman_rho` | `rho_lo90` | `rho_hi90` | `rho_given_length` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_polar_contacts` | `1` | `0.6711` | `0.4115` | `0.8501` | `0.5183` |
| `rosetta_catalytic_vdw_net` | `1` | `-0.6299` | `-0.8777` | `-0.2414` | `-0.4743` |
| `rosetta_cat_fa_sol` | `1` | `0.5651` | `0.1543` | `0.8487` | `0.538` |

:::


### Table S23. Plated designs: enrichment at every keep fraction, structure-space metrics {#S23}

::: {.tmeta}

**File.** `supplementary/S23_plates_enrichment.csv` · 816 rows × 27 columns · public

**Supports.** Results 3.3.2; Methods 2.4.2. **Cited in.** Methods [2.4.2](https://pdflink.invalid/paper.pdf#page=8); Results [3.3.2](https://pdflink.invalid/paper.pdf#page=18).

**A row is** one metric, one direction (keep the highest or the lowest values) and one keep fraction (816 rows).

:::

Enrichment on the 192 plated designs for the 102 metrics of the structure-space panel and its comparators, in both directions and at keep fractions of 5, 10, 25 and 50%: the number kept, the actives kept and the expected hits per 96-well plate with a 90% interval against the unfiltered 8.0.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric` / `canonical_key` / `input_class` / `in_main_set` | the metric |
| `direction` / `keep_fraction` / `n_kept` | keep the highest or the lowest values; the fraction and the number of designs kept |
| `n_active_kept` / `n_active_total` | actives among those kept, and 16 |
| `expected_hits_per_plate` / `hits_lo90` / `hits_hi90` | expected hits per plate with 90% interval |
| `baseline_hits_per_plate` / `enrichment_vs_baseline` | 8.0 and the ratio to it |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where in_main_set = 1, keep_fraction = 0.25).

::: {.excerpt}

| `metric` | `direction` | `keep_fraction` | `n_kept` | `n_active_kept` | `expected_hits_per_plate` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_frac_buried` | `low` | `0.25` | `48` | `2` | `4.0` |
| `catalytic_frac_buried` | `high` | `0.25` | `48` | `1` | `2.0` |
| `catalytic_pairwise_dist_max` | `low` | `0.25` | `48` | `3` | `6.0` |

:::

**Notes.**

- Descriptive only. Released as a CSV only for the full 816 rows.


### Table S24. Plated designs: enrichment for prediction-based metrics {#S24}

::: {.tmeta}

**File.** `supplementary/S24_plates_prediction_based_enrichment.csv` · 232 rows × 27 columns · public

**Supports.** Results 3.3.2; Methods 2.4.2. **Cited in.** Methods [2.4.2](https://pdflink.invalid/paper.pdf#page=8); Results [3.3.2](https://pdflink.invalid/paper.pdf#page=18).

**A row is** one prediction-based metric, one direction and one keep fraction (232 rows).

:::

The same as [S23](#S23) for the 29 prediction-based metrics (Chai-1 with the transition-state analogue and zinc; active-site accuracy against the design's own model).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric` / `canonical_key` / `input_class` / `in_main_set` | the metric |
| `direction` / `keep_fraction` / `n_kept` / `n_active_kept` | as in [S23](#S23) |
| `expected_hits_per_plate` / `hits_lo90` / `hits_hi90` / `enrichment_vs_baseline` | expected hits per plate, 90% interval and ratio to 8.0 |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where keep_fraction = 0.25, direction = high).

::: {.excerpt}

| `metric` | `direction` | `keep_fraction` | `n_active_kept` | `expected_hits_per_plate` |
|----------|----------|----------|----------|----------|
| `chai_plddt_mean` | `high` | `0.25` | `8` | `16.0` |
| `chai_ptm_mean` | `high` | `0.25` | `9` | `18.0` |
| `frac_Y` | `high` | `0.25` | `12` | `24.0` |

:::

**Notes.**

- Descriptive only (16 active designs).


### Table S25. Sanity floors by class of metric {#S25}

::: {.tmeta}

**File.** `supplementary/S25_sanity_floor_by_input_class.csv` · 53 rows × 8 columns · public

**Supports.** Methods 2.5 (detection floor); Results 3.4.1. **Cited in.** Methods [2.5](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one sanity-floor condition on one data set and one class of metric (53 rows).

:::

The sanity-floor conditions (all catalytic residues replaced by Gly, scrambled sequence on the native backbone, unrelated protein, ligand removed on the pilot set) for the 143-enzyme set, the shortened-motif set, the pilot set and the de novo set: how many metrics of each class were scored and how many responded. One row reconciles the detection floor with the Gly step: the responses are identical on 98 of 98 metrics (the same change scored twice).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `dataset` / `condition` / `input_class` | the data set, the condition and the class of metric |
| `n_metrics` / `n_scored` / `n_responds` / `n_unscored` | metrics in the class, scored, responding and not scored |
| `note` | remarks, including the reconciliation |

:::

**Excerpt** (first 3 rows where dataset = main set (143), condition = cat_to_gly).

::: {.excerpt}

| `dataset` | `condition` | `input_class` | `n_metrics` | `n_scored` | `n_responds` |
|----------|----------|----------|----------|----------|----------|
| `main set (143)` | `cat_to_gly` | `bookkeeping` | `20` | `20` | `8` |
| `main set (143)` | `cat_to_gly` | `seq_only` | `29` | `29` | `10` |
| `main set (143)` | `cat_to_gly` | `struct_site` | `34` | `26` | `25` |

:::


### Table S26. Control matching: the loosest tier needed {#S26}

::: {.tmeta}

**File.** `supplementary/S26_control_match_tiers.csv` · 81 rows × 6 columns · public

**Supports.** Methods 2.5; Results 3.4.1. **Cited in.** Methods [2.5](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one analysis, lesion test and matching tier (81 rows).

:::

For each analysis and lesion test, how many (enzyme, step) entries needed each loosest matching tier: 0 = exact match, tiers 3 and above drop packing matching, tier 5 also relaxes burial (main set only), -1 = no control found; and the share of the lesion test.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis_set` / `lesion_test` | the analysis (data set and controls) and the lesion test (catalytic lesion, second-shell lesion or the retired deformation experiment) |
| `worst_tier` / `n_entries` / `share_of_lesion_test` | loosest tier used, number of entries and their share of the lesion test |
| `note` | definition of the tiers |

:::

**Excerpt** (first 3 rows where analysis_set = main set, packing-matched controls, lesion_test = catalytic lesion).

::: {.excerpt}

| `analysis_set` | `lesion_test` | `worst_tier` | `n_entries` | `share_of_lesion_test` |
|----------|----------|----------|----------|----------|
| `main set, packing-matched controls` | `catalytic lesion` | `-1.0` | `8` | `0.0035` |
| `main set, packing-matched controls` | `catalytic lesion` | `0.0` | `226` | `0.0997` |
| `main set, packing-matched controls` | `catalytic lesion` | `2.0` | `496` | `0.2189` |

:::


### Table S27. Control matching: balance of residues changed in the two arms {#S27}

::: {.tmeta}

**File.** `supplementary/S27_control_arm_balance.csv` · 15 rows × 9 columns · public

**Supports.** Methods 2.5; Results 3.4.1. **Cited in.** Methods [2.5](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one analysis and lesion test (15 rows).

:::

The share of (enzyme, step) pairs in which the control arm changed fewer or more residues than the catalytic arm, the median and mean ratio, and the number with no control. The comparison of medians used elsewhere cannot see this imbalance.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis_set` / `lesion_test` / `pairs` | the analysis, the lesion test and the number of pairs |
| `control_fewer_share` / `control_more_share` | shares with fewer or more residues changed in the control arm |
| `median_ratio` / `mean_ratio` / `catalytic_only_no_control` | ratio of residues changed and pairs with no control |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `analysis_set` | `lesion_test` | `pairs` | `control_fewer_share` | `control_more_share` | `median_ratio` |
|----------|----------|----------|----------|----------|----------|
| `pilot set` | `catalytic lesion` | `212` | `0.1981` | `0.0` | `1.0` |
| `pilot set` | `second-shell lesion` | `159` | `0.0` | `0.0` | `1.0` |
| `pilot set` | `deformation` | `205` | `0.0` | `0.0` | `1.0` |

:::


### Table S28. Catalytic lesion: every metric scored (Table 10 plus supplementary comparators and per-step flags) {#S28}

::: {.tmeta}

**File.** `supplementary/S28_catalytic_lesion_all_metrics_ranked.csv` · 43 rows × 73 columns · public

**Supports.** Results 3.4.1; the complete version of Table 10. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric scored on the catalytic-lesion ladder (43 in all).

:::

Table 10 with the 8 supplementary comparators and every flag that decides whether a step counts. Metrics are grouped by the lesion step at which they are first detected and ranked by the mean of the rank statistic R over the counted steps. For each step (isosteric 15.3, non-isosteric 36.4, Ala 53.2, Gly 80.5 A3) it gives R with interval, the number of informative proteins and the flags that the metric responds, that the control response is above its noise and that the metric is specific; the number of steps counted; the first step detected and the first step at which the metric is specific (the onset of specificity); the mean R of the 143 main enzymes alone; and, for the prediction-based metrics, the distance-matched R. Structure-space metrics: 195 pooled natural enzymes (143 main + 52 pilot); prediction-based: 59 enzymes, 286 pairs.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `detection_group` / `rank_in_group` / `rank` / `rank_in_table_10` | group by first detected step, rank in the group, overall rank and rank among the 35 items of Table 10 |
| `metric_name` / `canonical_key` / `source` / `input_class` / `role` / `in_ranked_set` | the metric, class, role and whether it is one of the 35 ranked items |
| `n_steps` / `n_steps_interpretable` | steps with a value and steps counted |
| `r_mean` / `r_lo` / `r_hi` | mean R over counted steps with 95% interval over enzyme sub-subclasses |
| r_<step> / _lo / _hi / n_<step> | R, interval and informative proteins for isosteric, non_isosteric, ala and gly |
| responds_<step> / control_above_noise_<step> / specific_<step> | the per-step flags |
| `first_step_detected` / `first_step_specific` | onsets of detection and of specificity |
| `r_matched` / `n_pairs_matched` / `n_systems_matched` | distance-matched R and its size (prediction-based metrics) |
| `r_mean_primary_only` / `above_best_of_all_quantities_threshold` | mean R of the 143 main enzymes and the best-of-N flag |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `detection_group` | `rank_in_group` | `metric_name` | `r_mean` | `r_lo` | `r_hi` |
|----------|----------|----------|----------|----------|----------|
| `isosteric` | `1` | `chai_per_chain_ptm_min_mean` | `0.7524` | `0.6768` | `0.8238` |
| `isosteric` | `2` | `propka_catalytic_pka_range` | `0.6834` | `0.5759` | `0.7806` |
| `isosteric` | `3` | `chai_iptm_mean` | `0.6732` | `0.5991` | `0.7463` |

:::

**Notes.**

- Descriptive of a pooled set. [S29](#S29) and [S30](#S30) hold the specificity-ratio analysis.


### Table S29. Structure-space specificity by metric family and lesion step, with the panel statistic and sensitivity sets {#S29}

::: {.tmeta}

**File.** `supplementary/S29_specificity_by_family_and_step.csv` · 20 rows × 27 columns · public

**Supports.** Results 3.4.1 and 3.4.2. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19), [3.4.2](https://pdflink.invalid/paper.pdf#page=21).

**A row is** one family of metrics at one lesion step or dose (20 rows).

:::

The number of eligible, responding and specific structure-space metrics (as distinct metrics) by family (site-scoped Rosetta energy, catalytic geometry, catalytic pKa, all main-set metrics) at each step of the catalytic lesion and each second-shell dose, the geometric-mean specificity ratio of the main-set panel (isosteric, 1.075 [0.958, 1.178]), and the counts in four sensitivity sets (shortened motif, no packing matching or count gate, pilot set, de novo designs). At the isosteric step 23 of 29 metrics respond and none is specific; specificity appears for 5 metrics at the non-isosteric step and for 8 at the Ala and Gly steps.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `family` / `lesion_test` / `level` / `dose_value` / `dose_unit` | family, lesion test (catalytic lesion or second-shell lesion), step or dose and its size |
| `n_eligible_keys` / `n_responds_keys` / `n_specific_keys` / `n_cells` | counts as distinct metrics, and cells |
| `sr_geomean_ci90` | geometric-mean specificity ratio of the panel with 90% interval |
| `sens_shortened_motif` / `sens_no_packing_match` / `sens_pilot_set` / `sens_de_novo_set` | specific / eligible in the shortened-motif, no-packing-match, pilot and de novo sets |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where lesion_test = catalytic lesion).

::: {.excerpt}

| `family` | `level` | `n_eligible_keys` | `n_responds_keys` | `n_specific_keys` | `sens_shortened_motif` |
|----------|----------|----------|----------|----------|----------|
| `Rosetta energy (site-scoped)` | `isosteric` | `15` | `13` | `0` | `0 of 15` |
| `Catalytic geometry (site-scoped)` | `isosteric` | `8` | `5` | `0` | `0 of 8` |
| `Catalytic pKa` | `isosteric` | `6` | `5` | `0` | ` ` |

:::


### Table S30. Re-predicted catalytic lesion: the prediction-based metrics under three successive controls and the pre-specified rule {#S30}

::: {.tmeta}

**File.** `supplementary/S30_predictor_ladder_three_controls.csv` · 6 rows × 23 columns · public

**Supports.** Results 3.4.1; Methods 2.5.1 (Eq. 24). **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one prediction-based metric or reference row (6 rows).

:::

Specificity of the prediction-based metrics on the natural arm of the re-predicted ladder (59 enzymes, 286 pairs): the specificity ratio on the isosteric step with the original control, in the distance-matched subset (68 pairs, 21 systems) and after regression adjustment on all steps (with the unadjusted ratio on the same pairs), and the label of the rule specified before the analysis. The ratio of the interface terms falls once the control is matched or adjusted on the distance to the ligand (ipTM: 1.96 with the original control, 0.47 in the distance-matched subset and 1.18 after adjustment); no interface term meets the rule.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric` / `role` | the metric and main or reference |
| `n_pairs_isosteric` / `n_systems_isosteric` | pairs and systems at the isosteric step |
| `sr_mean_isosteric_original_control` | specificity ratio with the original control |
| `distance_matched_k_of_N` / `sr_distance_matched` | size of the distance-matched subset and the ratio in it |
| `unadjusted_gmr_all_steps` / `adjusted_gmr_all_steps` | geometric-mean ratio over all steps, unadjusted and adjusted for distance and burial |
| `rule_label` | the label from the pre-specified rule (lower 90% bound above 1.2 with at least 30 pairs in 15 systems) |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `metric` | `sr_mean_isosteric_original_control` | `sr_distance_matched` | `adjusted_gmr_all_steps` | `rule_label` |
|----------|----------|----------|----------|----------|
| `ame_crystal_clash_max` | `1.84 [1.31, 2.69]` | `1.05 [0.79, 1.39]` | `1.18 [0.95, 1.46]` | `testable; not specific (lower 90%…` |
| `ame_crystal_rmsd_min` | `2.67 [1.02, 4.74]` | `0.98 [0.68, 1.21]` | `1.90 [1.40, 2.53]` | `knockon_displacement_no_specifici…` |
| `chai_iptm_mean` | `1.96 [1.44, 2.71]` | `0.47 [0.24, 1.04]` | `1.18 [0.85, 1.60]` | `testable; not specific (lower 90%…` |

:::


### Table S31. Sensitivity of the specificity-ratio counts to motif size, packing matching and count gating {#S31}

::: {.tmeta}

**File.** `supplementary/S31_motif_packing_sensitivity.csv` · 20 rows × 7 columns · public

**Supports.** Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one analysis and one lesion step (20 rows).

:::

Counts of eligible, responding and specific metrics at each step for five analyses: the pilot set, the main set without packing matching or count gating, the main set with packing-matched controls (primary), the main set with the motif shortened to at most 3 residues, and the 30 de novo designs with a created-site control.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `reader_name` / `motif_and_controls` | the analysis and how its motif and controls are defined |
| `level` | lesion step |
| `n_eligible_keys` / `n_responds_keys` / `n_specific_keys` / `n_cells` | counts as distinct metrics, and cells |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `reader_name` | `level` | `n_eligible_keys` | `n_responds_keys` | `n_specific_keys` |
|----------|----------|----------|----------|----------|
| `pilot set` | `isosteric` | `23` | `12` | `0` |
| `pilot set` | `non_isosteric` | `23` | `12` | `0` |
| `pilot set` | `ala` | `23` | `14` | `0` |

:::


### Table S32. Re-predicted ladder: seed-noise context {#S32}

::: {.tmeta}

**File.** `supplementary/S32_replicate_noise_context.csv` · 56 rows × 12 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one prediction-based metric in one arm and subset (56 rows).

:::

Noise context from the second-seed replicate on 30 natural pairs: the median absolute change in each arm against the seed noise of the metric, for the nine prediction-based metrics, on all pairs and on the original matched subset.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `metric_name` / `subset` / `arm` | natural or de novo, the metric, all_pairs or M0_matched, and catalytic or control |
| `k_pairs` / `N_pairs` / `k_systems` / `N_systems` | pairs and systems |
| `median_abs_delta` / `median_sigma_native` / `frac_abs_delta_gt_sigma_native` | median absolute change, the metric's seed noise and the share of pairs whose change exceeds it |

:::

**Excerpt** (first 3 rows where source = natural, subset = all_pairs).

::: {.excerpt}

| `metric_name` | `subset` | `arm` | `median_abs_delta` | `median_sigma_native` | `frac_abs_delta_gt_sigma_native` |
|----------|----------|----------|----------|----------|----------|
| `chai_iptm_mean` | `all_pairs` | `catalytic` | `0.00666` | `0.00154` | `0.8292` |
| `chai_iptm_mean` | `all_pairs` | `control` | `0.00254` | `0.00154` | `0.6797` |
| `chai_aggregate_score_mean` | `all_pairs` | `catalytic` | `0.00556` | `0.00127` | `0.8392` |

:::


### Table S33. Specificity ratio of every eligible metric at every step {#S33}

::: {.tmeta}

**File.** `supplementary/S33_eligible_metrics.csv` · 256 rows × 29 columns · public

**Supports.** Methods 2.5.1 (Eq. 22); Results 3.4.1 and 3.4.2. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19), [3.4.2](https://pdflink.invalid/paper.pdf#page=21).

**A row is** one eligible (site-scoped) metric at one lesion step or dose (256 rows).

:::

The median change at the catalytic lesion and its interval, the specificity ratio with 95% interval, whether the metric responds and whether it is specific, and the verdict: specific, non_specific, blind (does not respond), invariant (does not change) or below the floor of five units. Steps of the catalytic lesion are isosteric, non_isosteric, ala, gly; second-shell doses are second_shell_1, _2, _4.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `canonical_key` / `metric_name` / `input_class` / `in_main_set` | the metric (aliases collapse in canonical_key) |
| `lesion_test` / `level` / `n_systems` | catalytic lesion or second-shell lesion, the step or dose and the number of enzymes |
| `delta_median` / `delta_ci_lo` / `delta_ci_hi` | median change at the catalytic lesion with interval |
| `sr_median` / `sr_ci_lo` / `sr_ci_hi` | specificity ratio with 95% interval |
| `responds` / `specific` / `verdict` / `applicability_status` | the flags, the verdict and the applicability status |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where in_main_set = 1, level = ala).

::: {.excerpt}

| `canonical_key` | `lesion_test` | `level` | `n_systems` | `sr_median` | `verdict` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_frac_buried` | `catalytic lesion` | `ala` | `143` | `1.9091` | `specific` |
| `catalytic_pairwise_dist_max` | `catalytic lesion` | `ala` | `124` | `0.0` | `blind` |
| `catalytic_pairwise_dist_mean` | `catalytic lesion` | `ala` | `124` | `0.7262` | `non_specific` |

:::


### Table S34. Specificity ratio of whole-protein and sequence-only comparators at every step {#S34}

::: {.tmeta}

**File.** `supplementary/S34_global_comparators.csv` · 308 rows × 29 columns · public

**Supports.** Methods 2.5.1; Results 3.4. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19), [3.4.2](https://pdflink.invalid/paper.pdf#page=21).

**A row is** one comparator metric at one lesion step or dose (308 rows).

:::

The same cells as [S33](#S33) for the whole-protein and sequence-only metrics, which are not in the main set. They show that composition metrics have a ratio of 1 by construction and that whole-protein energies move with the lesion.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `canonical_key` / `metric_name` / `input_class` | the comparator |
| `lesion_test` / `level` / `n_systems` | as in [S33](#S33) |
| delta_*, sr_*, responds, specific, verdict | as in [S33](#S33) |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows where level = ala).

::: {.excerpt}

| `canonical_key` | `lesion_test` | `level` | `n_systems` | `sr_median` | `verdict` |
|----------|----------|----------|----------|----------|----------|
| `frac_A` | `catalytic lesion` | `ala` | `143` | `1.1744` | `non_specific` |
| `frac_C` | `catalytic lesion` | `ala` | `143` | `nan` | `blind` |
| `frac_D` | `catalytic lesion` | `ala` | `143` | `0.9842` | `non_specific` |

:::


### Table S35. The specific cells that survive the controls {#S35}

::: {.tmeta}

**File.** `supplementary/S35_survivors_by_status.csv` · 97 rows × 10 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric at one step in one analysis (97 rows: 74 natural, 23 de novo).

:::

The cells that are specific under the control of their analysis, with the specificity ratio, the population (natural or de novo) and the applicability status of the metric. Of the 97, 69 are of metrics with status OK, 27 of whole-protein comparators (GLOBAL) and 1 of a metric with too little coverage.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis_set` / `lesion_test` / `level` | the analysis, the lesion test and the step |
| `metric_name` / `canonical_key` / `input_class` / `in_main_set` | the metric |
| `sr_text` | specificity ratio with interval, as text |
| `applicability_status` / `population` | applicability status and natural or de novo |

:::

**Excerpt** (first 3 rows where analysis_set = main set, packing-matched controls, in_main_set = 1).

::: {.excerpt}

| `analysis_set` | `lesion_test` | `level` | `metric_name` | `sr_text` | `population` |
|----------|----------|----------|----------|----------|----------|
| `main set, packing-matched controls` | `catalytic lesion` | `ala` | `catalytic_frac_buried` | `1.91 [1.4, 2.72]` | `natural` |
| `main set, packing-matched controls` | `catalytic lesion` | `ala` | `catalytic_radius_of_gyration` | `1.76 [1.43, 2.19]` | `natural` |
| `main set, packing-matched controls` | `catalytic lesion` | `ala` | `catalytic_rel_sasa_mean` | `2.4 [1.93, 3.03]` | `natural` |

:::


### Table S36. Rank statistic R per lesion step on the 143 main enzymes {#S36}

::: {.tmeta}

**File.** `supplementary/S36_ranking_statistic_by_lesion_step.csv` · 313 rows × 14 columns · public

**Supports.** Methods 2.5.1 (Eq. 19). **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric at one step of the catalytic lesion (313 rows).

:::

The rank statistic R (probability that a metric changes more at the catalytic lesion than at the matched control) for the 143 main enzymes alone, with 90% intervals, for 83 distinct metrics including comparators. This is the per-step form of R on the main enzymes; Table 10 and [S28](#S28) report the pooled analysis on 195 enzymes with 95% intervals and the counted-step rule, so the values for the same metric differ.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_name` / `canonical_key` / `input_class` / `in_main_set` | the metric |
| `lesion_step` / `volume_A3` | lesion step and its median side-chain volume change |
| `R` / `R_lo90` / `R_hi90` / `n_systems` / `n_clusters` | R with 90% interval, enzymes and enzyme sub-subclasses |
| `responds` / `interpretable` | whether the metric responds and whether R is interpretable |
| `applicability_status` | applicability status |

:::

**Excerpt** (first 3 rows where in_main_set = 1, lesion_step = ala).

::: {.excerpt}

| `metric_name` | `lesion_step` | `R` | `R_lo90` | `R_hi90` | `n_systems` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_frac_buried` | `ala` | `0.7557` | `0.686` | `0.8189` | `131` |
| `catalytic_pairwise_dist_max` | `ala` | `0.203` | `0.1522` | `0.2574` | `133` |
| `catalytic_pairwise_dist_mean` | `ala` | `0.3262` | `0.2553` | `0.4` | `141` |

:::


### Table S37. Re-predicted ladder: distance of the substituted and control residues to the ligand {#S37}

::: {.tmeta}

**File.** `supplementary/S37_ladder_pair_distances.csv` · 312 rows × 34 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one catalytic/control pair of the ladder (312 pairs: 286 natural, 26 de novo).

:::

For every pair the residue types, the burial of each residue, the distance of the substituted and of the control residue to the ligand (in the reference structure and in the prediction), whether the control is adjacent to a catalytic residue, and whether the pair falls in each of the calipers used in [S40](#S40).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `base_system` / `level` | natural or denovo, the system and the lesion step |
| `wt` / `new_aa` / `cat_position` / `ctl_position` | residue substituted and its position in the catalytic and control arms |
| `cat_rel_sasa` / `ctl_rel_sasa` / `abs_diff_rel_sasa` | relative accessible area of the two residues and the difference |
| `d_lig_cat_ref` / `d_lig_ctl_ref` / `abs_diff_d_lig_ref` | distance to the ligand in the reference structure (A) |
| `d_lig_cat_chai` / `d_lig_ctl_chai` | distance in the Chai-1 prediction |
| `control_adjacent_to_catalytic` / `ligand_status` | adjacency to a catalytic residue; whether the ligand could be located |
| in_caliper_* | membership of the primary caliper and of sensitivity calipers |

:::

**Excerpt** (first 3 rows where source = natural, level = isosteric, ligand_status = ok).

::: {.excerpt}

| `base_system` | `level` | `wt` | `new_aa` | `d_lig_cat_ref` | `d_lig_ctl_ref` | `abs_diff_rel_sasa` |
|----------|----------|----------|----------|----------|----------|----------|
| `M0024_1nzy_a2` | `isosteric` | `F` | `L` | `3.433` | `24.224` | `0.0031` |
| `M0024_1nzy_a2` | `isosteric` | `F` | `Y` | `3.433` | `10.504` | `0.0008` |
| `M0050_1dbt_a1` | `isosteric` | `D` | `N` | `3.703` | `17.378` | `0.0002` |

:::

**Notes.**

- Released as a CSV only for the full 312 rows.


### Table S38. Re-predicted ladder: candidates for a new distance-matched control {#S38}

::: {.tmeta}

**File.** `supplementary/S38_new_distance_matched_controls.csv` · 291 rows × 17 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one candidate control for one pair that had no control within the caliper (291 rows).

:::

The candidate controls for the pairs that had none in the caliper, which were selected (54 pairs, 53 new predictions), their distances and burial, and the reason when none was selected (no candidate in the caliper for 213 pairs; no reference distance for 20; no ligand in the baseline prediction for 4).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `base_system` / `source` / `level` | system, natural or de novo, step |
| `wt` / `new_aa` / `cat_position` / `orig_ctl_position` / `new_ctl_position` | the substitution and the original and new control positions |
| `d_lig_cat_ref` / `d_lig_ctl_new` / `abs_diff_d` | distances to the ligand and their difference |
| `cat_rel_sasa` / `ctl_rel_sasa_new` / `abs_diff_rel` | burial and its difference |
| `n_candidates` / `selected` / `reason` | number of candidates, 1 if selected, and the reason when not |

:::

**Excerpt** (first 3 rows where selected = 1).

::: {.excerpt}

| `base_system` | `level` | `new_ctl_position` | `d_lig_cat_ref` | `d_lig_ctl_new` | `selected` | `reason` |
|----------|----------|----------|----------|----------|----------|----------|
| `DN_campaign1__E4` | `ala` | `30` | `2.16` | `2.6964` | `1` | `selected` |
| `M0024_1nzy_a2` | `ala` | `82` | `3.433` | `4.512` | `1` | `selected` |
| `M0050_1dbt_a1` | `isosteric` | `193` | `3.703` | `5.0744` | `1` | `selected` |

:::


### Table S39. Re-predicted ladder: specificity ratio in strata of the distance to the ligand {#S39}

::: {.tmeta}

**File.** `supplementary/S39_ladder_distance_strata.csv` · 203 rows × 27 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric in one distance stratum, for one source (203 rows).

:::

The specificity ratio of each metric in the near, mid and far third of the pairs by the distance of the substituted residue to the ligand (edges 2.73 and 3.66 A), and on all pairs, with the median distances of the two arms.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `metric_name` / `role` / `applicability_status` / `headline` | the metric, interface or global, applicability status and whether it is a headline row |
| `stratum` / `edge_lo` / `edge_hi` / `k_pairs` / `k_systems` | the stratum and its size |
| SR_mean (+ lo/hi 95 and 90) / SR_median (+ lo/hi 95) | specificity ratio of the mean and of the median change with intervals |
| `mean_abs_delta_cat` / `mean_abs_delta_ctl` | mean absolute change in the two arms |
| `median_d_lig_cat` / `median_d_lig_ctl` / `median_abs_diff_d_lig` | median distances to the ligand |

:::

**Excerpt** (first 3 rows where source = natural, metric_name = chai_iptm_mean).

::: {.excerpt}

| `metric_name` | `stratum` | `k_pairs` | `k_systems` | `SR_mean` | `SR_mean_lo95` | `SR_mean_hi95` |
|----------|----------|----------|----------|----------|----------|----------|
| `chai_iptm_mean` | `all_pairs_original_gate` | `286` | `59` | `2.0359` | `1.4653` | `2.8031` |
| `chai_iptm_mean` | `all_pairs` | `281` | `58` | `2.0359` | `1.4532` | `2.833` |
| `chai_iptm_mean` | `near_third` | `89` | `27` | `2.4894` | `1.2129` | `4.7288` |

:::


### Table S40. Re-predicted ladder: caliper-matched subsets and the rule labels {#S40}

::: {.tmeta}

**File.** `supplementary/S40_ladder_matched_subsets.csv` · 348 rows × 25 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1 (68 to 69 pairs in 21 to 22 systems). **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric in one matched subset for one source (348 rows).

:::

The specificity ratio in caliper-matched subsets: original_controls (original controls within the caliper), original_plus_new_controls (with the new controls added, the subset of Table 10) and the sensitivity sets distance_in_prediction, distance_to_organic_atoms, caliper_1A and caliper_3A that use other distance definitions and calipers, with the label from the pre-specified rule (lower 90% bound above 1.2 with at least 30 pairs in 15 systems).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `metric_name` / `role` / `applicability_status` | the metric and its status |
| `set_id` / `control` | the matched subset and original or original+new controls |
| `k_pairs` / `k_systems` / `N_pairs` / `N_systems` | subset size and total |
| SR_mean (+ lo/hi) / SR_median (+ lo/hi) | specificity ratio with intervals |
| `verdict` / `rule_applies` | the label (for example not_testable (coverage), global_comparator_no_verdict) and whether the pre-specified rule applies |

:::

**Excerpt** (first 3 rows where source = natural, metric_name = chai_iptm_mean).

::: {.excerpt}

| `metric_name` | `set_id` | `k_pairs` | `k_systems` | `SR_mean` | `verdict` |
|----------|----------|----------|----------|----------|----------|
| `chai_iptm_mean` | `original_controls` | `17` | `16` | `0.3831` | `not_testable (coverage)` |
| `chai_iptm_mean` | `distance_in_prediction` | `23` | `22` | `0.4155` | `sensitivity:not_testable (coverag…` |
| `chai_iptm_mean` | `distance_to_organic_atoms` | `16` | `15` | `0.369` | `sensitivity:not_testable (coverag…` |

:::


### Table S41. Re-predicted ladder: regression-adjusted ratios {#S41}

::: {.tmeta}

**File.** `supplementary/S41_ladder_regression_adjusted.csv` · 116 rows × 28 columns · public

**Supports.** Methods 2.5.1 (Eq. 24); Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric with the original or the extended set of controls, for one source (116 rows).

:::

The ratio of catalytic to control change adjusted for the distance to the ligand and the burial, log(|delta| + eps) ~ arm + d_lig + relSASA, beside the unadjusted ratio on the same pairs, and the regression coefficients.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `metric_name` / `role` / `applicability_status` | the metric |
| `model` / `control` | the regression and original_controls or plus_new_controls |
| `k_pairs` / `k_systems` / `n_rows` / `eps` | size and the small constant that keeps zero changes finite |
| adj_GMR_cat_over_ctl (+ lo/hi95) | adjusted geometric-mean ratio |
| unadj_GMR_cat_over_ctl (+ lo/hi95) | unadjusted ratio on the same pairs |
| `beta_d_lig_per_A` / beta_relSASA (+ lo/hi95) | coefficients per A of distance and per unit of relative accessible area |

:::

**Excerpt** (first 3 rows where source = natural, metric_name = chai_iptm_mean).

::: {.excerpt}

| `metric_name` | `control` | `k_pairs` | `adj_GMR_cat_over_ctl` | `unadj_GMR_cat_over_ctl` |
|----------|----------|----------|----------|----------|
| `chai_iptm_mean` | `original_controls` | `261` | `1.1785` | `2.0198` |
| `chai_iptm_mean` | `plus_new_controls` | `261` | `1.0882` | `1.7922` |

:::


### Table S42. Panel equivalence statistic: earlier whole panel against the main-set metrics {#S42}

::: {.tmeta}

**File.** `supplementary/S42_equivalence_earlier_vs_main_panel.csv` · 6 rows × 10 columns · public

**Supports.** Results 3.4.1; Methods 2.5.1 (equivalence to 1). **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one analysis and set of metrics (6 rows).

:::

The geometric-mean specificity ratio of the panel with a 90% interval (nested bootstrap that recomputes every metric inside each draw), for the earlier whole panel (100 to 103 metrics, including composition metrics that have a ratio of 1 by arithmetic) and for the 27 main-set metrics with a defined ratio (isosteric step: 1.075 [0.958, 1.178]).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis_set` / `metric_set` / `n_metrics` | the analysis, the set of metrics and its size |
| `geomean_sr` / `ci90_lo` / `ci90_hi` / `median_sr` | geometric-mean ratio, 90% interval and median |
| `n_clusters` / `status` / `note` | resampling clusters, status and remarks |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `analysis_set` | `metric_set` | `n_metrics` | `geomean_sr` | `ci90_lo` | `ci90_hi` |
|----------|----------|----------|----------|----------|----------|
| `pilot set` | `earlier whole panel (all metrics …` | `103` | `0.9642` | `0.7479` | `1.2195` |
| `main set` | `earlier whole panel (all metrics …` | `102` | `0.9575` | `0.8969` | `1.0839` |
| `main set, packing-matched controls` | `earlier whole panel (all metrics …` | `102` | `0.9947` | `0.9374` | `1.1342` |

:::


### Table S43. Re-predicted ladder: specificity ratio per step for all metrics {#S43}

::: {.tmeta}

**File.** `supplementary/S43_ladder_re_predicted_per_level.csv` · 231 rows × 16 columns · public

**Supports.** Methods 2.5.1; Results 3.4.1. **Cited in.** Methods [2.5.1](https://pdflink.invalid/paper.pdf#page=9); Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one metric at one step for one source (231 rows).

:::

The re-predicted catalytic-lesion ladder per step (ALL steps pooled, isosteric, non-isosteric, Ala, Gly) for all 44 metrics, natural and de novo: pairs and systems, specificity ratio (median and mean) with intervals, and the verdict of the earlier rule.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `source` / `metric_name` / `canonical_key` / `input_class` / `ame_flavour` | the metric |
| `level` / `n_pairs` / `n_systems` | step and size |
| `sr_median` / `sr_lo` / `sr_hi` | ratio of medians with interval |
| `sr_mean` / `sr_mean_lo` / `sr_mean_hi` | ratio of means with interval |
| `verdict_earlier_rule` / `applicability_status` | verdict of the earlier rule and applicability status |

:::

**Excerpt** (first 3 rows where source = natural, level = isosteric, canonical_key = chai_iptm).

::: {.excerpt}

| `metric_name` | `level` | `n_pairs` | `n_systems` | `sr_mean` | `sr_mean_lo` | `sr_mean_hi` |
|----------|----------|----------|----------|----------|----------|----------|
| `chai_iptm_max` | `isosteric` | `118` | `59` | `1.622` | `1.058` | `2.526` |
| `chai_iptm_mean` | `isosteric` | `118` | `59` | `1.963` | `1.44` | `2.707` |
| `chai_iptm_std` | `isosteric` | `118` | `59` | `1.046` | `0.605` | `1.878` |

:::


### Table S44. Second-shell lesion: every metric scored (Table 11 plus supplementary comparators and per-dose flags) {#S44}

::: {.tmeta}

**File.** `supplementary/S44_second_shell_lesion_all_metrics_ranked.csv` · 37 rows × 59 columns · public

**Supports.** Results 3.4.2; the complete version of Table 11. **Cited in.** Methods [2.5.2](https://pdflink.invalid/paper.pdf#page=12); Results [3.4.2](https://pdflink.invalid/paper.pdf#page=21).

**A row is** one metric scored on second-shell removal (37 in all).

:::

Table 11 with the 8 supplementary comparators and the flags at each dose (1, 2 and 4 residues removed): R with interval, the number of informative proteins, and whether the metric responds, whether the control response is above its noise and whether it is specific. No step counts for any metric, so no rank on this test is interpretable and no reference level is computed.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `detection_group` / `rank_in_group` / `rank` / `rank_in_table_11` | group by first dose detected, rank in the group, overall rank and rank among the 29 items of Table 11 |
| `metric_name` / `canonical_key` / `source` / `input_class` / `role` / `in_ranked_set` | the metric and its role |
| `n_steps` / `n_steps_interpretable` | doses with a value and counted (0 for every metric) |
| r_second_shell_<d> / _lo / _hi / n_second_shell_<d> | R, interval and informative proteins at dose 1, 2 and 4 |
| `responds_` / `control_above_noise_` / specific_second_shell_<d> | per-dose flags |
| `r_mean_all_steps` / `first_step_detected` / `first_step_specific` | mean R over all doses and the onsets |

:::

The shared block of 12 provenance columns (see Conventions) is also present and is not repeated above.

**Excerpt** (first 3 rows).

::: {.excerpt}

| `detection_group` | `rank_in_group` | `metric_name` | `r_mean_all_steps` | `n_steps_interpretable` |
|----------|----------|----------|----------|----------|
| `second_shell_4` | `1` | `propka_catalytic_shift_mean` | `0.7005` | `0` |
| `second_shell_4` | `2` | `propka_catalytic_pka_mean` | `0.6915` | `0` |
| `never` | `1` | `catalytic_frac_buried` | `0.781` | `0` |

:::

**Notes.**

- Because both arms are scored over the catalytic residues, a high raw R on this test measures location.


### Table S45. Drift of the current Chai-1 engine against the earlier predictions {#S45}

::: {.tmeta}

**File.** `supplementary/S45_engine_drift_check.csv` · 176 rows × 5 columns · public

**Supports.** Results 3.2. **Cited in.** Results [3.2](https://pdflink.invalid/paper.pdf#page=15).

**A row is** one metric on one re-run prediction (176 rows).

:::

A drift check: four predictions (two cognate predictions of the substrate swap and two predictions of the catalytic-lesion ladder) were re-run with the current Chai-1 engine, and every metric is compared with its stored value. Most differences are small (median absolute difference 0.0007) but the largest is 0.91, which is why Chai-1 results are reported with seed noise and are not claimed to be bitwise reproducible.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `prediction` | the prediction that was re-run (system, condition and seed) |
| `metric_name` | the metric |
| `stored` / `rerun` / `abs_diff` | stored value, value of the re-run and their absolute difference |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `prediction` | `metric_name` | `stored` | `rerun` | `abs_diff` |
|----------|----------|----------|----------|----------|
| `M0112_3dfr_a1__cognate__s101` | `ame_crystal_clash_max` | `2.722` | `2.7284` | `0.0064` |
| `M0112_3dfr_a1__cognate__s101` | `ame_crystal_pass` | `1.0` | `1.0` | `0.0` |
| `M0112_3dfr_a1__cognate__s101` | `ame_crystal_rmsd_max` | `0.8037` | `0.8055` | `0.0018` |

:::


### Table S46. Effective dimensionality of the panel {#S46}

::: {.tmeta}

**File.** `supplementary/S46_effective_dimensionality.csv` · 4 rows × 10 columns · public

**Supports.** Results 3.4.1. **Cited in.** Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one set of metrics and one panel (4 rows).

:::

The participation ratio and related measures of the effective number of independent metrics, for the earlier whole panel and for the 29 structure-space main-set metrics, for native values (7.85 of 29) and for isosteric responses (10.5).

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric_set` / `panel` / `n_metrics` / `n_systems_complete` | the set, the panel and sizes |
| `participation_ratio` / `effective_rank_fraction` | effective number of independent metrics and its share |
| `var_explained_pc1` / `n_pcs_for_90pct` / `median_abs_offdiag_r` | variance in the first component, components for 90% and median absolute correlation between metrics |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `metric_set` | `panel` | `n_metrics` | `participation_ratio` | `var_explained_pc1` |
|----------|----------|----------|----------|----------|
| `earlier whole panel` | `native values across systems` | `97` | `12.12` | `0.195` |
| `earlier whole panel` | `isosteric responses (catalytic ar…` | `76` | `14.2` | `0.155` |
| `main-set metrics (one member per …` | `native values across systems` | `29` | `7.85` | `0.207` |

:::


### Table S47. De novo designs: burial equivalence of the created-site control {#S47}

::: {.tmeta}

**File.** `supplementary/S47_denovo_created_control.csv` · 5 rows × 11 columns · public

**Supports.** Results 3.4.1. **Cited in.** Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one burial metric (5 rows).

:::

In the 30 de novo designs the control is a position mutated to the catalytic residue type. For the five burial metrics the table gives the catalytic-arm and control-arm medians, the paired difference with 90% interval and whether they differ.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `metric` / `n_systems` / `n_clusters` | the burial metric, designs and backbone clusters |
| `catalytic_arm_median` / `control_arm_median` | medians in the two arms |
| `paired_diff_median` / `paired_diff_ci90_lo` / `paired_diff_ci90_hi` / `ratio_median` | paired difference with interval and ratio |
| `differs` / `note` | 1 if the arms differ |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `metric` | `n_systems` | `catalytic_arm_median` | `control_arm_median` | `paired_diff_median` | `differs` |
|----------|----------|----------|----------|----------|----------|
| `catalytic_rel_sasa_mean` | `30` | `0.1433` | `0.1315` | `0.0278` | `0` |
| `catalytic_rel_sasa_max` | `30` | `0.2157` | `0.2042` | `0.0256` | `0` |
| `catalytic_sasa_mean` | `30` | `32.1092` | `29.456` | `6.2169` | `0` |

:::


### Table S48. Experiments that could not be made or were retired {#S48}

::: {.tmeta}

**File.** `supplementary/S48_not_measurable.csv` · 9 rows × 4 columns · public

**Supports.** Results 3.4.1. **Cited in.** Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one experiment (9 rows).

:::

The deformation experiment (apparent specific cells track the clash burden present before repacking), oxyanion-hole removal (the step that was run located no bound ligand in any of the 143 structures and removed a proxy residue, so it did not test the named change), metal removal (no cell could be scored on any metric), the de novo second shell and deformation experiments, PLACER on the isosteric step, the unrelated-protein sanity floor and the two trapping-mutant tiers.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `reader_name` / `claim_type` | the experiment and the kind of claim it would have supported |
| `role` | retired or not_measurable |
| `mechanism_or_caveat` | why it could not be made |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `reader_name` | `role` | `mechanism_or_caveat` |
|----------|----------|----------|
| `sanity floor: unrelated protein` | `retired` | `signed paired-median statistic ca…` |
| `oxyanion-hole step` | `retired` | `well-defined perturbation, but no…` |
| `metal removal` | `not_measurable` | `no scoreable cell on any metric` |

:::


### Table S49. PLACER ensemble metrics on the isosteric step (not interpretable) {#S49}

::: {.tmeta}

**File.** `supplementary/S49_placer_isosteric.csv` · 50 rows × 12 columns · public

**Supports.** Results 3.4.1. **Cited in.** Results [3.4.1](https://pdflink.invalid/paper.pdf#page=19).

**A row is** one PLACER metric in one analysis (50 rows).

:::

The specificity ratio, verdict and applicability of 25 PLACER ensemble metrics on the isosteric step, in two analyses. They are not interpretable: the control arm is covered 1.6 to 3.2 times less than the catalytic arm in every crop configuration, so the count of specific metrics moves with the crop anchor alone.

**Key columns.**

::: {.defs}

| Column | Meaning |
|--------------------------------|------------------------------------------------------------------------------|
| `analysis_set` / `metric_name` / `level` / `n_systems` | the analysis, the metric, the step and enzymes |
| `sr_median` / `sr_ci_lo` / `sr_ci_hi` | specificity ratio with 95% interval |
| `responds` / `specific` / `verdict` / `applicability_status` | flags, verdict (blind, non_specific, specific, no_dynamic_range) and status (GLOBAL or X-CONFOUND) |

:::

**Excerpt** (first 3 rows).

::: {.excerpt}

| `analysis_set` | `metric_name` | `n_systems` | `sr_median` | `verdict` | `applicability_status` |
|----------|----------|----------|----------|----------|----------|
| `main set, packing-matched controls` | `placer_catalytic_rmsf_max` | `132` | `1.0106` | `blind` | `X-CONFOUND` |
| `main set, packing-matched controls` | `placer_catalytic_rmsf_mean` | `132` | `0.9058` | `blind` | `X-CONFOUND` |
| `main set, packing-matched controls` | `placer_centroid_dev_mean` | `132` | `0.9237` | `blind` | `X-CONFOUND` |

:::


# Appendix A. Main-text tables

The seven data tables of the Results (Tables 5 to 11), with the supplementary tables that hold the complete version or more detail. Tables 1 to 4 of the Methods are descriptive and are not released as files.

| Table | File | Rows × columns | More detail in |
|----------|------------------------------------------------------------|----------------|------------------------------|
| **T5** | `main/T5_dead_vs_active.csv` | 30 × 26 | [S11](#S11), [S7](#S7), [S8](#S8) |
| **T6** | `main/T6_plated_designs_auroc.csv` | 30 × 28 | [S13](#S13) |
| **T7** | `main/T7_substrate_swap.csv` | 30 × 32 | [S14](#S14), [S15](#S15) |
| **T8** | `main/T8_bglb_variants.csv` | 30 × 27 | [S16](#S16), [S17](#S17), [S18](#S18), [S19](#S19) |
| **T9** | `main/T9_plated_designs.csv` | 30 × 26 | [S21](#S21), [S20](#S20), [S23](#S23), [S22](#S22), [S24](#S24) |
| **T10** | `main/T10_specificity_catalytic_lesion.csv` | 35 × 36 | [S28](#S28), [S29](#S29), [S30](#S30) |
| **T11** | `main/T11_specificity_second_shell_lesion.csv` | 29 × 30 | [S44](#S44), [S29](#S29) |

# Appendix B. Notes on the data

- Two sets of numbers for natural enzymes in the substrate swap: [S14](#S14) uses all 59 natural enzymes, Table 7 uses the evaluation set of 55.
- Two forms of the rank statistic R: [S36](#S36) is R on the 143 main enzymes with 90% intervals; Table 10 and [S28](#S28) are the pooled analysis on 195 enzymes with 95% intervals and the counted-step rule. Values for the same metric differ.
- Among the 29 prediction-based metrics of the ladder with ligand-distance-matched controls, the cells of [S3](#S3) keep the label NOT-RUN although the analysis was carried out (results in [S40](#S40) and [S41](#S41)).
