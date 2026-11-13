# The Tree: everything Second Sun is doing, in one map

**Started 13 Nov 2026 (Ahmed's decision, question round after the T156 result).** Every bug, fix, study, build and idea hangs under exactly ONE node here. The fix and build queues are storage, grouped by these same node numbers. **Nothing is filed without a node**, and `research/tree/tree_check.py` fails if an item has no place. Only the ACTIVE path is worked on; NEXT waits its turn; WAITS names what it waits for; PARKED sleeps until a node above wakes it.

**Rules of the Tree**
1. **The scoreboard decides Petrova work.** A Petrova change counts only if the fixed T156 test (2,000 planted planets, raw light) shows more planets reaching tier 1 *without* more upside-down false alarms. No bench result, no change.
2. **Biggest loss first.** Branch 1 nodes are ordered by how many planets they lose on the scoreboard.
3. **Outside audits (Codex, Fable) only at a version freeze**, not after every fix. Bugs found between freezes are filed on their node and wait their turn unless they break a running result.
4. **One active path at a time.** A new finding goes on its node; it does not jump the queue unless it is bigger than the active loss.
5. **Accepted fixes wait on the bench (Ahmed, 13 Nov 2026).** A fix that passes stays in the bench copies; all accepted fixes enter the real Petrova code together at the freeze, each behind a switch, with two proofs then: switches off reproduce 1.0.0 exactly, switches on reproduce the bench numbers. Until then every bench number is a copy-based measurement.

## Goal
**Find a circumbinary planet in TESS data, or prove a clean, measured null.** Both are wins (29 Oct 2026).

## Scoreboard (T156, 13 Nov 2026)
Saturn-like planets (3,000 to 6,000 ppm, 6 to 12 h): **R = 0.27 (0.21 to 0.34)**, so **FIX FIRST** under `research/stage3/G1-RECOVERY-BAR.md`. Old belief "about 4 in 10" was only for planets already inside a searched window.
Where the 222 Saturn-like test planets stop: found but held below tier 1 **53**, outside windows **45**, not found **41**, mask **15**, no safe windows **7**, caught **61**.

## ACTIVE path now
1. **Codex brief 006, everything left on branch 1** (Ahmed's round, 13 Nov 23:30): P planet-level bench (decides G1 under the new `research/stage3/G1-PLANET-BAR.md`, written before any planet number) with a multi-transit combination design study; S short-binary noise fix (node 1.5); W window repair (node 1.2); M mask or support (node 1.4). Brief `research/astra/inbox/006-branch-one.md` on astra/006-branch-one, cap 40 weekly points of its bar.
2. **No freeze yet** (Ahmed).

**Bench so far:** Petrova 1.0.0 R 27.5% [20.7, 33.7]. **Baseline now (repeater rule b plus FIX 91, adopted, not frozen): R 33.3% [25.9, 40.1]**, background real 176, upside-down 83 (Codex 005 part 0, all three gates PASS).
**Codex 005 findings:** A: the +59/-6 real-side change is NOT eclipse leftovers (54 of 56 classifiable sit 2+ eclipse widths away), spread over 33 stars, cause UNCERTAIN, no narrower lock supported. B (node 1.5): all 19 short-period misses are below SNR 7; depth survives detrending; higher noise in short binaries is LIKELY the cause (median best SNR 6.2 vs 9.3, scatter 3,070 vs 2,221 ppm); binary-phase origin UNCERTAIN; ceiling 7.9 points. C (node 1.2): of 52 window losses, 15 are true archive gaps, 21 lost at load, 16 have usable data before the window rule; ceiling 2.6 to 7.0 points. Needed for GO: +16.7 points and a lower bound of 40%; the two biggest ceilings together give 14.9 points even if perfect.

## Road ahead (Claude's estimate, 13 Nov 2026; Codex rounds counted, not promised)
1. **Brief 006** (running next): planet-level P decides G1. One round.
2. **One or two fix rounds** on what 006 finds (likely the multi-transit combination, if it helps). One to two rounds.
3. **T109 real known-planet check** (synthetic bench against real planets), after 006 and its fixes, before the freeze (Ahmed agreed 14 Nov).
4. **Freeze Petrova 1.1** (all accepted fixes into the real code, two proofs, outside audit by Fable or Codex). One round.
5. **G1 preparation and the one-shot G1 search**, then the plain verdict. One to two rounds.
6. **Housekeeping phase** (Ahmed, 14 Nov): fix every bug on the chain Census uses, build the kept tasks (Tree home page, control room, learning rebuild, F4), archive the rest.
7. **Census** (new fuel, about 1,400 stars), (the learning rebuild and the Tree home page move into step 6).
About 4 to 6 more Codex rounds before G1, roughly one to two weeks at this pace if both meters allow.

## Triage of 14 Nov 2026 (Ahmed approved; file `research/tree/TRIAGE-2026-11-14.md`)
Dropped 12 (T37b, T36, T50, T101, T117, T118, T121, T122, T123, T124, T140, T148); merged 8 into 4 (T51 and T53 into T159, T106 into T141, T128 into T142, T57a to T58b into T57); parked 17 with a wake-up trigger; the rest keep a phase: NOW (Petrova via Codex), G1 PREPARATION, HOUSEKEEPING PHASE (after G1, before Census: fix every bug on the chain Census uses, build what is kept, archive the rest), CENSUS. Node lists below may still name dropped tasks; the build queue is the source of each task's status. No cap on the queue size (Ahmed).

---

## 1. How well we see (Petrova, the engine)
**1.1 Tier-1 flags hold found planets back.** Loss: 53 of 222 Saturn-like; 158 of 439 strong (6,000 ppm or more). The biggest and most fixable. *Status: NEXT (first after Codex's report).*
- NEXT: repeater flag (Codex 003 reference-band price: on 17 of the 53, clearing it alone frees 13; it counts every same-kind event in the sector, not repeats of one source, `stage3_core.py` 21, 272, 284); FIX 91 opposite-sign flag on the real arm only (frees 0 in the reference band, a correctness fix); T34 step check (on 18 of the 53 but clearing it alone frees 1: it overlaps other flags).
- NEXT: T157 phase-key and veto synthetic study; FIX 90 veto summary text; FIX 30 and T145 orbit-locked dips (why real dips repeat at the binary phase).

**1.2 Planet falls outside the searched windows.** Loss: 45 + 7 of 222. *Status: NEXT (second).*
- T155 QLP "no safe windows" losses; T137 window table per sector and CCD; FIX 26 coverage hole in sparse fields; FIX 70 QLP windows depend on the manifest; FIX 84 QLP quality bit from sector 56.

**1.3 The detector misses the dip.** Loss: 41 of 222 (570 of 2,000 over all depths, mostly shallow). *Status: WAITS (after 1.1 and 1.5).*
- DONE: T158 multi-window study. Verdict (Codex 003): no demonstrated win. 41 more dips among 570 failures; the 22 to 55 was planted bumps recovered, NOT false alarms (Claude's earlier wording was wrong); no background alarm test exists. Requiring both extra windows to agree gains 1 dip: a low-priority lead only.
- PARKED: FIX 11 longer detrending window; FIX 14 mask-before-detrend; FIX 16 B-lite follow-ups.

**1.4 The eclipse mask eats the transit.** Loss: 15 of 222. *Status: PARKED (small).* FIX 24 G2 ephemeris for the eclipse flags.

**1.5 Blind spot: binaries of 5 to 10 days.** R 0.13 (6 of 48). *Status: NEXT after 1.1.* Codex 003: the loss is BEFORE detection (19 of 48 give no event, 40%, against 13% in other bins); flags are not the cause (6 of 48). Binary variability or residual structure upsetting the detrending is LIKELY, not shown. T161 diagnosis (build queue).

**1.6 False alarms (keep the upside-down count low).** The other side of every fix. *Status: PARKED; each item is priced on the bench when its node is active.*
- T31 depth guard and T33 flare shape (accepted in the 0.9 study, check whether Petrova 1.0 carries them); T32 near-zero noise guard; T35 the 3 h box; FIX 19, 21, 22 (SAP and QLP flux halves).

**1.7 The scoreboard and its tools.** *Status: DONE for now (T156 is the bench).*
- T156 bench (rerun after every candidate change); **AGREED by Ahmed (14 Nov): after brief 006 and its fixes, BEFORE G1 (G1 is one shot): T109 known-planet check** (targets listed in `research/stage3/cbp-census-2026-11-14.md`: 12 transiting systems, all with free TESS data, none in fence A or B; first TOI-1338 and TIC 172900988, whose planets transit in TESS data; the 10 Kepler systems only where their planets are predicted to transit inside TESS sectors, UNCERTAIN until checked) (run the bench chain on the real, published circumbinary planets with TESS data, e.g. TOI-1338 b, to make sure the synthetic bench agrees with real planets); PARKED: T36 cross-sector plant harness.

## 2. Where we look (the fuel)
**2.1 Census: our own binary list from TESS after sector 26** (about 1,400 good targets, about 1 to 2 planets expected at Kepler's rate). *Status: WAITS on branch 1 (no new fuel into a 1-in-4 engine).*
- T136 Census plan; T139 public EB lists first; T138 transit probability in Horizon; T140 Horizon against the professionals; T148 PLATO count; T152 second FFI product; T153 Gaia DR4 refresh (DR4 due 2 Dec 2026).

**2.2 G1: the last unseen list (552 rows, one shot).** *Status: WAITS: FIX FIRST verdict, then Amendment 4 and a frozen Petrova version that passes the bar.* T37b (a fresh-set test) folds into this.

**2.3 Data and downloads.** *Status: PARKED.* FIX 25 "sector 1751" files; FIX 72 MAST timeouts; T150 the Annex index; T151 machine-learning dataset (T150 gets a by-catch extension: IDEA, 14 Nov).

**2.4 Parked new systems.** *Status: PARKED (three-weeks rule of 3 Nov).* T119 Horizon, T120 Vigil, T121 Witness (no-go), T122 research, T123 OMS (deferred), T124 evidence index. T163 eclipse-timing lane, feasibility first (IDEA, 14 Nov; parked until after G1).

## 3. How we prove it (honesty and statistics)
**3.1 Statistics and controls.** *Status: NEXT for 86 and 87 (they touch how the next result is read).* FIX 86 power line test; FIX 87 gate PASS on empty bins; FIX 88 "floor" wording; PARKED: T101 scrambled control, T129 effective sample size, T117 evidence ladder, T118 negative controls, T54 funnel test.

**3.2 Records, reproducibility and tests.** *Status: PARKED.* FIX 89 amendment times; FIX 83 tests that pass after skip; FIX 85 file encodings; T128 and T142 run record; T130 number-to-file audit; T52 settings read from the run.

**3.3 Leads: how a dip becomes a claim.** *Status: PARKED until a lead exists.* FIX 27 eclipse-timing second key; T46 to T49 lead cards; T106 and T141 linkers; T125 to T127 follow-up, second implementation, novelty; T60 Rabtsevich follow-up (date-driven: after 26 Nov 2026 Claude checks the Sector 110 result and tells Ahmed plainly either way; note his candidate is a single-star planet, not circumbinary). T162 exploratory lane for sub-bar events (IDEA, RS-023; PARKED until after G1, then decided with a rule written first, Ahmed agreed 14 Nov).

**3.4 Going public later.** *Status: PARKED.* T108 playbook; T149 is our upside-down result new.

## 4. Tools and book
**4.1 Book and learning.** *Status: WAITS: the learning rebuild starts after G1 or Census is fully done (Ahmed, 13 Nov 2026).* T160 the Tree as the home page (design rounds first); T131 to T134 learning space, dashboard, Keystone; T113 to T116 rehearsal and spaced re-ask; T57a to T58b chapter checks; T146 Engine Room; T147 one key name; T59c F4 redesign; FIX 73 to 76 chips, Back button, voice, formulas.

**4.2 Search window and control room.** *Status: WAITS: after G1 or Census (Ahmed).* T159 control room on Netlify (plan `research/stage3/CONTROL-ROOM-PLAN.md`); T51, T53, T50; FIX 77 exporter label.

**4.3 Machine, scripts and housekeeping.** *Status: PARKED.* FIX 82 hard-coded paths; FIX 69 preview loop; FIX 78 stale task records; FIX 80 flaky browser test; T55 preview recipe; T143 slim RESUME.

**4.4 Eyes pages.** *Status: PARKED.* T59d, T59e, T59g, T110.

---
**Closed in the 13 Nov clean-up** (text kept in the archives `research/stage3/archive-*-QUEUE-to-2026-11-13.md`): FIX 12, 13, 20, 29 superseded by T156; FIX 68 done; T104, T111, T112, T144 done; T56 a working rule; T59a, T59b, T135, T154 folded into T159.
