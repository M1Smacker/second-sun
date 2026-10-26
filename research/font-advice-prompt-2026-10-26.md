# Prompt for another AI: which fonts suit the Second Sun book (26 Oct 2026)

*Written by Claude Code at Ahmed's request. Everything below the line is the text to paste into the other AI. Facts were taken from `book/docs/assets/observatory.css`, `extra.css`, `mkdocs.yml` and the visual identity brief. When the answer comes back, run Compass on it before any font changes (to-do item 10a).*

---

I need your expert opinion on fonts for a book I publish as a website. Please read all of it, then answer in the format at the end. I am not happy with the current font and I cannot always say exactly why, so I need you to diagnose as well as suggest.

## 1. What the book is

"Second Sun" is a citizen-science project. I am Ahmed, an amateur who is learning astronomy as the project goes. The project hunts for planets that orbit two stars (circumbinary planets, the "Tatooine" kind) in public data from NASA's TESS space telescope.

The book is the public record of the project and also my textbook. An AI (Claude) writes it as a diary addressed to me, in second person ("you"), in plain English. It teaches me what each step means and admits what we do not know. Every claim carries an honest label (VERIFIED, LIKELY, UNCERTAIN, NOT TESTED). Professional astronomers may also read it, so it must look serious and trustworthy, never gimmicky.

What is in it: 15 topic chapters, a 7-level learning track, dated field notes (the diary), a glossary, a table of claims and their status, a candidates page, interactive demonstrations with light-curve plots, a practice mode where I learn to spot faint dips in noisy brightness curves (with short feedback lines after each answer), and a read-aloud feature. The home page is a star map of the constellation Cygnus.

The tone of the writing is calm, warm but exact: a teacher who is honest about uncertainty.

## 2. How it is built

- A static website: MkDocs with the Material theme, hosted on GitHub Pages. Plain CSS and JavaScript, no framework.
- It works offline (a service worker caches everything), so fonts must be self-hosted. No Google Fonts or other outside requests on the live site.
- Fonts must be free, with a licence that allows self-hosting and redistribution (SIL Open Font License or similar). Variable fonts in woff2 are preferred. Please give the licence and the download page for each suggestion.
- Keep it light. I would like the whole font set to stay near or under about 200 KB of woff2 in total, but tell me if quality needs more.
- The book is in English only.

## 3. Who reads it, and how

- Me, mainly on an iPhone (375 px wide, 16 px side margins), in short sessions, very often at night in a dark room. At 17 px only about 35 to 42 characters fit on a line, so a wide font makes lines even shorter. I also read on a PC (body 18 px).
- The dark theme is the default; light is on request.
  - Dark: background #0c1018, text #f2f4f9, secondary text #c3c9d6, one amber accent #eebf6a.
  - Light: background #faf9f6, text #10141b, accent #6f4608.
  - All text must keep a contrast ratio of at least 7:1.
- The mood I want: a scientific research notebook crossed with a mission control room. Calm and professional, one accent colour, nothing glowing.
- Not wanted: decorative or handwritten fonts, fake aged paper, sci-fi display fonts, neon, gimmicks.

## 4. The current typography (what I have now and do not like)

- Body, headings and interface: Inter (variable, upright and italic). Body is 17 px on phone and 18 px on PC, line height 1.7, OpenType features cv11 and ss03 on. Headings are Inter 600 with slightly negative letter spacing.
- Labels, data and the page nameplate: IBM Plex Mono 400 and 500, small, uppercase, letter-spaced. It is used for the line under each title that reads like an instrument label, the tab labels, table headers and the numbers inside plots.
- Until 23 October 2026 the body was Source Serif 4. I switched to Inter on 23 October and I am not satisfied with it either. I do not know exactly why. Please say what in Inter, at body length, in dark mode on a phone, could make a book feel cold, generic or like software documentation, but treat that as your hypothesis, not my diagnosis.
- A designer's draft brief (not decided) proposes one open-licence serif for titles and quotes, possibly for the body too, plus a sans for the interface, with at most two families. Its proposed sizes (phone, then PC): cover title 36 to 42 and 52 to 64 px; chapter title 28 to 32 and 36 to 44; section heading 21 to 24 and 24 to 30; body 17 to 19 and 18 to 20 at line height 1.65; small caps labels 11 to 13; captions 13 to 14; tables 14 to 16. You may disagree with any of it.

## 5. What the text contains (the font has to handle it)

- Long prose in second person, with short headings, quotes, lists, tables, small notes and call-outs, and buttons.
- Numbers everywhere. Table columns need tabular (equal width) figures, for example: TIC 123456789, period 5.2 d, strength 7.4 σ, depth 0.31 %.
- Science and maths characters: Greek letters (σ μ λ Δ θ), ± × ≈ ≥ ≤ → ° ² ³, a true minus sign (U+2212), subscripts, and the astronomy symbols ⊕ (Earth) and ☉ (Sun), which many fonts lack. Tell me which of your suggestions contain these glyphs and what fallback to use for the rest. Author names with accents also appear.
- Italic matters (paper titles, terms being defined). A true italic is preferred over a slanted roman.
- Tiny text: 12 px uppercase labels and 13 px labels inside plots.
- A sample of the voice (illustrative, not a real result): "Ahmed, the star dipped by a third of one percent for six hours and then came back. That is the size a planet about six Earths wide would make. It is also the size of a great many ordinary mistakes, so today we call it a lead, not a planet."
- A sample label: "VERIFIED / SECTOR 14 / 10 MIN BINS / STRENGTH 7.2 σ".

## 6. What I want from you

1. **Diagnosis.** Why Inter, and briefly Source Serif 4, may feel wrong for this book, and what qualities the type must have here (warmth, authority, small-size legibility, dark mode).
2. **Top 3 complete pairings, ranked.** For each: the family for titles, body, interface and data; weights and styles; licence and download page; approximate woff2 size; why it suits this book; its weaknesses. Include at least one all-sans option, one serif-body option, and one single-superfamily option (serif, sans and mono from one family) if a good one exists. Say whether IBM Plex Mono should stay, and why.
3. **Serif body on an OLED iPhone at night.** What to watch for (glare around bright text on dark, weight, size), whether a slightly heavier weight or a slightly softer text colour helps while keeping 7:1, and whether to offer a reader switch "Reading font: serif or sans".
4. **For your top pick:** a CSS starting point (@font-face rules, font stacks with fallbacks, sizes, line heights and letter spacing for body, headings, labels and tables), and the OpenType features worth turning on (tabular figures, proper minus, small caps, lining or oldstyle figures in prose).
5. **A five-minute way** for me to compare your candidates on my own phone.
6. **A short list of fonts that look attractive but would be wrong** for this book, and why.

## 7. Rules for your answer

- You cannot see my site or my screen, so say plainly what you could not verify. Label each claim VERIFIED (you checked the font's own page or specimen), LIKELY or UNCERTAIN.
- Never invent a licence, a file size or a glyph coverage claim. If unsure, say so and tell me the page where I can check.
- Plain English, readable on a phone, about 1,200 words. Do not use en or em dashes.
- No paid fonts and nothing that needs a subscription.
