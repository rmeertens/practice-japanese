#!/usr/bin/env python3
"""Render the per-JLPT-level kanji sheets to standalone print HTML.

Reads kanji-sheets/data/n{level}.json (see generate_kanji_data.py) and
writes, per level, a self-contained HTML file for each of three sheets:
  - n{level}.html          practice: meaning shown, write the kanji
  - n{level}-meaning.html  reverse:  kanji shown, write the meaning
  - n{level}-answers.html  answer key for both directions
Those files are then printed to PDF (see render_sheets_pdfs.mjs).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sheet_html import render_answers_page, render_meaning_page, render_practice_page

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "kanji-sheets" / "data"
LEVELS = [5, 4, 3, 2, 1]


def main():
    if len(sys.argv) != 2:
        print("usage: render_kanji_html.py <out-dir>")
        sys.exit(1)
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    for level in LEVELS:
        items = json.loads((DATA_DIR / f"n{level}.json").read_text())
        title = f"JLPT N{level} Kanji"

        stem = f"tokidoki-kanji-n{level}"

        practice = render_practice_page(
            f"{title} Practice", "kanji", items, "meaning",
            "Write each kanji from memory in the box below its meaning.",
        )
        (out_dir / f"{stem}.html").write_text(practice)
        print(f"N{level} practice: {len(items)} boxes")

        meaning = render_meaning_page(
            f"{title} Meaning Practice", "kanji", items, "kanji",
            "Write the English meaning of each kanji on the lines below it.",
        )
        (out_dir / f"{stem}-meaning.html").write_text(meaning)
        print(f"N{level} meaning practice: {len(items)} boxes")

        answers = render_answers_page(f"{title} Answer Key", "kanji", items, "kanji", "meaning")
        (out_dir / f"{stem}-answers.html").write_text(answers)
        print(f"N{level} answers: {len(items)} cells")


if __name__ == "__main__":
    main()
