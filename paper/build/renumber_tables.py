#!/usr/bin/env python3
"""One-time renumbering of the supplementary tables by first citation.

Old ids (S01 ... S29 with letters, plus A3, A4, A5) become S1, S2, S3 ... in
the order in which they are first cited in Introduction, Methods, Results and
Discussion (HTML comments do not count). The mapping is written to
table_ids.csv, which make_public_tables.py and build_supplement.py read.

    python3 renumber_tables.py            # dry run: print the mapping
    python3 renumber_tables.py --apply    # also rewrite the Markdown files

Run it once. After it has run the Markdown files carry the new ids and the
frozen mapping lives in table_ids.csv.

    python3 renumber_tables.py --again           # dry run: first-citation order of the CURRENT S numbers
    python3 renumber_tables.py --again --apply   # renumber again after the text changed

--again is for when text edits have changed the order of first citation: it
maps the current S numbers to new ones in citation order, rewrites the Markdown
(ranges such as S2-S7 are expanded first and collapsed again) and the new_id
column of table_ids.csv. The old ids in table_ids.csv, which the build scripts
key on, do not change.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
TABLES = PAPER.parent / "tables"
DOCS = ["introduction.md", "methods.md", "results.md", "discussion.md"]

# Not released in tables/public/: working copies of S01/S03 and the GPU ledger.
NOT_PUBLIC = {"A1", "A2", "S25"}

ID_RE = re.compile(r"(?<![\w/.-])(S\d{2}[a-g]?|A[345])(?![\w-])")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# a run of ids separated by commas / "and", e.g. "Tables S6, S7 and S8"
LIST_RE = re.compile(r"\bS(\d+)(?:(?:, and |, | and )S\d+)+")


def public_old_ids():
    rows = list(csv.DictReader(open(TABLES / "INDEX.csv", encoding="utf-8")))
    return [r["table_id"] for r in rows
            if r["table_id"] not in NOT_PUBLIC and not r["table_id"].startswith("T")]


def first_citation_order(texts):
    order, where = [], {}
    for name in DOCS:
        t = texts[name]
        masked = COMMENT_RE.sub(lambda m: " " * len(m.group(0)), t)
        for m in ID_RE.finditer(masked):
            old = m.group(1)
            if old not in where:
                order.append(old)
                where[old] = f"{name}:{t.count(chr(10), 0, m.start()) + 1}"
    return order, where


def collapse_runs(text):
    """'Tables S6, S7 and S8' -> 'Tables S6-S8' (runs of three or more)."""
    def sub(m):
        s = m.group(0)
        nums = [int(x) for x in re.findall(r"S(\d+)", s)]
        seps = re.findall(r"(, and |, | and )(?=S)", s)
        out, i = [], 0
        while i < len(nums):
            j = i
            while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                j += 1
            if j - i >= 2:
                out.append(f"S{nums[i]}–S{nums[j]}")
            else:
                out.extend(f"S{n}" for n in nums[i:j + 1])
            i = j + 1
        if len(out) == len(nums):
            return s
        last = seps[-1] if seps else " and "
        last = " and " if last.strip(", ") == "and" else last
        return out[0] if len(out) == 1 else ", ".join(out[:-1]) + (last if len(out) > 1 else "") + out[-1]
    new = LIST_RE.sub(sub, text)
    # "Table S6-S8" -> "Tables S6-S8"
    return re.sub(r"\bTable (S\d+–S\d+)", r"Tables \1", new)


CUR_RE = re.compile(r"(?<![\w/.-])S(\d{1,2})(?![\w-])")
RANGE_RE = re.compile(r"\bS(\d+)–S(\d+)\b")


def expand_ranges(text):
    """'Tables S2–S7' -> 'Tables S2, S3, S4, S5, S6 and S7' (outside comments)."""
    def sub(m):
        a, b = int(m.group(1)), int(m.group(2))
        items = [f"S{i}" for i in range(a, b + 1)]
        return ", ".join(items[:-1]) + " and " + items[-1]
    parts, pos = [], 0
    for c in COMMENT_RE.finditer(text):
        parts.append(RANGE_RE.sub(sub, text[pos:c.start()]))
        parts.append(c.group(0))
        pos = c.end()
    parts.append(RANGE_RE.sub(sub, text[pos:]))
    return "".join(parts)


def again(apply):
    rows = list(csv.DictReader(open(HERE / "table_ids.csv", encoding="utf-8")))
    cur = {r["new_id"] for r in rows}
    texts = {n: expand_ranges((PAPER / n).read_text(encoding="utf-8")) for n in DOCS}
    order, where = [], {}
    for name in DOCS:
        t = texts[name]
        masked = COMMENT_RE.sub(lambda m: " " * len(m.group(0)), t)
        for m in CUR_RE.finditer(masked):
            sid = f"S{m.group(1)}"
            if sid in cur and sid not in where:
                order.append(sid)
                where[sid] = f"{name}:{t.count(chr(10), 0, m.start()) + 1}"
    order += sorted(cur - set(order), key=lambda x: int(x[1:]))
    mapping = {c: f"S{i}" for i, c in enumerate(order, 1)}
    moved = {c: n for c, n in mapping.items() if c != n}
    print(f"{len(order)} tables; {len(moved)} change number: " + ", ".join(f"{c}->{n}" for c, n in moved.items()))
    if not apply:
        return
    for name, t in texts.items():
        masked = COMMENT_RE.sub(lambda m: " " * len(m.group(0)), t)
        out, last = [], 0
        for m in CUR_RE.finditer(masked):
            sid = f"S{m.group(1)}"
            if sid in mapping:
                out.append(t[last:m.start()])
                out.append(mapping[sid])
                last = m.end()
        out.append(t[last:])
        new = "".join(out)
        parts, pos = [], 0
        for c in COMMENT_RE.finditer(new):
            parts.append(collapse_runs(new[pos:c.start()]))
            parts.append(c.group(0))
            pos = c.end()
        parts.append(collapse_runs(new[pos:]))
        (PAPER / name).write_text("".join(parts), encoding="utf-8")
    first = {mapping[c]: where.get(c, "uncited") for c in order}
    old_of = {r["new_id"]: r["old_id"] for r in rows}
    with open(HERE / "table_ids.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["old_id", "new_id", "first_cited"])
        for c in order:
            w.writerow([old_of[c], mapping[c], first[mapping[c]]])
    print("rewrote", ", ".join(DOCS), "and table_ids.csv")


def main():
    if "--again" in sys.argv:
        return again("--apply" in sys.argv)
    apply = "--apply" in sys.argv
    texts = {n: (PAPER / n).read_text(encoding="utf-8") for n in DOCS}
    public = public_old_ids()
    order, where = first_citation_order(texts)
    unknown = [o for o in order if o not in public]
    if unknown:
        sys.exit(f"cited but not public: {unknown}")
    uncited = [p for p in public if p not in order]
    order += uncited          # tables nobody cites follow in their old order
    mapping = {old: f"S{i}" for i, old in enumerate(order, 1)}

    with open(HERE / "table_ids.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["old_id", "new_id", "first_cited"])
        for old in order:
            w.writerow([old, mapping[old], where.get(old, "uncited")])
    print(f"{len(order)} public supplementary tables; uncited: {uncited or 'none'}")
    for old in order:
        print(f"  {old:5s} -> {mapping[old]:4s}  {where.get(old, 'uncited')}")

    if not apply:
        return
    for name, t in texts.items():
        masked = COMMENT_RE.sub(lambda m: " " * len(m.group(0)), t)
        out, last = [], 0
        for m in ID_RE.finditer(masked):
            out.append(t[last:m.start(1)])
            out.append(mapping[m.group(1)])
            last = m.end(1)
        out.append(t[last:])
        new = "".join(out)
        # visible source paths now point into the public directory
        new = new.replace("`tables/main/", "`tables/public/main/")
        # collapse runs only outside comments
        parts, pos = [], 0
        for c in COMMENT_RE.finditer(new):
            parts.append(collapse_runs(new[pos:c.start()]))
            parts.append(c.group(0))
            pos = c.end()
        parts.append(collapse_runs(new[pos:]))
        (PAPER / name).write_text("".join(parts), encoding="utf-8")
    print("rewrote", ", ".join(DOCS))


if __name__ == "__main__":
    main()
