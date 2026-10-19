# Friction log (wave 1b)

One line each: what failed, what I did instead.

- 2026-10-19: arXiv helper script crashed printing non-ASCII author names (Windows console cp1252). `PYTHONIOENCODING` is ignored under `py -I`, so I set `sys.stdout.reconfigure(encoding="utf-8")` inside the script. No data lost.
- 2026-10-19: arXiv HTML pages of Davies+2026 and Oddo+2026 are ~180-190k characters; WebFetch reads 100k per call, so each needed two calls (offset 100000).
- 2026-10-19: arXiv author queries (`au:Orosz_J`, `au:Kostov_V`) returned unrelated or near-empty results; author search on arXiv is unreliable. Used topic queries, Semantic Scholar citations and paper reference lists instead.
- 2026-10-19: Semantic Scholar citation lists are incomplete (2 citers for Kostov+2020, 0 for Davies+2026); one HTTP 429 (rate limit), handled by waiting and retrying. Treated the citation trail as partial and leaned on the full reference lists of Davies+2026 and Oddo+2026.
- 2026-10-19: Semantic Scholar keyword search for "Kruse circumbinary" returned nothing (empty or silent failure; not retried).
- 2026-10-19: a bash heredoc writing claims.md failed (unmatched quote); rewrote the file with the Write tool. No content lost.
- 2026-10-19: GitHub search found no STANLEY repo under "STANLEY"/"circumbinary"; it only turned up via `gh search code "STANLEY circumbinary"` (TKleanthousT/stanley_cbp). Lesson: search code, not just repo names.
- 2026-10-19: a `gh search repos QATS` output crashed my one-line JSON printer (a surrogate character in an unrelated repo description). Results were still readable; no QATS astronomy repo on GitHub besides Agol's UW web folder.
- 2026-10-19: saved two fetched files (GI index HTML 1.75 MB; STANLEY ANTIC CSV 47 KB) to the scratchpad on C: first, then moved them to D:\second-sun\data\wave-1\ and logged both in downloads.csv. Nothing else was downloaded.
- 2026-10-19: ADS not used (JavaScript-heavy, per instructions). This is the main blind spot for unpublished/conference-only work.
- 2026-10-19: not read in full, due to the 100k-character fetch window: the last ~60k characters of STANLEY I (injection results) and the later sections of the TOI-1338 and TIC 172900988 papers.
