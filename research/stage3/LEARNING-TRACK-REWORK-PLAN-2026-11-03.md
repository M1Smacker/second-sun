# Learning track rework: plan only (3 Nov 2026, 22:50 Kuwait)

Ahmed studied two or three chapters of the learning track on the night of 2 Nov and reported six problems. This file is the plan. NOTHING is built, the book is unchanged, no research stint has started. Out of scope by his words: widening the track to astronomy in general (not filed, not planned).

## What he reported, and what our own files say
Labels: CONFIRMED (read in code or counted by script). Anything about how his phone behaves: UNCERTAIN until tested.

| # | His report | What we found | Label |
|---|---|---|---|
| 1 | Verified / not verified on every line | Evidence chips come from `{{claim:F-xxx}}` in the chapter text (`hooks.py` chip()). 125 chips in 15 chapters (20,648 words); chapters 1 to 3 hold 31 in about 3,900 words (8 per 1000 words); 60 of 238 body paragraphs carry one. Each chip is an inline link to the claims register page. The words VERIFIED / LIKELY / UNVERIFIED are the labels on them. | CONFIRMED |
| 2 | Clicking a link leaves the page, no way back | `book/docs/manifest.webmanifest` sets `"display": "standalone"`: if the book is opened from the iPhone home-screen icon there is no browser Back button or address bar. `book.js` has no Back, history or "where was I" code. The chips and glossary links change page. Whether he uses the icon or Safari is not known. | manifest and missing code CONFIRMED; his phone UNCERTAIN |
| 3 | Wants a dashboard that keeps him on track | Today: a text list "The path at a glance" in `learn/index.md`, a Progress page and a readiness bar on the home page. No per-chapter read state, no "continue where you stopped", no current-level bar on chapter pages. | CONFIRMED |
| 4 | Voice is bad, hard to understand | `book.js` read-aloud uses the browser's `speechSynthesis` and never chooses a voice (`u.voice` is not set), so the phone speaks with its default voice. Equations, tables, code and superscripts are skipped or stripped, so sentences that lean on them lose words. | code CONFIRMED; how it sounds UNCERTAIN |
| 5 | Formula text looks odd, a font problem | The build has no maths renderer (no MathJax, KaTeX or arithmatex in `mkdocs.yml`, `hooks.py` or `main.html`). The 14 formula blocks (`.ss-eq`, in 8 chapters) are plain text set in the reading font Atkinson, with two tiny symbol fonts for Greek and signs (`observatory.css` lines 4 to 6). So fractions, powers and subscripts are typed characters, not typeset. His guess (font) is LIKELY right; not yet seen on a phone-sized render. | CONFIRMED setup; look UNCERTAIN |
| 6 | Many questions left unanswered, "assumed I already know" | Not measurable from the files alone. Prior work `research/learning-and-checking-literature-2026-11-02.md` covers HOW to teach (practice, worked examples, mastery checks) but was read from search summaries only, so nothing there is CONFIRMED by a primary page. Nobody has yet listed the questions a newcomer has page by page. | NOT TESTED |

One honesty guard for item 1: the label is today the only place a reader is told a claim is unsure. If the chips leave the reading path, the sentence itself must say so in plain words for every LIKELY or UNVERIFIED claim (13 of 98 rows today: 12 LIKELY, 1 UNVERIFIED). The claims register and its labels stay exactly as they are; they move to their own place, they are not deleted.

## The plan, in order of dependence
Costs are weekly-usage points, LIKELY (from the ledger: a book change plus publish about 0.3, a small scripted edit under 0.2; no new measurement).

**LT-6 First: the content audit (study RS-008, cap 2 points, written before it starts).** It decides how much text changes, so formatting work on text that will be rewritten is wasted. Questions tied to decisions:
1. What did a newcomer ask, page by page? Source 1 (strongest): Ahmed's own questions from the chapters he read, dictated (5 to 10 is enough). Output: a question log, one row per question (page, sentence, what was missing).
2. Which words, symbols or steps are used before they are explained, or never? Source 2 (own data, no cost): a script over the reading order in `path.yml` (`track:`) listing terms, abbreviations and symbols at first use against the glossary and earlier text. Output: a dependency gap list per chapter.
3. For each gap, what does a good introduction do? Source 3: re-open (not search summaries) the two or three primary sources the 2 Nov note rests on that bear on explanation order (worked examples, expertise reversal) and pull the exact sentences; label them. Output: a short "standard" every paragraph is held to.
4. Decision it feeds: which chapters get a rewrite, which get inserted explanation boxes, which are fine; and whether the track is "enough to teach" (his question), answered per level.
Stop line: 2 points or the question log and gap list both filed. Needs Ahmed: his question list (5 minutes, can be dictated).

**LT-1 Labels out of the reading path (fix, about 0.5).** Default: chips hidden while reading, one switch "Show evidence" (remembered on the device), and each chapter ends with a collapsed "Evidence for this chapter" list that carries the label, claim and source (the "other tab" he asked for, also reachable as an Evidence entry in the menu next to the claims register). Sentence wording checked for the 13 LIKELY / UNVERIFIED claims. Touches `hooks.py` chip(), `extra.css`, `book.js`, claims page links.

**LT-2 Back and where-am-I (fix, about 0.8).** A fixed Back control and a "Back to my place" button that return to the page and scroll spot he left; a one-line track bar on chapter pages (Level 2 of 6 · Chapter 4 · section); glossary and evidence links open a small peek instead of leaving the page, with "open page" as a second choice. Needs one answer from him: icon or Safari (decides whether the standalone mode is the cause). Touches `book.js`, `main.html`, `extra.css`.

**LT-3 The track dashboard (build, about 1.5 to 2).** One page, scientific-instrument style in the existing observatory look: level ladder with state per chapter (not started / opened / read to the end), "Continue" button, quiz and check results from the learn checks, open questions logged in LT-6. State stays on the device (no account, no cloud). A NEW design, so it falls under his own 3 Nov rule (no new system designs until T122 verdicts and G3 result); he decides the timing. Design is written and reviewed before any build.

**LT-4 Voice (fix, about 0.5 for a picker; about 1.5 for pre-made audio).** Three routes, to be tried with the same paragraph so he can listen on his phone: (a) choose the best voice the device offers (free; on iPhone the better voices have to be downloaded in its own settings, so UNCERTAIN what Safari exposes); (b) pre-made audio files per chapter from an open-source neural voice run on his PC (a project download, I tell him size and place; about 4 MB per chapter, 60 MB for 15, estimate); (c) a paid cloud voice (outward, needs his yes). Independent of the voice: a pronunciation list (SNR, ppm, TIC numbers, symbols) so equations and codes are spoken as words; I expect this to help understanding as much as the voice does (LIKELY, untested).

**LT-5 Formulas (fix, about 0.6).** One test page with the same four formulas set three ways: as now, in a maths-capable font, and typeset properly (self-hosted KaTeX, works offline, about 300 KB). He picks by looking on his phone; then all 14 blocks are converted. Earlier font tests (`research/redesign-type-tests/REPORT.md`) found a cut of Noto Sans Math works, so (b) is cheap.

## Order I recommend
1. RS-008 part 1 and his question list (cap 1).
2. LT-1 and LT-2 together, one publish (book 2.10.0, a feature, second number), because they are what he hit first and neither depends on the audit.
3. LT-5 and LT-4 samples for him to judge (taste decisions only he can make), then convert.
4. RS-008 part 2 and the rewrite order, then LT-3 once the design is approved.
Total about 6 to 7 points, spread over several days, inside each day's cap. Nothing starts without his go.

## Questions for Ahmed (plain chat)
1. Do you open the book from the home-screen icon or from Safari?
2. Can you dictate 5 to 10 of the questions you had, with the chapter or page, even roughly?
3. Labels: hidden by default with a switch and an Evidence list at the end of each chapter. OK?
4. Voice: shall I make three short samples of the same paragraph for you to listen to?

## Not done / not verified
No page was opened on a phone-sized screen for this plan; items 4 and 5 are judged from code. The question log does not exist yet, so "is the track enough to teach" has no answer yet.
