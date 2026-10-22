"""Contrast check for the book's colour tokens (Ahmed asked for high contrast, 2026-10-23).
Reads the tokens from docs/assets/extra.css and fails if text or the accent drops below 7:1 on any surface
(tertiary text: 4.5:1). Run: python tools/test_contrast.py. The publish script runs it before every publish."""
import re
import sys
from pathlib import Path

CSS = (Path(__file__).resolve().parents[1] / "docs/assets/extra.css").read_text(encoding="utf-8")


def lum(h):
    ch = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def tokens(scheme):
    block = re.search(r'\[data-md-color-scheme="%s"\]\s*\{(.*?)\}' % scheme, CSS, re.S).group(1)
    return dict(re.findall(r"--ss-([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", block))


fails = []
for scheme in ("slate", "default"):
    t = tokens(scheme)
    for surface in ("bg", "surface", "raised"):
        for name, need in (("text", 7), ("text-2", 7), ("accent", 7), ("text-3", 4.5)):
            r = ratio(t[name], t[surface])
            if r < need:
                fails.append(f"{scheme}: {name} {t[name]} on {surface} {t[surface]} is {r:.1f}:1, need {need}:1")
    if ratio(t["on-accent"], t["accent"]) < 7:
        fails.append(f"{scheme}: button text on accent is {ratio(t['on-accent'], t['accent']):.1f}:1, need 7:1")
if fails:
    print("\n".join(fails))
    sys.exit(1)
print("contrast ok: text, secondary text and accent are at least 7:1 on every surface in both schemes")
