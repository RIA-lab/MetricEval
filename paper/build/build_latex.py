#!/usr/bin/env python3
"""Build the LaTeX source of the paper and of the Supplementary Information.

Writes paper/latex/ (paper.tex, supplementary.tex, references.bib, paper.bbl,
README.txt) and paper/latex_source.zip (sources only).

  * paper.tex          the title, the Abstract, 1 Introduction, 2 Methods, 3 Results,
                       4 Discussion and the references, as in paper.pdf.
  * supplementary.tex  the description of the supplementary tables (as supplementary.pdf).
  * references.bib     the entries cited, in the order of first citation. paper.tex lists
                       them with \\nocite in that order, so that the BibTeX (unsrt) numbers
                       equal the numbers of paper.pdf.

The text is the same Markdown as for the PDFs (introduction.md, methods.md, results.md,
discussion.md, abstract.md and the generated supplementary.md text); pandoc writes the LaTeX, latex_filter.lua maps
figures and boxes, latex_preamble.tex adds packages. Both documents are compiled
with latexmk in a scratch directory to check them; the compiled PDFs are not part
of the release (paper.pdf and supplementary.pdf are).

    python3 build_latex.py            # write paper/latex/ and paper/latex_source.zip
    python3 build_latex.py --no-zip   # write the sources and compile them only
"""
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

import build_pdf as bp
import build_supplement as bs
from common import HERE, PAPER, TITLE

OUT = PAPER / "latex"
ZIP = PAPER / "latex_source.zip"
PANDOC_FROM = "markdown-implicit_figures-auto_identifiers-citations"   # smart quotes on
CITE_KEY = "`\\cite{%s}`{=latex}"

README = """\
LaTeX source of the paper and of its Supplementary Information
===============================================================

  paper.tex            title, Abstract, 1 Introduction, 2 Methods, 3 Results, 4 Discussion
                       and the references
  supplementary.tex    describes the 49 supplementary tables and the seven data tables of the Results
  references.bib       entries cited in paper.tex
  paper.bbl            BibTeX output for paper.tex (so that paper.tex compiles without BibTeX)

Compile (pdfLaTeX; the standard TeX Live packages amsmath, cite, caption, framed,
longtable, booktabs, hyperref are used):

  latexmk -pdf paper
  latexmk -pdf supplementary

or  pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper

Numbering: section numbers are part of the headings; table, box and equation numbers
are written in the text. Citation numbers follow the order of first citation in the
Introduction, Methods and Results (references are listed with \\nocite in that order).

The data tables are not part of this source: they are released as CSV files
(main/ and supplementary/ of the released directory), and the supplement describes them.
"""


# ------------------------------------------------------------------ citations
def cites_to_latex(text, local, order):
    """[n, m] (section-local numbers) -> raw LaTeX \\cite{key,key}; `order` collects keys by first citation."""
    pieces, last = [], 0
    for m in bp.MATH_RE.finditer(text):
        pieces.append(("t", text[last:m.start()]))
        pieces.append(("m", m.group(0)))
        last = m.end()
    pieces.append(("t", text[last:]))

    def sub(m):
        keys = []
        for n in (int(x) for x in re.split(r",\s*", m.group(1))):
            if n not in local:
                sys.exit(f"citation [{n}] has no entry in this section's reference list")
            key = local[n][0]
            if key not in order:
                order.append(key)
            keys.append(key)
        return CITE_KEY % ",".join(keys)

    return "".join(bp.CITE_RE.sub(sub, p) if kind == "t" else p for kind, p in pieces)


def write_bib(order):
    bib = (PAPER / "references.bib").read_text(encoding="utf-8")
    entries = {}
    for m in re.finditer(r"^@\w+\{([^,\s]+),.*?^\}\s*$", bib, re.S | re.M):
        entries[m.group(1)] = m.group(0).strip()
    missing = [k for k in order if k not in entries]
    if missing:
        sys.exit(f"not in references.bib: {missing}")
    (OUT / "references.bib").write_text("\n\n".join(entries[k] for k in order) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ paper
def paper_markdown():
    order = []
    sections = []
    for name in bp.BODY_FILES:
        raw = (PAPER / name).read_text(encoding="utf-8")
        body, local = bp.split_refs(raw, name)
        for old, new in bp.SENTENCE_PATCHES:
            body = body.replace(old, new)
        body = bp.prepare_blocks(body)
        body = body.replace(bp.TOP_MARK + " ", "")
        body = cites_to_latex(body, local, order)
        body = bp.link_ids(body, lambda n: None)          # table ids stay plain text
        sections.append(body)
    abstract = bp.prepare_blocks((PAPER / "abstract.md").read_text(encoding="utf-8"))
    md = "\n\n".join([abstract, *sections,
                      "```{=latex}\n\\bibliographystyle{unsrt}\n\\bibliography{references}\n```"])
    return md, order


def run_pandoc(md_text, title, subtitle, out_tex, before_body=None):
    with tempfile.TemporaryDirectory() as d:
        src = Path(d) / "in.md"
        src.write_text(md_text + "\n", encoding="utf-8")
        cmd = ["pandoc", str(src), "-f", PANDOC_FROM, "-t", "latex", "-s", "--columns=20",
               "--lua-filter", str(HERE / "latex_filter.lua"),
               "-H", str(HERE / "latex_preamble.tex"),
               "-V", "documentclass=article", "-V", "fontsize=10pt", "-V", "geometry:margin=2.3cm",
               "-V", "colorlinks=true", "-V", "linkcolor=blue", "-V", "urlcolor=blue",
               "--metadata", f"title={title}", "--metadata", "date=", "-o", str(out_tex)]
        if subtitle:
            cmd += ["--metadata", f"subtitle={subtitle}"]
        if before_body:
            bf = Path(d) / "before.tex"
            bf.write_text(before_body, encoding="utf-8")
            cmd += ["-B", str(bf)]
        subprocess.run(cmd, check=True)
    tex = out_tex.read_text(encoding="utf-8")
    tex = postprocess(tex)
    out_tex.write_text(tex, encoding="utf-8")


def postprocess(tex):
    # table captions carry their own "Table n." label: unnumbered captions
    tex = tex.replace("\\caption{", "\\caption*{")
    # \tag needs an amsmath display environment
    tex = re.sub(r"\\\[(.*?)\\\]", lambda m: ("\\begin{equation*}" + m.group(1) + "\\end{equation*}")
                 if "\\tag" in m.group(1) else m.group(0), tex, flags=re.S)
    tex = re.sub(r"[ \t]+$", "", tex, flags=re.M)
    return tex


def build_paper():
    md, order = paper_markdown()
    write_bib(order)
    nocite = "\\nocite{" + ",\n  ".join(order) + "}\n"
    run_pandoc(md, TITLE, None, OUT / "paper.tex", before_body=nocite)
    return len(order)


# ------------------------------------------------------------------ supplement
def build_supplement():
    ids, index = bs.load()
    md = bs.render(ids, index, {}, {}, latex=True)
    md = re.sub(r'<div class="title-block">.*?</div></div>\n*', "", md, count=1, flags=re.S)
    md = re.sub(r"\[([^\]]+)\]\(https://pdflink\.invalid/[^)]*\)", r"\1", md)
    run_pandoc(md, TITLE, "Supplementary Information", OUT / "supplementary.tex")


# ------------------------------------------------------------------ compile and zip
def compile_check(names):
    """Compile in a scratch directory; return {name: pages}; copy paper.bbl back into OUT."""
    pages = {}
    with tempfile.TemporaryDirectory() as d:
        scratch = Path(d)
        for f in OUT.iterdir():
            if f.suffix in (".tex", ".bib", ".png", ".bbl"):
                shutil.copy(f, scratch)
        for name in names:
            r = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", name],
                               cwd=scratch, capture_output=True, text=True)
            log = (scratch / (Path(name).stem + ".log")).read_text(encoding="utf-8", errors="replace")
            errors = re.findall(r"^[^\n]*:\d+: [^\n]*$", log, re.M)
            overfull = len(re.findall(r"Overfull \\hbox \((\d+\.?\d*)pt", log))
            pdf = scratch / (Path(name).stem + ".pdf")
            if r.returncode != 0 or not pdf.exists() or errors:
                print("\n".join(errors[:20]) or r.stdout[-2000:])
                sys.exit(f"{name}: LaTeX compile failed")
            info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
            pages[name] = int(re.search(r"Pages:\s+(\d+)", info).group(1))
            big = [float(x) for x in re.findall(r"Overfull \\hbox \((\d+\.?\d*)pt too wide", log)]
            print(f"{name}: {pages[name]} pages, {overfull} overfull boxes"
                  + (f" (largest {max(big):.0f}pt)" if big else ""))
            shutil.copy(pdf, Path(tempfile.gettempdir()) / f"latex_check_{pdf.name}")
        bbl = scratch / "paper.bbl"
        if bbl.exists():
            shutil.copy(bbl, OUT / "paper.bbl")
    return pages


def make_zip():
    files = ["paper.tex", "supplementary.tex", "references.bib", "paper.bbl", "README.txt"]
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for name in files:
            info = zipfile.ZipInfo(f"latex_source/{name}", date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (OUT / name).read_bytes())
    print(f"wrote {ZIP} ({ZIP.stat().st_size // 1024} KiB)")


def main():
    OUT.mkdir(exist_ok=True)
    (OUT / "README.txt").write_text(README, encoding="utf-8")
    n_refs = build_paper()
    build_supplement()
    print(f"wrote {OUT}/paper.tex ({n_refs} references) and supplementary.tex")
    compile_check(["paper.tex", "supplementary.tex"])
    if "--no-zip" not in sys.argv:
        make_zip()


if __name__ == "__main__":
    main()
