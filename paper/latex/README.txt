LaTeX source of the paper and of its Supplementary Information
===============================================================

  paper.tex            title, 1 Introduction, 2 Methods, 3 Results, 4 Discussion and the
                       references; the Abstract is a reserved heading only
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
Introduction, Methods and Results (references are listed with \nocite in that order).

The data tables are not part of this source: they are released as CSV files
(main/ and supplementary/ of the released directory), and the supplement describes them.
