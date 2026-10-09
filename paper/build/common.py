"""Helpers shared by build_pdf.py and build_supplement.py."""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PAPER = HERE.parent
TABLES = PAPER.parent / "tables"

# Links between the two PDFs are written with this placeholder host; Chromium
# would turn a relative href into an absolute file:// path, so after printing
# the host is stripped again and the link becomes relative ("supplementary.pdf#page=3").
LINK_HOST = "https://pdflink.invalid/"

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/opt/pw-browsers/chromium/chrome-linux/chrome",
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
    shutil.which("google-chrome") or "",
]

MATH_RE = re.compile(r"\$\$.*?\$\$|(?<!\$)\$(?!\$)[^$\n]+?\$(?!\$)", re.S)
# spans in which a table id must not be turned into a link
PROTECT_RE = re.compile(r"\$\$.*?\$\$|\$[^$\n]+?\$|`[^`]*`|\]\([^)]*\)|<[^>]+>|\[[^\]]*\]\(")
ID_TOKEN = re.compile(r"(?<![\w/.#-])S(\d{1,2})(?![\w-])")


def find_chrome():
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("no Chromium/Chrome found; set CHROME=/path/to/chrome")


def pandoc_html(md, html_out, template, title):
    subprocess.run(
        [
            "pandoc", str(md),
            "-f", "markdown-implicit_figures-smart-auto_identifiers-citations",
            "-t", "html5",
            "--columns=20",
            "--template", str(template),
            "--katex=node_modules/katex/dist/",
            "--metadata", f"pagetitle={title}",
            "-o", str(html_out),
        ],
        check=True,
    )


def print_pdf(html_path, pdf_path):
    chrome = find_chrome()
    subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=30000", f"--print-to-pdf={pdf_path}", Path(html_path).as_uri()],
        check=True, stderr=subprocess.DEVNULL,
    )
    dom = subprocess.run(
        [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
         "--virtual-time-budget=30000", "--dump-dom", Path(html_path).as_uri()],
        check=True, capture_output=True, text=True,
    ).stdout
    return len(re.findall(r"katex-error", dom))


def relativize_links(pdf_path):
    """Turn https://pdflink.invalid/x.pdf#page=n into the relative link x.pdf#page=n."""
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import NameObject, TextStringObject

    reader = PdfReader(str(pdf_path))
    writer = PdfWriter(clone_from=reader)
    n = 0
    for page in writer.pages:
        for annot in page.get("/Annots") or []:
            action = annot.get_object().get("/A")
            if action is None:
                continue
            action = action.get_object()
            uri = action.get("/URI")
            if uri and str(uri).startswith(LINK_HOST):
                action[NameObject("/URI")] = TextStringObject(str(uri)[len(LINK_HOST):])
                n += 1
    tmp = Path(str(pdf_path) + ".tmp")
    with open(tmp, "wb") as f:
        writer.write(f)
    os.replace(tmp, pdf_path)
    return n


def page_texts(pdf_path):
    out = subprocess.run(["pdftotext", "-layout", str(pdf_path), "-"],
                         check=True, capture_output=True, text=True).stdout
    return out.split("\f")[:-1] if out.endswith("\f") else out.split("\f")


def link_ids(md, href):
    """Replace table ids (S12) in prose by Markdown links; href(n) gives the target or None."""
    out = []
    in_fence = False
    for line in md.split("\n"):
        if line.startswith(":::") or line.startswith("```"):
            in_fence = in_fence if line.startswith(":::") else not in_fence
            out.append(line)
            continue
        if in_fence or line.startswith("#") or line.startswith("|--") or line.startswith("<div"):
            out.append(line)
            continue
        pieces, last = [], 0
        for m in PROTECT_RE.finditer(line):
            pieces.append(ID_TOKEN.sub(lambda t: _link(t, href), line[last:m.start()]))
            pieces.append(m.group(0))
            last = m.end()
        pieces.append(ID_TOKEN.sub(lambda t: _link(t, href), line[last:]))
        out.append("".join(pieces))
    return "\n".join(out)


def _link(m, href):
    target = href(int(m.group(1)))
    return f"[S{m.group(1)}]({target})" if target else m.group(0)
