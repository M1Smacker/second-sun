# Visual identity brief v2 (ChatGPT's revision, saved unchanged) plus the Compass addendum

*Saved 24 Oct 2026 so nobody has to paste it again. The brief below is exactly what ChatGPT returned after the revision prompt (`research/chatgpt-visual-identity-revision-prompt-2026-10-24.md`). The Compass review is `research/compass-reviews/2026-10-24-visual-identity-brief-v2.md`. The addendum at the end is part of the brief when it is run. Status: not run yet; planned for after the weekly reset (about 01:00 Tuesday 27 Oct Kuwait time), in a fresh session, only when Ahmed says "run Phase 1".*

---

SECOND SUN, VISUAL IDENTITY REDESIGN

Phase 1: Design a complete interactive prototype in a Claude Artifact

## Mission

Redesign the visual identity of the Second Sun book as one coherent, editorial-quality reading experience. Combine the intimacy of a scientist’s notebook, the clarity of a scientific monograph, and the quiet atmosphere of an astronomical observatory.

This is a design task, not a content rewrite or a software migration. Preserve the real scientific record, its authorship, evidence system, navigation, and working features. Make the reading experience feel deliberately designed rather than like ordinary documentation.

THIS IS A TWO-PHASE TASK.

Phase 1: Prototype only. Build a complete, interactive, self-contained Claude Artifact. Do not edit the real website, repository, configuration, source files, data, or deployment. Do not begin Phase 2.

STOP after Phase 1 and present the Artifact to Ahmed for review. Phase 2 may begin only after Ahmed explicitly approves the design. Approval of the prototype is not permission to deploy automatically. No permanent changes are authorized by this brief.

## 1. Project facts

Treat the following as verified source material. Do not invent missing information.

Project and technology

* Second Sun is a static book built with Material for MkDocs, a custom overrides directory, Python build hooks, and three custom CSS files: extra.css, observatory.css, and shape.css.
* Plain JavaScript powers Eyes mode, interactive demonstrations, and read-aloud functionality. The site includes an offline service worker.
* Published at m1smacker.github.io/second-sun and used on an iPhone Home Screen as a web app.
* Fonts are hosted locally: Inter variable, including upright and italic styles, and IBM Plex Mono in weights 400 and 500. Both use the SIL Open Font License. Source Serif 4 was the body font before 23 October 2026.
* A day/night switch already exists.

Authorship and voice

The author credit is Ahmed Hanzala. The byline is “Ahmed Hanzala with Claude”. The book is a diary written by Claude to Ahmed about their work. The home page begins “Ahmed, this is your book”. Field notes use second person and are written by Claude from the day’s work. Ahmed’s words appear as his actual decisions and questions, not invented personal prose.

The evidence system uses shape-coded chips: VERIFIED has a solid outline, LIKELY has a dashed outline, and UNVERIFIED has a dotted outline. Each chip links to the claims register, where claims have identifiers such as F-059. Shape, not colour, communicates evidence status.

Real structure

Three existing top-level tabs organize the book:

* Read: Start here; The journey path; The story so far; How to read this book; six Parts and their 15 chapters.
* Hunt: Progress; Quests; Candidates, currently none; Eyes mode; Field notes; Learning track.
* Reference: Glossary; Facts, the claims register; Reading list.

The six Parts are The sky and the data, Two suns, Finding dips, Is it real?, The professionals’ tool, and How the project runs. Their chapters cover stars and missions, light curves, circumbinary planets, transit detection, statistics, vetting, STANLEY, project operations, publishing, and mistakes.

Each Part also has an overview, a Check yourself review, optional Try it yourself labs, and a printable one-page cheat sheet. These supplementary pages are not in the menu.

Field notes are dated 19, 20, 21, 23, and 24 October 2026. The Learning track contains levels L0 to L6 on one page and one lesson page, L1. Unwritten levels must remain visibly unwritten.

Homepage and content samples

The current homepage contains the title and byline, a real Cygnus sky map, four status tiles, an introduction, a Where you are panel, six mission-readiness gauges, six mission-status rows, the contents by Part, and a More list.

The map uses real sky positions, with east to the left. Its six large stars represent the six Parts, small dots represent chapters, and amber specks represent 546 of the project’s 549 Kepler stars. It is generated from the Bright Star Catalogue and the Villanova Kepler eclipsing-binary catalogue.

A chapter includes its reading path, title, metadata, Listen button, three-bullet one-minute summary, narrative, plain-language explanation, numbered sections, tappable glossary terms, evidence chips, Mark as read, and a contextual Next link.

A field note includes a title, metadata, plain-language summary, sections explaining the work and its rationale, a practical suggestion, findings and non-findings, and collapsible questions.

Current state and reader

The latest verified field note is dated 24 October 2026. Use “Field notes since 19 October 2026” and “day 6” where appropriate. No volume, edition, or publication date is established. Current readiness is 48 of 100 and candidate count is zero. These are current project values, not design decorations.

Ahmed reads mainly on an iPhone in short sessions, often at night, and also uses a PC. On 23 October 2026, he approved a dark default, light mode on request, high contrast, quiet motion, three tabs, the Cygnus map homepage, optional labs, and Inter. Propose changes as decisions for him, not as already approved changes.

## 2. Design direction

Deliver one finished direction, shown in both night and day schemes. Night is the default. Include a working scheme switch.

Use the visual language of a serious, beautifully typeset scientific book: generous whitespace, precise alignment, restrained astronomical details, clear chapter hierarchy, elegant rules, and carefully composed figures. The sky should establish identity, not compete with the writing.

Avoid generic dashboards, generic documentation styling, excessive cards, decorative handwritten fonts, fake aged paper, stock space imagery, gratuitous gradients, neon effects, excessive animation, and invented handwritten annotations.

Replace repeated boxed callouts with a small editorial vocabulary: a plain-language explanation, a short summary, an evidence note, and a practical experiment suggestion. Keep each device visually distinct and use boxes only when they serve a clear purpose.

## 3. Design tokens

Use these starting values. Text, secondary text, and accent text must each achieve at least 7:1 contrast against every surface in both schemes. Lighter brass tones are ornaments only, never text. Non-text ornaments must achieve at least 3:1 contrast where necessary to convey information.

| Token | Night | Day |
|---|---|---|
| Background | #0c1018 | #faf9f6 |
| Surface | #131a27 | #f1efe9 |
| Raised surface | #1a2233 | #ffffff |
| Primary text | #f2f4f9 | #10141b |
| Secondary text | #c3c9d6 | #3a4251 |
| Tertiary text | #9aa3b6 | #566070 |
| Accent text | #eebf6a | #6f4608 |
| Decorative brass | #eebf6a | #b08d57 |
| Rule | #2a3448 | #d9d5cb |

Use 4, 8, 12, 16, 24, 32, 48, and 64 px spacing units; 1 px hairlines and 2 px emphasis rules; 6 px corner radius; and a minimum 44 px interactive target. Decorative brass on day surfaces is allowed only for non-text ornaments and must pass the visibility check.

## 4. Typography and layout

Use at most two font families in the proposed design: one free-to-host, open-licensed serif for titles, quotations, and optionally body text, plus Inter for interface text. Decide whether IBM Plex Mono remains for technical labels and data. If retained, explain why it is necessary despite the two-family preference; otherwise use Inter for those roles. All proposed fonts must permit local hosting under an open licence. Google Fonts may be used inside the Artifact only.

| Role | Family | Size at 375 px | Desktop size | Weight and line height |
|---|---|---|---|---|
| Cover title | Serif | 36 to 42 px | 52 to 64 px | Regular, 1.1 |
| Part title | Serif | 30 to 34 px | 40 to 48 px | Regular, 1.15 |
| Chapter title | Serif | 28 to 32 px | 36 to 44 px | Regular, 1.2 |
| Section heading | Serif | 21 to 24 px | 24 to 30 px | Regular, 1.25 |
| Body | Serif or Inter | 17 to 19 px | 18 to 20 px | Regular, 1.65 |
| Small caps label | Inter | 11 to 12 px | 12 to 13 px | Medium, 1.4 |
| Caption | Inter | 13 to 14 px | 14 px | Regular, 1.45 |
| Table | Inter | 14 to 15 px | 14 to 16 px | Regular, 1.5 |
| Code | Monospace | 13 to 14 px | 14 px | Regular, 1.5 |
| Note | Inter | 14 to 15 px | 15 to 16 px | Regular, 1.5 |

Use a body reading measure of 60 to 70 characters. On desktop, provide a restrained contents rail beside the main reading column. On mobile, use one column, compact navigation, and no persistent rail that crowds the text. Include a subtle running header with the book or Part identity and a folio showing the chapter number or page context. Use no simulated print page numbers where no pagination exists.

Number figures per chapter, such as “Figure 2.1”. Captions must identify what is shown and provide a source label. Tables should use clear column alignment, quiet horizontal rules, and accessible labels rather than heavy grid boxes.

## 5. Signature element

The real Cygnus map is the identity anchor. Embed the actual SVG supplied for the Artifact. Reuse a small, simplified fragment of the same map as a Part marker and a running-header glyph, approximately 20 to 28 px in the header and 40 to 56 px at Part openings. Do not redraw star positions arbitrarily, invent constellations, or make decorative marks resemble data. Preserve east-left orientation and identify the map’s source.

## 6. Build the Artifact

Create a single self-contained HTML, CSS, and JavaScript Artifact. It is private until shared. Do not assume it can inspect the live website or repository automatically.

Embed the actual material supplied for the prototype: the Cygnus map SVG, complete chapter list, Chapter 2 text (about 6 KB), the 24 October field note (about 7 KB), and the real TOI-1338 sector 98 light-curve figure (about 40 KB), with labelled 10-minute averages.

Build in this order:

1. Homepage: Identity, byline, Cygnus map, short introduction, restrained status line near the foot, and a link to Progress. Keep metrics off the cover area. Preserve the truth that there are no candidates yet and no discovery.
2. Chapter view: Use real Chapter 2 content, evidence chips, glossary interactions, Listen, reading progress, Mark as read, and Next.
3. Field note view: Use the real 24 October note and distinguish Claude’s account of the work from Ahmed’s decisions.
4. Contents and navigation: Show the actual hierarchy and make navigation between views work. Include old and proposed labels side by side wherever a rename is proposed.
5. Phone pass: Review all views at 375 px, then check desktop layout.

Provide a view switcher and a working day/night switch. Clearly identify the views as prototype views, not live routes. The Artifact cannot be assumed to test on a physical iPhone. Check its phone layout in a desktop browser pane and state this limitation.

## 7. Preserve existing functionality

The prototype must account for all of these features, even where the supplied sample content cannot reproduce the full production implementation:

* Eyes mode, including its canvas game, answer buttons, banner, and results table.
* Optional labs and per-Part printable cheat sheets.
* Listen, glossary pop-ups, Mark as read, and reading progress.
* Search and instant page navigation.
* Day/night switch and offline reading expectations.

The contents and chapter views must explicitly show where Listen, Mark as read, and glossary definitions live. Do not imply that a static demonstration replaces the production implementation.

## 8. Acceptance checklist

Before showing Ahmed the Artifact, verify each item:

* [ ] One coherent direction is shown in both schemes, with night as default.
* [ ] Byline and authorship distinctions are correct.
* [ ] The supplied real map, chapter, field note, and light curve are used.
* [ ] Every figure has a source label.
* [ ] Evidence chips preserve their correct shapes and claim links.
* [ ] No chapter, finding, statistic, date, edition, or claim is invented.
* [ ] Current metrics match the supplied real project state.
* [ ] Text, secondary text, and accent text achieve 7:1 contrast on every surface.
* [ ] Non-text ornaments meet 3:1 contrast where needed.
* [ ] No sideways scrolling occurs at 375 px.
* [ ] Interactive targets are at least 44 px high.
* [ ] Keyboard focus is visible and reduced-motion preferences are respected.
* [ ] Reading measure, type hierarchy, figures, tables, and callouts follow this brief.
* [ ] Every visible prototype control works or is explicitly labelled as a non-functional demonstration.
* [ ] No en dashes or em dashes appear in visible text.
* [ ] No production files or deployment were changed.

Allow at most two self-revisions before presenting the Artifact to Ahmed. Report any failed checks honestly.

## 9. Phase 2: conditions for later work

Phase 2 is not authorized by this brief. Only after Ahmed explicitly approves the prototype may a separate implementation plan be prepared for the real site.

Any later build must pass a strict MkDocs site build; verify every link and anchor; achieve 7:1 contrast for text, secondary text, and accent text in both schemes; work at 375 px without sideways scrolling; preserve minimum 44 px targets; respect reduced motion; retain locally hosted fonts and offline operation; and contain no en or em dashes in visible text.

Eyes mode, optional labs, Listen, glossary pop-ups, Mark as read, reading progress, search, instant navigation, printable Part cheat sheets, and the day/night switch must survive. These are mandatory conditions, not optional improvements.

## 10. Decision log

End the Artifact with a concise decision list for Ahmed:

1. Confirm night as the default scheme or request day.
2. Approve or reject serif titles with Inter for the interface.
3. Approve or reject the IBM Plex Mono label treatment.
4. Approve or reject proposed label changes, showing old and new labels side by side.
5. Approve or reject any proposed layout or navigation changes.

Do not treat silence or prototype review as approval. Stop after presenting the Artifact, the acceptance checklist, known limitations, and this decision list.

---

## Compass addendum (24 Oct 2026), part of the brief when it is run

1. Contrast: day decorative brass is `#9a7a3c` (3.8, 3.5 and 4.0 on background, surface and raised). Tertiary text only for non-essential metadata, at least 4.5:1. Captions, labels and chip text use secondary text or stronger. Control borders and chip outlines reach 3:1 and never use the rule colour. Map stars, chip outlines and light-curve points that carry meaning use text-strength colours. Compute every ratio with a script and print them in the checklist.
2. Measure: 60 to 70 characters on desktop only. On a phone fill the column with 16 px gutters (about 38 to 45 characters at 17 to 19 px) and do not shrink the type.
3. Fonts: name one open serif (Source Serif 4 or Literata) and say why. Default body is Inter, because Ahmed chose Inter for reading on 23 Oct. Offer serif body only as a visible "Reading font: Inter or serif" switch. Add "body font" as item 6 of the decision log.
4. Type: add a sub-section heading role (19 to 21 px at 375 px, 21 to 24 px on desktop, line height 1.3). Small caps labels at least 12 px. Specify the desktop reading column width, the contents rail width, and the running header and folio text.
5. Byline and authorship labels are one component with one source of text, not hard-coded into layouts, because the balance of credit may change over time.
6. Field note: mark Ahmed's decisions only where the note itself reports what he said or chose ("You said", "You chose"). Add no new attributions.
7. The margin is the evidence apparatus: chips, claim ids, glossary terms and the "Idea" and "You could try" lines. Show one "Idea" line and the collapsible questions in the field note view.
8. Sources, read from the repository by Claude Code so Ahmed copies nothing: map SVG from the built home page (generated by `book/hooks.py`), chapter list from `book/mkdocs.yml`, Chapter 2 from `book/docs/book/02-light-curves.md`, the field note from `book/docs/field-notes/2026-10-24.md`, the light curve from `book/docs/assets/data/toi1338-s98.json` (label it: TESS sector 98, TOI-1338, 10-minute averages). Look at these live pages before designing: home, Chapter 2, field notes index, the 24 Oct note, Progress, Eyes mode, Learning track.
9. Read the readiness and candidate values from the live home page on the day of the build and print their "updated" date beside them.
