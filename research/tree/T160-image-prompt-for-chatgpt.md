# T160 design prompt for ChatGPT (Plus, image generation)

Written by Claude, 13 Nov 2026, for Ahmed to paste into ChatGPT. The goal is only design mock-ups (pictures) of the Tree home page; nothing is built from them until Ahmed and Claude agree on a design in question rounds.

---

You are designing ONE page: the home page of a private research notebook website called **Second Sun**. Please make **design mock-up images** (not code). Read all of this before you draw anything.

## What Second Sun is
Second Sun is a long-term personal research project: a search through NASA TESS telescope data for a **circumbinary planet**, a planet that orbits two stars at once (like Tatooine). Our own search filter is called **Petrova**. The website is the project's book and notebook. It has chapters, lessons, field notes, a live "Search window" page and progress pages. Its owner is learning astrophysics through the project. The site is phone-first, read mostly on an iPhone and added to the home screen like an app.

Live site (open it if you can browse, and look at the home page, a chapter page and the "Search window" page to match the style): https://m1smacker.github.io/second-sun/
If you cannot open it, follow the style rules below exactly.

## What this new home page is
The home page today shows a star picture. It will be replaced by **The Tree**: one interactive map of everything the project is doing. Everything in the project is a branch or a leaf. Tapping any part opens it and explains what it is, why it matters, its status and its progress, with a link to read more.

The Tree's real content:

**Top (the root or crown): the goal.** "Find a circumbinary planet in TESS data, or prove a clean, measured null." Next to it, a **scoreboard**: "Petrova catches 27% of Saturn-like test planets (range 21 to 34%). Verdict: fix first." Show it as a progress meter, not a big number banner.

**Four branches:**
1. **How well we see (Petrova, the engine).** Its leaves are the ways a planet gets lost, each with a count out of 222 test planets:
   - 1.1 Flags hold found planets back: 53
   - 1.2 Outside the searched windows: 52
   - 1.3 The detector misses the dip: 41
   - 1.4 The eclipse mask eats the transit: 15
   - 1.5 Blind spot: binaries of 5 to 10 days
   - 1.6 False alarms
   - 1.7 The scoreboard and its tools
2. **Where we look (the fuel).** Leaves: 2.1 Census (our own binary-star list), 2.2 G1 (the last unseen list, one shot), 2.3 Data and downloads, 2.4 Parked new ideas.
3. **How we prove it (honesty and statistics).** Leaves: 3.1 Statistics and controls, 3.2 Records and tests, 3.3 Leads (how a dip becomes a claim), 3.4 Going public later.
4. **Tools and book.** Leaves: 4.1 Book and learning, 4.2 Search window and control room, 4.3 Machine and housekeeping, 4.4 Eyes pages.

**Every node has a status:** ACTIVE (being worked on now; only one path at a time), NEXT, WAITS (for something named), PARKED, or DONE. Right now the active path is: Codex's report, then node 1.1. Branch 1 leaves are ordered by how many planets they lose.

## How it must behave (show this in the images)
- **Clickable, not highlighted.** The owner said: "It should not be highlighted. It should just be clickable." So: no glow, no neon, no pulsing, no heavy colour fills to show what is clickable. Show that a node can be tapped through calm cues only: a thin outline, a small chevron or "+", a label that looks tappable, a subtle state change on press.
- **Tap a node and it opens in place** (an expanding card or a bottom sheet on phone) with: the name, one plain sentence on what it is, one on why it matters, its status word, a small progress bar or count, the items under it (for example "FIX 91: a flag applied to one side only"), and a "Read more" link and a "Learn this" link to the matching lesson.
- **The active path is easy to follow without highlighting**, for example a solid line for the active path against thin dotted lines elsewhere, or a small status word on each node.
- **Calm and readable.** It's a research notebook, not a game. It should feel like a night observatory: quiet, precise, warm.

## Style rules (copy the book exactly)
- **Default theme is dark ("night observatory"):** page background `#0c1018`, cards `#131a27`, raised cards `#1a2233`, lines and borders `#2a3448`, main text `#f2f4f9`, second text `#c3c9d6`, quiet text `#9aa3b6`, accent warm gold `#eebf6a` (text on gold is `#0c1018`). Status colours from the Search window: green `#3ecf6e` (live), amber `#eebf6a` (warning or waiting), red `#e5584f` (stale or failed). Use them only as small dots or thin marks, never large fills.
- **There is also a light theme:** background `#faf9f6`, cards `#f1efe9`, raised `#ffffff`, lines `#d9d5cb`, text `#10141b`, `#3a4251`, `#566070`, accent dark amber `#6f4608`. Show at least one light-theme frame.
- **Fonts:** interface and labels in IBM Plex Sans; reading text in Atkinson Hyperlegible Next; numbers and data in IBM Plex Mono.
- **Shapes:** corners 6 px, thin 1 px borders, no drop shadows or very soft ones only, motion short and gentle (about 200 ms ease-out, no bounce).
- **Phone first:** design for an iPhone portrait screen (375 px wide) first. Every tappable thing is at least 44 by 44 px; no text smaller than 14 px.
- **Words:** plain, simple English. No dashes as punctuation (no "—" or "–"). No filler slogans or marketing lines. No star names or catalogue numbers anywhere.

## What to make
Make **three design directions**, each as its own set of images, so the owner can choose:
- **A. A real tree:** trunk, branches, leaves, drawn with thin gold lines on the dark sky, the goal at the crown, roots for the tools.
- **B. A clean branching diagram:** a vertical outline tree, like a family tree or file tree, very readable on a phone.
- **C. A radial map:** the goal in the centre, the four branches as arcs around it, the leaves on the rim.

For **each direction**, make these frames:
1. Phone, dark theme: the home page as it first opens (the whole Tree visible or easy to scroll, the goal and the scoreboard at the top).
2. Phone, dark theme: node 1.1 tapped and opened (its card or bottom sheet with the details listed above).
3. Desktop (about 1440 px wide), dark theme: the whole Tree with one node open beside it.
For the direction you think is best, also make 4. Phone, light theme: the home page.

Make the images large and readable (one frame per image), with real text from the content above, not placeholder text.

## How to check your own work before you show it
- Compare every colour with the hex values above. No new colours except very small tints of these.
- Check that nothing is highlighted to show it is clickable (no glow, no bright fills).
- Check the text size (nothing under 14 px at phone scale) and the tap targets (44 px).
- Check that the active path can be followed with no colour at all (shape or line style only), so it works for colour-blind readers.
- Check that every number matches the content above.
- Then write a short note under the images: which direction you recommend and why, what is clickable in each frame, and anything you were unsure about.
