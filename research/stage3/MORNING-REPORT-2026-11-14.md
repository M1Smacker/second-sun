# Morning report, 14 Nov 2026 (night run 04:02 to about 06:05 Kuwait)

**Plain verdict: found nothing new in the sky (no hunt ran tonight). The big measurement is in: about one planet in two (P = 0.48) reaches the top list, just under the 0.50 bar, so FIX FIRST before G1. Two keys agree.**

## 1. P, the planet-level test (decides G1)
- Codex planted 1,250 Saturn-like planets in real light (all transits, all sectors). P = **0.484** (95% 0.44 to 0.52). My own code on the same files: **0.486**. FIX FIRST: GO needs 0.50, we are 0.016 short.
- Old against new: one *transit* reached tier 1 about 1 time in 4 (R 0.27); one *planet* about 1 time in 2. Better, because a planet gets several tries.
- No period bin under 0.20, so no blind spot to name. Slow binaries do best (0.64), fast ones worst (0.41).
- Biggest fixable loss: transits found but held back by a flag. FIX 92 and FIX 93 aim at that.
- Report: `research/stage3/006-check/P-CHECK-2026-11-14.md`.

## 2. Two real known planets (T109)
- **TOI-1338 b: found.** 4 of 13 transits reach tier 1 (31%), the same as the bench predicts.
- **TIC 172900988 b: missed.** Both transits were found (SNR 8.3 and 15.7) but held back by the ramp, gap and step flags. Its data is 30-minute TESS-SPOC light, about 20 times noisier.
- Only these two known circumbinary planets have transited in TESS.

## 3. Built tonight (no input needed)
- T129: events cluster on stars (design effect 1.5 to 2.1); the G2 and G3 verdicts stand.
- T142 run record, T127 novelty check (6 sources), T54 funnel check: built, tested, each test shown to fail when broken.
- T125 follow-up protocol: drafted only. It binds only if you approve it.
- tree_check fixed (it was skipping phase-tagged builds).

## 4. Number audit (T130): all 15 field notes, 1,544 numbers
- 1,490 trace to a file, a recount script, or are not results. 49 have no saved source (build checks, Eyes generator settings, private event details); none is a verdict number.
- **3 wording calls for you** (no verdict changes):
  1. 11 Nov note: "34 against 13" should be **32** against 13.
  2. 10 Nov note: 0.58/0.95 pools sizes K 12 to 25 only, not all tested sizes.
  3. The correction box "almost all in binaries slower than 20 days" is **wrong**: 31% (G2) and 5% (G3). It sits in **8 book places**.
- Also still live: the old "82.7% of strong ones" sentence (corrections C3 and C4, waiting since 3 Nov).
- One small fix done by me: the 24 Oct note's test counts (16 checks, 18 mutations). Book 2.11.4.
- Small imprecision, your call: the 23 Oct note calls TOI-1338 b "the 0.2% dip"; it is about 0.26%.

## 5. Codex (updated 09:20)
- Codex finished 006 at 07:56: the same P (48.4%, FIX FIRST). The short-binary fix (S) passes but only lifts P to 48.6%; the window repair fails its gate.
- New: the planted bumps lose to the planted dips in slow binaries because of one flag, "dominated" (it holds 21 bumps against 6 dips in the 20 to 27 day bin). Why the flag does this is not known yet: my first guess (eclipse leftovers) was tested and is wrong. Same flag as FIX 93.
- Fence check of its branch: clean (no frozen file, no fenced star).
- The 007 line is now stale. **Send this instead:** "Read research/astra/inbox/008-after-006.md and do it in order. No polling."

## 6. Your calls
1. The 3 wording calls above (and C3/C4).
2. Approve T125 and T127 into the G1 preregistration, or not yet.

## Meter
Weekly about 95%, five-hour about 75% (resets 09:00 Kuwait). Book 2.11.5 (home recap) publishing.
