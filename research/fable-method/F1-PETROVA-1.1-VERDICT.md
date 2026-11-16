# F1 verdict: what Petrova 1.1 should be (Fable, 16 Nov 2026; a proposal, nothing is frozen)

**Verdict in one line: no combination can be frozen today, and none is near the 0.75 bar. The best candidate is the adopted set B plus the depth cap (FIX 96), the dump-shape rule (DS) and the eclipse-timing change (FIX 94, form M2): it finds about 3.3 points more planets than B (95% interval +2.0 to +4.7) with FEWER alarms on both arms (156 real / 59 upside-down against 174 / 79), which gives P about 0.52, still 23 points short of 0.75.** Two of its three levers (DS and M2) also let in dips that only exist on the real arm, so each needs its guard and the fresh-bench test below before a freeze.

Names: P = share of test planets caught, on the 1,098 planted planets of Codex 006. B = today's adopted rules. C96 = FIX 96, hold any dip deeper than a planet of 2 Jupiter radii could make on that star. DS = dump-shape rule (release some dips held for sitting near a thruster firing). M1, M2 = the two FIX 94 forms that stop the eclipse mask blanking whole light curves (M1: timing padding off; M2: windows moved to the sector's own measured eclipse offset, padding capped at the eclipse width). All numbers below are bench copies on development stars; scripts in `data/fable/f1/`.

## 1. The question Claude asked first: does the depth cap really cost 4.7 points? No. (CONFIRMED)
Script `f1_subpop.py` re-scores Codex 023's saved outcomes, split by whether the planted depth is possible for a planet of at most 2 Jupiter radii on that host.

| Planets | n | B | B+C96 | B+C96+DS | B+C96+M2 | B+C96+DS+M2 | change of the last against B (paired, 95%) |
|---|---|---|---|---|---|---|---|
| All 1,098 (the bar's fixed bench) | 1,098 | 48.11 | 43.44 | 45.11 | 44.80 | 46.49 | -1.61 (-4.15 to +0.76) |
| Possible planets (within cap, or radius unknown) | 968 | 48.40 | 48.31 | 50.20 | 49.76 | **51.67** | **+3.26 (+2.01 to +4.66)** |
| Impossible planets (above cap) | 130 | 45.2 | 7.3 | 7.3 | 7.9 | 7.9 | -37 |

- The 130 sit on 60 big stars (radius 2.7 to 18 Suns). A 3,000 to 6,000 ppm dip there needs a body of 2 to 14 Jupiter radii (median 2.7): a brown dwarf or a star, not a planet. B "finds" 45% of them, and C96 correctly holds them. So the 4.7-point loss in 023 is the cap doing its job on test planets that cannot exist. On planets that can exist the cap costs 1 dip in 968 (-0.10 point).
- Second sample, rule written in the work log before looking: on the T156 bench (2,000 single dips, other planets) limited to possible depths, the same combination is +2.92 points (+1.85 to +4.18) on all trials and +1.00 (0.00 to +2.94) on the 203 Saturn-like ones. Same direction and size. (T156 was scored by 023 too, so this is support, not the fresh-seed test.)
- **What Ahmed must decide (I cannot):** the bar file fixes the 1,098 as the reference. I recommend a new dated bar file that defines the reference planets physically (depth drawn from the planet size, at most 2 Jupiter radii on the host radius), written BEFORE the fresh bench is drawn. This is not a trick to raise P: on today's numbers B itself moves only from 48.11 to 48.40. Until he decides, every result is quoted on both.
- Two open details on the cap, to measure before a freeze (TEST MORE): (a) one possible planet was lost because its measured depth (75% to 105% of the cap) scattered over the line; a margin fixed from physics, not from events (a 7-sigma dip has about 14% depth error, so 1.5 x cap is 3 sigma) should be benched for what it gives back to the background; (b) the cap is switched off when the star has no catalogue radius, and the biggest leftover eclipses in section 3 pass through exactly there. A fallback radius (the most generous of the four radius sources already checked in `research/stage3/fix96/`) should be benched.

## 2. Verdict per lever
| Lever | Planets (paired, possible planets) | Alarms | Verdict |
|---|---|---|---|
| C96 depth cap | -0.10 (1 dip) | real 174 to 124, upside-down 79 to 53 | **ADOPT at the freeze**, with the two details above benched first |
| DS dump-shape | +1.89 (+1.06 to +2.81); T156 +1.8 | with C96: +19 real, +3 upside-down | **TEST MORE**: gain is real, but see section 3; needs the pointing guard from F4 |
| M2 mask timing (M1 is the same within noise: 49.51 against 49.76) | +1.36 (+0.43 to +2.45) | with C96: +15 real net (24 new), +3 upside-down | **TEST MORE**: adopt the M2 form with the leftover-eclipse check of section 4 |
| Short-binary light subtraction (Codex 024) | +0.4, inside noise | 180 / 78 | **REJECT for 1.1** (failed its own rule); its 10 extra detections die at the same tier-2 holds, so revisit only after F4 |
| Stray-light loader change (Codex 025) | not benched yet (Claude is finishing it) | | see F2 |

Choice between M1 and M2: by mechanism, not rank. M2 keeps a window where the sector's own light says the eclipse is; M1 trusts a catalogue time that is known to be wrong on these stars. M2.

## 3. The trap in "more planets, no more upside-down alarms" (LIKELY)
The freed upside-down budget is real (79 to 53). But DS and M2 mostly add events the upside-down arm cannot show. On the untouched background the two arms run at about 2.3 real per upside-down event (124 / 53). Against that:
- DS adds 19 real for 3 upside-down. Expected real at the usual ratio: about 7. So about 12 of the 19 are dips with no mirror: most likely pointing dips before thruster firings (RS-031, RS-038).
- M2 adds 24 new real for 3 upside-down (`new-real-events.csv` of 023, read row by row): at least 14 of the 24 sit on 6 stars and are plainly eclipses the catalogue cannot place: two of 7% to 9% depth at signal 209 and 264 on a star with no radius (cap off), one of 2% at signal 122, one of 0.9% at signal 100, three of 0.5% to 0.7% on one 34-day binary, four of 0.10% to 0.14% with the same length on one star. A binary-phase test does not catch them (I tried: only 2 of 24 repeat at the same catalogue phase) because the catalogue PERIOD is wrong on these stars, which is the reason their windows were so wide in the first place.
- Why it matters: G1 reads real against upside-down. Dips with no mirror are exactly what a false planet lead is made of. Tree rule 1 as written (upside-down only) would pass both levers; I recommend the freeze test also bound NEW REAL events (rule 4 in section 5).

## 4. FIX 94 design that can survive its controls
**Finding (CONFIRMED by reading the code): FIX 94 and FIX 101 are the same line.** `pipeline/petrova_mask.py` `windows()` adds `3 x sqrt(eT0^2 + (n x eP)^2)` to every window. FIX 94 called it "timing padding" (Codex 010, 14 Nov: 112 G2 stars, 711 blanked light curves); RS-038 found it again from the other side as "mask drift" (FIX 101). M1 is "term set to zero"; M2 is "centre on the sector's refit, term capped at the eclipse width". Brief 026's V1 and V3 are near copies of M2 and M1. **Change brief 026 before launch** (section 6).

Design M4 ("place it, then check it"), per star-sector, no long-baseline timing fit (that failed its controls twice, Codex 012 and 014):
1. Compute the padding term at the sector's time. If it is at most one catalogue eclipse width: frozen behaviour, bit for bit (class A).
2. Otherwise (class B, the catalogue cannot place the eclipse): never blank. Use M2: window centred on the sector's own refit offset, half-width = usual width plus the term capped at one eclipse width.
3. **Leftover-eclipse check, same on both arms:** after masking, the star is marked `timing_unverified` when (i) any leftover dip is deeper than the host's planet cap (C96, with the fallback radius), or (ii) three or more leftover events on the star, over all its sectors, have depths within 30% of each other and times that fit one strict period. Events on a marked star are held at tier 2 with that flag, never deleted. Two similar dips alone do NOT mark a star: a real planet makes those (the twin-transit lesson of RS-025).
4. The repeat lane keeps running as today.

Controls, written before any run: (a) class A identity: zero changed events on 50 class A star-sectors; (b) planted wrong-time eclipses: put 2% and 5% eclipses at a shifted time on quiet class B stars; M2 alone must fail this (failing-first), M4 must hold them; (c) planted planets with two and three crossings of equal depth on class B stars: M4 must not hold more than M2 does, beyond 0.5 point of P; (d) new real events on class B stars not above new upside-down events x 2.3 plus 5.
What would reject M4: control (d) fails, or the planet gain against B falls under +0.5 point. Then the answer for 1.1 is "class B stars stay blanked", which costs about 1.4 points and is safe.

## 5. The one combined test before a freeze (pass rule; all must hold)
Candidate K = B + C96 (with margin and fallback radius as benched) + DS with its pointing guard (F4) + M4. K is written into a bench copy and hashed BEFORE the test.
1. **Fresh planet bench:** new seed, new planets, same drawing rules as Codex 006, both arms, raw-light injection before every step. If Ahmed has signed the physical bar file, depths are drawn under it; if not, both readings are reported.
2. Paired change K minus B on the fresh bench: 95% whole-star interval above zero AND point estimate at least +2.0 points.
3. Untouched background: upside-down at most 79, real at most 174.
4. New real events against B: (new real) minus 2.3 x (new upside-down) at most 5.
5. Dip-against-bump control passes in every binary-period bin.
6. Zero-planet identity: untouched class A star-sectors give the same events as B with C96.
7. T156 on possible planets: R not below B.
8. Known planets (T109): TOI-1338 b tier-1 transits not fewer than under B.

This test decides "1.1 is better than B and may be frozen". It does not decide G1 GO: that still needs P at least 0.75 with lower bound 0.65 on the fresh bench, and K will not reach it. Status: NOT RUN. The fresh bench needs the Codex 006 drawing code and about 3 to 5 hours of machine time for three mask modes; it is Claude's or Codex's first job after F4's guard exists.

## 6. For Claude: brief 026 (FIX 101) should change before launch
- Drop V1 and V3 as new variants: they repeat M2 and M1, already benched three times (Codex 010, 011, 023). Reuse those replays.
- Use the job for what is missing: (a) the star list: 010 chose stars with padding over 0.5 d or a blanked file (112 in G2, none in G3); RS-038 counts windows over a quarter of the orbit, which may add stars and G3: measure the difference; (b) build the leftover-eclipse check of section 4 and run controls (a) to (d); (c) the fallback radius for C96.
- Keep its residue control but replace "within 0.3 d of a catalogue eclipse time": on these stars the catalogue time and period are wrong, so that control cannot fail. Use control (d) above.

## 7. How far from 0.75, said plainly
- Today B: 0.48. Best candidate after its guards: about 0.50 to 0.52 (LIKELY). Gap to the bar: about 23 points.
- 0.75 is out of reach with the levers in F1. What could change that is in the two pools nobody has opened: planets detected but held below tier 1 (11.6 points, task F4) and crossings never scored (13.8 points, of which perhaps 9 are real losses, task F2). With every known pool closed RS-037 puts the ceiling at 0.71 to 0.74 (LIKELY), so 0.75 needs nearly everything to work; an honest forecast for a Petrova 1.2 is 0.60 to 0.65 (UNCERTAIN).
- Model note for the record: Codex jobs 023 to 025 ran on GPT-6.1-Sol at high effort, not GPT-6-Astra.

## Labels
CONFIRMED: section 1 and the code identity in section 4. LIKELY: section 3 (classification by reading 24 rows and a ratio argument; no pixel or pointing test run). NOT TESTED: M4, the cap margin, the fallback radius, the fresh bench.
