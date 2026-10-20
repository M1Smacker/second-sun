# Decision log

Dated decisions. Nothing here gets re-argued unless new evidence appears; if it does, add a new dated entry rather than editing the old one.

## 2026-10-19: Project founding (25 question rounds)
All founding decisions are recorded in `RESEARCH-PLAN.md`, section 2 (superseded answers marked there).

## 2026-10-19: Plan approved; use all of this week's leftover usage
Ahmed approved the research plan and asked for wave 1 as three parallel sessions tonight, with limit math so the leftover weekly usage (47%, resetting ~01:00 Kuwait 2026-10-20) is used and not wasted.

## 2026-10-19: Wave 1 merged; first-campaign recommendation (awaiting Ahmed)
Claude recommends **G1 (Kepler-field binaries re-observed by TESS: "switched-on" planets)** as the first main-quest campaign, with G4 (secondary-star / multi-dip / partial-dip search) built in and G7 (vetting TTT's unchecked binaries → VSX side wins) as the side stream. It depends on wave 2/3 measuring TESS precision on Kepler-field stars. Full reasoning: `research/wave-1-gap-check/GAP-REPORT.md` section 3. **Status: proposed, not yet decided by Ahmed.**

## 2026-10-19: Tonight's remaining waves run on scheduled queue runners
The app refuses to start sessions from an automated turn, so waves 2, 4, 3, 5, 9, 6, 7 run on one-off scheduled tasks (`second-sun-runner-1..5`) that claim waves from `research/WAVE-QUEUE.md`. Authorised by Ahmed's instruction to use all of this week's leftover usage and his round-16 approval of scheduled sessions spending leftover usage near the reset. Hard stop 21:50 UTC.

## 2026-10-19 ~17:05 UTC: G1 approved as the first campaign
Ahmed (from his phone): "your searches are great. Follow it." The first main-quest campaign is **G1: Kepler-field eclipsing binaries re-observed by TESS ("switched-on" circumbinary planets)**, with G4 built into the pipeline and G7 as the side-wins stream. It still depends on wave 2/3 confirming TESS precision on Kepler-field stars; if precision fails, fall back to G2 (bright end) per GAP-REPORT section 3.

## 2026-10-19 ~17:05 UTC: Scheduled runners failed; research continues in the main session
Runners 1-2 fired on time but froze ~10 s in, on a permission prompt (scheduled tasks start in default mode). Stopped them; runners 3-5 disabled. The app also refuses start_session on turns that come from Ahmed's phone. Waves now run inline in the main session (Auto mode).

## 2026-10-19 18:48 UTC: Delete big cutouts, keep what we extract from them
Ahmed: "yes delete cutouts". This changes the "keep raw data" rule for **TESScut cutouts only**. After we extract a light curve from a cutout, we keep the light curve plus the settings used (sector, size, aperture), then delete the cutout. Any cutout can be downloaded again from MAST. All other raw data (SPOC/QLP/TESS-SPOC light curves, catalogues) is still kept. The two wave-2 test cutouts (153 MB) were deleted the same night.

## 2026-10-19 20:59 UTC: The book looks professional, not gamey
Ahmed: "make sure the bible still look professional and cleaner. dont make it a full gamey look. It should explain everything very cleanly and it should be personalized to me." This replaces "full gamification". The book is a clean, calm reference with a restrained night-sky palette and one accent colour. Progress tracking stays but quiet (levels, a milestones page, a sky-coverage map, a cool-finds gallery, plain candidate cards); no XP counters, level-up banners, badges or glowing effects on content pages. Every page: plain words first, then detail, glossary links for terms. Written to Ahmed, built on his own data, targets, goals, pace and level. Sent to the burn-3 book session at 20:59 UTC.

## 2026-10-19 21:16 UTC: Site blueprint adopted (building waits)
Ahmed: "Yes, adopt the blueprint with your 3 additions as the plan for the book. Don't start building yet." The blueprint (written by a website session from Ahmed's studio, read and checked by Claude) is now research/SITE-BLUEPRINT.md. Key points: stay on Material 9.7.7 with all custom logic in plain Python scripts (engine replaceable; review Feb 2027 or at Zensical 1.0, Starlight as fallback); claims as IDs resolved at build; one amber accent; no XP/ranks/badges; offline via a 3-cache service worker under 25 MB; noindex via meta tag (robots.txt can't work on a project site); public repo means pushed content is visible from day one. Additions: one claim-ID scheme; Side wins + Credit and AI use pages; a switch to keep candidate data local until both keys pass. Note: Claude asked for approval before listing the 3 additions (the question box ended the turn); they were listed right after, with a request to object.

## 2026-10-20 00:55 UTC: PENDING (Ahmed): ExoFOP is publish-first
Found by burn 3, re-checked by Claude at the source (exofop.ipac.caltech.edu/tess/help.php and news.php, fetched 2026-10-20 00:55 UTC): community planet candidates must now be **published in a peer-reviewed journal before upload**; an RNAAS note is allowed only if the detection and vetting method was previously published in a peer-reviewed journal and is cited. Uploads were paused 2026-03-31 and reopened 2026-08-19 under these rules. This breaks the ladder "clean CTOIs, then paper": the order becomes **write-up first, then ExoFOP upload, then TOI**, and the scoop switch should flip at write-up submission. Decision needed from Ahmed before the first candidate; no candidate exists yet.

## 2026-10-20 11:40 UTC: Bible Overhaul, and the same-day lesson rule
Ahmed: "Do it. For today you need to only work on the Bible... I gotta catch up on the learning... I would also like lessons on how to find stars etc myself... Name this an overhaul of the Bible... whatever changes we make after a day of work, instantly gets saved properly in teaching format to the Bible... Plan only task for now." Decided: (1) the star hunt is paused while the book catches up; "core first" is set aside for this overhaul only. (2) Plan saved in research/BIBLE-OVERHAUL-PLAN.md (7 new chapters, 10 hands-on labs, Parts structure, 6 build batches); nothing built yet. (3) **Same-day lesson rule:** every work block that changes code, data, results, decisions or mistakes writes a Field Note in teaching format into the book in that same block, before it is called finished or before a usage pause; wrap-ups report how many commits the book is behind. Status: plan awaiting Ahmed's go on the Parts renumbering, labs on .venv, no helpers.

## 2026-10-20: PENDING (Ahmed): the 136 G1 rows with unknown morphology
Found during the Bible Overhaul (Lab 9): `morph < 0.5` admits morph = -1 ("not measured" in the Villanova catalogue), 136 of 552 rows. Options: (a) drop them; (b) keep them but measure their eclipses ourselves from TESS before searching (the automatic eclipse finder already does this; a star with no eclipses found gets flagged); (c) keep as is. Claude's default when the hunt resumes: (b). Nothing changed yet; the hunt is paused.
