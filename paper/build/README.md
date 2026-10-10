# Building the PDFs and the LaTeX source

`paper/paper.pdf` (title, Introduction, Methods, Results, Discussion, references; the Abstract is a reserved heading), `paper/supplementary.pdf` (description of every table) and
`paper/latex_source.zip` (the LaTeX source of both) are built from the Markdown sources in `paper/` and the CSV
files in `tables/`. Only `tables/public/` is released (as the root of the public repository); it holds no internal
codes, and `check_public_text.py` fails if any appears in the text, the tables, the PDFs or the LaTeX.

```
npm install                       # once: KaTeX
python3 renumber_tables.py        # ran once; the numbering by first citation is frozen in table_ids.csv
python3 renumber_tables.py --again --apply   # only after text edits changed the order of first citation
python3 renumber_main_tables.py   # ran once: Results Tables 3-9 became 5-11 when the Methods got Tables 1-4
python3 renumber_methods_sections.py   # ran once: 2.1 became the experiment overview, the tests moved to 2.2-2.5
python3 make_public_tables.py     # tables/ -> tables/public/ (hash-checked, renamed, cross-references renumbered)
python3 build_all.py              # supplementary.pdf and paper.pdf, repeated until cross-link pages are stable
python3 build_latex.py            # paper/latex/ and paper/latex_source.zip (compiled once with latexmk to check)
python3 check_public_text.py      # lint: internal codes in the Markdown, the public tables, both PDFs and the .tex files
python3 check_structure.py        # table captions 1..n, S numbers in first-citation order, references cited, T5-T11 files
python3 make_figure1.py           # redraws paper/fig1_study_map.png (the figure is not used in the paper at present)
```

Needs `pandoc`, a Chromium/Chrome binary (set `CHROME=` to override), `pdftotext`, the Python packages `pypdf` and
`pillow`, and for the LaTeX build a TeX Live with `latexmk`, `pdflatex`, `bibtex` and the packages amsmath, cite, caption,
framed, longtable, booktabs, hyperref.

| File | Role |
|---|---|
| `supplement_spec.py` | descriptions of the 49 supplementary tables (the single source for `public/INDEX.csv` and the PDF) |
| `table_ids.csv` | generated id -> number by first citation |
| `make_public_tables.py` | builds `tables/public/` (values unchanged; internal columns dropped, codes translated, free text reworded) |
| `scrub_rules.py` | the rules `make_public_tables.py` applies: dropped and renamed columns, value maps, text replacements |
| `check_public_text.py` | fails if an internal code, path or working name appears in public content |
| `check_structure.py` | fails if table captions, table and S numbers, references or the public file names are inconsistent |
| `renumber_main_tables.py`, `renumber_tables.py` | one-time renumbering of the main-text tables; renumbering of the S tables by first citation (`--again`) |
| `build_latex.py`, `latex_filter.lua`, `latex_preamble.tex` | pandoc LaTeX source of `paper.tex` and `supplementary.tex`; `references.bib` with the entries cited, in citation order |
| `make_figure1.py` | redraws Figure 1 (HTML to PNG with Chromium) |
| `public_tables_crosswalk.csv` | private: generated id and file of every public table (not released) |
| `build_supplement.py` | writes `paper/supplementary.md` and `supplementary.pdf` (`--check` validates the spec against the CSVs) |
| `build_pdf.py` | writes `paper/paper.pdf` from `introduction.md`, `methods.md`, `results.md`, `discussion.md` (S numbers in the text become links into the supplement; the references are merged and numbered by first citation) |
| `common.py`, `template*.html`, `paper.css`, `supplement.css` | shared helpers (the title of the paper is `TITLE` in `common.py`) and styling |

Links between the two PDFs are relative (`supplementary.pdf#page=N`, `paper.pdf#page=N`), so keep both files in one folder.
