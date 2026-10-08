# 2 Methods

**How this section is organised.** Section 2 has four subsections, one for each subsection of the Results (2.1 → 3.1, 2.2 → 3.2, 2.3 → 3.3, 2.4 → 3.4). Each of them is written to the same template, in the same order: **Question**, **Data**, **Change** (or **Contrast**, when nothing is perturbed), **Comparator**, **Scoring**, **Statistics and decision rule**, **Limits**. Before 2.1 comes the map of the whole study (Figure 1, Tables 1 and 2) and the terms and metrics that every subsection uses (Boxes 1 and 2).

## The study at a glance

We ask one question: **do the in-silico metrics used to filter designed enzymes respond to catalysis, or to something simpler, such as how close a change is to the active site?** A metric that detects catalysis should move more when a catalytic residue is damaged than when the same damage is made elsewhere in the same protein. Figure 1 shows how the study tests this, in four experiments.

![The study map](fig1_study_map.png)

**Figure 1. The study map.** The four experiments, what is changed or contrasted in each, what the metric is compared with, which metrics are used, and which claim the experiment supports. Numbers are taken from Tables 1 and 2. <!-- src: tables/main/T1_design_overview.csv; tables/main/T2_datasets.csv -->

The four experiments sit at three levels of evidence, from the most controlled to the most realistic:

- **Perturbation with a matched control** (2.1, 2.2). We damage a protein on purpose and compare the metric's response at the catalytic site with its response to the identical damage at a matched non-catalytic site. This supports claims about **specificity**.
- **A real contrast** (2.3). Nothing is perturbed. We compare metric values between enzymes that are catalytically dead and enzymes that are active. This supports claims about **discrimination**.
- **Measured effects** (2.4). Nothing is perturbed. We compare metric values with measured activity. This supports claims about **ranking**.

Two kinds of metric are tested. **Structure-space metrics** read atomic coordinates; they are tested in 2.1, 2.3 and 2.4. **Prediction-based metrics** read the output of a structure predictor that is given a sequence and a ligand; they are tested in 2.2, and again in 2.3 and 2.4. The metrics tested in both parts are the ones this paper reports (Box 2).

**Table 1. The experiments in detail.** Each row is one experiment: the Results subsection that reports it, what is changed or contrasted, what the metric is compared with, which metrics are scored, and how many units there are. <!-- src: tables/main/T1_design_overview.csv -->

<!-- cols: 1.45,2.2,3.0,2.6,1.6,1.7 -->
| Results | Experiment | What is changed or contrasted | Compared with | Metrics | Units |
|---|---|---|---|---|---|
| 3.1 | Chemistry ladder in structures | catalytic residues replaced in four steps: isosteric, non-isosteric, to Ala, to Gly | the identical substitution at matched non-catalytic sites | 29 structure-space | 143 enzymes |
| 3.1 | Second-shell support removed | 1, 2 or 4 second-shell residues removed | matched control | same 29 | 143 enzymes |
| 3.1 | Detection floor | all catalytic residues replaced by Gly (the same lesion as the Gly step) | the untouched structure, put through the same treatment | same 29 | 143 enzymes |
| 3.2 | Substrate swap | the ligand given to the predictor: cognate, same class, different class, decoy | the cognate ligand; noise from 5 seeds | 5 prediction-based | 59 enzymes, 30 designs |
| 3.2 | Chemistry ladder, re-predicted | one catalytic residue substituted per prediction | matched control, then a distance-matched control | same 5 | 312 pairs in 74 systems |
| 3.3 | Zymogen versus mature enzyme | none (real dead and active forms) | reference rows and a confound floor | 29 structure-space | 49 pairs |
| 3.3 | Zymogen versus mature, re-predicted | none | reference rows | 5 prediction-based | 28 pairs |
| 3.4 | BglB variants | none (real substitutions with measured kinetics) | five declared baselines | 29 structure-space | 432 variants at 175 positions |
| 3.4 | BglB variants, re-predicted | none | the same baselines | 5 prediction-based | same |
| 3.4 | Plated designs | none (192 designs, 16 with measured activity) | a random filter and reference rows | both kinds | 192 designs |

**Table 2. Datasets.** Which data each Results subsection uses, and what the labels are. <!-- src: tables/main/T2_datasets.csv -->

<!-- cols: 2.2,1.8,3.6,2.4,2.7 -->
| Dataset | Used in | Composition | Labels | Notes |
|---|---|---|---|---|
| 143-enzyme set | 3.1 | enzymes from the Mechanism and Catalytic Site Atlas (M-CSA), 77 enzyme sub-subclasses, median 6 catalytic residues; 2 carry a bound ligand | none | the primary set |
| Shortened-motif set | 3.1 (sensitivity) | the same 143 enzymes with at most 3 catalytic residues kept | none | tests whether motif size matters |
| Pilot set | 3.1 (sensitivity) | 53 enzymes (annotation from UniProt active sites and M-CSA, mixed; 35 peptidases; 34 with a ligand) | none | not a subset of the 143-enzyme set; shares one PDB entry |
| Curated designs | 3.1 (sensitivity), 3.2 | 30 de novo metallohydrolase designs with a three-histidine zinc site; transition-state analogue supplied | 16 active, 3 inactive, others unlabelled | 23 of the 30 are on the plates |
| Substrate-swap enzymes | 3.2 | 59 M-CSA enzymes, stratified by enzyme class | none | 28 are also in the 143-enzyme set |
| Ladder pairs | 3.2 | 74 systems (59 natural, 15 designs); 312 catalytic/control pairs | none | one residue per prediction |
| Zymogen–mature pairs | 3.3 | 49 pairs scored (55 candidates) | dead (zymogen) or active (mature) | trapping-mutant pairs were examined and retired (Supplement) |
| Re-predicted pairs | 3.3 | 28 zymogen pairs; 21 share a ligand between the two forms | as above | subset of the 49 |
| BglB variants | 3.4 | β-glucosidase B: 655 single-point variants at 207 positions; 432 analysed at 175 positions | log10 kcat/KM relative to wild type: 166 impaired, 254 wild-type-like | one enzyme; variant-level data are not redistributed |
| Plated designs | 3.4 | 192 designs on two 96-well plates | 16 with measured kcat/KM; 176 with *no reported activity* (not negatives) | the comparison class is "not reported" |

> **Box 1 — Terms used throughout.** **Lesion**: a deliberate change to a protein (a substitution, a removal, or a swap of the ligand given to a predictor). **Response (Δ)**: how much a metric changes because of a lesion, measured against the same protein put through the same treatment without it. **Matched control**: the identical lesion applied at a non-catalytic site of the same protein, matched on residue type and burial (and, where stated, packing, secondary structure and distance to the ligand). **Specificity ratio (SR)**: the response at the catalytic site divided by the response at the control; SR = 1 means the metric cannot tell the two apart. **Discrimination (AUROC)**: the probability that a randomly chosen member of one class scores higher than a member of the other, where 0.5 means no discrimination; we report the direction-free form max(A, 1 − A), which cannot fall below 0.5. **Ranking**: whether a metric orders designs or variants by measured activity (Spearman ρ, or expected hits per plate). **Reference row or baseline**: a quantity that needs no catalytic information (resolution, sequence length, tyrosine fraction, the distance to the catalytic residues) which any useful metric must beat.

**Box 2 — The 34 reported metrics and the reference rows.** In a structure, "perturbed residues" are the residues that were changed; in the control arm they are the control residues, so a site-scoped metric never knows which residues are catalytic — it only knows which residues it was handed. <!-- src: tables/audit/A5_main_metric_set.csv; src/mrx/perturb/engine.py scoring_scope -->

<!-- cols: 2.4,4.6,2.0,2.6 -->
| Group | Metrics | Reads | Scored over |
|---|---|---|---|
| Rosetta energy, site-scoped (15) | attraction, repulsion, intra-residue repulsion, solvation, lk-ball solvation, electrostatics, hydrogen bonds (backbone–side-chain, side-chain–side-chain), rotamer (Dunbrack), Ramachandran, amino-acid propensity, omega torsion, net van der Waals, site total, worst single residue | coordinates | the perturbed residues |
| Catalytic geometry (8) | fraction buried, relative solvent-accessible area (mean, max), total solvent-accessible area, pairwise distance (mean, max), radius of gyration, polar contacts | coordinates | the perturbed residues |
| Catalytic pKa (6) | PROPKA pKa (min, max, mean, range) and pKa shift (mean, max absolute) | coordinates | the perturbed residues |
| Interface confidence (3) | ipTM, aggregate score, per-chain pTM minimum | predictor output | the protein–ligand interface |
| Active-site accuracy (2) | AME RMSD (catalytic-atom RMSD to a reference structure after backbone superposition, best of the predicted models); ligand clearance (closest approach of the ligand to the backbone, best of the models) | predictor output and a reference structure | the catalytic atoms; the ligand |
| Reference rows (6; never counted as metrics under test) | resolution, sequence length, net charge, tyrosine fraction, pLDDT, pTM | deposit, sequence or predictor | whole protein |

**Which metrics are reported.** The panel contains 216 named quantities, which collapse to 191 distinct metrics once literal aliases are merged; 63 of them are bookkeeping counters and constants on which no test can be run. Whether a metric can be tested in a given experiment is decided from three things only — what the metric reads, whether it is defined under the experimental condition, and the design of the experiment — never from the result. A metric with no residue-set input (whole-protein energies, sequence composition, whole-prediction confidence) cannot respond *specifically* to catalytic residues, and a metric whose input cannot reach the perturbed quantity cannot register the lesion at all (sequence composition under a rotamer change, for example). Such metrics are kept as comparators in the Supplement. The main text reports the **34 metrics that are valid and tested in both Part 1 and Part 2** (Box 2), so that one set of metrics runs through the whole paper, plus six reference rows chosen before any result was seen. <!-- src: tables/audit/A5_main_metric_set.csv (34 main, 6 reference, 63 bookkeeping of 191 keys); tables/audit/A1_metric_contracts.csv (216 names); tables/RULES.md; tables/rules.json -->

---

## 2.1 Structure-space metrics under matched perturbation → Results 3.1

**In one sentence.** We damage the catalytic residues of 143 enzymes in the computer, and ask whether each structure-space metric moves more than it does when the same damage is made at a matched non-catalytic site.

**Illustration.** In a serine protease the catalytic triad is Asp, His and Ser. The *Ala step* builds a structure in which those three residues are replaced by Ala. The *control* builds a structure in which three buried, non-catalytic residues of the same original types are replaced by Ala, with the same repacking. A metric is *specific* if it changes clearly more in the first structure than in the second.

**Question.** Do structure-space metrics see damage to catalytic residues, and do they respond more to it than to the same damage at a matched site elsewhere in the protein?

**Data.** The 143-enzyme set (Table 2): M-CSA enzymes (release 2026-07-31), chosen at up to 25 per top-level enzyme class so that 77 enzyme sub-subclasses are covered. Catalytic residues are the M-CSA residues with a catalytic role (median 6 per enzyme); structures come from the Protein Data Bank. Two variants of the set test sensitivity: a shortened motif (the first three catalytic residues only) and the 53-enzyme pilot set. <!-- src: data/systems/p2_d0_v2/summary.json -->

**Change.** Two kinds of lesion, each applied to the catalytic residues:
- **The chemistry ladder** replaces each catalytic residue in one of four steps of increasing change in side-chain volume: **isosteric** (for example Ser→Cys, Asp→Asn, Thr→Val; median change 15.3 Å³), **non-isosteric** (36.4 Å³), **to Ala** (53.2 Å³) and **to Gly** (80.5 Å³). <!-- src: results/rung_geometry.json -->
- **Second-shell removal** mutates 1, 2 or 4 residues in the shell around the catalytic residues.

Every change is made in side-chain rotamer space on the fixed backbone, followed by an 8 Å fixed-backbone repack with the changed residues held and constrained minimisation. Protonation is fixed. The **detection floor** replaces all catalytic residues by Gly at once, which is the same lesion as the Gly step, and asks only whether the metric notices. <!-- src: tables/main/T3_part1A_structure_space.csv -->

**Comparator.** Two comparisons are made, and they answer different questions.
- *Against the structure's own reference.* Every perturbed structure and its reference go through the identical treatment, because 26 of 103 metrics move under the treatment alone; each arm is compared with its own treated reference, never with the untouched crystal.
- *Against the matched control.* The control makes the **identical substitution** (same original and same new residue type) at buried, non-catalytic positions of the same protein, matched on burial (within 0.10 relative solvent-accessible area) and, in the primary analysis, on local packing, secondary structure and distance to the ligand where available. When no exact match exists, the matcher relaxes its criteria in a fixed order and records the loosest tier used. Only comparisons where both arms change the same number of residues are counted.

**Scoring.** The 29 structure-space metrics (Box 2) are computed on every structure. For the chemistry ladder, site-scoped metrics are computed over the changed residues in each arm (the catalytic residues in the catalytic arm, the control residues in the control arm); for second-shell removal both arms are scored over the catalytic residues. The response is Δ = metric(changed) − metric(own reference), summarised as the median over enzymes.

**Statistics and decision rule.**
- *Intervals* are percentile bootstrap intervals that resample **enzyme sub-subclasses**, not enzymes, so that related enzymes are not counted as independent (2,000 draws, fixed seed 20260807).
- A metric **responds** when the interval of its median Δ excludes zero.
- The specificity ratio is SR = median |Δ| at the catalytic site ÷ median |Δ| at the control.
- A metric is called **specific** only when all five conditions hold: (1) the catalytic response is significant; (2) the interval of SR excludes 1; (3) the control arm contributes at least half as many observations as the catalytic arm; (4) the control response exceeds 1% of the metric's own native standard deviation, because a ratio whose denominator is below the metric's noise is not specificity; (5) both arms changed equal numbers of residues.
- Counts are given as **distinct metrics**, with literal duplicates collapsed.
- The whole panel is summarised by the geometric-mean SR over metrics with a defined ratio, with a nested bootstrap (3,000 draws) that recomputes every metric inside each draw, so that correlation between metrics is carried through. Equivalence to 1 is judged against a ±25% band. <!-- src: results/isosteric_equivalence_clustered.json; src/mrx/stats/blindness.py -->

**Limits.**
- The match is on burial, packing and local environment, not on distance to the catalytic site; its quality is reported in the Supplement.
- The effective number of independent metrics is smaller than the count (participation ratio 7.9 for the metrics' native values and 10.5 for their isosteric responses, out of 29). <!-- src: tables/spec/derived/dimensionality_main.json -->
- Two supplementary designs show how far the result depends on the control: the same experiment without packing matching and arm-count gating, and the 30 de novo designs with a constructed control.
- Experiments that could not be made are listed in the Supplement and are not reported as null results: a deformation axis (most apparent specific cells tracked the clash burden present before repacking), oxyanion-hole removal (the rung that had been run located no bound ligand in any of the 143 structures and removed a proxy residue instead, so it did not test the named change) and metal removal (no cell could be scored on any metric). <!-- src: tables/supp/S08_not_measurable.csv; results/P2KE/oxyanion_provenance.json; results/P2K/g_clash_attribution.csv -->

---

## 2.2 Prediction-based metrics: substrate swap and the re-predicted ladder → Results 3.2

**In one sentence.** We give a structure predictor (Chai-1) the wrong substrate, and then a catalytically damaged sequence, and ask whether its confidence and active-site accuracy respond to catalysis or only to the distance between the changed residue and the ligand.

**Illustration (substrate swap).** Chai-1 predicts a hydrolase together with its own substrate, and again together with a substrate of a different enzyme class. If ipTM falls when the wrong substrate is given, the metric "knows" which substrate belongs to the protein; the AUROC measures how reliably it does.

**Question.** Do prediction-based metrics know which substrate a protein was given, and is their response to a catalytic substitution specific once the control is matched on distance to the ligand?

**Data.** Substrate swap: 59 natural enzymes and 30 de novo designs. Re-predicted ladder: 74 systems (59 natural, 15 designs) forming 312 catalytic/control pairs (Table 2). <!-- src: results/P5/t1_systems.csv; results/P5/caxis_design.csv -->

**The predictor.** Chai-1 is run on the sequence, the ligand (as a chemical structure) and, where relevant, the catalytic metal, with default settings and a fixed seed. Each prediction yields confidence scores and several models.

**Change.**
- *Substrate swap.* The protein is untouched; what changes is the ligand supplied: the cognate substrate (five seeds), a different substrate of the same enzyme class, one from a different class, and a decoy taken from an unrelated structure (three seeds each). The catalytic metal is kept in every condition. The apo condition (no ligand) is excluded for interface and ligand-dependent terms, because without a ligand there is no interface to be confident about.
- *Re-predicted ladder.* The same four steps as 2.1, but one catalytic residue is substituted in the **sequence** per prediction and the complex is re-predicted.

**Comparator.**
- *Substrate swap* has no matched control. Its comparator is the cognate condition, and its noise floor is the spread over the five cognate seeds.
- *Ladder.* Each substitution is paired with the identical substitution at a buried non-catalytic position (same original and same new residue, matched on burial). The change is measured against the unperturbed prediction of the same system at the same seed.
- *Distance control (pre-registered).* Catalytic residues touch the ligand by definition, so an interface metric would respond more to a catalytic substitution than to a distant control even if it knew nothing about catalysis. Before any distance was computed we froze the following plan. For every pair we measure the minimum distance from the substituted side chain to the ligand. We then analyse (i) distance strata; (ii) a **caliper-matched subset**: pairs whose distances differ by at most 2 Å and whose burial differs by at most 0.10, with the same residue types and the control not adjacent to a catalytic residue, extended by 54 pairs given a new in-caliper control (53 new predictions) wherever one existed; and (iii) a regression adjustment, log|Δ| ~ arm + ligand distance + burial. <!-- src: results/P5_1B/PREREG_1B.md -->

**Scoring.** The five reported prediction-based metrics (Box 2) are computed on each prediction.
- **Active-site accuracy (AME)** superposes a predicted model on a reference structure by the whole shared backbone and measures the RMSD of the catalytic atoms (best of the models, symmetry-equivalent atoms resolved). The reference is the deposited structure for natural enzymes and the design's own model for designs; the two flavours are never pooled. In the ladder, both pair members are scored over the catalytic set *minus* the substituted position, so AME reports only the displacement of the remaining catalytic residues.
- **Ligand clearance** is the closest approach of the ligand to the backbone, best case over models.
- **Interface confidence** (ipTM, aggregate score, per-chain pTM minimum) and ligand clearance need a ligand and are undefined without one.

**Statistics and decision rule.**
- *Substrate swap:* direction-free AUROC between the metric under the cognate ligand and under each wrong ligand, with bootstrap intervals over systems. Because the statistic cannot fall below 0.5, the upper bound of the interval is the informative one. To check whether a ligand-size effect explains the discrimination, we stratify by the difference in heavy-atom count and in charge between the cognate and the wrong ligand, and report the paired win fraction P(cognate scores higher).
- *Ladder:* SR = mean |Δ| at the catalytic site ÷ mean |Δ| at the control (a median-based form is also given), with 5,000 bootstrap draws over systems (seed 20260806). <!-- src: results/P5_1B/REPORT.md -->
- *Decision rule (frozen before the analysis):* an interface metric counts as **specific** only if the lower 90% bound of its mean-based SR in the matched subset exceeds 1.2, with at least 30 pairs in at least 15 systems. AME is reported as knock-on displacement with no specificity verdict, because the substituted residue is excluded from its own comparison.

**Limits.**
- One seed per ladder prediction (a replicate with a second seed on 30 natural pairs estimates the seed noise).
- Chai-1 is not bitwise reproducible; we report the drift of a re-run against the earlier predictions.
- The distance-matched subset is a subpopulation: 213 of 312 pairs have no in-caliper candidate anywhere in their protein. <!-- src: results/P5_1B/REPORT.md sections 4 and 6; results/P5_1B/canary_drift.csv -->

---

## 2.3 Real dead and active enzymes: zymogen–mature pairs → Results 3.3

**In one sentence.** Without perturbing anything, we ask whether the metrics separate a catalytically dead enzyme from its active form when the two have the same catalytic residues.

**Illustration.** A zymogen is an inactive precursor that already contains the catalytic residues of the mature enzyme. A metric that detected catalytic competence would separate the two structures; a metric that only reads the geometry of the catalytic residues would not, because that geometry is almost the same in both.

**Question.** Without any perturbation, do the metrics separate catalytically dead enzymes from active ones?

**Data.** Pairs of structures of the same protein, the zymogen (dead) and the mature enzyme (active). 49 pairs were scored from 55 candidates. After superposing the catalytic constellation, the median RMSD between the two forms is 0.207 Å (0.484 Å after backbone superposition), so the chemistry of the site is intact in the dead form and the pair isolates catalytic competence from catalytic chemistry. A second class, substrate-trapping mutants, was verified against the primary literature (26 of 30 pairs were not confirmed dead) and retired; it appears in the Supplement only. <!-- src: results/P0/REPORT.md (median RMSD table); tables/supp/S08_not_measurable.csv -->

**Contrast.** Nothing is changed; the contrast is dead against active. Structure-space metrics are computed on the deposited structures (catalytic residues from M-CSA and UniProt annotation). For the prediction-based metrics, 28 of the pairs were re-predicted with Chai-1 (three seeds), giving both forms the same ligand set. Interface terms are defined only on the 21 pairs whose two forms share a ligand, and AME is measured against each form's own deposited structure.

**Comparator.** There is no matched control. The comparison is with:
- **Reference rows** that need no catalytic information: crystallographic resolution, sequence length, net charge and tyrosine fraction (and, for predictions, pLDDT and pTM).
- A **confound floor** from a same-state null: 96 pairs of independent structures of the same protein in the same functional state. The floor is the highest AUROC with which a covariate that needs no catalytic information — resolution, sequence length or net charge — separates the zymogen pairs from that null (0.655, net charge). A metric that does not clear it has not been shown to see more than these covariates do. <!-- src: results/P0b/p0b_summary.json (confound_floor); results/P0b/paired_null.csv -->

**Scoring.** Each reported metric is computed on both forms of each pair (Box 2). The statistic is the direction-free AUROC of dead against active.

**Statistics and decision rule.** Percentile bootstrap intervals. The pre-registered criterion was that at least two metrics reach AUROC > 0.8, all systems pooled. With 49 pairs the null standard error of an AUROC is about 0.06, so only an AUROC above roughly 0.7 can be excluded from chance; a point estimate is not offered as a headline when its interval is wider than 0.2. <!-- src: results/P0/REPORT.md section 3; tables/main/T5_part2A_real_dead_active.csv -->

**Limits.**
- 49 pairs is a small anchor. The pair sets differ between analyses (49 scored, 28 re-predicted, 21 sharing a ligand), and each table states which it uses.
- The interface-term AUROCs on the re-predicted pairs were computed before the definedness gate and include apo pairs; they are flagged as not interpretable and restated in the Supplement rather than re-scored.

---

## 2.4 Measured effects: BglB variants and plated designs → Results 3.4

**In one sentence.** Without perturbing anything, we ask whether metrics computed on real variants and real designs track the activity that was measured for them, and whether they do better than simply knowing how close the change is to the active site.

**Illustration.** A variant is *impaired* if the assay measured a clearly lower kcat/KM than wild type. A metric "ranks" if impaired variants have larger |Δ| than variants that stayed wild-type-like. The baselines ask whether knowing only the distance from the mutated residue to the catalytic glutamates does as well.

**Question.** Do the metrics track measured activity, across real substitutions in one enzyme and across designs that were actually ordered and tested?

**Data (BglB).** β-glucosidase B from *Paenibacillus polymyxa*, characterised by the D2DCure consortium: 655 single-point variants at 207 positions (1,288 rows including 272 wild-type replicates measured at eight institutions). Variant numbering is offset by three from the numbering of the crystal structure (PDB 2JIE; structure position = variant position + 3). The catalytic residues are Glu167 (proton donor) and Glu356 (nucleophile) in structure numbering, taken from the UniProt active-site features, the conserved motifs TINEP and ITENG, and the covalent link to the glucosyl intermediate in the deposited structure. <!-- src: results/D4_bglb/PLAN.md; data/systems/d4_bglb_v1/variant_features_summary.json -->

Labels are the log10 ratio of kcat/KM to the wild type of the same institution; the spread of the wild-type replicates (0.293 log10) is the noise floor. A variant is **folded** if it was expressed and is not destabilised (T50 or Tm less than 2 standard deviations below wild type). Folded variants are classed as *impaired* (kcat/KM at least 2 standard deviations, a 3.8-fold loss or more, below wild type; 166 variants), *wild-type-like* (within 2 standard deviations; 254) or *improved* (12). The comparison of 3.4 is impaired against wild-type-like; destabilised (108), non-expressed (83) and insufficient-data (32) variants are set aside, because their kinetics cannot be attributed to the catalytic site. The analysed set is the 432 folded variants with kinetics, at 175 positions. <!-- src: data/systems/d4_bglb_v1/label_summary.json; data/systems/d4_bglb_v1/exclusions.json; results/D4_bglb/PLAN.md -->

**Data (plates).** A deposited metallohydrolase design campaign: 192 designs on two 96-well plates, of which 16 have a reported kcat/KM and 176 have *no reported activity*. A design absent from the characterised-hits table was not measured and found dead; it was simply not reported, so these are never treated as negatives. The catalytic motif is the three histidines that coordinate the zinc, derived geometrically and checked against the 23 curated annotations (23 of 23 agree). <!-- src: results/P6/REPORT.md -->

**Contrast.** Nothing is perturbed experimentally; the variants and designs are the contrast.
- *BglB, structure-space metrics.* Each variant is built in silico with the same rotamer-space substitution, repack and minimisation as in 2.1 (the wild type goes through the identical treatment with five seeds). Metrics are computed over the two catalytic glutamates for every variant; the response is |Δ| against the treated wild type.
- *BglB, prediction-based metrics.* Each variant and the wild type are predicted with Chai-1 together with the assay substrate, 4-nitrophenyl β-D-glucopyranoside (pNPG, the reporter substrate of the published BglB assays; no metal, because BglB is metal-independent). AME is measured against the wild-type crystal, which carries a covalent glucosyl intermediate rather than the substrate. <!-- src: results/D4_bglb/m3/substrate.json -->
- *Plates.* Designs are scored as deposited; their predictions use the design's transition-state-analogue ligand and zinc, with accuracy measured against the design's own model.

**Comparator.** Five **declared baselines**, fixed before any metric was joined to a label: the absolute change in side-chain volume; the distance from the mutated residue to the nearest catalytic residue in the wild-type structure (the *distance baseline*); the burial of the mutated residue; BLOSUM62; and the dataset's own Rosetta score (available for only 248 of the variants, so compared on that subset). For the plates, the comparison is with a random filter and with the reference rows.

**Scoring.** The 29 structure-space metrics and the 5 prediction-based metrics (Box 2) are computed for every variant and design where they are defined.

**Statistics and decision rule.**
- *BglB:* AUROC of |Δ| for impaired against wild-type-like variants, and Spearman correlation with the log ratio, with bootstrap intervals that resample **positions** (5,000 draws, seed 20260807), because variants at one position are not independent. A metric **beats** a baseline only if the position-clustered interval of the difference in AUROC excludes zero. Multiplicity is calibrated with a permutation null (2,000 permutations). <!-- src: results/D4_bglb/m3/REPORT.md section 4 -->
- *Plates:* the **expected hits per 96-well plate** if a plate were filled only from the 25% of designs a metric keeps (the hit rate among the kept designs × 96; the filter may keep the high or the low end), with bootstrap intervals, against the 95th percentile of a random filter (14.0 hits; an unfiltered plate holds 8.0, that is 16 of 192). Separately, the Spearman correlation of each metric with log kcat/KM among the 16 active designs, computed on the native design values with sequence length partialled out of both sides. By prior ruling (2026-08-09) the plate analysis is **descriptive**: no hypothesis test against activity is made. <!-- src: results/P6/enrichment_summary.json -->

**Limits.**
- One enzyme, and 16 actives across the plates.
- The BglB wild-type reference for prediction-based accuracy is a covalent-intermediate crystal.
- Cluster units for designs are proxies, because backbone-cluster identifiers are not held.

---

**Provenance and data availability.** Every number in this paper is read from a table generated by script from committed result files, with seeds and input hashes recorded. Each experiment's analysis plan was committed and dated before the analysis it governs, and amendments are listed with the date they were made. The Supplement gives, for every metric and every experiment, whether the metric was applicable and why; the full per-metric tables behind Tables 3–6; and the experiments that could not be made. Structures and predictor weights are third-party and are not redistributed; their hashes are. BglB variant-level data are not redistributed because their licence is unstated; only aggregates are reported. <!-- src: tables/INDEX.csv; tables/README.md -->
