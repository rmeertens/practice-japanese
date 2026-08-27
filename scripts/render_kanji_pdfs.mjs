#!/usr/bin/env node
// Print the per-level practice-sheet HTML (see render_kanji_html.py) to PDF
// with a repeating header/footer (level + page numbers) via Chromium print.
//
// Full regeneration pipeline:
//   python3 scripts/generate_kanji_data.py <path-to-kanji-data.json>
//   python3 scripts/render_kanji_html.py <build-dir>
//   node scripts/render_kanji_pdfs.mjs <build-dir> kanji-sheets
//
// Requires the `playwright` npm package to be resolvable (locally installed,
// or run with NODE_PATH pointing at a global install) and a Chromium build
// on disk — adjust executablePath below if yours lives elsewhere.
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, "..");

const buildDir = process.argv[2];
const outDir = process.argv[3];
if (!buildDir || !outDir) {
  console.error("usage: render_kanji_pdfs.mjs <build-html-dir> <out-pdf-dir>");
  process.exit(1);
}

const levels = [5, 4, 3, 2, 1];

const headerTemplate = (level, label) => `
  <div style="font-size:8px; width:100%; padding:0 10mm; color:#888; display:flex; justify-content:space-between;">
    <span>Tokidoki — JLPT N${level} Kanji ${label}</span>
  </div>`;

const footerTemplate = `
  <div style="font-size:8px; width:100%; padding:0 10mm; color:#888; display:flex; justify-content:flex-end;">
    <span class="pageNumber"></span>&nbsp;/&nbsp;<span class="totalPages"></span>
  </div>`;

async function printOne(browser, htmlPath, outPath, level, label) {
  const page = await browser.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
  await page.pdf({
    path: outPath,
    format: "A4",
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: headerTemplate(level, label),
    footerTemplate,
    margin: { top: "14mm", bottom: "12mm", left: "12mm", right: "12mm" },
  });
  await page.close();
  console.log(`N${level} ${label} -> ${outPath}`);
}

const browser = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
try {
  for (const level of levels) {
    await printOne(
      browser,
      path.join(buildDir, `n${level}.html`),
      path.join(outDir, `tokidoki-kanji-n${level}.pdf`),
      level,
      "Practice",
    );
    await printOne(
      browser,
      path.join(buildDir, `n${level}-answers.html`),
      path.join(outDir, `tokidoki-kanji-n${level}-answers.pdf`),
      level,
      "Answer Key",
    );
  }
} finally {
  await browser.close();
}
