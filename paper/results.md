# 3 Results

Each subsection follows one order: the experiment, the dataset, the criteria by which the metrics are ranked, and the result table. Counts of metrics are of distinct metrics in the main set of 33 (29 structure-space, 4 prediction-based; Box 2 of the Methods), and intervals are 95% bootstrap intervals that resample the unit named in each subsection, unless stated otherwise. Numbers in square brackets are references, listed at the end of this section. The complete per-metric tables are in the Supplement.

---

## 3.1 Activity discrimination test

**Experiment.** Metrics are scored on real proteins in which one state has no catalytic activity and the other has it, and each metric is ranked by how well its value separates the two states. Nothing is perturbed (Methods 2.1). Two datasets are used, each with its own table.

### 3.1.1 Zymogen–mature pairs

**Dataset.** 21 zymogen–mature pairs from 21 peptidases (9 serine, 8 cysteine, 4 aspartic), downloaded from the RCSB Protein Data Bank [1, 2]. The zymogen is the dead form and the mature enzyme the active form, and the two forms share a ligand. Catalytic residues come from M-CSA [3] and UniProt [4] annotation; prediction-based quantities are Chai-1 [5] predictions of both forms with the shared ligand. Every item is scored on all 21 pairs (Methods 2.1.1). <!-- src: tables/spec/derived/zymogen21_meta.json -->

**Ranking criteria.** The 33 main-set metrics and 6 reference rows are ranked by the direction-free AUROC [6, 7] of dead against active (0.5 = no separation), with a 95% bootstrap interval that resamples pairs. "Higher in" is the form in which the metric takes larger values. An AUROC in bold exceeds the best-of-39 threshold [8], the 95th percentile of the best AUROC among 39 unrelated items under random label swaps within pairs (median 0.63, 95th percentile 0.68). <!-- src: tables/spec/derived/zymogen21_meta.json (selection_null_max_p50, selection_null_max_p95) -->

<!-- cols: 0.7,3.8,2.4,1.6,2.6,1.4 -->
| Rank | Item | Group | Mode | AUROC [95% interval] | Higher in |
|---|---|---|---|---|---|
| 1 | *pLDDT* [9] | Reference row | prediction | **0.79 [0.68, 0.90]** | active |
| 2 | *pTM* [9] | Reference row | prediction | **0.75 [0.62, 0.87]** | active |
| 3 | Intra-residue repulsion (Rosetta, site) [10] | Rosetta energy | structure | 0.61 [0.52, 0.72] | dead |
| 4 | Repulsion (Rosetta, site) [10] | Rosetta energy | structure | 0.60 [0.51, 0.72] | dead |
| 5 | *Crystallographic resolution* | Reference row | structure | 0.58 [0.50, 0.72] | dead |
| 6 | Fraction buried | Geometry | structure | 0.57 [0.50, 0.69] | dead |
| 7 | Attraction (Rosetta, site) [10] | Rosetta energy | structure | 0.56 [0.51, 0.64] | active |
| 8 | lk-ball solvation (Rosetta, site) [10] | Rosetta energy | structure | 0.56 [0.50, 0.66] | dead |
| 9 | Ramachandran (Rosetta, site) [10] | Rosetta energy | structure | 0.56 [0.51, 0.63] | dead |
| 10 | *Sequence length* | Reference row | structure | 0.56 [0.50, 0.65] | dead |
| 11 | Relative SASA, mean | Geometry | structure | 0.55 [0.50, 0.66] | active |
| 12 | Total SASA | Geometry | structure | 0.55 [0.50, 0.67] | active |
| 13 | Rotamer, Dunbrack (Rosetta, site) [10] | Rosetta energy | structure | 0.55 [0.50, 0.66] | dead |
| 14 | Pairwise distance, max | Geometry | structure | 0.54 [0.50, 0.64] | dead |
| 15 | ipTM (Chai-1) [5, 11] | Interface confidence | prediction | 0.54 [0.50, 0.61] | active |
| 16 | pKa, range (PROPKA) [12, 13] | pKa | structure | 0.54 [0.50, 0.69] | dead |
| 17 | Polar contacts | Geometry | structure | 0.54 [0.50, 0.59] | dead |
| 18 | Ligand clearance [14] | Active-site accuracy | prediction | 0.54 [0.50, 0.65] | dead |
| 19 | Net van der Waals (Rosetta, site) [10] | Rosetta energy | structure | 0.54 [0.50, 0.61] | active |
| 20 | Relative SASA, max | Geometry | structure | 0.53 [0.50, 0.65] | active |
| 21 | Radius of gyration | Geometry | structure | 0.53 [0.50, 0.64] | dead |
| 22 | AME RMSD [14] | Active-site accuracy | prediction | 0.53 [0.50, 0.66] | active |
| 23 | Pairwise distance, mean | Geometry | structure | 0.53 [0.50, 0.64] | dead |
| 24 | Solvation (Rosetta, site) [10] | Rosetta energy | structure | 0.53 [0.50, 0.60] | dead |
| 25 | Omega torsion (Rosetta, site) [10] | Rosetta energy | structure | 0.53 [0.50, 0.63] | dead |
| 26 | pKa, min (PROPKA) [12, 13] | pKa | structure | 0.52 [0.50, 0.65] | active |
| 27 | Amino-acid propensity (Rosetta, site) [10] | Rosetta energy | structure | 0.52 [0.50, 0.59] | active |
| 28 | Electrostatics (Rosetta, site) [10] | Rosetta energy | structure | 0.52 [0.50, 0.58] | active |
| 29 | pKa, max (PROPKA) [12, 13] | pKa | structure | 0.52 [0.50, 0.67] | dead |
| 30 | H-bond, backbone to side chain (Rosetta, site) [10] | Rosetta energy | structure | 0.52 [0.50, 0.58] | dead |

**Table 3. Separation of real dead from active enzymes on the 21-pair evaluation set (top 30 of 39 ranked items).** The 39 items are the 33 main-set metrics and the 6 reference rows (italic), ranked by the direction-free AUROC of dead against active (floor 0.5) over 21 pairs from 21 proteins; every row has n = 21 pairs. Intervals are 95% bootstrap intervals that resample pairs. "Higher in" is the form in which the metric takes larger values. An AUROC in bold exceeds the best-of-39 threshold, the 95th percentile of the best AUROC among 39 unrelated metrics in label-swap simulations (median 0.63, 95th percentile 0.68; defined in the Methods; it is a reference level, not a confidence interval or a p-value). The nine lowest-ranked items (AUROC 0.50 to 0.52) and all 158 metrics scored on these pairs are in Table S17c. Source: `tables/main/T3_dead_vs_active.csv`.

The wider pair sets and the ranking of all scored metrics are in Tables S17, S17c and S18.

### 3.1.2 Plated designs

**Dataset.** 192 designs from a deposited metallohydrolase design campaign [15]: 16 have a reported kcat/KM (*reported active*) and 176 have *no reported activity*. The comparison is reported active against no reported activity; the 176 were not reported and are never called inactive. The designs lie in 136 backbone clusters, the 16 reported active designs in 8 of them (10 of the 16 in two clusters). Structure-space metrics are computed on the designs as deposited and prediction-based quantities on Chai-1 [5] predictions with the design's transition-state-analogue ligand and zinc. Every item is scored on all 192 designs (Methods 2.1.2). <!-- src: data/systems/p6_d3_v1/systems.csv; tables/spec/derived/plates192_meta.json; results/P6_m3/enrichment_summary.json -->

**Ranking criteria.** The 36 items are 29 structure-space and 2 prediction-based main-set metrics and 5 reference rows (tyrosine fraction, net charge, sequence length, pLDDT, pTM). They are ranked by the direction-free AUROC [6, 7] of reported active against no reported activity (0.5 = no separation), with a 95% bootstrap interval that resamples the 136 backbone clusters [16]. "Higher in" is the group in which the metric takes larger values. An AUROC in bold exceeds the best-of-36 threshold [8], the 95th percentile of the best AUROC among 36 items when the activity labels are permuted among designs (median 0.66, 95th percentile 0.73); the permutation treats designs as exchangeable, which understates the chance range when the actives are clumped in few clusters. AME is measured on the plates against each design's own model, a different metric from AME against a deposited structure, and is not ranked here. <!-- src: tables/spec/derived/plates192_meta.json -->

<!-- cols: 0.7,3.3,2.2,1.5,2.5,2.3 -->
| Rank | Item | Group | Mode | AUROC [95% interval] | Higher in |
|---|---|---|---|---|---|
| 1 | Intra-residue repulsion (Rosetta, site) [10] | Rosetta energy | structure | **0.80 [0.64, 0.89]** | no reported activity |
| 2 | Repulsion (Rosetta, site) [10] | Rosetta energy | structure | **0.78 [0.57, 0.92]** | no reported activity |
| 3 | *Tyrosine fraction* | Reference row | structure | **0.75 [0.55, 0.86]** | active |
| 4 | *pLDDT* [9] | Reference row | prediction | 0.73 [0.53, 0.86] | active |
| 5 | *pTM* [9] | Reference row | prediction | 0.72 [0.54, 0.85] | active |
| 6 | Site total (Rosetta) [10] | Rosetta energy | structure | 0.71 [0.52, 0.82] | no reported activity |
| 7 | Rotamer, Dunbrack (Rosetta, site) [10] | Rosetta energy | structure | 0.71 [0.58, 0.88] | no reported activity |
| 8 | Per-chain pTM minimum (Chai-1) [5, 9] | Interface confidence | prediction | 0.70 [0.54, 0.83] | active |
| 9 | ipTM (Chai-1) [5, 11] | Interface confidence | prediction | 0.70 [0.52, 0.84] | active |
| 10 | *Sequence length* | Reference row | structure | 0.68 [0.51, 0.86] | no reported activity |
| 11 | Worst residue (Rosetta, site) [10] | Rosetta energy | structure | 0.68 [0.52, 0.78] | no reported activity |
| 12 | Attraction (Rosetta, site) [10] | Rosetta energy | structure | 0.67 [0.57, 0.82] | active |
| 13 | lk-ball solvation (Rosetta, site) [10] | Rosetta energy | structure | 0.66 [0.54, 0.82] | active |
| 14 | Total SASA | Geometry | structure | 0.65 [0.54, 0.89] | active |
| 15 | Relative SASA, mean | Geometry | structure | 0.65 [0.53, 0.89] | active |
| 16 | Electrostatics (Rosetta, site) [10] | Rosetta energy | structure | 0.64 [0.51, 0.79] | no reported activity |
| 17 | Pairwise distance, max | Geometry | structure | 0.64 [0.51, 0.77] | active |
| 18 | Relative SASA, max | Geometry | structure | 0.62 [0.52, 0.84] | active |
| 19 | Pairwise distance, mean | Geometry | structure | 0.61 [0.51, 0.77] | active |
| 20 | Radius of gyration | Geometry | structure | 0.61 [0.51, 0.77] | active |
| 21 | H-bond, side chain (Rosetta, site) [10] | Rosetta energy | structure | 0.61 [0.51, 0.73] | no reported activity |
| 22 | Solvation (Rosetta, site) [10] | Rosetta energy | structure | 0.60 [0.51, 0.71] | no reported activity |
| 23 | Amino-acid propensity (Rosetta, site) [10] | Rosetta energy | structure | 0.60 [0.51, 0.73] | active |
| 24 | Polar contacts | Geometry | structure | 0.59 [0.50, 0.74] | active |
| 25 | Omega torsion (Rosetta, site) [10] | Rosetta energy | structure | 0.58 [0.50, 0.81] | active |
| 26 | *Net charge* | Reference row | structure | 0.56 [0.51, 0.83] | active |
| 27 | pKa, max (PROPKA) [12, 13] | pKa | structure | 0.56 [0.50, 0.78] | no reported activity |
| 28 | pKa, range (PROPKA) [12, 13] | pKa | structure | 0.55 [0.50, 0.77] | no reported activity |
| 29 | Net van der Waals (Rosetta, site) [10] | Rosetta energy | structure | 0.54 [0.50, 0.80] | active |
| 30 | Fraction buried | Geometry | structure | 0.53 [0.50, 0.70] | no reported activity |

**Table 4. Separation of reported active from no-reported-activity designs on the 192-design evaluation set (top 30 of 36 ranked items).** The 36 items are 29 structure-space and 2 prediction-based main-set metrics and 5 reference rows (italic), ranked by the direction-free AUROC (floor 0.5) of the 16 reported active designs against the 176 with no reported activity; every row has n = 192 designs (16 active). Intervals are 95% bootstrap intervals that resample the 136 backbone clusters. "Higher in" is the group in which the metric takes larger values: "active" (reported active) or "no reported activity" (the 176 designs for which no activity was reported, which are not known to be inactive). An AUROC in bold exceeds the best-of-36 threshold, the 95th percentile of the best AUROC among 36 unrelated items when the activity labels are permuted among designs (median 0.66, 95th percentile 0.73; a reference level, not a confidence interval or a p-value). Items 31 to 36 and all 128 metrics scored on the designs are in Table S17d. Source: `tables/main/T4_plated_designs_auroc.csv`.

The ranking of all metrics scored on the designs is in Table S17d.

---

## 3.2 Substrate discrimination test

**Experiment.** Each enzyme is predicted with Chai-1 [5] in four conditions that differ only in the ligand supplied: its cognate ligand, a wrong ligand of the same enzyme class, a wrong ligand of a different class, and a decoy ligand taken from an unrelated structure. Each prediction-based quantity is ranked by how well it separates the cognate prediction from a wrong-ligand prediction of the same enzyme (Methods 2.2).

**Dataset.** 55 natural enzymes of M-CSA [3], of the 59 in the experiment: on these, every scored quantity has a defined value in all four conditions and every supplied ligand was present in the prediction (four enzymes are excluded because a heme-type ligand could not be built into a chemical structure and the predictor dropped it). One n, 55 enzymes, applies to every row (Methods 2.2). <!-- src: tables/spec/derived/swap55_meta.json; results/P5_1B/s_axis_dropped_cells.csv -->

**Ranking criteria.** Chai-1 returns five models per prediction, and each score is summarised over them as a mean, a maximum or a spread (standard deviation across models), and for the AME RMSD also as a minimum, so one metric appears in several rows. The 30 scored quantities are the four prediction-based main-set metrics (ipTM, per-chain pTM minimum, ligand clearance, AME RMSD), whole-prediction confidence scores (including the reference rows pLDDT and pTM), the AME pass bit and four bookkeeping counters. Each is ranked by the mean of three direction-free AUROCs [6, 7], one per kind of wrong ligand (same class, different class, decoy), each with a 95% interval that resamples enzymes. "Higher in" is the condition in which the quantity takes larger values. A mean in bold exceeds the best-of-30 threshold [8], the 95th percentile of the best AUROC among 30 quantities when the four ligand conditions are permuted within each enzyme (median 0.56, 95th percentile 0.61). <!-- src: tables/main/T5_substrate_swap.csv; src/mrx/metrics/m3.py -->

<!-- cols: 0.6,2.6,1.6,2.4,2.0,2.0,2.0,0.9,1.3 -->
| Rank | Quantity | Summary over the five models | Group | Same class | Different class | Decoy | Mean | Higher in |
|---|---|---|---|---|---|---|---|---|
| 1 | ipTM [5, 11] | mean | Interface confidence (main set) | 0.69 [0.60, 0.78] | 0.75 [0.66, 0.84] | 0.65 [0.55, 0.76] | **0.70** | cognate |
| 2 | ipTM [5, 11] | maximum | Interface confidence (main set) | 0.68 [0.59, 0.77] | 0.74 [0.65, 0.83] | 0.65 [0.54, 0.74] | **0.69** | cognate |
| 3 | ipTM [5, 11] | spread (SD) | Interface confidence (main set) | 0.70 [0.60, 0.79] | 0.69 [0.60, 0.77] | 0.67 [0.59, 0.75] | **0.69** | wrong ligand |
| 4 | pTM [9] | spread (SD) | Whole-prediction confidence | 0.62 [0.55, 0.70] | 0.64 [0.58, 0.71] | 0.64 [0.57, 0.71] | **0.64** | wrong ligand |
| 5 | Ligand clearance [14] | best model | Active-site accuracy (main set) | 0.61 [0.52, 0.69] | 0.65 [0.57, 0.74] | 0.62 [0.53, 0.71] | **0.63** | wrong ligand |
| 6 | *pTM* [9] | mean | Reference row | 0.60 [0.56, 0.66] | 0.63 [0.58, 0.69] | 0.64 [0.58, 0.70] | **0.62** | cognate |
| 7 | pTM [9] | maximum | Whole-prediction confidence | 0.60 [0.56, 0.66] | 0.63 [0.58, 0.69] | 0.63 [0.58, 0.70] | **0.62** | cognate |
| 8 | Per-chain pTM minimum [5, 9] | spread (SD) | Interface confidence (main set) | 0.58 [0.51, 0.68] | 0.58 [0.51, 0.68] | 0.69 [0.59, 0.79] | **0.62** | wrong ligand |
| 9 | AME RMSD [14] | spread (SD) | Active-site accuracy (main set) | 0.55 [0.51, 0.60] | 0.56 [0.51, 0.62] | 0.57 [0.52, 0.63] | 0.56 | wrong ligand |
| 10 | Per-chain pTM minimum [5, 9] | mean | Interface confidence (main set) | 0.58 [0.51, 0.67] | 0.60 [0.51, 0.71] | 0.50 [0.50, 0.62] | 0.56 | cognate |
| 11 | Per-chain pTM minimum [5, 9] | maximum | Interface confidence (main set) | 0.58 [0.51, 0.67] | 0.59 [0.51, 0.71] | 0.50 [0.50, 0.62] | 0.56 | cognate |
| 12 | AME RMSD [14] | maximum | Active-site accuracy (main set) | 0.53 [0.50, 0.57] | 0.54 [0.51, 0.58] | 0.54 [0.51, 0.59] | 0.54 | wrong ligand |
| 13 | AME RMSD [14] | minimum | Active-site accuracy (main set) | 0.53 [0.50, 0.56] | 0.54 [0.51, 0.57] | 0.52 [0.50, 0.57] | 0.53 | wrong ligand |
| 14 | AME RMSD, no symmetry resolution [14] | minimum | Active-site accuracy (main set) | 0.52 [0.50, 0.56] | 0.54 [0.51, 0.57] | 0.53 [0.50, 0.57] | 0.53 | wrong ligand |
| 15 | AME RMSD [14] | mean | Active-site accuracy (main set) | 0.53 [0.50, 0.56] | 0.53 [0.51, 0.57] | 0.52 [0.50, 0.57] | 0.53 | wrong ligand |
| 16 | pLDDT [9] | spread (SD) | Whole-prediction confidence | 0.51 [0.50, 0.55] | 0.52 [0.50, 0.57] | 0.54 [0.50, 0.60] | 0.52 | mixed |
| 17 | Per-chain pTM of the protein [5, 9] | mean | Whole-prediction confidence | 0.52 [0.50, 0.54] | 0.52 [0.50, 0.54] | 0.53 [0.51, 0.56] | 0.52 | cognate |
| 18 | Per-chain pTM of the protein [5, 9] | maximum | Whole-prediction confidence | 0.52 [0.50, 0.54] | 0.52 [0.50, 0.55] | 0.53 [0.51, 0.55] | 0.52 | cognate |
| 19 | pLDDT [9] | best model | Whole-prediction confidence | 0.52 [0.50, 0.54] | 0.53 [0.51, 0.55] | 0.51 [0.50, 0.54] | 0.52 | cognate |
| 20 | *pLDDT* [9] | mean | Reference row | 0.52 [0.50, 0.54] | 0.53 [0.51, 0.55] | 0.51 [0.50, 0.54] | 0.52 | cognate |
| 21 | Per-chain pTM of the protein [5, 9] | spread (SD) | Whole-prediction confidence | 0.50 [0.50, 0.55] | 0.52 [0.50, 0.56] | 0.50 [0.50, 0.55] | 0.51 | wrong ligand |
| 22 | Symmetry swaps (count) | single value | Bookkeeping counter | 0.51 [0.50, 0.54] | 0.51 [0.50, 0.53] | 0.50 [0.50, 0.52] | 0.51 | cognate |
| 23 | pLDDT [9] | lowest residue | Whole-prediction confidence | 0.50 [0.50, 0.52] | 0.50 [0.50, 0.53] | 0.50 [0.50, 0.53] | 0.50 | cognate |
| 24 | AME pass bit [14] | single value | Active-site accuracy (pass bit) | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.53] | 0.50 [0.50, 0.53] | 0.50 | mixed |
| 25 | Backbone atoms aligned (count) | single value | Bookkeeping counter | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 | mixed |
| 26 | Catalytic atoms (count) | single value | Bookkeeping counter | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 | mixed |
| 27 | Models predicted (count) | single value | Bookkeeping counter | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 | mixed |
| 28 | Inter-chain clash flag [5] | maximum | Whole-prediction confidence | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 | mixed |
| 29 | Inter-chain clash flag [5] | mean | Whole-prediction confidence | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 | mixed |
| 30 | Inter-chain clash flag [5] | spread (SD) | Whole-prediction confidence | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 [0.50, 0.50] | 0.50 | mixed |

**Table 5. The substrate swap on the 55-enzyme evaluation set, 30 scored prediction-based quantities ranked by AUROC.** Direction-free AUROC (floor 0.5) of the cognate prediction against a wrong-ligand prediction of the same enzyme, in three columns by kind of wrong ligand, with 95% intervals that resample enzymes; the value of an enzyme in a condition is the mean over seeds 101, 202 and 303. Rows are ranked by the mean of the three AUROCs; a mean in bold exceeds the best-of-30 threshold (median 0.56, 95th percentile 0.61; permutation of the four ligand conditions within each enzyme, defined in the Methods; a reference level, not a confidence interval or a p-value). Chai-1 predicts five models for every prediction, and each score is summarised over them (mean, maximum, spread as the standard deviation across models, and for the AME RMSD also the minimum), so one metric appears in several rows, one per summary. Reference rows are in italic. Source: `tables/main/T5_substrate_swap.csv`.

The earlier analysis of all 59 natural enzymes, the ligand-size strata and the 30 de novo designs are in Tables S14 and S14b.

---

## 3.3 Activity ranking test

**Experiment.** Metrics are scored on real proteins whose activity was measured, and each metric is ranked by the rank correlation between its value and the measured activity (Methods 2.3). Two datasets are used, each with its own table.

### 3.3.1 BglB variants

**Dataset.** BglB, a β-glucosidase from *Paenibacillus polymyxa*, with single-point variants characterised by the D2DCure consortium [17] (data retrieved from d2dcure.com on 2026-08-06): 655 variants at 207 positions, of which the **432 variants at 175 positions that are folded (expressed and not destabilised) and have kinetics** are the evaluation set. The measured value is the *impairment*, the log10 of the loss of kcat/KM relative to the wild type (larger = more impaired). Each variant is built in the computer on the crystal structure of the wild type (RCSB PDB entry 2JIE [1, 2], which carries a covalent glucosyl intermediate) and structure-space metrics are computed over the two catalytic glutamates (Glu167 and Glu356, from the UniProt [4] active-site features) before and after the substitution; prediction-based metrics are computed on Chai-1 [5] predictions of the variant with the assay substrate (pNPG) (Methods 2.3.1). <!-- src: results/D4_bglb/main_meta.json; tables/spec/derived/bglb432_meta.json; data/raw/d4_bglb_2jie/PROVENANCE.md -->

**Ranking criteria.** The 41 items are the 28 structure-space main-set metrics that BglB defines (the omega term does not change under a side-chain substitution on a fixed backbone), the 4 prediction-based main-set metrics, 4 reference rows (tyrosine fraction, net charge, pLDDT, pTM) and 5 baselines declared before any metric was joined to a label: the distance from the mutated residue to the nearest catalytic residue, the burial of the mutated residue, the BLOSUM62 score of the substitution, the change in side-chain volume and the Rosetta score that comes with the BglB data (248 of the 432 variants). Each is ranked by the Spearman rank correlation ρ [18] with the measured impairment, with a 95% bootstrap interval that resamples the 175 positions [16]. For a metric the score is the size of its change (the absolute difference between the variant and the unsubstituted protein), with the direction fixed in advance (larger in more impaired variants); for a baseline it is the baseline itself, pointed so that a larger value means more impaired. A ρ in bold exceeds the best-of-41 threshold [8], the 95th percentile of the best ρ among 41 items when the measured impairments are permuted among whole positions (median 0.24, 95th percentile 0.32). The last column says whether the item beats the distance baseline: the interval of the difference between its ρ and the baseline's, on the same bootstrap draws, lies above 0. <!-- src: tables/spec/derived/bglb432_meta.json; tables/main/T6_bglb_variants.csv -->

<!-- cols: 0.7,3.7,2.3,1.5,2.6,1.6 -->
| Rank | Item | Group | Mode | Spearman ρ [95% interval] | Beats the distance baseline |
|---|---|---|---|---|---|
| 1 | pKa, range (PROPKA) [12, 13] | pKa | structure | **0.48 [0.35, 0.59]** | no |
| 2 | pKa, min (PROPKA) [12, 13] | pKa | structure | **0.46 [0.32, 0.57]** | no |
| 3 | pKa shift, max absolute (PROPKA) [12, 13] | pKa | structure | **0.46 [0.32, 0.58]** | no |
| 4 | pKa, max (PROPKA) [12, 13] | pKa | structure | **0.46 [0.32, 0.58]** | no |
| 5 | *Distance to the catalytic residues* | Reference row | – | **0.46 [0.32, 0.57]** | – |
| 6 | Intra-residue repulsion (Rosetta, site) [10] | Rosetta energy | structure | **0.45 [0.30, 0.57]** | no |
| 7 | Relative SASA, mean | Geometry | structure | **0.45 [0.32, 0.57]** | no |
| 8 | pKa shift, mean (PROPKA) [12, 13] | pKa | structure | **0.45 [0.31, 0.57]** | no |
| 9 | pKa, mean (PROPKA) [12, 13] | pKa | structure | **0.45 [0.31, 0.57]** | no |
| 10 | Total SASA | Geometry | structure | **0.45 [0.31, 0.57]** | no |
| 11 | Repulsion (Rosetta, site) [10] | Rosetta energy | structure | **0.45 [0.31, 0.57]** | no |
| 12 | Pairwise distance, max | Geometry | structure | **0.45 [0.30, 0.56]** | no |
| 13 | Attraction (Rosetta, site) [10] | Rosetta energy | structure | **0.44 [0.30, 0.56]** | no |
| 14 | Rotamer, Dunbrack (Rosetta, site) [10] | Rosetta energy | structure | **0.44 [0.29, 0.56]** | no |
| 15 | lk-ball solvation (Rosetta, site) [10] | Rosetta energy | structure | **0.44 [0.31, 0.54]** | no |
| 16 | Radius of gyration | Geometry | structure | **0.43 [0.28, 0.56]** | no |
| 17 | Net van der Waals (Rosetta, site) [10] | Rosetta energy | structure | **0.43 [0.28, 0.55]** | no |
| 18 | Relative SASA, max | Geometry | structure | **0.43 [0.29, 0.54]** | no |
| 19 | Pairwise distance, mean | Geometry | structure | **0.43 [0.28, 0.55]** | no |
| 20 | Electrostatics (Rosetta, site) [10] | Rosetta energy | structure | **0.43 [0.28, 0.55]** | no |
| 21 | Site total (Rosetta) [10] | Rosetta energy | structure | **0.42 [0.27, 0.55]** | no |
| 22 | Worst residue (Rosetta, site) [10] | Rosetta energy | structure | **0.42 [0.26, 0.55]** | no |
| 23 | Solvation (Rosetta, site) [10] | Rosetta energy | structure | **0.41 [0.27, 0.54]** | no |
| 24 | H-bond, side chain (Rosetta, site) [10] | Rosetta energy | structure | **0.35 [0.19, 0.49]** | no |
| 25 | *Burial of the mutated residue* | Reference row | – | **0.33 [0.21, 0.43]** | – |
| 26 | ipTM (Chai-1) [5, 11] | Interface confidence | prediction | **0.33 [0.19, 0.45]** | no |
| 27 | Per-chain pTM minimum (Chai-1) [5, 9] | Interface confidence | prediction | 0.28 [0.15, 0.41] | no |
| 28 | *pTM* [9] | Reference row | prediction | 0.26 [0.12, 0.38] | no |
| 29 | *Rosetta score in the BglB data set* | Reference row | – | 0.21 [0.06, 0.35] | – |
| 30 | Fraction buried | Geometry | structure | 0.19 [0.06, 0.30] | no |

**Table 6. BglB variants: top 30 of 41 ranked items on the 432-variant evaluation set.** Spearman rank correlation ρ between each item and the measured impairment of the 432 variants, with a 95% interval that resamples the 175 positions. For a metric the score is the size of its change, for a baseline its own score, with the direction fixed in advance (a larger change in more impaired variants), so a negative ρ would be kept. The 41 items are the 32 main-set metrics that BglB defines, four reference rows and five declared baselines; reference rows and baselines are in italic. A value in bold exceeds the best-of-41 threshold (median 0.24, 95th percentile 0.32; permutation of the measured impairments among whole positions; a reference level, not a confidence interval or a p-value). Structure-space rows have 431 variants with a value, prediction-based rows 432 and the Rosetta score of the BglB data 248. Items 31 to 41, and all 114 quantities analysed, are in Table S20c. Source: `tables/main/T6_bglb_variants.csv`.

The binary comparison of impaired and wild-type-like variants, its sensitivity analyses and the ranking of all quantities are in Tables S20b and S20c.

### 3.3.2 Plated designs

**Dataset.** The 192-design campaign of 3.1.2 [15]. Only the 16 designs with a reported kcat/KM have a measured activity, so the evaluation set is those 16 designs and every row has n = 16; they lie in 8 of the 136 backbone clusters (Methods 2.3.2). The other 176 designs have no reported activity and are not part of this ranking. <!-- src: results/P6/REPORT.md; results/P6_m3/enrichment_summary.json -->

**Ranking criteria.** The 36 items are those of Table 4. Each is ranked by the size of the Spearman correlation ρ [18] between its value on the design as deposited and log10 kcat/KM, with a 90% bootstrap interval over designs. No direction is fixed in advance, so the sign is reported ("higher value means higher or lower activity"), and the last column gives ρ with the sequence length partialled out of both sides. A ρ in bold has an interval that excludes 0, which about 3.6 of the 36 items would show for unrelated metrics. The analysis is descriptive (Methods 2.3.2): no hypothesis test and no chance threshold. <!-- src: tables/main/T7_plated_designs.csv (note column) -->

<!-- cols: 0.7,3.4,2.0,1.4,2.6,1.9,1.6 -->
| Rank | Item | Group | Mode | Spearman ρ [90% interval] | Higher value means | ρ, length partialled out |
|---|---|---|---|---|---|---|
| 1 | Polar contacts | Geometry | structure | **0.67 [0.41, 0.85]** | higher activity | 0.52 |
| 2 | Net van der Waals (Rosetta, site) [10] | Rosetta energy | structure | **−0.63 [−0.88, −0.24]** | lower activity | −0.47 |
| 3 | *pLDDT* [9] | Reference row | prediction | **0.60 [0.24, 0.83]** | higher activity | 0.36 |
| 4 | *Sequence length* | Reference row | structure | **−0.58 [−0.82, −0.23]** | lower activity | – |
| 5 | Solvation (Rosetta, site) [10] | Rosetta energy | structure | **0.57 [0.15, 0.85]** | higher activity | 0.54 |
| 6 | Amino-acid propensity (Rosetta, site) [10] | Rosetta energy | structure | **0.54 [0.08, 0.81]** | higher activity | 0.64 |
| 7 | *Net charge* | Reference row | structure | 0.46 [−0.02, 0.80] | higher activity | 0.22 |
| 8 | Pairwise distance, mean | Geometry | structure | −0.43 [−0.71, 0.02] | lower activity | −0.29 |
| 9 | Site total (Rosetta) [10] | Rosetta energy | structure | −0.42 [−0.69, 0.01] | lower activity | −0.37 |
| 10 | Radius of gyration | Geometry | structure | −0.41 [−0.69, 0.03] | lower activity | −0.29 |
| 11 | H-bond, side chain (Rosetta, site) [10] | Rosetta energy | structure | −0.40 [−0.74, 0.05] | lower activity | −0.14 |
| 12 | Ramachandran (Rosetta, site) [10] | Rosetta energy | structure | −0.38 [−0.82, 0.15] | lower activity | −0.09 |
| 13 | Repulsion (Rosetta, site) [10] | Rosetta energy | structure | −0.33 [−0.73, 0.17] | lower activity | 0.21 |
| 14 | pKa, mean (PROPKA) [12, 13] | pKa | structure | −0.30 [−0.57, 0.09] | lower activity | 0.09 |
| 15 | pKa shift, mean (PROPKA) [12, 13] | pKa | structure | −0.30 [−0.56, 0.09] | lower activity | 0.09 |
| 16 | Relative SASA, mean | Geometry | structure | −0.25 [−0.76, 0.31] | lower activity | −0.35 |
| 17 | Total SASA | Geometry | structure | −0.25 [−0.76, 0.30] | lower activity | −0.35 |
| 18 | Relative SASA, max | Geometry | structure | −0.25 [−0.76, 0.28] | lower activity | −0.34 |
| 19 | Attraction (Rosetta, site) [10] | Rosetta energy | structure | −0.25 [−0.66, 0.25] | lower activity | −0.20 |
| 20 | Pairwise distance, max | Geometry | structure | 0.23 [−0.26, 0.64] | higher activity | 0.26 |
| 21 | Intra-residue repulsion (Rosetta, site) [10] | Rosetta energy | structure | −0.23 [−0.65, 0.30] | lower activity | −0.46 |
| 22 | lk-ball solvation (Rosetta, site) [10] | Rosetta energy | structure | −0.21 [−0.53, 0.19] | lower activity | 0.08 |
| 23 | Electrostatics (Rosetta, site) [10] | Rosetta energy | structure | −0.19 [−0.58, 0.25] | lower activity | −0.61 |
| 24 | Per-chain pTM minimum (Chai-1) [5, 9] | Interface confidence | prediction | 0.18 [−0.35, 0.66] | higher activity | −0.00 |
| 25 | Rotamer, Dunbrack (Rosetta, site) [10] | Rosetta energy | structure | 0.18 [−0.31, 0.57] | higher activity | 0.11 |
| 26 | H-bond, backbone to side chain (Rosetta, site) [10] | Rosetta energy | structure | 0.17 [−0.21, 0.52] | higher activity | 0.32 |
| 27 | pKa, max (PROPKA) [12, 13] | pKa | structure | −0.16 [−0.49, 0.26] | lower activity | 0.16 |
| 28 | *pTM* [9] | Reference row | prediction | −0.15 [−0.64, 0.41] | lower activity | −0.26 |
| 29 | *Tyrosine fraction* | Reference row | structure | −0.14 [−0.68, 0.40] | lower activity | 0.00 |
| 30 | pKa, range (PROPKA) [12, 13] | pKa | structure | −0.13 [−0.53, 0.31] | lower activity | −0.07 |

**Table 7. Plated designs: top 30 of 36 ranked items on the 16 designs that have a reported kcat/KM.** Spearman rank correlation ρ between each metric (native value on the design) and log10 kcat/KM, with a 90% interval that resamples designs; items are ranked by the size of ρ because no direction is fixed in advance. A value in bold has an interval that excludes 0 (about 3.6 of the 36 items would show this for unrelated metrics). The last column gives ρ with the sequence length partialled out of both sides. The 36 items are 29 structure-space and 2 prediction-based main-set metrics and 5 reference rows (italic). Descriptive only: no hypothesis test and no chance threshold. Items 31 to 36, and all 106 metrics with a correlation, are in Table S22c; the hits-per-plate analysis of the 192 designs is in Table S22d. Source: `tables/main/T7_plated_designs.csv`.

The ranking of all metrics with a correlation and the hits-per-plate analysis of the 192 designs are in Tables S22c and S22d.

---

## 3.4 Detection ability test

**Experiment.** Each metric is ranked by whether it changes more under a lesion at a catalytic residue than under the identical lesion at a matched non-catalytic control position of the same protein (Methods 2.4). Two perturbation axes are tested, each with its own datasets and table.

### 3.4.1 Axis C: the chemistry ladder

**Experiment.** One catalytic residue is replaced in four steps of increasing change in side-chain volume (isosteric 15 Å³, non-isosteric 36 Å³, to Ala 53 Å³, to Gly 81 Å³), in the crystal structure by a rotamer-space edit and repack, or in the sequence of the re-predicted complex with Chai-1 [5]; the control makes the identical substitution at a matched buried non-catalytic position of the same protein.

**Dataset.** For the 29 structure-space main-set metrics: the 143 M-CSA enzymes [3] (77 enzyme sub-subclasses; packing-matched, count-gated controls) pooled with the 52 enzymes of the 53-enzyme pilot set that are not in it (active sites from UniProt [4] and M-CSA; controls matched on residue type and burial only; the one pilot enzyme that shares a PDB entry with the main set is counted once), 195 enzymes in all. For the four prediction-based main-set metrics and the two reference rows (pLDDT and pTM): the natural arm of the re-predicted ladder, the 59 natural enzymes of the substrate-swap set with 286 catalytic/control pairs. The 30 de novo designs and the 15 designed systems of the ladder, whose control is constructed, are not pooled (Tables S28 and S29) (Methods 2.4.1). <!-- src: tables/spec/derived/axis_ranking_meta.json; data/systems/p2_d0_v2/systems.csv; data/systems/p1_d0_v1/systems.csv; results/P5/caxis_design.csv -->

**Ranking criteria.** The 35 items are the 29 structure-space and 4 prediction-based main-set metrics and the 2 reference rows (italic). The rank statistic R is the probability that a metric changes more at the catalytic lesion than at the matched control of the same protein (0.5 = no specificity; above 0.5, more change at the catalytic lesion). The change of a metric is the absolute difference between the perturbed and the unperturbed structure (or prediction), a tie counts one half, and proteins in which neither arm moves are dropped. A step counts toward a structure-space metric only if the metric responds to the lesion (the interval of its median change excludes zero) and the control response is above the metric's own noise; a step that is not counted is in parentheses, and "–" is a step with fewer than five informative proteins. The mean R over the counted steps ("Steps counted": counted of the steps with a value) has a 95% bootstrap interval that resamples enzyme sub-subclasses (systems for the predictor). Rows are grouped by the lesion at which the metric is first detected (the smallest step at which it responds; "Never" if at none) and ranked by mean R within each group; a metric with no counted step has no mean and closes its group. A mean in bold exceeds the best-of-33 threshold [8], the 95th percentile of the best R among 33 items when the catalytic and control labels are swapped within each protein (median 0.57, 95th percentile 0.62). The distance-matched R (prediction-based metrics only) is computed on the pairs whose control lies at the same distance from the ligand as the catalytic residue (within 2 Å and within 0.10 in relative solvent-accessible area), pooled over the four steps (68 to 69 pairs in 21 to 22 systems); the original control of the predictor sat a median 13.4 Å from the ligand, the catalytic residue 3.1 Å. "Specific from" is the smallest step at which a structure-space metric is specific under the specificity ratio rule (it responds, the ratio is above 1, the control response is above the noise and both arms changed equal numbers of residues); "never" means no step of the four, and "–" that the rule does not exist for the predictor. <!-- src: tables/supp/S26_axis_C_all_metrics_ranked.csv; tables/spec/derived/axis_ranking_meta.json; results/P5_1B/REPORT.md -->

<!-- cols: 1.3,0.6,2.6,1.6,1.2,2.8,2.2,1.1,2.2,1.0 -->
| Detected from | Rank in group | Item | Group | Mode | R at isosteric / non-isosteric / Ala / Gly | Mean R [95% interval] | Steps counted | R, distance-matched [95% interval] | Specific from |
|---|---|---|---|---|---|---|---|---|---|
| Isosteric | 1 | Per-chain pTM minimum (Chai-1) [5, 9] | Interface confidence | prediction | 0.81 / 0.73 / 0.75 / 0.72 | **0.75 [0.68, 0.82]** | 4 of 4 | 0.59 [0.42, 0.76] | – |
| Isosteric | 2 | pKa, range (PROPKA) [12, 13] | pKa | structure | 0.70 / 0.67 / – / – | **0.68 [0.58, 0.78]** | 2 of 2 | – | never |
| Isosteric | 3 | ipTM (Chai-1) [5, 11] | Interface confidence | prediction | 0.71 / 0.71 / 0.69 / 0.58 | **0.67 [0.60, 0.75]** | 4 of 4 | 0.35 [0.24, 0.50] | – |
| Isosteric | 4 | Solvation (Rosetta, site) [10] | Rosetta energy | structure | 0.59 / 0.73 / 0.60 / 0.62 | **0.63 [0.57, 0.70]** | 4 of 4 | – | non-iso |
| Isosteric | 5 | Relative SASA, mean | Geometry | structure | 0.48 / 0.55 / 0.73 / 0.69 | 0.61 [0.56, 0.67] | 4 of 4 | – | non-iso |
| Isosteric | 6 | pKa, min (PROPKA) [12, 13] | pKa | structure | 0.54 / 0.67 / – / – | 0.61 [0.53, 0.67] | 2 of 2 | – | never |
| Isosteric | 7 | Repulsion (Rosetta, site) [10] | Rosetta energy | structure | 0.48 / 0.55 / 0.64 / 0.62 | 0.57 [0.52, 0.62] | 4 of 4 | – | Ala |
| Isosteric | 8 | pKa shift, mean (PROPKA) [12, 13] | pKa | structure | 0.46 / 0.67 / – / – | 0.56 [0.47, 0.66] | 2 of 2 | – | never |
| Isosteric | 9 | *pTM* [9] | Reference row | prediction | 0.60 / 0.48 / 0.60 / 0.58 | 0.56 [0.49, 0.64] | 4 of 4 | 0.45 [0.30, 0.60] | – |
| Isosteric | 10 | Relative SASA, max | Geometry | structure | 0.49 / (0.50) / 0.56 / 0.55 | 0.53 [0.48, 0.59] | 3 of 4 | – | Gly |
| Isosteric | 11 | Attraction (Rosetta, site) [10] | Rosetta energy | structure | 0.53 / 0.58 / 0.55 / 0.46 | 0.53 [0.46, 0.60] | 4 of 4 | – | Ala |
| Isosteric | 12 | *pLDDT* [9] | Reference row | prediction | 0.62 / 0.37 / 0.55 / 0.58 | 0.53 [0.46, 0.60] | 4 of 4 | 0.49 [0.34, 0.63] | – |
| Isosteric | 13 | Ramachandran (Rosetta, site) [10] | Rosetta energy | structure | 0.43 / 0.55 / 0.55 / 0.56 | 0.52 [0.47, 0.59] | 4 of 4 | – | Gly |
| Isosteric | 14 | Intra-residue repulsion (Rosetta, site) [10] | Rosetta energy | structure | 0.48 / 0.59 / 0.48 / 0.52 | 0.52 [0.47, 0.57] | 4 of 4 | – | never |
| Isosteric | 15 | Rotamer, Dunbrack (Rosetta, site) [10] | Rosetta energy | structure | 0.45 / 0.47 / 0.58 / 0.58 | 0.52 [0.46, 0.57] | 4 of 4 | – | Ala |
| Isosteric | 16 | Radius of gyration | Geometry | structure | 0.42 / 0.48 / 0.62 / – | 0.51 [0.45, 0.57] | 3 of 3 | – | Ala |
| Isosteric | 17 | Amino-acid propensity (Rosetta, site) [10] | Rosetta energy | structure | 0.45 / (0.57) / 0.52 / 0.53 | 0.50 [0.45, 0.55] | 3 of 4 | – | never |
| Isosteric | 18 | pKa, max (PROPKA) [12, 13] | pKa | structure | 0.43 / 0.56 / – / – | 0.49 [0.39, 0.61] | 2 of 2 | – | never |
| Isosteric | 19 | Worst residue (Rosetta, site) [10] | Rosetta energy | structure | 0.45 / 0.46 / 0.54 / (0.43) | 0.48 [0.44, 0.53] | 3 of 4 | – | never |
| Isosteric | 20 | Net van der Waals (Rosetta, site) [10] | Rosetta energy | structure | 0.45 / 0.55 / 0.47 / 0.39 | 0.46 [0.39, 0.52] | 4 of 4 | – | never |
| Isosteric | 21 | H-bond, side chain (Rosetta, site) [10] | Rosetta energy | structure | 0.47 / 0.42 / 0.43 / 0.42 | 0.43 [0.35, 0.52] | 4 of 4 | – | never |
| Isosteric | 22 | Site total (Rosetta) [10] | Rosetta energy | structure | 0.41 / 0.58 / 0.41 / 0.29 | 0.42 [0.37, 0.47] | 4 of 4 | – | never |
| Isosteric | 23 | Pairwise distance, mean | Geometry | structure | 0.43 / 0.49 / 0.32 / – | 0.41 [0.34, 0.50] | 3 of 3 | – | non-iso |
| Isosteric | 24 | pKa, mean (PROPKA) [12, 13] | pKa | structure | 0.40 / (0.47) / – / – | 0.40 [0.28, 0.54] | 1 of 2 | – | never |
| Isosteric | 25 | H-bond, backbone to side chain (Rosetta, site) [10] | Rosetta energy | structure | 0.26 / 0.29 / 0.31 / 0.29 | 0.29 [0.19, 0.39] | 4 of 4 | – | never |
| Isosteric | 26 | Electrostatics (Rosetta, site) [10] | Rosetta energy | structure | 0.26 / 0.20 / 0.24 / 0.26 | 0.24 [0.18, 0.30] | 4 of 4 | – | never |
| Isosteric | – | Polar contacts | Geometry | structure | (0.93) / (0.97) / (0.96) / (0.96) | – | 0 of 4 | – | never |
| Non-isosteric | 1 | AME RMSD [14] | Active-site accuracy | prediction | 0.61 / 0.73 / 0.68 / 0.72 | **0.68 [0.62, 0.75]** | 4 of 4 | 0.45 [0.33, 0.57] | – |
| Non-isosteric | 2 | lk-ball solvation (Rosetta, site) [10] | Rosetta energy | structure | (0.56) / 0.53 / 0.59 / 0.65 | 0.59 [0.51, 0.67] | 3 of 4 | – | non-iso |
| Non-isosteric | 3 | Total SASA | Geometry | structure | (0.46) / 0.51 / (0.49) / 0.58 | 0.55 [0.48, 0.60] | 2 of 4 | – | non-iso |
| Non-isosteric | 4 | pKa shift, max absolute (PROPKA) [12, 13] | pKa | structure | (0.53) / 0.53 / – / – | 0.53 [0.42, 0.65] | 1 of 2 | – | never |
| Ala | 1 | Fraction buried | Geometry | structure | (0.54) / (0.56) / 0.70 / 0.63 | **0.66 [0.59, 0.74]** | 2 of 4 | – | Ala |
| Gly | 1 | Omega torsion (Rosetta, site) [10] | Rosetta energy | structure | (0.46) / – / (0.58) / 0.52 | 0.52 [0.45, 0.60] | 1 of 3 | – | never |
| Never | 1 | Ligand clearance [14] | Active-site accuracy | prediction | 0.57 / 0.63 / 0.57 / 0.63 | 0.60 [0.54, 0.66] | 4 of 4 | 0.57 [0.44, 0.70] | – |
| Never | – | Pairwise distance, max | Geometry | structure | (0.30) / (0.36) / (0.19) / – | – | 0 of 3 | – | never |

**Table 8. Axis C, the chemistry ladder: the 35 ranked items grouped by the lesion at which they are first detected and ranked by R within the group.** Rank statistic R, the probability that a metric changes more at the catalytic lesion than at the matched control (0.5 = no specificity), at the four steps and as the mean over the steps counted, with a 95% interval that resamples enzyme sub-subclasses (systems for the predictor). "Detected from" is the smallest lesion step (isosteric 15 Å³, non-isosteric 36 Å³, Ala 53 Å³, Gly 81 Å³) at which the metric responds; "Specific from" the smallest step at which it is specific under the specificity ratio rule (structure-space metrics; "–" where the rule does not apply). Structure-space metrics: up to 195 natural enzymes (143 main + 52 pilot; the number of enzymes in which a metric moves at all ranges from 1 to 150 per metric and step); prediction-based metrics and reference rows (italic): 59 natural enzymes, 286 pairs. A step in parentheses is not counted. A mean in bold exceeds the best-of-33 threshold (median 0.57, 95th percentile 0.62; a reference level, not a confidence interval or a p-value). The distance-matched R is for the prediction-based metrics only. The 8 supplementary comparators and all per-step flags are in Table S26. Source: `tables/main/T8_specificity_axis_C.csv`.

The 8 supplementary comparators, the per-step flags, the specificity ratio and the frozen rule for the predictor are in Tables S26, S28 and S29.

### 3.4.2 Axis E: second-shell removal

**Experiment.** One, two or four residues of the second shell around the catalytic residues are mutated and the structure is repacked (second-shell removal); the control does the same for the same number of residues around matched non-catalytic positions, and both arms are scored over the catalytic residues.

**Dataset.** The 143 M-CSA enzymes [3] pooled with the 52 pilot enzymes that are not in it, with a control arm for up to 193 of them; the number of enzymes in which a metric moves at all ranges from 0 to 182 per metric and dose. Structure-space metrics only: no predictor run was made for this axis (Methods 2.4.2). <!-- src: tables/spec/derived/axis_ranking_meta.json; results/P2KE/blindness_map.csv -->

**Ranking criteria.** The 29 structure-space main-set metrics are ranked as in Table 8, with R at the three doses (1, 2 and 4 residues removed) and its mean over the doses; "Detected from" is the smallest number of residues removed at which the metric responds ("Never" if none), and rows within a group are ranked by raw R. A metric with no R in at least five proteins has "–". No reference level is computed and no value is in bold (see the caption); the last column counts, for each metric, the doses (of 3) at which it responds to the removal and at which the control response is above the metric's noise.

<!-- cols: 1.2,0.6,3.0,1.8,2.7,2.3,2.2 -->
| Detected from | Rank in group | Item | Group | R at 1 / 2 / 4 residues removed | Mean R [95% interval] | Doses with a response / with a control above noise |
|---|---|---|---|---|---|---|
| 4 residues | 1 | pKa shift, mean (PROPKA) [12, 13] | pKa | 0.74 / 0.72 / 0.64 | 0.70 [0.64, 0.75] | 1 / 0 |
| 4 residues | 2 | pKa, mean (PROPKA) [12, 13] | pKa | 0.73 / 0.71 / 0.64 | 0.69 [0.63, 0.75] | 1 / 0 |
| Never | 1 | Fraction buried | Geometry | 0.91 / 0.79 / 0.65 | 0.78 [0.68, 0.87] | 0 / 0 |
| Never | 2 | Rotamer, Dunbrack (Rosetta, site) [10] | Rosetta energy | 0.79 / 0.76 / 0.69 | 0.75 [0.69, 0.79] | 0 / 0 |
| Never | 3 | pKa, max (PROPKA) [12, 13] | pKa | 0.75 / 0.72 / 0.68 | 0.71 [0.66, 0.77] | 0 / 0 |
| Never | 4 | Pairwise distance, mean | Geometry | 0.76 / 0.75 / 0.63 | 0.71 [0.65, 0.77] | 0 / 0 |
| Never | 5 | Radius of gyration | Geometry | 0.77 / 0.71 / 0.64 | 0.71 [0.64, 0.76] | 0 / 0 |
| Never | 6 | pKa, range (PROPKA) [12, 13] | pKa | 0.74 / 0.72 / 0.65 | 0.71 [0.65, 0.76] | 0 / 0 |
| Never | 7 | lk-ball solvation (Rosetta, site) [10] | Rosetta energy | 0.72 / 0.73 / 0.66 | 0.70 [0.66, 0.75] | 0 / 1 |
| Never | 8 | Total SASA | Geometry | 0.73 / 0.71 / 0.66 | 0.70 [0.65, 0.75] | 0 / 0 |
| Never | 9 | Intra-residue repulsion (Rosetta, site) [10] | Rosetta energy | 0.72 / 0.73 / 0.64 | 0.70 [0.64, 0.75] | 0 / 0 |
| Never | 10 | pKa shift, max absolute (PROPKA) [12, 13] | pKa | 0.75 / 0.68 / 0.66 | 0.70 [0.64, 0.75] | 0 / 1 |
| Never | 11 | Relative SASA, mean | Geometry | 0.73 / 0.71 / 0.64 | 0.70 [0.64, 0.74] | 0 / 0 |
| Never | 12 | Attraction (Rosetta, site) [10] | Rosetta energy | 0.73 / 0.69 / 0.61 | 0.67 [0.63, 0.72] | 0 / 0 |
| Never | 13 | Relative SASA, max | Geometry | 0.69 / 0.69 / 0.64 | 0.67 [0.61, 0.73] | 0 / 0 |
| Never | 14 | Electrostatics (Rosetta, site) [10] | Rosetta energy | 0.74 / 0.70 / 0.58 | 0.67 [0.62, 0.72] | 0 / 1 |
| Never | 15 | Worst residue (Rosetta, site) [10] | Rosetta energy | 0.74 / 0.68 / 0.59 | 0.67 [0.61, 0.72] | 0 / 0 |
| Never | 16 | pKa, min (PROPKA) [12, 13] | pKa | 0.74 / 0.67 / 0.60 | 0.67 [0.61, 0.73] | 0 / 0 |
| Never | 17 | Net van der Waals (Rosetta, site) [10] | Rosetta energy | 0.74 / 0.67 / 0.58 | 0.66 [0.61, 0.71] | 0 / 1 |
| Never | 18 | H-bond, side chain (Rosetta, site) [10] | Rosetta energy | 0.72 / 0.68 / 0.59 | 0.66 [0.59, 0.72] | 0 / 1 |
| Never | 19 | Site total (Rosetta) [10] | Rosetta energy | 0.71 / 0.66 / 0.60 | 0.66 [0.60, 0.71] | 0 / 1 |
| Never | 20 | Pairwise distance, max | Geometry | 0.72 / 0.65 / 0.60 | 0.66 [0.52, 0.76] | 0 / 0 |
| Never | 21 | Repulsion (Rosetta, site) [10] | Rosetta energy | 0.71 / 0.63 / 0.62 | 0.65 [0.60, 0.71] | 0 / 1 |
| Never | 22 | Solvation (Rosetta, site) [10] | Rosetta energy | 0.72 / 0.66 / 0.57 | 0.65 [0.60, 0.70] | 0 / 1 |
| Never | 23 | H-bond, backbone to side chain (Rosetta, site) [10] | Rosetta energy | 0.56 / 0.68 / 0.65 | 0.63 [0.56, 0.70] | 0 / 0 |
| Never | 24 | Polar contacts | Geometry | 0.59 / 0.59 / 0.65 | 0.61 [0.49, 0.73] | 0 / 0 |
| Never | 25 | Ramachandran (Rosetta, site) [10] | Rosetta energy | 0.10 / 0.00 / 0.00 | 0.03 [0.00, 0.11] | 0 / 3 |
| Never | – | Omega torsion (Rosetta, site) [10] | Rosetta energy | – / – / – | – | 0 / 3 |
| Never | – | Amino-acid propensity (Rosetta, site) [10] | Rosetta energy | – / – / – | – | 0 / 3 |

**Table 9. Axis E, second-shell removal: the 29 structure-space main-set metrics grouped by the dose at which they are first detected and ranked by raw R within the group.** Rank statistic R, the probability that a metric changes more when second-shell residues are removed around the catalytic residues than around a matched control (0.5 = no specificity), at the three doses and as the mean over the doses, with a 95% interval that resamples enzyme sub-subclasses. "Detected from" is the smallest number of residues removed at which the metric responds ("Never" if none); a metric with no R in at least five proteins has "–". No cell qualifies as interpretable, so no reference level is computed and no value is in bold: the last column counts, for each metric, the doses (of 3) at which it responds to the removal and at which the control response is above the metric's noise. The 8 supplementary comparators and the per-dose flags are in Table S27. Source: `tables/main/T9_specificity_axis_E.csv`.

The 8 supplementary comparators, the per-dose flags and the specificity ratio are in Tables S27 and S28.

---

<!-- refs:start -->
## References for Section 3

*Reference numbers are local to this section.*

[1] Burley, S. K., Bhatt, R., Bhikadiya, C. et al. Updated resources for exploring experimentally-determined PDB structures and Computed Structure Models at the RCSB Protein Data Bank. Nucleic Acids Research 53, D564–D574 (2025). doi:10.1093/nar/gkae1091 <!-- bib: burley2025 -->

[2] Berman, H. M., Westbrook, J., Feng, Z. et al. The Protein Data Bank. Nucleic Acids Research 28, 235–242 (2000). doi:10.1093/nar/28.1.235 <!-- bib: berman2000 -->

[3] Ribeiro, A. J. M., Holliday, G. L., Furnham, N., Tyzack, J. D., Ferris, K., Thornton, J. M. Mechanism and Catalytic Site Atlas (M-CSA): a database of enzyme reaction mechanisms and active sites. Nucleic Acids Research 46, D618–D623 (2018). doi:10.1093/nar/gkx1012 <!-- bib: ribeiro2018 -->

[4] The UniProt Consortium. UniProt: the Universal Protein Knowledgebase in 2023. Nucleic Acids Research 51, D523–D531 (2023). doi:10.1093/nar/gkac1052 <!-- bib: uniprot2023 -->

[5] Chai Discovery, Boitreaud, J., Dent, J. et al. Chai-1: Decoding the molecular interactions of life. bioRxiv (2024). doi:10.1101/2024.10.10.615955 <!-- bib: chai2024 -->

[6] Hanley, J. A., McNeil, B. J. The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology 143, 29–36 (1982). doi:10.1148/radiology.143.1.7063747 <!-- bib: hanley1982 -->

[7] Mann, H. B., Whitney, D. R. On a test of whether one of two random variables is stochastically larger than the other. The Annals of Mathematical Statistics 18, 50–60 (1947). doi:10.1214/aoms/1177730491 <!-- bib: mann1947 -->

[8] Westfall, P. H., Young, S. S. Resampling-Based Multiple Testing: Examples and Methods for p-Value Adjustment. Wiley (1993). <!-- bib: westfall1993 -->

[9] Jumper, J., Evans, R., Pritzel, A. et al. Highly accurate protein structure prediction with AlphaFold. Nature 596, 583–589 (2021). doi:10.1038/s41586-021-03819-2 <!-- bib: jumper2021 -->

[10] Alford, R. F., Leaver-Fay, A., Jeliazkov, J. R. et al. The Rosetta All-Atom Energy Function for Macromolecular Modeling and Design. J. Chem. Theory Comput. 13, 3031–3048 (2017). doi:10.1021/acs.jctc.7b00125 <!-- bib: alford2017 -->

[11] Evans, R., O’Neill, M., Pritzel, A. et al. Protein complex prediction with AlphaFold-Multimer. bioRxiv (2021). doi:10.1101/2021.10.04.463034 <!-- bib: evans2021 -->

[12] Olsson, M. H. M., Søndergaard, C. R., Rostkowski, M., Jensen, J. H. PROPKA3: Consistent Treatment of Internal and Surface Residues in Empirical pKa Predictions. Journal of Chemical Theory and Computation 7, 525–537 (2011). doi:10.1021/ct100578z <!-- bib: olsson2011 -->

[13] Søndergaard, C. R., Olsson, M. H. M., Rostkowski, M., Jensen, J. H. Improved Treatment of Ligands and Coupling Effects in Empirical Calculation and Rationalization of pKa Values. Journal of Chemical Theory and Computation 7, 2284–2295 (2011). doi:10.1021/ct200133y <!-- bib: sondergaard2011 -->

[14] Ahern, W., Yim, J., Tischer, D. et al. Atom-level enzyme active site scaffolding using RFdiffusion2. Nature Methods 23, 96–105 (2026). doi:10.1038/s41592-025-02975-x <!-- bib: ahern2026 -->

[15] Kim, D., Woodbury, S. M., Ahern, W. et al. Computational design of metallohydrolases. Nature 649, 246–253 (2026). doi:10.1038/s41586-025-09746-w <!-- bib: kim2026 -->

[16] Field, C. A., Welsh, A. H. Bootstrapping Clustered Data. Journal of the Royal Statistical Society Series B: Statistical Methodology 69, 369–390 (2007). doi:10.1111/j.1467-9868.2007.00593.x <!-- bib: field2007 -->

[17] Carlin, D. A., Caster, R. W., Wang, X. et al. Kinetic Characterization of 100 Glycoside Hydrolase Mutants Enables the Discovery of Structural Features Correlated with Kinetic Constants. PLOS ONE 11, e0147596 (2016). doi:10.1371/journal.pone.0147596 <!-- bib: carlin2016 -->

[18] Spearman, C. The proof and measurement of association between two things. The American Journal of Psychology 15, 72–101 (1904). doi:10.2307/1412159 <!-- bib: spearman1904 -->

<!-- refs:end -->
