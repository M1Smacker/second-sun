// Prints Ahmed's Eyes scores from a rounds file (one JSON round per line), using the SAME scoring code as the book (docs/assets/eyes-core.js).
// Usage: node book/tools/eyes_report.mjs research/eyes-scores/rounds.jsonl
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const E = createRequire(import.meta.url)(path.join(here, "..", "docs", "assets", "eyes-core.js"));
const file = process.argv[2];
const rounds = fs.existsSync(file) ? fs.readFileSync(file, "utf8").split("\n").filter(Boolean).map((l) => JSON.parse(l)) : [];
const pc = (k, n) => (n ? `${k}/${n} (${Math.round(100 * k / n)}%)` : "none yet");
const out = [];
if (!rounds.length) { console.log("No Eyes rounds in the cloud yet."); process.exit(0); }

const by = (m) => rounds.filter((r) => r.mode === m);
const done = rounds.filter((r) => r.status === "done");
out.push(`EYES SCORES  (${rounds.length} rounds: ${["practice", "test", "real"].map((m) => `${by(m).length} ${m}`).join(", ")}; ${rounds.length - done.length} abandoned)`);
out.push(`First round ${E.fmtDate(rounds[0].t0)}, latest ${E.fmtDate(rounds.at(-1).t0)}. Devices: ${[...new Set(rounds.map((r) => (r.device && (r.device.label || r.device.id)) || "?"))].join(", ")}.`);

for (const m of ["practice", "test"]) {
  const rs = by(m); if (!rs.length) continue;
  const s = E.summarize(rs.flatMap((r) => r.a));
  out.push("", `${m.toUpperCase()}: ${rs.length} round(s), ${s.n} curves: ${s.right} right, ${s.wrong} wrong, ${s.unsure} not sure (${Math.round(100 * s.right / s.n)}% right)`);
  out.push(`  clear dips found ${pc(s.clearFound, s.clear)} | faint dips found ${pc(s.faintFound, s.faint)} | quiet curves called a dip ${pc(s.falseAlarms, s.quiet)} | odd things named right ${pc(s.oddSpotted, s.odd)}${s.oddCalledDip ? ` (called a dip: ${s.oddCalledDip})` : ""}`);
  const lastN = rs.slice(-5), t = E.summarize(lastN.flatMap((r) => r.a));
  out.push(`  last ${lastN.length} round(s): ${Math.round(100 * t.right / t.n)}% right, clear dips ${pc(t.clearFound, t.clear)}, false alarms ${pc(t.falseAlarms, t.quiet)}`);
}
out.push("", "RECENT ROUNDS (newest first):");
for (const r of rounds.slice(-8).reverse()) {
  const s = r.s || E.summarize(r.a);
  out.push(`  ${E.fmtDate(r.t0)}  ${r.mode.padEnd(8)} ${String(r.a.length).padStart(3)}/${String(r.n).padEnd(3)} right ${s.right} wrong ${s.wrong} unsure ${s.unsure}  dips ${s.dipsFound}/${s.dips}  false alarms ${s.falseAlarms}/${s.quiet}  ${r.status}`);
}
const days = {}; for (const r of rounds) days[E.localDay(r.t0)] = (days[E.localDay(r.t0)] || 0) + r.a.length;
out.push("", "CURVES PER DAY: " + Object.entries(days).map(([d, n]) => `${d} ${n}`).join(", "));
const p = E.passLine(rounds);
out.push("", "PASS LINE (official test, Standard):", ...p.lines.map((l) => "  " + l));
console.log(out.join("\n"));
