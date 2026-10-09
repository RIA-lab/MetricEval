#!/usr/bin/env python3
"""Build both PDFs until the page numbers used by their cross-links are stable.

    python3 make_public_tables.py   # once, or whenever tables/ changes
    python3 build_all.py            # supplementary.pdf, paper.pdf
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(script):
    subprocess.run([sys.executable, str(HERE / script)], check=True, cwd=HERE)


def pages():
    return [(HERE / f).read_text() if (HERE / f).exists() else "" for f in ("supplement_pages.json", "paper_pages.json")]


def main():
    for i in range(1, 5):
        before = pages()
        run("build_supplement.py")
        run("build_pdf.py")
        if pages() == before:
            print(f"cross-link page numbers stable after {i} round(s)")
            return
    sys.exit("page numbers did not settle")


if __name__ == "__main__":
    main()
