# Research questions after the sealed search (30 Oct 2026): WAITING FOR AHMED'S APPROVAL

Nothing in this file has been researched yet. Each question follows `research/RESEARCH-BLUEPRINT.md`: it names the decision it feeds, what our own data already says (with the file), what would change the plan, and how the hour would be spent (own data first, then primary sources, exact sentences, labels, filed). On approval, each approved question gets at least one hour of focused work and a section in `research/stage3/post-sealed-literature-<date>.md`; every finding becomes a plan change, a task in `research/stage3/BUILD-QUEUE.md` (T31 to T60) or, if it is a bug, an item in `research/stage3/FIX-QUEUE.md`. Evidence behind every question: `research/stage3/DEEP-ANALYSIS-AFTER-SEALED-2026-10-30.md`.

**Cost guess (labelled a guess):** past research rounds cost 0.5 to 1.5 weekly points for 10 to 20 minutes; an hour per question is about 1.5 to 3 points in a fresh context. Priority 1 (six questions) is about 9 to 18 points; priority 2 (five) about 8 to 14; priority 3 (three) about 3 to 7. The weekly figure was 72% at the last reading. Ahmed's cap is 75% with a stop line at 74%, so approving priority 1 needs a new cap from him.

## Priority 1: they decide how we word the win and what Vesper 0.9 must change

**Q1. Where was TOI-1338 b really, in the later sectors?**
- Decision fed: task T44 (a labelled post-hoc S6 line) and whether Vesper's sensitivity to a real circumbinary planet is nearer 1 of 7 or 5 of 7.
- Own data: real events 0.6 to 1.4 days after the Kostov 2020 prediction in sectors 65, 89, 93, 96, 98; several at tier 1A (`post-sealed-analysis/toi1338_why.out`). Upside-down events also sit within a day of some epochs.
- Would change the plan: if a later ephemeris puts the transits where the events are, S6 gets a second line and the sensitivity statement changes.
- Hour: (1) own data: expected offset growth from the period uncertainty alone, and how many upside-down events sit as close by chance; (2) primary sources: later papers or tables on TOI-1338 timing and period (to be located and opened, none assumed), the NASA Exoplanet Archive row; (3) refit the epochs with the newer ephemeris and re-score under the same window rule, labelled post hoc.
- Starting label: UNCERTAIN.

**Q2. What does a null of this power actually rule out?**
- Decision fed: the sentence we publish about the result, how many stars or sectors the next search needs, whether to go multi-sector (older fix item 12 and task T37).
- Own data: completeness by K and box (`benchmark-g2-sealed.txt` S4), the cluster-robust ceiling (excess above about 8 kept dips excluded), periods in `data/xmatch/cbp.csv` (95, 187, 229, 303 days) against a 27 day sector.
- Would change the plan: if one sector rarely catches a transit of a long-period planet, the search design (single sector) caps what any null can say, and linking sectors becomes the priority.
- Hour: (1) own data: convert K to a planet radius per star brightness class and box (the open item 12 of the older queue), count transits per sector for a range of periods; (2) primary sources: circumbinary occurrence and period distribution from the Kepler circumbinary papers and the transit-probability formulas (to be opened, not recalled); (3) a one-page "what the null rules out" table with intervals.
- Starting label: NOT TESTED.

**Q3. Are the short deep upside-down survivors flares, and does a shape test separate them?**
- Decision fed: task T33 (flare-shape check) and whether the control needs a flare-aware variant.
- Own data: 44 of 59 upside-down tier-1 events are 3 h boxes, 23 of 59 deeper than 1%, one at 1.0e7 ppm; real tier 1 is 16 of 26 at 3 h (`analyse4.out`). The raw ratio rises with SNR (1.09 to 1.78).
- Would change the plan: if flare shapes explain them, a shape flag could cut false alarms without touching real transit-like boxes; if not, the control has another defect.
- Hour: (1) own data: rise and decay measurements on the 59 and 26 events and on a few hundred random events; (2) primary sources: flare profile templates and TESS flare catalogues (to be located); (3) a candidate flag and its price on planted dips, report-only.
- Starting label: LIKELY (not tested).

**Q4. What is the right unit and the right estimate for the control?**
- Decision fed: tasks T38 and T39, the amendment that rewrites S1 before the next sealed-style run.
- Own data: events cluster on stars (development 78 events on 21 stars; sealed one star holds 56 raw real events); ratio 1.41 (sample) against 1.18 (full run); bootstrap results in `analyse4.out`.
- Would change the plan: the star becomes the counting unit; the ratio gets a per-bar value with an interval.
- Hour: (1) own data: bootstrap over stars at every bar and for the ratio itself, power of the star-level test at our size; (2) primary sources: how transit-search papers state false-alarm rates when events cluster (to be located); (3) the draft amendment text, not yet applied.
- Starting label: LIKELY.

**Q5. What does the step check measure, and why does it fire on 82% to 90% of all raw events?**
- Decision fed: task T34, the biggest completeness cost.
- Own data: step is on 51% of the strong planted dips that were lost; fires on 81.6% of real and 90.3% of upside-down raw events (`analyse2.out`); the C-study found a looser threshold just trades 1 for 1.
- Would change the plan: a better baseline estimate (not a looser threshold) could recover planted dips at the same false-alarm rate.
- Hour: (1) own data: distribution of the before and after lift values for planted dips, raw events and survivors, split by box length (a long box against a 2 day detrend window is a known issue, item 11 of the older queue); (2) primary sources: the detrending tool's documentation on window length and how published searches test baselines; (3) a candidate replacement and a paired comparison on the same planted dips.
- Starting label: UNCERTAIN.

**Q6. How should single events in different sectors be linked for long-period planets?**
- Decision fed: whether Vesper 0.9 gets a cross-sector step, and what to do with 6 leads that have several sectors.
- Own data: the first pair search found 0 real pairs (older queue item 10); in the sealed run 2 of 6 leads have kept events in other sectors; period coverage as in Q2.
- Would change the plan: a timing-variation-aware linker could turn single events into candidates, or show there is nothing to link.
- Hour: (1) own data: per-star kept events across sectors for all 895 stars (needs task T43 for the development slice); (2) primary sources: methods for circumbinary and monotransit linking (the blueprint already names the Martin and Fabrycky variable-window work and the mono-cbp paper); (3) a design sketch with the exact rule fixed before running.
- Starting label: UNCERTAIN.

## Priority 2: they sharpen the numbers

**Q7. Which known planets can we test on, besides TOI-1338 b?** Decision: a larger S6. Own data: `cbp.csv` has 53 rows, most not transiting (imaging, timing, microlensing); Kepler-1660 already serves as a control. Hour: list entries that transit and have TESS light curves, check against our star lists and the sealed rule, source tables from the archive. Label: NOT TESTED.

**Q8. Which light curves hold absurd values, and how many are there in all 895 stars?** Decision: tasks T31, T32 and a data-quality count. Own data: SNR 3.5e26 (TIC 392536805, sector 76, QLP) and depth 1.0e7 ppm. Hour: scan every group file for depth above 100% and tiny noise, trace to product and star-sector, read the product notes on zero or negative flux. Label: UNCERTAIN.

**Q9. Why do the two slices differ so much in the raw real against upside-down ratio (0.98 against 1.41)?** Decision: whether the next split is stratified, and how to read S1. Own data: top ten stars hold 41% of raw real events in development and 22% in sealed. Hour: per-star table of the ratio, check stellar activity indicators in our own tables, then sources on flare rates of close binaries. Label: UNCERTAIN.

**Q10. How different is the QLP-only half of the sample?** Decision: whether tier 1B (no second light curve) is reported or led separately. Own data: `rows_sealed.pkl` has the best product per row. Hour: completeness and false-alarm rate for QLP-only against SPOC stars, the share of stars that can never reach 1A. Label: NOT TESTED.

**Q11. Is the 3 h box worth having for circumbinary planets?** Decision: task T35. Own data: 62% of real and 75% of upside-down tier-1 events are 3 h. Hour: planted recovery by duration with and without it, published circumbinary transit durations. Label: UNCERTAIN.

## Priority 3: they shape the leads and the road ahead

**Q12. Which checks turn a lead into a candidate, and which can we do from our files?** Decision: tasks T47 and T49 and the "2 or 3 more checks" list on the cards. Own data: the light-curve headers (look for crowding and flux-fraction keys), the centroid columns. Hour: read the TESS data validation documentation and the light-curve tool documentation, test the keys on the six sealed leads, draft the checklist. Label: NOT TESTED.

**Q13. How accurate are trained humans on TESS dips, and are Ahmed's Eyes pass lines sensible?** Decision: keep or change the pass line (clear-hit 0.85, false alarm 0.10) and the real-candidate Eyes page design. Hour: volunteer-vetting papers (to be located), compare with our own Eyes constants in `eyes-core.js`. Label: UNCERTAIN.

**Q14. How does an amateur report a candidate, and what leaves the public book at that moment?** Decision: the "go professional" playbook Ahmed described (the book becomes partly private). Own data: what the data branch and book currently expose (names, TIC numbers, pictures). Hour: the ExoFOP and follow-up submission guidelines and preprint options (to be opened), the git-history problem (removing star data from a public repository does not remove it from history, so the data branch is kept separate and can be recreated). Label: NOT TESTED.

## How I propose to run it
- Order: Q4, Q3, Q1, Q5, Q2, Q6 for priority 1 (Q4 first because it fixes how every later number is judged). Each in its own fresh context, one hour each, a filed literature section and a build-queue or fix-queue update per question.
- Machine work (the 895-star census, task T43) can run alongside at no usage cost.
- Nothing here touches the frozen Vesper 0.8.0 or any preregistered number.
