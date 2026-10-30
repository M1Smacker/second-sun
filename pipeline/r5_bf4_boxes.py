"""Vesper study C5a follow-up: where do the upside-down tier-1 survivors sit once the 3 h box is gone? Aggregates only (upside-down events; no real event is read).
Question: did the survivors vanish with the 3 h box, or move to the next box (4 h)? Compares the baseline run with the bf4 run on each set.
Usage: python r5_bf4_boxes.py   (writes research\\stage3\\r5-bf4-boxes.txt)"""
import os, importlib
import dataset as DS

RUNS = {"g1": {"baseline-0.7.1": "fd788be04650", "bf4": "g1opt_35a004cf05b1", "bf4+c2": "g1opt_bff6de851f27"},
        "g2": {"baseline-0.7.1": "dev_73f62615e365", "bf4": "dev_03085648d90d", "bf4+c2": "dev_53de1d854920"}}
T1 = ["1A", "1L", "1B"]


def main():
    out = ["Vesper study C5a follow-up (30 Oct 2026): upside-down events at SNR 7 or more, all tiers (found) and tier-1 (survivors), by box length. Aggregates only."]
    for name, runs in RUNS.items():
        os.environ["SS_SET"] = name
        importlib.reload(DS)
        import stage3_core as C, stage3_report as R
        importlib.reload(C); importlib.reload(R)
        for label, run in runs.items():
            ev, meta = R.load(str(C.DS.RUNS / run / "groups"))
            F = ev[ev.primary & (ev.kind == "flip") & (ev.snr >= 7)]; S = F[F.tier.isin(T1)]
            f = lambda d: ", ".join(f"{int(k) if k == int(k) else k} h: {int(v)}" for k, v in d.dur_h.value_counts().sort_index().items())
            out.append(f"{C.DS.NAME} {label} (run {run}): upside-down found {len(F)} [{f(F)}]; tier-1 survivors {len(S)} [{f(S)}]")
    txt = "\n".join(out)
    print(txt)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "research", "stage3", "r5-bf4-boxes.txt"), "w", encoding="utf-8").write(txt + "\n")


if __name__ == "__main__":
    main()
