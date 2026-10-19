# Wave 2 open questions

1. **Tmag distribution of the 2,920 Kepler EBs.** This decides how many have QLP/TESS-SPOC light curves versus needing DIY, and so the real G1 data budget (10-30 GB vs ~300 GB). Owner: wave 3 (already in its brief).
2. **Proposed rule change for TESScut cutouts:** keep the extracted light curves + settings, delete the cutouts (they're re-downloadable). Needs Ahmed's OK, because it changes the "keep raw data" decision.
3. ZTF multi-band: the first call asked for g,r but returned g only. Retest.
4. The ASAS-SN `skypatrol` client is untested; ATLAS needs an account (add to wave 5's account schedule).
5. AWS egress / cost for anonymous bulk reads: unverified.
6. The TESS planning-guide PDF (`data/wave-2/Guide-to-TESS-for-EM-planning.pdf`) uses custom font encoding. Extract it with a real PDF library to verify D1/D5 from the primary text.
7. Gaia DR3 table details (D30) are memory-level; verify against Gaia docs when building the vetting pipeline.
8. The CDPP measurement (D34) didn't mask Kepler-16's eclipses explicitly; redo it properly in wave 3.
