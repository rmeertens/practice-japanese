#!/usr/bin/env python3
"""Render the per-JLPT-level kanji practice grid to standalone print HTML.

Reads kanji-sheets/data/n{level}.json (see generate_kanji_data.py) and
writes a self-contained HTML file per level to the given output directory.
Those files are then printed to PDF (see render_kanji_pdfs.mjs).
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "kanji-sheets" / "data"
LEVELS = [5, 4, 3, 2, 1]

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JLPT N{level} Kanji Practice Sheet — Tokidoki</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #1a1a1a;
  }}
  .intro {{
    padding: 2mm 0 5mm;
  }}
  .intro h1 {{
    font-size: 15pt;
    font-weight: 700;
  }}
  .intro p {{
    font-size: 8.5pt;
    color: #555;
    margin-top: 1.5mm;
  }}
  .grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 3mm;
  }}
  .box {{
    width: 21mm;
    break-inside: avoid;
    page-break-inside: avoid;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }}
  .box-meaning {{
    font-size: 6.6pt;
    line-height: 1.25;
    text-align: center;
    color: #222;
    height: 7.2mm;
    display: flex;
    align-items: flex-end;
    justify-content: center;
    padding-bottom: 0.8mm;
    overflow: hidden;
  }}
  .box-square {{
    width: 21mm;
    height: 21mm;
    border: 0.4mm solid #999;
    position: relative;
  }}
  /* Flat-color guide lines, not a gradient: Chromium's print-to-PDF turns
     CSS gradients into shading-pattern + transparency-group XObjects, and
     with 1000+ boxes on the N1 sheet that bloats the PDF into something
     many printers' RIPs choke on. Plain fills stay cheap vector rects. */
  .box-square::before, .box-square::after {{
    content: "";
    position: absolute;
    background: #ddd;
  }}
  .box-square::before {{
    left: 50%;
    top: 0;
    bottom: 0;
    width: 0.25mm;
    margin-left: -0.125mm;
  }}
  .box-square::after {{
    top: 50%;
    left: 0;
    right: 0;
    height: 0.25mm;
    margin-top: -0.125mm;
  }}
  .row-break {{
    flex-basis: 100%;
    height: 0;
  }}
</style>
</head>
<body>
  <div class="intro">
    <h1>JLPT N{level} Kanji Practice — {count} kanji</h1>
    <p>Tokidoki · tokidoki.meertens.dev — Write each kanji from memory in the box below its meaning.</p>
  </div>
  <div class="grid">
{boxes}
  </div>
</body>
</html>
"""

BOX_TEMPLATE = '    <div class="box"><div class="box-meaning">{meaning}</div><div class="box-square"></div></div>'

# Answer key: same order as the practice sheet, but denser — the kanji
# itself replaces the empty writing box, so no need for a full-size square.
ANSWER_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>JLPT N{level} Kanji Answer Key — Tokidoki</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    color: #1a1a1a;
  }}
  .intro {{
    padding: 2mm 0 5mm;
  }}
  .intro h1 {{
    font-size: 15pt;
    font-weight: 700;
  }}
  .intro p {{
    font-size: 8.5pt;
    color: #555;
    margin-top: 1.5mm;
  }}
  .grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 2mm;
  }}
  .cell {{
    width: 15mm;
    break-inside: avoid;
    page-break-inside: avoid;
    border: 0.3mm solid #ccc;
    padding: 1mm 0.5mm;
    text-align: center;
  }}
  .cell-kanji {{
    font-family: 'IPAGothic', 'Noto Sans CJK JP', sans-serif;
    font-size: 15pt;
    line-height: 1.3;
  }}
  .cell-meaning {{
    font-size: 5.6pt;
    line-height: 1.15;
    color: #444;
    height: 6.2mm;
    overflow: hidden;
  }}
</style>
</head>
<body>
  <div class="intro">
    <h1>JLPT N{level} Kanji Answer Key — {count} kanji</h1>
    <p>Tokidoki · tokidoki.meertens.dev — Same order as the practice sheet, for checking your answers.</p>
  </div>
  <div class="grid">
{cells}
  </div>
</body>
</html>
"""

CELL_TEMPLATE = (
    '    <div class="cell"><div class="cell-kanji">{kanji}</div>'
    '<div class="cell-meaning">{meaning}</div></div>'
)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def main():
    if len(sys.argv) != 2:
        print("usage: render_kanji_html.py <out-dir>")
        sys.exit(1)
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    for level in LEVELS:
        items = json.loads((DATA_DIR / f"n{level}.json").read_text())

        boxes = "\n".join(
            BOX_TEMPLATE.format(meaning=esc(it["meaning"]))
            for it in items
        )
        html = PAGE_TEMPLATE.format(level=level, count=len(items), boxes=boxes)
        out_path = out_dir / f"n{level}.html"
        out_path.write_text(html)
        print(f"N{level}: {len(items)} boxes -> {out_path}")

        cells = "\n".join(
            CELL_TEMPLATE.format(kanji=esc(it["kanji"]), meaning=esc(it["meaning"]))
            for it in items
        )
        answer_html = ANSWER_PAGE_TEMPLATE.format(level=level, count=len(items), cells=cells)
        answer_path = out_dir / f"n{level}-answers.html"
        answer_path.write_text(answer_html)
        print(f"N{level} answers: {len(items)} cells -> {answer_path}")


if __name__ == "__main__":
    main()
