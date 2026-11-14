# Drops: one small file per finished piece of work (Ahmed's idea, 14 Nov 2026)

Write a drop the moment a piece of work ends (Claude or Codex). Python never writes the words: after G1 the builder (T160, `research/tree/TREE-BRAIN-PLAN-2026-11-14.md` section 9) reads these files and fans each one out to the Tree, the book field note, the recap, versions, RESUME and the ledger, then publishes.

File name: `YYYY-MM-DD-HHMM-short-slug.md`. Shape:

```
---
type: finding | change | decision | lesson | research | fix | build | question | run | version | rule
node: 1.4            # Tree node
date: 2026-11-14 16:20
label: CONFIRMED | LIKELY | UNCERTAIN | NOT TESTED   # findings only
status: open | done | superseded
by: Claude | Codex | Ahmed
links: [path, path]  # files, reports, commits
ids: [FIX 94, Codex 010]   # every id named, explained in the plain line
supersedes: []       # drop file names this one replaces
---
**Plain:** one line anyone can read.
**Why it matters:** one line.
**Explanation:** a few plain sentences.
**Technical:** numbers, method, caveats.
```
Star ids and star data are allowed (Ahmed, 14 Nov 2026). Leads may be shown at once, marked 'not checked yet'. Not allowed: unblinding a sealed run, fence A or B stars, private memory text.
