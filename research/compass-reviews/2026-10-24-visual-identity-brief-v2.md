# Compass review: ChatGPT's revised "Second Sun, Visual Identity Redesign" brief (v2), 24 Oct 2026

*Review only: nothing built, no Artifact made, no site file changed. I checked v2 against my first review (`2026-10-24-visual-identity-prompt.md`, 12 concerns), the repository, and measured its own colour tokens and type sizes with a script. The brief itself is saved unchanged in `research/visual-identity-brief-v2-2026-10-24.md`, with the addendum below appended.*

Labels: **VERIFIED** (measured or read), **LIKELY**, **UNCERTAIN**, **NOT TESTED**.

## 1. Verdict: APPROVE WITH A SHORT ADDENDUM (accept about 92%; no second round with ChatGPT needed)

v2 took nearly every concern on board. What remains is nine small fixes that I can apply myself as an addendum when the brief is run, which is cheaper than another round.

## 2. How v2 answered the 12 concerns

| # | Concern | Result in v2 |
|---|---|---|
| 1 | Voice and authorship | **Done.** Byline "Ahmed Hanzala with Claude", diary written to Ahmed, field notes second person, Ahmed's words only as real decisions. Gap: the evidence chips, claim ids and "Idea" lines are not named as the margin |
| 2 | Reopens 23 Oct decisions | **Done.** Both schemes with a switch, night default, five-item decision log |
| 3 | Contrast | **Mostly done.** Token table and 7:1 rule are sound (see section 3); two slips |
| 4 | Fonts | **Mostly done.** Two families, open licence, hosting rule. The serif is left unnamed and the body is "Serif or Inter" |
| 5 | Phone and accessibility | **Done**, but one rule is impossible on a phone (section 3) |
| 6 | Features to keep | **Done** (section 7 of the brief) |
| 7 | Invention limits | **Done.** "Field notes since 19 October 2026", "day 6", no edition. Missing: an "as of" date on the metrics |
| 8 | Naming and Learning track | **Done**, old and new labels side by side |
| 9 | What an Artifact can do | **Mostly done.** "Supplied" material has no named source, and the list of live pages to inspect was dropped |
| 10 | Length | **Not met** (asked for 1,100 to 1,500 words; v2 is roughly double, **UNCERTAIN, estimated, not counted**). Acceptable: the facts block is most of it and it costs little next to the build |
| 11 | Vagueness | **Mostly done.** Tokens, type roles, sizes and a signature-element spec are concrete. Missing: a sub-section heading level, column and rail widths, header and folio content |
| 12 | Scope | **Done.** Build order and two self-revisions |

The eight additions I asked for are all present. The change log and the list of questions for Ahmed are not in what was pasted (**UNCERTAIN**: ChatGPT may have sent them separately).

## 3. What I measured, and what is wrong

**Colour (VERIFIED, by script).** Every text, secondary text and accent pairing on all three surfaces in both schemes passes 7:1 (lowest: day accent on surface 7.15, night secondary on raised 9.58). Two slips:
1. **Day "decorative brass" `#b08d57` fails the brief's own 3:1 rule** on the two main surfaces: 2.94:1 on the background, 2.69:1 on the surface (3.09 on raised). `#9a7a3c` gives 3.82, 3.50 and 4.02, so it passes everywhere.
2. **Tertiary text is not covered.** It measures 6.28 to 7.51 at night and 5.53 to 6.36 by day: below 7:1 but above 4.5:1. It must be restricted to non-essential metadata.
Also, hairline rules (1.3 to 1.5:1) are fine only as decoration; control borders and chip outlines must not use them.

**Reading measure (LIKELY, calculated).** "60 to 70 characters" cannot be met on a phone: at 375 px with 16 px gutters, 17 to 19 px text fits about **35 to 42 characters**. The rule must be desktop only; shrinking the font to chase 60 would hurt readability.

**Type table.** There is no sub-section heading level, but the real chapters have one (the right-hand contents of Chapter 2 nests items under 2.3, **VERIFIED** on the live page). Labels at 11 px are below the book's present 13 px small text and tiring on an iPhone at night; 12 px minimum.

**Body font.** On 23 Oct Ahmed chose Inter "for reading, headings and UI" (comment in `observatory.css`). A serif body reopens that pick more strongly than serif titles. Show serif body as a visible "Reading font" switch so he can compare, with Inter as the default.

**Byline.** Ahmed told me the book is meant to become his own notebook later, with exact credit to Claude. The byline and "who wrote this" labels should therefore be one component fed by one source, not hard-coded into layouts.

## 4. The addendum to append when the brief is run

> **Compass addendum (24 Oct 2026).**
> 1. Contrast: day decorative brass is `#9a7a3c` (3.8, 3.5 and 4.0 on background, surface and raised). Tertiary text only for non-essential metadata, at least 4.5:1. Captions, labels and chip text use secondary text or stronger. Control borders and chip outlines reach 3:1 and never use the rule colour. Map stars, chip outlines and light-curve points that carry meaning use text-strength colours. Compute every ratio with a script and print them in the checklist.
> 2. Measure: 60 to 70 characters on desktop only. On a phone fill the column with 16 px gutters (about 38 to 45 characters at 17 to 19 px) and do not shrink the type.
> 3. Fonts: name one open serif (Source Serif 4 or Literata) and say why. Default body is Inter, because Ahmed chose Inter for reading on 23 Oct. Offer serif body only as a visible "Reading font: Inter or serif" switch. Add "body font" as item 6 of the decision log.
> 4. Type: add a sub-section heading role (19 to 21 px at 375 px, 21 to 24 px on desktop, line height 1.3). Small caps labels at least 12 px. Specify the desktop reading column width, the contents rail width, and the running header and folio text.
> 5. Byline and authorship labels are one component with one source of text, not hard-coded into layouts, because the balance of credit may change over time.
> 6. Field note: mark Ahmed's decisions only where the note itself reports what he said or chose ("You said", "You chose"). Add no new attributions.
> 7. The margin is the evidence apparatus: chips, claim ids, glossary terms and the "Idea" and "You could try" lines. Show one "Idea" line and the collapsible questions in the field note view.
> 8. Sources, read from the repository by Claude Code so Ahmed copies nothing: map SVG from the built home page (generated by `book/hooks.py`), chapter list from `book/mkdocs.yml`, Chapter 2 from `book/docs/book/02-light-curves.md`, the field note from `book/docs/field-notes/2026-10-24.md`, the light curve from `book/docs/assets/data/toi1338-s98.json` (label it: TESS sector 98, TOI-1338, 10-minute averages). Look at these live pages before designing: home, Chapter 2, field notes index, the 24 Oct note, Progress, Eyes mode, Learning track.
> 9. Read the readiness and candidate values from the live home page on the day of the build and print their "updated" date beside them.

## 5. Cost and timing
Unchanged: 4 to 8 weekly points for round one, 1 to 3 per revision (**UNCERTAIN**). Run it after the reset (about 01:00 Tuesday 27 Oct Kuwait time) in a fresh session. The brief and addendum are in the repository, so nothing needs pasting.

## 6. The single best next step
Tell me "run Phase 1" after the weekly reset. I will read `research/visual-identity-brief-v2-2026-10-24.md` (brief plus addendum) and build the Artifact.
