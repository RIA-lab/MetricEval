#!/usr/bin/env python3
"""Build paper/paper.pdf from the Markdown sections.

Included: Methods (2), Results (3) and one merged, globally numbered reference
list. Title, Abstract, 1 Introduction and 4 Discussion are reserved as empty
headings (see RESERVED below).

Pipeline: Markdown -> pandoc (HTML, KaTeX math) -> headless Chromium (PDF).

    npm install          # once, in this directory (installs KaTeX)
    python3 build_pdf.py # writes ../paper.pdf

Needs: pandoc, python3, and a Chromium/Chrome binary (set CHROME to override).
"""
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
OUT_PDF = PAPER / "paper.pdf"
OUT_HTML = HERE / "paper.html"
OUT_MD = HERE / "paper.build.md"

# Sections to include with their content, in paper order.
BODY_FILES = ["methods.md", "results.md"]

# Reserved sections: heading only, no body. (kind, heading text)
TITLE_PLACEHOLDER = "[Title]"

SENTENCE_PATCHES = [
    # The source files say their reference list is local to the section; in the
    # PDF there is one merged list.
    ("Numbers in square brackets are references (list at the end).",
     "Numbers in square brackets are references (see References)."),
    ("Numbers in square brackets are references, listed at the end of this section.",
     "Numbers in square brackets are references, listed in the References."),
]

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("google-chrome") or "",
]

MATH_RE = re.compile(r"\$\$.*?\$\$|(?<!\$)\$(?!\$)[^$\n]+?\$(?!\$)", re.S)
CITE_RE = re.compile(r"\[(\d+(?:,\s*\d+)*)\]")
REF_LINE_RE = re.compile(r"^\[(\d+)\]\s+(.*?)\s*<!--\s*bib:\s*(\S+)\s*-->\s*$")
REFS_BLOCK_RE = re.compile(r"<!--\s*refs:start\s*-->(.*?)<!--\s*refs:end\s*-->", re.S)
COLS_RE = re.compile(r"^<!--\s*cols:\s*([\d.,\s]+?)\s*-->$")


def split_refs(text, name):
    """Return (body without reference block, {local number: (key, text)})."""
    m = REFS_BLOCK_RE.search(text)
    if not m:
        sys.exit(f"{name}: no <!-- refs:start --> ... <!-- refs:end --> block")
    refs = {}
    for line in m.group(1).splitlines():
        r = REF_LINE_RE.match(line.strip())
        if r:
            refs[int(r.group(1))] = (r.group(3), r.group(2))
    if not refs:
        sys.exit(f"{name}: reference block has no parsable entries")
    return text[: m.start()] + text[m.end():], refs


LIST_ITEM_RE = re.compile(r"^\s*(?:[-*+]|\d+\.)\s")
TOP_MARK = "TOPCAPTIONMARK"   # caption that sits above its table (see fix_captions)
WIDE_COLS = 10         # tables with at least this many columns go on a landscape page


def space_lists(block):
    """Pandoc needs a blank line before a list; the source often has none."""
    out, prev = [], ""
    for line in block.split("\n"):
        if LIST_ITEM_RE.match(line) and prev.strip() and not LIST_ITEM_RE.match(prev) \
                and not prev.lstrip().startswith(("|", ">")) and not prev.startswith(" "):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def prepare_blocks(text):
    """Table widths from the `cols` hints, table captions, boxes, comment removal."""
    blocks = re.split(r"\n{2,}", text.strip("\n"))
    out = []
    hint = None
    for b in blocks:
        lines = b.split("\n")
        m = COLS_RE.match(lines[0].strip())
        if m:                       # `cols` hint: alone, or on the line above the table
            hint = [float(x) for x in m.group(1).split(",")]
            lines = lines[1:]
            if not lines:
                continue
            b = "\n".join(lines)
        if hint is not None and b.lstrip().startswith("|"):
            tbl = b.split("\n")
            ncol = tbl[0].strip().strip("|").count("|") + 1
            if len(hint) != ncol:
                sys.exit(f"cols hint {hint} does not match {ncol} columns: {tbl[0][:60]}")
            if ncol >= WIDE_COLS:   # keep headers such as "Rank in group" from breaking per letter
                hint = [max(w, 1.0) for w in hint]
            tbl[1] = "|" + "|".join("-" * max(3, round(w * 10)) for w in hint) + "|"
            b = "\n".join(tbl)
            hint = None
        out.append(b)

    def is_cap(b):
        return b.lstrip().startswith(("**Table ", "**Figure "))

    def ncols(tbl):
        return tbl.split("\n")[0].strip().strip("|").count("|") + 1

    final = []
    i = 0
    while i < len(out):
        b = out[i]
        s = b.lstrip()
        nxt = out[i + 1] if i + 1 < len(out) else ""
        if is_cap(b) and nxt.lstrip().startswith("|"):
            # caption above its table: make it the table's own <caption> (top)
            tbl, cap = nxt, f": {TOP_MARK} {b.strip()}"
            i += 2
        elif s.startswith("|"):
            # table; a following caption paragraph becomes its <caption> (bottom)
            tbl = b
            if i + 1 < len(out) and is_cap(nxt):
                cap = f": {nxt.strip()}"
                i += 2
            else:
                cap = ""
                i += 1
        else:
            if is_cap(b):      # a figure caption
                b = f"::: {{.caption}}\n{b}\n:::"
            elif s.startswith("**Box "):
                cls = "box keep-next" if nxt.lstrip().startswith("|") else "box"
                b = f"::: {{.{cls.replace(' ', ' .')}}}\n{b}\n:::"
            final.append(space_lists(b))
            i += 1
            continue
        unit = tbl + ("\n\n" + cap if cap else "")
        if ncols(tbl) >= WIDE_COLS:
            unit = f"::: landscape\n{unit}\n:::"
        final.append(unit)
    text = "\n\n".join(final)
    text = re.sub(r"[ \t]*<!--.*?-->", "", text, flags=re.S)  # src / bib notes
    return re.sub(r"\n{3,}", "\n\n", text)


def renumber(text, local, key_to_global, order):
    """Rewrite [n, m] citations from a section-local to the global numbering."""
    pieces = []
    last = 0
    for m in MATH_RE.finditer(text):
        pieces.append(("t", text[last:m.start()]))
        pieces.append(("m", m.group(0)))
        last = m.end()
    pieces.append(("t", text[last:]))

    def sub(m):
        nums = [int(x) for x in re.split(r",\s*", m.group(1))]
        gl = []
        for n in nums:
            if n not in local:
                sys.exit(f"citation [{n}] has no entry in this section's reference list")
            key = local[n][0]
            if key not in key_to_global:
                key_to_global[key] = len(key_to_global) + 1
                order.append((key, local[n][1]))
            gl.append(key_to_global[key])
        gl = sorted(set(gl))
        parts, k = [], 0
        while k < len(gl):  # collapse runs of three or more: 3-5
            j = k
            while j + 1 < len(gl) and gl[j + 1] == gl[j] + 1:
                j += 1
            if j - k >= 2:
                parts.append(f"{gl[k]}–{gl[j]}")
            else:
                parts.extend(str(x) for x in gl[k : j + 1])
            k = j + 1
        return "[" + ", ".join(parts) + "]"

    return "".join(CITE_RE.sub(sub, p) if kind == "t" else p for kind, p in pieces)


def reference_html(order):
    rows = []
    for n, (key, text) in enumerate(order, 1):
        esc = html.escape(text, quote=False)
        esc = re.sub(
            r"doi:(\S+)",
            lambda m: f'<a href="https://doi.org/{m.group(1)}">doi:{m.group(1)}</a>',
            esc,
        )
        rows.append(f'<div class="ref"><span class="refnum">[{n}]</span> {esc}</div>')
    return "\n".join(rows)


def check_bib(keys):
    bib = (PAPER / "references.bib").read_text(encoding="utf-8")
    missing = [k for k in keys if not re.search(r"@\w+\{" + re.escape(k) + r",", bib)]
    if missing:
        print(f"warning: not in references.bib: {missing}", file=sys.stderr)


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("no Chromium/Chrome found; set CHROME=/path/to/chrome")


def main():
    key_to_global, order = {}, []
    sections = []
    for name in BODY_FILES:
        raw = (PAPER / name).read_text(encoding="utf-8")
        body, local = split_refs(raw, name)
        for old, new in SENTENCE_PATCHES:
            body = body.replace(old, new)
        body = prepare_blocks(body)
        body = renumber(body, local, key_to_global, order)
        body = body.replace("](fig1_study_map.png)", "](../fig1_study_map.png)")
        sections.append(body)
    check_bib([k for k, _ in order])

    md = "\n\n".join(
        [
            f'<div class="title-block"><h1 class="doc-title">{TITLE_PLACEHOLDER}</h1></div>',
            "# Abstract {.unnumbered .reserved}",
            "# 1 Introduction {.reserved}",
            sections[0],
            sections[1],
            "# 4 Discussion {.reserved}",
            "# References {.unnumbered}",
            f'<div class="refs">\n{reference_html(order)}\n</div>',
        ]
    )
    OUT_MD.write_text(md + "\n", encoding="utf-8")

    subprocess.run(
        [
            "pandoc", str(OUT_MD),
            "-f", "markdown-implicit_figures-smart-auto_identifiers-citations",
            "-t", "html5",
            "--columns=20",
            "--template", str(HERE / "template.html"),
            "--katex=node_modules/katex/dist/",
            "--metadata", "pagetitle=MetricEval: Methods and Results (draft)",
            "-o", str(OUT_HTML),
        ],
        check=True,
    )

    h = OUT_HTML.read_text(encoding="utf-8")
    h = re.sub(r"<caption>\s*" + TOP_MARK + r"\s*", '<caption class="top">', h)
    OUT_HTML.write_text(h, encoding="utf-8")

    chrome = find_chrome()
    subprocess.run(
        [
            chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
            "--no-pdf-header-footer", "--virtual-time-budget=30000",
            f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri(),
        ],
        check=True, stderr=subprocess.DEVNULL,
    )

    dom = subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
         "--virtual-time-budget=30000", "--dump-dom", OUT_HTML.as_uri()],
        check=True, capture_output=True, text=True,
    ).stdout
    errs = len(re.findall(r"katex-error", dom))
    print(f"wrote {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KiB); "
          f"{len(order)} references; KaTeX errors: {errs}")
    if errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
