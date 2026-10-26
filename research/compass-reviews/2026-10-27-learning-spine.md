# Compass review: the learning spine proposal (27 Oct 2026)

**Verdict: REVISE.** The direction is right (one path instead of three). Three decisions for Ahmed come before any building. Review only: nothing in the book was changed.

## The proposal
One spine: the levels drive the order; each level shows its chapters, labs, questions and the field notes that taught it; the topic list stays as browse; the Journey page becomes "how the project unfolded"; chapters and field notes link to each other.

## What I checked (VERIFIED, read in the repo on 27 Oct)
- **Three orders exist, plus a switch between two of them.**
  - Topic order is chapters 1 to 15 in six Parts (`mkdocs.yml`).
  - Journey order is 4, 5, 1, 2, 3, 6, 7, 8, 9, 12, 10, 11, 13, 14, 15 (`data/path.yml`).
  - Level order is L0 to L6 (`docs/learn/index.md`).
  - Chapter pages carry a "Reading order: Journey / Topic" switch (`shape.py`), so the chapter Next link already depends on a setting. The levels are not part of it.
- **The levels live in the Hunt tab**, away from the chapters in the Read tab. Only L1 has its own page in the menu; L0 and L2 to L6 are sections of one page.
- **Four chapters belong to no level:** 3 (Our data), 13 (Your workshop), 14 (Credit and publishing), 15 (Our mistakes). Chapters 2, 10 and 11 are split across levels.
- **The track disagrees with the numbers in two places:** L3 (chapters 7 and 8) comes before L4 (chapters 4 to 6), and L2 reaches forward to section 11.3.
- **Chapters link to no field notes** (zero links in `docs/book`). Only the Journey page links to notes.

## What needs changing
1. **Decide the order first (Ahmed's call).** Recommendation: the levels are the one reading path; chapter numbers stay as permanent labels. Renumbering would touch every link, the glossary, the claims register and the notes (cost and risk high, not tested). Each chapter then says "Level 4, step 2 of 3" and its Next link follows the levels. Remove the Journey/Topic switch.
2. **Give the four orphan chapters a home.** Suggest chapter 3 into L0 (it is about the data), and chapters 13 to 15 into a new "L7 Running the project" or a clearly marked "beyond the levels" step.
3. **Keep L3 before L4 (measure before you hunt) and say why in one sentence.** Swapping them is possible but level numbers carry Ahmed's saved progress; I advise against it.
4. **Move the levels to the front of the Read tab** (call it Learn) and keep Hunt for project state. Biggest single fix for the "disconnected" feeling. A menu edit only.
5. **Generate the cross-links from one data file** (like `path.yml`), not by hand, so they cannot drift. Strict build and link checks will catch breaks.
6. **Build order:** do the data, the level pages and the pager now; leave how it looks to the redesign, so the layout is not built twice. Keep level ids unchanged so saved progress survives.

## Cost
Build 2.5 to 5 points if there is no renumbering (UNCERTAIN; renumbering would push it past 6). Review cost about 0.6.

## Best next step
Ahmed answers three questions: (1) levels as the path with stable chapter numbers, yes or no; (2) where chapters 3 and 13 to 15 go; (3) keep L3 before L4, yes or no. Then the build.
