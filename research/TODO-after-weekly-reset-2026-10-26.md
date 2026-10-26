# To-do after the weekly reset (written 26 Oct 2026; reset is about 01:00 Tuesday 27 Oct Kuwait)

**Update 26 Oct, later:** Ahmed has emailed the astronomer (done, item 14). No reply yet, and the full 549-star search no longer waits for one. The settings are frozen and hashed before the run instead (item 18e); if a reply arrives later, it goes through Compass first and any change becomes a new frozen version, so the first run stays valid as version 1. New: item 10a (fonts).

**Rule: nothing here starts until Ahmed says so.** "continue this" resumes the visual Artifact (see `D:\ss-artifact-work\RESUME-HERE.md`). Check `get_usage` first. Point estimates are weekly-limit percent, ranges, about plus or minus 50 percent. Basis: this session measured about 3 points for the whole feedback engine (build, tests, two publishes), about 0.5 to 1 for a Compass review, about 1 point for reading and preparing the Artifact without writing it, about 12 points for one full 5-hour window of heavy parallel work (usage log). A fresh session is cheaper per step than this very long one.

## A. Safety: copy to D (copy only, not a move; it may be outdated)
1. One-click backup script on D (robocopy, no deletions of old copies, skips node_modules and caches) for: `C:\CLaudeCode` (client work), `C:\Users\hanzl\.claude` (my memory of Ahmed, settings, transcripts), V8 (wherever `V8-LOCATION.txt` points), Al Mundhir Voucher Books, templates, plus Second Sun's untracked bits. 0.5 to 1 point.
2. Laptop guide: what to install (Claude Code, Python, Node, Git), requirements files for the two Python environments that have none, how to point Claude at the copy (memory is filed under the folder path; copy it to the new key). 0.3 to 0.5.
3. Push or commit the exposed client repos (almundhir-website 1 unpushed, nexo-website 2 uncommitted, project-morgue 4 uncommitted), only after Ahmed's OK. 0.1.
4. D has no second copy of itself: a small encrypted cloud copy of the critical set (memory, secrets, private leads, notes). Ahmed picks the service.
5. Ahmed: restrict the Firebase web key to the site address; consider BitLocker on D and a small UPS.

## B. Eyes mode fixes (Ahmed asked; plan first, then build)
6. After every practice or test round, say plainly at the top "You got N of 30 (or 50) right" (and the Dip, No dip, Odd, Not sure split), on the finish screen, so he never has to open My results. Optionally a running "right so far". Tests plus browser check. 0.3 to 0.5.
7. PC layout of Eyes: ask for a PC screenshot first (one guess maximum), then make the curve a smaller, wider (horizontal) shape, with answer buttons, the feedback and Next visible in one screen without scrolling (side by side on a wide screen), keyboard Enter for Next kept. 1 to 1.5.
8. Whole book on PC: too much empty space at the sides. Fix it as part of the redesign (item 10), or a small interim CSS widening if Ahmed insists. Interim 1.5 to 3.

## C. The book
9. **Learning spine (new).** Today three orders disagree: topic order (1 to 15), learning-track order (L0 uses Ch 1 to 2, L3 uses Ch 7 to 8, L4 uses Ch 4 to 6, L5 to L6 use Ch 9 to 12) and journey order (starts at Ch 4). Proposal: one spine, the levels drive the order; each level shows its chapters, labs, questions and the field notes that taught it; topic list stays as browse; the Journey page becomes "how the project unfolded"; every field note lists chapters touched and every chapter lists the notes that taught it. Compass review first, then build. 3 to 6.
10. **Visual identity Artifact** (Phase 1 only, then stop). Add to the brief: the one-spine structure, and a wide PC layout that uses the sides (a horizontal reading layout with a contents rail and a margin column). 4 to 7.
10a. **Fonts (Ahmed does not like the current Inter body).** He is collecting another AI's opinion on fonts that suit the book (prompt written 26 Oct). When he shares it: Compass pass first (licence must allow self-hosting, works offline, readable at 375 px, 7:1 contrast unaffected, no layout shift), then fold the chosen pair into the visual identity Artifact (item 10) so the font is decided once, with a visible "reading font" switch only if he wants it. Review 0.5 to 1; the change itself is part of item 10 or the redesign.
11. After Ahmed approves the Artifact: the real implementation is a separate plan and a separate go.

## D. Ready for an expert reader
12. A "Prior work and how we differ" page (Thornton, Montet and colleagues at UNSW on eclipse-timing precession, 27 candidates; Davies and colleagues at Warwick on mono-cbp, one candidate; Oddo and others), plus a one-page "for astronomers" start page. 1 to 1.5.
13. Visitor guard: only Ahmed's devices count in his results and only they upload (visitors can play without any upload). 0.5 to 0.8.
14. DONE (26 Oct): Ahmed emailed the astronomer himself; no reply yet. Nothing more to draft. If a reply comes, share it and I run Compass on it before anything changes.

## E. Compass and housekeeping
15. Compass upgrade: review Claude AI's report, then fold the useful parts into `COMPASS.md`. 1 to 1.5.
16. Ahmed's saved prompts: a Compass review each, 0.5 to 1 each.
17. Field note for 25 to 26 Oct (same-day rule). 0.3.

## F. Science (needs Ahmed's go, and the prerequisites below)
18. **Before the full 549-star search (Stage 3):** (a) put the catalogue-phase eclipse check (C5) into the pipeline; (b) mark the 237 QLP-only stars as "no second product"; (c) use real-curve false-alarm rates for list sizing; (d) cheap eclipse fold-check of the 136 stars with no measured shape; (e) freeze settings and hash them now (no longer waiting for an expert reply); (f) emit panel data for the review page. 2 to 3.
19. Run Stage 3 on all 5,064 usable star-sectors (machine about 2.5 to 3 hours, estimated from Stage 2: 474 groups in 15 minutes on 8 cores; the light curves are already on D) and babysit it. 0.5 to 1.
20. Aggregates, first-tier list (about 60 events expected), contact sheets. 1 to 2.
21. Vetting the first tier: automatic checks, a locked real-candidate page for the blind human key, pixel and neighbour tools if needed. 5 to 9.
22. Publication path (ExoFOP accepts candidates only after publication): decide only when a candidate survives both keys; then 0.5 to 1.

## G. Points, honest totals
Items 1 to 5: 1 to 2. Items 6 to 8: 1.8 to 3 (plus 1.5 to 3 if the interim widening is done). Item 9: 3 to 6. Item 10: 4 to 7. Items 12 and 13: 1.5 to 2.3 (item 14 is done). Item 10a: 0.5 to 1. Items 15 to 17: 1.8 to 3.5 plus prompts. Items 18 to 22: 9 to 16. **Everything except the science: about 14 to 26 points. With the science: about 24 to 42**, a quarter to under half of one weekly allowance, but order matters.
Suggested order: A, then B (quick wins), then D, then C9 and C10 (decided together), then E, then F as soon as Ahmed says start (the expert reply is no longer a gate; his hard-test pass gates the vetting of the first tier, not the run itself).

## H. Timing advice for the three science decisions
- **Full search (Ahmed decided 26 Oct: proceed without waiting for the astronomer's reply):** compute is cheap, so the only gates left are the Stage 3 pre-fixes (item 18, including freezing and hashing the rules) and Ahmed's "start". The human key (hard test line passed) is needed to vet the first tier, not to run the search, so the run can come first and the review follows. Realistic start: within a few days of the reset, about two work sessions after Ahmed says "start". The hunt stays on hold until he says it.
- **136 stars with no shape:** decide before the freeze, by data not by guess: fold-check all 136 first; those with a clear eclipse join the main run, the rest form a separate "shape unknown" batch searched last.
- **ExoFOP and publication:** no decision needed until a candidate survives both keys. The rule already says publish first. Only pick a venue and the AI-use wording then.

## I. Ahmed's own actions
Three official starter rounds on a date after 24 Oct; hard practice; check the new feedback lines on the iPhone (reload the book once); Firebase key restriction; choose the cloud copy; tell me which group the astronomer you emailed belongs to (UNSW or Warwick) so the prior-work page names the right one; share any reply; share the other AI's font advice.
