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
