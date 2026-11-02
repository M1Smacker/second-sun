# Vesper Loom: research file (blueprint method; started 2 Nov 2026 about 06:00 Kuwait; written overnight while Ahmed sleeps)

Ahmed's order (2 Nov, about 05:10): research the Loom extensively and exhaustively with `research/RESEARCH-BLUEPRINT.md`, EARLIER than the other optional work, then reshape phase 0 from what it finds and do phase 0 only if there is room under the stop line; tell him in the morning how useful the research was. His priorities for the Loom: **trust** (two runs comparable, too many moving parts) first, speed a distant second, "connected" means both scripts that fit together and the book and status pages, no drastic change.

**Status line (update as I go):** STARTED. Own-data checks next, then the web.

## 0. How usefulness will be judged (written BEFORE reading any source, so it cannot be bent to fit)
- **Counterfactual test on today's three incidents** (score each yes, partly or no: does the research hand me a concrete, named practice that would have PREVENTED or DETECTED it before it cost anything?): (I1) hidden input: QLP windows borrowed from a manifest that grew (item 70); (I2) the same tier logic written in several places, caught only by a consistency check (retier, the price table, merge_sap); (I3) an older run used as baseline without checking that it was made under the same conditions.
- **Plan changes caused** (count): phase 0 design changes, phases added, dropped or reordered, tools adopted or rejected. A question whose answer changes nothing is recorded as "no change" and does not count as useful.
- **Cost:** weekly points spent on the research (get_usage before and after; estimate written first: 2.0, hard stop at 3.0).
- Verdict in the morning report: useful if at least 2 of 3 incidents get a concrete answer AND at least 3 plan changes; marginal if 1 incident or 1 to 2 changes; not useful otherwise. The numbers go in `usage-ledger.md`.

## 1. Questions, each tied to the decision it feeds
- **Q1 cache keys (feeds phase 1 design and "home-made or framework").** How do reproducible build and workflow systems decide a result is stale (Snakemake rerun triggers, DVC lock files, Make timestamps, Bazel and Nix hermetic inputs), what do they hash, and which failure modes do they document for inputs that are not declared (our neighbour windows)? Answer that would change the plan: a system that already keys on code, input content, parameters and software environment and is small enough to adopt, or a named failure that tells us what the key must contain.
- **Q2 data and pipeline provenance in survey pipelines (feeds the run recipe in phase 0).** What do Kepler SOC and DR25, TESS SPOC, QLP and TESS-SPOC document so that a result can be tied to exact data and code versions (data release notes, reprocessing, file checksums)? Our own note: "the same star can have different files later". Changes: the fields the recipe must record.
- **Q3 neighbour-dependent inputs (feeds the item 70 fix).** How do pipelines whose correction for one star depends on other stars (Kepler PDC cotrending basis vectors, TESS CBVs, QLP) freeze and version that shared input? Changes: a windows table per star list as a versioned file (expected) or something else.
- **Q4 switches and hidden state in scientific code (feeds phase 2).** What is the evidence-based practice for study switches (feature flags), configuration passed explicitly versus environment variables read at import, and for proving that "switch off equals the old behaviour" (golden-master or differential tests, mutation testing)? Sources on configuration debt and testing scientific software. Changes: how options are passed, what gates a refactor of frozen files.
- **Q5 trustworthy comparison of pipeline variants (feeds the study harness and incident I3).** How do injection-recovery and variant-comparison studies keep two runs comparable (paired injections, same inputs, input fingerprints, event-set diff gates)? Changes: automatic like-for-like gates in the harness.
- **Q6 where time goes and what is known to be fast (feeds phase 3).** Our own profile of the chain first; then what the detrending (wotan biweight) and box-search literature report for speed (BLS and TLS implementations, numba, vectorising). Changes: which speed step is worth its risk (cache, parallel count, algorithm).
- **Q7 numerical reproducibility across worker counts (feeds the 70% CPU order and any parallel change).** Are our results bit-identical when the worker count or order changes (numba, floating point reductions, multiprocessing)? Our own test first (zero difference with 8 workers passed 300 of 300 on 2 Nov); the literature only for the part we cannot test. Changes: whether worker count may vary freely.
- **Q8 connected status (feeds phase 4).** What minimal run-manifest or status format do workflow and provenance standards use (JSON lines, RO-Crate, W3C PROV, OpenLineage) and is any of them small enough for our pages? Changes: one status file format.

## 2. Our own house first (cheapest check, filled before the web)
(to fill)

## 3. Findings by question (source, exact sentence, label, decision fed)
(to fill)

## 4. What changes in the plan
(to fill)

## 5. Usefulness verdict
(to fill at the end, against section 0)
