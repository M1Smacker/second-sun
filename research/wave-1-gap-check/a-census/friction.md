# Friction log, wave 1a (census, precedents, physics, NASA path)

One line per failed command, blocked site, wrong assumption or workaround. Times are UTC, 2026-10-19.

- arXiv API over plain `http://export.arxiv.org` returned an empty body (0 bytes); worked over `https://` with redirects followed (`curl -L`).
- Python `-I` (isolated mode) ignores `PYTHONIOENCODING`, so printing non-ASCII titles crashed on the Windows cp1252 console; fixed with `sys.stdout.reconfigure(encoding="utf-8")` inside the script.
- **3 of 28 arXiv IDs I recalled from memory were wrong** (1711.04059, 2001.06049 and 1505.04240 resolve to unrelated maths/statistics papers, not the Welsh & Orosz review, Socia et al. 2020 Kepler-1661 or Welsh et al. 2015 Kepler-453). Caught by the title/author match rule; correct IDs looked up by search instead. This is exactly the failure the "verify every ID" rule exists for.
- WebFetch on an arXiv **PDF** (2004.07783) returned unreadable compressed binary; workaround: ar5iv HTML (`ar5iv.labs.arxiv.org/html/<id>`) for pre-2024 papers, `arxiv.org/html/<id>` for recent ones. Side effect: the tool auto-saved the 9.1 MB PDF under `C:\Users\hanzl\.claude\projects\...\tool-results\` (on the nearly full C: drive); left in place, harness-owned.
- `arxiv.org/html/2408.15307` (Deeg & Doyle 2024 review) returned 404 and ar5iv redirected to the abstract: no HTML version exists, so that review stays at abstract depth.
- Semantic Scholar API returned HTTP 429 (rate limit) on the first call; did not retry (only needed for one minor lookup, KIC 3853259, left as an open question).
- WebFetch summaries are a small model's reading of the page. One summary of Martin 2018 dropped the μ from the HW99 term "−4.27eμ"; caught by reading HW99 itself. Numbers quoted from WebFetch summaries were cross-checked against a second source where they mattered (HW99, transit counts, binary periods).
- NEA TAP `like '%Kepler-64%'` matched Kepler-640 to 649 (SQL wildcard), harmless; PH1 b is listed under its own name, not Kepler-64 b.
- `exoplanets.nasa.gov/news/1617/...` (TOI-700 release) now 301-redirects to the generic `science.nasa.gov/exoplanets/`; used the current nasa.gov URL found by search instead. Old NASA links in papers may be dead.
