#!/usr/bin/env python3
"""One-time shift of the Methods section numbers.

Section 2.1 is now the experiment overview, so the four tests move from 2.1-2.4 to
2.2-2.5 (and 2.1.1 -> 2.2.1, 2.3.2 -> 2.4.2, ...). This script rewrites every reference
to those sections:

  * methods.md: headings and cross-references ("as in 2.1", "(2.3.1; results in ...)");
  * results.md and discussion.md: "Methods 2.x" references;
  * supplement_spec.py: the section numbers on the `supports=` lines.

Only 2.1-2.4 with an optional .1/.2 are touched; decimals such as "2.5 Å", "2.73" and the
Introduction (where "2.4" is a number) are left alone.

    python3 renumber_methods_sections.py            # dry run
    python3 renumber_methods_sections.py --apply    # rewrite once
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
DONE = HERE / ".renumber_methods_sections.done"
SEC = re.compile(r"(?<![\d.])2\.([1-4])((?:\.[12])?)(?!\d)(?!\.\d)(?! ?Å)")
COMMENT = re.compile(r"<!--.*?-->", re.S)


def shift(text, only_lines=None):
    def sub(m):
        return f"2.{int(m.group(1)) + 1}{m.group(2)}"

    out = []
    for line in text.split("\n"):
        if only_lines is not None and only_lines not in line:
            out.append(line)
            continue
        # leave HTML comments (source notes) untouched
        parts, pos = [], 0
        for c in COMMENT.finditer(line):
            parts.append(SEC.sub(sub, line[pos:c.start()]))
            parts.append(c.group(0))
            pos = c.end()
        parts.append(SEC.sub(sub, line[pos:]))
        out.append("".join(parts))
    return "\n".join(out)


def main():
    apply = "--apply" in sys.argv
    if apply and DONE.exists():
        sys.exit("already applied")
    jobs = [(PAPER / "methods.md", None), (PAPER / "results.md", None), (PAPER / "discussion.md", None),
            (HERE / "supplement_spec.py", "supports=")]
    for f, only in jobs:
        old = f.read_text(encoding="utf-8")
        new = shift(old, only)
        changed = [(a, b) for a, b in zip(old.split("\n"), new.split("\n")) if a != b]
        print(f"{f.name}: {len(changed)} lines")
        if not apply:
            for a, b in changed:
                ma = SEC.findall(COMMENT.sub("", a))
                print("   ", [m[0] + m[1] for m in ma], "->", [f"{int(m[0]) + 1}{m[1]}" for m in ma])
        else:
            f.write_text(new, encoding="utf-8")
    if apply:
        DONE.write_text("applied\n")


if __name__ == "__main__":
    main()
