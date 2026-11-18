# 030 decisions before N1 results

Branch astra/030-notch-tier-bench. No branch switches, commits, pushes, or other git writes. Data and redirected pipeline copies are confined to data/astra/030/. Tree nodes 1.3, 1.5 and 1.6.

The executable frozen grid has nine box lengths: 3, 4, 5, 6.5, 8, 10, 12, 15 and 20 hours. The brief's phrase "ten lengths" disagrees with the code. Preserve the actual frozen grid, which is also what the RS-039 reference initializes. Do not invent a tenth length.

N1 uses the reference five-day biweight, cadence-aware binning, minimum box/flank coverage of 80%/60%, lower flank, median-centred depth, and MAD scale. Physical event depth is lower-flank mean minus box mean. The existing step measurements use the five-day flattened curve's median, through the unchanged step function. Cross-product and PDC confirmation use the N1 statistic with their existing tier limits. The only extra degenerate-data handling is no detection when the robust scale is zero or nonfinite.

Generate candidates once at 4.5, then filter before recalculating mirror/repeater flags, SAP merging, cross-star coincidence, orbit/phase flags, OAE and FIX 95. Greedy selection above any higher threshold is a subset of the candidates at 4.5; synthetic tests check that property. Retain unrounded N1 scores and centres to prevent rounding across a threshold or the new mirror boundary. Off-switch serialization is unchanged. Mirror distance is at most one quarter of the event's own box length, in either orientation.

Choice rule, unchanged: lowest of 4.5, 5, 5.5, 6, 6.5, 7 with at most 174 real and 79 upside-down tier-1 alarms. If none qualifies, no chosen N1 exists, so no fresh N1 is scored. Otherwise the choice is saved before the choosing/fresh/T156 injections are scored. No threshold is selected from planet recovery.

Use the existing 006 draws, the host-radius definition of the 968 possible planets, and Fable X1 draws with seed 2026111601. No new draw law. Inject into loaded flux before windows, eclipse masking and detrending, on both signs. Keep the historical B novelty rules. N1 credits only crossings not already present in its own untouched background; T156 also retains the historical preexisting exclusion.

P averages the five binary-period-bin rates equally. Bootstrap whole hosts, retaining all planets on a host together, 10,000 draws with seed 2026111830. Rule (c) uses every bin of the possible-planet populations on both choosing and fresh benches; all-planet controls are also diagnostic outputs. R uses the exact 222-trial reference subset for the brief's 34.207% comparison, with possible-only R also reported.

Rule 4 new-event matching preserves the existing bench tolerance: same campaign, host, sector and arm, within 0.1 day plus half the larger box. This is a tolerance-based comparison, not byte identity. Hold counts overlap. TOI-1338 matching uses the existing T109 observed/forecast windows, but tier decisions come from the full background context and adopted B rules.

Long work uses foreground subprocesses, three scoring/generation workers maximum, two Numba threads each, private logs, and terminal checkpoints. Shared injection output directories are created before parallel work. The full-run script locks source hashes; a changed source cannot reuse completed markers silently. Producer verification does not replace Claude's independent review.
