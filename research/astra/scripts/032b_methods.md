# 032b implementation choices, fixed before fitting

Use 032 measurement, alias resolution, product-error scales and v3 error model unchanged. G2 affected measurements come from 014's raw calibration-worker records. The seen control sample is the 53 usable primary tracks of 032, including its six catalogue disagreements. The held-out experiment is not a new test of those seen controls.

G3 eligibility requires at least three distinct sector group files among design-seen targets. Select exactly 60 with seed 2026112318 and 014's unchanged five-bin allocator. Record sample membership and bin counts before fitting. Do not replace selected stars that fail measurement, lack a width or have fewer than three measured sectors.

Measure all sectors with the unchanged code, then split measured primary or secondary times by sector. The largest TESS sector number with measurements is held out. The unchanged v3 linear fitter and usability rule receive only earlier-sector times. Its clipping pass must not remove held-out times. Predict their existing integer cycle labels, not the nearest wrapped cycle. H1 denominator is all selected primary tracks with at least three measured sectors, including failed training fits. H2 denominator is usable training fits. Empty denominators fail. Apply the median 0.25-width and maximum 0.5-width limits inclusively to every measured held-out eclipse.

Separately fit all measured sectors for catalogue agreement as in 032 and for any permitted Part B ephemerides. The full-sector fit must never enter held-out usability or predictions. Full-data eclipse discovery and template measurement are intentionally preserved from 032, as the brief requires. Thus the withheld information is the times used in the linear ephemeris fit; this is not a fully blind raw-flux prediction experiment.

Use the same 014 noise library and seed for the 30-case alias trap. Preserve all sample failures in counts; primary and secondary counts and five period bins are separate. G3 has no finite catalogue period errors, so combined-sigma period agreement is unavailable there. No catalogue-agreement threshold is used as a gate here. The recorded 032 FAIL remains unchanged.

Part B is allowed only if both judging sets pass H1, H2 and H3. A failure is terminal for Part B and cannot authorize tuning.
