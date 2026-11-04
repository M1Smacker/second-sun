# CENSUS: how Second Sun works from now on (4 Nov 2026)

Agreed by Ahmed on 4 Nov 2026 after the G3 result. The name was my choice; his words: "you should go with census... since you're the second key, I give you that advantage that you have control over things you like." This file is the reference for the new direction. Nothing in it has been built yet.

## 1. Why we are changing
- Three hunts (G1, G2, G3) searched 2,056 stars and 19,464 star-sectors. All three gave clean nulls. The method is careful (frozen versions, upside-down noise control, planted-dip completeness, preregistration), but the fuel was small.
- G3 showed that more faint stars is not the answer: 612 faint stars were worth about 18 to 20 "star-equivalents" for a Kepler-16-size planet, against about 87 for 594 bright G2 stars (`horizon-first-reach-2026-11-03.md`).
- Ahmed: "change or quit, so we evolve." Agreed. Staying on small catalogue slices will keep giving nulls that teach little.

## 2. The core insight
- The bottleneck is the published lists, not the sky and not the clock. TESS moves to a new strip of sky every 27 days and has covered most of the sky, many parts several times. The main 2-minute eclipsing-binary list (Prsa et al. 2022, MAST TESS-EBs v1.0) only covers sectors 1 to 26 and was last updated 29 Jun 2022 (CONFIRMED on the MAST page). About four years of later data have no equivalent list.
- So there are bright, long-period eclipsing binaries in TESS data that no list names, and that nobody has searched with our method. Finding them first is our opening.
- Rough size (my estimate, NOT measured): stars with Tmag about 13.5 or brighter are on the order of 10 to 20 million; perhaps 1 to 2 in 100 are eclipsing binaries TESS could catch; a fraction of those are slow, well-separated binaries. Plausible targets: tens of thousands. Gaia DR3 lists 2,184,477 eclipsing-binary candidates (CONFIRMED, Mowlavi et al. 2023), most of them faint.

## 3. The goal of Census
- **The most stars where a planet would actually show, not the most stars.** Agreed by Ahmed. Size target: well over 1,000 stars, likely several thousand, chosen by value.
- One flagship search, done once, on a list nobody else has, with a Petrova (Vesper) improved and audited for it.

## 4. The stages (each step shown to Ahmed and taught before it is done)
1. **Teach** how eclipsing binaries are found in light curves (first lesson, 4 Nov).
2. **Census list (idea 1; groundwork 4 Nov night: `CENSUS-STEP1-COUNTS`, `CENSUS-STEP2-RESEARCH`: 364,656 new stars, fetching is about 3 files a second and 1.8 MB a file from a public AWS bucket, so one pilot of the 5,193 long-coverage stars is about 7 hours and 135 GB):** find eclipsing binaries ourselves in TESS 2-minute data after sector 26, then FFI data; cross-check with Gaia DR3 and the TESS Ten Thousand Catalog; vet with the usual checks (secondary eclipse, odd-even depths, nearby-star blends). Three-week rule lifted for this one system (Ahmed, 4 Nov).
3. **Rank by value (idea 2):** before any big download, score every candidate binary by Horizon reach (with the transit-geometry factor, T138) TIMES an occurrence prior by binary period (about zero below 7 days, Hamers 2016; Q2 of 4 Nov night showed reach alone favours the wrong stars: short binaries) and keep the best few thousand.
4. **Petrova upgrades that pay (idea 3):** recover the 14% of reads with no safe windows; settle the false-alarm check (missed its mark twice: 8.91 and 9.34 per 1,000 against 8); raise recovery of TOI-1338 b-size dips (6% in G3). Plus the fix-list and build-list items that Census needs.
5. **New search idea to research (idea 4; literature check done 4 Nov night, `CENSUS-IDEA4-LITERATURE-2026-11-04.md`: the concept is already published on Kepler data, STANLEY and Windemuth 2019; only the TESS sparse single-event linking with an upside-down control may be open, so borrow and extend):** circumbinary transits shift in time and depth because the stars move. Combine dips that fit one possible planet orbit across all sectors instead of judging each dip alone. Literature check first (some groups do versions of this); call it ours only if it is.
6. **One big audit of Petrova,** then freeze a new version.
7. **Preregister Census** (rules written before any result), prepare the Search window (standing rule), then the one search on Ahmed's explicit go.

## 5. How we work from now on
- Ahmed is in the loop at every step: I explain or teach each step before doing it, especially anything not in the learning course. No plan, research and execute on my own for Census.
- Original means a new combination finished properly, not a claim that nobody ever tried something. Any "first" claim is checked against the literature before we say it.
- Take good practice from others (Rabtsevich included) when it helps Petrova; do not copy for the sake of it.
- Patience and discipline are the advantage: months of unglamorous, self-checked work that professionals rarely do.
- Unchanged: frozen versions, one-shot tests, counts first, named leads private until two keys and Ahmed's yes, labels CONFIRMED/LIKELY/UNCERTAIN/NOT TESTED, usage logged.
- It may take months. That is accepted.

## 6. Open decisions for Ahmed
- When to start building the Census list (after the first lesson).
- The Petrova rename (Option A) can ride along with the upgrade stage.
- Whether the Learning Space and Keystone wait until after Census stage 2.
