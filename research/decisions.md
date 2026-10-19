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
