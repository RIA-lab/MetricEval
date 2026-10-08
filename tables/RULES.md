# Applicability rules for the paper tables

Machine-readable source of truth: `rules.json` (its sha256 is recorded in `MANIFEST.json`). This file explains it.

## Principle

A test is meaningful for a metric only if the metric's **input** can see the thing the test changes.
Applicability is decided from inputs, definedness and test design -- **never from verdicts**
(a unit test shuffles the verdicts and asserts the matrix does not move).

## Why the rules are needed (verified in code, see `audit/A1_metric_contracts.csv`)

* Sequence-only metrics have no residue-set input. Under the C axis the X control makes the *identical*
  substitution (residue type matched exactly), so their specificity ratio is 1 by arithmetic; under G and
  `metal_removed` they cannot change at all.
* In the C and G axes the X-control arm scores "catalytic-scoped" metrics over the **control residues**
  (`src/mrx/perturb/engine.py` `scoring_scope`). They are *perturbed-site-scoped*: they know which residues
  they were handed, not which are catalytic. In E both arms are scored over the catalytic residues.
* AME in the M3 chemistry ladder never sees the substituted side chain (it is excluded from its own comparison).
* Interface terms (ipTM, aggregate score, per-chain pTM minimum, ligand clearance) are undefined without a ligand,
  and a catalytic residue is near the ligand by definition: they need a proximity-matched control.
* `ops/p5_score_t2.py` never calls the definedness gate (42 of 324 T2 inputs have no ligand).

## Status codes

See `rules.json` -> `status_codes`. Precedence (first match wins):
`X-BOOKKEEP` > `X-ARM` > `X-NOINPUT` > `X-WITHDRAWN` > `X-NOCTRL` > `NOT-RUN` > `DUP` > matrix cell >
`REF` override > `X-UNDEF-COV`.

## Input class x test class

Input classes: `seq_only`, `bookkeeping`, `struct_whole`, `struct_site`, `deposit_meta`, `pred_global`,
`pred_interface`, `ame`, `placer_csv`, `placer_site`.
Test classes: `detection_dup` (N0 cat->Gly, identical to the C-Gly rung), `spec_C`, `spec_E`, `G`, `sanity_n0`
(other N0 conditions), `S_m3` (substrate swap), `ladder_m3` (M3 chemistry ladder), `placer_c`, `real_m1`,
`real_m3` (2A), `rank_m1`, `rank_m3` (2B). The full matrix is in `rules.json`.

Sub-classes of `struct_site` (Rosetta site-scoped, catalytic geometry, triad, ligand/metal M1, PROPKA) share one
row: their differing coverage (triad only on peptidase systems, ligand metrics on ~2 of 143 systems, PROPKA after
truncation) is applied by the **coverage rule**, not by hand.

## Deviations from the approved plan (recorded on purpose)

* PLACER site-scoped ensemble metrics are `X-CONFOUND` in every crop configuration, not "OK in crop-matched P2K":
  the control arm is covered 1.6-3.2x less than the catalytic arm in every configuration
  (`results/isoplacer/REPORT.md`), so no configuration gives a like-for-like ratio.
* A single coverage threshold (>= 50 % of units and >= 20 units; `partial` flag below 80 %) is used for both
  testability and the main set, because an 80 % hard threshold would drop the interface terms (defined on 21 of
  28 zymogen pairs = 75 %) for an arbitrary reason.

## Main metric set

`V1` and `V2` as in `rules.json` -> `main_set`. Reference rows (fixed a priori): `seq_length`, `frac_Y`,
`net_charge`, `resolution_A` (2A only), `chai_plddt_mean`, `chai_ptm_mean` (M3 tests only), plus the BglB
distance-to-catalytic-residues baseline (`d_cat`, not a panel metric).

## Claim types

detection (can the metric see damage), specificity (catalytic vs matched control), equivalence, not_measurable,
discrimination (real contrast), ranking (measured label), enrichment, baseline, design, audit.
