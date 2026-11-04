# Census idea 4: has anyone already combined circumbinary dips that fit one orbit? (literature check, night of 4 Nov 2026; research stint RS-011; report only)

Idea 4 in the Census plan: circumbinary transits shift in time and depth because the stars move; judge dips together by whether they fit one possible planet orbit across all sectors, instead of each dip alone. Question: is that already done, and what is left that could be ours? Method: five arXiv API queries (circumbinary with search, timing, single transit, linking, TESS) and the abstracts of the six most relevant hits read in full on their arXiv abstract pages. Nothing beyond abstracts was opened.

## Plain verdict
**The concept is NOT original; published methods already link or stack circumbinary dips along a modelled orbit, on Kepler data. What I could not find is that done on sparse TESS single events across many sectors with an upside-down control. That narrower gap may be ours, but I have not proved it.** Label: LIKELY for "concept already published", UNCERTAIN for "the narrow gap is open" (five queries, abstracts only).

## What the abstracts say (CONFIRMED: read on arXiv)
- **Ofir 2008** (arXiv:0805.1116): CB-BLS, a modified box search for circumbinary planets whose transits are neither periodic nor of one depth.
- **Windemuth, Agol and Carter 2019** (arXiv:1909.07443): corrects large timing and duration variations from the binary's reflex motion using Keplerian models of the binary and planet orbits, then allows extra aperiodicity with the Quasi-periodic Automated Transit Search; recovers Kepler-35 and Kepler-64; Kepler data.
- **Kostov, Welsh and Haghighipour 2020** (arXiv:2008.02756): planets that cross the binary several times in one conjunction give an orbital period estimate (within 10 to 20% for low-eccentricity orbits) from data spanning under 5% of the period; they expect hundreds of such candidates in TESS. This is a single-sector version of the linking idea.
- **Martin and Fabrycky 2021, STANLEY** (arXiv:2101.03186): stacks shallow transits of variable duration and interval using N-body integrations; recovers all known Kepler circumbinary planets including the three of Kepler-47; says it will be applied to a broad sample of eclipsing binaries. This is the closest published match to idea 4, with full dynamics.
- **Davies et al. 2026, mono-cbp** (arXiv:2604.09435): semi-automated search of the TESS Eclipsing Binary Catalogue for individual transit events with automated vetting; one candidate; recovery 50% or more for each known planet, over 75% for 9 of 14. Individual events, not orbit linking (from the abstract).
- **Klagyivik et al. 2016** (arXiv:1610.08471): CoRoT, removal of binary eclipses and a search for quasi-periodic transit-like features, upper limits for coplanar planets.
- Already in our files from earlier work: Oddo et al. 2026 (single-transit detection on TESS M-dwarf binaries, occurrence limits), Armstrong 2014, mono-cbp (see `research/audit-2026-10-28-varwise-mono-cbp.md`).

## What could still be ours (original means a new combination finished properly, not "nobody ever")
1. **Linking across sectors for sparse TESS single events**, with a planet orbit model that predicts where the next dips should fall, tested against many sectors per star. STANLEY and Windemuth do the stacking on continuous Kepler light; mono-cbp and Oddo stop at single events. Not found in five queries (UNCERTAIN).
2. **A real control:** the upside-down copy of every light curve goes through the same linking, so the false-alarm rate of the linking step is measured, not assumed. None of the abstracts mentions such a control (abstracts only; NOT TESTED in the full texts).
3. **Preregistered, on a list nobody has searched** (Census). That is the combination.

## Plan change
- Census stage 5 (research the idea) is downgraded from "maybe novel" to "borrow and extend": read STANLEY and Windemuth in full before designing any linking step; claim nothing as new except the narrow combination above, and only after a second, wider search (Google Scholar style queries, citations of STANLEY and Windemuth, ADS) that I have not done.
- Keep the plain use: two or more dips that agree with one stable circumbinary orbit are better evidence than one, so linking is also a way to bring S2 (false alarms) down, because a chance coincidence of two noise dips on one orbit is rarer. Estimated effect NOT tested.
- Sparse sampling is the catch: a planet at 77 days gives about one transit in three 27-day sectors, so most stars have only one or two events; linking helps only for stars with many sectors, which again says choose stars with long coverage (Q2).

## Labels
CONFIRMED: the six abstracts as summarised. LIKELY: that the concept is already in the literature. UNCERTAIN: that the narrow TESS single-event linking gap is open. NOT TESTED: full texts; ADS and citation search; whether Davies et al. link events across sectors.
