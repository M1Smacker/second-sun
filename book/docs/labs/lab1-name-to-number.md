# Lab 1: from a name to a number

<p class="ss-meta">Lab · at your PC · about 15 min · Level L0 · read Chapter 1 first</p>

!!! plain "In plain words"
    You type a star's name. The script asks NASA's catalogue which star that is, then prints its catalogue numbers, where it sits in the sky, how bright and how far away it is, how crowded its neighbourhood is, and every ready-made light curve that exists for it. This is exactly how I start with any star.

**Goal:** go from "Kepler-16" to everything we need to know before downloading data.

## What you should see

From a real run on your PC (20 October 2026) {{claim:F-035}} {{claim:F-036}}:

```text
Kepler-16  ->  TIC 299096355   (KIC 12644769, Gaia DR3 2133476355197071616)
  position: RA 289.07573 deg, Dec 51.75744 deg
  brightness: TESS magnitude 10.94 (smaller = brighter)
  star: 4018 K, radius 0.77 Sun, distance 75 parsecs
  neighbours within 1 arcminute: 15, of which 4 are less than 5 magnitudes fainter

Ready-made light curves: 94
  CDIPS        8 files, sectors [14, 15, 26, 40, 41, 53, 54, 55]
  QLP         17 files, sectors [14, 15, 26, 40, 41, 53, 54, 55, 56, 73, 74, 75, 76, 80, 81, 82, 83]
  SPOC        26 files, sectors [14, 15, 26, 40, 41, 53, 54, 55, 56, 73, 74, 75, 76, 80, 81, 82, 83]
  TARS        17 files, sectors [14, 15, 26, 40, 41, 53, 54, 55, 56, 73, 74, 75, 76, 80, 81, 82, 83]
  TASOC        9 files, sectors [14, 15, 26]
  TESS-SPOC   17 files, sectors [14, 15, 26, 40, 41, 53, 54, 55, 56, 73, 74, 75, 76, 80, 81, 82, 83]
```

## Do it yourself

??? note "The commands, when you are at your PC"

    ```powershell
    cd D:\second-sun
    .\.venv\Scripts\python.exe labs\lab1_name_to_number.py "Kepler-16"
    ```

    It takes about 20 seconds, because it's asking NASA's servers over the internet.

## Reading it line by line

- **Three names, one star.** TIC is TESS's catalogue number, KIC is Kepler's, and the Gaia number is from the European star map (Chapter 1). Our G1 list stores the KIC and the TIC for every star.
- **Position.** RA and Dec are the sky's longitude and latitude. Dec +51.8° puts Kepler-16 in the northern sky, in the constellation Cygnus, inside Kepler's old field.
- **TESS magnitude 10.94.** About 100 times too faint to see with your eyes (Chapter 1), but bright for TESS. Our G1 list goes down to 13.5.
- **4018 K, 0.77 Suns.** The catalogue treats the light as one star. Kepler-16 is really two stars too close together to separate, so these are blended values.
- **Neighbours.** A TESS pixel is 21 arcseconds wide {{claim:F-024}}, so a star within 1 arcminute shares pixels with ours. Four neighbours bright enough to matter means a dip **could** come from one of them. That's why Chapter 11 exists.
- **94 light curves.** Six different teams turned the same TESS pictures into light curves. **SPOC** is NASA's own and the best. **QLP** is MIT's, made for many more stars (Chapter 3). SPOC has 26 files for 17 sectors because some sectors have both a 2-minute and a 20-second version.
- **Sectors 14 to 83, with gaps.** TESS came back to this part of the sky in 2019, 2020, 2021, 2022, and from late 2023 through 2024 (years checked in the archive's search table).

## How the script works

Open `labs\lab1_name_to_number.py` in Notepad and follow along:

1. `Catalogs.query_object(name, radius=2/60, catalog="TIC")` asks for every TIC star within 2 arcminutes of the name's position.
2. It sorts them by distance and takes the closest: our star. The others are the neighbours.
3. `lk.search_lightcurve(f"TIC {star['ID']}")` asks MAST which light curves exist, and the loop groups them by team.

## What can go wrong

| You see | Why | Fix |
|---|---|---|
| `Could not resolve ... to a sky position` | The name isn't known to the name service | Try the TIC number instead: `"TIC 299096355"` |
| A different star than you expected | Two catalogued stars sit very close together | Check the `KIC` matches the G1 list |
| `nan` for temperature or distance | The catalogue has no value | Normal for some stars |

## Your turn

Pick a star from your G1 list. Open `D:\second-sun\targets\g1_targets.csv` in Notepad and take the **third** star (KIC 4150611). Run:

```powershell
.\.venv\Scripts\python.exe labs\lab1_name_to_number.py "KIC 4150611"
```

**Tell me:** its TIC number (check it against the `tic` column), its TESS magnitude, how many neighbours sit within 1 arcminute, and which teams made light curves for it.

**Back to:** [Try it yourself, Part 1](../parts/part1/labs.md)
