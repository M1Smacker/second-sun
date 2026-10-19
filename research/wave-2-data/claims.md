# Wave 2 claims (D-numbers)

| # | Claim | Source | Label | Checked |
|---|---|---|---|---|
| D1 | TESS: 4 cameras of 24°×24° (24°×96° total); 4 CCDs of 2048×2048 each; ~21.1″ pixels; 10.5 cm entrance pupil | Sullivan, Winn+ 2015, arXiv:1506.03845 (quoted via search summary) | LIKELY | 2026-10-19 |
| D2 | 13.7-d orbit; each star observed for 1 month to 1 year depending on ecliptic latitude, longest near the ecliptic poles; TESS stars 10-100× brighter than Kepler's | Ricker, Winn+ 2014, arXiv:1406.0151 (abstract fetched) | VERIFIED | 2026-10-19 |
| D3 | FFI cadence 30 min (S1-26), 10 min (S27-55), 200 s from S56 (Sept 2022) | wave 1c DRN text; MIT TESS observations page via search | VERIFIED | 2026-10-19 |
| D4 | S98 SPOC 2-min LC of TIC 260128333 = 40,157 cadences; 20-s LC = 241,046 cadences | downloaded files (handson_results.csv) | VERIFIED | 2026-10-19 |
| D5 | Downlinks every ~7 d since EM2 (3 shorter gaps per sector); perigee gaps; flagged cadences | TIaRA TESS 1, arXiv:2402.07800 (search summary) | LIKELY | 2026-10-19 |
| D7-D15 | Measured sizes per star-sector: QLP 0.66 MB; TESS-SPOC 1.15 MB; SPOC 2-min LC 1.89 MB (4.16 MB double S98); 20-s LC 24.8 MB (double); TPF 101 MB (double); TESScut 15×15 49.8 MB (S82) / 110 MB (S98); TGLC 30-min 0.055 MB. Download times 4.6-70.9 s | handson_results.csv | VERIFIED | 2026-10-19 |
| D16 | TESS quality bits; lightkurve DEFAULT / HARD / HARDEST masks = 17087 / 24319 / 65535 | lightkurve 2.6.0 source, `TessQualityFlags` | VERIFIED | 2026-10-19 |
| D17 | Momentum dumps every 2-6 d; since S56 generally flanked by ≳0.2-d gaps | TESSILATOR, arXiv:2407.18761 (search summary) | LIKELY | 2026-10-19 |
| D18 | Earth/Moon scattered light: 1-d background oscillation, end-of-orbit upturns | HEASARC condensed DRNs (S1-S2) via search | LIKELY | 2026-10-19 |
| D19 | DRN index: latest is DRN 142 = Sector 104; PDF path pattern | archive.stsci.edu/tess/tess_drn.html (fetched) | VERIFIED | 2026-10-19 |
| D20 | lightkurve / astroquery / TESScut downloads work on this PC after the truststore fix | hands-on | VERIFIED | 2026-10-19 |
| D21 | AWS `s3://stpubdata/tess` (us-east-1): no account, public domain, monthly updates; anonymous HTTPS listing works | registry.opendata.aws/mast-tess (fetched) + hands-on listing | VERIFIED | 2026-10-19 |
| D22 | HLSPs (TESS-SPOC, QLP, TGLC) under `stpubdata/mast/hlsp/` | AWS registry pages via search | LIKELY | 2026-10-19 |
| D25 | Kepler noise on quiet solar-type stars ~50% above the pre-launch target | Gilliland+ 2011, arXiv:1107.5207 (abstract) | VERIFIED (abstract) | 2026-10-19 |
| D26 | TESS covered the Kepler CBP hosts in S14-15, 26, 40-41, 53-56, 73-76, 80-83; nothing after S83 | wave 1c ground_truth_out.md | VERIFIED | 2026-10-19 |
| D28 | Gaia DR4 release 2 Dec 2026, 12:00 CET; archive down from 25 Nov 2026 | ESA Gaia news 2026 (item dated 8 Oct 2026, fetched) | VERIFIED | 2026-10-19 |
| D29 | DR4: epoch data for all sources, 66 months (Jul 2014 - Jan 2020), ~400 TB | ESA DR4 content page via search | LIKELY | 2026-10-19 |
| D30 | Useful DR3 tables: gaia_source (RUWE), nss_two_body_orbit, vari_eclipsing_binary, astrophysical_parameters | memory + wave 1c (vari_eclipsing_binary count verified there) | LIKELY | 2026-10-19 |
| D31 | ZTF light-curve API: no account for public data; Kepler-16 → 970 g-band points, MJD 58204-60948; comma-separated BANDNAME; radius ≤ 0.1667°; >1,000 objects → HATS notebook | IRSA API docs (fetched) + hands-on | VERIFIED | 2026-10-19 |
| D32 | ASAS-SN Sky Patrol v2: 111 M targets; Python client `skypatrol`; up to 1 M light curves | Hart+ 2023, arXiv:2304.03791 (search summary) + GitHub README | LIKELY | 2026-10-19 |
| D33 | ATLAS forced photometry requires registration + token | client docs (TOM Toolkit, sdapy) via search | LIKELY | 2026-10-19 |
| D34 | Kepler-16 (Tmag 10.94), S82, after 12-h flatten + 4σ clip: 1-hr CDPP 236 ppm (SPOC 2-min), 279 ppm (TESS-SPOC 200 s), 293 ppm (QLP 200 s) | hands-on (lightkurve estimate_cdpp) | VERIFIED (crude method: eclipses not explicitly masked) | 2026-10-19 |
| D35 | Avast Web/Mail Shield re-signs HTTPS (issuer "Avast Web/Mail Shield Root"); certifi-based `requests` fails; truststore fixes it | hands-on (peer-certificate inspection) | VERIFIED | 2026-10-19 |
