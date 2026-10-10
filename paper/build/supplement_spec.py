"""Descriptions of the supplementary tables: the single source for
tables/public/INDEX.csv, the Supplementary PDF and its validation.

Keys are the ids under which the tables were generated (table_ids.csv maps them
to the S numbers of the paper). Text may refer to other tables as {S17c}; build
scripts replace such placeholders with the S number. Everything in the text
fields is public: no internal codes, file paths or working names.

Fields
  topic     group label in the table of contents
  title     reader-facing title
  supports  where the paper uses the table
  row       what one row is
  contents  what the table holds
  columns   key columns: (name or "a / b / c" for a group, meaning)
  excerpt   columns shown in the 3-row excerpt (optional filter in `where`)
  notes     caveats and relations to other tables
"""

AUDIT = "Metric audit"
ACT = "Activity discrimination (3.1)"
SUB = "Substrate discrimination (3.2)"
RANK = "Activity ranking (3.3)"
DET = "Detection ability (3.4)"

TABLES = {
# ----------------------------------------------------------------- Substrate swap
"S14": dict(
    topic=SUB,
    title="Substrate swap on all systems: all 33 prediction-based quantities, natural enzymes and de novo designs",
    supports="Results 3.2; the all-system analysis behind Table 7",
    row="one prediction-based quantity under one wrong-ligand condition, for one source (natural enzymes or de novo designs)",
    contents=("The substrate swap before the 55-enzyme evaluation set was fixed: all 59 natural enzymes (cognate value averaged "
              "over five seeds) and all 30 de novo designs, for every one of the 33 prediction-based quantities that were scored, "
              "including the Chai-1 combined score (a rescaled ipTM) that Table 7 leaves out. For each quantity and each wrong "
              "ligand (same enzyme class, different class, decoy; apo for the quantities that are defined without a ligand) it gives "
              "the mean under the cognate and under the other condition, the paired change, the change in units of seed noise, and "
              "the direction-free AUROC with its interval."),
    columns=[("source", "natural or denovo"),
             ("metric_name / canonical_key / input_class", "the quantity, the distinct metric it belongs to and its class"),
             ("ame_flavour", "crystal = active-site accuracy against the deposited structure; self_design = against the design's own model (never pooled)"),
             ("in_main_set", "1 for the four main-set metrics (each appears several times: mean, maximum and spread over the five predicted models are separate rows)"),
             ("condition", "same_ec, diff_ec, decoy or apo"),
             ("n_systems", "systems with a value (59 natural, 30 de novo)"),
             ("mean_cognate / mean_condition / mean_delta", "mean value under the cognate ligand, under the condition, and the paired difference"),
             ("median_delta_over_sigma / frac_beyond_1sigma", "median change in units of the seed-to-seed standard deviation, and the share of systems that move by more than one"),
             ("auroc / auroc_lo / auroc_hi", "direction-free AUROC of cognate against the condition, 95% interval over systems")],
    excerpt=["source", "metric_name", "condition", "n_systems", "mean_cognate", "mean_condition", "auroc"],
    where={"source": "natural", "condition": "diff_ec", "in_main_set": "1"},
    notes=["n is 59 natural enzymes here and 55 in Table 7, whose evaluation set drops four enzymes whose ligand could not be built.",
           "Per-metric results of this table are descriptive; the ranking and the best-of-30 threshold are in Table 7."]),

# ----------------------------------------------------------------- Metric audit
"A5": dict(
    topic=AUDIT,
    title="Main metric set: the role of every distinct metric, and why",
    supports="Methods, Table 1 and 'Which metrics are reported'; the main set of 33 metrics used in Tables 5 to 11",
    row="one distinct metric (a canonical key; aliases and per-model summaries of one score are merged), 191 in all",
    contents=("The audit that fixes which metrics the paper reports. For each distinct metric it gives the applicability status "
              "in the detection test of the catalytic lesion, in the dead-against-active tests and in the activity-ranking tests, "
              "and the resulting role: main (33, valid and tested in the deliberate-change tests and in the tests on real proteins), "
              "reference (6, comparators chosen before any result was seen), excluded_bookkeeping (63 counters and constants) or one of "
              "the supplement roles (supp_global 44, supp_placer 25, supp_excluded 10, supp_aggregate 4, supp_partial 3, "
              "supp_real_protein_tests_only 2, and supp_derived 1, the Chai-1 combined score, a rescaled ipTM). The reason for each "
              "role is in the last column. The status is decided from what a metric reads, whether it is defined and the design of "
              "the experiment, never from a result."),
    columns=[("canonical_key / members / rep_metric", "the distinct metric, the names merged into it and the representative one"),
             ("mode / input_class / subfamily / aggregator", "structure-space or prediction-based, what the metric reads, its family and how it is summarised"),
             ("status_detection_test / fraction_detection_test", "applicability status in the detection test of the catalytic lesion and the share of units on which the metric is defined"),
             ("status_dead_vs_active_tests / fraction_dead_vs_active_tests / partial_dead_vs_active_tests", "the same for the dead-against-active tests"),
             ("status_ranking_tests / ranking_tests_ok", "status in each activity-ranking test (BglB variants, plated designs) and the tests in which the metric is OK"),
             ("role", "main, reference, excluded_bookkeeping, supp_global, supp_placer, supp_excluded, supp_aggregate, supp_partial, supp_real_protein_tests_only or supp_derived"),
             ("reason", "why the metric has that role")],
    excerpt=["canonical_key", "input_class", "status_detection_test", "status_dead_vs_active_tests", "role"],
    where={"role": "main"},
    notes=["The status vocabulary is in the Conventions.",
           "NOT-RUN in status_ranking_tests marks the PLACER metrics, which were not computed in the BglB and plated-design analyses."]),

"S01": dict(
    topic=AUDIT,
    title="Metric contracts: what each named quantity reads, over which residues, and where it is valid",
    supports="Methods, Table 1 and 'Which metrics are reported'",
    row="one named quantity (216 in all; an alias is a separate row linked by alias_of and canonical_key)",
    contents=("The input contract of every quantity in the panel: what it reads (sequence only, whole-protein structure, site-scoped "
              "structure, predictor output, active-site accuracy, PLACER output, deposit metadata or bookkeeping), over which residues it "
              "is scored in the catalytic arm and in the two kinds of control arm, which inputs it needs, which kinds of metric it is "
              "valid for and which changes it cannot respond to."),
    columns=[("metric_name / canonical_key / alias_of / alias_kind", "the quantity, the distinct metric after aliases are merged, and the kind of alias"),
             ("aggregator / metric_family / subfamily", "how it is summarised, and its family and subfamily"),
             ("input_class", "sequence-only, whole-protein structure, site-scoped structure, prediction, active-site accuracy (AME), PLACER, deposit metadata or bookkeeping"),
             ("scope_catalytic_arm / scope_control_arm_catalytic_lesion / scope_control_arm_second_shell", "the residues the metric is scored over in the catalytic arm, in the control arm of the catalytic lesion and in the control arm of the second-shell lesion"),
             ("needs_cat_residue / needs_ligand / needs_reference / needs_predictor", "the inputs the metric needs"),
             ("valid_modes", "structure-space, prediction-based, PLACER, any or deposit metadata"),
             ("invariant_under", "changes the metric cannot register (for example sequence composition under a rotamer change)"),
             ("ame_flavour / note", "for active-site accuracy, the reference it is measured against; remarks on the metric, including where the metric as computed differs from its earlier description")],
    excerpt=["metric_name", "input_class", "scope_catalytic_arm", "valid_modes"],
    where={"input_class": "struct_site"}),

"A3": dict(
    topic=AUDIT,
    title="Applicability of every metric in every test (long format)",
    supports="Methods, 'Which metrics are reported'",
    row="one named quantity in one test (216 quantities x 30 tests = 6,480 rows)",
    contents=("Whether each quantity can be tested in each of the 30 tests, and if not why. Status counts: OK 468, GLOBAL 339, REF 15, "
              "OK-KNOCKON 6, OK-PROVISIONAL 10 (testable); X-ARM 2,296, X-BOOKKEEP 1,920, X-NOINPUT 576, X-WITHDRAWN 381, X-UNDEF-COV 203, "
              "X-NOCTRL 118, X-CONFOUND 10, NOT-RUN 79, DUP 59 (not testable, with the reason). The reason and the coverage "
              "(defined_k of defined_N units) are given. Decided from inputs, definedness and design only, never from results."),
    columns=[("metric_name / canonical_key / input_class", "the quantity, the distinct metric and its class"),
             ("test / test_class", "the test (its name and class as in {S03}) and the class alone, for example 'dead against active, prediction-based'"),
             ("status / reason", "the applicability status and the reason in words"),
             ("defined_k / defined_N / fraction / partial", "number of units on which the metric is defined, of how many, their ratio, and whether coverage is partial")],
    excerpt=["metric_name", "test", "status", "reason"],
    where={"status": "OK"},
    notes=["Released as a CSV only: with 6,480 rows it is not printed. {S02} is its summary by class of metric.",
           "Of the 79 cells with status NOT-RUN, 50 are PLACER metrics that were not computed in the BglB and plated-design analyses. The other 29 are prediction-based metrics in the ladder with ligand-distance-matched controls: this analysis was carried out (results in {S16c} and {S16d}) but its cells keep the label NOT-RUN."]),

"S02": dict(
    topic=AUDIT,
    title="Applicability by class of metric and test",
    supports="Methods, 'Which metrics are reported' (summary of {A3})",
    row="one class of metric in one test with one status (340 rows)",
    contents=("A summary of {A3}: for each input class and test, how many metrics receive each status. The quickest way to see why a "
              "whole class of metrics is absent from a result."),
    columns=[("input_class", "class of metric (ame, bookkeeping, pred_global, pred_interface, seq_only, struct_site, struct_whole, ...)"),
             ("test / test_class", "the test and its class"), ("status", "applicability status"), ("n_metrics", "number of metrics of that class with that status in that test")],
    excerpt=["input_class", "test_class", "status", "n_metrics"], where={"status": "OK"}),

"A4": dict(
    topic=AUDIT,
    title="Counts restated on the eligible metrics (denominators before and after the audit)",
    supports="Methods, 'Which metrics are reported'",
    row="one headline count of the earlier whole-panel analysis (58 in all)",
    contents=("The counts of responding and specific metrics of the earlier analysis (original_k of original_N, over every metric with a "
              "testable cell) restated on the eligible metrics only (eligible_k of eligible_N, also as distinct metrics and for the "
              "whole-protein comparators), with the breakdown of what was excluded and why. It shows how much of the earlier denominators "
              "were metrics that could not respond."),
    columns=[("analysis / level / statistic", "the earlier analysis (data set and lesion), the lesion step and the statistic ('responds' or 'specific')"),
             ("original_k / original_N", "count and denominator of the earlier analysis"),
             ("eligible_k / eligible_N / eligible_distinct_k / eligible_distinct_N", "the same on eligible metrics, and as distinct metrics"),
             ("global_k / global_N", "the count among whole-protein comparators"),
             ("excluded_breakdown / recompute_kind / note", "which statuses were excluded and how many, how the recount was done, and a note")],
    excerpt=["analysis", "level", "statistic", "original_k", "original_N", "eligible_k", "eligible_N"]),

"S03": dict(
    topic=AUDIT,
    title="Test inventory: the 30 tests, with comparator, control type, role and caveats",
    supports="Methods 2.2 to 2.5; the key to the test names in {A3} and {S02}",
    row="one test: an experiment on a data set with one kind of metric (30 in all)",
    contents=("Every test with its name and class, the kind of metric (structure-space or prediction-based), the unit and the number of "
              "units, the resampling unit, the changes applied, the comparator and control type, the role (primary, sensitivity, sanity, "
              "retired, not_measurable or dup) and the caveats. {A3} and {S02} use the test names of this table."),
    columns=[("test / reader_name / test_class / mode", "the test (name with its class), the name alone, the class, and structure-space or prediction-based"),
             ("unit / n_units / n_clusters / cluster_def", "what is counted, how many, and the resampling unit"),
             ("levels / comparator / control_type", "what is changed or contrasted, what the metric is compared with and how the control is built"),
             ("claim_type / role", "the kind of claim and the role: primary, sensitivity, sanity, retired, not_measurable or dup"),
             ("caveats", "limits of the test")],
    excerpt=["reader_name", "test_class", "mode", "claim_type", "role"]),

# ----------------------------------------------------------------- 3.1
"S17": dict(
    topic=ACT,
    title="Wider set of 49 zymogen-mature pairs: all 136 scored metrics, with the same-state null",
    supports="Results 3.1.1 (wider set); Methods 2.2.1",
    row="one scored metric (136 in all)",
    contents=("The analysis on the 49 pairs for which structure-space metrics were scored (before the evaluation set of 21 pairs that share "
              "a ligand was fixed): the direction-free AUROC of dead against active with interval, the directed AUROC, the number of pairs, "
              "and the AUROC of the same metric on 96 same-state null pairs, which shows how much separation arises without any dead/active "
              "difference."),
    columns=[("metric_name / canonical_key / input_class / in_main_set", "the metric, its class and whether it is a main-set metric"),
             ("n_pairs", "pairs with a value (49 at most)"),
             ("auroc / auroc_lo / auroc_hi / auroc_directed", "direction-free AUROC with 95% interval over pairs, and the directed value"),
             ("auroc_vs_same_state_null / n_zymogen_pairs / n_same_state_null_pairs", "AUROC of zymogens against the same-state null pairs and the numbers in each group"),
             ("applicability_status", "applicability status")],
    excerpt=["metric_name", "in_main_set", "n_pairs", "auroc", "auroc_lo", "auroc_hi"],
    notes=["Structure-space and PLACER metrics only; the 4 prediction-based metrics were scored on the 28 re-predicted pairs ({S18}).",
           "Results are descriptive of a wider set; the evaluation set is the 21 pairs of {S17c}."]),

"S18": dict(
    topic=ACT,
    title="Zymogen pairs re-predicted with Chai-1, restated with the definedness gate",
    supports="Results 3.1.1 (wider-set check for the prediction-based metrics)",
    row="one prediction-based metric (33 in all)",
    contents=("The 28 zymogen-mature pairs re-predicted with Chai-1: the AUROC of each metric with interval, the number of pairs reported "
              "against the number on which the metric is defined, and a note where the earlier value was not interpretable. "
              "Active-site accuracy is relabelled as measured against each form's own deposited structure."),
    columns=[("metric_name / metric_reported_as", "the metric and the name it carried in the earlier report"),
             ("input_class", "class of metric"),
             ("n_pairs_reported / n_pairs_defined_restated", "pairs in the earlier report and pairs on which the metric is defined"),
             ("auroc / auroc_lo / auroc_hi", "direction-free AUROC with 95% interval"),
             ("applicability_status / restatement_note", "applicability status and what was restated")],
    excerpt=["metric_name", "n_pairs_reported", "n_pairs_defined_restated", "auroc", "applicability_status"],
    where={"applicability_status": "OK"},
    notes=["28 pairs include the 7 apo pairs that are not in the 21-pair evaluation set."]),

"S17b": dict(
    topic=ACT,
    title="Definitions of the pair sets",
    supports="Methods 2.2.1; Results 3.1.1",
    row="one set of zymogen-mature pairs (6 in all)",
    contents=("The six sets used in 3.1 with their size and definition: 55 candidate rows, 49 scored pairs, 45 with PLACER, "
              "28 re-predicted pairs, the 21-pair evaluation set (pairs that share a ligand) and the 96 same-state null pairs, and which "
              "table uses each."),
    columns=[("pair_set / n", "the set and its size"), ("definition", "how the set is defined"),
             ("used_for", "the table that uses it")],
    excerpt=["pair_set", "n", "used_for"]),

"S19": dict(
    topic=ACT,
    title="Substrate-trapping mutants checked against the literature (tier retired)",
    supports="Results 3.1.1 (retired tier); Methods 2.2.1",
    row="one verdict category (6 rows)",
    contents=("The 30 trapping-mutant pairs verified against the primary literature: 15 confirmed reduced, 4 confirmed inactive, "
              "4 active and 7 not stated; 26 of the 30 (86.7%, 95% Wilson interval 70.3 to 94.7%) are not confirmed dead. Every deposited "
              "construct carries an engineered substitution. The tier is retired."),
    columns=[("verdict", "confirmed_reduced, confirmed_inactive, active, not_stated, and the summary rows"),
             ("n_pairs / denominator", "number of pairs and the total (30)"), ("note", "interval of the mislabelling rate")],
    excerpt=["verdict", "n_pairs", "denominator", "note"]),

"S17c": dict(
    topic=ACT,
    title="Zymogen-mature evaluation set: all 158 metrics ranked by AUROC (complete Table 5)",
    supports="Results 3.1.1; the complete version of Table 5",
    row="one metric scored on the 21 pairs (158 in all)",
    contents=("Every metric scored on the 21 pairs that share a ligand: structure-space, PLACER and prediction-based metrics, including "
              "whole-protein and sequence-only comparators, ranked by direction-free AUROC of dead against active. The best-of-158 "
              "threshold (95th percentile of the best AUROC among 158 unrelated metrics in label-swap simulations) is marked: seven "
              "metrics exceed it, all summaries of whole-prediction confidence (pLDDT and per-chain pTM), which are comparators and "
              "not main-set metrics."),
    columns=[("rank / rank_in_table_5", "rank among all 158 and rank among the 39 items of Table 5"),
             ("metric_name / canonical_key / source / input_class", "the metric, the distinct metric, structure-space / PLACER / prediction-based, and class"),
             ("role", "main, reference or a supplement role (43 rows carry main because aliases of the 33 main-set metrics are separate rows)"),
             ("n_pairs / auroc / auroc_ci_lo / auroc_ci_hi", "pairs (21) and AUROC with 95% interval over pairs"),
             ("higher_in / auroc_directed", "the form (dead or active) in which the metric is larger, and the directed AUROC"),
             ("above_best_of_158_threshold / applicability_status", "1 if above the threshold; applicability status")],
    excerpt=["rank", "metric_name", "role", "auroc", "auroc_ci_lo", "auroc_ci_hi"]),

"S24": dict(
    topic=ACT,
    title="Reference rows on the wider sets, BglB baselines and hits per plate of reference rows",
    supports="Results 3.1 and 3.3; Methods 2.2 and 2.4",
    row="one reference item for one measure (35 in all)",
    contents=("Reference rows (items that need no catalytic information) on sets other than the evaluation sets of Tables 5 and 6, with intervals: "
              "crystallographic resolution, sequence length, net charge and tyrosine fraction (AUROC on the 49 zymogen pairs) and pLDDT and pTM (AUROC on the 28 re-predicted pairs; the values on the 21-pair evaluation set are in {S17c}); the five declared BglB baselines "
              "(side-chain volume change, negative distance to the catalytic residues, burial, BLOSUM62 and the Rosetta score of the BglB data; "
              "signed AUROC of the binary contrast on the 432-variant set; their rank correlations and the BglB reference rows are in {S20c}); and expected hits per 96-well plate at each keep fraction for tyrosine fraction, net charge "
              "and sequence length on the plates (the AUROC and correlation of the reference rows on the designs are in {S17d} and {S22c})."),
    columns=[("reference_item / metric", "the reference row (and the end kept for plate rows)"),
             ("measure", "AUROC (direction-free), AUROC (signed, pre-directed) or expected hits per 96-well plate"),
             ("keep_fraction", "fraction of designs kept (plate rows only)"),
             ("estimate / ci_lo / ci_hi / n", "the value, its interval and the number of units")],
    excerpt=["reference_item", "measure", "estimate", "ci_lo", "ci_hi", "n"],
    where={"measure": "AUROC (signed, pre-directed)"},
    notes=["Contains aggregates of D2DCure data (licence unstated); no per-variant rows."]),

"S17d": dict(
    topic=ACT,
    title="Plated designs: all 128 metrics ranked by the AUROC of active against no active designs (complete Table 6)",
    supports="Results 3.1.2; the complete version of Table 6",
    row="one metric scored on the 192 designs (128 in all)",
    contents=("Every metric scored on the 192 plated designs, ranked by the direction-free AUROC of the 16 active designs against "
              "the 176 no active designs, with 95% interval over the 136 backbone clusters. The best-of-128 threshold (permuting "
              "labels among designs) is marked: ten metrics exceed it. They are two main-set metrics (the intra-residue repulsion, 0.80, and the "
              "repulsion of the catalytic residues, 0.78), two aliases or per-residue variants of the latter, four sequence-composition rows, one whole-protein term (omega) and the Rosetta reference energy."),
    columns=[("rank / rank_in_table_6 / in_table_6", "rank among 128, rank among the 36 items of Table 6 and membership of Table 6"),
             ("metric_name / canonical_key / source / input_class / role", "the metric, its source, class and role"),
             ("n_designs / n_active", "192 and 16"),
             ("auroc / auroc_ci_lo / auroc_ci_hi / auroc_directed / higher_in", "AUROC, interval, directed AUROC and the group in which the metric is larger"),
             ("above_best_of_all_metrics_threshold / applicability_status", "1 if above the best-of-128 threshold; applicability status")],
    excerpt=["rank", "metric_name", "role", "auroc", "auroc_ci_lo", "auroc_ci_hi"],
    notes=["Designs are not exchangeable (10 of the 16 active designs lie in two backbone clusters), so the threshold understates the chance range."]),

# ----------------------------------------------------------------- 3.2
"S14b": dict(
    topic=SUB,
    title="Substrate swap stratified by ligand size and charge",
    supports="Results 3.2; Methods 2.3 (size check, Eq. 10)",
    row="one quantity, source, wrong-ligand condition and stratum of the difference in ligand size or charge, for one analysis variant",
    contents=("The check of whether ligand size or charge explains the discrimination. For each headline quantity (ipTM, per-chain pTM "
              "minimum, the combined score, ligand clearance), comparator (pTM, pLDDT, AME RMSD) and the two baselines (ligand heavy-atom "
              "count and formal charge), the cells (an enzyme and one wrong ligand) are stratified by the difference in heavy-atom "
              "count (smaller, matched, larger), by the charge difference (same, different) and jointly. For each stratum it gives the paired "
              "win fraction, the AUROC of the absolute value, the Spearman correlation of the size difference with the change, intervals "
              "over systems and clusters, and whether the effect survives."),
    columns=[("source / variant", "natural or denovo; primary or the variant that excludes ipTM = 0 cells (excl_iptm0)"),
             ("metric_name / role", "the quantity and headline, comparator or baseline"),
             ("stratum_family / stratum", "all, size (smaller, matched, larger), charge (q_same, q_diff) or joint, and the stratum"),
             ("condition", "same_ec, diff_ec, decoy or the three pooled (pooled_3)"),
             ("k_cells / N_cells / k_systems / N_systems", "cells and systems in the stratum"),
             ("win_frac / win_lo95 / win_hi95", "paired win fraction (cognate higher than wrong ligand) with 95% interval"),
             ("auroc_abs / spearman_dn_vs_change / survives", "AUROC of absolute value, Spearman correlation of size difference with the change, and 1 / 0 / 'n<10, not estimated'")],
    excerpt=["metric_name", "stratum", "condition", "k_cells", "N_cells", "win_frac"],
    where={"variant": "primary", "source": "natural", "stratum_family": "size"},
    notes=["Released as a CSV only for the full 1,136 rows; the excerpt shows the structure."]),

"S16g": dict(
    topic=SUB,
    title="Drift of the current Chai-1 engine against the earlier predictions",
    supports="Results 3.2",
    row="one metric on one re-run prediction (176 rows)",
    contents=("A drift check: four predictions (two cognate predictions of the substrate swap and two predictions of the "
              "catalytic-lesion ladder) were re-run with the current Chai-1 engine, and every metric is compared with its stored value. "
              "Most differences are small (median absolute difference 0.0007) but the largest is 0.91, which is why Chai-1 results "
              "are reported with seed noise and are not claimed to be bitwise reproducible."),
    columns=[("prediction", "the prediction that was re-run (system, condition and seed)"), ("metric_name", "the metric"),
             ("stored / rerun / abs_diff", "stored value, value of the re-run and their absolute difference")],
    excerpt=["prediction", "metric_name", "stored", "rerun", "abs_diff"]),

# ----------------------------------------------------------------- 3.3
"S20c": dict(
    topic=RANK,
    title="BglB: every analysed quantity ranked by rank correlation with the measured impairment (complete Table 8)",
    supports="Results 3.3.1; the complete version of Table 8",
    row="one quantity analysed on the 432 BglB variants (114 in all)",
    contents=("Every quantity analysed on the 432-variant evaluation set: 84 structure-space metrics, 25 prediction-based metrics and the five "
              "declared baselines, ranked by the Spearman correlation of the size of its change with the measured impairment, with 95% "
              "interval over the 175 positions. It carries the best-of-114 threshold, whether the quantity beats the distance baseline, the "
              "correlation of the signed change, and beside them the AUROC of the binary contrast (impaired against wild-type-like "
              "variants) with its interval, threshold and beats-the-distance flag. No quantity beats the distance baseline; 34 exceed the "
              "best-of-114 threshold."),
    columns=[("rank / rank_in_table_8 / in_table_8", "rank among 114, rank among the 41 items of Table 8 and membership of Table 8"),
             ("metric_name / canonical_key / source / input_class / role", "the quantity, its source (structure-space, prediction-based or baseline), class and role"),
             ("n_variants", "variants with a value (431 or 432; 248 for the Rosetta score of the BglB data)"),
             ("rho / rho_ci_lo / rho_ci_hi", "Spearman correlation and 95% interval over positions"),
             ("above_best_of_all_quantities_threshold / beats_distance_baseline / diff_vs_distance_baseline_ci_lo", "threshold flag, beats-the-distance flag and the lower end of the difference in correlation"),
             ("rho_signed_delta", "correlation of the signed change"),
             ("auroc / auroc_ci_lo / auroc_ci_hi", "AUROC of the binary contrast with 95% interval; the columns that follow (threshold, beats-the-distance flag and difference against the distance baseline) are for the AUROC")],
    excerpt=["rank", "metric_name", "role", "rho", "rho_ci_lo", "rho_ci_hi"],
    notes=["Aggregates of D2DCure data (licence unstated); no per-variant rows."]),

"S20a": dict(
    topic=RANK,
    title="BglB: all 84 structure-space and comparator metrics",
    supports="Results 3.3.1; Methods 2.4.1",
    row="one metric analysed on the 432 BglB variants (84 in all)",
    contents=("Spearman correlation, signed, direction-free and magnitude AUROC with intervals, the paired difference against the "
              "distance baseline and whether the metric beats all baselines, for every structure-space metric and comparator (36 site-scoped, "
              "28 sequence-only, 15 whole-protein, 5 bookkeeping). None beats all baselines."),
    columns=[("metric / canonical_key / input_class / in_main_set", "the metric, its class and main-set membership"),
             ("rho / rho_lo / rho_hi", "Spearman correlation with 95% interval over positions"),
             ("auc_signed / auc_dirfree / auc_mag (+ _lo, _hi)", "AUROC of the binary contrast using the signed change, the direction-free form and the magnitude, with intervals"),
             ("diff_vs_neg_d_cat_lo / beats_all_baselines", "lower end of the difference against the distance baseline; whether the metric beats all five baselines")],
    excerpt=["metric", "in_main_set", "rho", "rho_lo", "rho_hi", "beats_all_baselines"],
    where={"in_main_set": "1"},
    notes=["Aggregates of D2DCure data (licence unstated); no per-variant rows."]),

"S20b": dict(
    topic=RANK,
    title="BglB: sensitivity analyses",
    supports="Results 3.3.1",
    row="the main analysis and one of ten sensitivity analyses (11 rows)",
    contents=("The main analysis and ten sensitivity analyses with their sizes, the number of metrics with an interval above 0.5, the number "
              "that beat the distance baseline and the AUROC of the distance baseline. The analyses are: the main analysis (432 variants); "
              "variants near to and distal from the catalytic residues (144 and 288); variants with a measured stability (292); "
              "each institution left out in turn (FIU, MiraCosta, UC Davis); other thresholds for the impaired label (1 and 3 standard "
              "deviations, with 173 and 139 impaired variants); responding metrics only (70 metrics analysed); and without the variants "
              "at catalytic positions (431 variants, one position removed). In every analysis no metric beats the distance baseline."),
    columns=[("analysis", "the analysis"), ("n_variants / n_positions / n_impaired / n_wtlike", "size of the analysis"),
             ("n_metrics_analysed / n_auc_mag_ci_above_half", "metrics analysed and metrics whose AUROC interval lies above 0.5"),
             ("n_beats_neg_d_cat / n_beats_all_baselines", "metrics that beat the distance baseline and all baselines"),
             ("auc_neg_d_cat_baseline", "AUROC of the distance baseline")],
    excerpt=["analysis", "n_variants", "n_positions", "n_impaired", "n_wtlike", "n_beats_neg_d_cat"],
    notes=["Aggregates of D2DCure data (licence unstated); no per-variant rows."]),

"S21": dict(
    topic=RANK,
    title="BglB: prediction-based metrics (Chai-1 with the assay substrate)",
    supports="Results 3.3.1; Methods 2.4.1",
    row="one prediction-based quantity or sequence-only reference row analysed on the 432 BglB variants (28 in all: 25 prediction-based, 3 sequence-only)",
    contents=("The same columns as {S20a} for the quantities computed from Chai-1 predictions of each variant with the assay substrate "
              "(pNPG, no metal), and for the three sequence-only reference rows; active-site accuracy is measured against the wild-type crystal, which carries a covalent glucosyl "
              "intermediate. Here rho is the correlation of the signed change, as in {S20a}. Twelve rows are main-set metrics; the largest signed correlation is 0.17 "
              "(AME RMSD, naive minimum) and the largest magnitude is 0.25 (ipTM, -0.25); the size-of-change correlation of Table 8 is in {S20c} (ipTM 0.33)."),
    columns=[("metric / canonical_key / input_class / in_main_set", "the metric, its class and main-set membership"),
             ("rho / rho_lo / rho_hi", "Spearman correlation with 95% interval over positions"),
             ("auc_signed / auc_dirfree / auc_mag (+ _lo, _hi)", "AUROC of the binary contrast"),
             ("beats_all_baselines", "whether the metric beats all five baselines")],
    excerpt=["metric", "in_main_set", "rho", "rho_lo", "rho_hi"],
    where={"in_main_set": "1"},
    notes=["Aggregates of D2DCure data (licence unstated); no per-variant rows."]),

"S22d": dict(
    topic=RANK,
    title="Plated designs: hits per 96-well plate for every metric (filter-style analysis)",
    supports="Results 3.3.2; Methods 2.4.2 (Eqs. 16 and 17)",
    row="one metric scored on the 192 designs (128 in all)",
    contents=("The filter-style analysis, for every metric: the expected hits per 96-well plate and the "
              "actives among the 48 designs kept when the quarter of designs that the metric ranks highest, or lowest, fills the plate "
              "(8.0 hits when unfiltered), each with a 90% interval over designs, ranked by the better end. 30 metrics exceed the random-filter "
              "band (14.0 hits)."),
    columns=[("rank / rank_among_ranked_items / ranked_item", "rank among 128, rank among the 36 items of Table 9 and whether the metric is one of them"),
             ("metric_name / canonical_key / source / input_class / role", "the metric and its class"),
             ("n_designs / n_active / n_kept_highest / n_kept_lowest", "192, 16 and the number kept (fewer than 48 when designs tie at the cut)"),
             ("hits_highest_quarter / hits_highest_ci_lo90 / hits_highest_ci_hi90 / actives_in_highest_quarter", "hits per plate for the highest quarter, 90% interval and actives kept"),
             ("hits_lowest_quarter / hits_lowest_ci_lo90 / hits_lowest_ci_hi90 / actives_in_lowest_quarter", "the same for the lowest quarter"),
             ("better_end / best_hits_per_plate / above_random_band", "the better end, its hits per plate and whether it exceeds the random band"),
             ("note", "for example a tie at the cut")],
    excerpt=["rank", "metric_name", "role", "better_end", "best_hits_per_plate", "above_random_band"],
    notes=["Descriptive only: no hypothesis test."]),

"S22c": dict(
    topic=RANK,
    title="Plated designs: every metric ranked by correlation with kcat/KM among the 16 designs that have a value (complete Table 9)",
    supports="Results 3.3.2; the complete version of Table 9",
    row="one metric with a rank correlation on the 16 designs with a reported kcat/KM (106 in all)",
    contents=("Every metric that has a correlation, ranked by the size of the Spearman correlation with log10 kcat/KM, with a 90% interval "
              "over designs, whether the interval excludes 0 (33 do), the direction, and the correlation with the sequence length "
              "partialled out and whether it survives that control."),
    columns=[("rank / rank_in_table_9 / in_table_9", "rank among 106, rank among the 36 items of Table 9 and membership of Table 9"),
             ("metric_name / canonical_key / source / input_class / role", "the metric and its class"),
             ("n_designs / rho / rho_ci_lo90 / rho_ci_hi90", "16 designs, Spearman correlation and 90% interval over designs"),
             ("interval_excludes_zero / higher_value_means", "whether the interval excludes 0 and whether a larger value means higher or lower activity"),
             ("rho_given_length / survives_length_control", "correlation with the sequence length partialled out of both sides, and whether it survives")],
    excerpt=["rank", "metric_name", "rho", "rho_ci_lo90", "rho_ci_hi90", "higher_value_means"],
    notes=["Descriptive only; about 10% of unrelated metrics are expected to have an interval that excludes 0."]),

"S22b": dict(
    topic=RANK,
    title="Plated designs: ordering among the 16 active designs, structure-space metrics and comparators",
    supports="Results 3.3.2; Methods 2.4.2 (Eq. 15)",
    row="one metric of the structure-space panel or a comparator (81 in all)",
    contents=("The Spearman correlation with log kcat/KM among the 16 active designs with and without the sequence length partialled out, "
              "with 90% intervals and whether the interval excludes 0 (24 do)."),
    columns=[("metric_name / canonical_key / input_class / in_main_set", "the metric and its class"),
             ("spearman_rho / rho_lo90 / rho_hi90 / excludes_zero", "correlation, 90% interval and whether it excludes 0"),
             ("rho_given_length / survives_length_control", "correlation with length partialled out and whether it survives")],
    excerpt=["metric_name", "in_main_set", "spearman_rho", "rho_lo90", "rho_hi90", "rho_given_length"],
    where={"in_main_set": "1"}),

"S22a": dict(
    topic=RANK,
    title="Plated designs: enrichment at every keep fraction, structure-space metrics",
    supports="Results 3.3.2; Methods 2.4.2",
    row="one metric, one direction (keep the highest or the lowest values) and one keep fraction (816 rows)",
    contents=("Enrichment on the 192 plated designs for the 102 metrics of the structure-space panel and its comparators, in both directions "
              "and at keep fractions of 5, 10, 25 and 50%: the number kept, the actives kept and the expected hits per 96-well plate "
              "with a 90% interval against the unfiltered 8.0."),
    columns=[("metric / canonical_key / input_class / in_main_set", "the metric"),
             ("direction / keep_fraction / n_kept", "keep the highest or the lowest values; the fraction and the number of designs kept"),
             ("n_active_kept / n_active_total", "actives among those kept, and 16"),
             ("expected_hits_per_plate / hits_lo90 / hits_hi90", "expected hits per plate with 90% interval"),
             ("baseline_hits_per_plate / enrichment_vs_baseline", "8.0 and the ratio to it")],
    excerpt=["metric", "direction", "keep_fraction", "n_kept", "n_active_kept", "expected_hits_per_plate"],
    where={"in_main_set": "1", "keep_fraction": "0.25"},
    notes=["Descriptive only. Released as a CSV only for the full 816 rows."]),

"S23": dict(
    topic=RANK,
    title="Plated designs: enrichment for prediction-based metrics",
    supports="Results 3.3.2; Methods 2.4.2",
    row="one prediction-based metric, one direction and one keep fraction (232 rows)",
    contents=("The same as {S22a} for the 26 prediction-based metrics and the three sequence-only reference rows (Chai-1 with the transition-state analogue and zinc; active-site accuracy "
              "against the design's own model)."),
    columns=[("metric / canonical_key / input_class / in_main_set", "the metric"),
             ("direction / keep_fraction / n_kept / n_active_kept", "as in {S22a}"),
             ("expected_hits_per_plate / hits_lo90 / hits_hi90 / enrichment_vs_baseline", "expected hits per plate, 90% interval and ratio to 8.0")],
    excerpt=["metric", "direction", "keep_fraction", "n_active_kept", "expected_hits_per_plate"],
    where={"keep_fraction": "0.25", "direction": "high"},
    notes=["Descriptive only (16 active designs)."]),

# ----------------------------------------------------------------- 3.4
"S05": dict(
    topic=DET,
    title="Sanity floors by class of metric",
    supports="Methods 2.5 (detection floor); Results 3.4.1",
    row="one sanity-floor condition on one data set and one class of metric (53 rows)",
    contents=("The sanity-floor conditions (all catalytic residues replaced by Gly, scrambled sequence on the native backbone, unrelated "
              "protein, ligand removed on the pilot set) for the 143-enzyme set, the shortened-motif set, the pilot set and the de novo set: "
              "how many metrics of each class were scored and how many responded. One row reconciles the detection floor with the Gly step: "
              "the responses are identical on 98 of 98 metrics (the same change scored twice)."),
    columns=[("dataset / condition / input_class", "the data set, the condition and the class of metric"),
             ("n_metrics / n_scored / n_responds / n_unscored", "metrics in the class, scored, responding and not scored"), ("note", "remarks, including the reconciliation")],
    excerpt=["dataset", "condition", "input_class", "n_metrics", "n_scored", "n_responds"],
    where={"dataset": "main set (143)", "condition": "cat_to_gly"}),

"S06a": dict(
    topic=DET,
    title="Control matching: the loosest tier needed",
    supports="Methods 2.5; Results 3.4.1",
    row="one analysis, lesion test and matching tier (81 rows)",
    contents=("For each analysis and lesion test, how many (enzyme, step) entries needed each loosest matching tier: 0 = exact match, tiers 3 and "
              "above drop packing matching, tier 5 also relaxes burial (main set only), -1 = no control found; and the share of the lesion test."),
    columns=[("analysis_set / lesion_test", "the analysis (data set and controls) and the lesion test (catalytic lesion, second-shell lesion or the retired deformation experiment)"),
             ("worst_tier / n_entries / share_of_lesion_test", "loosest tier used, number of entries and their share of the lesion test"), ("note", "definition of the tiers")],
    excerpt=["analysis_set", "lesion_test", "worst_tier", "n_entries", "share_of_lesion_test"],
    where={"analysis_set": "main set, packing-matched controls", "lesion_test": "catalytic lesion"}),

"S06b": dict(
    topic=DET,
    title="Control matching: balance of residues changed in the two arms",
    supports="Methods 2.5; Results 3.4.1",
    row="one analysis and lesion test (15 rows)",
    contents=("The share of (enzyme, step) pairs in which the control arm changed fewer or more residues than the catalytic arm, the "
              "median and mean ratio, and the number with no control. The comparison of medians used elsewhere cannot see this imbalance."),
    columns=[("analysis_set / lesion_test / pairs", "the analysis, the lesion test and the number of pairs"),
             ("control_fewer_share / control_more_share", "shares with fewer or more residues changed in the control arm"),
             ("median_ratio / mean_ratio / catalytic_only_no_control", "ratio of residues changed and pairs with no control")],
    excerpt=["analysis_set", "lesion_test", "pairs", "control_fewer_share", "control_more_share", "median_ratio"]),

"S26": dict(
    topic=DET,
    title="Catalytic lesion: every metric scored (Table 10 plus supplementary comparators and per-step flags)",
    supports="Results 3.4.1; the complete version of Table 10",
    row="one metric scored on the catalytic-lesion ladder (43 rows, 41 distinct metrics)",
    contents=("Table 10 with 8 further rows (6 supplementary comparators and 2 aliases of ranked metrics) and every flag that decides whether a step counts. Metrics are grouped by the "
              "lesion step at which they are first detected and ranked by the mean of the rank statistic R over the counted steps. For each step "
              "(isosteric 15.3, non-isosteric 36.4, Ala 53.2, Gly 80.5 A3) it gives R with interval, the number of informative proteins and "
              "the flags that the metric responds, that the control response is above its noise and that the metric is specific; the number of "
              "steps counted; the first step detected and the first step at which the metric is specific (the onset of specificity); "
              "the mean R of the 143 main enzymes alone; and, for the prediction-based metrics, the "
              "distance-matched R. Structure-space metrics: 195 pooled natural enzymes (143 main + 52 pilot); prediction-based: 59 enzymes, 286 pairs."),
    columns=[("detection_group / rank_in_group / rank / rank_in_table_10", "group by first detected step, rank in the group, overall rank and rank among the 35 items of Table 10"),
             ("metric_name / canonical_key / source / input_class / role / in_ranked_set", "the metric, class, role and whether it is one of the 35 ranked items"),
             ("n_steps / n_steps_interpretable", "steps with a value and steps counted"),
             ("r_mean / r_lo / r_hi", "mean R over counted steps with 95% interval over enzyme sub-subclasses"),
             ("r_<step> / _lo / _hi / n_<step>", "R, interval and informative proteins for isosteric, non_isosteric, ala and gly"),
             ("responds_<step> / control_above_noise_<step> / specific_<step>", "the per-step flags"),
             ("first_step_detected / first_step_specific", "onsets of detection and of specificity"),
             ("r_matched / n_pairs_matched / n_systems_matched", "distance-matched R and its size (prediction-based metrics)"),
             ("r_mean_primary_only / above_best_of_all_quantities_threshold", "mean R of the 143 main enzymes and the best-of-N flag")],
    excerpt=["detection_group", "rank_in_group", "metric_name", "r_mean", "r_lo", "r_hi"],
    notes=["Descriptive of a pooled set. {S28} and {S29} hold the specificity-ratio analysis."]),

"S28": dict(
    topic=DET,
    title="Structure-space specificity by metric family and lesion step, with the panel statistic and sensitivity sets",
    supports="Results 3.4.1 and 3.4.2",
    row="one family of metrics at one lesion step or dose (20 rows)",
    contents=("The number of eligible, responding and specific structure-space metrics (as distinct metrics) by family (site-scoped "
              "Rosetta energy, catalytic geometry, catalytic pKa, all main-set metrics) at each step of the catalytic lesion and each "
              "second-shell dose, the geometric-mean specificity ratio of the main-set panel (isosteric, 1.075 [0.958, 1.178]), and the "
              "counts in four sensitivity sets (shortened motif, no packing matching or count gate, pilot set, de novo designs). "
              "At the isosteric step 23 of 29 metrics respond and none is specific; specificity appears for 5 metrics at the non-isosteric "
              "step and for 8 at the Ala and Gly steps."),
    columns=[("family / lesion_test / level / dose_value / dose_unit", "family, lesion test (catalytic lesion or second-shell lesion), step or dose and its size"),
             ("n_eligible_keys / n_responds_keys / n_specific_keys / n_cells", "counts as distinct metrics, and cells"),
             ("sr_geomean_ci90", "geometric-mean specificity ratio of the panel with 90% interval"),
             ("sens_shortened_motif / sens_no_packing_match / sens_pilot_set / sens_de_novo_set", "specific / eligible in the shortened-motif, no-packing-match, pilot and de novo sets")],
    excerpt=["family", "level", "n_eligible_keys", "n_responds_keys", "n_specific_keys", "sens_shortened_motif"],
    where={"lesion_test": "catalytic lesion"}),

"S29": dict(
    topic=DET,
    title="Re-predicted catalytic lesion: the prediction-based metrics under three successive controls and the pre-specified rule",
    supports="Results 3.4.1; Methods 2.5.1 (Eq. 24)",
    row="one prediction-based metric or reference row (6 rows)",
    contents=("Specificity of the prediction-based metrics on the natural arm of the re-predicted ladder (59 enzymes, 286 pairs): the "
              "specificity ratio on the isosteric step with the original control, in the distance-matched subset (68 pairs, 21 systems) and "
              "after regression adjustment on all steps (with the unadjusted ratio on the same pairs), and the label of the rule specified "
              "before the analysis. The ratio of the interface terms falls once the control is matched or adjusted on the distance to the "
              "ligand (ipTM: 1.96 with the original control, 0.47 in the distance-matched subset and 1.18 after adjustment); no interface "
              "term meets the rule."),
    columns=[("metric / role", "the metric and main or reference"),
             ("n_pairs_isosteric / n_systems_isosteric", "pairs and systems at the isosteric step"),
             ("sr_mean_isosteric_original_control", "specificity ratio with the original control"),
             ("distance_matched_k_of_N / sr_distance_matched", "size of the distance-matched subset and the ratio in it"),
             ("unadjusted_gmr_all_steps / adjusted_gmr_all_steps", "geometric-mean ratio over all steps, unadjusted and adjusted for distance and burial"),
             ("rule_label", "the label from the pre-specified rule (lower 90% bound above 1.2 with at least 30 pairs in 15 systems)")],
    excerpt=["metric", "sr_mean_isosteric_original_control", "sr_distance_matched", "adjusted_gmr_all_steps", "rule_label"]),

"S10": dict(
    topic=DET,
    title="Sensitivity of the specificity-ratio counts to motif size, packing matching and count gating",
    supports="Results 3.4.1",
    row="one analysis and one lesion step (20 rows)",
    contents=("Counts of eligible, responding and specific metrics at each step for five analyses: the pilot set, the main set without packing "
              "matching or count gating, the main set with packing-matched controls (primary), the main set with the motif shortened to at "
              "most 3 residues, and the 30 de novo designs with a created-site control."),
    columns=[("reader_name / motif_and_controls", "the analysis and how its motif and controls are defined"),
             ("level", "lesion step"), ("n_eligible_keys / n_responds_keys / n_specific_keys / n_cells", "counts as distinct metrics, and cells")],
    excerpt=["reader_name", "level", "n_eligible_keys", "n_responds_keys", "n_specific_keys"]),

"S16f": dict(
    topic=DET,
    title="Re-predicted ladder: seed-noise context",
    supports="Methods 2.5.1; Results 3.4.1",
    row="one prediction-based metric in one arm and subset (56 rows)",
    contents=("Noise context from the second-seed replicate on 30 natural pairs: the median absolute change in each arm against the seed "
              "noise of the metric, for the nine prediction-based metrics, on all pairs and on the original matched subset."),
    columns=[("source / metric_name / subset / arm", "natural or de novo, the metric, all_pairs or original_matched, and catalytic or control"),
             ("k_pairs / N_pairs / k_systems / N_systems", "pairs and systems"),
             ("median_abs_delta / median_sigma_native / frac_abs_delta_gt_sigma_native", "median absolute change, the metric's seed noise and the share of pairs whose change exceeds it")],
    excerpt=["metric_name", "subset", "arm", "median_abs_delta", "median_sigma_native", "frac_abs_delta_gt_sigma_native"],
    where={"source": "natural", "subset": "all_pairs"}),

"S04a": dict(
    topic=DET,
    title="Specificity ratio of every eligible metric at every step",
    supports="Methods 2.5.1 (Eq. 22); Results 3.4.1 and 3.4.2",
    row="one eligible (site-scoped) metric at one lesion step or dose (256 rows)",
    contents=("The median change at the catalytic lesion and its interval, the specificity ratio with 95% interval, whether the metric "
              "responds and whether it is specific, and the verdict: specific, non_specific, blind (does not respond), invariant "
              "(does not change) or below the floor of five units. Steps of the catalytic lesion are isosteric, non_isosteric, ala, gly; "
              "second-shell doses are second_shell_1, _2, _4."),
    columns=[("canonical_key / metric_name / input_class / in_main_set", "the metric (aliases collapse in canonical_key)"),
             ("lesion_test / level / n_systems", "catalytic lesion or second-shell lesion, the step or dose and the number of enzymes"),
             ("delta_median / delta_ci_lo / delta_ci_hi", "median change at the catalytic lesion with interval"),
             ("sr_median / sr_ci_lo / sr_ci_hi", "specificity ratio with 95% interval"),
             ("responds / specific / verdict / applicability_status", "the flags, the verdict and the applicability status")],
    excerpt=["canonical_key", "lesion_test", "level", "n_systems", "sr_median", "verdict"],
    where={"in_main_set": "1", "level": "ala"}),

"S04b": dict(
    topic=DET,
    title="Specificity ratio of whole-protein and sequence-only comparators at every step",
    supports="Methods 2.5.1; Results 3.4",
    row="one comparator metric at one lesion step or dose (308 rows)",
    contents=("The same cells as {S04a} for the whole-protein and sequence-only metrics, which are not in the main set. Composition "
              "metrics have no ratio in 147 of their 203 cells and, in the other 56, a ratio between 0.5 and 2.7 (9 cells equal 1); whole-protein energies move with the lesion."),
    columns=[("canonical_key / metric_name / input_class", "the comparator"), ("lesion_test / level / n_systems", "as in {S04a}"),
             ("delta_*, sr_*, responds, specific, verdict", "as in {S04a}")],
    excerpt=["canonical_key", "lesion_test", "level", "n_systems", "sr_median", "verdict"],
    where={"level": "ala"}),

"S07": dict(
    topic=DET,
    title="The specific cells that survive the controls",
    supports="Methods 2.5.1; Results 3.4.1",
    row="one metric at one step in one analysis (97 rows: 74 natural, 23 de novo)",
    contents=("The cells that are specific under the control of their analysis, with the specificity ratio, the population "
              "(natural or de novo) and the applicability status of the metric. Of the 97, 69 are of metrics with status OK, 27 of whole-protein "
              "comparators (GLOBAL) and 1 of a metric with too little coverage."),
    columns=[("analysis_set / lesion_test / level", "the analysis, the lesion test and the step"),
             ("metric_name / canonical_key / input_class / in_main_set", "the metric"),
             ("sr_text", "specificity ratio with interval, as text"),
             ("applicability_status / population", "applicability status and natural or de novo")],
    excerpt=["analysis_set", "lesion_test", "level", "metric_name", "sr_text", "population"],
    where={"analysis_set": "main set, packing-matched controls", "in_main_set": "1"}),

"S12": dict(
    topic=DET,
    title="Rank statistic R per lesion step on the 143 main enzymes",
    supports="Methods 2.5.1 (Eq. 19)",
    row="one metric at one step of the catalytic lesion (313 rows)",
    contents=("The rank statistic R (probability that a metric changes more at the catalytic lesion than at the matched control) for the "
              "143 main enzymes alone, with 90% intervals, for 83 distinct metrics including comparators. This is the per-step form "
              "of R on the main enzymes; Table 10 and {S26} report the pooled analysis on 195 enzymes with 95% intervals and the counted-step rule, so the values "
              "for the same metric differ."),
    columns=[("metric_name / canonical_key / input_class / in_main_set", "the metric"),
             ("lesion_step / volume_A3", "lesion step and its median side-chain volume change"),
             ("R / R_lo90 / R_hi90 / n_systems / n_clusters", "R with 90% interval, enzymes and enzyme sub-subclasses"),
             ("responds / interpretable", "whether the metric responds and whether R is interpretable"), ("applicability_status", "applicability status")],
    excerpt=["metric_name", "lesion_step", "R", "R_lo90", "R_hi90", "n_systems"],
    where={"in_main_set": "1", "lesion_step": "ala"}),

"S16a": dict(
    topic=DET,
    title="Re-predicted ladder: distance of the substituted and control residues to the ligand",
    supports="Methods 2.5.1; Results 3.4.1",
    row="one catalytic/control pair of the ladder (312 pairs: 286 natural, 26 de novo)",
    contents=("For every pair the residue types, the burial of each residue, the distance of the substituted and of the control residue to "
              "the ligand (in the reference structure and in the prediction), whether the control is adjacent to a catalytic residue, "
              "and whether the pair falls in each of the calipers used in {S16c}."),
    columns=[("source / base_system / level", "natural or denovo, the system and the lesion step"),
             ("wt / new_aa / cat_position / ctl_position", "residue substituted and its position in the catalytic and control arms"),
             ("cat_rel_sasa / ctl_rel_sasa / abs_diff_rel_sasa", "relative accessible area of the two residues and the difference"),
             ("d_lig_cat_ref / d_lig_ctl_ref / abs_diff_d_lig_ref", "distance to the ligand in the reference structure (A)"),
             ("d_lig_cat_chai / d_lig_ctl_chai", "distance in the Chai-1 prediction"),
             ("control_adjacent_to_catalytic / ligand_status", "adjacency to a catalytic residue; whether the ligand could be located"),
             ("in_caliper_*", "membership of the primary caliper and of sensitivity calipers")],
    excerpt=["base_system", "level", "wt", "new_aa", "d_lig_cat_ref", "d_lig_ctl_ref", "abs_diff_rel_sasa"],
    where={"source": "natural", "level": "isosteric", "ligand_status": "ok"},
    notes=["Released as a CSV only for the full 312 rows."]),

"S16e": dict(
    topic=DET,
    title="Re-predicted ladder: candidates for a new distance-matched control",
    supports="Methods 2.5.1; Results 3.4.1",
    row="one candidate control for one pair that had no control within the caliper (291 rows)",
    contents=("The candidate controls for the pairs that had none in the caliper, which were selected (54 pairs, 53 new predictions), their "
              "distances and burial, and the reason when none was selected (no candidate in the caliper for 213 pairs; no reference distance "
              "for 20; no ligand in the baseline prediction for 4)."),
    columns=[("base_system / source / level", "system, natural or de novo, step"),
             ("wt / new_aa / cat_position / orig_ctl_position / new_ctl_position", "the substitution and the original and new control positions"),
             ("d_lig_cat_ref / d_lig_ctl_new / abs_diff_d", "distances to the ligand and their difference"),
             ("cat_rel_sasa / ctl_rel_sasa_new / abs_diff_rel", "burial and its difference"),
             ("n_candidates / selected / reason", "number of candidates, 1 if selected, and the reason when not")],
    excerpt=["base_system", "level", "new_ctl_position", "d_lig_cat_ref", "d_lig_ctl_new", "selected", "reason"],
    where={"selected": "1"}),

"S16b": dict(
    topic=DET,
    title="Re-predicted ladder: specificity ratio in strata of the distance to the ligand",
    supports="Methods 2.5.1; Results 3.4.1",
    row="one metric in one distance stratum, for one source (203 rows)",
    contents=("The specificity ratio of each metric in the near, mid and far third of the pairs by the distance of the substituted residue "
              "to the ligand (edges 2.73 and 3.66 A), and on all pairs, with the median distances of the two arms."),
    columns=[("source / metric_name / role / applicability_status / headline", "the metric, interface or global, applicability status and whether it is a headline row"),
             ("stratum / edge_lo / edge_hi / k_pairs / k_systems", "the stratum and its size"),
             ("SR_mean (+ lo/hi 95 and 90) / SR_median (+ lo/hi 95)", "specificity ratio of the mean and of the median change with intervals"),
             ("mean_abs_delta_cat / mean_abs_delta_ctl", "mean absolute change in the two arms"),
             ("median_d_lig_cat / median_d_lig_ctl / median_abs_diff_d_lig", "median distances to the ligand")],
    excerpt=["metric_name", "stratum", "k_pairs", "k_systems", "SR_mean", "SR_mean_lo95", "SR_mean_hi95"],
    where={"source": "natural", "metric_name": "chai_iptm_mean"}),

"S16c": dict(
    topic=DET,
    title="Re-predicted ladder: caliper-matched subsets and the rule labels",
    supports="Methods 2.5.1; Results 3.4.1 (68 to 69 pairs in 21 to 22 systems)",
    row="one metric in one matched subset for one source (348 rows)",
    contents=("The specificity ratio in caliper-matched subsets: original_controls (original controls within the caliper), "
              "original_plus_new_controls (with the new controls added, the subset of Table 10) and the sensitivity sets "
              "distance_in_prediction, distance_to_organic_atoms, caliper_1A and caliper_3A that use other distance "
              "definitions and calipers, with the label from the pre-specified rule (lower 90% bound above 1.2 with at least 30 pairs in 15 systems)."),
    columns=[("source / metric_name / role / applicability_status", "the metric and its status"),
             ("set_id / control", "the matched subset and original or original+new controls"),
             ("k_pairs / k_systems / N_pairs / N_systems", "subset size and total"),
             ("SR_mean (+ lo/hi) / SR_median (+ lo/hi)", "specificity ratio with intervals"),
             ("verdict / rule_applies", "the label (for example not_testable (coverage), global_comparator_no_verdict) and whether the pre-specified rule applies")],
    excerpt=["metric_name", "set_id", "k_pairs", "k_systems", "SR_mean", "verdict"],
    where={"source": "natural", "metric_name": "chai_iptm_mean"}),

"S16d": dict(
    topic=DET,
    title="Re-predicted ladder: regression-adjusted ratios",
    supports="Methods 2.5.1 (Eq. 24); Results 3.4.1",
    row="one metric with the original or the extended set of controls, for one source (116 rows)",
    contents=("The ratio of catalytic to control change adjusted for the distance to the ligand and the burial, "
              "log(|delta| + eps) ~ arm + d_lig + relSASA, beside the unadjusted ratio on the same pairs, and the regression coefficients."),
    columns=[("source / metric_name / role / applicability_status", "the metric"),
             ("model / control", "the regression and original_controls or plus_new_controls"),
             ("k_pairs / k_systems / n_rows / eps", "size and the small constant that keeps zero changes finite"),
             ("adj_GMR_cat_over_ctl (+ lo/hi95)", "adjusted geometric-mean ratio"), ("unadj_GMR_cat_over_ctl (+ lo/hi95)", "unadjusted ratio on the same pairs"),
             ("beta_d_lig_per_A / beta_relSASA (+ lo/hi95)", "coefficients per A of distance and per unit of relative accessible area")],
    excerpt=["metric_name", "control", "k_pairs", "adj_GMR_cat_over_ctl", "unadj_GMR_cat_over_ctl"],
    where={"source": "natural", "metric_name": "chai_iptm_mean"}),

"S11": dict(
    topic=DET,
    title="Panel equivalence statistic: earlier whole panel against the main-set metrics",
    supports="Results 3.4.1; Methods 2.5.1 (equivalence to 1)",
    row="one analysis and set of metrics (6 rows)",
    contents=("The geometric-mean specificity ratio of the panel with a 90% interval (nested bootstrap that recomputes every metric inside "
              "each draw), for the earlier whole panel (100 to 103 metrics, including composition metrics, most of which have no ratio or a ratio close to 1) and "
              "for the 27 main-set metrics with a defined ratio (isosteric step: 1.075 [0.958, 1.178])."),
    columns=[("analysis_set / metric_set / n_metrics", "the analysis, the set of metrics and its size"),
             ("geomean_sr / ci90_lo / ci90_hi / median_sr", "geometric-mean ratio, 90% interval and median"), ("n_clusters / status / note", "resampling clusters, status and remarks")],
    excerpt=["analysis_set", "metric_set", "n_metrics", "geomean_sr", "ci90_lo", "ci90_hi"]),

"S15": dict(
    topic=DET,
    title="Re-predicted ladder: specificity ratio per step for all metrics",
    supports="Methods 2.5.1; Results 3.4.1",
    row="one metric at one step for one source (231 rows)",
    contents=("The re-predicted catalytic-lesion ladder per step (ALL steps pooled, isosteric, non-isosteric, Ala, Gly) for all 44 named quantities (24 distinct metrics; 33 quantities each for natural "
              "and for de novo enzymes): pairs and systems, specificity ratio (median and mean) with intervals, and the verdict of the earlier rule."),
    columns=[("source / metric_name / canonical_key / input_class / ame_flavour", "the metric"), ("level / n_pairs / n_systems", "step and size"),
             ("sr_median / sr_lo / sr_hi", "ratio of medians with interval"), ("sr_mean / sr_mean_lo / sr_mean_hi", "ratio of means with interval"),
             ("verdict_earlier_rule / applicability_status", "verdict of the earlier rule and applicability status")],
    excerpt=["metric_name", "level", "n_pairs", "n_systems", "sr_mean", "sr_mean_lo", "sr_mean_hi"],
    where={"source": "natural", "level": "isosteric", "canonical_key": "chai_iptm"}),

"S12b": dict(
    topic=DET,
    title="Effective dimensionality of the panel",
    supports="Results 3.4.1",
    row="one set of metrics and one panel (4 rows)",
    contents=("The participation ratio and related measures of the effective number of independent metrics, for the earlier whole panel and for "
              "the 29 structure-space main-set metrics, for native values (7.85 of 29) and for isosteric responses (10.5 of 23)."),
    columns=[("metric_set / panel / n_metrics / n_systems_complete", "the set, the panel and sizes"),
             ("participation_ratio / effective_rank_fraction", "effective number of independent metrics and its share"),
             ("var_explained_pc1 / n_pcs_for_90pct / median_abs_offdiag_r", "variance in the first component, components for 90% and median absolute correlation between metrics")],
    excerpt=["metric_set", "panel", "n_metrics", "participation_ratio", "var_explained_pc1"]),

"S09": dict(
    topic=DET,
    title="De novo designs: burial equivalence of the created-site control",
    supports="Results 3.4.1",
    row="one burial metric (5 rows)",
    contents=("In the 30 de novo designs the control is a position mutated to the catalytic residue type. For the five burial metrics the "
              "table gives the catalytic-arm and control-arm medians, the paired difference with 90% interval and whether they differ."),
    columns=[("metric / n_systems / n_clusters", "the burial metric, designs and backbone clusters"),
             ("catalytic_arm_median / control_arm_median", "medians in the two arms"),
             ("paired_diff_median / paired_diff_ci90_lo / paired_diff_ci90_hi / ratio_median", "paired difference with interval and ratio"), ("differs / note", "1 if the arms differ")],
    excerpt=["metric", "n_systems", "catalytic_arm_median", "control_arm_median", "paired_diff_median", "differs"]),

"S08": dict(
    topic=DET,
    title="Experiments that could not be made or were retired",
    supports="Results 3.4.1",
    row="one experiment (9 rows)",
    contents=("The deformation experiment (apparent specific cells track the clash burden present before repacking), oxyanion-hole removal "
              "(the step that was run located no bound ligand in any of the 143 structures and removed a proxy residue, so it did not test the named "
              "change), metal removal (no cell could be scored on any metric), the de novo second shell and deformation experiments, PLACER on the "
              "isosteric step, the unrelated-protein sanity floor and the two trapping-mutant tiers."),
    columns=[("reader_name / claim_type", "the experiment and the kind of claim it would have supported"),
             ("role", "retired or not_measurable"),
             ("mechanism_or_caveat", "why it could not be made")],
    excerpt=["reader_name", "role", "mechanism_or_caveat"]),

"S13": dict(
    topic=DET,
    title="PLACER ensemble metrics on the isosteric step (not interpretable)",
    supports="Results 3.4.1",
    row="one PLACER metric in one analysis (50 rows)",
    contents=("The specificity ratio, verdict and applicability of 25 PLACER ensemble metrics on the isosteric step, in two analyses. They are "
              "not interpretable: the control arm is covered 1.6 to 3.2 times less than the catalytic arm in every crop configuration, so the "
              "count of specific metrics moves with the crop anchor alone."),
    columns=[("analysis_set / metric_name / level / n_systems", "the analysis, the metric, the step and enzymes"),
             ("sr_median / sr_ci_lo / sr_ci_hi", "specificity ratio with 95% interval"),
             ("responds / specific / verdict / applicability_status", "flags, verdict (blind, non_specific, specific, no_dynamic_range) and status (GLOBAL or X-CONFOUND)")],
    excerpt=["analysis_set", "metric_name", "n_systems", "sr_median", "verdict", "applicability_status"]),

"S27": dict(
    topic=DET,
    title="Second-shell lesion: every metric scored (Table 11 plus supplementary comparators and per-dose flags)",
    supports="Results 3.4.2; the complete version of Table 11",
    row="one metric scored on second-shell removal (37 rows, 35 distinct metrics)",
    contents=("Table 11 with 8 further rows (6 supplementary comparators and 2 aliases of ranked metrics) and the flags at each dose (1, 2 and 4 residues removed): R with interval, the number "
              "of informative proteins, and whether the metric responds, whether the control response is above its noise and whether it is "
              "specific. No step counts for any metric, so no rank on this test is interpretable and no reference level is computed."),
    columns=[("detection_group / rank_in_group / rank / rank_in_table_11", "group by first dose detected, rank in the group, overall rank and rank among the 29 items of Table 11"),
             ("metric_name / canonical_key / source / input_class / role / in_ranked_set", "the metric and its role"),
             ("n_steps / n_steps_interpretable", "doses with a value and counted (0 for every metric)"),
             ("r_second_shell_<d> / _lo / _hi / n_second_shell_<d>", "R, interval and informative proteins at dose 1, 2 and 4"),
             ("responds_ / control_above_noise_ / specific_second_shell_<d>", "per-dose flags"),
             ("r_mean_all_steps / first_step_detected / first_step_specific", "mean R over all doses and the onsets")],
    excerpt=["detection_group", "rank_in_group", "metric_name", "r_mean_all_steps", "n_steps_interpretable"],
    notes=["Both arms are scored over the catalytic residues."]),
}
