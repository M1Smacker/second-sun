# One-page verdicts and cross-cutting answers, RS-004 (3 Nov 2026, Sonnet 5.5 Extra, cap 1.5)

Sources: `vigil-literature-2026-11-03.md` (RS-001), `horizon-literature-2026-11-03.md` (RS-002), `witness-literature-2026-11-03.md` (RS-003), `research/compass-reviews/2026-11-03-observatory-memory-system.md` (OMS). Freeze in force: no new system gets a design until the research verdicts are in and the G3 result is read (Ahmed, 3 Nov 2026). Labels as before.

## 1. Verdicts, one per system

| System | Verdict | One reason | Cost now | Needs |
|---|---|---|---|---|
| **Horizon** (T119) | **GO, cheaper** | The planting engine and a crude ceiling calculator already exist; the same method is published (Oddo 2026) so ours is comparable | about 3.0 plus T107 first (about 0.3) | Ahmed: nothing new (radius default kept; he may prefer the 2 to 16 range) |
| **Vigil** (T120) | **CHANGED, go later** | Data supply is real but thin and late (SPOC about 25 days, QLP late, 100 to 230 new star-sectors a sector); p-value claims are not possible; predictions work only with two events | design about 1 after Horizon, build about 3 to 5 (UNCERTAIN) | Ahmed: version (Q2), what he owns for a cloud step |
| **Witness** (T121) | **NO-GO for now** | Narrowly fails its own pre-written kill rule (6 of 40, p 0.0139); channels flag real transits as readily as false alarms (2 of 9) | 0 | none; reopen at 150 control events |
| **OMS** (T123/T124) | **DEFER; evidence index kept** | Most of it exists as files; almost no labelled real artifacts | index about 0.8 inside Loom phase 4 | none |

Plain order of work that follows: Q1 to Q4 answered, then G3 prepared and searched, Horizon R0 text and the G3 preregistration addendum committed BEFORE the G3 result is opened, then Horizon runs, then Vigil design only if Horizon and the 0.9 decision are in.

## 2. Parked ideas (T-1 to T-3, N-1 to N-3, S-1)

- **T-1 answered, CONFIRMED (rehearsal.js and VESPER-VERSIONS.md read).** The rehearsal answers are planet, eclipse, flare, instrument, step, noise. They map many-to-one onto Vesper's nine flags: eclipse to `c5` and `ecl_overlap`; step to `step` and `ramp`; instrument to `gap_dump` and `common`; noise to `repeater` and `dominated`; flare has no flag in 0.8.0 (the flare-shape check `fl` was accepted on development in the 0.9 study, not frozen); planet is tier 1 with no flag.
- **T-2 answered by arithmetic.** To test whether Ahmed's eye beats the flags on the same items with McNemar's test, 80% power against a 70/30 split of the disagreements needs about 47 items where they disagree. If they disagree on 15% of items, that is about 310 items, roughly two full decks (a deck is 8 sessions of 20).
- **T-3 answered, reasoning (LIKELY).** The page shows no flags and the truth only after the answer is locked (the page tests include "panels cannot leak the truth"), so his labels stay independent as long as the lessons teach shapes, not flag names. Risk: he may learn the flag rules from the lesson text; keep flag names out of the rehearsal.
- **Twin Test verdict:** parked; needs about two full decks of his answers after the training changes (T113 to T115). Cost then about 0.5.
- **N-1 answered, rough.** A pattern count (`N of M` or `x%`) over the book pages finds about 80 hand-typed numbers (an upper bound: not all are measured results); 30 pages already use claim tokens (207 chips).
- **N-2 answered, CONFIRMED.** `book/hooks.py` already resolves `{{claim:ID}}` tokens from `book/data/claims.csv` and fails the build on duplicate ids or unknown labels, so a second token type that reads numbers from a results file and fails when the file is missing or older than a rule is a small extension (about 1.0, UNCERTAIN). It is not a new database.
- **N-3 answered:** it would read the Loom phase 4 status JSON; do it after Loom phase 4. Verdict: parked, low priority.
- **S-1 answered, reasoning:** a generator for the resume file would stop clock slips (`mistakes.md` has the 19 Oct entry), but the anchor file works; verdict parked.

## 3. Cross-cutting (X-1 to X-7)

- **X-1 dependency order.** T107 (host radii, 0.3) before Horizon; Loom phase 0 (windows table, with the G3 reference-windows answer Q1) before the G3 search and before Horizon's coverage step; Q2 (version) before the G3 search and before Vigil's protocol; Horizon R0 text and the G3 preregistration addendum before the G3 result is opened; Loom phase 4 (status JSON) before Vigil's runner, the evidence index (T124) and the Numbers Desk; Vigil's design needs Horizon's meter for its yield line. Witness blocks nothing.
- **X-2 kill criteria written now (before more work).** Horizon is killed if, in the reality check, planted recovery overstates real recovery by more than a factor of 2 on at least 2 known planets and the realism arm cannot close the gap. Vigil is killed if, over the last 12 sectors, fewer than 300 new star-sector products a year reach us, or TESS ends before the protocol has produced 6 monthly runs. Witness: applied and killed (RS-003).
- **X-3 what the book may claim.** Horizon: "an upper bound on what the search could have seen, not a measurement of how common planets are", with scenarios (coplanar, isotropic) shown. Vigil: "we look at new sectors about a month after they arrive; counts are public, leads stay private". Witness: "tested on 40 false alarms and 9 real transits, did not separate them, not built".
- **X-4 upkeep.** Vigil: monthly review about 0.3 point (plan figure); local only: no further cost; with a cloud job add the 60-day keep-alive, a secret rotation and checks of the runner image, about 0.1 a month (UNCERTAIN).
- **X-5 claims and the check that could have failed.** Control stable per sector (dispersion index: could have been high; it was 1.12 sealed, 2.28 development), supply and lag (MAST metadata: could have been dense; it was thin), Witness (a control that nearly passed), Horizon floor (an observed table), Horizon reach (the TOI-1338 b reality check, not yet run). Claims resting on my reasoning alone, flagged: the ledger scope (two-event leads), the cloud-counts-only design, the ceiling recipe with a background, the 0.8% versus 10% tension.
- **X-6 what Ahmed has to provide or decide (one list).** (1) Q1 to Q4 for G3 (below). (2) Vigil version (inside Q2). (3) Whether he has an always-on device or a card he would use (V-C11), and whether he will create a private GitHub repository and set its secrets himself (V-C3, V-C4). (4) A time for the open questions (RS-005 covers most). (5) His call on Horizon's radius range (default kept) and on adding the 2 to 16 range for comparability. (6) The permission to fetch the small TESS Cycle 9 target lists, if he wants V-A4 answered. No account needs to be created by me.
- **X-7 stop lines.** Each research stint stops at its cap; what is unfinished is filed as open (research-sessions.md), not rushed.
