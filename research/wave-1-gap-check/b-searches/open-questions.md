# Open questions (wave 1b)

Ordered by how much the answer would change Second Sun's direction.

1. **What exactly is in the Tufts STANLEY TESS sample, and when will they publish?** GI G09079 says "10,000 eclipsing binaries near the TESS Continuous Viewing Zone, plus 204 well-characterised EBs". Which catalogue? Which magnitude limit? Southern CVZ only, or both? Up to which sector? This is the single biggest overlap risk. *Routes:* ADS search for Kleanthous / Tubthong / Martin AAS abstracts (needs Ahmed's free ADS account); watch arXiv. This is the kind of question where emailing D. Martin could save months, per our contact rule (Claude drafts, Ahmed sends), but only once we have a concrete slice to ask about.
2. **What is Oddo/Dragomir's "TESS 10k sample" search covering?** Talk title only (ESA workshop, Dec 2025). If it covers all 10,001 TESS Ten Thousand EBs, gap #2 shrinks to the ~900,000 unvetted list and to sectors after their cutoff.
3. **Did NASA Goddard's systematic search ("Kruse et al., in prep", 2021) ever produce results?** Not found on arXiv or the web. It may exist as an AAS abstract, or it may have been dropped.
4. **Non-eclipsing binaries: is there really no search?** Absence is based on arXiv abstract queries only. Needs an ADS full-text check before it goes in the gap list as "unclaimed". Practical question for waves 2-3: which non-eclipsing binary catalogue (e.g. Gaia DR3 SB1/astrometric orbits) has orbits good enough to predict CBP transit timing?
5. **Which TESS sectors cover the Kepler field, and has anyone searched them for the ~17-30 "will transit someday" Kepler CBPs (Martin 2017)?** Hand to wave 1c / the merge (sector coverage).
6. **Thornton+2025 and Esmer & Daylan 2025 sector cutoffs.** Read at abstract level only; their last sector is unknown.
7. **mono-cbp and STANLEY on Windows + Python 3.12.** Both declare `batman-package` (C extension); STANLEY needs `rebound`; mono-cbp pins `scipy < 1.13`. Wave 3 must test them. It is not obvious, and it may decide the WSL question.
8. **Licences.** mono-cbp is GPL-3.0 (copying its code into our MIT repo would force GPL); QATS has no licence file. Wave 3 / wave 5.
9. **Is KIC 6504534 (Armstrong+2014 candidate, ~170 d) the same system as Kepler-1661 (P ~175 d)?** Memory only (claim B57). If yes, it is a nice "automated search found it first" precedent for the book. Cheap check: the Kepler-1661 paper's target ID.
10. **Davies+2026 journal details.** Web results show MNRAS 548(4), stag743. Not read on the journal site.
11. **Kepler ETV surveys** (e.g. Borkovits et al. Kepler triples) were not reviewed. They are mostly about stellar third bodies, so they're low priority for a transit quest.
