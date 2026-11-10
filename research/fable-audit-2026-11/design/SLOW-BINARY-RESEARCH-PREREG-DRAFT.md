# DRAFT preregistration: G4a, the slow-binary re-search (written by Fable, 10 Nov 2026)

**Status: a draft in the audit folder. Not approved, not filed, nothing started.** It becomes a preregistration only when Ahmed approves it, Petrova 1.0 is frozen, and this text is committed BEFORE any light is read with 1.0.

## Why
Vesper 0.8.1's eclipse mask deleted most strong dips in binaries slower than about 10 to 14 d before the search (audit finding F-01). Those dips were never scored, flagged or seen by anyone. With a corrected mask the same light can be searched for the first time. It costs no download and it is where 8 of the 12 known transiting circumbinary planets live (binary period over 18 d).

## What is and is not blind (said plainly, before the data)
- NOT blind: every event 0.8.1 reported on these stars (real and upside-down), the G1 to G3 verdicts, and the counts by period in the audit (`evidence/p01b_real_vs_flip.txt`). The mask design was chosen from injections and from upside-down and real COUNTS, never from looking at an event in the masked light.
- Blind: any dip in light the 0.8.1 mask removed. No script of ours has scored that light; no person has looked at it.
- Consequence: the evidence of this hunt is counted ONLY from events whose centre lies in cadences that the 0.8.1 mask removed and the 1.0 mask keeps ("the recovered light"). Events in light both masks keep are reported for completeness but are never evidence here, because 0.8.1 already judged that light.

## Star list (rule fixed now)
Every star of `targets/g1_targets.csv`, `g2_targets.csv` (development AND sealed) and `g3_targets.csv` whose catalogue binary period is 10 d or more. No brightness cut beyond the original lists. One row per TIC. The list file and its SHA-256 are committed with the preregistration. Expected size from the audit counts: G2 about 426 stars and G3 about 276 stars at 10 d or more; G1 NOT COUNTED (count it before filing).
Why 10 d: on real light the loss is about a third to two thirds from 10 d and small below (`evidence/p01c_real_light.txt`); below 10 d the recovered light is too little to matter.

## Search
- Petrova 1.0, frozen, hash recorded here before the run. Same light files already on disk (hash the manifest). No new download.
- Both arms. The upside-down arm is built with the mirrored mask rule.
- One shot. The run script refuses without the frozen hash, the go file and a clean tree, as `g3_run.py` does.

## Success checks (preregistered)
- **R1 completeness, measured before the run:** on a random 300 star-sectors of this list, dips injected into raw light before any step, K 8 to 25, durations 4 to 20 h: tier-1 recovery in every binary-period bin (10-14, 14-20, 20-27, over 27 d) is at least 0.8 of the recovery of the same injection added after the mask. If not, the hunt does not start.
- **R2 exchangeability, measured before the run on the same 300 star-sectors with nothing injected, upside-down and real pooled and unlabelled:** not looked at. Instead on SYNTHETIC light with toy eclipses and on light already judged by 0.8.1 (kept by both masks): real over upside-down event ratio between 0.8 and 1.25 in every period bin. If not, the hunt does not start.
- **S1 (the result):** in the recovered light only, first-tier real events against first-tier upside-down events at bars 7, 8, 10, 12, star-level bootstrap as in `scorecard_plus.py`. Rule for an excess as in G3: chance 0.01 or less at bar 7 and real above expected at the other bars.
- **S2 (false alarms, new definition for 1.0):** upside-down first-tier events per 1,000 star-sectors of recovered light, reported with a star-level interval and NO pass or fail mark (Ahmed's decision of 10 Nov: option A). A mark may be set for later hunts from this number.
- **S3 single-visit lane:** dips in phases seen only once (cannot be told from a second eclipse by repetition) are counted separately, never as S1 evidence, and go to the binary-phase duration key and the eye.

## Leads
Stage rules for leads are written and committed before the results are read (the standing rule). A lead needs two keys and Ahmed's yes before anything is said. Star IDs, times and pictures stay under `data\`. The Search window shows counts only.

## What a null will and will not say
A null says: in N star-sectors of slow binaries, no dip of at least K times the noise survived the checks, with completeness c(period, K) measured by pre-mask injection. It replaces, for these stars, the 0.8.1 statements that F-01 voided. It says nothing about planets smaller than the reach map shows.

## Open choices for Ahmed (before filing)
1. Include the G2 development stars (they were used to tune c6)? My lean: yes, flagged as a separate stratum; their recovered light was never seen either.
2. Period cut 10 d (my lean) or 14 d.
3. Name: G4a, or fold it into Census as its first stage.

## Cost (UNCERTAIN)
After Petrova 1.0 exists: preregistration and list 0.5; R1 and R2 about 1; the run about 0.5 (machine time minutes); scoring and report about 1. Sonnet with Opus review.
