# The two-key method for real candidates (agreed discussion with Ahmed, 24 Oct 2026)

*Ahmed asked: how do we make sure we are not both wrong, and how sure can Claude be on real data? This is the answer, saved. Nothing here is built yet. Related: `eyes-saving-plan-2026-10-23.md`, `firebase-setup-steps.md`.*

## 1. The three kinds of verdict Claude may give (never "planet")
1. **CONFIRMED ARTIFACT**, with the named cause (eclipse, thruster firing or data gap, same moment on other stars, flare or glitch, scattered light, neighbour star).
2. **CONSISTENT WITH A PLANET.** Not proof. It means the checks we have done did not rule it out.
3. **UNRESOLVED.** Always an allowed answer; the default when the evidence does not settle it.

## 2. How sure Claude can be, by type of event
| What it might be | Confidence | Why |
|---|---|---|
| Eclipse of the two stars | very high | known timing and catalogue ephemeris |
| Thruster firing, data gap, jitter | very high | quality flags; other stars show it at the same moment |
| Flare or glitch (spike up) | very high | planets only make dips |
| Scattered light | fairly high | background flux column |
| Dip from a neighbouring star | moderate until pixels are tested | needs the pixel and catalogue test |
| Shallow single dip versus red noise | cannot be settled from one event | needs repeats, a prediction or other evidence |

In practice the answer is certain only because we planted it. On real data there is no ground truth. Claude is good at numbers and systematic checks, weaker at judging a noisy picture by eye, and has made about ten logged mistakes in this project: the process below is the safeguard, not trust in Claude.

## 3. How we avoid both keys being wrong together
Agreement between two opinions is not evidence. Defences, in order of strength:
1. **Independent and blind.** Claude writes and fingerprints (hash) its verdict BEFORE Ahmed answers; Ahmed answers BEFORE seeing it. Disagreement is the useful signal. (The 3 trial leads are already fingerprinted this way.)
2. **Blind controls with known truth in every session.** Hidden fake dips injected into real G1 stars, plus known-false items (known-host events, quiet stretches, eclipses). Measures both keys' error rates on data like the real data; a key that fails controls counts for less that session.
3. **Tests that need no opinion:** the same dip in a second data product (independent pipelines); a pixel test (does it come from our star or a neighbour; Kepler and Gaia catalogues); the star's own eclipse timing; same moment on other stars; the Kepler-era data; the shape (flat-bottomed, symmetric ingress and egress, a length that fits the binary's geometry).
4. **A prediction made before the data.** The strongest test is predicting the next dip and checking it. TESS returns to the Kepler field in July and August 2027.
5. **Outside eyes.** For anything big, Claude drafts the message to astronomers and Ahmed sends it.
- **Rule:** two opinions never make a candidate. A candidate needs both keys AND at least one independent physical test passed. Everything else stays UNRESOLVED. We only ever claim "candidate", with a probability.
- **Pre-registered rules:** criteria written before looking; frozen lead lists with a hash; no moving goalposts.
- **Calibrate on the future:** when truth arrives (2027 TESS data, ExoFOP dispositions), score all past verdicts of both keys.

## 4. The two pages (requested by Ahmed; NOT built; he must approve; his last instruction was "do not build anything yet")
**Eye training record** (Hunt tab, next to Eyes): rounds attempted, curves seen, right, wrong, not sure, hit rate by kind (clear, faint, quiet, odd), trend over time, pass-line status, recent rounds. Updates automatically once Firebase is set up (daily publish; device numbers immediately).

**Real-candidate Eyes page**, built LOCKED and EMPTY (no real data) until Firebase is up, he has done many practice rounds and Claude is completely sure he is ready (Claude alone decides; the page shows a visible progress bar to the pass line):
- Answers: planet-like dip, eclipse, flare or spike, jump, instrument or scattered light, other variable star, can't tell; plus how sure and an optional note. Saved after every answer, uploaded by itself.
- Graphs: whole sector, a zoom around the event, and a second data product underneath; eclipses, thruster firings and data gaps marked; same scales; in hours from the event.
- No right/wrong counter: his labels go to Claude, the second key, who verifies against the independent tests above.
- Teaching: after his answer is saved, Claude's reading and explanation are shown (pre-recorded and fingerprinted, so no hindsight); if he is clearly off, it says why.
- Rehearsal mode (Claude's suggestion): fake candidates injected into real stars with known answers, to practise the real interface first.
- Can be PUBLIC for now (Ahmed's decision: nobody is looking; revisit when something big appears).

## 5. What Claude can and cannot promise
Can: build and browser-test both pages against every failure mode it can think of, as done for Eyes mode (17 logic checks, 34 browser checks, each mutation-tested). Cannot: promise zero bugs, test on a real iPhone, or give certainty about a shallow single dip. Pixel tests need small data downloads (logged, asked first).

## 6. Prompt for Claude AI (optional outside research on presenting the dots)
> I'm building a web page where a beginner and an AI both classify candidate dips in TESS light curves (circumbinary planets, long dips of 3 to 18 hours, eclipsing binary hosts) as planet-like, eclipse, flare, step, instrumental, or unclear. Research best practice for presenting these to a human: the Planet Hunters TESS and Zooniverse interfaces, Kepler/TESS data-validation one-page reports, LATTE and DAVE vetting plots. Tell me which panels, zoom levels, axes, markers and colours help people judge accurately, what causes human mistakes (anchoring, over-reading noise), how to avoid biasing a second reviewer, and how to measure reviewer accuracy with hidden controls. Give concrete layout recommendations for a phone screen and cite sources I can check.
