#!/usr/bin/env python3
"""Redraw Figure 1 (the study map) as paper/fig1_study_map.png.

HTML -> headless Chromium screenshot. The text of the four boxes is the same as
in the Methods sections 2.1 to 2.4; edit BOXES here and rerun. The figure is not used in the
paper at present (the study map was removed from section 2).

    python3 make_figure1.py
"""
import html
import subprocess
import tempfile
from pathlib import Path

from common import PAPER, find_chrome

OUT = PAPER / "fig1_study_map.png"
W, H = 1625, 1545

TITLE = "Do design metrics respond to catalysis, or to where a change is?"
SUB = "Four tests; the number in each box header is its Methods and Results subsection (2.x and 3.x)"
LEFT = "Real proteins"
RIGHT = "Deliberate changes"

BOXES = [
    ("left", "Activity discrimination test", "2.1 / 3.1", [
        ("Contrast", "zymogen (dead) against mature enzyme (active)"),
        ("Comparator", "reference rows; best-of-39 and best-of-36 thresholds"),
        ("Metrics", "29 structure-space + 4 prediction-based"),
        ("Data", "21 pairs (peptidases); 192 plated designs (16 active)"),
        ("Claim", "discrimination")]),
    ("right", "Substrate discrimination test", "2.2 / 3.2", [
        ("Change", "the ligand given to the predictor: cognate, same class, different class, decoy"),
        ("Comparator", "the cognate ligand; a best-of-30 threshold"),
        ("Metrics", "30 prediction-based quantities (4 main-set metrics)"),
        ("Data", "55 natural enzymes"),
        ("Claim", "discrimination between ligands")]),
    ("left", "Activity ranking test", "2.3 / 3.3", [
        ("Contrast", "432 BglB variants with measured kinetics; 192 plated designs, 16 with reported activity"),
        ("Comparator", "five declared baselines and reference rows; a best-of-41 threshold"),
        ("Metrics", "29 structure-space + 4 prediction-based"),
        ("Data", "175 positions; 16 designs with a measured activity"),
        ("Claim", "ranking (rank correlation)")]),
    ("right", "Detection ability test", "2.4 / 3.4", [
        ("Change", "catalytic residues replaced in four steps (isosteric to Gly), in the structure or the sequence; 1, 2 or 4 second-shell residues removed"),
        ("Comparator", "the identical change at matched non-catalytic sites; for the predictor also matched on ligand distance"),
        ("Metrics", "29 structure-space + 4 prediction-based"),
        ("Data", "195 natural enzymes; 59 enzymes, 286 pairs"),
        ("Claim", "detection ability (specificity)")]),
]

CSS = f"""
* {{ box-sizing: border-box; }}
body {{ margin: 0; width: {W}px; height: {H}px; background: #fff; color: #222;
        font-family: "DejaVu Sans", "Liberation Sans", sans-serif; }}
.wrap {{ padding: 14px 16px 0 16px; }}
h1 {{ font-size: 32px; margin: 0 0 18px; font-weight: 700; color: #111; }}
.sub {{ font-size: 22px; color: #444; margin: 0 0 54px; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; column-gap: 28px; row-gap: 52px; }}
.gh {{ font-size: 26px; font-weight: 700; padding-bottom: 10px; margin-bottom: -38px; border-bottom: 3px solid; }}
.gh.left {{ color: #b5651d; border-color: #b5651d; }}
.gh.right {{ color: #2c6a9a; border-color: #2c6a9a; }}
.box {{ border: 3px solid; border-radius: 14px; overflow: hidden; min-height: 610px; }}
.box.left {{ border-color: #b5651d; background: #f8efe4; }}
.box.right {{ border-color: #2c6a9a; background: #eaf1f8; }}
.bh {{ display: flex; justify-content: space-between; align-items: center; color: #fff;
       padding: 18px 22px; font-size: 25px; font-weight: 700; }}
.bh span {{ font-size: 20px; font-weight: 400; }}
.left .bh {{ background: #b5651d; }}
.right .bh {{ background: #2c6a9a; }}
.rows {{ padding: 16px 22px; }}
.row {{ display: grid; grid-template-columns: 200px 1fr; padding: 7px 0; font-size: 24px; line-height: 1.42; }}
.row b {{ font-size: 23px; }}
.left .row b {{ color: #b5651d; }}
.right .row b {{ color: #2c6a9a; }}
"""


def page():
    e = html.escape
    cells = []
    # group headings sit above their column
    cells.append(f'<div class="gh left">{e(LEFT)}</div><div class="gh right">{e(RIGHT)}</div>')
    for side, name, num, rows in BOXES:
        body = "".join(f'<div class="row"><b>{e(k)}</b><div>{e(v)}</div></div>' for k, v in rows)
        cells.append(f'<div class="box {side}"><div class="bh">{e(name)}<span>{e(num)}</span></div>'
                     f'<div class="rows">{body}</div></div>')
    return (f"<!doctype html><meta charset='utf-8'><style>{CSS}</style><body><div class='wrap'>"
            f"<h1>{e(TITLE)}</h1><div class='sub'>{e(SUB)}</div><div class='grid'>{''.join(cells)}</div></div></body>")


def main():
    with tempfile.TemporaryDirectory() as d:
        f = Path(d) / "fig1.html"
        f.write_text(page(), encoding="utf-8")
        raw = Path(d) / "raw.png"
        subprocess.run([find_chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={W},{H + 200}", "--force-device-scale-factor=1",
                        f"--screenshot={raw}", f.as_uri()], check=True, stderr=subprocess.DEVNULL)
        from PIL import Image
        Image.open(raw).crop((0, 0, W, H)).save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KiB)")


if __name__ == "__main__":
    main()
