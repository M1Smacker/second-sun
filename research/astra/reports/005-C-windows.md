# 005 C. Window losses, node 1.2 (GPT-6.1 Sol)

**Verdict: 16 of the 52 reference window losses have usable input samples and could be addressed by coverage work. Safe recovery remains unmeasured.** Saved T156 statuses determine the 52 reference window losses. Saved traces lack pre-quality and pre-window cadence arrays. Predeclared targeted diagnostic reads only these design files and replays preparation without detection. Compare recorded finite TIME and frozen quality-selected raw timestamps to the same 1.5 cadence centre test, then reconstruct own-SPOC/neighbour coverage. Use available archived quality and saved instrument timing to count associations, without calling an exclusion safe or harmful solely from its flag. No changes to windows or masks in this measurement.

## Results

| Centre support | G2 | G3 | Total |
|---|---:|---:|---:|
| No recorded finite timestamp near centre | 14 | 1 | 15 |
| Recorded timestamp, excluded at load | 17 | 4 | 21 |
| Quality-selected flux outside safe windows | 6 | 4 | 10 |
| Quality-selected flux, no safe windows | 1 | 5 | 6 |

CONFIRMED from 005_windows.py. The original stage breakdown reconciles exactly: 45 outside/gap and seven no-safe-window classifications. One of the original seven also loses centre support at load, so only six offer immediately usable input samples. The tested centre test is the original 1.5 median cadence tolerance, and pertains to the archived products selected by the original best-product rule. In 20 of 21 load losses at least one finite archived flux sample exists inside the tolerance. Frozen load rejected it or did not return it. One has no finite archived flux. This distinction uses the frozen flux column and the permitted SAP fallback. It does not identify the causal quality bit for each discarded sample.

The ten safe-window exclusions break down into three own-SPOC coverage exclusions, five neighbour intersections and two explicit half-day window-start trims. One of the ten lies within half a day of a momentum dump. These are traceable mechanisms and associations. The trim is an intended settling/scattered-light protection (pipeline/detect_v2.py:94-110). The intersection and own-SPOC rules inherit quality and gaps from other products (stage2_search.py:150-160 and audit_all.py:107-109). A dump association does not establish scattered light as the cause. No case here has evidence that its exclusion only costs light without providing protection.

## Coverage candidate for later testing

Node 1.2, fill missing detector coverage using independent, quality-screened SPOC time support on the same sector/camera/CCD, retaining at least two independent reference windows and the current intersection and start trim. Measure the six missing-window cases first. Use approved design-only references or shared machine-input time support within the fence. Require independently verified additional references before activating the candidate. Own QLP quality alone is insufficient evidence for removing the neighbour safeguard. This candidate needs a validated expanded window table and then new processing of affected planted and un-injected files. Neither is available in the current targeted replay. No change or candidate bench was executed. The six eligible trials give an upper bound for this missing-coverage candidate, not predicted recovery.

Future acceptance predeclared: reference R rises from the combined baseline, background upside-down tier-1 stays at most old + 2 x sqrt(old + 1), and each paired dip-minus-bump 99% interval includes zero. Preserve the fixed 2,000 draws and unchanged background population. Invalidate the comparison if old window/flag replay changes under unchanged settings.

CONFIRMED distinction: truly absent samples cannot be restored by a window rule. UNCERTAIN: how many of the 16 can actually be recovered with safe support. NOT TESTED: causal protection of each excluded interval and new coverage performance. No bug established. STOP SIGNS: no candidate widening without evidence. QUEUE PROPOSALS: node 1.2, log these counts under T155 and FIX 26/70. IDEAS: only the candidate above. Questions for Ahmed: none. Usage in combined ledger. Branch astra/005-three-diagnoses.
