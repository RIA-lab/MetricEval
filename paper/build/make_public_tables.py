#!/usr/bin/env python3
"""Build tables/public/ (the releasable tables) from tables/.

  tables/public/main/T{n}_*.csv            tables 1 to 9 of the paper (the paper's numbering)
  tables/public/supplementary/S{n}_*.csv   supplementary tables, numbered by first citation
  tables/public/INDEX.csv                  id, file, title, rows, columns, licence, sha256
  tables/public/README.md

Every source table is checked against the sha256 in tables/MANIFEST.json first.
Values and results are unchanged. What changes (rules in scrub_rules.py):
columns that only point into the private project are dropped; internal codes
(analysis, test and lesion codes) become the plain names used in the paper;
free text is reworded; cross-references between tables are renumbered.
The mapping old id -> new id comes from table_ids.csv (renumber_tables.py); the
full crosswalk (old ids, source files) is written to public_tables_crosswalk.csv
next to this script and is not released.

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
import scrub_rules as R  # noqa: E402
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
KEEP_VERBATIM = {"input_id", "prediction", "base_system", "canonical_key", "metric_name", "metric", "members", "rep_metric",
                 "alias_of", "item"}
ID_RE = re.compile(r"(?<![\w/.-])(S\d{2}[a-g]?)(?![\w-])")
CLAIM_RE = re.compile(r"^(P\w+?)_([CEG]):")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug_of(old_name):
    s = re.sub(r"^[AST]\d+[a-g]?_", "", old_name)
    return re.sub(r"(part[12][AB]_)", "", s)


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]


def scrub_cell(col, v):
    if not v:
        return v
    if v in R.TEXT_EXACT:
        return R.TEXT_EXACT[v]
    m = R.VALUE_MAPS.get(col)
    if m and v in m:
        return m[v]
    for pat, rep in R.TEXT_REGEX:
        v = pat.sub(rep, v)
    return v


def scrub_text(v):
    """Free text outside the tables (INDEX titles): the same replacements as for cells."""
    for pat, rep in R.TEXT_REGEX:
        v = pat.sub(rep, v)
    return v


def test_labels():
    """test_id -> unique readable label, from the (private) test inventory."""
    header, body = read(TABLES / "supp" / "S03_test_inventory.csv")
    ix = {h: i for i, h in enumerate(header)}
    labels = {}
    for r in body:
        name = scrub_cell("reader_name", r[ix["reader_name"]])
        labels[r[ix["test_id"]]] = R.test_label(name, r[ix["test_class"]])
    if len(set(labels.values())) != len(labels):
        dup = [v for v in labels.values() if list(labels.values()).count(v) > 1]
        sys.exit(f"test labels are not unique: {sorted(set(dup))}")
    return labels


def main():
    ids = {r["old_id"]: r["new_id"] for r in csv.DictReader(open(HERE / "table_ids.csv", encoding="utf-8"))}
    index = {r["table_id"]: r for r in csv.DictReader(open(TABLES / "INDEX.csv", encoding="utf-8"))}
    manifest = json.load(open(TABLES / "MANIFEST.json", encoding="utf-8"))["outputs"]
    labels = test_labels()

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

    jobs = [(t, t, "main") for t in [f"T{i}" for i in range(1, 10)]]
    jobs += [(old, new, "supplementary") for old, new in sorted(ids.items(), key=lambda kv: int(kv[1][1:]))]

    rows_out, cross = [], []
    for old, new, kind in jobs:
        src_rel = index[old]["path"]
        src = TABLES.parent / src_rel
        if sha(src) != manifest[src_rel]:
            sys.exit(f"hash mismatch for {src_rel}")
        stem = Path(src_rel).stem
        slug = R.FILE_SLUG.get(old)
        fname = f"{slug}.csv" if kind == "main" and slug else (f"{stem}.csv" if kind == "main" else f"{new}_{slug or slug_of(stem)}.csv")
        dst = PUBLIC / kind / fname

        header, body = read(src)
        changed = set()

        # a column name used twice breaks most CSV readers; drop the later copy if identical
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

        ix = {h: i for i, h in enumerate(header)}
        # a readable `test` column replaces the private test id where rows are per test
        if "test_id" in ix and old in ("A3", "S02", "S03"):
            pos = ix["test_id"]
            header = header[:pos] + ["test"] + header[pos + 1:]
            for r in body:
                r[pos] = labels[r[pos]]
            ix = {h: i for i, h in enumerate(header)}
        # the claim id of the restated counts becomes the name of the analysis
        if "claim_id" in ix:
            j = ix["claim_id"]
            for r in body:
                m = CLAIM_RE.match(r[j])
                if not m:
                    sys.exit(f"{old}: unexpected claim_id {r[j]!r}")
                r[j] = f"{R.ANALYSIS[m.group(1)]}; {R.LESION[m.group(2)]}"
        # test ids inside the status columns of the metric audit
        for col in ("v2b_status", "v2b_tests_ok"):
            if col in ix:
                j = ix[col]
                for r in body:
                    for k, v in R.SHORT_TEST.items():
                        r[j] = r[j].replace(k, v)

        drop_cols = {h for h in header if h in R.DROP_COLS and not (h == "test" )}
        drop_cols |= {h for (t, h) in R.DROP_TABLE_COLS if t == old and h in ix}
        keep = [j for j, h in enumerate(header) if h not in drop_cols]
        if len(keep) != len(header):
            changed.add("internal columns removed")
        header = [header[j] for j in keep]
        body = [[r[j] for j in keep] for r in body]

        fixes = HEADER_FIXES.get(old, {})
        new_header = []
        for h in header:
            h2 = fixes.get(h, h)
            h2 = R.TABLE_RENAME_COLS.get((old, h2), R.RENAME_COLS.get(h2, h2))
            h2 = re.sub(r"\bno reported activity\b", "no active", h2)
            new_header.append(h2)
        if new_header != header:
            changed.add("column names changed")
        if len(set(new_header)) != len(new_header):
            sys.exit(f"{old}: renaming produced duplicate columns: {new_header}")

        for r in body:
            for j, (h, nh) in enumerate(zip(header, new_header)):
                v = r[j]
                if not v or nh in KEEP_VERBATIM:
                    continue
                nv = tr_ids(v, old)
                for t, c, a, b in CELL_FIXES:
                    if t == old and c == h:
                        nv = nv.replace(a, b)
                nv = scrub_cell(nh, nv)
                if nv != v:
                    r[j] = nv
                    changed.add("codes and cross-references translated")

        # experiments that were run are labelled as run
        if old in ("S03", "T1"):
            fix, key = (R.ROLE_FIX, "reader_name") if old == "S03" else (R.T1_ROLE_FIX, "experiment")
            if key in new_header and "role" in new_header:
                ki, ri = new_header.index(key), new_header.index("role")
                for r in body:
                    if r[ki] in fix and r[ri] == "not_run":
                        r[ri] = fix[r[ki]]
                        changed.add("role corrected")

        with open(dst, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(new_header)
            w.writerows(body)

        if kind == "main":
            title = scrub_text(R.MAIN_TITLES.get(old, index[old]["title"]))
            supports, topic = f"Table {old[1:]} of the paper", "Main text"
        else:
            sp = spec.TABLES[old]
            title, supports, topic = sp["title"], sp["supports"], sp["topic"]
        rows_out.append({
            "public_id": new, "kind": kind, "file": f"{kind}/{fname}", "title": title,
            "supports": supports, "topic": topic, "rows": len(body), "columns": len(new_header),
            "licence_flag": index[old]["licence_flag"], "sha256": sha(dst),
        })
        cross.append({"public_id": new, "source_id": old, "source_file": src_rel,
                      "changes": "; ".join(sorted(changed)) or "none"})

    with open(PUBLIC / "INDEX.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(rows_out)
    with open(HERE / "public_tables_crosswalk.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(cross[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(cross)

    n_main = sum(r["kind"] == "main" for r in rows_out)
    n_supp = len(rows_out) - n_main
    d2 = [r["public_id"] for r in rows_out if r["licence_flag"] != "public"]
    (PUBLIC / "README.md").write_text(README.format(
        n_main=n_main, n_supp=n_supp, d2=", ".join(d2),
        a=ids["A5"], b=ids["S03"]), encoding="utf-8")
    print(f"wrote {n_main} main + {n_supp} supplementary tables to {PUBLIC}")
    print("changed:", sum(c["changes"] != "none" for c in cross), "tables;", "D2DCure-flagged:", d2)


README = """# Public tables

{n_main} main-text tables and {n_supp} supplementary tables of the paper, as CSV (UTF-8, comma-separated, one header row).
The Supplementary PDF describes every table: what a row is, what the columns mean and which part of the paper uses it.
`INDEX.csv` lists all tables with title, size, licence flag and a sha256 of each file.

```
main/            T1 ... T9          Tables 1 to 9 of the paper
supplementary/   S1 ... S{n_supp}        supplementary tables, numbered in the order in which the paper first cites them
INDEX.csv        id, file, title, where the paper uses it, rows, columns, licence flag, sha256
```

## Numbering
Supplementary tables are numbered S1, S2, S3 ... by first citation in the Methods and Results.
{a} to {b} describe which metric can be tested in which experiment and why.

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
Tables flagged `D2DCure_aggregate` in `INDEX.csv` ({d2}) are aggregates of D2DCure BglB data, whose licence is
unstated. They contain no per-variant row. Check the licence before redistributing them.

## Integrity
`sha256` in `INDEX.csv` is the hash of each file as released.
"""

if __name__ == "__main__":
    main()
