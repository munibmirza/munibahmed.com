// Builds web/index.html from InterAudit-P1.html with the inline <script> obfuscated.
// Source stays readable; only the deployed copy is protected.
const fs = require("fs");
const path = require("path");
const JavaScriptObfuscator = require("javascript-obfuscator");

const SRC = path.join(__dirname, "InterAudit-P1.html");
const OUT_DIR = path.join(__dirname, "web");
const OUT = path.join(OUT_DIR, "index.html");

let html = fs.readFileSync(SRC, "utf8");

// Grab the LAST <script>...</script> (the app logic). Library <script src> tags are untouched.
const re = /<script>([\s\S]*?)<\/script>/g;
let match, last = null;
while ((match = re.exec(html)) !== null) last = match;
if (!last) { console.error("No inline <script> found."); process.exit(1); }

const original = last[1];
console.log("Inline JS length:", original.length);

const obf = JavaScriptObfuscator.obfuscate(original, {
  // strong but safe: renames identifiers + hides all strings, no control-flow
  // flattening / dead-code (those most often break large apps).
  compact: true,
  simplify: true,
  identifierNamesGenerator: "hexadecimal",
  renameGlobals: false,
  stringArray: true,
  stringArrayEncoding: ["base64"],
  stringArrayThreshold: 1,
  splitStrings: true,
  splitStringsChunkLength: 10,
  transformObjectKeys: false,   // keep GL_MAP dynamic lookups intact
  numbersToExpressions: false,
  unicodeEscapeSequence: false,
  target: "browser",
}).getObfuscatedCode();

console.log("Obfuscated JS length:", obf.length);

const protectedHtml =
  html.slice(0, last.index) +
  "<script>" + obf + "</script>" +
  html.slice(last.index + last[0].length);

if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });
fs.writeFileSync(OUT, protectedHtml, "utf8");

// copy assets
const assetsSrc = path.join(__dirname, "assets");
const assetsOut = path.join(OUT_DIR, "assets");
if (!fs.existsSync(assetsOut)) fs.mkdirSync(assetsOut, { recursive: true });
for (const f of ["founder.jpg", "founder_cutout.png", "icon.png"]) {
  const s = path.join(assetsSrc, f);
  if (fs.existsSync(s)) fs.copyFileSync(s, path.join(assetsOut, f));
}

console.log("Wrote protected build -> web/index.html");
