"""Compares a round saved by the browser (printed by `site_check.mjs eyesreal`) with the document the REAL cloud holds, field by field, then deletes the test document.
Usage: python eyes_e2e.py <path to the JSON line printed by eyesreal>"""
import json, sys
import eyes_firestore as F

res = json.load(open(sys.argv[1], encoding="utf-8-sig"))      # utf-8-sig: PowerShell 5.1 adds a byte-order mark to redirected files
local, dev = res["round"], res["device"]
print("browser reported sent:", res["sent"], "| status line:", res["statusText"][:140])
cloud = [r for r in F.list_rounds() if r["id"] == local["id"]]
ok = len(cloud) == 1
print("cloud holds exactly one copy of the round:", ok)
if ok:
    c = cloud[0]
    for k in ("v", "id", "mode", "source", "n", "t0", "t1", "status", "s"):
        same = c[k] == local[k]; ok &= same; print(f"  {k:7s} same as on the device: {same}")
    same = c["a"] == local["a"]; ok &= same; print(f"  a       all {len(local['a'])} answers identical (kind, truth, answer, right/wrong, time, look-backs, curve data): {same}")
    same = c["device"] == {"id": dev["id"], "label": dev["label"]}; ok &= same; print(f"  device  same: {same}")
    print("  answers on the device:", [e["ans"] for e in local["a"]], "| in the cloud:", [e["ans"] for e in c["a"]])
    print("  right/wrong/unsure on device:", [local['s'][k] for k in ('right', 'wrong', 'unsure')], "| in cloud:", [c['s'][k] for k in ('right', 'wrong', 'unsure')])
    print("test document deleted from the cloud:", F.admin_delete(local["id"]).status_code == 200)
print("END-TO-END PASS" if ok else "END-TO-END FAIL")
sys.exit(0 if ok else 1)
