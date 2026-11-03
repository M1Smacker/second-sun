# Renaming the filter from Vesper to Petrova: what it touches and what it costs (overview, 3 Nov 2026, evening)

Ahmed's wish (3 Nov 2026): Petrova should be the name of the filter. He asked for an overview only. NOTHING has been renamed. The G3 search stays paused.

## What the count says (own files, `git ls-files`, 815 tracked files, 45 not text)
The word appears 359 times in 119 tracked files (spellings: Vesper 219, VESPER 122, vesper 18). Grouped by what a rename may do to it:

| Group | Files | Mentions | What a rename does |
|---|---|---|---|
| Live documents (RESUME, CLAUDE.md, queues, plans, briefing, book pages, versions table, status panel) | 41 | 133 | rename the words; safe |
| Dated or locked records (field notes, handoffs, Compass reviews, preregistrations, literature notes, R0 rule, leads rules, zero-difference proofs) | 36 | 133 | keep as written, add one name note (they are history; the preregistrations are protected by their lock commits, the runner does not hash them) |
| Generated book data (`watch.json`) | 1 | 3 | regenerate |
| The 11 fingerprinted code files | 5 of 11 | 15 | **must not change**: any edit changes the code hash and the frozen version 0.8.0 / 0.8.1 stops being what it says |
| Other pipeline files and scripts (comments, strings, `g3_run.py`, `vopts.py` docs) | 36 | 75 | leave; some strings (`"Vesper 0.8.1"`) are compared by the freeze check |
| Also: environment variable `VESPER_OPTS` | 38 files, 52 uses | | stays; it is part of the frozen code and of recorded run settings |
| Recorded run settings in `data\` (provenance of the finished runs) | not counted | | never rewritten |

Plus 5 file names with the word (`VESPER-BRIEFING.md`, `VESPER-STUDY-PLAN.md`, `VESPER-VERSIONS.md`, `vesper-study-literature-2026-10-29.md`, one Compass review) referenced from 5, 9, 11, 3 and 3 files; 8 memory files and the memory index; the book home status panel. The book has no page whose address contains the word, so no live link breaks.

## Two ways to do it
- **A. Display name (recommended, do it before the G3 go).** Every sentence a person reads says Petrova. The code, the frozen version identity and the recorded runs keep the internal name Vesper, stated once in a naming note ("Petrova, internal code name Vesper; versions 0.8.0 and 0.8.1 keep the code name"). Frozen hashes and proofs are untouched; check with `g3_run.py check` after. Cost about 0.6 weekly points (0.4 to 1.0): scripted replacement and diff review of 41 live files, 5 file renames with their references, 8 memory files, a book publish (about 3 minutes of machine time), the naming note. From the ledger: small scripted edits cost under 0.2 each, the last two book publishes about 0.3.
- **B. Also rename the code (not now).** Touches 5 fingerprinted files, so it is a new version (0.8.2): three new zero-difference proofs of 300 star-sectors each, a new freeze and hash, a preregistration amendment, a re-run of the four tests. Cost about 2 to 3 points and it delays G3 by that much, for no scientific gain. If wanted, fold it into the 0.9 freeze: those proofs happen anyway then, and the extra cost is about 0.2.

## Risks, said plainly
- Old and new names mixed in a result would confuse provenance: hence the one naming note and the rule that dated records keep their words.
- Two names for one thing in the book for a while if only some pages are updated: do it in one commit and one publish.
- A search on 3 Nov for a transit-search pipeline named Petrova found none (LIKELY: one search only, not a trademark check).
- The second new name, Astrion (Asterion), has no system chosen yet; Vigil's name is still an open question (V-F9).

Label: counts CONFIRMED (script over tracked files); costs LIKELY (ledger-based estimate, not measured); name clash LIKELY (one search).
