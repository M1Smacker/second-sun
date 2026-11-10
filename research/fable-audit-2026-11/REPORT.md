# Fable audit of Second Sun, run 1. REPORT (10 Nov 2026)

Auditor: Claude Fable 5.2, medium effort, under `01-FABLE-BRIEF.md` as changed by `02-AMENDMENT-1-SCALE-DOWN.md`. Repo read at commit c9b9aca. Nothing in the project was changed. Counts only; no star names. Details and evidence: `findings-P.md`, `findings-N.md`, `findings-S.md`, `findings-R.md`, `scripts/`, `evidence/`, `work-orders/`. Lessons: private skill `second-sun-auditor`.

## URGENT

**U-1 (F-01). The filter deletes planet dips in slow binaries before it searches. CONFIRMED.**
`detect_v2.eclipse_mask_auto` treats any low phase bin in one sector as an eclipse. In a slow binary each phase is seen once, so a planet's dip is masked. On real G2 light, an 8 h dip at 25 times the noise was found 0 times in 25 for binaries slower than 20 d, 3 in 25 at 14 to 20 d, 7 in 25 at 10 to 14 d; all of them are found when injected after the mask, which is how every one of our recovery tests injected. Consequences: the G1 to G3 nulls say little about deep transits in binaries slower than about 14 d (38% of G2 sealed star-sectors, 16% of G3); completeness, Horizon E and the Census odds are too optimistic about our reach; S1 was biased toward "no excess"; the arms are not exchangeable, which is LIKELY a main cause of the S2 excess in G2. 8 of the 12 known transiting circumbinary hosts are slower than 18 d. The sealed verdicts stand as filed. This is not a planet signal and no lead was seen.

**U-2 (F-17). Star IDs of the sealed G2 run are public in the history of the `watch-data` branch. CONFIRMED.** The current feed is clean. Old commits (titled "counts only") carry star id and sector per event. No lead exists there, but the privacy rule is broken. Fixing it rewrites a public branch: Ahmed's yes.

## Plain verdict
Found something big: the search was partly blind exactly where circumbinary planets are known to live, and fixing that one function is worth more than any new star list. Nothing else found changes a filed verdict.

## Ranked findings (by effect on the chance of finding a planet)

Cost is weekly points: Sonnet 5.5 Extra / Opus 5.5 / Fable. "Fable used" says whether Fable's judgement was needed to find it.

| ID | Area | Finding | Label | Effect on planet chance | Risk if ignored | Cost S / O / F | Tag | Fable used | Work order |
|---|---|---|---|---|---|---|---|---|---|
| F-01 | P | Eclipse mask cuts dips in slow binaries; all recovery tests inject after the mask | CONFIRMED | Fixing it before Census: about +10 to +16 points of "at least one" (same as 600 to 900 more stars); opens the slow binaries | Census repeats the blind spot; nulls overstated | measure 1.5 / design 2 / (design 2) | Sonnet ok (measure), Opus needed (design) | yes | WO-F01 |
| F-11 | S | Slow binaries already on disk were never truly searched: a zero-download new hunt | LIKELY | E not computed; best-supported place to look | The cheapest planet chance is left unused | prereg 1 / 1 / - | Opus needed | yes | WO-F01 part B, then a preregistration |
| F-07 | N | Census odds arithmetic right (36-52%, 21-31% reproduced); inputs need the mask factor | CONFIRMED / UNCERTAIN size | Corrects every forecast; believed rate after 3 nulls rises | Decisions sized on optimistic E | - / 1 / - | Opus needed | yes | WO-F10 |
| F-04 | P | Lost QLP reads (13.9 to 16.1%): three cheaper stand-ins for neighbour windows | LIKELY | Up to +8% reach (T137's own estimate), 20% for Census | Fifth of full-frame light thrown away | 1 / - / - | Sonnet ok | judgement | WO-F04 |
| F-12 | S | FFI door: verdict CLOSED stands; U6 was the wrong gate; re-test under a new plan with an on-demand second key and TESS-derived ephemerides | LIKELY | Decides whether about 7,500 new bright stars are usable | Door stays shut for the wrong reason, or opens on bad periods | 1 / 1 / - | Opus needed | yes | memo below |
| F-13 | S | Gaia DR4 is dated 2 December 2026; G5 and stage D should wait for it | CONFIRMED (date) | Better slow periods for the whole G5 pool | G5 list built twice | 1 / - / - | Sonnet ok | no (a date lookup) | WO-F13 |
| F-14 | S | Census stage 2 plan is right but must not start under 0.8.1; rank stars by coverage as well as brightness | LIKELY | Coverage-first order raises E per download | Census odds cut by a quarter to a half | - / 0.5 / - | Opus needed | yes | findings-S |
| F-02 | P | FIX 84 measured: nothing leaks in Sectors 56 to 93; a new flag (bit 29) rides on 11.9% of kept cadences from Sector 94 | CONFIRMED counts; meaning UNCERTAIN | Protects the G3 null; guards the newest light | Unknown flag in 10% of G3 QLP files | 0.4 / - / - | Sonnet ok | small | WO-F02 |
| F-09 | N | Horizon: dilution 1.0 and blend-inflated radii cancel by luck; not written down; fails where radii are per-component | LIKELY | Up to a factor 2 in depth for some stars | E wrong either way for G2 | - / 0.6 / - | Opus needed | yes | WO-F09 |
| F-08 | N | S2 interval right (7.08 to 10.28); "FAIL" is within noise of the mark (chance 0.24); confirms Q6 | CONFIRMED | Stops a cause hunt in 0.8.1 | Points spent chasing noise | 0 | - | small | none (decision) |
| F-05 | P | Tests do not test the science path (no pre-mask injection, no arm exchangeability, skip prints pass) | LIKELY | Protects every future null | The next F-01 goes unseen | 0.8 / - / - | Sonnet ok | no (routine once F-01 is known) | WO-F05 |
| F-06 | P | Known planets on real light: NOT DONE | NOT TESTED | Proof of the fix | - | 0.6 / - / - | Sonnet ok | no | WO-F06 |
| F-10 | N | 0.21, 0.45, noise fit, g, counts that do not reconcile: NOT re-derived | NOT TESTED | Sizing of G5 | Small | - / 1 / - | Opus needed | no | WO-F10 |
| F-15 | S | M-dwarf hosts: a labelled stratum in G5, not a hunt | UNCERTAIN | Small | Effort on a 46-star pool | 0.5 / - / - | Sonnet ok | judgement | WO-F15 |
| F-16 | S | K2, PLATO, CHEOPS: NOT RESEARCHED | NOT TESTED | Unknown | - | 0.5 / - / - | Sonnet ok | no | WO-F16 |
| F-17 | R | Star IDs public in `watch-data` history | CONFIRMED | None (privacy) | Rule broken; future leads could leak the same way | 0.5 / - / - | Sonnet ok, Ahmed's yes | small | WO-F17p |
| F-18 | R | Nine rule conflicts, stale core rules, costly per-task bookkeeping | LIKELY | More science per point | Points go to upkeep | 0.8 / - / - | Sonnet ok, Ahmed's yes | judgement | WO-F18 |
| F-19 | R | Queues: about 8 stale fixes, 4 done-unticked and 8 dead builds, 5 duplicates | LIKELY | Clearer priorities | Wrong item worked next | (in WO-F18) | Sonnet ok | no | WO-F18 |
| F-20 | R | Reproducibility: hard paths, no CI, zero-diff proofs freeze bugs in, backup on the same disk | LIKELY | Protects results | One disk failure loses the sealed runs | 1 to 2 / - / - | Sonnet ok | judgement | existing FIX 82, 83 |
| F-21 | R | Ledger explains under half of a week's spend; reading is the expensive habit | LIKELY | More science per point | Budget surprises | 0.2 / - / - | Sonnet ok | judgement | findings-R |
| F-03 | P | Flip-match flag is one-sided in code but touches 1 event per run | CONFIRMED | None | None | (in WO-F01 B) | - | small | - |
| F-22 | S | New idea: binary-phase duration key | NOT TESTED | A free vetting key; fewer false leads | - | - / 1.5 / - | Opus needed | yes | WO-F22 |

Not audited (Amendment 1): the book, the learning track, Eyes correctness, FIX 80.

## Research stints (ready to copy into `research/research-sessions.md`)
- **RS-015 (Fable), 10 Nov 2026.** Question: Gaia DR4 release date, and PLATO launch date. One Haiku helper, 3 tool calls, cap 5. Answered 1 of 2. Gaia DR4: "Gaia DR4 (based on 66 months of data) 2 December 2026" (heading on https://www.cosmos.esa.int/web/gaia/release): CONFIRMED date; contents of the eclipsing-binary product NOT VERIFIED. PLATO launch: no date on https://www.cosmos.esa.int/web/plato: NOT VERIFIED. Plan change: G5 list and FFI-door stage D wait for DR4 (F-13).
- RS-013 (K2, PLATO) and RS-014 (M dwarfs): not started; passed to Sonnet as WO-F16 and WO-F15.

## Petrova 1.0 candidates (0.8.1 is never edited)
1. Eclipse mask from the catalogue ephemeris and widths, or a repeat rule over all sectors (low in at least 2 cycles); never mask a single-visit phase by depth alone. (F-01)
2. Mirror every sign-sensitive step on the upside-down arm so the arms are exchangeable; two-sided flip-match. (F-01, F-03)
3. All recovery and completeness tests inject into raw loaded light. (F-01, F-05)
4. FIX 11 and FIX 14 in the same pass (detrending window for long boxes; mask before detrend).
5. Replace neighbour windows by flags, background or same-camera windows, per WO-F04. (F-04)
6. Decide bit 29 for Sector 94+. (F-02)
7. Binary-phase duration key as a flag. (F-22)
8. A new S2 defined on the exchangeable design, with its mark preregistered. (F-08)

## Top 3 outside-the-box ideas
1. Search the light we already threw away: a preregistered re-search of slow binaries on disk with Petrova 1.0. Zero download.
2. Coverage-first star lists: continuous viewing zones and 8+ sector stars before 1 to 3 sector stars.
3. The binary-phase duration key (WO-F22).
Others in one line each: multi-dip count excess per star; eclipse timing as a second key on a lead only; a learned vetter only after the arms are exchangeable; K2's 80-day campaigns.

## FFI door v2 (memo)
Keep the filed verdict (CLOSED on U6). For a v2 preregistration, after DR4: frame = DR4 slow eclipsing binaries to G 14; ephemerides derived from TESS light itself, Gaia used only to nominate stars; gates = light exists in 2 or more sectors, loads, noise within 1.5 times the fit, eclipses found where TESS says, and an on-demand second key (pixel cut-out check plus one independent reduction) computable for at least 80% of sampled events. Drop "both QLP and TESS-SPOC exist" as a gate: they are the same pixels. Positive control: a known circumbinary transit recovered from full-frame light with the Petrova 1.0 mask.

## 2027 roadmap (sketch)
- Now to end of January (Checker Season): WO-F01 part A, WO-F02, WO-F05, WO-F06 by Sonnet; Petrova 1.0 design and freeze; preregister and run the slow-binary re-search; DR4 counts after 2 Dec.
- February to May (boards): machine-only jobs, nothing that needs Ahmed.
- June to mid November (Engineer Summer): Census on a coverage-ranked list with 1.0; vetter from the Annex; FFI door v2; G5 preregistration.
- Late November on (Inventor Year): G5; K2 or PLATO pilot if WO-F16 finds unsearched data.

## Proposed rule changes (report only)
1. New: every recovery or completeness test injects into raw light, before any step.
2. New: the two arms must be exchangeable; test it per period bin on every version.
3. New: an outside re-derivation by script for every number that reaches Ahmed as a decision.
4. New: `counts_only` is the default for anything pushed; payloads are searched for star ids before a push.
5. Change: RESUME is one current block of about 400 words plus an archive; recap and field note once a day.
6. Retire or mark superseded: the stale and conflicting entries listed in `findings-R.md` F-18.
7. Helpers: cheapest model that can do the job, one at a time, never an expensive model for reading.

## Decisions for Ahmed
1. Approve WO-F01 part A now (Sonnet, next week), and Petrova 1.0 design as the top priority ahead of Census?
2. "Fable only" work before the reset: I recommend one item, the Petrova 1.0 mask design (WO-F01 part B) with the slow-binary re-search preregistration draft. Everything else can be done by Sonnet or Opus.
3. S2: option A (restate, no pass or fail), and a new S2 for 1.0.
4. `watch-data` history: rewrite it (yes or no).
5. FFI door: accept CLOSED as filed and plan v2 after DR4?
6. G4 and G5 list rules: value-ranked by coverage (my lean) or simple cuts; G5 waits for DR4?
7. RESUME shortening, the push of local commits, the outside-check rule, queue and rule tidy (WO-F18).

## Usage
Start 7% bar, 0% Fable. First attempt (4 Fable helpers reading history) cost about 10 bar points for two summaries. After the restart at 19%: areas P, N, S, R, L and this report cost about 5 bar points. Ledger: `fable-ledger.md`.
