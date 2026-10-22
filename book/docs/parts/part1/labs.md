# Try it yourself: Part 1

<p class="ss-meta">Optional · hands-on · at your PC</p>

!!! plain "In plain words"
    You can read the whole book without these. Each lab shows the real output first, so you can follow along without running anything. The commands are in a fold, for when you are at your PC.

## [Lab 0: your workbench](../../labs/lab0-workbench.md)

<p class="ss-meta">Lab · at your PC · about 10 min · Level L0</p>

Before you can look at stars yourself, your PC needs the right tools: Python (a programming language) and a few astronomy toolkits. They're already installed in the project folder on D:. In this lab you open a terminal, run one check, and read what it tells you.

## [Lab 1: from a name to a number](../../labs/lab1-name-to-number.md)

<p class="ss-meta">Lab · at your PC · about 15 min · Level L0 · read Chapter 1 first</p>

You type a star's name. The script asks NASA's catalogue which star that is, then prints its catalogue numbers, where it sits in the sky, how bright and how far away it is, how crowded its neighbourhood is, and every ready-made light curve that exists for it. This is exactly how I start with any star.

## [Lab 2: get the data and look inside](../../labs/lab2-get-the-data.md)

<p class="ss-meta">Lab · at your PC · about 15 min · Level L0 · after Lab 1</p>

Now you download one month of TESS data for Kepler-16 (one sector, about 2 MB) and open the file. It's a table: one row every 2 minutes, with the time, the brightness, and a "quality" number that warns about bad moments. Every planet search starts from a file like this one.

## [Lab 3: plot a light curve and measure its noise](../../labs/lab3-plot-and-read.md)

<p class="ss-meta">Lab · at your PC · about 20 min · Level L1 · after Lab 2 and Chapter 2</p>

You draw the Kepler-16 file from Lab 2 as a graph, raw and cleaned, with the thruster firings marked. Then the script measures how much the brightness wobbles when you average 10 minutes, 1 hour, 3 hours or 6 hours of data. That table is how you judge whether a dip is real (Chapter 7).

---

[Review: Part 1](review.md) · [Back to the chapters](../../start/index.md)
