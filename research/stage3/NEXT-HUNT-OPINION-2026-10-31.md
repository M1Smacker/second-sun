# When to resume the hunt, and which stars next (second key opinion, 31 Oct 2026)

Asked by Ahmed on 31 Oct 2026. This is an opinion for his decision, not a plan that has started. Nothing frozen is touched.

## What is left in the catalogue we used (our own data, counted 31 Oct)
Source: `data/xmatch/ebs.csv` (Prsa et al. 2022, 4,584 eclipsing binaries, 4,578 stars). Our G2 rule (detached, binary period over 5 d, Tmag 13.5 or brighter, not in G1) takes 895 stars and the saved list matches it exactly. G1 has 549. Stars left in the catalogue: 3,630. By rule:

| Pool | Stars | With 2+ sectors | Verdict |
|---|---|---|---|
| Detached, P over 5 d, Tmag 13.5 to 14.5 | 31 | 14 | too faint, too few |
| Detached, P over 5 d, Tmag over 14.5 | 27 | 11 | too faint |
| Semi-detached (morph 0.5 to 0.7), P over 5 d, Tmag 13.5 or brighter | 93 | 50 | worth adding to a list |
| Detached, 3 to 5 d, Tmag 13.5 or brighter | 478 | 261 | low yield (below) |
| Detached, under 3 d, Tmag 13.5 or brighter | 603 | 315 | low yield |
| Contact (morph 0.7 or more) | 980 | 521 | no (light always varying) |

So the catalogue we used is spent for our rule. The catalogue covers sectors 1 to 26 (MAST lists v1.0; a search found no newer release; our saved copy lists sectors up to 39, whether its periods were redone is UNCERTAIN).

## Why the short binaries are low yield (LIKELY, from a search snippet, paper not opened)
Kepler found no transiting circumbinary planet around binaries shorter than about 7 days; the shortest host is Kepler-47 at about 7.4 d. Martin, Mazeh and Fabrycky 2015 ([arXiv:1505.05749](https://arxiv.org/abs/1505.05749)) argue a distant third star shrinks the inner binary and removes planets. Martin and Triaud 2014 ([doc.rero.ch copy](https://doc.rero.ch/record/299170/files/stv1870.pdf)) say a drop in planet numbers below about 5 d would explain the missing detections. A 2020 review ([arXiv:2002.10492](https://arxiv.org/abs/2002.10492)) calls the third-star explanation partial. So 3 to 5 d and shorter stars would mostly make a null sample.

## Opinion
1. Do not resume the search yet. A fresh star list is spent once (the sealed lesson). Running frozen 0.8.0 again would repeat the flare-shaped false alarms (about 18 of 42 measured upside-down tier-1 events show the flare shape) and spend the list on a filter we already know can be priced and improved.
2. Order: (a) Vesper 0.9 study on the 301 development stars that are already on disk: T31, T32, T33, T34, T35 as separate switches priced with T103 and T104, then T37; (b) the scorecard amendments written first: T38, T39, T44, T45, T105; (c) a new star list with the rule and the count written and committed before any download (T37b, plus T111 and T112 below); (d) download (Ahmed's yes), one search, scorecard.
3. Rough cost: (a) and (b) about 8 points of my usage, (c) about 1, (d) about 3. Weekly reset is Tue 3 Nov about 01:00 Kuwait (the meter now reads 80% against the 83% cap), so the study and amendments fit the week of 3 Nov and the search the week of 10 Nov. Earliest sensible start of the new search: mid November, results about one to three days after the download ends.
4. Which stars: first choice is a list from outside our saved catalogue (TESS binaries found after sector 26: the live Villanova portal, or Gaia DR3 eclipsing-binary candidates), detached, binary period over 7 d (where planets are known to exist), Tmag 13 or brighter, ranked by how many sectors the star has (expected detections per planet-bearing star grow with sectors; sealed stars had a median of 6 sectors with data, a TOI-1338 b-like planet at P = 95 d gives about 0.62 tier-1 detections per planet-bearing star over all its sectors). Aim for 600 to 900 stars (G2 was 895 stars and about 28 GB). The count is NOT KNOWN until that catalogue is pulled (a small file, needs Ahmed's yes).
5. Fallback with no new list download: the 93 semi-detached P over 5 d stars (too few to power a test, useful only as an extra). The 301 development stars are not a fresh test. The 478 detached 3 to 5 d stars would make a null-only sample and I would not spend the list on them.
6. Power: more stars help only as the square root; a filter that removes a fifth to two fifths of the false alarms helps by a similar amount. The flare check's price on planted dips is NOT TESTED, so that gain is a hope until T33 and T103 are done.

Labels: pool counts CONFIRMED (own data); short-binary deficit LIKELY; sector-yield figure from the 31 Oct null-power script (exploratory); size of a new list NOT TESTED.
