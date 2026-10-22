# Lab 0: your workbench

<p class="ss-meta">Lab · at your PC · about 10 min · Level L0</p>

!!! plain "In plain words"
    Before you can look at stars yourself, your PC needs the right tools: Python (a programming language) and a few astronomy toolkits. They're already installed in the project folder on D:. In this lab you open a terminal, run one check, and read what it tells you.

**Goal:** run your first command and confirm the workbench is ready.

## What you need to know first

- A **terminal** is a window where you type commands instead of clicking. On Windows it's called **PowerShell**.
- **Python** runs our scripts. The project has its own copy, with all the toolkits, at `D:\second-sun\.venv`. A copy like this is called a **virtual environment**: it keeps the project's tools separate from everything else on your PC.
- **Why D:?** Your C: drive is nearly full. Every lab keeps downloads and temporary files on D:. The file `labs/_env.py`, which every lab loads first, makes sure of that.

The toolkits you'll meet:

| Toolkit | What it does |
|---|---|
| `numpy` | fast maths on long lists of numbers (a light curve is a long list) |
| `astropy` | astronomy basics: times, coordinates, the FITS file format |
| `lightkurve` | finds, downloads and plots TESS and Kepler light curves |
| `astroquery` | asks NASA's archives questions (like "which star is this?") |
| `matplotlib` | draws graphs |
| `wotan` | flattens slow wiggles out of a light curve (Chapter 8) |
| `batman` | draws a perfect planet transit, used to make fake planets (Chapter 9) |

## What you should see

From a real run on your PC (20 October 2026):

```text
Python 3.12.10 at D:\second-sun\.venv\Scripts\python.exe
  numpy       1.26.4
  astropy     7.2.3
  lightkurve  2.6.0
  astroquery  0.4.11
  matplotlib  3.11.2
  wotan       installed
  batman      2.5.1
Drive C:\ free: 22 GB of 479 GB
Drive D:\ free: 540 GB of 1000 GB
Caches go to: D:\second-sun\.cache
Lab downloads go to: D:\second-sun\data\labs
NASA's archive (MAST): reachable
```

How to read it: every toolkit has a version number (wotan doesn't publish one, so it just says "installed"). D: has plenty of space. **MAST** is the archive where NASA keeps all TESS and Kepler data (Chapter 3), and your PC can reach it.

## Do it yourself

??? note "The commands, when you are at your PC"

    1. Press the Windows key, type **PowerShell**, press Enter. A dark window opens.
    2. Copy this, paste it into the window (right-click pastes), press Enter:

    ```powershell
    cd D:\second-sun
    ```

    3. Then this:

    ```powershell
    .\.venv\Scripts\python.exe labs\lab0_check.py
    ```

## What can go wrong

| You see | Why | Fix |
|---|---|---|
| `The term '.\.venv\...' is not recognized` | You're not in the project folder | Run the `cd D:\second-sun` line first |
| A toolkit says `MISSING` | Something got uninstalled | Tell me the line; don't reinstall it yourself |
| `MAST: NOT reachable` | No internet, or MAST is down | Check your internet; try again in 10 minutes |
| Avast pops up about Python | It's scanning a new program | Let it finish. Don't change Avast's settings |

## Your turn

Open the file `D:\second-sun\labs\lab0_check.py` in Notepad (right-click, Open with, Notepad). It's 20 lines. Find the line that checks the free space on your drives, and the line that asks MAST whether it's awake. You don't need to understand every word; just find them.

**Tell me:** "Lab 0 done" and your free space on C:.

**Back to:** [Try it yourself, Part 1](../parts/part1/labs.md)
