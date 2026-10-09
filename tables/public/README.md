# tables/public: the tables released with the paper

9 main-text tables and 49 supplementary tables, as CSV (UTF-8, comma-separated, one header row).
The Supplementary PDF (`paper/supplementary.pdf`) describes every table: what a row is, what the columns
mean, which part of the paper uses it. `INDEX.csv` lists them all with a sha256 of each file.

```
main/            T1 ... T9   the paper's Tables 1 to 9 (the numbers of the paper)
supplementary/   S1 ... S49   supplementary tables, numbered in the order in which the Methods and Results first cite them
INDEX.csv        id, file, title, where the paper uses it, rows, columns, licence flag, sha256, id and file in tables/
```

## Numbering
Supplementary tables were renumbered S1, S2, S3 ... by first citation in the paper. `INDEX.csv` keeps the
id under which each table was generated (`source_id`, for example `S17c`) and its file in `tables/`.
SS2 to SS6 are the metric audit (the former A5, S01, A3, S02, A4 and S03).

## What was changed relative to `tables/`
* Files are renamed `S<n>_<name>.csv`; internal experiment labels (1A, 1B, 2A, 2B) are not used in the names.
* Column names `rank_in_table_5` / `in_table_5` (supplementary table for Table 6) and `rank_in_table_6` / `in_table_6`
  (for Table 7) are renamed to the paper's current numbers.
* References to other tables inside text cells (for example `see S17c`) are translated to the new numbers.
* S34 and S35 had a column name used twice (`n_clusters`, identical in every row); the second copy is removed.
* Nothing else is altered: values are as generated. `INDEX.csv` records, per table, whether anything was changed.
* Not released: the working copies A1 and A2 (S3 and S7 are their reader-facing versions) and the GPU ledger.

## Licence and caveats
* Tables flagged `D2DCure_aggregate` in `INDEX.csv` (T6, S13, S17, S18, S19, S20) are aggregates of D2DCure BglB data, whose licence is
  unstated. They contain no per-variant row. Check the licence before redistributing them.
* Columns named `source_artifact(s)`, `evidence_path`, `artifacts`, `system_table` and `code_ref` point into the private
  project (`results/...`, `data/...`, `src/...`) and do not resolve in this repository.
* Internal codes in some tables are explained in the Supplementary PDF (Conventions): `P2K`, `P1`, `P3v2` ... are analyses
  (translated in the PDF and in S7), `M1` is structure-space and `M3` prediction-based.
* `role = not_run` in S7 is stale for three experiments that were run (see the PDF).

## Integrity
`sha256` in `INDEX.csv` is the hash of the file as released; the hash of each source table was checked against
`tables/MANIFEST.json` before it was copied.
