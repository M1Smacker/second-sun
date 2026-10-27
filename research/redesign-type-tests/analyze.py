import sys, os, json, glob, collections
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
HERE = os.path.dirname(os.path.abspath(__file__))
used = json.load(open(os.path.join(HERE, 'glyphs_used.json'), encoding='utf-8'))
USED = [u['ch'] for u in used]
ASTRO = ['⊙', '⊕', '☉', '♃']   # circled dot, circled plus, sun, jupiter
ALL = USED + ASTRO
NAMES = {u['ch']: u['name'] for u in used}
import unicodedata
for a in ASTRO: NAMES[a] = unicodedata.name(a)

def cmap_of(path):
    f = TTFont(path)
    return set(f.getBestCmap().keys())

def style_of(fn):
    return 'italic' if 'italic' in fn else 'normal'

report = {}
for fam in sorted(os.listdir(os.path.join(HERE, 'dl'))):
    d = os.path.join(HERE, 'dl', fam)
    files = sorted(glob.glob(os.path.join(d, '*.woff2')))
    per = collections.defaultdict(dict)   # style -> {char: [(file,size)]}
    sizes = {}
    for p in files:
        fn = os.path.basename(p)
        sizes[fn] = os.path.getsize(p)
        cm = cmap_of(p)
        st = style_of(fn)
        for ch in ALL:
            if ord(ch) in cm:
                per[st].setdefault(ch, []).append(fn)
    report[fam] = {'files': sizes, 'cover': {st: {ch: v for ch, v in m.items()} for st, m in per.items()}}

# print coverage matrix for the normal style
print('Chars required: %d used by the book today + %d astronomy candidates' % (len(USED), len(ASTRO)))
fams = list(report)
print('%-9s' % 'char', *['%-9s' % f[:9] for f in fams])
for ch in ALL:
    row = []
    for f in fams:
        c = report[f]['cover'].get('normal', {})
        row.append('%-9s' % ('yes' if ch in c else '-'))
    print('%s U+%04X' % (ch, ord(ch)), *row)
print()
for f in fams:
    c = report[f]['cover'].get('normal', {})
    n_used = sum(1 for ch in USED if ch in c)
    n_ast = sum(1 for ch in ASTRO if ch in c)
    tot = sum(report[f]['files'].values())
    print('%-9s used %2d/%d  astro %d/%d   files %d  total %6.1f KB' % (f, n_used, len(USED), n_ast, len(ASTRO), len(report[f]['files']), tot / 1024))
json.dump(report, open(os.path.join(HERE, 'coverage.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
