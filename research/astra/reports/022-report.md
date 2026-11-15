Found 8 issues, 7 confirmed and 1 explanation that remains a hypothesis.

# 022 Twinlight lessons 2.3 to 2.5 fact-check

Codex, runtime model and effort unverified. The brief specifies neither. AS-022, 15 Nov 2026, 15:39 Kuwait, from `Get-Date`.

**Process slip.** I attempted to retrieve an IAU PDF URL through the web tool. The request returned 404 and retrieved no PDF. This should have used an HTML source from the outset. The successful IAU check used arXiv HTML.

**Branch** `astra/022-factcheck-lessons-2-3-to-2-5`. Node **4.1**, the learning rebuild. Scope was findings only. Deliverables are this report, the usage row, and private scripts and evidence under `data/astra/022/`. The pre-existing `.codex_run.lock` belongs to the runner.

**Decision and cap.** Decide which lesson claims Claude should correct or qualify before accepting their fact-check. Predicted 30 five-hour points and 6 weekly points. Research cap 14 web calls, used 14. Both usage meters are inaccessible in the headless runner.

## Findings

Line numbers refer to the current lesson Markdown. P2 means a substantive scientific or teaching error, P3 a misleading approximation or explanation, and P4 a small arithmetic or presentation defect. No P1 finding.

| ID | Lesson | Line | Claim | What is wrong and proposed correction | Evidence | Severity | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LX-01 | 2.5 | 94 | The constant becomes exactly 1 because the units are defined by Earth's orbit | Modern AU, year and solar-mass conventions give a coefficient extremely close to 1. The stated exactness and explanation of the definitions are false. Say approximately 1 and identify the year convention. | Independent calculation gives `4*pi^2*AU^3/(GM_sun*Julian_year^2) = 1.000037773849`. The AU is fixed in metres and a Julian year is 365.25 days. [JPL parameters](https://ssd.jpl.nasa.gov/astro_par.html) | P2 | CONFIRMED |
| LX-02 | 2.5 | 8, 12 | An eclipse every 19.7 days, with that beat maintained for the whole 3-billion-year lifetime | Each eclipse kind repeats roughly once per binary orbit. The pair has two eclipses per orbit with unequal gaps. Its present age establishes no lifelong unchanged eclipse clock. Remove the lifetime claim and specify which eclipse repeats. | The paper reports an eccentric, precessing binary. Its orbital period describes a full revolution. Lesson 1.1 already explains the unequal gaps. [Kostov, sections II and IV](https://arxiv.org/html/2105.08614) | P2 | CONFIRMED |
| LX-03 | 2.3 | 74 | Hint `1.79` says the learner used temperature squared | That calculation gives about **1.85**, using both the original and rounded lesson inputs. A learner making the intended mistake receives generic feedback. Change the hint key to the recomputed value. | `1.3124^2*(5983/5772)^2 = 1.850622356`. Rounded steps give `1.850786938`. Both lie outside the 2% hint-matching band around 1.79. `checks.json`, arithmetic | P3 | CONFIRMED |
| LX-04 | 2.4 | 16 | The separation is smaller than anything a telescope can separate | This overstates a valid statement about TESS. The lesson's separation and published distance correspond to approximately 0.77 milliarcseconds. Optical interferometry reaches finer angular resolution. Restrict the claim to TESS. Target-specific interferometric feasibility was untested. | Script gives `0.77153 mas`. CHARA lists **0.20 mas in the visible at 650 nm**. [CHARA observing documentation](https://chara.gsu.edu/observers/planning-an-observation) | P3 | CONFIRMED |
| LX-05 | 2.4 | 24 to 26, 86 | Seen depth equals the radius ratio squared times the light share | The dilution multiplier is valid, but the area-ratio expression needs the uniform-disc and full-overlap assumptions. Otherwise a beginner can apply it throughout ingress, to a grazing crossing, or to a limb-darkened star. Introduce `seen depth = share * blocked fraction of the crossed star's light`, then give the area approximation. | Winn section 2.5 describes depth increasing near a bright stellar centre and decreasing near the limb. Lesson 1.4 already supplies the relevant assumptions. [Winn](https://arxiv.org/html/1001.2010) | P3 | CONFIRMED |
| LX-06 | 2.4 | 57 | The remainder of the 2,860 versus 2,655 ppm gap comes from the three listed effects | These are plausible corrections, but their contributions have not been demonstrated for this crossing. Qualify them as possible contributors and include parameter uncertainty. Limb darkening can change the depth in either direction. | Calculation gives 2,858.35 ppm and a 7.66% excess over the plotted average. The quoted planet-radius uncertainty alone corresponds to about 7.82% first-order depth uncertainty. A toy red-band calculation raises the prediction to 2,871.07 ppm. The actual attribution remains unmeasured. [Winn, section 2.5](https://arxiv.org/html/1001.2010) | P3 | HYPOTHESIS |
| LX-07 | 2.4 | 67 | Dividing 2,655 ppm by 0.463 gives 5,736 ppm | The displayed division gives **5,734.34 ppm**. The downstream 10.8-Earth-radius answer still rounds correctly. | Independent division in `checks.json`. The 7.38 answer and its tolerance remain valid. | P4 | CONFIRMED |
| LX-08 | 2.4, 2.5 | 2.4 line 76, 2.5 line 39 | First uses of arcseconds and SI | Both are unexplained terms in a beginner course. Define an arcsecond as a small angular unit, 1/3,600 degree. Expand SI as the standard metre, kilogram and second unit system, and give G's units when introducing it. | Static inspection of the three lessons and the earlier lesson text. G's required dimensions also follow from the displayed `g = GM/r^2`. | P4 | CONFIRMED |

## Checks and results

### Independent arithmetic and answer metadata

Expected scales were written into the fresh calculation before interpreting its results. The stars should total a few solar luminosities, the diluted dip a few thousand ppm, orbital speeds tens of km/s, and the station period about an hour and a half.

One command reruns the checks against the saved public sources. It imports no project pipeline code.

```powershell
& 'D:\second-sun\.venv\Scripts\python.exe' -B data/astra/022/factcheck.py
```

The script writes `data/astra/022/checks.json` and prints the same evidence. `checks.log` records the execution. The fresh source download command was the same command with `--fetch`, which intentionally requires a new `sources` folder.

| Check | Actual result |
| --- | --- |
| Problem groups inspected | 23, comprising 17 numeric and 6 verbal answers |
| Independently calculated or reasoned answers accepted by declared metadata | 23 of 23 |
| Numeric answers altered upward by 20% | All 17 rejected by the tolerance comparison |
| Wrong numeric hint keys checked against all accepted answers | 29 checked, 0 accepted as correct |
| Every hint explanation inspected | One wrong misconception value, LX-03 |
| Numeric answer alternatives | Equivalent at the stated precision, including 92 and 92.4 minutes |

This is arithmetic and metadata execution in Python. I read the JavaScript comparison rule to establish relative-tolerance semantics. The browser answer form was not exercised in this brief.

The fresh values include luminosities **2.30766 and 1.98840 Suns**, total **4.29606**, surface-brightness ratio **1.04555**, red-dwarf luminosity **0.00291904**, and **342.58** such red dwarfs per Sun. The lesson's rounded examples and remaining numerical hints agree at teaching precision.

For dilution, the radius ratio is **0.0785853**, undiluted depth **6,175.65 ppm**, and bolometric light share **0.462842**. The inferred radii are **7.37639** with dilution forgotten and **10.84059** after correction. The public plot independently reproduces the **2,655.3941 ppm** average from its 12 specified points. This uses the plot's own zero level and rounded data. Its deepest plotted point is approximately **3,888 ppm**, so this average is a different statistic from the maximum depth.

For gravity, the lesson's rounded inputs give **29.7842 km/s** for Earth, **49.0341 km/s** for the circular approximation around the pair, **14.89 km/s** at 4 AU, and **13.0594 km/s** at 5.2 AU. The station example gives **7,672.59 m/s**, **5,544.86 seconds**, **92.4143 minutes**, **15.582 orbits per day**, and **0.885339** of surface gravity. The intermediate rounding and final answer tolerances are adequate.

### The eclipse-depth explanation

**CONFIRMED within the stated simplified model.** The paper's orbital elements support the lesson's conclusion that unequal overlap supplies most of the contrast. I minimized projected separation and separately checked it on a dense angular grid. I computed circle overlap both analytically and by numerical integration.

Using eccentricity **0.44780**, orientation **69.589 degrees**, inclination **89.4182 degrees** and separation scale **0.191934 AU**, the two projected centre separations are **0.23600 and 0.57735 solar radii**. The overlap-area ratio is **1.21481**. Including the temperature-derived surface-brightness ratio gives uniform-disc eclipse depths **45.1179% and 35.5218%**. Numerical overlap integrals agree within **3.3e-9 square solar radii**. These results support the stated direction and dominant contribution of geometry.

The orbital elements use the paper's Family 1, together with the lesson's abstract radii and temperatures. This is an illustrative cross-check, with parameters from different reported summaries. It is not a reproduction of the paper's limb-darkened three-body fit or the four-sector plotted eclipses at their actual dates. The complete input set is recorded in `checks.json`. [Published orbital tables](https://arxiv.org/html/2105.08614)

### The 8% transit-depth gap

**CONFIRMED arithmetic, UNCERTAIN causal attribution.** The average is recovered from the existing public plot. The 2,860 ppm prediction rounds correctly. Parameter uncertainty, averaging, stellar intensity along the crossing and passband modelling all matter to a comparison at this precision.

The additional band calculation uses two ideal blackbodies, photon weighting and a flat 600 to 1,000 nm response. It gives a secondary share **0.464902**, a small upward correction. This is a toy sensitivity check. It uses no measured TESS response curve or stellar-atmosphere model. No correction was fitted to the observed residual. [TESS wavelength coverage](https://arxiv.org/html/1406.0151), [transit intensity effects](https://arxiv.org/html/1001.2010)

### Primary-source fact checks

The following short quotations or table-row extracts were opened in the primary sources. Values are also compared against the fresh arithmetic above.

| Claim checked | Primary evidence and result |
| --- | --- |
| Radii, temperatures, contamination and age | Abstract radii match 1.3827 and 1.3124. Table 3 extracts include `Teff, 1 (K) 6050 100`, `Teff, 2 (K) 5983 100`, `Contamination 0.000453`, and `Age (Gyr) 3.1 0.1`. The age is model-dependent. [Kostov](https://arxiv.org/html/2105.08614) |
| Planet size, crossing order and mass precision | The abstract supports 11.25 Earth radii and the two-star crossing sequence. Its stellar mass errors are below 0.1%. The statement of a five-day gap is supported. [Kostov abstract](https://arxiv.org/abs/2105.08614) |
| Sun temperature, solar and terrestrial GM, radius conversion | B3 table entries give 5772 K, `1.3271244e20` and `3.986004e14` in SI. Nominal Sun radius divided by nominal Earth equatorial radius gives **109.07637**, which rounds to 109.08. These are conversion constants. [IAU B3](https://arxiv.org/html/1510.07674) |
| TESS pixel and red response | Ricker table 1 says `one pixel, or 0.35 x 0.35 arcmin`. Multiplying 0.35 by 60 gives **21 arcseconds**. Its wavelength row is 600 to 1,000 nm. [Ricker](https://arxiv.org/html/1406.0151) |
| Proxima and red dwarfs | Proxima table 1 gives `m_V (mag) 11.13 +/- 0.01`. The introduction identifies it as the nearest stellar neighbour. NASA describes red dwarfs as the most common stellar type and too faint for the unaided eye. The specific local-census claim remains LIKELY because the supporting Collins full text was inaccessible. [ESPRESSO paper](https://arxiv.org/html/2005.12114), [NASA stellar types](https://science.nasa.gov/universe/stars/types/) |
| Neptune and Saturn size | Equatorial-radius entries are **24,764 and 60,268 km**. Dividing by Earth's equatorial radius gives **3.88266 and 9.44921**, consistent with the stated 3.9 and 9.4 rounding. [JPL planetary table](https://ssd.jpl.nasa.gov/planets/phys_par.html) |
| Jupiter speed | NASA's row reads `Mean orbital velocity (km/s) 13.07` for Jupiter, consistent with the independent circular estimate. [NASA comparison table](https://science.nasa.gov/learn/basics-of-space-flight/chapter1-2/) |
| Station period | NASA says `Each orbit takes 90-93 minutes`. The calculated 92.414 minutes lies within that range. [ISS orbit tutorial](https://eol.jsc.nasa.gov/Tools/orbitTutorial.htm) |
| Kepler and Newton publication dates | NASA explicitly dates Harmonices Mundi to **1619** and Principia to **1687**. The difference is 68 years, consistent with about 70. [Kepler history](https://science.nasa.gov/solar-system/orbits-and-keplers-laws/), [Newton history](https://science.nasa.gov/earth/earth-observatory/planetary-motion/) |
| G and astronomical units | JPL gives `G = 6.67430` times `10^-11` in SI, consistent with 6.674 at lesson precision, and lists the fixed AU and Julian-year definitions used in LX-01. [JPL constants](https://ssd.jpl.nasa.gov/astro_par.html) |
| Temperature and luminosity law | OpenStax section 5.2 states that blackbody energy flux is proportional to the fourth power of absolute temperature. Multiplying by spherical area gives the normalized luminosity law used here. [OpenStax 5.2](https://openstax.org/books/astronomy-2e/pages/5-2-the-electromagnetic-spectrum) |

The cannonball explanation is physically sound. Its exact attribution in the lesson's Sources section needs bibliographic care. Carnegie associates its illustrated example with the later *Treatise of the System of the World*, using a 1731 copy. The Smithsonian's indexed 1728 catalogue entry could not be fully opened, so I have not certified the first-publication date of that illustration. [Carnegie's illustrated explanation](https://cosmology.carnegiescience.edu/timeline/1687/orbit-of-the-moon.html)

### Renumbered references

The brief says nine changes. Read-only inspection of commit `28f7a9fa` identifies **ten changed sentences** in the named earlier lessons. All ten point to appropriate subjects in `book/data/learn-units.yml`. Some target units are planned entries.

| Earlier lesson and line | Target | Checked subject |
| --- | --- | --- |
| 1.1, 71 | Lesson 2.3 | Unequal eclipse depths |
| 1.1, 131 | Unit 4 | Eccentric eclipsing binaries |
| 1.2, 51 | Lesson 2.4 | Dilution |
| 1.2, 76 | Lesson 2.4 | Dilution |
| 1.3, 82 | Unit 6 | Removing slow changes |
| 1.4, 41 | Unit 6 | Transit-shape handling in searches |
| 1.4, 81 | Unit 4 | Circumbinary transits |
| 1.4, 139 | Unit 6 | Injection and detection sensitivity |
| 2.1, 86 | Unit 4 | Stability limit |
| 2.2, 66 | Unit 4 | Moving stars and varying transit duration |

### OpenStax wording spot-check

**CONFIRMED limited negative result.** Downloaded chapter sections **3.2, 3.3, 3.4, 5.1 and 5.2**. Compared each of the three lesson bodies against all five sections after case and punctuation normalization. There are **zero shared eight-word sequences in 15 comparisons**. Read the relevant gravity, orbit, inverse-square and radiation passages as well. No copied sentence was found in this sample. The chapter examples use different values and their prose differs from the lessons.

This does not establish originality against every OpenStax chapter or identify close paraphrases. The pages' attribution section confirms CC BY-NC-SA. The comparison is a wording spot-check with that limited scope. [Chapter 3 sample](https://openstax.org/books/astronomy-2e/pages/3-3-newtons-universal-law-of-gravitation), [chapter 5 sample](https://openstax.org/books/astronomy-2e/pages/5-2-the-electromagnetic-spectrum)

## What I did NOT check

- Full three-body integrations, parameter posteriors, actual-epoch eclipse geometry, or a fitted limb-darkening decomposition of either depth contrast.
- A new reduction of raw FITS data. The 2,655 ppm check used the existing published-system plot. Earlier brief 018's raw-data result agrees.
- Target-specific CHARA sensitivity, scheduling or observability. The resolution comparison tests the lesson's universal telescope assertion.
- Every OpenStax sentence, chapter 3.1, 3.5 and later sections, or every chapter 5 section. Close-paraphrase detection was outside the wording comparison.
- The original historical texts for Galileo, Huygens or the cannonball illustration. Institutional sources support the broad history, while the illustration attribution remains uncertified.
- A fully opened primary local-star census. The Collins paper and a RECONS-authored review were located, but full-text access failed. NASA's opened material supports the broader stellar-population statement.
- Browser answer handling, mobile layout, accessibility, the book build or live pages. Python checks cover the declared answers, tolerances, hints and arithmetic.
- Independent review of my script. This is producer verification. Recorded hashes identify the inputs and downloaded bytes.

## STOP SIGNS hit

No scientific fence or frozen-code stop was needed. Research used lesson assets and public references. The failed PDF request is disclosed above. Several source pages returned access errors, and equivalent primary HTML supplied the central numerical evidence. No package installation was needed.

## QUEUE PROPOSALS

All findings belong to **FIX, Tree node 4.1**. Claude can group LX-01 and LX-02 as lesson 2.5 scientific corrections, LX-03 and LX-07 as answer-feedback and arithmetic corrections, and LX-04, LX-05 and LX-08 as wording corrections. LX-06 calls for qualifying the causal sentence, with a full transit fit only if a quantitative attribution is wanted. Claude files the entries.

## IDEAS

None beyond the requested fact-check.

## Disagreements with Claude

The claim of an exactly unit Kepler coefficient is contradicted by the defined-unit calculation. The assertion that all telescopes are unable to resolve this angular scale is contradicted by CHARA's published resolution. The evidence and proposed wording are recorded above for Claude's review.

## Questions for Ahmed

None. I used the brief's read-only interpretation and checked all ten reference changes found in the commit.

## Downloads and usage

Downloaded eight HTML pages with Python into the new `data/astra/022/sources/` folder, **3,037,139 bytes total**. Three are arXiv primary papers or resolutions and five are the OpenStax wording sample. `sources/manifest.json` records each URL, size and SHA-256. HTML and extracted text remain under the private task-output directory. A subsequent attempt to save the RECONS-authored Annual Reviews page returned HTTP 403. Its `sources-review` folder contains only a failure record.

Predicted 30 five-hour points and 6 weekly points. Actual usage is unavailable in this headless session. Fourteen web calls used the fourteen-call cap. The report and usage entry disclose this missing measurement. Lesson learned from the check is that a maximum-depth approximation and a window-averaged observed depth require matching definitions before interpreting their difference.

**Next** Claude reviews these eight findings to decide the lesson corrections, estimated at about 1 weekly point. This step belongs to Claude.
