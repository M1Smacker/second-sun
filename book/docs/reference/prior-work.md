# Prior work and how we differ

<p class="ss-meta">Reference · about 4 min · written 27 Oct 2026</p>

!!! plain "In plain words"
    Other teams have already searched TESS for planets that orbit two stars, with published methods and peer review. This page lists the ones we know, says how deeply we have read each, and says honestly where this project is different and where it is not.

## The published searches we know

| Work | What it did | How we read it |
|---|---|---|
| Davies et al. 2026, *MNRAS* 548 ([arXiv:2604.09435](https://arxiv.org/abs/2604.09435)), a Warwick team | A semi-automated search for single transits (the tool is called mono-cbp). It searched 512 detached eclipsing binaries with orbits over 7 days and reported one weak candidate. An event was kept only if it survived at least 18 of 21 different detrendings (F-021). | abstract; Table 2 (F-001) |
| Thornton et al. 2026, *MNRAS* 548 ([arXiv:2512.07934](https://arxiv.org/abs/2512.07934)) | 27 candidate two-star planets from the slow turning of the binary's orbit (apsidal precession), found by timing eclipses, not by looking for transits. | title only |
| Oddo et al. 2026 ([arXiv:2610.22625](https://arxiv.org/abs/2610.22625)) | The occurrence of two-star planets around red-dwarf eclipsing binaries in TESS. An earlier conference abstract, "Towards Transiting Tatooines" (2024), described the search. | title only |
| Martin and Fabrycky 2021, *AJ* 162, 84 | STANLEY: stack shallow crossings that do not keep time, using simulated orbits. | abstract; we ran it (F-044, F-045) |

"Title only" means we confirmed the paper exists and what it is called, and nothing more. We will not describe results we have not read.

## How this project is different, as far as we know

- **Different list.** Our list is 549 Kepler eclipsing binaries, looked at again in TESS data. Davies et al. used TESS-selected binaries, Thornton et al. used Gaia binaries, and Oddo et al. used red-dwarf binaries. How many of our stars are also in Davies et al.'s 512 we have not measured yet.
- **Different method from Thornton et al.** They time the eclipses; we look for the planet's own dips. The two approaches are complementary, and a star that shows up in both would be interesting.
- **Same kind of method as Davies et al., built separately.** Both look for dips in detrended light curves. We have not used their code in any result, and we have not compared the two detectors on the same stars.
- **What is new is small.** An open, labelled record of every step, mistakes included; two keys on every candidate, one of them human; and a book that teaches the method. No new science yet.

## What we depend on

The published searches above, STANLEY's published code (MIT licence), and NASA's public TESS and Kepler data. If you notice something we have misread or left out, please [open an issue](https://github.com/M1Smacker/second-sun/issues).
