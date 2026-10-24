# Prompt for ChatGPT: revise the Second Sun visual identity brief (24 Oct 2026)

*Written by Claude Code at Ahmed's request, after the Compass review in `research/compass-reviews/2026-10-24-visual-identity-prompt.md`. Everything below the line is the text to paste into ChatGPT. Facts in it were read from the repository and the live book on 24 Oct 2026.*

---

You wrote the brief titled "SECOND SUN, VISUAL IDENTITY REDESIGN (Phase 1: design a complete interactive prototype in a Claude Artifact)". I am Claude Code, the AI that builds and maintains the Second Sun book together with its author, Ahmed Hanzala. Ahmed asked me to review your brief against the real project before anyone builds from it, and to ask you to revise it.

Your intent is good and most of it should stay. This message lists what to keep, the verified facts about the real book (you may not be able to open the site, so treat these facts as the source of truth), my concerns with the fix I want for each, and the improvements I am asking you to add. Please return one revised, paste-ready brief. I will review the revision again before anything is built, and you do not need to build anything yourself.

## A. Keep these exactly as they are

- The two-phase structure and the hard stop: Phase 1 is a prototype in a Claude Artifact only, nothing in the real site, repository or deployment is touched, and Phase 2 starts only after Ahmed's explicit approval.
- The honesty rules: no invented chapters, discoveries, statistics, annotations, dates or editions.
- One finished design direction, not several concepts.
- The balance of editorial book, research journal and quiet astronomy, the avoid-list, and the idea that the opening page shows identity before metrics.

## B. Verified facts about the real book

**B1. Technology.** A static site built with Material for MkDocs (`mkdocs-material`, `custom_dir: overrides`), a Python build hook that generates the Cygnus map and an offline service worker, and custom CSS in three files (`extra.css`, `observatory.css`, `shape.css`). Plain JavaScript, no framework (Eyes mode practice game, small interactive demos, a read-aloud button). Hosted on GitHub Pages at m1smacker.github.io/second-sun and added to the iPhone Home Screen as a web app. It works offline: the service worker precaches 4.7 MB of a 25 MB budget. Fonts are hosted inside the book: Inter (variable, latin, upright and italic) and IBM Plex Mono (weights 400 and 500, used for labels and data), both under the SIL Open Font License. The body font before 23 Oct 2026 was Source Serif 4. There is a day/night switch.

**B2. The real structure.** Author name on the book: Ahmed Hanzala (use exactly this spelling). Three top tabs:
- Read: Start here; The journey path; The story so far; How to read this book; then six Parts. Part 1 The sky and the data (1 Stars, names and missions; 2 Light curves; 3 Our data). Part 2 Two suns (4 Two suns; 5 Wandering transits; 6 Orbits and the three-body problem). Part 3 Finding dips (7 Noise and statistics; 8 Our detector; 9 Fake planets). Part 4 Is it real? (10 Vetting; 11 Pixels and neighbours). Part 5 The professionals' tool (12 STANLEY). Part 6 How the project runs (13 Your workshop; 14 Credit and publishing; 15 Our mistakes, as lessons). Each Part also has an overview page, a "Check yourself" review page, an optional "Try it yourself" labs page and a printable one-page cheat sheet, none of which are in the menu.
- Hunt: Progress; Quests; Candidates (none yet); Eyes mode; Field notes (an index plus notes dated 19, 20, 21, 23 and 24 Oct 2026); Learning track (levels L0 to L6 on one page, plus one lesson page, L1).
- Reference: Glossary; Facts (the claims register); Reading list.

**B3. The homepage today, top to bottom.** Title; byline "Project diary, Ahmed Hanzala with Claude, NASA TESS public data"; the Cygnus map (an SVG of the real sky around Cygnus, east to the left, built from the Bright Star Catalogue and the Villanova Kepler EB catalog: six large stars are the six Parts at their true positions, small dots are chapters, amber specks are 546 of the project's 549 Kepler stars); four tiles (where you stopped, readiness 48 of 100, candidates 0, latest field note); an intro paragraph written to Ahmed; a "Where you are" box; a "Mission readiness" panel with six gauges; a "Mission status" panel with six rows; the contents by Part; a short "More" list.

**B4. A chapter today.** A "You are here" strip with progress dots and the path; title; a one-line meta label; a Listen button (read aloud); a "1-minute summary" box (three bullets); a short story; an "In plain words" box; numbered sections (2.1, 2.2 ...); tappable glossary terms that open a small definition; small shape-coded evidence chips; a "Mark as read" button and a "Next" link that says why you might want it. Left menu and right contents rail on desktop.

**B5. A field note today.** Title such as "24 October 2026: feedback that is measured, not copied"; a meta line "Field note, day 6, about 9 min" (day 1 is 19 Oct 2026); an "In plain words" box; sections: What we did and why; The idea behind it; How you could do it yourself; What we found and what we did not; Questions (collapsible). The index is a table of date and main lesson.

**B6. Colour tokens today.** Night: background #0c1018, surface #131a27, raised #1a2233, line #2a3448, text #f2f4f9, secondary #c3c9d6, tertiary #9aa3b6, accent #eebf6a. Day: background #faf9f6, surface #f1efe9, raised #ffffff, line #d9d5cb, text #10141b, secondary #3a4251, tertiary #566070, accent #6f4608. Corner radius 6 px. Minimum tap height 44 px.

**B7. Who wrote what.** The book is a diary written to Ahmed by Claude from the day's work: it addresses him as "you", the home page opens "Ahmed, this is your book", and the byline is "Ahmed Hanzala with Claude". Field notes are second person and written by Claude. Ahmed's own words appear as his decisions and questions, not as authored paragraphs. Every fact carries an evidence chip whose meaning is carried by shape, not colour: VERIFIED (solid outline), LIKELY (dashed), UNVERIFIED (dotted). Chips link to the claims register, where each fact has an id (for example F-059).

**B8. The reader and his earlier decisions.** Ahmed reads mostly on an iPhone in short bursts, often at night, and also on a PC. On 23 Oct 2026, after 19 rounds of questions, he approved: a dark night-sky look by default with light on request, high contrast, quiet motion, three tabs, the map home page, optional labs, and the Inter font (chosen from Literata, Inter and Source Serif 4). Your brief may propose changes to any of this, but they must be presented as choices for him to approve.

**B9. Checks that every real build must pass (Phase 2).** Text, secondary text and accent colours at least 7:1 contrast on every surface in both schemes; no sideways scroll at 375 px width and tap targets at least 44 px; offline use with fonts hosted in the book; reduced-motion respected; a strict site build; every link and anchor resolving; no en or em dashes in visible text.

**B10. Features that must survive any redesign.** Eyes mode (a canvas game with answer buttons, a banner and a results table), the optional labs, the Listen button, glossary pop-ups, mark-as-read and reading progress, search, instant page navigation, the per-Part cheat sheets, the day/night switch.

## C. My concerns, and the fix I want in the revised brief

1. **Voice.** Your brief pictures a first-person field notebook. The real record is a diary written to Ahmed by Claude (B7). Remove any request for personal reflections, handwritten-style annotations or "his voice". Ask the design to show who wrote what (byline "Ahmed Hanzala with Claude"; each field note marked as written by Claude from the day's work; Ahmed's decisions shown as decisions). The honest "marginalia" is the evidence apparatus: the shape-coded chips, claim ids, glossary terms, and the "Idea" and "You could try" lines. Ask for those to become the margin.
2. **It reopens yesterday's decisions (B8).** Ask for one direction shown in both schemes, night and day, with a switch, and say which scheme is the default. Ask the prototype to end with a short decision list for Ahmed: default scheme, serif titles plus Inter for the interface, any label renames, any layout change.
3. **Colour and contrast.** "Muted brass" fails the 7:1 rule when used as text on ivory. Measured: #b08d57 on #faf7ef is 2.9:1, #a67c3d on #f3ead7 is 3.2:1, a typical grey #6b6f7a on ivory is 4.7:1. These pass: ink #1b1f2a on ivory #faf7ef 15.4:1, deep brass #6f4608 on #faf9f6 7.8:1, amber #eebf6a on night #0c1018 11.2:1, ivory #f3ecdc on midnight #0f1a33 14.7:1. Ask for a rule: text, secondary text and accent text at least 7:1; brass and similar lighter tones only for non-text ornaments (rules, orbit lines, ticks), which should still be clearly visible (at least 3:1).
4. **Fonts.** The real site must host its fonts and needs an open licence. Ask for at most two families (a serif for titles, quotations and optionally body, plus Inter) and say whether the existing IBM Plex Mono labels stay or go, with a reason. The Artifact itself may load fonts through Google Fonts because that is all an Artifact allows, but name only fonts that are free to host.
5. **Device and accessibility.** Ask for phone-first: design at 375 px first, tap targets at least 44 px, no sideways scroll, reduced motion, visible keyboard focus, and a reading measure of about 60 to 70 characters.
6. **Do not break (B10).** Add the list to the brief and ask that the contents and chapter views show where Listen, mark-as-read and the glossary live.
7. **Invention limits.** No volume, edition or publication date is supported. True and usable: "Field notes since 19 October 2026" and "day 6". Keep metrics off the cover, but ask for one plain status line near the foot of the opening page and a link to Progress, because the book's honesty ("nothing here is a discovery yet") must not be lost to elegance. Counts and statuses in the prototype must be copied from the real site, never made up.
8. **Naming.** "Learning record" is the existing "Learning track" (levels L0 to L6, one lesson page so far; show unwritten levels as such). Field notes currently sit under Hunt. Renaming tabs (for example Read to The Book) or giving the field journal its own top-level place are fine as proposals, because URLs come from file paths and are not affected by menu changes. Ask for old and new labels side by side in the contents view.
9. **What an Artifact can do.** It is a single self-contained page (HTML, CSS and JavaScript in one file), private until shared, with a size limit far above what this needs. It cannot be assumed to read the live site, so Claude will embed real material: the map SVG from the built home page, the chapter list, the text of Chapter 2 (about 6 KB), the 24 Oct field note (about 7 KB), and a light-curve figure drawn from the real TOI-1338 sector 98 file (40 KB, shown as labelled 10-minute averages). Claude can check the phone layout at 375 px in a desktop browser pane but cannot test on a real iPhone. Ask the brief to say this plainly and to stop asking Claude to "inspect the website" in the abstract: give it the page list to inspect instead (home, Chapter 2, the field notes index, the 24 Oct note, Progress, Eyes mode, Learning track).
10. **Length and cost.** The brief is long and repeats itself. Cut it by about a third. Replace broad review questions ("does it feel like a book?") with checks that can be answered yes or no.
11. **Vagueness that forces guesses.** Several instructions say "consider" or "explore" where the builder needs a decision. Replace them with specifics (see D).
12. **Scope and usage.** A polished five-view Artifact is a large job. State the build order (homepage, chapter, field note, contents and navigation, then the phone pass) and allow at most two self-revisions before showing Ahmed.

## D. How to make the brief better: please add these

1. **A design token table:** names, roles, and starting values for night and day (use the passing colours in C3), spacing scale, rule weights, radius.
2. **A type roles table:** role (cover title, part title, chapter title, section heading, body, small caps label, caption, table, code, note), family, size range at 375 px and at desktop, weight, line height, measure.
3. **Layout rules:** reading column width, desktop contents rail, mobile behaviour, running header and folio specification, figure numbering (for example "Figure 2.1" per chapter) and caption style, table style, and a short list of allowed callout types so the repeated boxed callouts of today are replaced by a few editorial devices.
4. **The signature element:** say exactly where the Cygnus map recurs (for example a Part marker, a running-header glyph, or a reading-progress ornament), at what size, and how it stays honest (true star positions, no decoration pretending to be data).
5. **A component inventory for the Artifact,** with the real content for each view, a view switcher, and the night/day switch.
6. **A decision log** at the end of the Artifact, as in C2.
7. **A measurable acceptance checklist,** for example: every text and accent colour at least 7:1, no sideways scroll at 375 px, tap targets at least 44 px, no en or em dashes, no figure without a source label, no invented number, byline and evidence chips present.
8. **A short Phase 2 section** that names the checks in B9 and the features in B10 as conditions for any later real build.

## E. What to send back

1. The revised brief, paste-ready, about 1,100 to 1,500 words, with the facts from section B embedded in a "Project facts" block. Keep the phase-gate wording from your original.
2. A change log of at most 12 bullets: what you changed and why.
3. Up to 5 questions you still need Ahmed to answer, each answerable in one line.

Do not add new ideas beyond those requested. Do not use en or em dashes in any text that would appear in the book. Do not ask for anything outside design.
