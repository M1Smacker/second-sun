---
name: second-sun-research
description: Use in Second Sun for any research question (astronomy, statistics, datasets, catalogues, methods, papers, tools, model or product facts) and before trusting any scientific claim. Wraps the project's research blueprint and source rules.
---

# Second Sun research (for Codex; written 12 Nov 2026)

Follow `research/RESEARCH-BLUEPRINT.md` in full. The short version:

1. **Tie the question to a decision.** Write in one line which decision the answer changes. No decision, no research.
2. **Write the cap first** (how many tool calls or how much of your usage bar) at the top of your report, then stop at it.
3. **Our own data and code first.** A count or a 40-line script on our files beats a paper. Then primary sources. Then nothing (label UNCERTAIN) rather than a guess.
4. **Primary sources only for claims:** NASA Exoplanet Archive, MAST and TESS docs, ADS, arXiv ABSTRACT or HTML pages (never open a PDF or file link in the browser; download papers with Python into `data\astra\downloads\<name>\` if you need the full text), official mission and catalogue pages, peer-reviewed papers. A search-engine summary or another AI's answer is a lead, not a source: on 23 Oct 2026 another AI's research answer had 6 wrong and 1 invented citation out of 12.
5. **Pull the exact sentence** (short quote) and the link for every claim that a conclusion rests on. Check ids and dates: release dates go stale (Gaia DR4: 2 December 2026, from ESA's page, read 10 Nov 2026).
6. **Label** CONFIRMED (primary source or our own script), LIKELY (secondary but consistent), UNCERTAIN (conflict or thin), NOT TESTED. Explain any conflict and which side you pick.
7. **Turn every finding into a plan change** (QUEUE PROPOSALS or a sentence on which decision moves) in your report.
8. Number research stints AS-001, AS-002, ... in your report title and in `research/astra/USAGE.md` (Claude's stints are RS-NNN in `research/research-sessions.md`; do not edit that file).

Facts that are easy to get wrong here: BTJD = BJD minus 2457000; Villanova `bjd0` is BJD minus 2400000; Kepler BKJD = BJD minus 2454833; QLP quality flags change at sectors 56 and 94; 109.08 Earth radii per solar radius; `dur_h / 24` for days.
