# Observatory Memory System (OMS): concept saved in full (3 Nov 2026)

**Status: DEFERRED. Concept preserved; nothing built, nothing in the pipeline or book changed.** Compass verdict: REVISE (on the proposal's own scale: DEFER). Ahmed agreed with the reduced scope and the reopen rule on 3 Nov 2026, about 02:00 Kuwait. Review: `research/compass-reviews/2026-11-03-observatory-memory-system.md`. Queue: T123 (full OMS, deferred) and T124 (the kept piece, the evidence index). Memory pointer: `project_oms_deferred.md`.

Origin: a proposal written by ChatGPT for Ahmed, given to Claude on 3 Nov 2026 at 01:39 Kuwait for a Compass pass. The proposal said REVIEW ONLY, no files, no commits. This file was written afterwards, at Ahmed's request ("make sure the concept of OMS is saved"). The structure below follows the proposal; the lists are kept as written.

## 1. The idea

Second Sun should not meet the same scientific problem twice without being able to retrieve what it learned. Today the knowledge sits in logs, research records, experiment results and decisions. OMS would be a scientifically grounded, searchable, versioned, evidence-linked historical memory built around the real workflow. Not a chatbot memory, not a generic AI knowledge base.

Example: a transit-like signal appears. Before it goes further, OMS retrieves: the same target's earlier suspicious dips; dips that coincided with eclipse residuals; a sector with documented quality issues; a detector configuration that struggled with this kind of signal; similar observations investigated before (artifact or unresolved); another sector with a similar shape. The investigator then sees what happened before, which configurations were involved, what is established, what is uncertain.

Key limit, in the proposal's words: historical similarity does not establish the same cause. A real planet could look like an old artifact. OMS retrieves evidence and gives context; it never decides.

## 2. The five components

**A. Target Memory.** The history of investigations of one target. Fields: target identifier and catalogue provenance; processed TESS sectors; observations and data products; detected signal-like events; investigation outcomes; documented data-quality issues; detector configurations used; injection-recovery results; links to experiments and decisions; unresolved questions. It must not hold unsupported conclusions about the star.

**B. Sector Memory.** Issues and observations per TESS sector and data product. Fields: sector id; observation and target references; known quality flags; instrumental or processing anomalies; missing observations; pipeline-specific problems; recurring patterns; evidence for each. Do not generalise from one target to a whole sector without evidence.

**C. Artifact Library** (called potentially the most important). A structured catalogue of investigated false-positive patterns. Categories: eclipse residuals, stellar variability, detrending-induced signals, instrumental discontinuities, gaps and interpolation, systematic noise, other documented non-planetary causes. Each entry: unique artifact id; description of the pattern; evidence for the classification; target and sector references; original data and experiment references; detector configuration; classification status; confidence and limitations; first observed and last updated dates; number of independently investigated observations. It must separate established artifacts from suspected patterns.

**D. Detector Memory.** How detection and validation configurations performed: which versions and configurations were tested; what happened to known injected signals; which recovered genuine injections; which produced false positives; whether detrending destroyed shallow signals; whether a parameter change helped or hurt; differences across target types or data products. Must not change the detector silently: no automatic threshold changes, no self-modifying pipeline; any change goes through the existing test, review and approval process; claims need reproducible experiments (injection-recovery and controls).

**E. Evidence Retrieval.** The link between the four. For a new signal (morphology, target, sector, configuration) search: (1) earlier observations of the same target; (2) the same sector; (3) similar investigated patterns; (4) experiments with comparable configurations; (5) relevant injection-recovery results; (6) earlier decisions and unresolved investigations. Output: a concise historical evidence report; every item points back to its original evidence.

Ahmed allowed a better architecture, merged components, renamed or rejected ones.

## 3. The hypothetical report (numbers illustrative only, not findings)

OBS-EXAMPLE-001, a 1,200 ppm transit-like dip. OMS returns: 14 comparable observations investigated before, 11 classified artifact, 3 unresolved, several involving eclipse residuals, a similar configuration tested under injection-recovery. Report line: "Historical warning: relevant previous investigations exist", with matching records, reasons for similarity, differences, evidence for earlier classifications, limitations, links. It must NOT say "false positive", reject the observation or change its priority. The new observation may strengthen, weaken or challenge a pattern: that is the feedback loop.

## 4. Eight integrity rules (architectural requirements)

1. Evidence before classification: every classification has traceable evidence; an AI description or similarity score is not evidence.
2. Historical similarity is not proof; it can justify more investigation, never accept or reject a candidate.
3. No autonomous scientific decisions: no auto reject or promote, no threshold changes, no rewriting history, no detector changes, no overriding humans, no planetary claim.
4. Preserve the two-key principle: OMS must not let AI-generated history shape the blind human review. Investigate withholding history from reviewers until their independent assessment is locked.
5. Immutable history: a changed classification keeps the old one, the new one, the reason, the evidence, the reviewer, the date, the software and data versions.
6. Provenance on every important record; the research process can be reconstructed.
7. Uncertainty stays visible: project vocabulary, no invented confidence percentages. (Note: the proposal lists VERIFIED, LIKELY, UNCERTAIN, NOT TESTED. Since 28 Oct 2026 our word is CONFIRMED, not VERIFIED.)
8. Reproducibility: a future investigator can find the original observation, experiment or analysis behind any entry.

## 5. Architecture questions Ahmed asked to be investigated

Options named: relational database, versioned JSON records, indexed metadata and evidence references, existing project structures, search indexes, deterministic similarity matching, optional embeddings. No vector database or language model assumed; lightweight and reliable; no new infrastructure or maintenance burden; evidence store kept separate from any future similarity layer and readable without any AI service. Ten questions: (1) what already exists; (2) what existing systems do part of this; (3) overlap with the Claims Register, Compass, decision logs; (4) what can be linked by reference instead of copied; (5) the smallest useful version; (6) updating records without losing provenance; (7) missing, incomplete or conflicting information; (8) whether retrieval adds confirmation bias; (9) use beyond the original target catalogue; (10) behaviour when the history store is unavailable.

## 6. Interface idea

A section called OBSERVATORY MEMORY, in the style of a scientific observatory research archive (not a SaaS dashboard, not a chatbot, no decorative statistics). Subsections: Target Histories, Sector Anomalies, Artifact Library, Detector Performance, Previous Investigations, Unresolved Questions, Memory Activity. Counts shown (targets with records, artifact patterns, sector observations, completed investigations, unresolved patterns, configurations with documented performance) must be computed from real records; empty categories never shown as findings. Respect the existing visual identity; no site redesign.

## 7. Integration points Ahmed wanted inspected

Target catalogue; existing data and observation records; detector output; Stage 1 and Stage 2 workflows; Claims Register; Compass; decision and experiment logs; candidate and lead records; evidence and provenance mechanisms; website and docs structure. Principle: no parallel system if the existing architecture fits; one coherent architecture, not five competing databases.

## 8. How usefulness should be tested (Ahmed's list)

Does retrieval find relevant history; reduce repeated work; surface known artifacts; improve traceability of decisions; separate known problems from unresolved ones; accidentally raise confirmation bias; can historical replay show gains? Proposed method: take a frozen set of past investigated observations, hide their outcomes, test whether OMS retrieves the relevant evidence without leaking the answer; measure retrieval usefulness and false associations. Never claim better accuracy just because more warnings or records were retrieved.

## 9. The report Ahmed asked for

A executive verdict; B existing architecture audit; C proposed architecture (diagram, responsibilities, data flow); D data model (entities, identifiers, provenance, versioning); E integration map (existing versus proposed points); F scientific risks; G validation strategy with measurable criteria; H implementation roadmap (scope, files, dependencies, tests, risks, acceptance per phase); I resource and maintenance assessment (measured versus estimated); J final recommendation, one of PROCEED, PROCEED WITH REDUCED SCOPE, DEFER, REJECT; then the single most important decision before it moves forward. Only A, B, F, G, J and the kept piece were answered in chat on 3 Nov; C, D, E, H, I were not written because the recommendation was to defer (a full set costs about 1 point if wanted).

## 10. Ahmed's own words on why

"Second Sun should not be just a machine that looks for periodic dips in stellar light curves. I want it to become a research environment that systematically learns from its own investigative history." He prefers "a small, reliable historical evidence system" to an impressive AI architecture, and wants every piece of knowledge traceable, verifiable and open to correction. "A good observatory doesn't just collect observations. It preserves what it learns from them."

## 11. What the Compass pass found (details in the review file)

- Measured 3 Nov: 52 open boxes and 12 done in the build queue; G3 download stalled at 410 of 612; Vesper 0.9 not frozen; Candidates page empty (no candidate has gone through the two-key process); git tracks 746 files, `.git` is 12 MB.
- Out of date in the proposal: 549 targets (that was G1; lists are now 549, 895, 612); Stage 1 and 2 (now Vesper 0.8.0 on the G lists; Stage 1 recorded no events); the Claims Register (`research/claims.md` is an empty table; the real one, `book/data/claims.csv`, 99 rows, holds book facts); VERIFIED (now CONFIRMED).
- Core problem: almost no labelled real artifacts exist. Known-truth examples are planted dips and the upside-down control. The sealed G2 run showed real events did not outnumber the control, so there is little real history to retrieve.
- The repo is public and `data\` is git-ignored, so real events cannot go into a public tamper-evident history.
- Existing partial equivalents: VESPER-VERSIONS.md and the frozen settings hashes (Detector Memory), Vesper's 9 flags and the 6 Eyes classes (Artifact Library), the Loom plan (windows table, run status record) and the Vigil ledger (Target and Sector Memory), decisions.md, mistakes.md, predictions.md, 15 Compass reviews, LEADS-RULES.md, the two-key method file.
- Risks: adaptive triage is a researcher degree of freedom against frozen and preregistered rules; sealed or spent data could leak into later reviews; showing "11 of 14 similar ones were artifacts" anchors a reviewer; more warnings is not more accuracy.

## 12. What is kept (T124) and when OMS reopens

Kept: an evidence index inside Loom phase 4. One read-only script that builds a plain page linking existing records by star list, Vesper version and sector. No new database, no real events, nothing classified. About 0.8 point (NOT TESTED).

Reopen the full OMS when all three hold (my rule of thumb, UNCERTAIN, not measured): the G3 result has been read; Loom phase 4 (run status record) exists; about 10 real leads have been closed with a documented cause. Full cost guess 12 to 20 points (UNCERTAIN).

## 13. Resume checklist

1. Read this file, the review file, T123 and T124.
2. Check the three reopen conditions against the files, not memory.
3. If they hold, ask Ahmed for the go, then write C, D, E, H, I of section 9 (about 1 point) before any build.
4. Never put real event records in the public repo; the store for them stays under `data\`.
5. Keep the evidence store readable with no AI service; any similarity layer is optional and separate.
