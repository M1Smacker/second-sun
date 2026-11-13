# The Tree: everything Second Sun is doing, in one map

**Started 13 Nov 2026 (Ahmed's decision, question round after the T156 result).** Every bug, fix, study, build and idea hangs under exactly ONE node here. The fix and build queues are storage, grouped by these same node numbers. **Nothing is filed without a node**, and `research/tree/tree_check.py` fails if an item has no place. Only the ACTIVE path is worked on; NEXT waits its turn; WAITS names what it waits for; PARKED sleeps until a node above wakes it.

**Rules of the Tree**
1. **The scoreboard decides Petrova work.** A Petrova change counts only if the fixed T156 test (2,000 planted planets, raw light) shows more planets reaching tier 1 *without* more upside-down false alarms. No bench result, no change.
2. **Biggest loss first.** Branch 1 nodes are ordered by how many planets they lose on the scoreboard.
3. **Outside audits (Codex, Fable) only at a version freeze**, not after every fix. Bugs found between freezes are filed on their node and wait their turn unless they break a running result.
4. **One active path at a time.** A new finding goes on its node; it does not jump the queue unless it is bigger than the active loss.

## Goal
**Find a circumbinary planet in TESS data, or prove a clean, measured null.** Both are wins (29 Oct 2026).

## Scoreboard (T156, 13 Nov 2026)
Saturn-like planets (3,000 to 6,000 ppm, 6 to 12 h): **R = 0.27 (0.21 to 0.34)**, so **FIX FIRST** under `research/stage3/G1-RECOVERY-BAR.md`. Old belief "about 4 in 10" was only for planets already inside a searched window.
Where the 222 Saturn-like test planets stop: found but held below tier 1 **53**, outside windows **45**, not found **41**, mask **15**, no safe windows **7**, caught **61**.

## ACTIVE path now
1. Codex finishes its brief 003 report (why each stage loses planets; multi-window study reading). *Waits for Ahmed's "continue" in Codex.*
2. Then **node 1.1**: price each tier-1 flag on the bench, starting with the repeater flag, plus FIX 91; one Petrova 1.1 candidate; bench rerun.

---

## 1. How well we see (Petrova, the engine)
**1.1 Tier-1 flags hold found planets back.** Loss: 53 of 222 Saturn-like; 158 of 439 strong (6,000 ppm or more). The biggest and most fixable. *Status: NEXT (first after Codex's report).*
- NEXT: repeater flag priced on the bench (from the T156 G2 diagnosis: removing it alone frees 99 trials); FIX 91 opposite-sign flag on the real arm only; T34 step check (fires on 51% of lost strong dips).
- NEXT: T157 phase-key and veto synthetic study; FIX 90 veto summary text; FIX 30 and T145 orbit-locked dips (why real dips repeat at the binary phase).

**1.2 Planet falls outside the searched windows.** Loss: 45 + 7 of 222. *Status: NEXT (second).*
- T155 QLP "no safe windows" losses; T137 window table per sector and CCD; FIX 26 coverage hole in sparse fields; FIX 70 QLP windows depend on the manifest; FIX 84 QLP quality bit from sector 56.

**1.3 The detector misses the dip.** Loss: 41 of 222 (570 of 2,000 over all depths, mostly shallow). *Status: ACTIVE (inside Codex 003), then WAITS.*
- ACTIVE: T158 multi-window study (first reading: 41 more dips but upside-down alarms also rise, 22 to 55; not a clean win yet).
- PARKED: FIX 11 longer detrending window; FIX 14 mask-before-detrend; FIX 16 B-lite follow-ups.

**1.4 The eclipse mask eats the transit.** Loss: 15 of 222. *Status: PARKED (small).* FIX 24 G2 ephemeris for the eclipse flags.

**1.5 Blind spot: binaries of 5 to 10 days.** R 0.13 (6 of 48). *Status: WAITS (Codex's report on why).* No item yet; one is filed when the cause is known.

**1.6 False alarms (keep the upside-down count low).** The other side of every fix. *Status: PARKED; each item is priced on the bench when its node is active.*
- T31 depth guard and T33 flare shape (accepted in the 0.9 study, check whether Petrova 1.0 carries them); T32 near-zero noise guard; T35 the 3 h box; FIX 19, 21, 22 (SAP and QLP flux halves).

**1.7 The scoreboard and its tools.** *Status: DONE for now (T156 is the bench).*
- T156 bench (rerun after every candidate change); PARKED: T36 cross-sector plant harness, T109 larger known-planet test (after Petrova 1.1).

## 2. Where we look (the fuel)
**2.1 Census: our own binary list from TESS after sector 26** (about 1,400 good targets, about 1 to 2 planets expected at Kepler's rate). *Status: WAITS on branch 1 (no new fuel into a 1-in-4 engine).*
- T136 Census plan; T139 public EB lists first; T138 transit probability in Horizon; T140 Horizon against the professionals; T148 PLATO count; T152 second FFI product; T153 Gaia DR4 refresh (DR4 due 2 Dec 2026).

**2.2 G1: the last unseen list (552 rows, one shot).** *Status: WAITS: FIX FIRST verdict, then Amendment 4 and a frozen Petrova version that passes the bar.* T37b (a fresh-set test) folds into this.

**2.3 Data and downloads.** *Status: PARKED.* FIX 25 "sector 1751" files; FIX 72 MAST timeouts; T150 the Annex index; T151 machine-learning dataset.

**2.4 Parked new systems.** *Status: PARKED (three-weeks rule of 3 Nov).* T119 Horizon, T120 Vigil, T121 Witness (no-go), T122 research, T123 OMS (deferred), T124 evidence index.

## 3. How we prove it (honesty and statistics)
**3.1 Statistics and controls.** *Status: NEXT for 86 and 87 (they touch how the next result is read).* FIX 86 power line test; FIX 87 gate PASS on empty bins; FIX 88 "floor" wording; PARKED: T101 scrambled control, T129 effective sample size, T117 evidence ladder, T118 negative controls, T54 funnel test.

**3.2 Records, reproducibility and tests.** *Status: PARKED.* FIX 89 amendment times; FIX 83 tests that pass after skip; FIX 85 file encodings; T128 and T142 run record; T130 number-to-file audit; T52 settings read from the run.

**3.3 Leads: how a dip becomes a claim.** *Status: PARKED until a lead exists.* FIX 27 eclipse-timing second key; T46 to T49 lead cards; T106 and T141 linkers; T125 to T127 follow-up, second implementation, novelty; T60 Rabtsevich follow-up (date-driven, after 26 Nov 2026).

**3.4 Going public later.** *Status: PARKED.* T108 playbook; T149 is our upside-down result new.

## 4. Tools and book
**4.1 Book and learning.** *Status: WAITS: the learning rebuild starts after G1 or Census is fully done (Ahmed, 13 Nov 2026).* T160 the Tree as the home page (design rounds first); T131 to T134 learning space, dashboard, Keystone; T113 to T116 rehearsal and spaced re-ask; T57a to T58b chapter checks; T146 Engine Room; T147 one key name; T59c F4 redesign; FIX 73 to 76 chips, Back button, voice, formulas.

**4.2 Search window and control room.** *Status: WAITS: after G1 or Census (Ahmed).* T159 control room on Netlify (plan `research/stage3/CONTROL-ROOM-PLAN.md`); T51, T53, T50; FIX 77 exporter label.

**4.3 Machine, scripts and housekeeping.** *Status: PARKED.* FIX 82 hard-coded paths; FIX 69 preview loop; FIX 78 stale task records; FIX 80 flaky browser test; T55 preview recipe; T143 slim RESUME.

**4.4 Eyes pages.** *Status: PARKED.* T59d, T59e, T59g, T110.

---
**Closed in the 13 Nov clean-up** (text kept in the archives `research/stage3/archive-*-QUEUE-to-2026-11-13.md`): FIX 12, 13, 20, 29 superseded by T156; FIX 68 done; T104, T111, T112, T144 done; T56 a working rule; T59a, T59b, T135, T154 folded into T159.
