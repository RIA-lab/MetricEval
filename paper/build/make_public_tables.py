#!/usr/bin/env python3
"""Build tables/public/ (the releasable tables) from tables/.

  tables/public/main/T{n}_*.csv            tables 1 to 9 of the paper (the paper's numbering)
  tables/public/supplementary/S{n}_*.csv   supplementary tables, numbered by first citation
  tables/public/INDEX.csv                  id, old id, file, title, rows, columns, licence, sha256
  tables/public/README.md

Every source table is checked against the sha256 in tables/MANIFEST.json first.
Data are copied verbatim except for (a) the documented header fixes and (b)
cross-references to other tables inside text cells, which are translated to the
new numbers. Paths into the private project (source_artifacts etc.) are left as
they are. The mapping old id -> new id comes from table_ids.csv
(renumber_tables.py).

    python3 make_public_tables.py
"""
import csv
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import supplement_spec as spec  # noqa: E402

TABLES = HERE.parent.parent / "tables"
PUBLIC = TABLES / "public"
csv.field_size_limit(10**9)

HEADER_FIXES = {
    # the generator still names these columns after the old table numbers
    "S20c": {"rank_in_table_5": "rank_in_table_6", "in_table_5": "in_table_6"},
    "S22c": {"rank_in_table_6": "rank_in_table_7", "in_table_6": "in_table_7"},
}
CELL_FIXES = {  # (table, column, old text, new text)
    ("S22c", "cluster_def", "Table 6", "Table 7"),
    ("S22d", "cluster_def", "Table 6", "Table 7"),
}
PATH_COLUMNS = {
    "source_artifacts", "source_artifact", "artifacts", "evidence_path", "system_table", "code_ref",
    "source_original", "source_new", "source_sha256", "input_id", "base_system", "test_ids",
}
ID_RE = re.compile(r"(?<![\w/.-])(S\d{2}[a-g]?)(?![\w-])")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug_of(old_name):
    s = re.sub(r"^[AST]\d+[a-g]?_", "", old_name)
    s = re.sub(r"(part[12][AB]_)", "", s)
    return s


def main():
    ids = {r["old_id"]: r["new_id"] for r in csv.DictReader(open(HERE / "table_ids.csv", encoding="utf-8"))}
    index = {r["table_id"]: r for r in csv.DictReader(open(TABLES / "INDEX.csv", encoding="utf-8"))}
    manifest = json.load(open(TABLES / "MANIFEST.json", encoding="utf-8"))["outputs"]

    def tr_ids(text, table):
        text = text.replace("control quality in S06", "control quality in \x00")
        text = ID_RE.sub(lambda m: ids.get(m.group(1), m.group(1)), text)
        text = text.replace("\x00", ids["S06a"] + " and " + ids["S06b"])
        if table == "A4":
            text = re.sub(r"\bin A3\b", "in " + ids["A3"], text)
        return text

    if PUBLIC.exists():
        assert PUBLIC.resolve().parent == TABLES.resolve() and PUBLIC.name == "public"
        shutil.rmtree(PUBLIC)
    (PUBLIC / "main").mkdir(parents=True)
    (PUBLIC / "supplementary").mkdir()

    # ---- the tables to release, in order: T1..T9, then S1..S49
    jobs = [(t, t, "main") for t in [f"T{i}" for i in range(1, 10)]]
    jobs += [(old, new, "supplementary") for old, new in sorted(ids.items(), key=lambda kv: int(kv[1][1:]))]

    rows_out = []
    for old, new, kind in jobs:
        src_rel = index[old]["path"]
        src = TABLES.parent / src_rel
        if sha(src) != manifest[src_rel]:
            sys.exit(f"hash mismatch for {src_rel}")
        stem = Path(src_rel).stem
        if kind == "main":
            fname = f"{stem}.csv"
        else:
            fname = f"{new}_{slug_of(stem)}.csv"
        dst = PUBLIC / kind / fname

        with open(src, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        header, body = rows[0], rows[1:]
        changed = set()
        # a column name used twice (S34 and S35 repeat `n_clusters`) breaks most CSV readers;
        # drop the later copy, but only if it is identical in every row
        seen, drop = {}, []
        for j, h in enumerate(header):
            if h in seen:
                if any(r[j] != r[seen[h]] for r in body):
                    sys.exit(f"{old}: repeated column {h!r} differs between its copies")
                drop.append(j)
            else:
                seen[h] = j
        if drop:
            keep = [j for j in range(len(header)) if j not in drop]
            header = [header[j] for j in keep]
            body = [[r[j] for j in keep] for r in body]
            changed.add("repeated column removed")
        fixes = HEADER_FIXES.get(old, {})
        new_header = [fixes.get(h, h) for h in header]
        if fixes:
            changed.add("column names renumbered")
        for r in body:
            for j, (h, v) in enumerate(zip(header, r)):
                if h in PATH_COLUMNS or not v:
                    continue
                nv = tr_ids(v, old)
                for t, c, a, b in CELL_FIXES:
                    if t == old and c == h:
                        nv = nv.replace(a, b)
                if nv != v:
                    r[j] = nv
                    changed.add("cross-references renumbered")
        with open(dst, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(new_header)
            w.writerows(body)

        if kind == "main":
            title, supports, topic = index[old]["title"], f"Table {old[1:]} of the paper", "Main text"
        else:
            sp = spec.TABLES[old]
            title, supports, topic = sp["title"], sp["supports"], sp["topic"]
        rows_out.append({
            "public_id": new, "kind": kind, "file": f"{kind}/{fname}", "title": title,
            "supports": supports, "topic": topic, "rows": len(body), "columns": len(new_header),
            "licence_flag": index[old]["licence_flag"], "source_id": old, "source_file": src_rel,
            "changes_from_source": "; ".join(sorted(changed)) or "none",
            "sha256": sha(dst),
        })

    with open(PUBLIC / "INDEX.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows_out)

    n_main = sum(r["kind"] == "main" for r in rows_out)
    n_supp = len(rows_out) - n_main
    d2 = [r["public_id"] for r in rows_out if r["licence_flag"] != "public"]
    (PUBLIC / "README.md").write_text(README.format(
        n_main=n_main, n_supp=n_supp, d2=", ".join(d2),
        s_first=ids["A5"], s_last=ids["S03"]), encoding="utf-8")
    print(f"wrote {n_main} main + {n_supp} supplementary tables to {PUBLIC}")
    print("changed:", sum(r["changes_from_source"] != "none" for r in rows_out), "tables;",
          "D2DCure-flagged:", d2)


README = """# tables/public: the tables released with the paper

{n_main} main-text tables and {n_supp} supplementary tables, as CSV (UTF-8, comma-separated, one header row).
The Supplementary PDF (`paper/supplementary.pdf`) describes every table: what a row is, what the columns
mean, which part of the paper uses it. `INDEX.csv` lists them all with a sha256 of each file.

```
main/            T1 ... T9   the paper's Tables 1 to 9 (the numbers of the paper)
supplementary/   S1 ... S{n_supp}   supplementary tables, numbered in the order in which the Methods and Results first cite them
INDEX.csv        id, file, title, where the paper uses it, rows, columns, licence flag, sha256, id and file in tables/
```

## Numbering
Supplementary tables were renumbered S1, S2, S3 ... by first citation in the paper. `INDEX.csv` keeps the
id under which each table was generated (`source_id`, for example `S17c`) and its file in `tables/`.
{s_first} to {s_last} are the metric audit (the former A5, S01, A3, S02, A4 and S03).

## What was changed relative to `tables/`
* Files are renamed `S<n>_<name>.csv`; internal experiment labels (1A, 1B, 2A, 2B) are not used in the names.
* Column names `rank_in_table_5` / `in_table_5` (supplementary table for Table 6) and `rank_in_table_6` / `in_table_6`
  (for Table 7) are renamed to the paper's current numbers.
* References to other tables inside text cells (for example `see S17c`) are translated to the new numbers.
* S34 and S35 had a column name used twice (`n_clusters`, identical in every row); the second copy is removed.
* Nothing else is altered: values are as generated. `INDEX.csv` records, per table, whether anything was changed.
* Not released: the working copies A1 and A2 (S3 and S7 are their reader-facing versions) and the GPU ledger.

## Licence and caveats
* Tables flagged `D2DCure_aggregate` in `INDEX.csv` ({d2}) are aggregates of D2DCure BglB data, whose licence is
  unstated. They contain no per-variant row. Check the licence before redistributing them.
* Columns named `source_artifact(s)`, `evidence_path`, `artifacts`, `system_table` and `code_ref` point into the private
  project (`results/...`, `data/...`, `src/...`) and do not resolve in this repository.
* Internal codes in some tables are explained in the Supplementary PDF (Conventions): `P2K`, `P1`, `P3v2` ... are analyses
  (translated in the PDF and in S7), `M1` is structure-space and `M3` prediction-based.
* `role = not_run` in S7 is stale for three experiments that were run (see the PDF).

## Integrity
`sha256` in `INDEX.csv` is the hash of the file as released; the hash of each source table was checked against
`tables/MANIFEST.json` before it was copied.
"""

if __name__ == "__main__":
    main()
