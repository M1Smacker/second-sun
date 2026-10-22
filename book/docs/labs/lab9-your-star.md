# Lab 9: your own star

<p class="ss-meta">Lab · at your PC · about 30 min · Level L6 · the final lab</p>

!!! plain "In plain words"
    This is the whole route on a real G1 star, start to finish: look it up, download its data, find and hide the two stars' eclipses, search for dips, check the dips against upside-down data and spacecraft events, and list what's left for a human to judge. Everything you learned in Labs 1 to 8, in one run. You'll pick the star.

**Goal:** search a G1 star yourself and judge the result like the second key.

!!! warning "Practice, not a hunt"
    Anything this lab finds is a practice event, not a candidate. Real candidates go through the full vetting sheet (Chapter 10), the pixel check (Chapter 11) and both keys. If something looks exciting, tell me; don't post it anywhere.

## What you should see

From a real run on your PC (20 October 2026) {{claim:F-053}}:

```text
TIC 48507019 = KIC 11285625, Tmag 9.812, binary period 10.7904443 d
SPOC 2-minute sectors available: 9; using the first 3
Eclipses found by folding all sectors: 2; masked 19.4% of the data

Sector 14: 0 events above SNR 7, 0 rejected (also in flipped data), 0 events in the flipped data

Sector 15: 0 events above SNR 7, 0 rejected (also in flipped data), 0 events in the flipped data

Sector 26: 0 events above SNR 7, 0 rejected (also in flipped data), 0 events in the flipped data

Events to vet by hand: 0. Pictures in D:\second-sun\labs\out
```

## Do it yourself

??? note "The commands, when you are at your PC"

    The example uses TIC 48507019 and 3 sectors:

    ```powershell
    cd D:\second-sun
    .\.venv\Scripts\python.exe labs\lab9_your_star.py 48507019 3
    ```

    The first number is a TIC from `targets\g1_targets.csv`; the second is how many SPOC sectors to use (about 2 MB each). Every download is written to `research\downloads.csv` automatically, as the project rules require.

## Reading it

- **2 eclipses found, 19.4% masked.** Both of the binary's eclipses were found from Kepler's period alone, by folding all three sectors together. One sector is often too short to pin down a long-period binary, which is why the lab folds them all at once (the lesson from Kepler-16, Chapter 10).
- **0 events, 0 in the flipped data.** A bright (9.8 mag), quiet star. Nothing crossed the bar.
- **What "nothing" means here:** no single crossing bigger than roughly 5 to 6 Earth radii (Chapter 9's floor, for a star this bright or brighter) in the unmasked 80% of three sectors. It does **not** mean no planet: a small one, or one that crossed during the masked 19.4% or between sectors, would be missed.

## How the script works

1. Finds your star in the G1 list (its period and Kepler number).
2. Searches MAST for SPOC 2-minute light curves and downloads the first few (Lab 2), logging each.
3. Folds all sectors at the binary's period to find and mask both eclipses (Lab 5).
4. For each sector: runs the search (Lab 4), runs it again on upside-down data (Chapter 8), reads the gaps and thruster firings, and applies the rules: events also found upside down are rejected; events near gaps or firings get **flags** (Chapter 10).
5. Prints what's left and saves a picture of each event.

## When an event does appear

Ask, in this order (the short version of Chapter 10):

1. **Flags?** Near a gap edge or a thruster firing: suspect, look at the raw data around it.
2. **Shape:** a dip with a flat or curved bottom, not a single spike or a step.
3. **Near an eclipse?** A dip just outside the red masked region may be the eclipse's edge.
4. **Second product (rule C8):** is it in QLP or TESS-SPOC data too?
5. **Pixels (Chapter 11):** is it on our star?

## Your turn

1. Open `targets\g1_targets.csv` and pick a star yourself: one with a **morph between 0 and 0.5** (not −1, see Chapter 1's warning), Tmag between 9 and 12. Check in `targets\g1_coverage.csv` that its `n_spoc` is at least 3.
2. Run the lab on it with 3 sectors.
3. Write down: how many eclipses were found, how much was masked, how many events, any flags.
4. If there's an event, open its picture and go through the five questions above.

**Tell me:** "Lab 9 done", the TIC you chose, and your notes. This is the lab where I check your judgment, not just your numbers.

**Back to:** [Try it yourself, Part 6](../parts/part6/labs.md)
