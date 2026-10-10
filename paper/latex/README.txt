LaTeX source of "MetricEval" (Methods, Results, references) and its Supplementary Information
=============================================================================================

  paper.tex            Title, Abstract, 1 Introduction and 4 Discussion are reserved headings
                       only; 2 Methods, 3 Results and the references are complete
  supplementary.tex    describes the 49 supplementary tables and the 9 main-text tables
  references.bib       entries cited in paper.tex
  paper.bbl            BibTeX output for paper.tex (so that paper.tex compiles without BibTeX)
  fig1_study_map.png   Figure 1

Compile (pdfLaTeX; the standard TeX Live packages amsmath, cite, caption, framed,
longtable, booktabs, hyperref are used):

  latexmk -pdf paper
  latexmk -pdf supplementary

or  pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper

Numbering: section numbers are part of the headings; table, box and equation numbers
are written in the text. Citation numbers follow the order of first citation in the
Methods and Results (references are listed with \nocite in that order).

The data tables are not part of this source: they are released as CSV files
(main/ and supplementary/ of the released directory), and the supplement describes them.
