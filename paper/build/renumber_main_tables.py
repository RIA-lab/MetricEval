#!/usr/bin/env python3
"""One-time renumbering of the main-text tables.

Section 2 (Methods) now has Tables 1 to 4, so the tables of the Results move up:
Results Tables 3 to 9 become 5 to 11 and the Discussion's Table 10 becomes 12.
This script rewrites the table numbers in the text that names them:

  * "Table 7", "Tables 3 and 4", "Tables 3 to 9", "Tables 8, 9 and S29" (digits 3 to 10 only;
    S numbers, equation numbers and the new Methods tables 1 and 2 are not touched);
  * "Source: main/T3_dead_vs_active.csv." in the Results captions;

in the four Markdown files and in the prose strings of the build files that describe
the tables (supplement_spec.py, build_supplement.py). Keys that name the private source
tables (T3 ... T9 in tables/main, rank_in_table_5 ...) are not text and are edited by hand.

    python3 renumber_main_tables.py            # dry run: list the changes
    python3 renumber_main_tables.py --apply    # rewrite the files (once)

Run it before the new Methods captions (Tables 1 to 4) are written.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
MAP = {3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11, 10: 12}
FILES = [PAPER / n for n in ("introduction.md", "methods.md", "results.md", "discussion.md")] + \
        [HERE / n for n in ("supplement_spec.py", "build_supplement.py")]
DONE = HERE / ".renumber_main_tables.done"

RUN_RE = re.compile(r"\b(Tables?) ((?:\d+|S\d+)(?:(?:, and |, | and | to |–)(?:\d+|S\d+))*)")
NUM_RE = re.compile(r"(?<![\w.])\d+(?![\w.])")
SRC_RE = re.compile(r"(Source: main/T)(\d)(_)")


def renum_run(m):
    body = NUM_RE.sub(lambda n: str(MAP.get(int(n.group(0)), int(n.group(0)))), m.group(2))
    # a token like S29 must stay: NUM_RE does not match digits glued to a letter
    return f"{m.group(1)} {body}"


def renum(text):
    text = RUN_RE.sub(renum_run, text)
    return SRC_RE.sub(lambda m: m.group(1) + str(MAP.get(int(m.group(2)), int(m.group(2)))) + m.group(3), text)


def main():
    apply = "--apply" in sys.argv
    if apply and DONE.exists():
        sys.exit("already applied; delete .renumber_main_tables.done only if you restored the old numbers")
    total = 0
    for f in FILES:
        old = f.read_text(encoding="utf-8")
        new = renum(old)
        if new == old:
            continue
        ol, nl = old.split("\n"), new.split("\n")
        changes = [(a, b) for a, b in zip(ol, nl) if a != b]
        total += len(changes)
        print(f"{f.name}: {len(changes)} lines")
        if not apply:
            for a, b in changes[:400]:
                for ma, mb in zip(re.finditer(r"Tables? [^.;)\n]{1,40}|Source: main/T\d_", a),
                                  re.finditer(r"Tables? [^.;)\n]{1,40}|Source: main/T\d_", b)):
                    if ma.group(0) != mb.group(0):
                        print(f"   {ma.group(0)!r} -> {mb.group(0)!r}")
        else:
            f.write_text(new, encoding="utf-8")
    print(f"{total} lines {'rewritten' if apply else 'would change'}")
    if apply:
        DONE.write_text("applied\n")


if __name__ == "__main__":
    main()
