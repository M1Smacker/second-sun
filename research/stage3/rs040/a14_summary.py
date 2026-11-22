"""RS-040 A14 summary (written before the full run's result was read). Per rule (maj, nn1): untouched alarms per 100 days in old and extra
time, both arms; planted crossings detected at notch 5 in old and extra time; the lead rule from a14_windows.py."""
import json, collections
H = "D:/second-sun/data/rs039"
S = collections.defaultdict(lambda: collections.Counter())
for c in ("g2", "g3"):
    for l in open(f"{H}/a14-{c}.jsonl", encoding="utf-8"):
        if not l.strip(): continue
        for f in json.loads(l)["files"]:
            s = S[f["rule"]]; s["files"] += 1
            for k in ("days_old", "days_extra", "r_old", "r_extra", "u_old", "u_extra"): s[k] += f[k]
            for p in f["planted"]: s[f"n_{p['where']}"] += 1; s[f"hit_{p['where']}"] += p["hit"]
for rule, s in S.items():
    rate = lambda a, w: 100 * s[f"{a}_{w}"] / s[f"days_{w}"] if s[f"days_{w}"] else float("nan")
    det = lambda w: s[f"hit_{w}"] / s[f"n_{w}"] if s[f"n_{w}"] else float("nan")
    print(f"{rule}: files {s['files']}, days old {s['days_old']:.0f}, extra {s['days_extra']:.0f} ({100*s['days_extra']/max(1,s['days_old']+s['days_extra']):.1f}% more light)")
    print(f"  alarms per 100 d real: old {rate('r','old'):.2f}, extra {rate('r','extra'):.2f} | upside-down: old {rate('u','old'):.2f}, extra {rate('u','extra'):.2f}")
    print(f"  planted crossings: old {s['n_old']} detected {det('old'):.3f}; extra {s['n_extra']} detected {det('extra'):.3f}")
    if rule == "nn1":
        print("  (nn1 has no old time: judged on extra-time rates against the maj files' old-time rates)")
    else:
        ok = rate('r','extra') <= 1.5 * rate('r','old') and rate('u','extra') <= 1.5 * rate('u','old') and det('extra') >= 0.8 * det('old')
        print(f"  lead for the Petrova 2.0 bench: {ok}")
if "nn1" in S and "maj" in S:
    m, n = S["maj"], S["nn1"]
    r_ok = 100 * n["r_extra"] / max(1e-9, n["days_extra"]) <= 1.5 * 100 * m["r_old"] / m["days_old"]
    u_ok = 100 * n["u_extra"] / max(1e-9, n["days_extra"]) <= 1.5 * 100 * m["u_old"] / m["days_old"]
    d_ok = (n["hit_extra"] / n["n_extra"] if n["n_extra"] else 0) >= 0.8 * (m["hit_old"] / m["n_old"] if m["n_old"] else 1)
    print(f"nn1 lead for the Petrova 2.0 bench: {r_ok and u_ok and d_ok}")
