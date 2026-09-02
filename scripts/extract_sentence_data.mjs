#!/usr/bin/env node
// Build sentence-sheets/data/ch{N}.json from sentences-data.js (the
// window.TRANSLATE_SENTENCES global shared with the Sentences flashcard
// mode) and verbs.js's CHAPTER_INFO (chapter titles/book), so the
// printable translation worksheets stay in sync with the live site's
// sentence bank — one source of truth, no hand-copied content.
//
// Usage: node scripts/extract_sentence_data.mjs
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");

// sentences-data.js assigns to `window.TRANSLATE_SENTENCES` inside an
// IIFE, so a plain object sandbox as `window` captures it directly.
const sentencesSrc = readFileSync(path.join(REPO_ROOT, "sentences-data.js"), "utf8");
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(sentencesSrc, sandbox);
const TRANSLATE_SENTENCES = sandbox.window.TRANSLATE_SENTENCES;
if (!TRANSLATE_SENTENCES) throw new Error("TRANSLATE_SENTENCES not found in sentences-data.js");

// verbs.js declares `const CHAPTER_INFO = {...}` as a bare top-level
// script (no window assignment) — vm doesn't reflect top-level const
// bindings onto the sandbox, so pull just that object literal out with a
// bracket-matching scan and eval it standalone. It's static data (no
// references to anything else in verbs.js), so this is safe.
const verbsSrc = readFileSync(path.join(REPO_ROOT, "verbs.js"), "utf8");
const marker = "const CHAPTER_INFO = ";
const startIdx = verbsSrc.indexOf(marker);
if (startIdx === -1) throw new Error("CHAPTER_INFO not found in verbs.js");
const braceStart = verbsSrc.indexOf("{", startIdx);
let depth = 0, endIdx = -1;
for (let i = braceStart; i < verbsSrc.length; i++) {
  if (verbsSrc[i] === "{") depth++;
  else if (verbsSrc[i] === "}") { depth--; if (depth === 0) { endIdx = i + 1; break; } }
}
const CHAPTER_INFO = new Function(`return (${verbsSrc.slice(braceStart, endIdx)});`)();

// Genki I and II don't map onto JLPT levels precisely, but Genki I
// (chapters 3-12) is a reasonable approximation of N5 grammar, and
// Genki II (13-23) mostly covers N4 (edging into N3 by its later
// chapters) — same rough labeling used for the practice sheets page.
const bookToLevel = { "Genki I": "N5", "Genki II": "N4" };

const outDir = path.join(REPO_ROOT, "sentence-sheets", "data");
mkdirSync(outDir, { recursive: true });

const chapters = Object.keys(TRANSLATE_SENTENCES).map(Number).sort((a, b) => a - b);
for (const num of chapters) {
  const info = CHAPTER_INFO[num];
  if (!info) throw new Error(`No CHAPTER_INFO for chapter ${num}`);
  const sentences = TRANSLATE_SENTENCES[num];
  const data = {
    number: num,
    title: info.title,
    book: info.book,
    level: bookToLevel[info.book] || null,
    sentences: sentences.map(({ ja, jaHtml, en }) => ({ ja, jaHtml, en })),
  };
  const outPath = path.join(outDir, `ch${num}.json`);
  writeFileSync(outPath, JSON.stringify(data, null, 2) + "\n");
  console.log(`ch${num}: ${info.title} (${data.level}) — ${sentences.length} sentences -> ${path.relative(REPO_ROOT, outPath)}`);
}
