#!/usr/bin/env python3
"""Structural checks of the Markdown sources and of the public tables.

  * methods.md has no "→ Results", Box, Limits paragraph or Illustration paragraph;
  * the table captions of Methods, Results and Discussion are numbered 1, 2, 3 ... once each, in order;
  * every "Table n" in the text names an existing caption, every S number exists;
  * the supplementary tables are numbered in the order of first citation (Introduction, Methods,
    Results, Discussion), and every one is cited;
  * every reference of a section's list is cited in that section;
  * tables/public/main holds T5 ... T11 and the file names match the captions' Source lines.

Exit status 1 and a list of problems if anything fails.

    python3 check_structure.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
PUBLIC = PAPER.parent / "tables" / "public"
DOCS = ["introduction.md", "methods.md", "results.md", "discussion.md"]
COMMENT = re.compile(r"<!--.*?-->", re.S)


def visible(name):
    return COMMENT.sub(lambda m: " " * len(m.group(0)), (PAPER / name).read_text(encoding="utf-8"))


def main():
    problems = []
    text = {n: visible(n) for n in DOCS}

    m = text["methods.md"]
    for pat, label in [(r"→ Results", "'→ Results' in a heading"), (r"\bBox \d", "a Box"), (r"^\*\*Limits", "a Limits paragraph"),
                       (r"^\*\*Illustration", "an Illustration paragraph"), (r"Figure 1", "Figure 1")]:
        if re.search(pat, m, re.M):
            problems.append(f"methods.md contains {label}")

    # captions
    caps = []
    for n in DOCS:
        for mm in re.finditer(r"^\*\*Table (\d+)\.", text[n], re.M):
            caps.append((int(mm.group(1)), n))
    nums = [c for c, _ in caps]
    if nums != list(range(1, len(nums) + 1)):
        problems.append(f"table captions are not 1..n once each in order: {caps}")
    n_tables = len(nums)

    # mentions of tables
    run = re.compile(r"\b(Tables?) ((?:\d+|S\d+)(?:(?:, and |, | and | to |–)(?:\d+|S\d+))*)")
    for n in DOCS:
        for mm in run.finditer(text[n]):
            body = mm.group(2) if mm.group(1) == "Tables" else re.match(r"\w+", mm.group(2)).group(0)
            for d in re.findall(r"(?<![\w.])\d+(?![\w.])", body):
                if int(d) > n_tables:
                    problems.append(f"{n}: 'Table {d}' but only {n_tables} tables have a caption")

    # supplementary tables
    cur = re.compile(r"(?<![\w/.-])S(\d{1,2})(?![\w-])")
    order = []
    for n in DOCS:
        for mm in cur.finditer(text[n]):
            s = int(mm.group(1))
            if s not in order:
                order.append(s)
    n_supp = len(list((PUBLIC / "supplementary").glob("S*.csv")))
    if order != list(range(1, n_supp + 1)):
        first_bad = next((i for i, (a, b) in enumerate(zip(order, range(1, n_supp + 1))) if a != b), None)
        problems.append(f"S numbers are not in first-citation order or not all cited (order starts {order[:12]}…; "
                        f"first mismatch at position {first_bad}; {len(order)} cited of {n_supp})")

    # references
    for n in ("methods.md", "results.md"):
        raw = (PAPER / n).read_text(encoding="utf-8")
        blk = re.search(r"<!--\s*refs:start\s*-->(.*?)<!--\s*refs:end\s*-->", raw, re.S)
        listed = {int(x) for x in re.findall(r"^\[(\d+)\]", blk.group(1), re.M)}
        body = COMMENT.sub(" ", raw[: blk.start()])
        body = re.sub(r"\$\$.*?\$\$|\$[^$\n]+?\$", " ", body, flags=re.S)
        cited = set()
        for mm in re.finditer(r"\[(\d+(?:,\s*\d+)*)\]", body):
            cited |= {int(x) for x in re.split(r",\s*", mm.group(1))}
        if listed - cited:
            problems.append(f"{n}: references listed but never cited: {sorted(listed - cited)}")
        if cited - listed:
            problems.append(f"{n}: citations without a reference: {sorted(cited - listed)}")

    # public main tables
    files = sorted(p.name for p in (PUBLIC / "main").glob("*.csv"))
    want = [f"T{i}_" for i in range(5, 12)]
    got = sorted(files, key=lambda f: int(re.match(r"T(\d+)_", f).group(1)))
    if [re.match(r"T\d+_", f).group(0) for f in got] != want:
        problems.append(f"tables/public/main holds {files}, expected T5 ... T11")
    for mm in re.finditer(r"Source: main/(T\d+_[\w]+\.csv)", text["results.md"]):
        if mm.group(1) not in files:
            problems.append(f"results.md cites main/{mm.group(1)}, which does not exist")

    if problems:
        print("\n".join(problems))
        return 1
    print(f"structure ok: {n_tables} table captions, {n_supp} supplementary tables in first-citation order, "
          f"{len(files)} main files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
