# Compass: how Second Sun reviews big proposals

*Named by Ahmed on 2026-10-20. Every big prompt about advice, upgrades or "how can we improve" goes through Compass before anything is built.*

## The rule
Review the proposal against our existing code, findings, tests and established astronomical methods. **Review only:** no file changes, no code, no modules, no implementation during a Compass pass.

## What a Compass review checks
1. **What already exists** in the repo (code, tests, results). Read the code; don't assume.
2. **Genuine gaps**: what is truly missing, not just renamed.
3. **Scientifically incorrect assumptions**, in the proposal *and* in our current code.
4. **Duplicated functionality**: an existing module, or a tool we already have (STANLEY, lightkurve, triceratops...), that does it.
5. **Risks**: scientific (false confidence, bias), practical (data size, C: drive, licences, usage budget).
6. **Sources**: verify claims against reliable sources where it matters; label each finding.
7. **Order**: recommend the sequence with the greatest scientific value, justified by current evidence.

## Labels
- **VERIFIED / CONFIRMED**: we ran it, or read it in a primary source.
- **LIKELY**: secondary source, abstract only, or memory consistent with sources.
- **UNCERTAIN**: plausible, open questions.
- **NOT TESTED**: proposed or written, never run.
A promising idea is not an improvement until its value is shown.

## Output format (concise, phone-readable)
1. **Verdict:** APPROVE, REVISE or REJECT.
2. **What's correct.**
3. **What needs changing**, and **why it matters**.
4. **The single best next step.**
Findings marked verified vs assumed vs untested throughout.

## Labels (Ahmed, 28 Oct 2026)
Use CONFIRMED, LIKELY, UNCERTAIN, NOT TESTED (CONFIRMED replaces VERIFIED in new notes). The standing rule "verify before concluding" is in `D:\second-sun\CLAUDE.md`: a search summary is a lead, not a source; open the paper or table.
