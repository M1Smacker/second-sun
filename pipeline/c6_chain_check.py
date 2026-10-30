"""v8 candidate c6: the switch built into the chain (stage3_report.apply_v7) must reproduce the offline C6 variant C numbers (c6_orbit_lock.py) on the frozen runs, and change nothing with the
switch off. Aggregates only (counts); no real event is opened. Usage: python c6_chain_check.py   (appends to research\stage3\c6-orbit-lock.txt)"""
import os, importlib
import dataset as DS, vopts as V

SETS = {"g1": "fd788be04650", "g2": "dev_73f62615e365"}
T1 = ["1A", "1L", "1B"]


def counts(name, on):
    os.environ["SS_SET"] = name; importlib.reload(DS)
    import stage3_core as C, stage3_report as R
    importlib.reload(C); importlib.reload(R)
    V.ON = frozenset({"c6"} if on else ())
    ev, _ = R.load(str(C.DS.RUNS / SETS[name] / "groups"))
    E = ev[ev.primary]
    return E, {k: int((E.tier.isin(T1) & (E.kind == k)).sum()) for k in ("real", "flip")}


out = ["", "c6 built into the chain (stage3_report.apply_v7, 30 Oct 2026), frozen runs re-loaded with the switch off and on:"]
for n in SETS:
    E0, a = counts(n, False); E1, b = counts(n, True)
    same = "orbit_lock" not in E0 and E0.tier.equals(E1.tier.where(~E1.orbit_lock, E0.tier))
    out.append(f"  {n}: tier-1 real {a['real']} -> {b['real']}, upside-down {a['flip']} -> {b['flip']}; locked events {int(E1.orbit_lock.sum())} on {E1[E1.orbit_lock].tic.nunique()} stars; "
               f"switch off adds no column and every unlocked event keeps its tier: {same}")
V.ON = frozenset()
print("\n".join(out)); open("../research/stage3/c6-orbit-lock.txt", "a", encoding="utf-8").write("\n".join(out) + "\n")
