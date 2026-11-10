# Area S findings (stars and data supply). Read at commit c9b9aca. Fable judgement on files already written; no new counts were run.

## F-11. The cheapest new stars are the ones already on disk: slow binaries in G1 to G3 were never truly searched for deep dips. LIKELY. Fable used: yes.
From F-01: in star-sectors with binary period over 14 d (G2 sealed 2,609; G3 670; G2 dev and G1 NOT COUNTED) a deep dip was deleted before the search with probability about 0.5 to 1.0. Nobody, human or machine, has seen those dips, so that light is still blind. A Petrova 1.0 with a correct mask can search it as a new preregistered hunt with zero download. 8 of 12 known transiting circumbinary hosts have binaries slower than 18 d, so this is the best-supported place to look.
Rank by planet chance per point (my judgement; E not computed):
1. Petrova 1.0 mask fix, then a preregistered re-search of the slow binaries on disk (no download, machine time only).
2. Long-coverage stars (continuous viewing zones, 8 or more sectors): the window function W = covered days / planet period is the main loss for slow systems, and a star with a year of light is worth several 3-sector stars. This is option 3 of `CENSUS-STAGE2-OPTIONS` (5,193 stars); do it before the 1-sector scan.
3. Census from CALNet, bright first (T139).
4. The full-frame door from Gaia, after DR4 (F-13).
5. Faint stars and M dwarfs (value about 0.21, F-15).
6. K2, PLATO: later (F-16).

## F-12. FFI door: U6 is the wrong gate; the door should be re-tested under a new plan, not re-read. LIKELY. Fable used: yes.
- As preregistered, U6 = 22.7% is under half of the 50% threshold, so the verdict is CLOSED. That verdict stands as filed. Do not re-interpret it.
- Why the gate was wrong: QLP and TESS-SPOC are two reductions of the SAME pixels. Agreement between them tests the software, not the sky. And G3 already ran 4,075 QLP files against 830 TESS-SPOC, so most of G3 was tier 1B anyway. A second product is a weak key and a poor gate.
- Better second key for full-frame stars, on events only (cheap because first-tier events are few): a pixel cut-out check (is the dip on the target pixel, does the centroid move), plus one independent reduction made on demand for that star-sector. Gate idea for v2: "an on-demand second key can be computed for at least 80% of sampled events".
- Can TESS supply the periods? Yes for binaries with at least 2 eclipses in the light we hold (period from eclipse times across sectors). For slower ones no period is needed if the mask is built from the eclipses themselves across ALL sectors with a repeat rule (F-01 fix). Gaia's periods (right for 59%, 34% for TWOGAUSSIANS, n = 90) are too weak to drive a fold-based mask: a wrong period leaves eclipses unmasked on the real arm and cuts random light elsewhere.
- QLP from Sector 94: readable by the frozen loader (24 of 24 sampled files loaded with `sys_rm_flux`), but carries an unexplained flag, bit 29, on 11.9% of kept cadences (F-02). Settle WO-F02 before trusting that era.
- Memo, not a preregistration (amendment): `FFI-DOOR-V2-MEMO` is section "FFI door v2" of the report.

## F-13. Gaia DR4 is dated 2 December 2026. CONFIRMED (ESA release page, heading "Gaia DR4 (based on 66 months of data) 2 December 2026", https://www.cosmos.esa.int/web/gaia/release, read 10 Nov 2026 by a helper). Contents of its eclipsing-binary products: NOT VERIFIED (the page says final contents are decided after validation).
Decision for Ahmed: do not build the G5 list or run FFI-door stage D on DR3. DR4 is three weeks away and doubles the time base (34 to 66 months), which is exactly what slow periods need. Work order WO-F13 (Sonnet, after 2 Dec): read the DR4 documentation, re-run the pool counts and the period check against Prsa.

## F-14. Census stage 2 (T139) plan check. LIKELY. Fable used: yes.
- "CALNet first, periods from TESS, do not size from the 80 Gaia periods" is right.
- Missing from the plan: (a) the finder test (option 2 in the options note) must inject eclipses AND planet dips before any mask; (b) the star value must include coverage, not only brightness; (c) the streaming fetcher with a stall alarm is still unbuilt and every step needs it; (d) Census must not start under 0.8.1: with the mask unfixed its odds drop by roughly a quarter to a half (F-07, case X).
- Draft star-list rules (Ahmed decides):
  - **G4 option A (my lean): value-ranked.** Score = (sectors with light) x (brightness weight from the noise fit) / (binary period), detached only, period 5 d or more, no upper period cut once the mask is fixed; take the top N by score. Puts long-coverage and bright stars first.
  - **G4 option B: simple cuts** as G2 (Tmag 13.5 or brighter, detached, period over 5 d). Easier to explain, wastes effort on 1 to 2 sector stars.
  - **G5 option A (my lean): wait for DR4**, then 5,000 to 10,000 stars to G 14 with TESS-derived ephemerides, M-dwarf hosts as a labelled stratum to G 15.
  - **G5 option B:** start now from DR3's 7,505 new stars. Not advised (41% wrong periods, list would be rebuilt in a month).

## F-15. M-dwarf hosts: a stratum, not a hunt. UNCERTAIN (no new research run; from our own notes and general knowledge). Fable used: yes (judgement).
- Reach is real: at Tmag 12 a 0.5 solar radius host shows 3 Earth radii at SNR 7 (our Q3 table), against 6 for a Sun-like host.
- The pool is tiny (46 red dwarfs with a good parallax in the Gaia slow pool) and giant planets are rare around single M dwarfs. Nobody knows the small-planet rate around M-dwarf binaries.
- So: include them as a labelled stratum in G5 (near zero cost), expect nothing, and do not build a separate search. Work order WO-F15 (Sonnet research, RS-014): one question, "published occurrence or detections of circumbinary planets around M-dwarf eclipsing binaries", cap 25 tool calls.

## F-16. Other missions: NOT RESEARCHED (budget). Fable used: no.
One research pass for Sonnet (RS-013, WO-F16): has anyone published a systematic transit search for circumbinary planets in K2 eclipsing binaries; PLATO launch date and first public data (the ESA PLATO page read on 10 Nov gives no date; NOT VERIFIED); CHEOPS is pointed follow-up only, useful later as a key on a lead.

## Top 3 outside-the-box ideas
1. **Search the light we already threw away** (F-11). Evidence: F-01 tables. Cost: Petrova 1.0 mask (WO-F01), one preregistration, machine time. Test: inject before the mask at the known planets' parameters; recovery must reach the "after mask" level in every period bin.
2. **Coverage-first lists** (continuous viewing zones and 8+ sector stars). Evidence: Horizon's own W = min(1, covered days / planet period) (`horizon_reach.py` line 86); TOI-1338 sits in the southern zone. Cost: no new code, a different sort order for Census. Test: compute E per star from Horizon for 3, 8 and 13 sector stars and rank.
3. **Binary-phase duration key.** A circumbinary transit's length depends on where the crossed star is in its orbit (star moving with the planet: long; against: short). For any dip with a known binary ephemeris the allowed duration range can be computed, so a dip of the wrong length for its phase is not a planet. This is how the Kepler planets were recognised (Kepler-16, Doyle et al. 2011; LIKELY from memory, source to be opened by WO-F17). A free physics key for vetting and for the future vetter. Cost: about 1 to 2 points to prototype (Opus). Test: the known transits in `data\known` must pass; upside-down events must fail at about the chance rate.
One line each, not pursued: multi-dip count excess per star across sectors; eclipse timing as a second key on a lead only; a learned vetter only after the arms are exchangeable; K2's 80-day campaigns.

## 2027 roadmap (half-page sketch, fitted to the study calendar)
- **Now to end of January (Checker Season).** Sonnet runs WO-F01 measurement and WO-F02. Petrova 1.0 design: catalogue or repeat-rule mask, exchangeable arms, pre-mask injection tests, binary-phase duration key as a flag. Freeze 1.0. Preregister and run the slow-binary re-search on disk (machine time). After 2 Dec: DR4 catalogue pull and counts (WO-F13).
- **February to May (boards).** Nothing that needs Ahmed. Machine-only jobs: the fetcher, the long-coverage download, recovery tables for 1.0.
- **June to mid November (Engineer Summer).** Census (G4) on a value-ranked list with 1.0. Build the vetter from the Annex. FFI door v2 on DR4 with TESS-derived ephemerides. G5 preregistration.
- **Late November on (Inventor Year).** G5. K2 or PLATO pilot if WO-F16 finds an unsearched archive.
