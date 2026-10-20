"""WCAG contrast for the book's design tokens (SITE-BLUEPRINT.md §4), measured, not eyeballed.
Text pairs need 4.5:1; UI boundaries (control borders) need 3:1. Exit code 1 on any failure."""
import sys

def lum(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]

def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)

T = {"dark": dict(bg="#0c1018", surface="#131a27", raised="#1a2233", line="#2a3448", text="#e6e8ee", text2="#aab1c0", text3="#7d8597", accent="#e2b45f", on_accent="#0c1018"),
     "light": dict(bg="#faf9f6", surface="#f1efe9", raised="#ffffff", line="#d9d5cb", text="#1a1e26", text2="#495160", text3="#6a7282", accent="#8a5a12", on_accent="#ffffff")}
fails = 0
for scheme, t in T.items():
    checks = [(f, b, 4.5) for f in ("text", "text2", "accent") for b in ("bg", "surface", "raised")]
    checks += [("text3", "bg", 4.5), ("on_accent", "accent", 4.5), ("text3", "surface", 3.0), ("text3", "raised", 3.0)]
    for f, b, need in checks:
        r = ratio(t[f], t[b])
        ok = r >= need
        fails += not ok
        print(f"{scheme:5s} {f:9s} on {b:7s} {r:5.2f}  need {need}  {'ok' if ok else 'FAIL'}")
header = ratio("#e6e8ee", "#131a27")   # header bar text, both schemes
print(f"header text on header bar {header:5.2f}  {'ok' if header >= 4.5 else 'FAIL'}")
fails += header < 4.5
sys.exit(1 if fails else 0)
