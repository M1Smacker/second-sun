# Burn 3 open questions

1. **DECISION NEEDED (Ahmed): the submission path.** ExoFOP now wants publication first (B9-B10). Options:
   - (a) Write our method up in a peer-reviewed venue first, then one RNAAS note per candidate citing it, then ExoFOP.
   - (b) An RNAAS note citing *already-published* methods we reuse. Does citing the published search/vetting tools we use count as "the methodology … previously published"? Ambiguous; only ExoFOP support can say.
   - (c) Hand strong candidates to a professional team (TFOP / Planet Hunters TESS style) and co-author.

   Founding decision C11 ("two keys, then submit") needs rewording either way.
2. Does the TOI team still accept candidates by any route other than ExoFOP (e.g. directly to the TESS Science Office)? Not found.
3. The fields of the Published Candidate Upload Request form (login needed, so this waits for Ahmed's ExoFOP account).
4. A&A: confirm the AI statement text, the current page-charge amounts, the sponsoring-country list (Kuwait? Pakistan?) and how an unaffiliated author's "country" is decided. aanda.org blocks our tools; Ahmed could open it in a browser.
5. MNRAS: is there any way around the £2,356 APC for a Kuwait-based independent author (discretionary waiver)? Probably not worth chasing; RNAAS is free.
6. iPhone offline test after the first deploy (B4): Add to Home Screen, open once online, switch on airplane mode, reopen; also check that a new deploy replaces the cache.
7. Repo name: `site_url` assumes `second-sun`.
8. ~~Quiz scoring~~ settled by the blueprint: self-marked, no stored scores.
9. Sky-coverage map and finds gallery: blueprint §5 (static SVG from coverage.csv); not built here.
10. Wave 9 leftover not in this brief: Windows Task Scheduler + a resumable batch-runner design.
11. Blueprint follow-ups (see report.md "Blueprint conflicts"): candidate status names after the ExoFOP rule change; when the scoop switch flips (write-up submission, not "CTOI time"); `cancel-in-progress` true vs false; "Level n of 6" vs "of 7".
12. Search index growth: 4.1 MB at 300 long dummy pages; the 25 MB precache budget may bind around 500+ long pages. Decide later whether to exclude log pages from search or raise the budget.
13. Does Material's instant navigation run `<script>` tags inside page content? Needed before demos load per page (blueprint §8). Untested.
14. iPhone: run the blueprint §6 checklist after the first deploy (the only offline evidence so far is headless Chrome on Windows).
