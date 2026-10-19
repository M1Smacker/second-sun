# Common rules for every research wave

Every research session follows these rules. The wave-specific questions are in your own brief and in `RESEARCH-PLAN.md` section 5.

## Read first
1. `D:\second-sun\RESEARCH-PLAN.md`: sections 0, 2, 3, your wave in section 5, and section 9.
2. Wave 1 results (the gap check), at least the plain-words summaries:
   - `research\wave-1-gap-check\a-census\report.md`
   - `research\wave-1-gap-check\b-searches\report.md`
   - `research\wave-1-gap-check\c-catalogues\report.md`
   - `research\wave-1-gap-check\GAP-REPORT.md` (if it exists by the time you start)

   Don't redo what wave 1 already established; cite it and build on it.

## Evidence
- Today is 2026-10-19 or later, and your training data may be older. Explicitly search for 2024-2026 information. Your memory is a lead, never a source.
- Every claim needs a source whose ID (arXiv ID / DOI / official URL) you actually fetched, with title and authors matched.
- Labels:
  - **VERIFIED**: primary source read, or a test or query you ran yourself
  - **LIKELY**: abstract or secondary source
  - **UNVERIFIED**: memory or one weak source.
- Read the few core sources in full; the rest by abstract or summary.
- Say "candidate" vs "planet" precisely. No hype.

## Tools
- WebSearch (standard mode; extended mode only for niche or very recent topics) and WebFetch.
- arXiv API: `http://export.arxiv.org/api/query?search_query=...`
- Semantic Scholar API: `https://api.semanticscholar.org/graph/v1/paper/search?query=...` (if you get HTTP 429, slow down).
- MAST, NASA Exoplanet Archive, VizieR and ExoFOP HTTP endpoints. GitHub read-only via `gh`.
- The ADS web UI is JavaScript-heavy; don't rely on it.

## Machine rules
- Python: use `py -3.12`, **never** the default 3.14. Install packages only if your brief says hands-on installs are allowed, and then only into `D:\second-sun\.venv` (create it with `py -3.12 -m venv D:\second-sun\.venv` if it doesn't exist).
- **Never write to C:** (it's 97% full). Point caches at D: by setting these environment variables for any Python you run:
  - `PIP_CACHE_DIR=D:\second-sun\.cache\pip`
  - `ASTROPY_CACHE_DIR=D:\second-sun\.cache\astropy`
  - `ASTROPY_CONFIG_DIR=D:\second-sun\.cache\astropy-config`
  - `XDG_CACHE_HOME=D:\second-sun\.cache`
  - `MPLCONFIGDIR=D:\second-sun\.cache\mpl`

  If a tool still writes to C:, log it in friction.md.
- Downloads: under 100 MB each unless your brief says otherwise. Save to `D:\second-sun\data\<your-wave>\` and append a row to `D:\second-sun\research\downloads.csv` (columns: `utc_time,what,source_url,size_bytes,dest_path,why,wave`). Measure sizes; never estimate them.

## Output
Write ONLY inside your wave folder, `D:\second-sun\research\<your-wave>\` (scripts go there too):
- `report.md`: plain-words summary first (for a total beginner; no jargon walls, explain every term), then technical detail and tables.
- `claims.md`: claim | source ID + link | label | date checked
- `sources.md`: ID | title | authors | year | link | read depth
- `open-questions.md`
- `friction.md`: every failed command, blocked site or workaround, one line each.

Checkpoint to these files at least every ~20 minutes of work, so a usage limit never loses findings.

## Don'ts
- Do NOT edit files outside your wave folder (except appending to downloads.csv).
- Do NOT git commit or push, create accounts, contact anyone, or submit anything anywhere.

## Usage
- This is a shared Claude Pro plan with parallel sessions. Be efficient: use targeted fetches and never re-fetch the same page.
- If your brief gives a hard stop time, checkpoint and finish before it, even if work remains; list what remains in open-questions.md.

## Finish
End with a final message of 12 lines or fewer:
- the 3-5 most important findings, each with its label
- the biggest open question
- the files you wrote
- 1-2 recommended key reads for a beginner, with why.
