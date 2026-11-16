# Work log X4: the "too faint" pool (Fable, 16 Nov 2026)

- 11:46 am. RS-037 puts 22.4 points of P in planets whose crossings are scored but never reach SNR 7. Nobody has measured whether that is physics (photon noise on faint stars) or the detector (slow wiggles left after detrending, depth eaten by detrending, a box that does not fit).
- Measurement fixed before running (`data/fable/f2/x4_faint.py`): for every planted crossing that reaches a score, plant the planet in the loaded light, run the frozen mask, detrend and box search, and record: best SNR over the ten box lengths; depth kept = measured box depth / planted depth at the nearest box length; noise against white = the search's noise for that box / (bin scatter / sqrt(bins in the box)).
- Ceilings to report: planets with some crossing at SNR 7+ today; the same if the noise were white (an upper bound nobody can reach); if a third of the excess noise were removed (a guess at what better detrending could do, labelled as a guess); if the full depth were kept.
- What would make the pool "physics": noise against white near 1 and depth kept near 1 for the faint crossings. What would make it "detector": noise against white well above 1.5 or depth kept well under 0.8.
- Smoke on 4 stars passed. Full run started in the background (g3 on 2 workers, then g2 on 3; the fresh bench generation holds 6 workers).
