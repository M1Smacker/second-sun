# FIX 96 radius check: is the depth cap holding events only because the catalogue makes the host too big?

Claude, 15 Nov 2026, after Codex 014 part 3 (`research/stage3/rs032/CODEX-014-PART3-KEY-2026-11-15.md`). Node 1.6.

**Plain verdict: PASS.** Every one of the 76 background events the cap held (50 real, 26 upside-down) stays held when each star gets the most generous radius we can find. The catalogue sizes are not making the cap too strict.

## Rule (written in the script before any radius was fetched)
Most generous radius = the smallest of the TIC radius in our light-curve headers, the TIC 8.2 radius at MAST, Gaia DR3 GSP-Phot and Gaia DR3 FLAME. If at least 80% of the held events stay held, the radius risk is small. Same rule for both arms.

## Data
138 design-seen hosts of the background events (0 fenced, checked by the script). Downloads into `data/fix96_radii_2026-11-15/`: `tic82.csv` (11,169 bytes, MAST) and `gaia_dr3.csv` (13,223 bytes, Gaia archive, DR2 to DR3 match by `dr2_neighbourhood`, closest and most similar). Script `fix96_radius_check.py`, rows `radius_rows.csv`, counts `radius_check.json`.

## Numbers
| | Real | Upside-down |
|---|---:|---:|
| Events with a radius | 158 | 77 |
| Held by the cap (header radius) | 50 | 26 |
| Still held with the most generous radius | 50 (100%) | 26 (100%) |
| Held events with a Gaia radius too | 43 | 21 |

- The sources agree: header radius over the smallest one has median 1.00 and maximum 1.25. No host has an independent radius under half the header one (0 of 130 with a radius; 110 have a Gaia radius).
- **Margin:** 22 of the 76 held events are within 2× the cap, and the closest are at 1.00 to 1.01×, so they sit right on the line. With the cap set for a 2.8 Jupiter-radius body instead of 2, these 22 would go free. That is a design choice for Fable (how big a body the cap allows), not tuned here.

## Limits (UNCERTAIN)
- Gaia GSP-Phot and FLAME also see the combined light of a binary, so they are not fully independent of the TIC for blends. LIKELY, not CONFIRMED.
- 12 held events (7 real, 5 upside-down) have only the two TIC radii.

## Plan change
FIX 96 goes to the Fable round as tested: bench cost 0 of 264 planted dips, background 174/79 to 124/53, radius risk checked. Open choice for Fable: the size of body the cap allows (2 Jupiter radii as tested).
