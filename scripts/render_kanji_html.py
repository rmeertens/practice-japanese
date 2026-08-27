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
    background:
      linear-gradient(to right, #ddd 0.25mm, transparent 0.25mm) 50% 0 / 50% 100% no-repeat,
      linear-gradient(to bottom, #ddd 0.25mm, transparent 0.25mm) 0 50% / 100% 50% no-repeat;
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


if __name__ == "__main__":
    main()
