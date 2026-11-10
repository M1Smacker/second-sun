# Amendment 1 to the Fable brief: scale down (10 Nov 2026, Ahmed's yes)

Ahmed: "Scale it down and remove book audit if you see that it's taking too much... Make sure that the entire audit of Fable is completed within its limits."

**This amendment overrides `01-FABLE-BRIEF.md` wherever they differ.** Everything not changed here still holds.

## Why
In the first run you read the brief and started 4 Fable-priced helpers on history. About 5 minutes later the 5-hour window was full and you stopped at about 02:54. That cost:
- **Weekly Fable:** 0% to 20%.
- **Weekly all models:** 7% to 17%, so Fable's meter probably moves the normal bar at half rate (UNCERTAIN).

Only 2 of the 4 helper reports were saved. No area was started. Reading, not judgement, burned the budget.

## 1. One budget, in normal-bar points
- **Hard stop:** "Weekly · all models" at **40%**. It was 17% at 09:35 on 10 Nov, so about **23 bar points** are left for all of run 1 (about 46% of the Fable meter at the observed rate).
- The "30 on Weekly Fable" line in brief 2.2 is deleted. Watch the normal bar.
- Ahmed's own chats also move this bar. If it climbs faster than your own use explains, keep to the line anyway.
- The 14 Nov fix step (brief 5.4) keeps its own budget: at most **8 bar points**, before the reset.

| Area | Budget (bar points) |
|---|---|
| P Petrova | 7 |
| N Numbers | 5 |
| S Stars and data | 5 |
| R Process (includes a tools privacy-leak check) | 2 |
| L Lessons skill and blind bug test | 2 |
| Report, work orders, decision rounds (reserved, never spent elsewhere) | 2 |
| **Total** | **23** |

**Pacing rule:**
- Read the meters at the start and end of each area, and log a row in `fable-ledger.md`.
- If an area hits its budget, stop it. Write its findings so far, mark the unfinished parts "NOT DONE, work order for Sonnet", and move on.
- Unspent budget rolls forward to the next area.
- At 38% on the bar, go straight to the report.

## 2. Book audit removed
- Brief 3.5 is dropped, apart from one item: the tools privacy check (could a star ID or event time leak publicly?). It moves into area R, about 0.5 points, code reading only.
- The book, learning track, Eyes correctness and flaky tests go into the report as one line: "not audited, budget".

## 3. Reading: cheap helpers, no re-reading
- **Helpers run on Sonnet** (Agent tool `model: "sonnet"`), never on Fable.
- At most **2 helpers at a time**. Each gets a tight question and a cap of about 25 tool calls, and returns at most about 1 page.
- **Do not re-read the history.** Use the two saved helper reports as your history:
  - `H1-resume-rules.md` and `H2-mistakes-ledger-queues.md`, in your old scratchpad: `C:\Users\hanzl\AppData\Local\Temp\claude\7e0db8f3d55f49f4\4e166baa-75ae-4de1-a35e-2891ae1a25ea\scratchpad\`.
  - First copy them to `evidence/history/` in this folder.
  - H3 and H4 were lost. Do not redo them.
- The full reading list in brief 3.0 is replaced by **reading on demand**: open a note only when a finding needs it.
  - No full `git log`. Use `git log --oneline` with grep for a topic when needed.
  - No `wave-*` folders. No compass reviews except the 8 Nov handoff verification.
- **Fable reads the core code itself:** `detect_v2.py`, `stage2_search.py`, `stage3_core.py`, `stage3.py`, `vopts.py`. Its judgement is what we pay for.
- Keep your own context lean. Write STATE.md often.

## 4. Scope cuts inside the areas
- **P:**
  - Keep the four known doubts (FIX 84, S2/WO-14, FIX 70, the test gaps) and a read of the core chain.
  - The known-planet test: TESS planets on real light only if the light is already on D: (`data\known`). The Kepler injections become a work order for Sonnet.
  - "Question everything" becomes half a page.
- **N:**
  - Re-derive the Census odds, the S2 interval, the Horizon reach (with the c 0.9 trim), and the faint-star value 0.21.
  - Spot-check the rest by reading.
- **S:**
  - Keep: the bright-pool sizing from the files we already have (Gaia counts, CALNet, Prsa, TTC, 2-minute lists), a check of Census stage 2 (T139), and draft G4/G5 star-list rules.
  - The FFI-door redesign becomes a short memo, not a full preregistration.
  - M dwarfs and Gaia DR4 get one short research question each.
  - The other missions get one short research pass, for unsearched data only.
- **Ideas and roadmap:**
  - Outside-the-box ideas: top **3** in depth, others one line each.
  - The 2027 roadmap becomes a half-page sketch.
- **Research:** about 15% of each area's budget at most, with the stint cap set by tool calls.
- **R:**
  - Rules and memory: a merge list for the skill.
  - Queues: dead and duplicate items only.
  - Tests and reproducibility: the top 5 problems.
  - Cost per result: half a page.
  - The pending 8 Nov decisions: one recommendation line each.
- **L:**
  - The skill stays: SKILL.md tight, plus at most 2 reference files.
  - The blind bug test drops to **4 planted bugs**.

## 5. Unchanged and still most important
- The audit changes nothing. Every brief 1.x rule still holds.
- Every finding gets a work order Sonnet 5.5 Extra can run cold (brief 5.2). Short is fine; complete is required. Unfinished parts become work orders too.
- One chat line per area, the full report in chat, ask-tool decision rounds, labels, no en or em dashes.

## 6. Restart checklist
1. Read this amendment, then brief sections 1, 5 and 6 again. Skip the rest unless needed.
2. Read the meters, log a ledger row, and update STATE.md.
3. Copy H1 and H2 to `evidence/history/`.
4. Send one chat line: "Fable resumed under Amendment 1, bar X%, Fable meter Y%."
5. Areas P, N, S, R, then L, the report and the rounds.
