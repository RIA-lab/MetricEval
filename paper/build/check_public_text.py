#!/usr/bin/env python3
"""Fail if internal codes appear in public content.

Also checks the references between tables: no old table id (T1 to T4), no unresolved {placeholder},
no "Table N" beyond the paper's last numbered table, and every "S<n> (column <name>)" must name a
column of that supplementary table.

Scans, when present: the Markdown sources (visible text, HTML comments excluded),
the generated supplementary.md, every file in tables/public (file names, headers,
cells, README, INDEX), the text of paper.pdf and supplementary.pdf, and the
LaTeX files in paper/latex. Exit status 1 and a list of findings if anything
matches.

    python3 check_public_text.py [--quiet]
"""
import csv
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PUBLIC = PAPER.parent / "tables" / "public"
csv.field_size_limit(10**9)

PATTERNS = {
    "axis C/E/G": r"\b[Aa]xis[ _][CEG]\b|axis_[CEG]|_axis\b|\b[Aa]xes [CE]\b|\bC-axis\b|\b[CEG] axis\b",
    "Part 1/2": r"\bParts? ?[12]\b",
    "internal documents": r"PREREG|RESEARCH_PLAN|CLAUDE|REPORT_|REPORT\.md|PROVENANCE|rules\.json|scores\.parquet|ADDENDUM",
    "private paths": r"(?<![\w/.])(?:ops|results|src|data|chai_lab|tables)/[\w.*-]",
    "ruling / user": r"human ruling|\bruling\b|user's|at the user|user asked|\bAgent \d",
    "analysis codes": r"\bP(?:0b?|1|2K?E?S?|3[vV]2|3|5T2|5_1B|5|6(?:_m3)?)\b|\bD4(?:_\w+)?\b|P6_PLATES|\bN0\b|\bisoplacer\b",
    "mode codes": r"\bM[13]\b",
    "experiment labels": r"\b(?:1A|1B|2A|2B)\b",
    "rule codes": r"\bPC7\b|is_gold|blindness|blocked_on",
    "test classes": r"\b(?:spec_[CE]|ladder_m3|S_m3|real_m[13]|rank_m[13]|sanity_n0|placer_c|detection_dup)\b",
    "old column names": r"status_a3|a3_status|test_id|source_artifact|source_sha256|evidence_path|code_ref|system_table",
    "legacy": r"[Ll]egacy",
    "other internal terms": r"\bglossary\b|\bp0b\b|decision of",
    "X control": r"\bmatched X\b|\bX arm\b|\bX control\b",
}
COMPILED = {k: re.compile(v) for k, v in PATTERNS.items()}


def scan_text(label, text, findings):
    for name, rx in COMPILED.items():
        for m in rx.finditer(text):
            a = max(0, m.start() - 40)
            findings.append((name, label, text[a:m.end() + 30].replace("\n", " ")))


def md_visible(path):
    t = path.read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->", " ", t, flags=re.S)


TABLE_LAST = 11


def supp_headers():
    out = {}
    for p in (PUBLIC / "supplementary").glob("S*.csv"):
        m = re.match(r"(S\d+)_", p.name)
        with open(p, newline="", encoding="utf-8") as f:
            out[m.group(1)] = next(csv.reader(f))
    return out


def check_references(findings):
    """Pointers between the public tables and to the paper's tables must resolve."""
    if not PUBLIC.exists():
        return
    heads = supp_headers()
    cells = []
    for p in sorted(PUBLIC.rglob("*.csv")):
        rel = str(p.relative_to(PUBLIC))
        with open(p, newline="", encoding="utf-8") as f:
            rows = list(csv.reader(f))
        seen = set()
        for r in rows[1:]:
            for c in r:
                if c and c not in seen:
                    seen.add(c)
                    cells.append((rel, c))
    for rel, c in cells:
        for m in re.finditer(r"\bT([1-4])\b", c):
            findings.append(("stale table id", rel, c[max(0, m.start() - 40):m.end() + 30]))
        for m in re.finditer(r"\{\w+\}", c):
            findings.append(("unresolved placeholder", rel, c[max(0, m.start() - 40):m.end() + 30]))
        for m in re.finditer(r"\bTable (\d+)\b", c):
            if int(m.group(1)) > TABLE_LAST:
                findings.append(("table number out of range", rel, c[max(0, m.start() - 40):m.end() + 30]))
        for m in re.finditer(r"\b(S\d+) \(column (\w+)\)", c):
            if m.group(1) not in heads or m.group(2) not in heads[m.group(1)]:
                findings.append(("column not in the cited table", rel, m.group(0)))
    idx = PUBLIC / "INDEX.csv"
    if idx.exists():
        with open(idx, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                for k in ("title", "supports"):
                    for m in re.finditer(r"\{\w+\}", r[k]):
                        findings.append(("unresolved placeholder", "INDEX.csv", r[k][:80]))
                    for m in re.finditer(r"\bTable (\d+)\b", r[k]):
                        if int(m.group(1)) > TABLE_LAST:
                            findings.append(("table number out of range", "INDEX.csv", r[k][:80]))


def main():
    findings = []
    check_references(findings)
    for name in ("abstract.md", "introduction.md", "methods.md", "results.md", "discussion.md", "supplementary.md"):
        p = PAPER / name
        if p.exists():
            scan_text(name, md_visible(p), findings)
    if PUBLIC.exists():
        for p in sorted(PUBLIC.rglob("*")):
            if p.is_dir():
                continue
            rel = str(p.relative_to(PUBLIC))
            scan_text(f"{rel} (file name)", p.name, findings)
            if p.suffix == ".csv":
                with open(p, newline="", encoding="utf-8") as f:
                    rows = list(csv.reader(f))
                scan_text(f"{rel} (header)", " | ".join(rows[0]), findings)
                seen = set()
                for r in rows[1:]:
                    for c in r:
                        if c and c not in seen and not re.fullmatch(r"[-\d.eE+]+", c):
                            seen.add(c)
                            scan_text(rel, c, findings)
            elif p.suffix in (".md", ".txt"):
                scan_text(rel, p.read_text(encoding="utf-8"), findings)
    for pdf in ("paper.pdf", "supplementary.pdf"):
        p = PAPER / pdf
        if p.exists():
            txt = subprocess.run(["pdftotext", str(p), "-"], capture_output=True, text=True).stdout
            scan_text(pdf, txt, findings)
    tex = PAPER / "latex"
    if tex.exists():
        for p in sorted(tex.glob("*.tex")):
            scan_text(p.name, re.sub(r"(?m)^\s*%.*$", " ", p.read_text(encoding="utf-8")), findings)

    if not findings:
        print("no internal codes found")
        return 0
    by = Counter((n, l) for n, l, _ in findings)
    print(f"{len(findings)} findings")
    for (n, l), c in sorted(by.items(), key=lambda kv: (-kv[1], kv[0])):
        ex = next(e for nn, ll, e in findings if (nn, ll) == (n, l))
        print(f"  [{n}] {l}: {c}x  e.g. …{ex}…")
    return 1


if __name__ == "__main__":
    sys.exit(main())
