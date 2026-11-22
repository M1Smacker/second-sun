# RS-043: what Gaia DR4 (2 December 2026) gives Census (Claude, 22 Nov 2026, 11:27 pm)

**Plain line: found something useful for the next fork. Gaia DR4 is still dated 2 December 2026 and will publish a catalogue of about 2.39 million eclipsing binaries with periods and geometric models. That is the list Census lacks (the Prsa TESS list stops at Sector 26, so our own list was going to be built from TESS light).**

Sources, read 22 Nov 2026 11:25 pm (CONFIRMED on the pages themselves):
- ESA release scenario, https://www.cosmos.esa.int/web/gaia/release: "Gaia DR4 (based on 66 months of data) 2 December 2026".
- ESA DR4 content table (last update 14 September 2026, "changes can be expected"), https://www.cosmos.esa.int/web/gaia/dr4: `vari_eclipsing_binary`, "Eclipsing binaries resulting from variability analysis", 2,392,500 rows, 419 MB; `nss_two_body_orbit` covers astrometric, spectroscopic and eclipsing binary orbit solutions; `epoch_photometry` 7.2 TB (about 100 epochs per source: too sparse to see planet transits, useful for eclipse periods); `vari_planetary_transit` 1,007 rows.

## What it changes (LIKELY)
1. **Census target list:** cross-match DR4 eclipsing binaries (period, eclipse widths, depths) to TESS stars with 2-minute or FFI light after Sector 26, then apply our value ranking (Horizon reach map, G2-type cut). This replaces much of "build our own EB list from TESS" (T136, T139) with a 419 MB table query. Our own TESS ephemerides stay needed for eclipse timing (FIX 94, RS-026).
2. **Mask timing:** DR4 periods over 66 months could sharpen eclipse ephemerides for the mask (node 1.4), a pool of up to 5.3 points that the catalogue drift term currently over-blanks (FIX 101). To test after release, on design stars only.
3. **Nothing to do before 2 December** except preparing the query and the cross-match plan; contents may still change.
Filed on the Tree, node 2.1 (T153). Waits for Ahmed's fork decision after D1.