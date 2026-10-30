import json, os, glob
R = r"D:\second-sun\data\stage3_g2\sealed_5f73692944aa"
EP = {27: 2049.69, 30: 2142.40, 34: 2237.92, 37: 2331.00, 62: 2989.35, 65: 3084.82, 68: 3177.98, 89: 3743.62, 93: 3836.04, 96: 3931.42, 98: 4024.62}
for sec, ep in EP.items():
    row = []
    for sub in ("groups", "groups_sap"):
        p = os.path.join(R, sub, f"260128333_{sec}.json")
        if not os.path.exists(p):
            row.append(f"{sub}: no file"); continue
        g = json.load(open(p))
        near = [(e["kind"], e["product"], round(e["center"] - ep, 2), e["dur_h"], round(e["snr"], 1), e.get("tier")) for e in g["events"] if abs(e["center"] - ep) < 1.5]
        ms = [(m["product"], m["status"]) for m in g["meta"]]
        row.append(f"{sub}: {len(g['events'])} events in sector, near epoch {near}, products {ms}")
    print(sec, ep, *row, sep="\n   ")
