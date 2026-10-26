# To-do list in phases A to H (rewritten 27 Oct 2026, after the weekly reset)

**Rule: nothing here starts until Ahmed says so.** "continue this" resumes the visual Artifact (see `D:\ss-artifact-work\RESUME-HERE.md`; check usage first). Points are weekly-limit percent, ranges, about plus or minus 50 percent.

**Basis for the estimates:** the whole feedback engine cost about 3 points (build, tests, two publishes); a Compass review 0.5 to 1; reading and preparing the Artifact without writing it about 1; one full 5-hour window of heavy work about 12; a fresh session is cheaper per step than a very long one.

**Status 27 Oct:** Ahmed emailed the astronomer (26 Oct), no reply, and the full 549-star search no longer waits for one (rules are frozen and hashed before the run; a later reply goes through Compass and becomes a new version). The font report was reviewed by Compass (`research/compass-reviews/2026-10-27-font-advice-report.md`): approve with addendum; main finding: the fonts served today have no Greek or math symbols, so σ and ≈ come from the phone's fallback font. Weekly usage 0 percent at the reset.

"was N" means the item number in the earlier version of this file.

## Phase A. Safety: copy to D (copy only, not a move; may be outdated)
- A1. One-click backup script on D (robocopy, never deletes old copies, skips node_modules and caches): client work `C:\CLaudeCode`, `C:\Users\hanzl\.claude` (memory of Ahmed, settings, transcripts), V8 (where `V8-LOCATION.txt` points), Al Mundhir Voucher Books, templates, Second Sun's untracked bits. Me. 0.5 to 1. (was 1)
- A2. Laptop guide: what to install (Claude Code, Python, Node, Git), requirements files for the two Python environments that have none, how to point Claude at the copy (memory is filed under the folder path; copy it to the new key). Me. 0.3 to 0.5. (was 2)
- A3. Push or commit the exposed client repos (almundhir-website 1 unpushed, nexo-website 2 uncommitted, project-morgue 4 uncommitted), only after Ahmed's OK. Me. 0.1. (was 3)
- A4. Ahmed: choose a small encrypted cloud copy of the critical set (memory, secrets, private leads, notes); restrict the Firebase web key to the site address; consider BitLocker on D and a small UPS. (was 4, 5)

**Phase A: 1 to 2 points.**

## Phase B. Eyes fixes (plan first, then build)
- B1. After every practice or test round, say plainly at the top of the finish screen "You got N of 30 (or 50) right", with the Dip, No dip, Odd, Not sure split, so Ahmed never has to open My results. Tests plus browser check. Me. 0.3 to 0.5. (was 6)
- B2. PC layout of Eyes: ask for a PC screenshot first (one guess maximum), then a smaller, wider (horizontal) curve with the answer buttons, the feedback and Next in one screen without scrolling (side by side on a wide screen); keyboard Enter for Next kept. Me. 1 to 1.5. (was 7)

**Phase B: 1.3 to 2 points.** The wide layout for the whole book is not here; it is part of Phase F.

## Phase C. Fonts
- C1. **Font test page** (added 27 Oct): a private Artifact, outside the book, nothing downloaded, nothing in the repo changes. Ahmed's real paragraph, a number table, "σ" labels, dark and light, 17 px / line height 1.7, a switcher: Inter and Source Serif 4 (controls), Literata, Plex Sans, Plex Serif, Atkinson. Me. 0.5 to 1. (new)
- C2. Ahmed reads it on the iPhone at night and picks; the pick feeds F2 and F4. If Greek or math symbols are missing in the pick, add a tiny Greek and math subset (a few KB, not yet tested). (was 10a)
- Addendum from the Compass review to honour in the build: remove Inter's `"cv11", "ss03"` setting, lining figures in prose and tabular figures in tables, keep Literata's optical-size axis, measure real file sizes against today's 130 KB, test offline caching.

**Phase C: 0.5 to 1 point.** (The Compass review of the font report is already done.)

## Phase D. Ready for an expert reader
- D1. A "Prior work and how we differ" page (Thornton, Montet and colleagues at UNSW on eclipse-timing precession, 27 candidates; Davies and colleagues at Warwick on mono-cbp, one candidate; Oddo and others), plus a one-page "for astronomers" start page. Me. 1 to 1.5. (was 12)
- D2. Visitor guard: only Ahmed's devices count in his results and only they upload (visitors can play without any upload). Me. 0.5 to 0.8. (was 13)
- D3. DONE 26 Oct: Ahmed emailed the astronomer himself. If a reply comes, share it; Compass runs on it before anything changes. (was 14)

**Phase D: 1.5 to 2.3 points.**

## Phase E. The 549-star search (needs Ahmed's "start"; no waiting for the astronomer)
- E1. Pre-fixes before Stage 3: (a) put the catalogue-phase eclipse check (C5) into the pipeline; (b) mark the 237 QLP-only stars as "no second product"; (c) use real-curve false-alarm rates for list sizing; (d) cheap eclipse fold-check of the 136 stars with no measured shape (clear eclipse joins the main run, the rest become a "shape unknown" batch searched last); (e) freeze the settings and hash them; (f) emit panel data for the review page. Me. 2 to 3. (was 18)
- E2. Run Stage 3 on all 5,064 usable star-sectors (machine about 2.5 to 3 hours, estimated from Stage 2: 474 groups in 15 minutes on 8 cores; the light curves are already on D) and babysit it. Me. 0.5 to 1. (was 19)
- E3. Aggregates, first-tier list (about 60 events expected, factor of 2 uncertain), contact sheets. Me. 1 to 2. (was 20)

**Phase E: 3.5 to 6 points.** Realistic start: within a few days of Ahmed's "start" (about two work sessions to be ready). The run can come before the vetting key is ready.

## Phase F. The book itself: spine, look, layout
- F1. **Learning spine.** Today three orders disagree: topic order (1 to 15), learning-track order (L0 uses Ch 1 to 2, L3 uses Ch 7 to 8, L4 uses Ch 4 to 6, L5 to L6 use Ch 9 to 12) and journey order (starts at Ch 4). Proposal: one spine, the levels drive the order; each level shows its chapters, labs, questions and the field notes that taught it; the topic list stays as browse; the Journey page becomes "how the project unfolded"; every field note lists the chapters it touched and every chapter lists the notes that taught it. Compass review first, then build. Me. 3 to 6. (was 9)
- F2. **Visual identity Artifact** (Phase 1 only, then stop). The brief gets two additions: the one-spine structure, and a wide PC layout that uses the sides (a horizontal reading layout with a contents rail and a margin column); it also uses the font Ahmed picks in C2. Me. 4 to 7. (was 10)
- F3. Ahmed approves, changes or rejects the Artifact. (was 11)
- F4. **The real redesign on the live book** (Phase 2): its own plan and its own go. Includes the new look, the fonts, the wide PC layout for the whole book (was 8), the spine layout, tests and the offline gate. Me. 6 to 12, a rough guess made before the design exists; **the earlier totals left this out.**
- Optional: if F4 is weeks away, a small interim CSS widening of the book on PC, 1.5 to 3.

**Phase F: 13 to 25 points.**

## Phase G. Vetting and publication (only if the search gives something)
- G1. Vet the first tier: automatic checks, a locked real-candidate page for the blind human key, pixel and neighbour tools if needed. Needs Ahmed's hard-test pass. Me. 5 to 9. (was 21)
- G2. Publication path (ExoFOP accepts candidates only after publication): decide only when a candidate survives both keys; publish first, then pick the venue and the AI-use wording. Me. 0.5 to 1. (was 22)

**Phase G: 5.5 to 10 points.**

## Phase H. Compass and housekeeping (slot in whenever)
- H1. Compass upgrade: review Claude AI's report (Ahmed shares it later), then fold the useful parts into `COMPASS.md`. Me. 1 to 1.5. (was 15)
- H2. Ahmed's saved prompts: a Compass review each, 0.5 to 1 each. (was 16)
- H3. Field note for 25 to 27 Oct (same-day rule). Me. 0.3. (was 17)

**Phase H: 1.3 to 1.8 points, plus 0.5 to 1 per saved prompt.**

## Totals
A 1 to 2, B 1.3 to 2, C 0.5 to 1, D 1.5 to 2.3, E 3.5 to 6, F 13 to 25, G 5.5 to 10, H 1.3 to 1.8.
**Everything: about 28 to 50 points** (a quarter to a half of one weekly allowance). Without the science (E and G): about 19 to 34. The earlier total of 24 to 42 missed the real redesign (F4, 6 to 12) and the font page.

**Suggested order:** A, B, C, D, then E (the search runs on the machine while the book work goes on), then F, then G when the search gives a first tier, with H slotted in between. Fonts (C) come before the Artifact (F2) so the type is decided once. Rough pace: A to E about 8 to 14 points, F about 13 to 25, G 5.5 to 10.

## Timing advice for the three science decisions
- **Full search (Ahmed decided 26 Oct: proceed without waiting for the astronomer's reply):** compute is cheap, so the only gates left are the Stage 3 pre-fixes (E1, including freezing and hashing the rules) and Ahmed's "start". The human key (hard test line passed) is needed to vet the first tier, not to run the search. The hunt stays on hold until he says "start".
- **136 stars with no shape:** decided by data, in E1(d), before the freeze.
- **ExoFOP and publication:** no decision needed until a candidate survives both keys. The rule already says publish first.

## Ahmed's own actions
Three official starter rounds on a date after 24 Oct; hard practice; check the new feedback lines on the iPhone (reload the book once); Firebase key restriction; choose the cloud copy; tell me which group the astronomer you emailed belongs to (UNSW or Warwick) so the prior-work page names the right one; share any reply; read the font test page on the phone and pick; share Claude AI's Compass answer.
