"""One check for leads_export: python test_leads.py (silent on success)."""
import pathlib, tempfile
import leads_export as L


def ev(kind, tier, snr, center, product="PDCSAP"):
    return dict(kind=kind, tier=tier, snr=snr, center=center, product=product, depth_ppm=1000, dur_h=6, flags=[])


def grp(tic, sec, evs):
    return dict(tic=tic, sector=sec, evs=evs, mtime=0, files={})


card = lambda tic, sec, e, blind, mt: dict(tic=tic, sector=sec, product=e["product"], tier=e["tier"], snr=e["snr"], depth=1000, dur=6, x=[0], y=[0], gaps=[])
A = {1: grp(10, 1, [ev("real", "1A", 9, 5.0), ev("real", "1A", 8, 5.3), ev("real", "1A", 7.5, 9.0), ev("flip", "1A", 8, 2.0), ev("real", "2", 12, 3.0)]),
     2: grp(99, 1, [ev("real", "1A", 20, 1.0)]),                      # a known host
     3: grp(10, 2, [ev("real", "1B", 7.2, 4.0)])}
ROWS = [(r, e) for r in A.values() for e in r["evs"]]
d = pathlib.Path(tempfile.mkdtemp())
out = L.build(d, A, {}, True, False, card, {}, known={99}, rows=ROWS)
real = {s["label"][:4]: (s["real"], s["flip"]) for s in out["stages"]}
assert real["Dips"] == (6, 1) and real["Kept"] == (5, 1) and real["Conf"] == (4, 1), real     # finished run counts events like the scorecard
assert real["Lead"] == (1, 1), real                                                           # one lead per star: star 10 (strongest 9, two distinct dips); star 99 is known
assert out["known"] == 1 and [c["id"] for c in out["cards"]] == ["L1"] and out["cards"][0]["others"] == [2] and out["cards"][0]["events"] == 2
assert out["verdict"].startswith("Finished: 1 lead for 2 or 3 more checks"), out["verdict"]
assert "do not outnumber" in L.verdict(True, False, 2, 1, 1) and L.verdict(True, False, 0, 5, 1).startswith("Finished: no leads")
assert L.verdict(False, False, 2, 5, 1).startswith("Not finished")
b = L.build(d, A, {}, True, True, card, {}, known={99}, rows=ROWS)                                        # blind: pooled counts, no kinds, no cards, no known count
assert all("real" not in s for s in b["stages"]) and b["cards"] == [] and b["known"] is None and b["verdict"].startswith("Finished. Counts only")
sealed = pathlib.Path(tempfile.mkdtemp()) / "sealed_x"; sealed.mkdir()
if not L.SCORECARD.exists():                                                                   # the latch: a sealed folder is blind even when asked not to be
    assert L.build(sealed, A, {}, True, False, card, {}, known={99}, rows=ROWS)["blind"] is True
print("test_leads ok")
