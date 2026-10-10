#!/usr/bin/env python3
"""Build paper/supplementary.md and paper/supplementary.pdf.

The Supplementary PDF does not reprint the tables. For every table it gives the
path of the CSV in the released directory, its size, what a row is, what the key
columns mean, a three-row excerpt, where the paper cites it, and caveats. The
descriptions are in supplement_spec.py; sizes, excerpts and citations are read
from the released CSV files and from the Markdown sources, so they cannot drift.
Paths are given relative to the released directory (main/..., supplementary/...).

    python3 build_supplement.py            # writes ../supplementary.md and ../supplementary.pdf
    python3 build_supplement.py --check    # validate the spec against the CSV files only

Page numbers (table of contents, links from the paper) need two passes; the
script repeats until they are stable. Links into the paper use paper_pages.json,
which build_pdf.py writes.
"""
import csv
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

from common import (HERE, LINK_HOST, PAPER, TABLES, link_ids, page_texts, pandoc_html, print_pdf,
                    relativize_links)
import supplement_spec as spec

PUBLIC = TABLES / "public"
OUT_MD = PAPER / "supplementary.md"
OUT_PDF = PAPER / "supplementary.pdf"
OUT_HTML = HERE / "supplementary.html"
SUPP_PAGES = HERE / "supplement_pages.json"
PAPER_PAGES = HERE / "paper_pages.json"
DOCS = [("methods.md", "Methods"), ("results.md", "Results"), ("discussion.md", "Discussion")]
PROV = ["claim_type", "unit", "n_units", "n_clusters", "cluster_def", "k", "N", "k_of_N",
        "denominator_def", "headline_ok", "status", "licence_flag"]
csv.field_size_limit(10**9)


class IdMap(dict):
    """{S17c} in the spec text -> the new number."""
    def __missing__(self, key):
        raise KeyError(f"unknown table id in spec text: {{{key}}}")


def load():
    ids = {r["old_id"]: r["new_id"] for r in csv.DictReader(open(HERE / "table_ids.csv", encoding="utf-8"))}
    index = OrderedDict((r["public_id"], r) for r in csv.DictReader(open(PUBLIC / "INDEX.csv", encoding="utf-8")))
    return ids, index


def read_csv(rel):
    with open(PUBLIC / rel, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows


# ---------------------------------------------------------------- validation
def validate(ids, index):
    problems = []
    fx = IdMap(ids)
    for old, new in ids.items():
        if old not in spec.TABLES:
            problems.append(f"{old}: no description in supplement_spec.py")
            continue
        sp = spec.TABLES[old]
        row = index[new]
        header = list(read_csv(row["file"])[0].keys())
        if len(header) != int(row["columns"]):
            problems.append(f"{new}: column count differs from INDEX")
        for name, _ in sp["columns"]:
            for tok in name.split(" / "):
                tok = tok.strip()
                if (re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", tok) and not tok.endswith("_") and tok not in header):
                    problems.append(f"{new}: documented column '{tok}' not in the CSV")
        for c in sp.get("excerpt", []):
            if c not in header:
                problems.append(f"{new}: excerpt column '{c}' not in the CSV")
        for c in sp.get("where", {}):
            if c not in header:
                problems.append(f"{new}: filter column '{c}' not in the CSV")
        for field in ("title", "contents", "row", "supports"):
            try:
                sp[field].format_map(fx)
            except KeyError as e:
                problems.append(f"{new}: {e}")
        for _, meaning in sp["columns"]:
            try:
                meaning.format_map(fx)
            except KeyError as e:
                problems.append(f"{new}: {e}")
        for note in sp.get("notes", []):
            try:
                note.format_map(fx)
            except KeyError as e:
                problems.append(f"{new}: {e}")
    return problems


# ---------------------------------------------------------------- citations
def cited_in(ids):
    """new id -> {doc label: [section numbers]} read from the Markdown sources."""
    out = {new: OrderedDict() for new in ids.values()}
    for fname, label in DOCS:
        text = (PAPER / fname).read_text(encoding="utf-8")
        text = re.sub(r"<!--.*?-->", lambda m: " " * len(m.group(0)), text, flags=re.S)
        sec = None
        for line in text.split("\n"):
            h = re.match(r"^#{1,4} (\d+(?:\.\d+)*)\b", line)
            if h:
                sec = h.group(1)
            for m in re.finditer(r"(?<![\w/.#-])S(\d{1,2})(?![\w-])", line):
                key = f"S{m.group(1)}"
                if key in out and sec:
                    lst = out[key].setdefault(label, [])
                    if sec not in lst:
                        lst.append(sec)
    return out


def cited_text(cites, paper_pages):
    parts = []
    for label, secs in cites.items():
        secs = sorted(secs, key=lambda s: [int(x) for x in s.split(".")])
        shown = []
        for s in secs:
            page = paper_pages.get(s)
            shown.append(f"[{s}]({LINK_HOST}paper.pdf#page={page})" if page and label != "Discussion" else s)
        parts.append(f"{label} " + ", ".join(shown) if label != "Discussion" else "Discussion")
    return "; ".join(parts) if parts else "not cited in the main text"


# ---------------------------------------------------------------- rendering
def clean(v, width=34):
    v = v.replace("\n", " ").replace("`", "'").replace("|", "/").strip()
    if re.fullmatch(r"-?\d+\.\d{7,}", v):
        v = f"{float(v):.4f}".rstrip("0").rstrip(".")
    return v if len(v) <= width else v[: width - 1] + "…"


def code_names(names):
    return " / ".join(f"`{t.strip()}`" if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", t.strip()) else t.strip()
                      for t in names.split(" / "))


def pipe_table(header, rows, widths):
    dashes = ["-" * max(3, int(w * 10)) for w in widths]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(dashes) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines)


def entry_md(old, new, sp, row, cites, paper_pages, fx):
    data = read_csv(row["file"])
    header = list(data[0].keys())
    n_prov = sum(c in header for c in PROV)
    lic = row["licence_flag"]
    lic_txt = ("public" if lic == "public"
               else "D2DCure aggregate (licence of the source data unstated; aggregates only, no per-variant rows)")
    md = [f"### Table {new}. {sp['title'].format_map(fx)} {{#{new}}}", ""]
    meta = [f"**File.** `{row['file']}` · {int(row['rows']):,} rows × {row['columns']} columns · {lic_txt}",
            f"**Supports.** {sp['supports'].format_map(fx)}. **Cited in.** {cited_text(cites, paper_pages)}.",
            f"**A row is** {sp['row'].format_map(fx)}."]
    md += ["::: {.tmeta}", "", "\n\n".join(meta), "", ":::", "", sp["contents"].format_map(fx), ""]
    md += ["**Key columns.**", "", "::: {.defs}", "",
           pipe_table(["Column", "Meaning"],
                      [[code_names(n), m.format_map(fx)] for n, m in sp["columns"]], [3.2, 7.8]),
           "", ":::", ""]
    if n_prov >= 10:
        md += [f"The shared block of {n_prov} provenance columns (see Conventions) is also present and is not repeated above.", ""]
    ex = sp.get("excerpt")
    if ex:
        where = sp.get("where", {})
        sel = [r for r in data if all(r.get(c) == v for c, v in where.items())] or data
        note = "first 3 rows" + (" where " + ", ".join(f"{c} = {v}" for c, v in where.items()) if where else "")
        md += [f"**Excerpt** ({note}).", "", "::: {.excerpt}", "",
               pipe_table([f"`{c}`" for c in ex], [[f"`{clean(r[c]) or ' '}`" for c in ex] for r in sel[:3]],
                          [1] * len(ex)), "", ":::", ""]
    notes = [n.format_map(fx) for n in sp.get("notes", [])]
    if notes:
        md += ["**Notes.**", ""] + [f"- {n}" for n in notes] + [""]
    return "\n".join(md)


def front_matter(ids, index, fx):
    n_supp = sum(r["kind"] == "supplementary" for r in index.values())
    s03, s02, a3, a5 = ids["S03"], ids["S02"], ids["A3"], ids["A5"]
    return f"""<div class="title-block"><h1 class="doc-title">[Title]</h1><div class="subtitle">Supplementary Information</div></div>

# 1 About these tables

This document describes the {n_supp} supplementary tables (S1 to S{n_supp}) and the nine main-text tables (T1 to T9) of the paper. It does not reprint them. Every table is released as a CSV file; each entry below gives the path, the number of rows and columns, what a row is, what the key columns mean, a three-row excerpt, the places in the paper that cite the table, and caveats. Supplementary tables are numbered in the order in which the Methods and Results first cite them.

```
README.md          what is released, what was changed, licence
INDEX.csv          one row per table: id, file, title, rows, columns, licence flag, sha256
main/              T1 ... T9     Tables 1 to 9 of the paper
supplementary/     S1 ... S{n_supp}    supplementary tables, one CSV per table
```

**How to read an entry.** *File* is the path of the CSV, its size and its licence flag. *Supports* is the part of the paper the table backs. *Cited in* lists the sections of the Methods, Results and Discussion that cite it (a link opens the paper at that section). *A row is* says what one row represents. *Key columns* explains the columns that matter; the shared provenance block (below) is not repeated. The *excerpt* shows real rows from the file.

# 2 Conventions shared by the tables

**Shared provenance columns.** The result tables (T3 to T9 and the supplementary tables whose entry says so) carry the same block of up to 12 columns, so that a row can be traced to its denominator: `claim_type`, `unit` and `n_units` (what was counted and how many), `n_clusters` and `cluster_def` (the resampling unit: enzyme sub-subclass for natural enzymes, campaign and plate well or backbone cluster for designs, position for BglB), `k`, `N` and `k_of_N` (a count with its denominator), `denominator_def`, `headline_ok` (1 if the row may be quoted as a headline result; 0 for per-metric detail, descriptive analyses, reference rows and wrong-ligand AUROCs), `status` and `licence_flag`.

**Claim types.** `detection` (can the metric see damage), `specificity` (catalytic against matched control), `equivalence` (panel ratio against 1), `discrimination` (a real contrast, dead against active), `ranking` (against a measured label), `enrichment`, `baseline` (a reference row), `design`, `audit`, `not_measurable`.

**Applicability status** (in {a3}, {s02} and the `applicability_status` columns). `OK` can be tested; `OK-KNOCKON` tested but reported as displacement of the other catalytic residues, with no specificity verdict; `OK-PROVISIONAL` the raw status of the interface terms in the re-predicted ladder, resolved by testability; `GLOBAL` tested but has no site input, so it is a comparator; `REF` a fixed reference row; `X-BOOKKEEP` a counter or constant; `X-NOINPUT` the input cannot reach the changed quantity; `X-ARM` the metric belongs to the other kind (structure space or prediction) than the test; `X-UNDEF-COV` defined on too few units; `X-WITHDRAWN` the test was withdrawn; `X-NOCTRL` no matched control exists; `X-CONFOUND` the control is confounded; `NOT-RUN`; `DUP` identical to another test and read once.

**Verdicts in the specificity tables.** `specific` (response significant, interval of the specificity ratio above 1, control adequate); `non_specific` (responds, not more than the control); `blind` (does not respond); `invariant` (does not change); and counts-floor labels for cells with too few units.

**Names that recur.** `canonical_key` is the distinct metric after literal aliases are merged (`metric_name` may be an alias); `in_main_set` is 1 for the 33 reported metrics; `role` is `main`, `reference` or a supplement role (see {a5}); `source` is structure-space, prediction-based, PLACER, baseline, natural or denovo as the table says; `lesion_test` is the catalytic lesion or the second-shell lesion; `level` or `lesion_step` is the lesion step (isosteric 15.3, non-isosteric 36.4, Ala 53.2, Gly 80.5 Å³ median side-chain volume change; `second_shell_1/2/4` is the second-shell dose); `ame_flavour` is `crystal` (against the deposited structure) or `self_design` (against a design's own model) and the two are never pooled; `sr_*` is a specificity ratio with its interval; `auroc` is direction-free unless a column says `signed` or `directed`; `rho` is a Spearman correlation.

**Test names.** Tables that refer to a test use the names of {s03}, a name followed by its class in square brackets, for example `main set [catalytic lesion, structure-space]`.

**Licence.** Tables flagged `D2DCure_aggregate` in `INDEX.csv` are built from the D2DCure BglB data, whose licence is unstated; they hold metric-level aggregates only, no per-variant row. All other tables are `public`.

**Reproducibility.** The tables were generated by script from result files with seeds and input hashes recorded; `INDEX.csv` gives the sha256 of every released file.
"""


LOOKUP = [
    ("Which 33 metrics are reported, and why the rest are not", "{A5}, {S01}; then {A3} and {S02} for the reason in each test"),
    ("What a metric reads, and over which residues it is scored", "{S01}"),
    ("The 30 tests, with comparator, control type and role", "{S03}"),
    ("The specificity ratio of one metric at one lesion step", "{S04a} (comparators: {S04b})"),
    ("Whether the controls were good", "{S06a}, {S06b} (structure space); {S16a}, {S16b}, {S16c}, {S16d}, {S16e} (predictor ladder)"),
    ("How fragile the structure-space specificity result is", "{S10}, {S11}, {S28}"),
    ("How a metric responds to the substrate swap, and the role of ligand size", "Table 5, {S14}, {S14b}"),
    ("The distance control for the interface terms", "Table 8, {S29}, {S16a}, {S16b}, {S16c}, {S16d}"),
    ("Every metric on the 21-pair evaluation set (complete Table 3)", "{S17c}"),
    ("Every metric on the 192 plated designs, active against no active (complete Table 4)", "{S17d}"),
    ("Every quantity analysed on the 432 BglB variants (complete Table 6)", "{S20c}"),
    ("Every metric on the 16 plated designs with a measured activity (complete Table 7)", "{S22c}"),
    ("Hits per plate when a metric fills a 96-well plate", "{S22d}"),
    ("The wider set of 49 pairs, the 28 re-predicted pairs, the pair-set definitions", "{S17}, {S18}, {S17b}"),
    ("BglB: every metric, prediction-based metrics, sensitivity analyses", "{S20a}, {S21}, {S20b}"),
    ("Plated designs: enrichment and ordering for every metric", "{S22a}, {S23}, {S22b}"),
    ("The reference rows (resolution, length, tyrosine fraction, distance)", "{S24}"),
    ("Experiments that could not be made", "{S08}, {S13}"),
]

MAIN_MORE = {
    "T1": "{S03}", "T2": "{S03}, {S17b}", "T3": "{S17c}, {S17}, {S18}", "T4": "{S17d}",
    "T5": "{S14}, {S14b}", "T6": "{S20c}, {S20a}, {S20b}, {S21}", "T7": "{S22c}, {S22d}, {S22a}, {S22b}, {S23}",
    "T8": "{S26}, {S28}, {S29}", "T9": "{S27}, {S28}",
}

DATA_NOTES = [
    "Two sets of numbers for natural enzymes in the substrate swap: {S14} uses all 59 natural enzymes, Table 5 uses the evaluation set of 55.",
    "Two forms of the rank statistic R: {S12} is R on the 143 main enzymes with 90% intervals; Table 8 and {S26} are the pooled analysis on 195 enzymes with 95% intervals and the counted-step rule. Values for the same metric differ.",
    "Among the 29 prediction-based metrics of the ladder with ligand-distance-matched controls, the cells of {A3} keep the label NOT-RUN although the analysis was carried out (results in {S16c} and {S16d}).",
]


def back_matter(ids, index, fx, paper_pages):
    md = ["# Appendix A. Main-text tables", "",
          "The nine tables of the paper, with the supplementary tables that hold the complete version or more detail.", ""]
    rows = []
    for tid in [f"T{i}" for i in range(1, 10)]:
        r = index[tid]
        rows.append([f"**{tid}**", f"`{r['file']}`", f"{int(r['rows'])} × {r['columns']}",
                     MAIN_MORE[tid].format_map(fx)])
    md += [pipe_table(["Table", "File", "Rows × columns", "More detail in"], rows, [1, 6, 1.6, 3]), ""]
    md += ["# Appendix B. Notes on the data", ""]
    md += [f"- {n.format_map(fx)}" for n in DATA_NOTES]
    return "\n".join(md)


def render(ids, index, supp_pages, paper_pages, latex=False):
    """latex=True: no page numbers (they belong to the HTML-printed PDF) and no links into the paper."""
    if latex:
        supp_pages, paper_pages = {}, {}
    fx = IdMap(ids)
    rev = {new: old for old, new in ids.items()}
    cites = cited_in(ids)
    parts = [front_matter(ids, index, fx)]

    lookup = pipe_table(["I want to know", "Go to"],
                        [[q, a.format_map(fx)] for q, a in LOOKUP], [6, 5])
    parts.append("# 3 Where do I find ...?\n\n::: {.defs}\n\n" + lookup + "\n\n:::\n")

    toc_rows = []
    for new in sorted((k for k in index if index[k]["kind"] == "supplementary"), key=lambda k: int(k[1:])):
        r = index[new]
        page = supp_pages.get(new, "")
        row = [f"[{new}](#{new})", r["title"], r["topic"], f"{int(r['rows']):,} × {r['columns']}"]
        toc_rows.append(row if latex else row + [str(page)])
    toc_head, toc_w = (["Table", "Title", "Topic", "Rows × cols"], [0.9, 6.2, 2.4, 1.5]) if latex else \
        (["Table", "Title", "Topic", "Rows × cols", "Page"], [0.9, 6.2, 2.4, 1.5, 0.7])
    parts.append("# 4 Table of contents\n\n::: {.defs .toc}\n\n" + pipe_table(toc_head, toc_rows, toc_w) + "\n\n:::\n")

    parts.append("# 5 Supplementary tables\n")
    for new in sorted((k for k in index if index[k]["kind"] == "supplementary"), key=lambda k: int(k[1:])):
        old = rev[new]
        parts.append(entry_md(old, new, spec.TABLES[old], index[new], cites[new], paper_pages, fx))
    parts.append(back_matter(ids, index, fx, paper_pages))

    md = "\n\n".join(parts)

    def href(n):
        return f"#S{n}" if n <= len(ids) else None

    return link_ids(md, href)


def find_pages(pdf, ids):
    texts = page_texts(pdf)
    pages = {}
    for new in ids.values():
        pat = re.compile(r"^\s*Table " + re.escape(new) + r"\. ", re.M)
        for i, t in enumerate(texts, 1):
            if pat.search(t):
                pages[new] = i
                break
    return pages, len(texts)


def main():
    ids, index = load()
    problems = validate(ids, index)
    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"spec validated against {len(ids)} public tables")
    if "--check" in sys.argv:
        return

    paper_pages = json.loads(PAPER_PAGES.read_text()) if PAPER_PAGES.exists() else {}
    supp_pages = json.loads(SUPP_PAGES.read_text()) if SUPP_PAGES.exists() else {}
    for attempt in range(1, 5):
        OUT_MD.write_text(render(ids, index, supp_pages, paper_pages) + "\n", encoding="utf-8")
        pandoc_html(OUT_MD, OUT_HTML, HERE / "template_supplement.html", "MetricEval: Supplementary Information")
        errs = print_pdf(OUT_HTML, OUT_PDF)
        relativize_links(OUT_PDF)
        new_pages, n_pages = find_pages(OUT_PDF, ids)
        if new_pages == supp_pages:
            break
        supp_pages = new_pages
    SUPP_PAGES.write_text(json.dumps(supp_pages, indent=1), encoding="utf-8")
    missing = [n for n in ids.values() if n not in supp_pages]
    print(f"wrote {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KiB, {n_pages} pages), "
          f"passes: {attempt}, tables located: {len(supp_pages)}/{len(ids)}")
    if missing or errs:
        sys.exit(f"missing entries in the PDF: {missing}; KaTeX errors: {errs}")


if __name__ == "__main__":
    main()
