# Wave 6: training quest, habitable zone, white dwarfs (PARTIAL)

*Second Sun research, wave 6. Run inline by the main session (Claude, Opus 5.5) on 2026-10-19 from ~17:38 UTC. Reading wave. Claims Q1… in `claims.md`.*

---

## In plain words (read this first)

- **Habitable-zone planets (opportunistic):** TESS's famous one, **TOI-700 d**, was found around a small red star that TESS watched for **11 sectors** because it sits in the long-stare zone. It gets ~86% of the sunlight Earth gets (Q1). For TESS, Earth-size planets in the habitable zone are realistic **only around small red stars with many sectors of data**. That's an "if we stumble on it" target, as planned.
- **White dwarfs (opportunistic):**
  - TESS found **one giant planet crossing a white dwarf** (WD 1856+534 b, 2020; Q2).
  - A 2024 search of **313** polluted white dwarfs in TESS found nothing new: only ~0.8% show transits at all (Q3).
  - A June 2026 paper found that **minute-long eclipses around white dwarfs are a "previously underexplored regime"**: standard TESS pipelines miss them, and a custom search in fast (20-s) data found 10 new white-dwarf binaries (Q4).

  **So:** white-dwarf work suits a *custom short-dip search on 20-second data*. That's a possible future side quest; keep it opportunistic.
- **Training quest (hidden siblings):** TOI-700 itself is the ideal practice target: a long-stare-zone star with three known small planets (1-2.6 Earth radii, 10-37 days). My memory says a **fourth planet, TOI-700 e, was found later using extra sectors**. That would be exactly a "hidden sibling" precedent, so it's the first thing to verify next session (UNVERIFIED).

## 1. Habitable zone
- Kopparapu+ 2013 (arXiv:1301.6674): updated 1-D climate-model HZ limits for F/G/K/M stars; the conservative Solar-System HZ in the older Kasting model is 0.95-1.67 AU (abstract; Q5). Use Kopparapu's online calculator / fits for our stars (next session).
- TOI-700 (TIC 150428135): M2 dwarf, 31.1 pc, southern CVZ, 11 sectors, three planets 1-2.6 R⊕, P = 9.98-37.43 d; TOI-700 d 1.19 ± 0.11 R⊕ at ~86% of Earth's insolation (Gilbert+ 2020, arXiv:2001.00952, abstract; Q1).

## 2. White dwarfs
- WD 1856+534 b: giant planet candidate transiting a white dwarf (Vanderburg+ 2020, arXiv:2009.07282, abstract; Q2).
- Robert & Farihi+ 2024 (arXiv:2407.21743): 313 metal-polluted WDs with TESS light curves; BLS + Lomb-Scargle recovered only the 2 known irregular transiters; transit fraction 0.8 (−0.4/+0.6)%; injection-recovery limits from dwarf- to Saturn-size planets, P = 1 h-27 d (Q3).
- Cavalier, de Wit+ 2026 (arXiv:2606.03850): a tailored search for minute-scale eclipses in TESS high-cadence data found 10 WD + cool M-dwarf binaries (periods of a few hours); standard pipelines don't recover such signals efficiently (Q4).

## Not done (carry over)
- **Verify TOI-700 e** (memory lead: found with extended-mission sectors). If true, it's the cleanest "hidden sibling" precedent for the training quest.
- What SPOC's multi-sector searches already cover (Guerrero+ 2021 / SPOC docs), so the training quest doesn't repeat NASA's work.
- A WD target list (Gentile Fusillo Gaia WD catalogue) and how many have 20-s data.
- Which M dwarfs have ≥ 10 sectors (habitable-zone feasibility list).
