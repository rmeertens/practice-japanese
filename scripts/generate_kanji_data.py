#!/usr/bin/env python3
"""Build per-JLPT-level kanji + meaning lists for the printable practice sheets.

Source data: davidluzgouveia/kanji-data (MIT), a KANJIDIC2-derived dataset
with an unofficial jlpt_new (N5-N1) level mapping matching the widely used
"Tanos" JLPT kanji lists. Kanji within each level are ordered by written-
frequency rank, which is the conventional order those lists are presented in.

Usage:
    python3 scripts/generate_kanji_data.py <path-to-kanji-data.json>

Writes kanji-sheets/data/n5.json .. n1.json, each a list of
{"kanji": "...", "meaning": "..."} objects in practice-sheet order.
"""
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "kanji-sheets" / "data"

LEVELS = [5, 4, 3, 2, 1]

# Drop meaning entries that are noise for a practice sheet. Always-noise:
# radical names and the old-time hour-range glosses that ride along with
# the Chinese-zodiac kanji (e.g. "11pm-1am"). Zodiac labels themselves
# ("Sign Of The Rat") are only dropped if the kanji has another meaning
# left without them, since a few zodiac kanji have no other common gloss.
ALWAYS_NOISE_RE = re.compile(r"radical \(no|^\d{1,2}\s*(am|pm)?\s*-\s*\d{1,2}\s*(am|pm)$", re.I)
ZODIAC_RE = re.compile(r"sign of the|chinese zodiac", re.I)
MAX_LEN = 26


def clean_meaning(meanings):
    if not meanings:
        return ""
    base = [m for m in meanings if not ALWAYS_NOISE_RE.search(m)]
    if not base:
        base = meanings
    non_zodiac = [m for m in base if not ZODIAC_RE.search(m)]
    filtered = non_zodiac if non_zodiac else base
    text = ", ".join(filtered[:2])
    if len(text) > MAX_LEN:
        text = text[:MAX_LEN].rsplit(" ", 1)[0].rstrip(",") + "…"
    return text


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    src = json.loads(Path(sys.argv[1]).read_text())

    by_level = {lvl: [] for lvl in LEVELS}
    for kanji, info in src.items():
        lvl = info.get("jlpt_new")
        if lvl in by_level:
            by_level[lvl].append({
                "kanji": kanji,
                "meaning": clean_meaning(info.get("meanings")),
                "freq": info.get("freq"),
                "strokes": info.get("strokes") or 0,
            })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for lvl in LEVELS:
        items = by_level[lvl]
        items.sort(key=lambda x: (
            x["freq"] is None,
            x["freq"] if x["freq"] is not None else 0,
            x["strokes"],
            x["kanji"],
        ))
        out = [{"kanji": it["kanji"], "meaning": it["meaning"]} for it in items]
        out_path = OUT_DIR / f"n{lvl}.json"
        out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
        print(f"N{lvl}: {len(out)} kanji -> {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
