import sys; sys.stdout.reconfigure(encoding="utf-8")
import os, sys, collections, unicodedata, json
root_repo = sys.argv[1]
c = collections.Counter(); files = collections.defaultdict(set)
for root in ['book/docs', 'book/data', 'book/progress', 'book/overrides']:
    for dp, dn, fn in os.walk(os.path.join(root_repo, root)):
        if 'assets' + os.sep + 'fonts' in dp:
            continue
        for f in fn:
            if f.endswith(('.md', '.yml', '.yaml', '.html', '.js', '.css', '.csv')) and not f.endswith('.min.js'):
                p = os.path.join(dp, f)
                try:
                    t = open(p, encoding='utf-8').read()
                except Exception:
                    continue
                for ch in t:
                    if ord(ch) > 127:
                        c[ch] += 1; files[ch].add(f)
out = []
for ch, n in c.most_common():
    out.append({'cp': ord(ch), 'ch': ch, 'n': n, 'files': len(files[ch]), 'name': unicodedata.name(ch, '?')})
    print(f"U+{ord(ch):04X} {ch} {n:6d} files={len(files[ch]):3d} {unicodedata.name(ch,'?')}")
print(len(c), 'distinct non-ASCII')
json.dump(out, open(os.path.join(os.path.dirname(__file__), 'glyphs_used.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
