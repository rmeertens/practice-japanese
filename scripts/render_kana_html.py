#!/usr/bin/env python3
"""Render the hiragana/katakana sheets to standalone print HTML.

Reads kana-sheets/data/{hiragana,katakana}.json (see generate_kana_data.py)
and writes, per script, two single-character sheets:
  - {script}.html          practice: romaji shown, write the kana
  - {script}-answers.html  answer key (kana + romaji together)
There's no "reverse" sheet for kana (write the romaji from the kana) since
romaji is a transliteration aid, not something learners need to produce
from memory the way a kanji's meaning or reading is.

Also reads kana-sheets/data/{hiragana,katakana}-words.json (hand-authored —
common whole words in that script, not derived from kana.js) and writes,
per word list, two more sheets:
  - {script}-words.html          practice: romaji + English meaning shown,
                                  write the whole word
  - {script}-words-answers.html  answer key — question (romaji + meaning)
                                  printed first, the kana word answer below

Those files are then printed to PDF (see render_sheets_pdfs.mjs).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sheet_html import render_answers_page, render_practice_page, render_word_answers_page, render_word_practice_page

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "kana-sheets" / "data"
SCRIPTS = ["hiragana", "katakana"]


def main():
    if len(sys.argv) != 2:
        print("usage: render_kana_html.py <out-dir>")
        sys.exit(1)
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    for script in SCRIPTS:
        items = json.loads((DATA_DIR / f"{script}.json").read_text())
        title = script.capitalize()

        stem = f"tokidoki-{script}"

        practice = render_practice_page(
            f"{title} Practice", "characters", items, "romaji",
            f"Write each {title.lower()} character from memory in the box below its romaji reading.",
        )
        (out_dir / f"{stem}.html").write_text(practice)
        print(f"{script} practice: {len(items)} boxes")

        answers = render_answers_page(f"{title} Answer Key", "characters", items, "kana", "romaji")
        (out_dir / f"{stem}-answers.html").write_text(answers)
        print(f"{script} answers: {len(items)} cells")

        words = json.loads((DATA_DIR / f"{script}-words.json").read_text())

        word_practice = render_word_practice_page(
            f"Common {title} Words",
            f"Read the romaji and English meaning, then write the word in {title.lower()} on the line below.",
            words,
        )
        (out_dir / f"{stem}-words.html").write_text(word_practice)
        print(f"{script} words practice: {len(words)} boxes")

        word_answers = render_word_answers_page(f"Common {title} Words — Answer Key", words)
        (out_dir / f"{stem}-words-answers.html").write_text(word_answers)
        print(f"{script} words answers: {len(words)} cells")


if __name__ == "__main__":
    main()
