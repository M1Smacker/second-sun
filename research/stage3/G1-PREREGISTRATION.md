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
