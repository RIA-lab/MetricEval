# Building the PDFs

`paper/paper.pdf` (Methods, Results, references) and `paper/supplementary.pdf` (description of every table)
are built from the Markdown sources in `paper/` and the CSV files in `tables/`.

```
npm install                       # once: KaTeX
python3 renumber_tables.py        # ran once; the numbering by first citation is frozen in table_ids.csv
python3 make_public_tables.py     # tables/ -> tables/public/ (hash-checked, renamed, cross-references renumbered)
python3 build_all.py              # supplementary.pdf and paper.pdf, repeated until cross-link pages are stable
```

Needs `pandoc`, a Chromium/Chrome binary (set `CHROME=` to override), `pdftotext` and the Python package `pypdf`.

| File | Role |
|---|---|
| `supplement_spec.py` | descriptions of the 49 supplementary tables (the single source for `public/INDEX.csv` and the PDF) |
| `table_ids.csv` | generated id -> number by first citation |
| `make_public_tables.py` | builds `tables/public/` |
| `build_supplement.py` | writes `paper/supplementary.md` and `supplementary.pdf` (`--check` validates the spec against the CSVs) |
| `build_pdf.py` | writes `paper/paper.pdf` (S numbers in the text become links into the supplement) |
| `common.py`, `template*.html`, `paper.css`, `supplement.css` | shared helpers and styling |

Links between the two PDFs are relative (`supplementary.pdf#page=N`, `paper.pdf#page=N`), so keep both files in one folder.
