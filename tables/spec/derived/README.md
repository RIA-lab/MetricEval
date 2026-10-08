# Derived inputs to the paper tables

Small aggregates computed from `results/scores.parquet` by read-only SLURM jobs (the parquet is never opened
on the login node). They exist so that `ops/make_tables.py` reads only committed files.

| file | produced by | job |
|---|---|---|
| `ctl_worst_tier.csv` | `ops/tables_control_audit.py` (copy of the audit script run from `data/interim/_cov_scratch/`) | 366787 |
| `ctl_arm_balance.csv` | `ops/tables_control_audit2.py` | 366793 |
| `panel_equivalence_main*.json` | `ops/panel_equivalence_main.py` (main-set restricted panel statistic) | see `runs/tables-panel-eq-*` |

`ctl_worst_tier.csv`: `x_worst_tier` is the loosest matching tier any control target needed (0 = exact, 5 = burial relaxed).
`ctl_arm_balance.csv`: per system, residues perturbed in the control arm vs the catalytic arm.
