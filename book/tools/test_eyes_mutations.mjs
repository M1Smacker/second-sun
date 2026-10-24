// Mutation test for the Eyes strength, hard-card and feedback code: break each file on purpose in one way, and demand that a test notices.
// A test family that still passes on broken code is not testing anything. Usage: node book/tools/test_eyes_mutations.mjs (takes a few minutes)
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url)), assets = path.join(here, "..", "docs", "assets");
const M = [
  // [name, file, [[from, to], ...], test, env variable that points the test at the broken copy]
  ["feedback: the lead lesson peeks at the true label", "eyes-feedback.js", [["const ranked = rank(F, ctx, true);", "const ranked = rank(F, ctx, false);"]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: a false alarm is called a miss", "eyes-feedback.js", [["Not this time:", "Dip missed:", true]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: length control prefers the wrong lengths and has no range", "eyes-feedback.js", [["Math.abs(n - 40) * 0.4 + (n > 44 || n < 36 ? 100 : 0)", "-Math.abs(n - 40) * 5"]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: a near miss is allowed to read as plain noise", "eyes-feedback.js", [["F.near_ratio >= T.near && F.near_ratio < 1 && F.depth_pts < 8", "false"], ["F.depth_pts < 8 && !(F.near_ratio >= T.near)", "F.depth_pts < 8"]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: strength is not the hunt's strength", "eyes-feedback.js", [["({ a: b.a, D: b.w, m: b.m, s: b.s })", "({ a: b.a, D: b.w, m: b.m, s: b.s * 1.3 })"]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: the pre-gap sag is never noticed", "eyes-feedback.js", [["F.pregap_z >= T.pregap", "F.pregap_z >= 99"]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: recent wordings are not avoided", "eyes-feedback.js", [["3 * (seen(0, m) + seen(1, w) + seen(2, l3))", "0"], ["((hash(ctx.cardId + m + w + l3) % 100) / 100) * 1.5", "0"]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["feedback: a number that was never measured appears in the text", "eyes-feedback.js", [["under the hunt's line of 7.`", "under the hunt's line of 8.`"], ["the hunt only keeps 7 or more.", "the hunt only keeps 8 or more."]], "test_eyes_feedback.mjs", "EYES_FEEDBACK"],
  ["hard cards: the quiet card's event is always put at the same place", "eyes-hard.js", [["off = ri(30, WIN - 30 - b.w); s = b.a - off; break; }", "off = 30; s = b.a - off; break; }"]], "test_eyes_hard.mjs", "EYES_HARD"],
  ["hard cards: fake planets are not as strong as they say", "eyes-hard.js", [["const dipDepth = (snr, d, ramp, sigT) => snr / unitSnr(d, ramp, sigT);", "const dipDepth = (snr, d, ramp, sigT) => snr * 0.5 / unitSnr(d, ramp, sigT);"]], "test_eyes_hard.mjs", "EYES_HARD"],
  ["hard cards: the quiet cards are not the best dip of a sector", "eyes-hard.js", [["cands = SS.huntBoxes(sec, P.sigT).boxes.filter((b) => (natural || b.w === wT) && b.a >= WIN && b.a + b.w <= SECTOR - WIN).sort((p, q) => q.s - p.s);", "cands = SS.huntBoxes(sec, P.sigT).boxes.filter((b) => (natural || b.w === wT) && b.a >= WIN && b.a + b.w <= SECTOR - WIN).sort((p, q) => p.s - q.s);"]], "test_eyes_hard.mjs", "EYES_HARD"],
  ["hard cards: decoy gaps removed, so a gap gives the answer away", "eyes-hard.js", [["rnd() < 0.4) {                           // decoy gaps", "rnd() < 0) {                           // decoy gaps"]], "test_eyes_hard.mjs", "EYES_HARD"],
  ["habit: the criterion has the wrong sign", "eyes-core.js", [["criterion = -(zh + zf) / 2;", "criterion = (zh + zf) / 2;"]], "test_eyes_feedback.mjs", "EYES_CORE"],
  ["habit: a band edge is moved (7 counts as under 7)", "eyes-core.js", [['[5, 7, "5 to 7"], [7, 10, "7 to 10"]', '[5, 7.5, "5 to 7"], [7.5, 10, "7 to 10"]']], "test_eyes_feedback.mjs", "EYES_CORE"],
  ["sequencing: a miss comes back too soon (1 to 3 cards)", "eyes-core.js", [["to = at + 3 + Math.floor(rnd() * 3);", "to = at + 1 + Math.floor(rnd() * 3);"]], "test_eyes_feedback.mjs", "EYES_CORE"],
  ["strength: the scale is not the hunt's (1.4826 changed)", "eyes-strength.js", [["const mm = median(good), sig = 1.4826 *", "const mm = median(good), sig = 1.48 *"]], "test_eyes_strength.mjs", "EYES_STRENGTH"],
  ["strength: a box with too few points is no longer skipped", "eyes-strength.js", [["const DURS_H = [3, 4, 5, 6.5, 8, 10, 12, 15], MIN_COVER = 0.8;", "const DURS_H = [3, 4, 5, 6.5, 8, 10, 12, 15], MIN_COVER = 0.4;"]], "test_eyes_strength.mjs", "EYES_STRENGTH"],
];

let caught = 0; const missed = [];
for (const [name, file, edits, test, envVar] of M) {
  const src = path.join(assets, file), mut = path.join(assets, file.replace(/\.js$/, ".mut.js")); let code = fs.readFileSync(src, "utf8");
  for (const [from, to, many] of edits) { if (many ? !code.includes(from) : code.split(from).length !== 2) throw new Error(`mutation "${name}": the text to break is not in ${file} exactly once: ${from.slice(0, 70)}`); code = many ? code.split(from).join(to) : code.replace(from, to); }
  fs.writeFileSync(mut, code);
  try {
    const r = spawnSync(process.execPath, [path.join(here, test)], { env: { ...process.env, [envVar]: mut }, encoding: "utf8", timeout: 170000 });
    const failed = r.status !== 0; if (failed) caught++; else missed.push(name);
    console.log((failed ? "caught " : "MISSED ") + name + (failed ? "   <- " + ((r.stderr.match(/AssertionError[^\n]*/) || r.stderr.match(/Error[^\n]*/) || [""])[0]).slice(0, 110) : ""));
  } finally { fs.rmSync(mut, { force: true }); }
}
console.log(`\n${caught} of ${M.length} mutations were caught by a test`);
if (missed.length) { console.log("NOT caught:", missed.join(" | ")); process.exit(1); }
