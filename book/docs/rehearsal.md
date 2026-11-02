# Rehearsal: the real layout

<p class="ss-meta">Hunt · step three of the ladder to real data · every answer saved</p>

!!! plain "In plain words"
    This is the dress rehearsal. Real candidates will be shown to you in exactly this layout, so you practise on it first. Each item is a stretch of real TESS light with at most one thing hidden in it. You look, say what you think it is, lock your answer, and only then see the truth. About three items in ten hide a fake planet. The rest are eclipses, instrument effects, flares, steps, or nothing at all.

<div class="ss-rehearsal" data-deck="../assets/rehearsal-deck.json"></div>
<p class="ss-fallback">With JavaScript on, this spot is the rehearsal: eight sessions of 20 items each.</p>

## How it works

- **Three panels, the same every time.** Panel 1 is the whole sector of light, with the binary's eclipses shaded grey and the event shown as a highlighted column. Panel 2 is the event up close, on a fixed scale (the same for every item of a star), with a faint line for every 6 minutes and a bold line for every 30 minutes. Panel 3 shows where the event falls in the binary's orbit.
- **Six answers.** *Planet-like*, *Eclipse*, *Flare*, *Instrumental*, *Step*, and *Unclear* (nothing there, or you cannot tell). No answer is pre-selected. You can say how sure you are, then you lock.
- **Lock, then truth.** A locked answer cannot be changed. The truth is shown with what was hidden and how deep it was, and whether you called it planet-like correctly.
- **No names, no numbers.** Nothing on the screen says which star it is, and nothing tells you in advance what the hunt's own score was. Only the picture.
- **What the hidden things are.** Fake planets are planted into real light (three clearly visible and three near the limit in every session). Eclipses are the real eclipses of the binary. Instrument effects are a ramp after a data gap or a dip that ends where the data stop. A flare brightens fast and fades slowly. A step is a level change that stays. "Nothing hidden" items are the best wiggle the hunt's own search finds in another part of the sector.
- **The line.** Over eight sessions on at least four different days: at least 80% of the clearly visible fake planets called planet-like, at most 15% of everything else called planet-like, and a d-prime of at least 2. The numbers were written down before this page existed. Claude decides whether your results are enough; the page only does the arithmetic.
- **Saved after every answer**, on this device, and sent by itself to the private cloud copy like the other Eyes rounds. A session you leave half done is kept as abandoned.

## Honest limits of this first version

- Only panels 1 to 3 are here. The second light-curve product, background and centroid panels come in a later version.
- The fake planets are trapezoids planted into real light. A real planet's shape may differ a little, so a good result here is necessary, not sufficient.
- There are eight sessions of 20. After the eighth, the same items come round again, so use the later rounds for habit, not for the line.
- A gap in the window is a real cue: instrument effects sit next to gaps, and the hunt itself would never keep an event next to a gap as a candidate.
- Everything shown is real light from binaries we used for tuning. No candidate and no event of the hunt appears here.
