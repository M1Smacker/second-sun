// Prints the rung 3 (rehearsal) pass line from a rounds file (one JSON round per line), using the SAME code as the book page (docs/assets/rehearsal.js).
// Usage: node book/tools/rehearsal_report.mjs research/eyes-scores/rehearsal-rounds.jsonl
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const R = createRequire(import.meta.url)(path.join(here, "..", "docs", "assets", "rehearsal.js"));
const file = process.argv[2];
const rounds = fs.existsSync(file) ? fs.readFileSync(file, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l)) : [];
if (!rounds.length) console.log("REHEARSAL (rung 3): no rehearsal rounds in the cloud yet.");
else {
  const pl = R.passLine(rounds), open = rounds.filter((r) => r.status !== "done").length;
  console.log(`REHEARSAL (rung 3): ${rounds.length} round(s) read, ${open} not finished (open or abandoned, never counted).`);
  for (const l of pl.lines) console.log("  " + l);
}
