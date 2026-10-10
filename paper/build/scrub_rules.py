"""Rules that turn the private tables in tables/ into the public tables in
tables/public/ without internal codes.

Nothing here changes a result: columns that only point into the private project
are dropped, internal codes are replaced by the plain names used in the paper,
and free text is reworded. make_public_tables.py applies these rules and
check_public_text.py fails the build if an internal token is left.
"""
import re

# ------------------------------------------------------------------ columns
# Pointers into the private project (paths, hashes, test and dataset ids).
DROP_COLS = {
    "source_artifacts", "source_artifact", "source_sha256", "artifacts", "evidence_path", "system_table",
    "code_ref", "source_original", "source_new", "n0_artifact",
    "test_id", "test_id_status", "test_id_primary", "test_ids", "rule_id", "in_artifact",
    "dataset_id", "phase_code", "in_glossary",
    "v1_test", "v2a_test",
    "legacy_rho_all_N0_levels", "legacy_rho_given_length",
}
# (table, column): dropped only in that table.
DROP_TABLE_COLS = {
    ("S03", "part"),           # internal experiment labels 1A / 1B / 2A / 2B
    ("S22b", "note"),          # only said that the legacy columns are not valid
    ("S16e", "input_id"), ("S16e", "existing_prediction"), ("S16e", "needs_gpu"),   # scheduling of the new predictions
    ("S16e", "priority_rank"), ("S16e", "system_round"),
}

TABLE_RENAME_COLS = {("S16g", "input_id"): "prediction"}

RENAME_COLS = {
    "status_a3": "applicability_status", "a3_status": "applicability_status",
    "status_a3_P2K_C": "applicability_status",
    "share_of_axis": "share_of_lesion_test", "phase": "analysis_set", "axis": "lesion_test",
    "axis_levels": "levels", "axes_levels": "levels",
    "p0b_auroc_vs_null": "auroc_vs_same_state_null", "p0b_n_zymogen": "n_zymogen_pairs",
    "p0b_n_null": "n_same_state_null_pairs",
    "sens_P2S": "sens_shortened_motif", "sens_P2": "sens_no_packing_match",
    "sens_P1": "sens_pilot_set", "sens_P3v2": "sens_de_novo_set",
    "frozen_rule_label": "rule_label",
    "in_caliper_S1_chai": "in_caliper_prediction_distance", "in_caliper_S2_organic": "in_caliper_organic_atoms",
    "in_caliper_S3_1A": "in_caliper_1A", "in_caliper_S3_3A": "in_caliper_3A",
    "scope_cat_arm": "scope_catalytic_arm", "scope_ctl_arm_CG": "scope_control_arm_catalytic_lesion",
    "scope_ctl_arm_E": "scope_control_arm_second_shell", "glossary_family": "metric_family",
    "unadjusted_gmr_all_rungs": "unadjusted_gmr_all_steps", "adjusted_gmr_all_rungs": "adjusted_gmr_all_steps",
    "rung": "lesion_step", "claim_id": "analysis",
    "v1_status": "status_detection_test", "v1_fraction": "fraction_detection_test",
    "v2a_status": "status_dead_vs_active_tests", "v2a_fraction": "fraction_dead_vs_active_tests",
    "v2a_partial": "partial_dead_vs_active_tests", "v2b_status": "status_ranking_tests",
    "v2b_tests_ok": "ranking_tests_ok", "part": "test_group",
    "verdict_legacy_rule": "verdict_earlier_rule",
}

# ------------------------------------------------------------------ names of analyses and lesions
LESION = {"C": "catalytic lesion", "E": "second-shell lesion", "G": "deformation"}
ANALYSIS = {
    "P1": "pilot set", "P2": "main set", "P2K": "main set, packing-matched controls",
    "P2KE": "main set, second-shell lesion", "P2S": "shortened motif (<=3 residues)",
    "P3": "de novo set (earlier version)", "P3V2": "de novo set, created-site control",
    "P3v2": "de novo set, created-site control",
}
MODE = {"M1": "structure-space", "M3": "prediction-based", "any": "any", "real": "deposit metadata",
        "baseline": "baseline", "PLACER": "PLACER"}
TEST_CLASS = {
    "spec_C": "catalytic lesion, structure-space", "spec_E": "second-shell lesion, structure-space",
    "G": "deformation (retired)", "S_m3": "substrate swap", "ladder_m3": "catalytic lesion, prediction-based",
    "real_m1": "dead against active, structure-space", "real_m3": "dead against active, prediction-based",
    "rank_m1": "activity ranking, structure-space", "rank_m3": "activity ranking, prediction-based",
    "sanity_n0": "sanity floor", "detection_dup": "detection floor (duplicate of the Gly step)",
    "placer_c": "PLACER on the isosteric step",
}
SHORT_TEST = {"D4_BGLB_M1": "BglB structure-space", "P6_PLATES_M1": "plates structure-space",
              "D4_BGLB_M3": "BglB prediction-based", "P6_PLATES_M3": "plates prediction-based"}

VALUE_MAPS = {
    "lesion_test": LESION, "mode": MODE, "valid_modes": MODE, "test_class": TEST_CLASS,
    "analysis_set": {**ANALYSIS},
    "invariant_under": {"G": "deformation"},
    "set_id": {"M0": "original_controls", "M1": "original_plus_new_controls", "S1_chai": "distance_in_prediction",
               "S2_organic": "distance_to_organic_atoms", "S3_1A": "caliper_1A", "S3_3A": "caliper_3A"},
    "stratum": {"T1_near": "near_third", "T2_mid": "middle_third", "T3_far": "far_third"},
    "analysis": {"a_distance_strata": "distance strata", "b_matched": "matched subsets",
                 "c_adjusted": "regression adjustment",
                 "main": "main analysis", "S1near": "variants near the catalytic residues",
                 "S1distal": "variants distal from the catalytic residues", "S2": "measured stability only",
                 "S3_FIU": "leave out FIU", "S3_MiraCosta": "leave out MiraCosta", "S3_UC_Davis": "leave out UC Davis",
                 "S4_1": "impaired threshold 1 SD", "S4_3": "impaired threshold 3 SD",
                 "S5": "responding metrics only", "S6": "without catalytic-position variants"},
    "role": {"supp_part2_only": "supp_real_protein_tests_only"},
    "subset": {"M0_matched": "original_matched"},
    "status": {"complete (distance control: blocked_on_1B)": "complete"},
    "condition": {"RECONCILIATION cat_to_gly vs C-Gly": "check: cat_to_gly against the Gly step"},
}

# pair_set names in the pair-set definitions
VALUE_MAPS["pair_set"] = {
    "P0 scored pairs (wider set)": "scored pairs (wider set)", "P0 PLACER pairs": "pairs with PLACER",
    "T2 zymogen pairs": "re-predicted pairs", "P0b same-state null pairs": "same-state null pairs",
}

# ------------------------------------------------------------------ free text (exact cell values)
# «S22c» in a key or value stands for the S number of that table in the current numbering (table_ids.csv)
TEXT_EXACT = {
    # T1 / T2
    "interface + AME metrics (main-set membership decided by 1B and 2B)": "interface + AME metrics",
    "cognate condition + 5-seed noise floor (no X control)": "cognate condition + 5-seed noise floor",
    "matched X control": "matched control", "matched X control + distance caliper": "matched control + distance caliper",
    "N0 cat_to_gly (identical to the C-Gly rung; read once)": "detection floor: all catalytic residues to Gly (identical to the Gly step; read once)",
    "TSA supplied for M3": "TSA supplied for the prediction-based metrics",
    "none in the M1 panel": "none in the structure-space panel",
    "main natural set (packing-matched controls = P2K)": "main natural set (packing-matched controls)",
    "M3 chemistry-ladder pairs": "prediction-based chemistry-ladder pairs",
    "S axis: substrate swap (natural enzymes)": "Substrate swap (natural enzymes)",
    "S axis: substrate swap (de novo designs)": "Substrate swap (de novo designs)",
    "C axis: chemistry ladder": "Catalytic lesion: chemistry ladder",
    "E axis: second-shell support removed": "Second-shell lesion: second-shell support removed",
    "C axis re-predicted: one residue substituted per prediction": "Catalytic lesion re-predicted: one residue substituted per prediction",
    "measured label; 176 'no reported activity' are NOT negatives": "measured label; the 176 'no active' designs are not confirmed negatives",
    "reported kcat/KM vs no reported activity (NOT inactive)": "active (reported kcat/KM) vs no active (not confirmed inactive)",
    # T7, T8, T9
    "descriptive only (human ruling 2026-08-09; relaxed on 2026-10-09 only for the AUROC of Table 4): Spearman rank correlation with log10 kcat/KM over the 16 designs that have a reported value (the other 176 have no measurement); no direction is fixed in advance, so ranked by the size of rho; 90% interval resamples designs; a 90% interval excludes 0 for about 10% of unrelated items, that is about 3.6 of the 36; rho_given_length partials the sequence length out of both sides; ranks 31 to 36 are in «S22c» (column rank_in_table_6)":
        "descriptive analysis: Spearman rank correlation with log10 kcat/KM over the 16 designs that have a reported value; ranked by the size of rho; 90% interval resamples designs; a 90% interval excludes 0 for about 10% of unrelated items, that is about 3.6 of the 36; rho_given_length partials the sequence length out of both sides; ranks 31 to 36 are in «S22c» (column rank_in_table_9)",
    # S3, S4
    "any Ser/Cys/Thr + His among the scored residues; in the X arm these are control residues; the row is absent when Ser/His is substituted":
        "any Ser/Cys/Thr + His among the scored residues; in the control arm these are control residues; the row is absent when Ser/His is substituted",
    "interface term: promoted/demoted by the rule frozen in PREREG_1B.md": "interface term: classified by the pre-specified rule for the predictor",
    "duplicate of the primary C-Gly cell; read once from the primary test": "duplicate of the primary Gly-step cell; read once from the primary test",
    "no matched X control in this test, so no specificity statement is possible": "no matched control in this test, so no specificity statement is possible",
    # S2 (main metric set)
    "valid in Part 1 (primary test) and Part 2 (2A and 2B)": "valid in the primary detection-ability test and in the activity tests",
    "valid in Part 1 but not Part 2 -> 2B:X-UNDEF-COV,X-ARM": "valid in the primary detection-ability test but not in the activity-ranking tests (X-UNDEF-COV, X-ARM)",
    "valid in Part 1 but not Part 2 -> 2A:X-UNDEF-COV": "valid in the primary detection-ability test but not in the dead-against-active tests (X-UNDEF-COV)",
    "Part 1 primary test status X-UNDEF-COV": "primary detection-ability test status X-UNDEF-COV",
    "PLACER: crop-coverage confound in Part 1; no 2B coverage": "PLACER: crop-coverage confound in the primary detection-ability test; not computed in the activity-ranking tests",
    # S7
    "N0: cat_to_gly": "detection floor: cat_to_gly", "N0: seq_scramble": "sanity floor: seq_scramble",
    "N0: ligand_removed": "sanity floor: ligand_removed", "N0: unrelated_protein": "sanity floor: unrelated_protein",
    "identical to the C-Gly rung: responds equal on 98/98 metrics (P2) and 96/96 (P2S)": "identical to the Gly step: responses equal on 98/98 metrics (main set) and 96/96 (shortened motif)",
    "as P2K; motif truncated to <=3 residues": "as the main set with packing-matched controls; motif truncated to <=3 residues",
    "as P2KE; motif <=3": "as the second-shell lesion of the main set; motif <=3",
    "motif size is a co-primary column: C-axis specific cells 5 (P2S) vs 28 (P2K)": "motif size changes the result: 5 specific cells with the shortened motif against 28 with the full motif",
    "P2K vs P2KE second-shell cells differ in 3 of 318 (repack nondeterminism)": "second-shell cells of two runs differ in 3 of 318 (repacking is not deterministic)",
    "37/42 (P2) and 40/47 (P2K) apparent specific cells track pre-repack clash burden": "37 of 42 (main set) and 40 of 47 (packing-matched main set) apparent specific cells track the clash burden present before repacking",
    "to be built by Agent 1B": "residue type exact + burial; matched on the distance to the ligand",
    "filled by Agent 1B": "",
    "PLACER on the isosteric rung (P2K)": "PLACER on the isosteric step",
    "retired tier; REPORT_T2.md still calls it the clean test": "retired tier",
    "descriptive only (2026-08-09 ruling); 16 actives; designs already filtered by the campaign; the ORDERING file results/P6/activity_ranking.csv averaged over all N0 levels (corrected copy: tables/spec/derived/p6_activity_ranking_native.csv); the enrichment rows are unaffected":
        "descriptive analysis; 16 actives; designs already filtered by the campaign",
    "descriptive only (2026-08-09 ruling); 16 actives; cluster-level N 136 (backbone clusters are a proxy); Chai-1 is not bitwise reproducible (drift up to 0.0105)":
        "descriptive analysis; 16 actives; cluster-level N 136 (backbone clusters are a proxy); Chai-1 is not bitwise reproducible (drift up to 0.0105)",
    "deformation (geometry) axis": "deformation (geometry) experiment", "de novo set, deformation axis": "de novo set, deformation experiment",
    "environment re-sweep, second shell": "second-shell lesion, main set",
    "C: isosteric; non_isosteric; ala; gly": "catalytic lesion: isosteric; non_isosteric; ala; gly",
    "C: isosteric only": "catalytic lesion: isosteric only",
    "E: second_shell 1/2/4 residues": "second-shell lesion: 1/2/4 residues", "E: second_shell 1/2/4": "second-shell lesion: 1/2/4 residues",
    "E: oxyanion_removed": "second-shell lesion: oxyanion_removed", "E: metal_removed": "second-shell lesion: metal_removed",
    "G: deform 0.25-3.0 A; chi inversion": "deformation: 0.25-3.0 A; chi inversion", "G: deform; inversion": "deformation: deform; inversion",
    "S: cognate; same_ec; diff_ec; decoy; apo": "substrate swap: cognate; same_ec; diff_ec; decoy; apo",
    "C (M3): isosteric; non_isosteric; ala; gly; one residue substituted per prediction": "catalytic lesion, prediction-based: isosteric; non_isosteric; ala; gly; one residue substituted per prediction",
    "C (M3)": "catalytic lesion, prediction-based", "C (M3) with d_lig caliper": "catalytic lesion, prediction-based, with a ligand-distance caliper",
    "D: zymogen vs mature": "zymogen vs mature", "D: trapping mutant vs WT": "trapping mutant vs wild type",
    "D: zymogen vs mature, same ligand set": "zymogen vs mature, same ligand set", "D: trapping vs WT": "trapping mutant vs wild type",
    # S21, S22 (plates)
    "one metric on the 192 plated designs; descriptive only (human ruling 2026-08-09; relaxed on 2026-10-09 only for the AUROC of Table 4); unfiltered plate 8.0 hits; a random choice of 48 designs holds more than 14.0 hits with probability 0.022 and either end of a random metric does so with probability 0.044 (hypergeometric)":
        "one metric on the 192 plated designs; descriptive analysis; unfiltered plate 8.0 hits; a random choice of 48 designs holds more than 14.0 hits with probability 0.022 and either end of a random metric does so with probability 0.044 (hypergeometric)",
    "one metric on the 16 designs with a reported kcat/KM; descriptive only (human ruling 2026-08-09; relaxed on 2026-10-09 only for the AUROC of Table 4)":
        "one metric on the 16 designs with a reported kcat/KM; descriptive analysis",
    # S26, S27, S30
    "identical to the C-Gly rung (reconciliation row below)": "identical to the Gly step (reconciliation row below)",
    "-1 = no control matched; 0 = exact; tiers >=3 drop packing; 5 also relaxes burial (P2K only; P2 tiers are not comparable: packing was not a criterion)":
        "-1 = no control matched; 0 = exact; tiers >=3 drop packing; 5 also relaxes burial (main set with packing matching only; tiers of the analysis without packing matching are not comparable)",
    "detection read once here: N0 cat->Gly is identical to this rung («S05»); primary = packing-matched, count-gated main set; control quality in «S06a» and «S06b»":
        "detection floor read once here: all catalytic residues to Gly is identical to this step («S05»); primary = packing-matched, count-gated main set; control quality in «S06a» and «S06b»",
    "legacy 102-metric statistic (0.958 [0.897, 1.084]) included ~34 composition metrics with SR = 1 by construction":
        "the earlier 102-metric statistic (0.958 [0.897, 1.084]) included ~34 composition metrics with SR = 1 by construction",
    # S39, S43, S45, S47
    "baseline_prediction_has_no_ligand (A1.1, A4)": "baseline_prediction_has_no_ligand",
    "legacy panel (all metrics with a testable cell)": "earlier whole panel (all metrics with a testable cell)",
    "legacy panel": "earlier whole panel",
    "restricted to the metrics valid in both parts; same construction (phase P2, complete cases)": "restricted to the metrics valid in all four tests; same construction (main set, complete cases)",
    "37/42 (P2) and 40/47 (P2K) apparent specific cells track pre-repack clash burden ": "",
}

# regex fallbacks, applied in order to any text cell not matched above
TEXT_REGEX = [
    (re.compile(r"valid in Part 1 \(primary test\) and Part 2 \(2A and 2B\)"), "valid in the primary detection-ability test and in the activity tests"),
    (re.compile(r"promoted by testability under 1B: 1B outcome: "), "promoted by testability in the predictor ladder: "),
    (re.compile(r"\s*\(tables/spec/derived/[\w.]+\)"), ""),
    (re.compile(r"the blindness-map counts gate compares MEDIANS"), "the response counts compare medians"),
    (re.compile(r"\bone metric on axis C;"), "one metric for the catalytic lesion;"),
    (re.compile(r"\bone metric on axis E;"), "one metric for the second-shell lesion;"),
    (re.compile(r"blindness map of the 143 main enzymes"), "response analysis of the 143 main enzymes"),
    (re.compile(r"the primary blindness map"), "the response analysis of the main enzymes"),
    (re.compile(r"\s*\(tables/spec/derived/axis_ranking_meta\.json\)"), ""),
    (re.compile(r"distance-matched subset M1\b"), "distance-matched subset"),
    (re.compile(r"\bno reported activity\b"), "no active"),
    (re.compile(r"\breported active\b"), "active"),
    (re.compile(r"\bmatched X control\b"), "matched control"),
    (re.compile(r"\bC-Gly (?:rung|step)\b"), "Gly step"),
    (re.compile(r"\blegacy\b"), "earlier"),
    (re.compile(r"\brungs?\b"), lambda m: "steps" if m.group(0).endswith("s") else "step"),
    (re.compile(r"\bglossary says\b"), "the earlier metric description says"),
    (re.compile(r"absent from the glossary"), "not in the earlier metric description"),
    (re.compile(r"; code is "), "; computed as "),
    (re.compile(r"\(p0b columns\)"), "(same-state null columns)"),
    (re.compile(r"\s*\((?:decision|ruling) of \d{4}-\d{2}-\d{2}\)"), ""),
]

# test labels for S4 / S5 (replace test_id): built from the private test inventory
def test_label(reader_name, test_class):
    return f"{reader_name} [{TEST_CLASS.get(test_class, test_class)}]"

# ------------------------------------------------------------------ roles that were run
ROLE_FIX = {   # reader_name of the experiment -> role
    "BglB single-point variants (prediction-based metrics)": "primary",
    "plate designs (prediction-based metrics)": "primary",
    "chemistry ladder with ligand-distance-matched controls (new)": "sensitivity",
}

# ------------------------------------------------------------------ file names and titles
FILE_SLUG = {
    "T8": "specificity_catalytic_lesion", "T9": "specificity_second_shell_lesion",
    "S26": "catalytic_lesion_all_metrics_ranked", "S27": "second_shell_lesion_all_metrics_ranked",
    "S11": "equivalence_earlier_vs_main_panel",
}
MAIN_TITLES = {
    "T8": "Specificity for the catalytic lesion: the 35 items grouped by the lesion step at which they are first detected and ranked by the rank statistic R within the group (Results 3.4.1)",
    "T9": "Specificity for the second-shell lesion: the 29 metrics grouped by the dose at which they are first detected and ranked by the rank statistic R within the group (Results 3.4.2)",
}
