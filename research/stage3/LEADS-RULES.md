# Leads: stage rules (written 30 Oct 2026, before any sealed result was read)

Ahmed asked (30 Oct 2026) for a section on the Search window page that shows plainly whether a run found anything and which dips deserve 2 or 3 more checks. These rules fix what the words mean before the sealed scorecard is opened, so they cannot be shaped by it. Any change after results are seen is written below as a dated amendment, never made silently.

## Stages (one event = one dip in one star-sector, both light products counted as the page already counts them)
1. **Events**: every dip at SNR 7 or more, both kinds.
2. **Kept**: tier 1A, 1L or 1B, so no Vesper safety check fired.
3. **Confirmed**: tier 1A, so the second light curve agrees at SNR 4 or more (a star with only one product cannot reach this stage).
4. **Lead**: Confirmed, kind real (not the upside-down control), and the star is not a known TOI host and not a known circumbinary planet host (`data/xmatch/toi.csv`, `cbp.csv`). A Confirmed real event on a known host is labelled KNOWN, not a lead. Two events of one star-sector within 0.5 days count as one lead (the higher SNR stays).
5. **Candidate**: only by two keys (Claude's analysis and Ahmed's own check, see Candidates page). The page never promotes anything to Candidate by itself.

## Checks listed on every lead card (fixed list, in this order)
1. Passed every Vesper safety check (automatic, true by stage 2).
2. Second light curve agrees (automatic, true by stage 3).
3. Not a known TOI or circumbinary host (automatic, true by stage 4).
4. Seen in another sector of the same star (automatic: counted, "single sector" if the star has no other sector in the run).
5. Looked at by eye by Ahmed (pending until he says so).
6. Pixel-level check, background and neighbouring stars (NOT BUILT; stays "not built" until a tool exists).
The card's "next check" is the first one that is pending.

## Control column
Every funnel stage shows real and upside-down side by side (pooled while the run is blind). The upside-down count is the number of false alarms to expect. If real Confirmed events do not outnumber upside-down Confirmed events, the verdict says the leads are as likely noise as dips.

## Verdict sentences (chosen by rule from the numbers, no free text)
- run not finished: "Not finished. No verdict yet."
- run blind (sealed, scorecard not yet filed): "Finished. Counts only until the scoring is filed."
- no leads: "Finished: no leads. Nothing survived every check, so this run adds to the null."
- N leads, real Confirmed above upside-down Confirmed: "Finished: N leads for 2 or 3 more checks."
- N leads, real Confirmed not above upside-down Confirmed: "Finished: N leads, but real dips do not outnumber the upside-down copies, so treat them as noise until a check says otherwise."

## What is public and when
- Counts, the funnel and the verdict are always public.
- Lead cards (TIC, sector, time, picture) are public on the book except while the run is blind. For `sealed_*` runs the exporter keeps the cards and the kind hidden until `research/stage3/benchmark-g2-sealed.txt` exists (the scorecard is filed).
- Ahmed's decision (30 Oct 2026): the book may show star details while nothing is serious. If a lead ever gets both keys and we go to professionals or NASA, the star data is removed from the book then. The details sit in `watch.json` on the data branch `watch-data`, separate from `main`, so that branch can be deleted and recreated to remove them from history.
- Lead cards are leads, never claims. The card wording never says planet.

## Amendments
**Amendment 1 (30 Oct 2026, written AFTER the sealed scorecard was read).** The first build counted the first-pass group files. On the sealed run it showed 129 real against 72 upside-down Confirmed and 53 leads, while the scorecard said NO EXCESS (26 real, 59 upside-down kept). The difference is the last checks (union, the c6 flag, the PDCSAP check) and counting only the best light curve of each star-sector. This was a counting error, not a change in what a lead is. Changes: (1) a finished run is counted from the scorecard's own events (stage3_report.load, best product, PDCSAP half), so the funnel reproduces the scorecard; (2) a lead is one per star, its strongest Confirmed event, with the number of Confirmed dips; (3) the page also shows the scored S1 verdict line when the scorecard exists. The definition of a lead (tier 1A, real, not a known host) is unchanged. While a run is still going the page shows running counts, labelled as such.

**Amendment 2: the follow-up protocol (APPROVED by Ahmed 14 Nov 2026 for the G1 preregistration, `G1-PREREGISTRATION.md`; frozen with it; written 14 Nov 2026, before any G1 lead exists; BUILD T125, from RS-007 and Rabtsevich's Zenodo 23175179 preregistration; it becomes binding only when Ahmed approves it inside the G1 preregistration, and is then frozen with it).**
What happens AFTER a lead exists, fixed now so it cannot be shaped by a lead we like.
1. **Who may start a follow-up.** Only a lead with both keys (Claude's analysis and Ahmed's own look). A lead stays private (`data\` only) until then; nothing below is public without Ahmed's yes.
2. **What the follow-up tests, written before it runs.** One file per lead, committed with its sha256 BEFORE the new data are read (or, for archival data, before the windows are looked at): the transit times allowed by every orbit family that fits the lead (a single circumbinary transit leaves the period open: list each family, as Kostov et al. 2021 Table 7 does for TIC 172900988, with its window width); the allowed depth range and the allowed duration range at each window (a circumbinary transit's length depends on the binary phase); the light curves and products; the processing (the frozen Petrova version that found the lead, nothing tuned); the threshold. Data sources in order: other sectors already observed (archival), sectors TESS will observe (checked on the official pointing pages, dated), and a TESS DDT request (below).
3. **Threshold and noise, measured in the same light.** The same windows placed at fake times in the same light curve (at least 1,000 placements, avoiding the predicted windows and the eclipse windows), on the real and on the upside-down arm; the threshold is the 99.9th percentile of the fake-window score. The expected false-detection rate is reported as measured, not the nominal 0.1%.
4. **Four outcomes, and only these.** RECOVERED: a dip above the threshold inside a predicted window, with depth and duration inside the allowed ranges (on the upside-down arm the same window must not score above the threshold). INCONSISTENT: a dip above the threshold in a window but outside the allowed depth or duration, or a dip only outside all windows: the lead as written is wrong; it is not evidence of no planet. EXCLUDED: the mean depth over the windows is below the threshold AND below the allowed range AND the sensitivity is at least 95% (the predicted transit, injected at the predicted times into this same raw light before every processing step, is recovered at least 95% of the time); every orbit family must be covered for the lead as a whole to be excluded, otherwise only the covered families are. INSUFFICIENT: everything else (windows not observed, gaps, sensitivity under 95%). INSUFFICIENT is never evidence against the lead.
5. **The first valid run defines the result.** The first run that writes its output file is the result, committed before any variant runs. Variants (other products, other detrending) are reported beside it, labelled as variants, and never replace it.
6. **Fixed result sentences.** RECOVERED: "The follow-up found the predicted dip; the lead becomes a candidate for two-key review, not a planet." INCONSISTENT: "The follow-up found a dip that does not match the prediction; the lead as written is not supported." EXCLUDED: "The follow-up rules out the predicted transit with at least 95% sensitivity; the lead is closed for the families covered." INSUFFICIENT: "The follow-up could not decide; the lead stays open."
7. **Deposit before the new data exist.** For a test on future data, the preregistration file and its hash go to a public, timestamped deposit (Zenodo, as Rabtsevich did) before the sector is observed. That is an outward, public action: only with both keys and Ahmed's yes, and it ends the lead's privacy for that star.
8. **TESS DDT route.** A Director's Discretionary Time request (official page https://tess.mit.edu/science/ddt/, read 3 Nov 2026) can be sent at any time, about six weeks before the sector starts, by email with the template; it asks for 2-minute or 20-second cadence on our star. Only for a two-key lead, with Ahmed's yes; Ahmed sends it or approves the exact text.
9. **Novelty, dated.** Before step 2, `pipeline/novelty_check.py` (T127) runs and its UTC sentence is copied into the lead file; INCOMPLETE is rerun, never read as novel.
