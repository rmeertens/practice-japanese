"""Shared print-HTML building blocks for the practice/answer/meaning sheets.

Used by render_kanji_html.py (JLPT kanji, from kanji-sheets/data/*.json)
and render_kana_html.py (hiragana/katakana, from kana-sheets/data/*.json).
Kept as plain string templates rather than a templating engine since the
whole point is a handful of near-identical, easy-to-print HTML pages.
"""

RESET_CSS = """
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; color: #1a1a1a; }
  .intro { padding: 2mm 0 5mm; }
  .intro h1 { font-size: 15pt; font-weight: 700; }
  .intro p { font-size: 8.5pt; color: #555; margin-top: 1.5mm; }
"""

# "Practice": a prompt label above an empty box, for writing the answer
# character by hand (used for both "write the kanji" and "write the kana").
PRACTICE_CSS = """
  .grid { display: flex; flex-wrap: wrap; gap: 3mm; }
  .box { width: 21mm; break-inside: avoid; page-break-inside: avoid; display: flex; flex-direction: column; align-items: stretch; }
  .box-label { font-size: 6.6pt; line-height: 1.25; text-align: center; color: #222; height: 7.2mm; display: flex; align-items: flex-end; justify-content: center; padding-bottom: 0.8mm; overflow: hidden; }
  .box-square { width: 21mm; height: 21mm; border: 0.4mm solid #999; position: relative; }
  /* Flat-color guide lines, not a gradient: Chromium's print-to-PDF turns
     CSS gradients into shading-pattern + transparency-group XObjects, and
     with 1000+ boxes on a full sheet that bloats the PDF into something
     many printers' RIPs choke on. Plain fills stay cheap vector rects. */
  .box-square::before, .box-square::after { content: ""; position: absolute; background: #ddd; }
  .box-square::before { left: 50%; top: 0; bottom: 0; width: 0.25mm; margin-left: -0.125mm; }
  .box-square::after { top: 50%; left: 0; right: 0; height: 0.25mm; margin-top: -0.125mm; }
"""

PRACTICE_CELL = (
    '    <div class="box"><div class="box-label">{label}</div><div class="box-square"></div></div>'
)

# "Answers": dense reference cells with both the glyph and its label, in
# practice-sheet order, for checking your work either direction.
ANSWERS_CSS = """
  .grid { display: flex; flex-wrap: wrap; gap: 2mm; }
  .cell { width: 15mm; break-inside: avoid; page-break-inside: avoid; border: 0.3mm solid #ccc; padding: 1mm 0.5mm; text-align: center; }
  .cell-glyph { font-family: 'IPAGothic', 'Noto Sans CJK JP', sans-serif; font-size: 15pt; line-height: 1.3; }
  .cell-label { font-size: 5.6pt; line-height: 1.15; color: #444; height: 6.2mm; overflow: hidden; }
"""

ANSWERS_CELL = (
    '    <div class="cell"><div class="cell-glyph">{glyph}</div>'
    '<div class="cell-label">{label}</div></div>'
)

# "Meaning practice": the reverse direction for kanji — the glyph is shown,
# and the learner writes its meaning on the ruled lines below.
MEANING_CSS = """
  .grid { display: flex; flex-wrap: wrap; gap: 3mm; }
  .box { width: 32mm; break-inside: avoid; page-break-inside: avoid; }
  .box-glyph { font-family: 'IPAGothic', 'Noto Sans CJK JP', sans-serif; font-size: 20pt; text-align: center; height: 12mm; display: flex; align-items: center; justify-content: center; }
  .box-writeline { height: 5mm; border-bottom: 0.3mm solid #bbb; }
"""

MEANING_CELL = (
    '    <div class="box"><div class="box-glyph">{glyph}</div>'
    '<div class="box-writeline"></div><div class="box-writeline"></div></div>'
)

# "Sentence worksheet": numbered example sentences (Japanese with furigana,
# or English) with the translation left blank on ruled lines beneath. Reuses
# the ".grid" wrapper class from PAGE_TEMPLATE as a vertical list instead of
# a flex-wrapped grid of small boxes — same template, different CSS.
SENTENCE_CSS = """
  .grid { display: flex; flex-direction: column; gap: 6mm; }
  .item { break-inside: avoid; page-break-inside: avoid; display: flex; gap: 3mm; align-items: flex-start; }
  .item-num { font-weight: 700; font-size: 10pt; color: #666; min-width: 6mm; padding-top: 0.5mm; }
  .item-body { flex: 1; }
  .item-prompt { font-size: 12.5pt; line-height: 1.7; }
  .item-prompt.jp { font-family: 'IPAGothic', 'Noto Sans CJK JP', sans-serif; }
  .item-prompt.en { font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-size: 11.5pt; }
  .item-lines { margin-top: 2.5mm; }
  .item-line { height: 6.5mm; border-bottom: 0.3mm solid #bbb; }
"""

SENTENCE_ITEM = (
    '    <div class="item"><div class="item-num">{num}.</div>'
    '<div class="item-body"><div class="item-prompt {lang}">{prompt}</div>'
    '<div class="item-lines"><div class="item-line"></div><div class="item-line"></div></div>'
    '</div></div>'
)

# Answer key: the question (as it appeared on that direction's worksheet)
# always printed first, then its answer below — one answer key per
# direction, matching the worksheet it checks.
SENTENCE_ANSWERS_CSS = """
  .grid { display: flex; flex-direction: column; gap: 3.5mm; }
  .item { break-inside: avoid; page-break-inside: avoid; display: flex; gap: 3mm; align-items: baseline; border-bottom: 0.2mm solid #eee; padding-bottom: 2.5mm; }
  .item-num { font-weight: 700; font-size: 9pt; color: #666; min-width: 6mm; }
  .item-body { flex: 1; }
  .item-question { font-size: 11.5pt; line-height: 1.5; }
  .item-question.jp { font-family: 'IPAGothic', 'Noto Sans CJK JP', sans-serif; }
  .item-answer { font-size: 9.5pt; color: #444; margin-top: 0.8mm; }
  .item-answer.jp { font-family: 'IPAGothic', 'Noto Sans CJK JP', sans-serif; font-size: 10.5pt; }
"""

SENTENCE_ANSWERS_ITEM = (
    '    <div class="item"><div class="item-num">{num}.</div>'
    '<div class="item-body"><div class="item-question {qlang}">{question}</div>'
    '<div class="item-answer {alang}">{answer}</div></div></div>'
)


def render_sentence_worksheet_page(title, subtitle, items, prompt_key, lang):
    """items: sentence dicts with ja/jaHtml/en. prompt_key is 'jaHtml' (write
    the English translation) or 'en' (write the Japanese translation); lang
    picks the prompt's font ('jp' or 'en')."""
    cells = [
        SENTENCE_ITEM.format(
            num=i + 1,
            lang=lang,
            prompt=it[prompt_key] if prompt_key == 'jaHtml' else esc(it[prompt_key]),
        )
        for i, it in enumerate(items)
    ]
    return render_page(title, len(items), "sentences", subtitle, SENTENCE_CSS, cells)


def render_sentence_answers_page(title, items, direction):
    """direction: 'to-english' (question is the Japanese sentence shown on
    that worksheet, answer is the English translation) or 'to-japanese'
    (question is the English sentence, answer is the Japanese)."""
    cells = []
    for i, it in enumerate(items):
        if direction == 'to-english':
            question, qlang = it['jaHtml'], 'jp'
            answer, alang = esc(it['en']), 'en'
        else:
            question, qlang = esc(it['en']), 'en'
            answer, alang = it['jaHtml'], 'jp'
        cells.append(SENTENCE_ANSWERS_ITEM.format(
            num=i + 1, question=question, qlang=qlang, answer=answer, alang=alang,
        ))
    return render_page(
        title, len(items), "sentences",
        "Same order as the worksheet, for checking your translations.",
        SENTENCE_ANSWERS_CSS, cells,
    )

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Tokidoki — {title}</title>
<style>{reset}{kind_css}</style>
</head>
<body>
  <div class="intro">
    <h1>{title} — {count} {unit}</h1>
    <p>Tokidoki · tokidoki.meertens.dev — {subtitle}</p>
  </div>
  <div class="grid">
{cells}
  </div>
</body>
</html>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_page(title, count, unit, subtitle, kind_css, cells_html):
    return PAGE_TEMPLATE.format(
        title=title,
        count=count,
        unit=unit,
        subtitle=subtitle,
        reset=RESET_CSS,
        kind_css=kind_css,
        cells="\n".join(cells_html),
    )


def render_practice_page(title, unit, items, label_key, subtitle):
    cells = [PRACTICE_CELL.format(label=esc(it[label_key])) for it in items]
    return render_page(title, len(items), unit, subtitle, PRACTICE_CSS, cells)


def render_answers_page(title, unit, items, glyph_key, label_key):
    cells = [
        ANSWERS_CELL.format(glyph=esc(it[glyph_key]), label=esc(it[label_key]))
        for it in items
    ]
    return render_page(
        title, len(items), unit,
        "Same order as the practice sheet, for checking your answers.",
        ANSWERS_CSS, cells,
    )


def render_meaning_page(title, unit, items, glyph_key, subtitle):
    cells = [MEANING_CELL.format(glyph=esc(it[glyph_key])) for it in items]
    return render_page(title, len(items), unit, subtitle, MEANING_CSS, cells)
