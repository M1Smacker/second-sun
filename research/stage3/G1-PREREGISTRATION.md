# G1 preregistration (DRAFT, started 14 Nov 2026)

**Status: DRAFT, not frozen.** G1 does not run until the planet bar says GO (`G1-PLANET-BAR.md`; today FIX FIRST, P 0.48). The whole file is frozen, with a hash, before G1 reads any data, and is never changed after that.

## Parts Ahmed has approved (go in unchanged at the freeze)
| Part | What it fixes in advance | Where | Approved |
|---|---|---|---|
| T125 | The follow-up protocol: what happens after a lead exists (two keys first, follow-up windows written per orbit family, fake-window threshold on both arms, four outcomes with fixed sentences, first valid run counts) | `LEADS-RULES.md` Amendment 2 | Ahmed in chat, 14 Nov 2026 |
| T127 | The novelty check: every lead is checked against local tables, NASA Exoplanet Archive, ExoFOP, SIMBAD and arXiv before follow-up; a failed source means INCOMPLETE, never new | `pipeline/novelty_check.py`, `test_novelty_check.py` | Ahmed in chat, 14 Nov 2026 |

## Parts still to write (named elsewhere, not yet approved)
- The measured P and every per-bin P, and any blind spot under 0.20 (`G1-PLANET-BAR.md`).
- The star-level power line and design effect beside the event-level one (T129).
- The Petrova version and frozen hash G1 runs on (after FIX FIRST).

## Proposed full contents (Claude, 14 Nov 2026, 19:23 Kuwait; NOT approved; input for Fable's task 3 on Monday and for Ahmed)
Model: G3's preregistration (sections 1 to 7 plus a lock record), with what G1 adds. Each part names where its content comes from.
1. **Purpose, one question:** does the unseen G1 list hold a circumbinary transit our frozen filter can see, or is it a clean measured null (both are wins, 29 Oct 2026).
2. **The star list, fixed by hashes:** the 552 unseen rows, fence A and fence B excluded by rule; what has already been read before the search (headers, manifests), said now.
3. **Version and one-shot rule:** Petrova 1.1 frozen hash (after the fix rounds), the guard script that refuses any other hash or star list, the settings file; G1 runs once.
4. **The bar it passed:** P on frozen 1.1, per-bin P with intervals, any bin under 0.20 named as a blind spot (`G1-PLANET-BAR.md`); R from T156 for reference (`G1-RECOVERY-BAR.md`); the two real known planets (T109) rerun on 1.1.
5. **What counts as an excess:** carry G3 section 5 (real tier 1 against the upside-down estimate, Poisson 0.01 at SNR 7, the other bars agreeing) unless a change is written here first; plus the star-level power line and design effect (T129).
6. **Leads:** `LEADS-RULES.md` stages and checks; Amendment 2 follow-up protocol (T125, approved); the novelty check (T127, approved); Ahmed's 14 Nov rule that leads are shown at once marked "not checked yet" (LEADS-RULES needs this written in as an amendment before the freeze); whether G1 is blind (cards and kinds hidden until the preregistered analysis) must be decided here: Claude's default is blind, as every sealed run so far.
7. **Reporting rules:** the plain verdict line first, then counts; labels; split by TOI, known circumbinary host, none; the Search window prepared by `SEARCH-WINDOW-BLUEPRINT.md`.
8. **Known limits, said now:** binaries with poor catalogue timing (FIX 94 until our own ephemerides are in; how many G1 stars it touches, counted before the run); events deeper than any planet (FIX 96); known spacecraft events (FIX 95); planets deeper than 6,000 ppm are untested on the bench; a planet's twin transits under OAE (RS-025 Q5); faint stars and QLP-only light; products and eras.
9. **What each outcome makes us do:** found (two keys, follow-up protocol), leads under check (named checks, private until both keys only if G1 is blind), clean null (the completeness sentence with its numbers).
10. **Lock record:** file hash, Ahmed's words and date; amendments only before any G1 light is searched, each dated and committed.


## Draft v2: text for the parts that can be written now (Claude Opus 5.5 medium, 14 Nov 2026, 10:35 pm Kuwait; NOT approved)
Built on tonight's facts. Parts that wait on a measurement say TBD and name it.

**1. Purpose.** One question: does the unseen G1 list hold a circumbinary transit that frozen Petrova 1.1 can see? A found planet and a clean measured null are both wins (29 Oct 2026). G1 runs once.

**2. Stars.** The 552 unseen G1 rows of `targets/r1_targets.csv` (list g1), identified by the file hash at the freeze. Fence A (G1 itself until the run) and fence B (sealed G2 and G3 rows) are never read before the run. Already read before the search, said now: target-table columns and archive manifests (file names and sectors) only. TBD at the freeze: the hash of the star list and the count of G1 stars whose catalogue timing term exceeds 0.5 d at any searched sector (the FIX 94 limit), computed from catalogue columns only, never from light.

**3. Version.** Petrova 1.1, frozen with its own settings hash after the fix rounds. Adopted so far (not frozen): repeater rule b, symmetric FIX 91, OAE, known spacecraft events flag (FIX 95). Candidates still open: the FIX 94 mask timing (needs validated eclipse times, Codex 014 part 2 and Fable), DS or DSp (dump rule), FIX 96. A guard script refuses any other hash or star list; `pipeline/run_record.py` writes the run record before the first group and verifies it in the readout (T142).

**4. The bar it passed.** P on frozen 1.1 (planet bench, equal weight over the five binary-period bins) at least 0.50 with its star-cluster interval, every per-bin P with its interval, any bin under 0.20 named a blind spot; T156 reference R for comparison; the two known planets rerun on 1.1 (TOI-1338 b, TIC 172900988 b). TBD: all numbers, after the freeze.

**5. What counts as an excess (proposed: carry Re-search 1 Amendment 3).** Recovered-light tier-1 real events against the upside-down count, stratified by binary-period bin, against a fixed reference measured on the design stars under Petrova 1.1 (written to a hashed file before the run): exact stratified chance at most 0.005 at SNR 7, and the sealed real count above the count expected from the reference share at SNR 8, 10 and 12. Printed with it: the sensitivity line from `pipeline/s1_sensitivity.py` (FIX 86, worded as a conditional sensitivity, never an exclusion); the false-alarm rate with both the Poisson and the star-clustered interval (FIX 88); the design effect of events clustering on stars (T129: deff 1.5 to 2.1 in Re-search 1); gate verdicts with explicit bin coverage (FIX 87, "PASS ON TESTED BINS" when a bin is untested).

**6. Leads.** `LEADS-RULES.md` stages; T125 follow-up protocol and T127 novelty check (both approved). Ahmed's rule of 14 Nov (leads shown at once, marked "not checked yet") applies AFTER the preregistered analysis if G1 is blind; while the run is sealed nothing is labelled. Needs an amendment to LEADS-RULES before the freeze.

**7. Reporting.** The plain verdict line first (found, nothing found, or N leads under check), then counts; labels CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED; split by TOI, known circumbinary host, none; Search window prepared by `SEARCH-WINDOW-BLUEPRINT.md` before the go.

**8. Known limits, said now.** (a) Binaries with poor catalogue timing (FIX 94) until validated eclipse times exist; (b) momentum-dump artefacts make one-sided dips that the upside-down control cannot see (RS-031, Codex 013), so any dump rule in 1.1 is judged with that limit stated; (c) events deeper than any planet (FIX 96) and planets deeper than 6,000 ppm are untested on the bench until Codex 014 part 3; (d) a planet's stronger transit can hide its weaker one under OAE (RS-025 Q5); (e) faint stars and QLP-only light; (f) the after-dump side of rule C7 (0.25 d) may be shorter than the 0.5 d ramps in the literature (RS-031, NOT TESTED).

**9. What each outcome makes us do.** Found: two keys, then the T125 protocol, then Ahmed's yes before any outward step. Leads under check: the named checks, in the stage order of LEADS-RULES. Clean null: the completeness sentence with the measured P and per-bin P, and the sensitivity line, never "no planets exist".

**10. Lock.** File hash, Ahmed's words and date; amendments only before any G1 light is searched, each dated and committed.

### Decisions for Ahmed before the freeze (open)
1. Is G1 blind (default yes, as every sealed run so far)?
2. Carry Re-search 1's stratified excess rule (part 5), or something else?
3. The reference counts: design stars under Petrova 1.1, hashed before the run (default yes).
4. Which known-limit items must be fixed before G1 rather than stated (default: only FIX 94 if Fable's design is validated in time).
