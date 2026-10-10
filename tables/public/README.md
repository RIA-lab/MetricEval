# Public tables

7 data tables of the Results (Tables 5 to 11) and 49 supplementary tables of the paper, as CSV (UTF-8, comma-separated, one header row).
The Supplementary PDF describes every table: what a row is, what the columns mean and which part of the paper uses it.
`INDEX.csv` lists all tables with title, size, licence flag and a sha256 of each file.

```
main/            T5 ... T11         Tables 5 to 11 of the paper (Tables 1 to 4, in the Methods, are descriptive and not released as files)
supplementary/   S1 ... S49        supplementary tables, numbered in the order in which the paper first cites them
INDEX.csv        id, file, title, where the paper uses it, rows, columns, licence flag, sha256
```

## Numbering
Supplementary tables are numbered S1, S2, S3 ... by first citation in the Methods and Results.
S1 to S6 describe which metric can be tested in which experiment and why.

## Conventions
* `applicability_status` says whether a metric can be tested in an experiment (`OK`, `GLOBAL`, `REF`, `OK-KNOCKON`,
  `OK-PROVISIONAL`) or why not (`X-ARM`, `X-NOINPUT`, `X-BOOKKEEP`, `X-UNDEF-COV`, `X-WITHDRAWN`, `X-NOCTRL`,
  `X-CONFOUND`, `NOT-RUN`, `DUP`); the Supplementary PDF explains each.
* `lesion_test` is `catalytic lesion`, `second-shell lesion` or `deformation` (an experiment that could not be used).
* `mode` and `valid_modes` are `structure-space` or `prediction-based`.
* Result tables carry the same columns for traceability of a row to its denominator: `claim_type`, `unit`, `n_units`,
  `n_clusters`, `cluster_def`, `k`, `N`, `k_of_N`, `denominator_def`, `headline_ok`, `status`, `licence_flag`.
* Pointers into the private project (file paths, hashes, internal ids) are not part of the public tables.

## Licence
Tables flagged `D2DCure_aggregate` in `INDEX.csv` (T8, S12, S16, S17, S18, S19) are aggregates of D2DCure BglB data, whose licence is
unstated. They contain no per-variant row. Check the licence before redistributing them.

## Integrity
`sha256` in `INDEX.csv` is the hash of each file as released.
