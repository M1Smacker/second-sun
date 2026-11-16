---
name: second-sun-method
description: Use in the Second Sun project (D:\second-sun, TESS circumbinary planet search, filter Petrova) at the START of any hard task: judging bench results, deciding what goes into a Petrova version, hunting for lost planets, designing a fix or a pass rule, or reviewing another model's job. It gives the order of work that produced results on 16 Nov 2026, built from the written work logs of Claude Fable (F1, F2, F4) and Codex (jobs 023, 024, 025). For bug checklists and number checks load second-sun-auditor as well; this file does not repeat it.
---

# Second Sun method: the order of work for a hard task

For any Claude model and any Codex model. "The meter" means your own usage panel. Where this file and `CLAUDE.md` or `AGENTS.md` disagree, they win. Checklists for bugs, numbers and stop signs are in the `second-sun-auditor` skill; read its section 0 first.

## The procedure, in order

1. **Read the brief, then only what a script needs.** Cap reading at about 50 KB before the first script. For each file ask: which script will this let me write? Write in the work log what you chose NOT to read.
2. **Write how you could be fooled, before any number (10 minutes).** Three ways this task could give a false good result, and the check that catches each. The three that have bitten here: picking the best of several on the bench that scored them; a rate that rises because the denominator changed; a gain on a meter that cannot see the cost (for example dips that have no upside-down mirror).
3. **Measure the meter after about 15 tool calls, then plan by calls.** On 16 Nov one call cost about 0.15 weekly points at 200K context. Divide what is left by that and give each task a number of calls. Drop the nice-to-have run now, not at the cap.
4. **Reproduce the known number first.** Before any new measurement, make your script print a number that is already on record (B: P 48.11, background 174 real / 79 upside-down; the 52 window losses of T156). If it does not match, stop and find out why. Nothing after that is trusted otherwise.
5. **Ask what the bench cannot see.** Open the code that builds the bench and find the line that decides what counts (the denominator, "observed", "affected", "matched"). Ask which pipeline step runs BEFORE that line. Anything lost before it is invisible to that bench.
6. **Explain every surprise by splitting it, before reporting it.** A surprising number gets one more short script that splits it by the obvious physical variable (host size, binary period, product, era, in or out of a flagged time). Report the split with the surprise.
7. **Reuse checked machinery instead of rebuilding it.** If another job already has a scorer with identity checks, make a private copy, add your options, and keep its assertions switched on. Never write into the other job's folders.
8. **Smoke the WHOLE chain on 3 to 5 items, then run long jobs in the background.** The smoke must go through every stage that the long run will reach, scoring and summary included. Then start the long run and do not watch it.
9. **Write the rule before the run.** Variant definitions, pass rule, seeds and the falsification check go into the work log or the report before the first outcome is read. A check you decide on after seeing the numbers is a description, not a test.
10. **Price both sides of every change.** A fix is judged on planets gained AND on what it lets in, on both arms, in the newly affected data only (events per 100 days there against the rest). A ceiling is not a gain: say "ceiling" and give the realistic share.
11. **Write the verdict line first, in plain words,** then the table, then what was not tested. Label each finding CONFIRMED, LIKELY, UNCERTAIN or NOT TESTED. Say plainly when the target is out of reach.
12. **Save state before every stop:** what is running, where its output is, the exact next command. Commit your own files by explicit path.

## Project rules of the form "if X, do Y before Z"

- If a result depends on the planted-planet population, split it into "planets that can exist on that host" and the rest before quoting it. (130 of the 1,098 reference planets need a body of 2 to 14 Jupiter radii.)
- If a change touches load, quality masks, windows or the eclipse mask, score it on a bench whose denominator is built from RAW cadences before using P. Today's P counts only crossings that survive the quality mask.
- If a change frees planets and adds few upside-down alarms, count the new REAL events too and compare with the usual ratio (about 2.3 real per upside-down event) before calling it safe.
- If a control uses catalogue eclipse times or periods on stars chosen BECAUSE their catalogue timing is bad, replace the control before running it: it cannot fail.
- If two queue items point at the same code line, merge them before briefing a job. (FIX 94 and FIX 101 are both the padding term in `petrova_mask.windows()`; a new job was about to re-bench variants already benched three times.)
- If you plan to release a guard flag, look up its price first (`research/fable-method/F4-VETTING-VOUCHING.md`): planets freed against real and upside-down alarms added.
- If you rebuild anything from neighbour stars' files, check the fence before opening them; spacecraft-level quantities are read from design stars only.
- If a quality flag looks like it removes good data, measure the event rate inside the flagged time on untouched light, both arms, before proposing to drop it. (Scattered-light bit 4096: 8 times the event rate.)
- If a long wait hits its cap, hand off as partial with the job still running and the one command that finishes it, rather than reading half-finished output.
- If a shell heredoc carries backslashes or a long document, write the file with the file tool instead.

## Stop signs

- You are about to quote the top row of a matrix as "the result" on the bench that chose it.
- You are comparing two rates whose denominators are not the same planets.
- A fix "costs nothing": you have not yet looked where its cost would show.
- You have read for 20 minutes and have not run a script.
- Your check passed and you cannot say what output would have made it fail.
- You are choosing a threshold while looking at the events it will judge (see the auditor skill, section 7).

## Worked examples (quoted from the logs)

**1. A surprising matrix, explained by one split (F1).** Codex 023's matrix said the depth cap costs 4.7 points of P. 023's own log had already found the lead: "Of 1,098 trials, 130 have assigned input depths above their host cap". Fable's log: "New: split by whether a planet of at most 2 Jupiter radii could make the planted depth on its host... On the other 968: B 48.40, B+C96 48.31 (cap costs 1 dip), B+C96+DS+M2 51.67, paired change +3.26 [+2.01, +4.66] with background 156 real / 59 upside-down against B's 174 / 79." The reading of the whole matrix reversed, from "every combination is worse than B" to "the full combination is better than B on both planets and alarms". Before looking at a second sample the log fixed the check: "the paired change ... must not be negative ... If it is negative, the planet-bench gain is suspect". It came out +2.92 [+1.85, +4.18].

**2. What the bench cannot see, and a fix that was not free (F2).** Reading the bench generator, not the pipeline, gave the finding: "the planet bench counts a crossing as 'observed' only if the loaded light of the best product has a cadence there, that is AFTER the hard quality mask." A census from raw cadences then counted 606 hidden crossings and a ceiling of 9.7 points. The obvious fix (drop the scattered-light bit) was prototyped with its cost measured in the newly admitted light: 16.9 real and 15.5 upside-down strong events per 100 days against 1.9 and 1.6. The report says "found something, but not a free win" and names the one small rule that IS clean (one-neighbour windows: 2.3 and 3.1 per 100 days).

**3. Audit your own shortcut after the result is in (Codex 024).** "Final coverage audit found a correctness gap in the no-op optimization. In 104 sectors, the untouched model coarsened to one bin or lacked three-cycle phase coverage. An injected eclipse mask can change that coverage, so a baseline no-op alone does not prove an injected no-op." It reran 197 sectors: "left all trial metrics unchanged". The result stood, and now it is known to stand.

**4. A prototype shown to fail, pass, and fail again (Codex 025).** "Fifteen archived 4096 cases fail under the original loader, pass with the prototype, and fail when the policy is reverted as a mutation. This establishes loader support. Searched support and tier-1 recovery remain separate outcomes in the pending bench." Note the last sentence: it does not claim more than was shown.

## The two sets of logs compared

| Step | Codex (023, 024, 025) | Fable (F1, F2, F4) | Which order worked better, with evidence |
|---|---|---|---|
| Rule before run | Always: pass rule, seed and exclusions written into the report before scoring | Hypotheses and variants written before measuring; pass rules written as designs | Same habit. Keep it. |
| Reproduce the known number | 023 reproduced B trial by trial; 025 rebuilt "the original 52 exactly" before tracing | F4 kept 023's identity assertions; summary printed 174 / 79 and 48.11 first | Same habit. Every later number rested on it. |
| Smoke test | 024 smoked generation, not scoring: "The first supervisor finished with a scoring failure after both raw-light campaigns completed" (a variable name clash, found after a 2-hour run) | Each of three long runs had a 3 to 5 item smoke through the last stage; two smokes failed within a minute (an escaped path, a too-strict assertion) and the long runs then ran clean | Smoke the whole chain, last stage included. |
| A surprising number | 023 ran a diagnostic and reported the cause as a note under the unchanged verdict | One more split script, and the split became the headline | Split before reporting: it changed the decision. |
| What the bench cannot see | Stayed inside the given bench (025 traced T156 losses precisely) | Opened the bench generator and asked what is decided before the denominator | Asking it found the blind spot; tracing inside the bench could not. |
| Mutation checks | Regular: "a deliberately asymmetric mutation that was rejected"; policy reverted as a mutation | Weak: failing-first shown (0 of 1,055 scored under the frozen chain) but no mutation of the new code | Codex's order is better here. Add a mutation to every prototype. |
| Waiting | Capped waits, no reading of healthy logs, partial handoff at the cap | Background runs, work on the next task while waiting | Both avoid polling. Start the next task while the machine works. |
| Coverage of own shortcuts | 024 audited its no-op skip and reran 197 sectors | T156 cross-check agreed only roughly; said so, did not chase it | Codex's audit is the better habit when the meter allows. |
| Reading | Reads rules, mailbox and prior scripts fully each time | Read 4 code files and one generator per task, then scripted | Shorter reading reached the first script sooner; no finding was lost by it in these logs. |

Note for fairness: Codex jobs 023 to 025 ran on GPT-6.1-Sol at high effort, not GPT-6-Astra, so this compares these two sets of logs, not the two model families.

## Upkeep
Add a dated line when a step here fails or a new rule earns its place, with the file that shows it. Do not copy rules from the auditor skill; link to them.
