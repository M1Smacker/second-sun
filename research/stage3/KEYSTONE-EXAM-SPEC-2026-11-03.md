# Keystone: the exam for the second key (specification, 3 Nov 2026, late evening)

Name: **Keystone** (provisional; the stone that locks an arch, and it is the key step. Ahmed can rename it). Idea from Ahmed, 3 Nov 2026: a full exam he takes once the learning track is done, so that he is qualified as the second key and, if Claude Code is ever gone, can continue the project himself ("he does not have to learn it exhaustively"). He asked for a very detailed file in the build list and for me to gather facts and data that would qualify him.

STATUS: specification only. Nothing is built, nothing is in the book. It cannot be taken before the learning track is finished; it is built after the Learning Space check engine (T133 stage 3). Research stint RS-009 (cap 1.5, written in `research/research-sessions.md`). Labels: CONFIRMED (read in a file or paper), LIKELY, UNCERTAIN, NOT TESTED.

## 1. What "second key" means here (our own rules, CONFIRMED)
- Rule C11 in Chapter 10: "two keys: Claude's analysis passes and you agree" (`book/docs/book/10-vetting.md` line 49). The Candidates page: a candidate "needs two keys before it goes anywhere: my analysis, and your own check". Chapter 14: step 1 is "Two keys: my analysis and your own check both pass". `LEADS-RULES.md` stage 5: a Candidate only by two keys; the page never promotes by itself. `CLAUDE.md` and Chapter 13: two keys before any submission.
- Learning level L6 names the goal: "being the second key, someone who can check a candidate independently" (`learn/index.md` line 6). Check L6-3: "You independently check a candidate and decide whether you agree, before anything is submitted. Both keys must turn."
- Ahmed's rule tonight: "a key is somebody who knows everything about our project inside out", read as: can explain, reproduce and challenge every decision rule and kind of number, not recite every file. The new second goal: continue the project alone.
So the exam certifies two separate abilities, and passing needs both: **K, the key duty** (judge a lead independently, including saying no to Claude) and **C, continuity** (run, read and safely extend the project without Claude Code).

## 2. Facts gathered that bear on the standard
Professional practice, read in the paper (Guerrero et al. 2021, ApJS 254, 39, arXiv 2103.12538, text read on the ar5iv copy on 3 Nov 2026): in the Prime Mission the TESS Science Office examined 55,281 SPOC two-minute candidate signals (TCEs) leading to 17,296 for manual vetting; about 105,400 TCEs from 82,490 full-frame targets leading to 14,629; the whole mission yielded 2,241 TOIs of which 1,676 were not later ruled out as false positives. The workflow has an automatic triage (TESS-ExoClass sorts TCEs into Tier One, Two, Three by warning flags and, per the paper, "borrows heavily" from the Kepler Robovetter), then data validation reports with centroid and difference-image tests, QLP multi-aperture depth comparison (a depth that grows with the aperture size usually points to a nearby source, in the paper's account), a match against catalogues of known eclipsing binaries, and manual vetting by people. CONFIRMED for the statements above; I did not read the paper's odd-even or per-test pass criteria. Take-away for the exam: a second key does not need to rebuild the pipeline, but must be able to read these diagnostics and use the same kinds of tests our tools provide.
Our own record (CONFIRMED in files):
- Vetting rules C1 to C11 (strength, robustness, shape, duration, not an eclipse, not a neighbour, not the spacecraft, independent data, physical size, circumbinary smoking gun, two keys).
- Lead stages 1 to 5 and the six checks on a lead card; check 6 (pixel level, background, neighbours) is "NOT BUILT" in the tool.
- Mission readiness shows the tools behind the second key's checks are partly manual: "Pixel check as an automatic tool" credit 0.25 (a hand-run lab, Lab 7) and "Neighbour check with catalogue positions inside the tool" credit 0 (`book/progress/mission.yml`). So today the second key does the pixel and neighbour check by hand: it must be taught and examined.
- His existing readiness ladder for judging dips by eye: the official test (30 curves; pass line 85% of clear dips found and at most 1 in 10 quiet curves called a dip, over 60 curves, 2 rounds, 2 days), the HARD test, and the Rehearsal in the real layout; 27 of 30 on 1 Nov (standard line close; hard and rehearsal rungs open). Keystone does not repeat these: it requires them passed.
- The record of our own failures: 15 logged mistakes in five patterns with rules (Chapter 15, 7 lessons), including a wrong number that a lab caught and the 82.7% mis-description found tonight. A real second key must be able to catch a mistake of Claude's.
- A public worked example of the opposite discipline: Rabtsevich's preregistration with four outcomes (recovered, inconsistent, excluded, insufficient; "excluded" needs sensitivity of at least 95%; RS-007).
- Practical facts a continuing owner needs (Chapter 13): the folder map, the registers (decisions, mistakes, claims), the safety rules (nothing on C:, no secrets in the repo, downloads over 20 GB need his OK, nothing outward without his OK, two keys before submission, never click the live Eyes page), git and the book publish script, frozen versions and `g3_run.py check`.

## 3. Competency domains (what he must be able to do)
Weights are shares of the written core; the practical, case and viva parts have their own lines (section 5). "Where taught" is the level in the learning track; "gap" means I could not find it taught well, to verify with his question list.

| Domain | Must be able to | Where taught | Gap or check |
|---|---|---|---|
| D1 Light curves and data | open a light-curve file, read TIME, FLUX, QUALITY; turn a dip into ppm and percent; dip depth to planet size; dilution | L0 to L2 | worked examples exist; notation questions NOT TESTED |
| D2 Noise and statistics | SNR, why 7, white vs red noise, look-elsewhere, upside-down control and why it over-counts, why scrambled controls fail for single dips | L3 | L3 has 6 checks |
| D3 Two-sun orbits | why crossings wander, critical period, the circumbinary smoking gun, why at most two transits fit in a sector | L4, L6 | L6 check 5 arithmetic to fix (corrections list C7) |
| D4 Our detector and its limits | box 3 to 20 h filter, tiers 1A/1L/1B, flags, completeness (found x kept), what a clean null means, freezing, preregistration, sealed vs development | L3, L5 | 82.7% description to fix (C3, C4, C6) |
| D5 Vetting and the second-key check | apply C1 to C11 to a case; do the pixel and neighbour check by hand (Lab 7); look a star up (TOI, known host, eclipsing binary); decide agree / disagree / need more, with written reasons | L5, L6 | tools partly manual (mission.yml); casebook not written |
| D6 Honest reporting | labels, nulls, not overclaiming, lead vs candidate vs claim, publishing order (write-up first, then ExoFOP), credit and AI disclosure, how to read another amateur's claim | L6, After | Chapter 14 covers it; RS-007 adds the four-outcome idea |
| D7 Running the project alone | clean shell, venv, D: paths, run the book build, run a check, read a scorecard, find a decision or mistake, commit, publish, restore state after a gap, ask another AI for help and verify its answer | After L6 (Ch 13 to 15) | no "if Claude is gone" runbook exists (to write, section 6) |
| D8 Judgement under uncertainty | decide what to do when a result contradicts, a check is missing or Claude is wrong; stop rules | all | tested mainly by cases and viva |

## 4. Exam format (five parts, taken in several sittings, not one day)
A. **Core written** (closed book, in the Learning Space check engine): about 60 items drawn from a bank of about 120 (two versions of each item so a retake is not memorised): choice, numbers with tolerance, pick the graph, interpret an observation. Covers D1 to D6.
B. **Practical cold run** (open book, own PC, Claude not used): six tasks, each with a written pass condition, for example: (1) from a clean shell, check a frozen version with `g3_run.py check` and say what the output means; (2) run `look_event.py` or the lab on a planted example and report the numbers; (3) find a number printed in the book and trace it to its file and key; (4) find the decision that froze the settings and the mistake it came from; (5) build the book locally and read the check output; (6) write the Candidates register entry for a planted case. Covers D7.
C. **Case panel**: six cases built only from planted fakes and public known objects (never a real private event), each with the evidence a real lead would carry. Two are genuine-looking but correctly "need more", one is a known eclipsing binary leftover, one is a neighbour blend, one is a gap-edge artefact, one is clean. Two cases are built from Claude's own logged mistakes: the correct answer there is to disagree with Claude, which is the point of the second key. Outcomes: accept for the second key, reject, or insufficient (modelled on the four-outcome rule). The answer key is written and dated before he sees the cases.
D. **Viva (written, in his own words)**: six short answers to a reviewer's questions ("why is a clean null a win?", "why 7?", "what is frozen and why?", "what is a lead, a candidate, a claim?", "what would make you say no to Claude?", "what do you do first if you find nothing is running?"). Scored against a rubric by Claude and, for the item bank and key, by an outside model's review (Compass), because Claude both writes and marks the exam and that is a conflict of interest.
E. **Gates from the existing ladder**: the official, hard and rehearsal eye tests passed; Part B's runbook (section 6) written by him and followed once by a "fresh" reader.

## 5. Standards (written before anyone takes it)
- Criterion-referenced, not curve-based. Core written: at least 85% overall and at least 70% in each of D1 to D6. Practical: all six tasks pass. Cases: at least 5 of 6 right and NO false accept of a planted fake or of a known binary. Viva: every answer scores "adequate" or better on the rubric.
- "Must-not-fail" items (any miss fails the exam until retaken): never submit or publish without two keys; never click the live Eyes page or write to the real database from a test; no secrets in the repo; nothing outward without his OK; do not retune a frozen setting after seeing results.
- Retakes: after 7 days, different item versions, different cases. No score is hidden or reset.
- The pass is recorded as a dated entry (version of the exam, scores, the standards used) in a register and, if the mission file allows, as an evidenced readiness item; the page cannot award it by itself (same rule as Candidates).
- What it does NOT certify: that the project's science is right (that is the registers' and the sealed tests' job), or that he can do research alone. It certifies that he can be the second key and keep the project running.

## 6. By-products to build with it
- `RUNBOOK-WITHOUT-CLAUDE.md`: a one-file manual written for him, tested by following it cold (what to open, which commands, where things live, what never to touch, how to get help from any other AI and how to verify its answer with the "verify before concluding" rule).
- A **vetting casebook**: the six case-panel cases plus four taught examples with the reasoning shown (the teaching version of Part C, shown before the exam).
- A pass register: `research/keystone-register.md`.

## 7. Where it fits and what it depends on
Depends on: the Learning Space stages 1 to 3 (check engine, `checks.yml`), the finished track and its question list from Ahmed, the three eye-test rungs, the corrections list applied. Does not duplicate: the 40 level checks (the bank reuses them), the Eyes ladder, mission readiness. Order: after the track is done and the Learning Space check engine exists; the casebook and runbook can be written earlier.
Risks: (1) writer and marker are the same model (mitigation: an outside review of the bank and key, answer key dated before use); (2) a memorised bank (mitigation: item versions, cases, viva); (3) scope creep to "knows everything" (mitigation: the competency table is the scope); (4) the exam passes him while a tool is still manual or missing (mitigation: the pixel and neighbour tools are listed as known limits in the exam itself).

## 8. Cost (UNCERTAIN, ledger-based gut)
Item bank of about 120 items with feedback and an outside review: 2 to 3. Practical drills and scripts (planted cases, the six tasks): 2 to 3. Case panel and casebook: 2 to 3. Runbook and its cold test: 1 to 2. Delivery inside the check engine: 1 to 2. Total about 8 to 13 points, spread over days after the Learning Space stage 3.

## 9. Open points for Ahmed
Name (Keystone or another); the standards in section 5; taking it in sittings; whether the viva may be spoken to Claude instead of written; whether a second reviewer outside Claude should mark the viva.

## Sources
Guerrero et al. 2021, "The TESS Objects of Interest Catalog from the TESS Prime Mission", ApJS 254, 39, arXiv 2103.12538 (ar5iv text read 3 Nov 2026). Our files cited above. The 2 Nov learning note (`research/learning-and-checking-literature-2026-11-02.md`, read from search summaries only, not CONFIRMED) for practice testing and mastery checks.
