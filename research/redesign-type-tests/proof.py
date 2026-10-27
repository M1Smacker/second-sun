import sys, os, json, glob, base64, unicodedata
sys.stdout.reconfigure(encoding='utf-8')
from fontTools.ttLib import TTFont
from fontTools import subset
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(HERE, 'dl')
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
used = json.load(open(os.path.join(HERE, 'glyphs_used.json'), encoding='utf-8'))
USED = [u['ch'] for u in used]
ASTRO = ['⊙', '⊕', '☉', '♃']
ALL = USED + ASTRO

def files(fam, pat='*.woff2'):
    return sorted(glob.glob(os.path.join(DL, fam, pat)))

def normal_files(fam):
    return [p for p in files(fam) if 'italic' not in os.path.basename(p)]

# ---------- 1. Cut the symbol subsets ----------
LATIN1_OK = set('·×÷°§±−²³̄')   # every text face draws these
src_math = files('notomath')[0]
fm = TTFont(src_math)
cm_math = fm.getBestCmap()
want = [ch for ch in ALL if ch not in LATIN1_OK and ord(ch) in cm_math]
missing_in_math = [ch for ch in ALL if ch not in LATIN1_OK and ord(ch) not in cm_math]
print('symbol subset wants %d chars; not in Noto Sans Math: %s' % (len(want), ' '.join('%s(U+%04X)' % (c, ord(c)) for c in missing_in_math)))

def cut(src, chars, dest, keep_hint=False):
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = []
    opts.hinting = keep_hint
    opts.notdef_outline = False
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    opts.drop_tables += ['DSIG', 'MATH']
    opts.glyph_names = False
    f = subset.load_font(src, opts)
    s = subset.Subsetter(opts)
    s.populate(unicodes=[ord(c) for c in chars])
    s.subset(f)
    subset.save_font(f, dest, opts)
    return os.path.getsize(dest)

sz_sym = cut(src_math, want, os.path.join(OUT, 'ss-symbols.woff2'))
print('ss-symbols.woff2 (Noto Sans Math subset): %d chars, %d bytes' % (len(want), sz_sym))
# the one glyph the book uses that Noto Sans Math lacks
cross = [ch for ch in missing_in_math]
sym2_all = files('notosym2')
sz_x = 0
cross_src = None
for p in sym2_all:
    cmx = TTFont(p).getBestCmap()
    if all(ord(c) in cmx for c in cross if c != '♃'):
        cross_src = p
if '✗' in cross:
    p = [q for q in sym2_all if ord('✗') in TTFont(q).getBestCmap()][0]
    sz_x = cut(p, ['✗'], os.path.join(OUT, 'ss-cross.woff2'))
    print('ss-cross.woff2 (Noto Sans Symbols 2, U+2717 only): %d bytes' % sz_x)
# Jupiter, not used anywhere today
if '♃' in cross:
    p = [q for q in files('notosym') if ord('♃') in TTFont(q).getBestCmap()]
    if p:
        sz_j = cut(p[0], ['♃'], os.path.join(OUT, 'ss-jupiter.woff2'))
        print('ss-jupiter.woff2 (Noto Sans Symbols, U+2643 only): %d bytes' % sz_j)

# re-open the cut files and prove the glyphs are really in them
chk = TTFont(os.path.join(OUT, 'ss-symbols.woff2')).getBestCmap()
assert all(ord(c) in chk for c in want), 'subset lost glyphs'
print('verified: all %d glyphs present in the cut file' % len(want))

# ---------- 2. Outlines for the proof table ----------
COLS = [
    ('atkinson', 'Atkinson Next'),
    ('literata', 'Literata'),
    ('plexsans', 'Plex Sans'),
    ('plexmono', 'Plex Mono'),
    ('inter', 'Inter'),
    ('sym', 'Noto Sans Math (cut)'),
]
def load_cols():
    cols = {}
    for key, label in COLS:
        if key == 'sym':
            cols[key] = [os.path.join(OUT, 'ss-symbols.woff2')]
            if os.path.exists(os.path.join(OUT, 'ss-cross.woff2')): cols[key].append(os.path.join(OUT, 'ss-cross.woff2'))
        elif key in ('plexsans', 'plexmono'):
            cols[key] = [p for p in normal_files(key) if '-400-' in p]
        elif key == 'literata':
            cols[key] = [p for p in normal_files(key) if '-wght-' in p]
        else:
            cols[key] = normal_files(key)
    return cols
cols = load_cols()
loaded = {k: [TTFont(p) for p in v] for k, v in cols.items()}

def outline(chfont, cp):
    for f in chfont:
        cmap = f.getBestCmap()
        if cp in cmap:
            gs = f.getGlyphSet()
            gname = cmap[cp]
            upm = f['head'].unitsPerEm
            adv = f['hmtx'][gname][0]
            pen = SVGPathPen(gs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
            sc = 100.0 / upm
            x0 = (100.0 - adv * sc) / 2.0
            tp = TransformPen(pen, (sc, 0, 0, -sc, x0, 80.0))
            gs[gname].draw(tp)
            return pen.getCommands(), round(adv / upm, 3)
    return None, None

proof = {'cols': [{'key': k, 'label': l} for k, l in COLS], 'rows': []}
cover = {k: 0 for k, _ in COLS}
for ch in ALL:
    row = {'ch': ch, 'cp': 'U+%04X' % ord(ch), 'name': unicodedata.name(ch).title(), 'used': ch in USED,
           'n': next((u['n'] for u in used if u['ch'] == ch), 0), 'cells': {}}
    for k, _ in COLS:
        d, adv = outline(loaded[k], ord(ch))
        row['cells'][k] = {'d': d, 'adv': adv}
        if d is not None: cover[k] += 1
    proof['rows'].append(row)
proof['cover'] = cover
proof['n_used'] = len(USED); proof['n_astro'] = len(ASTRO)
json.dump(proof, open(os.path.join(OUT, 'proof.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('coverage of %d used + %d astro characters:' % (len(USED), len(ASTRO)))
for k, l in COLS:
    nu = sum(1 for r in proof['rows'] if r['used'] and r['cells'][k]['d'] is not None)
    na = sum(1 for r in proof['rows'] if not r['used'] and r['cells'][k]['d'] is not None)
    print('  %-22s used %2d/%d  astro %d/%d' % (l, nu, len(USED), na, len(ASTRO)))

# ---------- 3. Variable-font defaults, for the record ----------
for fam in ('atkinson', 'literata', 'plexsans', 'plexmono'):
    f = TTFont(normal_files(fam)[0])
    ax = [(a.axisTag, a.minValue, a.defaultValue, a.maxValue) for a in f['fvar'].axes] if 'fvar' in f else 'static'
    print(fam, ax, 'upm', f['head'].unitsPerEm, 'xHeight', getattr(f['OS/2'], 'sxHeight', None), 'capH', getattr(f['OS/2'], 'sCapHeight', None))

# ---------- 4. Who draws each character in a font chain ----------
def chain_draws(chain_keys, ch):
    for k in chain_keys:
        for f in loaded[k]:
            if ord(ch) in f.getBestCmap():
                return k
    return None
chains = {
    'today (Inter, Plex Mono)': ['inter'],
    'A reading: Atkinson > symbols': ['atkinson', 'sym'],
    'B reading: Literata > symbols': ['literata', 'sym'],
    'UI: Plex Sans > symbols': ['plexsans', 'sym'],
    'labels: Plex Mono > symbols': ['plexmono', 'sym'],
}
chain_rep = {}
for name, keys in chains.items():
    who = collections = {}
    drawn = {}
    unc = []
    for ch in ALL:
        k = chain_draws(keys, ch)
        if k is None: unc.append(ch)
        else: drawn[k] = drawn.get(k, 0) + 1
    chain_rep[name] = {'drawn_by': drawn, 'uncovered': unc}
    print('%-34s %s  not drawn by any file: %s' % (name, drawn, ' '.join(unc) or 'none'))
json.dump(chain_rep, open(os.path.join(OUT, 'chains.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
