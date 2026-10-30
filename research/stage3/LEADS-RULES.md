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
