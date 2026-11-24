// Twinlight answer grader (learn.js num and same), run by publish_book.ps1 step 2j (Claude, 24 Nov 2026; FIX 104 from Codex 034b F5).
// Extracts the shipped functions unchanged and checks typed answers: fractions, units, thousands commas, words, and things that must fail.
// Shown to fail on the code before FIX 104 (5 of 12 fraction and word cases).
import fs from "node:fs";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const src = fs.readFileSync(fileURLToPath(new URL("../docs/assets/learn.js", import.meta.url)), "utf8");
const s = src.indexOf("  const num = "), e = src.indexOf("  const dueKey =", s);
if (s < 0 || e < 0) { console.error("grader functions not found in learn.js"); process.exit(1); }
const c = {};
vm.createContext(c);
vm.runInContext(src.slice(s, e) + "\nthis.num = num; this.same = same;", c);

// [typed, answer key, tolerance, expected, unit]
const cases = [
  ["1/2", "0.5", 0.03, true], ["1 / 4", "0.25", 0.04, true], ["3/4", "0.5", 0.03, false], ["1/0", "0", 0.03, false],
  ["1/2 AU", "0.5", 0.03, true, "AU"], ["1/2 km", "0.5", 0.03, false, "AU"], ["1/2/3", "0.5", 0.03, false], ["alert(1)/2", "0.5", 0.03, false],
  ["Yes!", "yes", 0.03, true], ["no!", "no", 0.03, true], ["maybe", "no", 0.03, false],
  ["2,970", "2970", 0.04, true], ["2.35", "2.35", 0.02, true], ["2.6", "2.35", 0.02, false], ["43 %", "43", 0.02, true, "percent"],
  ["11.88 days", "11.88", 0.01, true, "days"], ["11.88 km", "11.88", 0.01, false, "days"], ["1.6e6", "1636000", 0.03, true], ["0,5", "0.5", 0.03, true],
];
let bad = 0;
for (const [typed, want, tol, expect, unit] of cases) {
  const got = c.same(typed, want, tol, 0, unit || "");
  if (got !== expect) { bad++; console.log(`UNEXPECTED: "${typed}" against ${want}${unit ? " " + unit : ""}: ${got}, expected ${expect}`); }
}
console.log(`learn grader: ${cases.length} cases, ${bad} unexpected`);
process.exit(bad ? 1 : 0);
