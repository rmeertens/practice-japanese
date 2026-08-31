#!/usr/bin/env python3
"""Extract the hiragana/katakana lists straight from kana.js (the site's own
drawing-practice data) so the printable sheets always match what the app
itself teaches — no separate, potentially-out-of-sync data source.

Usage:
    python3 scripts/generate_kana_data.py

Writes kana-sheets/data/hiragana.json and katakana.json, each a list of
{"kana": "...", "romaji": "..."} objects in kana.js's own order
(gojuon, then dakuten/handakuten, then yoon).
"""
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "kana-sheets" / "data"

# kana.js is a plain browser script (assigns to `window`), not JSON/a CommonJS
# module — evaluate it in Node with a stub `window` and dump the result,
# rather than hand-parsing or re-transcribing ~200 kana/romaji pairs.
EXTRACT_JS = """
global.window = {};
const src = require('fs').readFileSync(process.argv[1], 'utf8');
eval(src);
process.stdout.write(JSON.stringify(window.KANA_DATA));
"""


def main():
    kana_js = REPO_ROOT / "kana.js"
    result = subprocess.run(
        ["node", "-e", EXTRACT_JS, str(kana_js)],
        capture_output=True, text=True, check=True,
    )
    data = json.loads(result.stdout)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for script in ["hiragana", "katakana"]:
        items = data[script]
        out_path = OUT_DIR / f"{script}.json"
        out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n")
        print(f"{script}: {len(items)} characters -> {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
