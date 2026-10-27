import html as _h
import os, sys, json, glob
sys.stdout.reconfigure(encoding='utf-8')
from lib import *

OUTDIR = os.path.join(HERE, '..', 'redesign-canvas')
PUB = os.path.join(OUTDIR, 'project')
LOC = os.path.join(OUTDIR, 'local')
os.makedirs(PUB, exist_ok=True); os.makedirs(LOC, exist_ok=True)
H = jload(os.path.join(HERE, 'heights.json'), {})

def kb(p): return os.path.getsize(p) / 1024.0
def dlf(fam, pat): return glob.glob(os.path.join(DL, fam, pat))[0]
BOOKF = 'D:/second-sun/book/docs/assets/fonts/'
SZ = {
 'sym': kb(os.path.join(OUT, 'ss-symbols.woff2')), 'cross': kb(os.path.join(OUT, 'ss-cross.woff2')),
 'inter_n': kb(BOOKF + 'inter-latin-wght-normal.woff2'), 'inter_i': kb(BOOKF + 'inter-latin-wght-italic.woff2'),
 'mono4_today': kb(BOOKF + 'ibm-plex-mono-latin-400-normal.woff2'), 'mono5_today': kb(BOOKF + 'ibm-plex-mono-latin-500-normal.woff2'),
 'atk_n': kb(dlf('atkinson', '*latin-wght-normal.woff2')), 'atk_i': kb(dlf('atkinson', '*latin-wght-italic.woff2')),
 'lit_n': kb(os.path.join(DL, 'literata', 'literata-latin-wght-normal.woff2')), 'lit_i': kb(os.path.join(DL, 'literata', 'literata-latin-wght-italic.woff2')),
 'lit_g': kb(os.path.join(DL, 'literata', 'literata-greek-wght-normal.woff2')),
 'ps4': kb(os.path.join(DL, 'plexsans', 'ibm-plex-sans-latin-400-normal.woff2')), 'ps6': kb(os.path.join(DL, 'plexsans', 'ibm-plex-sans-latin-600-normal.woff2')),
 'pm4': kb(os.path.join(DL, 'plexmono', 'ibm-plex-mono-latin-400-normal.woff2')),
 'nsm_full': kb(os.path.join(DL, 'notomath', 'noto-sans-math-latin-400-normal.woff2')),
}
def f1(x): return '%.1f' % x
tot_today = SZ['inter_n'] + SZ['inter_i'] + SZ['mono4_today'] + SZ['mono5_today']
tot_A = SZ['atk_n'] + SZ['atk_i'] + SZ['ps4'] + SZ['ps6'] + SZ['pm4'] + SZ['sym'] + SZ['cross']
tot_B = SZ['lit_n'] + SZ['lit_i'] + SZ['lit_g'] + SZ['ps4'] + SZ['ps6'] + SZ['pm4'] + SZ['sym'] + SZ['cross']
print('payload KB today %.1f  A %.1f  B %.1f' % (tot_today, tot_A, tot_B))

FACE = {'A': 'Atkinson Hyperlegible Next', 'B': 'Literata'}

def frame(face, size, inner, extra=''):
    cls = 'frame wide' if size == 'pcw' else 'frame'
    w = '540 px column' if size == 'pcw' else '390 px phone'
    return ('<div class="%s opt%s"><div class="fh"><span>%s \u00b7 %s</span><span>%s</span></div><div class="fb">%s%s</div></div>'
            % (cls, face, face, FACE[face], w, inner, extra))

def seg(name, items):
    out = ['<span class="seg" role="group" aria-label="%s">' % name]
    for i, (id_, lab, chk) in enumerate(items):
        out.append('<input class="sr" type="radio" name="%s" id="%s"%s><label for="%s">%s</label>' % (name, id_, ' checked' if chk else '', id_, lab))
    out.append('</span>')
    return ''.join(out)

def tog():
    return '<span class="tog"><label for="fa">A Atkinson</label><label for="fb">B Literata</label></span>'

def facepick(inner_board):
    return '<input class="sr" type="radio" name="face" id="fa" checked><input class="sr" type="radio" name="face" id="fb">' + inner_board

# ================================================================ TYPE COMPARE
def board_type():
    b = []
    b.append('<div class="wrap page">')
    b.append('<p class="lab">Version 2 \u00b7 type comparison</p><h1>Atkinson or Literata?</h1>')
    b.append('<p class="lede">Both columns use the same text, the same labels and the same sizes. Only the reading face and the headings change. The interface is IBM Plex Sans in both, and your dark palette is untouched.</p>')
    b.append('<div class="nav"><a class="btn" href="Main.dc.html">Back to the plan</a><a class="btn" href="Symbols.dc.html">Symbols and glyph proof</a></div>')
    b.append('<div class="bar"><span class="gl">Show</span>' + seg('v', [('v1', 'Both', True), ('v2', 'A', False), ('v3', 'B', False)]) +
             '<span class="gl">Text</span>' + seg('k', [('k1', 'Normal', True), ('k2', 'Large', False)]) + '</div>')
    # hierarchy
    b.append('<h2>The hierarchy</h2><p>One scale, not 16 px everywhere. The first number is the phone, the second is a PC. Both options use these sizes; the faces differ only in the rows marked A and B.</p>')
    b.append('<div class="tw"><table><thead><tr><th>Role</th><th>Phone / PC</th><th>A</th><th>B</th></tr></thead><tbody>'
             '<tr><td>Chapter title</td><td class="num">30 / 38 px, line 1.15</td><td>Atkinson Bold</td><td>Literata Semibold</td></tr>'
             '<tr><td>Section heading</td><td class="num">23 / 26 px, line 1.25</td><td>Atkinson Bold</td><td>Literata Semibold</td></tr>'
             '<tr><td>Subheading</td><td class="num">19 / 21 px, line 1.3</td><td>Atkinson Bold</td><td>Literata Semibold</td></tr>'
             '<tr><td>Body text</td><td class="num">17 / 18 px, line 1.6 / 1.65</td><td>Atkinson Regular</td><td>Literata Regular</td></tr>'
             '<tr><td>In plain words</td><td class="num">18 / 19 px</td><td>Atkinson Regular</td><td>Literata Regular</td></tr>'
             '<tr><td>Equations</td><td class="num">20 / 22 px</td><td>Atkinson, italic variables</td><td>Literata, italic variables</td></tr>'
             '<tr><td>Captions, notes</td><td class="num">15 px, line 1.5</td><td>Atkinson Regular</td><td>Literata Regular</td></tr>'
             '<tr><td>Buttons, menus, tabs</td><td class="num">16 px, Semibold</td><td colspan="2">IBM Plex Sans (both)</td></tr>'
             '<tr><td>Small caps labels</td><td class="num">12.5 px, +0.08em</td><td colspan="2">IBM Plex Sans Semibold (both)</td></tr>'
             '<tr><td>Scientific labels, plot notes</td><td class="num">13 px</td><td colspan="2">Candidate: Plex Mono, Plex Sans or the reading face (section 4)</td></tr>'
             '<tr><td>Code</td><td class="num">14.5 px</td><td colspan="2">IBM Plex Mono (both)</td></tr>'
             '</tbody></table></div>')
    cpl = MEAS.get('cpl')
    if cpl:
        b.append('<p class="small">Measured in the browser on the 540 px column at 18 px: about <b>%s</b> characters a line in A and <b>%s</b> in B (the target is 60 to 70).</p>' % (cpl['A'], cpl['B']))
    # phone
    b.append('<h2>1. A chapter on a phone</h2><p>Frames are exactly 390 px wide with 16 px side gutters, the same as an iPhone. If you are reading this on a phone, the frame is your screen width and everything is life size.</p>')
    b.append('<div class="pair">' + frame('A', 'ph', specimen('ph', 'A')) + frame('B', 'ph', specimen('ph', 'B')) + '</div>')
    # pc
    b.append('<div class="onlywide"><h2>2. The same chapter in a 540 px PC column</h2><p>Shown on wider screens only. This is the middle column of the three zone layout.</p>')
    b.append('<div class="pair">' + frame('A', 'pcw', specimen('pcw', 'A')) + frame('B', 'pcw', specimen('pcw', 'B')) + '</div></div>')
    # labels
    b.append('<h2>3. Look-alike letters and numbers</h2><p>Atkinson was designed so that similar shapes stay apart. Check the first line in each face: capital I, small L and the digit 1; capital O and zero.</p>')
    b.append('<div class="tw"><table><thead><tr><th>Face</th><th>Sample, 20 px</th></tr></thead><tbody>')
    for nm, ff in (('Atkinson Next', 'var(--ffA)'), ('Literata', 'var(--ffB)'), ('Plex Sans', 'var(--ffU)'), ('Plex Mono', 'var(--ffM)')):
        b.append('<tr><td>%s</td><td style="font-family:%s;font-size:20px;line-height:1.5;letter-spacing:.02em">Il1| O0o rn m 5S 8B 6G 2Z 0.84 \u2212 1,000</td></tr>' % (nm, ff))
    b.append('</tbody></table></div>')
    b.append('<h2>4. Scientific labels and plot notes</h2><p>The same drawing and the same notes four times. Only the label face changes. Plex Mono has no Greek letters, so the \u03c3 and \u0394 in its row are drawn by the small symbol file; look at how they sit. Labels are 13 px and drawn life size, not shrunk with the picture.</p>')
    b.append('<div class="pair">')
    for nm, lf in (('Plex Mono', 'var(--ffM)'), ('Plex Sans, tabular figures', 'var(--ffU)'), ('Atkinson Hyperlegible Next', 'var(--ffA)'), ('Literata', 'var(--ffB)')):
        b.append('<div class="frame"><div class="fh"><span>Labels in %s</span></div><div class="fb fig" style="--lf:%s">' % (nm, lf)
                 + curve_svg(358, 228, lf) + labstrip(lf)
                 + '<p class="src" style="margin-top:8px">A card built by the book\u2019s own code from TOI-1338 data (seed 12345). \u201cstrength 7.3\u201d is that card\u2019s measured strength. The strings under the drawing are real formulas from Chapters 7 and 11; they are here to test the type, not to describe this curve.</p></div></div>')
    b.append('</div>')
    # weight
    b.append('<h2>5. What each option downloads</h2><p>Kilobytes of font files for one chapter page that uses Greek, as the browser would fetch them. Latin only; the Latin extension files load only on pages that need them.</p>')
    b.append('<div class="tw"><table><thead><tr><th>Set</th><th>Files</th><th class="num">KB</th></tr></thead><tbody>'
             '<tr><td>Today</td><td>Inter normal and italic, Plex Mono 400 and 500</td><td class="num">%s</td></tr>'
             '<tr><td>Option A</td><td>Atkinson normal and italic (%s + %s), Plex Sans 400 and 600, Plex Mono 400, symbol files %s</td><td class="num">%s</td></tr>'
             '<tr><td>Option B</td><td>Literata normal, italic and Greek (%s + %s + %s), Plex Sans 400 and 600, Plex Mono 400, symbol files %s</td><td class="num">%s</td></tr>'
             '</tbody></table></div>'
             % (f1(tot_today), f1(SZ['atk_n']), f1(SZ['atk_i']), f1(SZ['sym'] + SZ['cross']), f1(tot_A),
                f1(SZ['lit_n']), f1(SZ['lit_i']), f1(SZ['lit_g']), f1(SZ['sym'] + SZ['cross']), f1(tot_B)))
    b.append('<p class="small">Both fit the offline cache with room to spare. The difference between A and B is mostly Literata\u2019s own Greek.</p>')
    obs = MEAS.get('notes')
    b.append('<h2>6. Decision</h2><p class="lede">Tell me A or B for the reading face, and which label face you prefer (Plex Mono, Plex Sans or the reading face). I have not picked for you.</p>')
    if obs: b.append('<div class="note"><p class="lab">What I noticed after rendering both</p>%s</div>' % obs)
    b.append('</div>')
    return ''.join(b)

# ================================================================ SYMBOLS
def board_symbols():
    rows = PROOF['rows']
    groups = [('Greek letters', lambda r: 0x370 <= ord(r['ch']) <= 0x3ff),
              ('Maths signs and primes', lambda r: ord(r['ch']) in (0x2248, 0x221a, 0x2265, 0x2264, 0x221d, 0x2192, 0x2212, 0xd7, 0xf7, 0xb1, 0xb2, 0xb3, 0xb0, 0x2032, 0x2033, 0x304)),
              ('Marks and arrows', lambda r: ord(r['ch']) in (0x2605, 0x2713, 0x2717, 0x25c0, 0x25b6, 0xb7, 0xa7)),
              ('Astronomy symbols, not used by the book yet', lambda r: not r['used'])]
    cols = PROOF['cols']
    short = {'atkinson': 'Atkinson', 'literata': 'Literata', 'plexsans': 'Plex Sans', 'plexmono': 'Plex Mono', 'inter': 'Inter', 'sym': 'Noto Math cut'}
    b = ['<div class="wrap page">']
    b.append('<p class="lab">Version 2 \u00b7 symbols</p><h1>Which font draws the Greek and maths?</h1>')
    b.append('<p class="lede">The book uses %d characters beyond plain letters and digits. I checked which fonts really contain each one by reading the font files, then drew the outline of every glyph from the file itself. A blank mark means the file has no glyph, so a phone would borrow one from a different font.</p>' % PROOF['n_used'])
    b.append('<div class="nav"><a class="btn" href="Main.dc.html">Back to the plan</a><a class="btn" href="Type-Compare.dc.html">Type comparison</a></div>')
    b.append('<h2>Result</h2>')
    b.append('<div class="note"><p><b>Inter, my earlier idea, is not enough.</b> It has the Greek letters but not \u2248 \u221a \u2265 \u2264 \u221d \u2192 \u2605 \u2713 \u2717 \u25c0 \u25b6, which the book uses.</p>'
             '<p><b>Noto Sans Math, cut down to what the book needs, covers all of them except \u2717.</b> The cut file is <b>%s KB</b>. The one missing mark, \u2717, comes from Noto Sans Symbols 2 as a <b>%s KB</b> file. Both are under the SIL Open Font Licence, the same licence as the other fonts.</p>'
             '<p><b>IBM Plex Mono has no Greek at all</b> in the files Google and Fontsource serve, so a \u03c3 in a Plex Mono label is drawn by the symbol file.</p></div>' % (f1(SZ['sym']), f1(SZ['cross'])))
    b.append('<div class="tw"><table><thead><tr><th>Font</th><th class="num">Draws of %d used</th><th class="num">of %d astronomy</th><th>Note</th></tr></thead><tbody>' % (PROOF['n_used'], PROOF['n_astro']))
    notes = {'atkinson': 'No Greek, no maths signs, no primes', 'literata': 'Greek and primes yes, maths signs no', 'plexsans': 'Greek and primes yes, maths signs no',
             'plexmono': 'No Greek; primes yes', 'inter': 'Greek and primes yes, maths signs no', 'sym': 'Cut file: only the characters the book needs, plus 3 astronomy'}
    for c in cols:
        k = c['key']
        nu = sum(1 for r in rows if r['used'] and r['cells'][k]['d'] is not None)
        na = sum(1 for r in rows if (not r['used']) and r['cells'][k]['d'] is not None)
        lab = c['label'] + (' (%s KB)' % f1(SZ['sym'] + SZ['cross']) if k == 'sym' else '')
        b.append('<tr><td>%s</td><td class="num">%d</td><td class="num">%d</td><td>%s</td></tr>' % (lab, nu, na, notes[k]))
    b.append('</tbody></table></div>')
    b.append('<p class="small">The cut file leaves out the ten Latin-1 characters (\u00b7 \u00d7 \u00f7 \u00b0 \u00a7 \u00b1 \u2212 \u00b2 \u00b3 and the combining macron) because every text face already draws them, so its 21 is out of 31 on purpose.</p>')
    b.append('<h2>Who draws what in each pairing</h2><div class="tw"><table><thead><tr><th>Text style</th><th>Font chain</th><th>Result for the 35 characters</th></tr></thead><tbody>')
    pretty = {'today (Inter, Plex Mono)': ('Today', 'Inter'), 'A reading: Atkinson > symbols': ('A reading', 'Atkinson, then symbol files'),
              'B reading: Literata > symbols': ('B reading', 'Literata, then symbol files'), 'UI: Plex Sans > symbols': ('Interface', 'Plex Sans, then symbol files'),
              'labels: Plex Mono > symbols': ('Mono labels', 'Plex Mono, then symbol files')}
    for k, v in CHAINS.items():
        nm, ch = pretty[k]
        unc = v['uncovered']
        res = ', '.join('%s %d' % ({'atkinson': 'Atkinson', 'literata': 'Literata', 'plexsans': 'Plex Sans', 'plexmono': 'Plex Mono', 'inter': 'Inter', 'sym': 'symbol files'}[a], n) for a, n in v['drawn_by'].items())
        res += '. Not drawn by any file: ' + (' '.join(unc) if unc else 'none') + ('. Today those fall to your phone\u2019s own font.' if nm == 'Today' else ('. (\u2643 Jupiter is not used by the book.)' if unc == ['\u2643'] else '.'))
        b.append('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % (nm, ch, res))
    b.append('</tbody></table></div>')
    b.append('<h2>Glyph proof</h2><p>Each outline is drawn from the font file named at the top of its column, not typed in a font and hoped for. The last column is the cut symbol file. The shaded column is the one the redesign would add.</p>')
    b.append('<div class="tw"><div class="gp"><span></span>' + ''.join('<span class="hd">%s</span>' % short[c['key']] for c in cols))
    for gname, pred in groups:
        gr = [r for r in rows if pred(r)]
        b.append('<span class="sec">%s</span>' % gname)
        for r in gr:
            use = ('used %d times' % r['n']) if r['used'] else 'candidate'
            b.append('<span class="lbl"><b aria-hidden="true">%s</b>%s<span class="gname"><br>%s \u00b7 %s</span></span>' % (_h.escape(r['ch']), r['cp'], _h.escape(r['name']), use))
            for c in cols:
                cell = r['cells'][c['key']]
                hl = ' hl' if c['key'] == 'sym' else ''
                if cell['d']:
                    b.append('<span class="c%s"><svg viewBox="0 -28 100 140" role="img" aria-label="%s has this glyph"><path d="%s"/></svg></span>' % (hl, short[c['key']], cell['d']))
                else:
                    b.append('<span class="c no%s" aria-label="%s has no glyph">none</span>' % (hl, short[c['key']]))
    b.append('</div></div>')
    b.append('<h2>Live text, as a phone would draw it</h2><p>A browser quietly borrows from another font when a glyph is missing, so this section proves nothing by itself; the outlines above are the proof. It shows how the cut file sits beside each text face.</p>')
    b.append('<div class="pair">')
    sample = 'The standard deviation (\u03c3) \u2248 1.4826 \u00d7 MAD; \u03c3<sub>N</sub> = \u03c3<sub>1</sub> / \u221a<i>N</i>; SNR \u2265 7; \u0394<i>x\u0304</i> \u2248 \u03b4 \u00d7 <i>d</i>; \u03bc = <i>m</i><sub>2</sub> / (<i>m</i><sub>1</sub> + <i>m</i><sub>2</sub>); \u2605 \u2713 \u2717 \u25c0 \u25b6 \u2192; \u2299 \u2295 \u2609.'
    for face in ('A', 'B'):
        b.append('<div class="frame opt%s"><div class="fh"><span>%s \u00b7 %s</span></div><div class="fb"><div class="sp r%s ph"><p style="margin-top:12px">%s</p><p style="font-weight:700">%s</p></div></div></div>' % (face, face, FACE[face], face, sample, sample.split(';')[0] + ' \u2248 \u03c3'))
    b.append('</div>')
    b.append('<h2>What I did not test</h2><ul><li>STIX Two Math, Latin Modern Math, DejaVu Sans and Libertinus Math. They are far larger than needed, and Noto Sans Math already covers everything the book uses.</li>'
             '<li>How the cut glyphs look next to a bold weight. Noto Sans Math has one weight, so \u03c3 in a bold heading is drawn regular, not faux bold.</li>'
             '<li>Greek in Plex Mono from IBM\u2019s own release. The version Google serves has none; I did not check IBM\u2019s download.</li></ul>')
    b.append('<p class="small">Full file for reference: Noto Sans Math is %s KB before cutting, the cut is %s KB.</p>' % (f1(SZ['nsm_full']), f1(SZ['sym'])))
    b.append('</div>')
    return ''.join(b)

# ================================================================ SHARED CHAPTER PIECES
RAIL = """<div class="railp">
<p class="lab" style="margin-top:0">Where you are</p>
<p class="here"><b>Chapter 2</b> \u00b7 Light curves<small>Level 0 \u00b7 step 2 of 15 on the track</small></p>
<p class="lab">The track: 7 levels, in learning order</p>
<ol class="track">
<li class="cur"><span class="tag">L0</span>What a light curve is<ul><li>1 Stars, names and missions</li><li class="cur" aria-current="page">2 Light curves</li><li>3 Our data</li></ul></li>
<li><span class="tag">L1</span>How big is the dip?<em>Lesson page, no chapter</em></li>
<li><span class="tag">L2</span>From dip depth back to size<em>Parts of chapters 2 and 11</em></li>
<li><span class="tag">L3</span>Bright stars, faint stars, noise<em>Chapters 7, 8</em></li>
<li><span class="tag">L4</span>Orbits, and why our dips wander<em>Chapters 4, 5, 6</em></li>
<li><span class="tag">L5</span>The fakes<em>Chapters 9, 10</em></li>
<li><span class="tag">L6</span>Two-key vetting<em>Chapters 11, 12</em></li>
<li><span class="tag">+</span>After Level 6<em>Chapters 13, 14, 15</em></li>
</ol>
<p class="lab">The 15 chapters, by fixed number</p>
<div class="nums">""" + ''.join('<span%s>%d</span>' % (' class="cur"' if i == 2 else '', i) for i in range(1, 16)) + """</div>
<p class="small" style="font-size:13px;margin:0">Numbers are topics and never change. The track decides which to read next, so 7 comes before 4.</p>
<p class="lab">In this chapter</p>
<p style="margin:0 0 4px">2.1 The intuition</p><p style="margin:0 0 4px">2.2 The scientific meaning</p><p style="margin:0 0 4px;color:var(--tx);font-weight:700">2.3 The technical explanation</p>
</div>"""

NOTE_F013 = ('<details class="inl" open><summary><span class="chip">F-013 verified</span> Evidence note</summary>'
             '<p>Transit depth is approximately (planet radius / star radius) squared.</p>'
             '<p>Source: standard geometry: blocked area / disc area (derived); see Winn 2010 review. Checked 2026-10-20.</p></details>')

def track_dots():
    groups = [3, 2, 3, 2, 2, 3]; cur = 2; out = ['<div class="dots" role="img" aria-label="Step 2 of 15 on your track, in Level 0">']; i = 0
    for gi, g in enumerate(groups):
        if gi: out.append('<b></b>')
        for _ in range(g):
            i += 1
            out.append('<i class="%s"></i>' % ('c' if i == cur else ('d' if i < cur else '')))
    out.append('</div>')
    return ''.join(out)

# ================================================================ PHONE BOARD
def phone_chapter():
    s = specimen('ph', '', eyebrow='', meta2='', long=False)
    s = s.replace('<p class="eyebrow"></p>', '').replace('<p class="meta"><br>about 25 min', '<p class="meta">about 25 min')
    s = s.replace('<p>Depths are tiny', NOTE_F013 + '<p>Depths are tiny', 1)
    head = ('<div style="padding:14px 16px 0"><div style="display:flex;align-items:center;justify-content:space-between;min-height:44px"><b style="font-size:16px">Second Sun</b><span class="btn" style="min-height:44px;padding:0 12px">Menu</span></div>'
            '<div style="border:1.5px solid var(--rule);border-radius:8px;padding:12px 14px;margin:8px 0 6px;background:var(--surf)">'
            '<p style="margin:0;font-size:16px"><b>Chapter 2</b> \u00b7 Light curves</p>'
            '<p style="margin:2px 0 0;font-size:14px;color:var(--tx2)">Level 0 \u00b7 step 2 of 15 on your track</p>' + track_dots() +
            '<details class="inl" open style="margin:6px 0 0;border-bottom:0"><summary>Chapter or level?</summary><p>A <b>chapter</b> is a topic with a fixed number, 1 to 15. A <b>level</b> is a stage of the track and says which chapters to read next, so the numbers can look out of order.</p></details>'
            '</div></div>')
    return head + '<div style="padding:0 16px 24px">' + s + '</div>'

def eyes_phone_choose():
    return ('<div style="padding:14px 16px 20px"><div style="display:flex;justify-content:space-between;align-items:center;min-height:40px"><span class="eyebrow" style="margin:0">Practice round</span><span style="font-size:14px;color:var(--tx2)">Card 12 of 30</span></div>'
            '<p class="eyebrow" style="margin-top:10px">Is there a dip?</p><div class="fig">' + curve_svg(358, 210) + '</div>'
            '<p class="src">Example card from the book\u2019s own card code. Not one of your rounds.</p>'
            '<p class="eyebrow" style="margin-top:14px">Your answer</p>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><button class="ans">Dip</button><button class="ans">No dip</button><button class="ans">Odd</button><button class="ans">Not sure</button></div></div>')

def fb_lines():
    return ''.join('<p>%s</p>' % _h.escape(t) for t in FB['lines'])

def eyes_phone_after():
    return ('<div style="padding:14px 16px 0"><div style="display:flex;justify-content:space-between;align-items:center;min-height:40px"><span class="eyebrow" style="margin:0">Practice round</span><span style="font-size:14px;color:var(--tx2)">Card 12 of 30</span></div>'
            '<div class="fig">' + curve_svg(358, 150, ann=True, T=10, B=34) + '</div>'
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px"><button class="ans on" aria-pressed="true">Dip</button><button class="ans off" disabled>No dip</button><button class="ans off" disabled>Odd</button><button class="ans off" disabled>Not sure</button></div>'
            '<div class="banner"><p class="eyebrow">Feedback</p><div class="fbk sp ph">' + fb_lines() + '</div></div></div>'
            '<div class="nextbar"><a class="btn pri">Next card</a></div>')

def board_phone():
    def ph(title, inner, h):
        return '<div style="width:390px"><p class="eyebrow" style="margin:0 0 8px">%s</p><div style="width:390px;border:1.5px solid var(--rule);border-radius:22px;overflow:hidden;background:var(--bg);min-height:%dpx" class="sp ph">%s</div></div>' % (title, h, inner)
    body = ('<div class="board" style="width:1380px;padding-bottom:32px"><div class="top"><span class="t">Phone, 390 px wide, life size</span><span style="display:flex;gap:12px;align-items:center">' + tog() +
            '<a class="btn" style="min-height:40px" href="Main.dc.html">Back to the plan</a></span></div>'
            '<div style="display:flex;gap:40px;align-items:flex-start;padding:28px 40px 0">'
            + ph('Chapter', phone_chapter(), 1500) + ph('Eyes: choose', eyes_phone_choose(), 640) + ph('Eyes: after answering', eyes_phone_after(), 760) +
            '</div><p class="small" style="padding:20px 40px 0;max-width:900px;margin:0">The layout order is proposed: curve, answer, feedback, then Next pinned to the bottom. I have not compared it pixel for pixel with today\u2019s phone page. The feedback text is the book\u2019s own, generated for this example card.</p></div>')
    return facepick(body)

# ================================================================ PC CHAPTER
def board_pc_chapter():
    spec_full = specimen('pcw', '', eyebrow='', meta2='', long=False)  # unused pieces; we compose rows below
    def sec(inner, rowi): return '<section class="mid sp pcw" style="grid-row:%d">%s</section>' % (rowi, inner)
    def mar(inner, rowi, pt=0): return '<aside class="mar" style="grid-row:%d;padding-top:%dpx">%s</aside>' % (rowi, pt, inner)
    g = []
    g.append('<nav class="rail" aria-label="Where you are and the learning track">' + RAIL + '</nav>')
    g.append(sec('<h1>2. Light curves: seeing planets as shadows</h1><p class="meta">about 25 min \u00b7 Maths: fractions, percentages, ppm, squares, averages</p>'
                 '<a class="btn">Listen to this chapter</a>'
                 '<div class="plain" style="margin-top:20px"><p class="eyebrow">In plain words</p><p>We cannot photograph these planets, so we watch a star\u2019s brightness over time. When a planet passes in front, the star dims a little: that is a transit.</p></div>'
                 '<p><b>What this chapter answers:</b> how does a brightness graph reveal a planet, and how does the TESS telescope collect that graph?</p>', 1))
    g.append(mar('', 1))
    g.append(sec('<h2>2.1 The intuition</h2><p>Stand at night and look at a distant streetlight. A moth flies across it. You can\u2019t see the moth, but for a moment the light looks a touch dimmer. If you\u2019d been measuring the light with a meter every few seconds, you\u2019d see a small notch in the readings. The size of the notch tells you how big the moth is compared with the lamp.</p><p>The star is the lamp. The planet is the moth. TESS is the meter.</p>', 2))
    g.append(mar('', 2))
    g.append(sec('<h2>2.2 The scientific meaning</h2><p>A <span class="term">light curve</span> is a list of (time, brightness) pairs. For a star with no planet and no partner, it\u2019s roughly flat, with random jitter (noise). A <span class="term">transit</span> shows as a dip with a flat bottom: the planet slides on, sits fully in front, slides off.</p><p>Three numbers describe a transit:</p>'
                 + ''.join('<div class="row3"><b>%s</b><span class="v"><span class="k">Meaning</span>%s</span><span class="v"><span class="k">Tells us</span>%s</span></div>' % r for r in [
                     ('Depth', 'how much dimmer the star gets', 'the planet\u2019s size compared with the star'),
                     ('Duration', 'how long the dip lasts', 'how fast the planet moves across, and the path it takes'),
                     ('Time (mid-point)', 'when it happens', 'for single-star planets, the period; for two-sun planets, a timing pattern (Chapter 5)')]), 3))
    g.append(mar('<div class="mn off"><span class="t">Glossary \u00b7 2 terms</span><p class="more">light curve, transit</p></div>', 3, 66))
    g.append(sec('<h2>2.3 The technical explanation</h2><h3>Depth and size</h3><p>The planet blocks a disc of light. The fraction blocked is the planet\u2019s disc area divided by the star\u2019s disc area. Area grows with radius squared, so <span class="chip">F-013 verified</span>:</p>'
                 '<div class="eq"><span class="c">Eq. 2.1 \u00b7 transit depth</span>depth \u2248 (<i>R</i><sub>p</sub> / <i>R</i><sub>\u2605</sub>)\u00b2</div>'
                 '<ul><li><i>R</i><sub>p</sub>: the planet\u2019s radius (centre to edge).</li><li><i>R</i><sub>\u2605</sub>: the star\u2019s radius.</li></ul>'
                 '<p>Depths are tiny, so we use <b>ppm</b> (parts per million): 1% = 10,000 ppm. Earth crossing the Sun: (1/109)\u00b2 \u2248 0.000084 = <b>84 ppm</b>. Jupiter crossing the Sun: about 1% = <b>10,000 ppm</b>.</p>', 4))
    g.append(mar('<div class="mn on"><span class="t">Evidence</span><p><span class="chip">F-013 verified</span></p><p>Transit depth is approximately (planet radius / star radius) squared.</p><p>Source: standard geometry: blocked area / disc area (derived); see Winn 2010 review. Checked 2026-10-20.</p><p class="why">Open because this paragraph is in view.</p></div>', 4, 96))
    g.append(sec('<h3>How TESS collects light curves</h3><p>TESS is a NASA space telescope that stares at one big patch of sky for about <b>27 days</b> (a <span class="term">sector</span>), then moves on <span class="chip">F-012 verified</span>. It records brightness two ways:</p>'
                 '<ul><li><b>Full-frame images</b> of the whole patch: every 30 minutes (sectors 1-26), every 10 minutes (27-55), every 200 seconds (56 onward) <span class="chip">F-012 verified</span>.</li>'
                 '<li><b>2-minute \u201cpostage stamps\u201d</b> for selected stars, which NASA\u2019s SPOC pipeline turns into ready-made light curves. Most of our tests use these.</li></ul>'
                 '<h3>Noise</h3><p>Every measurement jitters. For a star like TOI-1338 (TESS magnitude about 11.5), one hour of 2-minute data scatters by roughly <b>400 to 550 ppm</b> in our measurements (overnight test, <code>pipeline/diag_v2_results.json</code>). A planet\u2019s dip has to stand clearly above that, which is the subject of Chapter 8.</p>'
                 '<div class="btns"><a class="btn">Mark as read</a><a class="btn">Next: Chapter 3 \u2192</a></div>', 5))
    g.append(mar('<div class="mn off"><span class="t">Evidence \u00b7 F-012</span><p class="more">TESS observes one patch for about 27 days.</p></div><div class="mn off"><span class="t">Glossary \u00b7 sector</span></div>', 5, 6))
    grid = '<div class="grid">' + ''.join(g) + '</div>'
    css_extra = ''
    body = ('<div class="board" style="width:1366px;padding-bottom:20px"><div class="top"><span class="t">Second Sun \u00b7 Chapter 2 of 15</span><span style="display:flex;gap:12px;align-items:center">' + tog() +
            '<a class="btn" style="min-height:40px" href="Main.dc.html">Back to the plan</a></span></div>' + grid +
            '<div style="max-width:1120px;margin:20px auto 0;padding:16px 0 0;border-top:1px solid var(--rule);display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;font-size:14px;color:var(--tx2)">'
            '<div><p class="eyebrow">Left: two different lists</p><p style="margin:0">The track is the order to learn in (7 levels). The 15 chapters are fixed topics. Both are shown, labelled, and never merged.</p></div>'
            '<div><p class="eyebrow">Middle: the reading column</p><p style="margin:0">540 px wide at 18 px, about 70 characters a line. Nothing here depends on the margin, so it reads the same without it.</p></div>'
            '<div><p class="eyebrow">Right: a quiet margin</p><p style="margin:0">Only the note for what is on screen is open. Others fold to one line. Under 1100 px wide the notes sit inline instead.</p></div></div></div>')
    return facepick(body)

PC_GRID_CSS = """
.grid{display:grid;grid-template-columns:232px 540px 260px;column-gap:44px;justify-content:center;padding:28px 0 0}
.rail{grid-column:1;grid-row:1 / span 6;align-self:start;position:sticky;top:12px}
.mid{grid-column:2}.mar{grid-column:3;align-self:start}
"""

# ================================================================ PC EYES
def board_pc_eyes():
    def win(title, inner, h):
        return ('<div><p class="eyebrow" style="margin:0 0 8px">%s</p><div style="width:1366px;height:%dpx;border:1.5px solid var(--rule);border-radius:6px;overflow:hidden;position:relative;background:var(--bg)">%s</div></div>' % (title, h, inner))
    topbar = '<div class="top" style="min-height:52px;padding:4px 40px;position:relative;z-index:2;background:var(--bg)"><span class="t">Second Sun \u00b7 Eyes mode</span><span style="font-size:15px;font-weight:600">Practice round \u00b7 Card 12 of 30</span><span class="btn" style="min-height:40px">Menu</span></div>'
    f1_ = (topbar + '<div style="max-width:1000px;margin:0 auto;padding:22px 0 0"><p class="eyebrow">Is there a dip?</p><div class="fig">' + curve_svg(1000, 260, L=56, B=40) + '</div>'
           '<p class="src">Example card from the book\u2019s own card code. Not one of your rounds.</p>'
           '<p class="eyebrow" style="margin-top:10px">Your answer</p><div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px"><button class="ans">Dip</button><button class="ans">No dip</button><button class="ans">Odd</button><button class="ans">Not sure</button></div></div>')
    f2_ = (topbar + '<div style="max-width:1000px;margin:0 auto;padding:0;margin-top:-120px"><div class="fig" style="opacity:.55">' + curve_svg(1000, 260, L=56, B=40) + '</div>'
           '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:8px"><button class="ans on" aria-pressed="true">Dip</button><button class="ans off" disabled>No dip</button><button class="ans off" disabled>Odd</button><button class="ans off" disabled>Not sure</button></div>'
           '<div class="banner" style="max-width:700px"><p class="eyebrow">Feedback</p><div class="fbk sp pcw">' + fb_lines() + '</div></div></div>'
           '<div class="nextbar" style="position:absolute;left:0;right:0;bottom:0"><a class="btn pri" style="max-width:520px">Next card</a></div>'
           '<div style="position:absolute;right:3px;top:70px;width:6px;height:200px;border-radius:3px;background:var(--rule)"></div><div style="position:absolute;right:3px;top:150px;width:6px;height:120px;border-radius:3px;background:var(--tx3)"></div>')
    body = ('<div class="board" style="width:1406px;padding:0 0 32px"><div class="top"><span class="t">PC, 1366 by 650 window. The page scrolls when it needs to.</span><span style="display:flex;gap:12px;align-items:center">' + tog() +
            '<a class="btn" style="min-height:40px" href="Main.dc.html">Back to the plan</a></span></div><div style="padding:28px 20px 0;display:flex;flex-direction:column;gap:32px">'
            + win('1. Before answering: curve and the four buttons fit this window, without being forced to', f1_, 650)
            + win('2. After answering: the window has scrolled, so the feedback is readable and Next stays pinned', f2_, 650) +
            '</div><div style="padding:22px 40px 0;max-width:1100px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:28px;font-size:14px;color:var(--tx2)">'
            '<div><p class="eyebrow">Curve height follows the window</p><p style="margin:0">40% of the window height, never under 220 px or over 400 px, up to 1000 px wide. Short windows or a zoomed page just push the buttons lower; nothing is cut off.</p></div>'
            '<div><p class="eyebrow">Feedback is body text</p><p style="margin:0">18 px, about 62 characters a line, the same size as a chapter. It is never squeezed to fit.</p></div>'
            '<div><p class="eyebrow">Next stays under your thumb</p><p style="margin:0">The pinned bar appears after you answer. The page keeps bottom space so it never covers the last line.</p></div></div></div>')
    return facepick(body)

# ================================================================ ZOOMED
def board_zoom():
    chap = specimen('pcw', '', eyebrow='', meta2='', long=False)
    chap = chap.replace('<p class="eyebrow"></p>', '').replace('<p class="meta"><br>about 25 min', '<p class="meta">about 25 min')
    chap = chap.replace('<p>Depths are tiny', NOTE_F013 + '<p>Depths are tiny', 1)
    chap_card = ('<div style="padding:14px 16px 0"><div style="display:flex;align-items:center;justify-content:space-between;min-height:48px"><b>Second Sun</b><span class="btn" style="min-height:44px">Menu</span></div>'
                 '<div style="border:1.5px solid var(--rule);border-radius:8px;padding:12px 14px;margin:8px 0 6px;background:var(--surf)"><p style="margin:0"><b>Chapter 2</b> \u00b7 Light curves</p>'
                 '<p style="margin:2px 0 0;font-size:14px;color:var(--tx2)">Level 0 \u00b7 step 2 of 15 on your track</p>' + track_dots() +
                 '<details class="inl" style="margin:6px 0 0;border-bottom:0"><summary>Show the track and all 15 chapters</summary><p>The full list opens here instead of staying in a side rail.</p></details></div></div>')
    eyes = ('<div style="padding:14px 16px 0"><div style="display:flex;justify-content:space-between;align-items:center;min-height:44px"><span class="eyebrow" style="margin:0">Practice round</span><span style="font-size:14px;color:var(--tx2)">Card 12 of 30</span></div>'
            '<div class="fig">' + curve_svg(651, 220, L=56) + '</div><p class="src">Example card from the book\u2019s own card code.</p><p class="eyebrow">Your answer</p>'
            '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px"><button class="ans on">Dip</button><button class="ans off" disabled>No dip</button><button class="ans off" disabled>Odd</button><button class="ans off" disabled>Not sure</button></div>'
            '<div class="banner"><p class="eyebrow">Feedback</p><div class="fbk sp pcw">' + fb_lines() + '</div></div></div><div class="nextbar"><a class="btn pri">Next card</a></div>')
    def col(title, inner):
        return '<div style="width:683px"><p class="eyebrow" style="margin:0 0 8px">%s</p><div class="sp pcw" style="width:683px;border:1.5px solid var(--rule);border-radius:6px;overflow:hidden;background:var(--bg)">%s</div></div>' % (title, inner)
    body = ('<div class="board" style="width:1500px;padding-bottom:32px"><div class="top"><span class="t">Same pages at 200% zoom on a 1366 px window: 683 CSS px wide</span><span style="display:flex;gap:12px;align-items:center">' + tog() +
            '<a class="btn" style="min-height:40px" href="Main.dc.html">Back to the plan</a></span></div><div style="display:flex;gap:40px;padding:28px 40px 0;align-items:flex-start">'
            + col('Chapter, zoomed', chap_card + '<div style="padding:0 16px 24px">' + chap + '</div>') + col('Eyes, zoomed', eyes) + '</div>'
            '<p class="small" style="padding:18px 40px 0;margin:0;max-width:1000px">Under 1100 px the side rail folds into the card at the top, margin notes become inline notes that open under the sentence, and Eyes stacks. Text keeps its size, so nothing gets smaller when the window gets narrower.</p></div>')
    return facepick(body)

# ================================================================ MAIN
def board_main():
    b = ['<div class="page">']
    b.append('<p class="lab">Version 2 \u00b7 27 October 2026 \u00b7 for your decision</p><h1>Second Sun redesign plan</h1>')
    b.append('<p class="lede">Nothing on the live book has changed, and nothing is built. This is the plan after your feedback. The boards use the real text, the real claims and a real card from the book.</p>')
    b.append('<div class="nav"><a class="btn" href="Type-Compare.dc.html">Type comparison</a><a class="btn" href="Symbols.dc.html">Symbols</a><a class="btn" href="Phone.dc.html">Phone</a><a class="btn" href="PC-Chapter.dc.html">PC chapter</a><a class="btn" href="PC-Eyes.dc.html">PC Eyes</a><a class="btn" href="Zoomed.dc.html">200% zoom</a></div>')
    b.append('<h2>What you asked, and what I did</h2><div class="tw"><table><thead><tr><th>Your point</th><th>What changed</th></tr></thead><tbody>'
             '<tr><td>1. Compare Atkinson and Literata</td><td>A side by side page with identical text, a real type scale (not 16 px everywhere), and Plex Mono kept as a label candidate. Dark palette untouched.</td></tr>'
             '<tr><td>2. Quieter right margin, chapters versus levels</td><td>The margin opens only the note for what is on screen; the rest fold to one line. The left rail now shows the 7 level track and the 15 chapters as two labelled things.</td></tr>'
             '<tr><td>3. Eyes without a forced fit</td><td>No no-scroll rule. The curve follows window height, feedback is body text, Next is pinned after you answer, and zoom folds it to one column.</td></tr>'
             '<tr><td>4. Test a symbol font</td><td>Inter fails. A 1.9 KB cut of Noto Sans Math plus a 0.9 KB one-glyph file covers everything the book uses. Glyph outlines drawn from the files.</td></tr>'
             '<tr><td>5. Fair comparison and a real phone view</td><td>One comparison page with both options at real 390 px width, and a phone board with the chapter and both Eyes states.</td></tr>'
             '</tbody></table></div>')
    b.append('<h2>Two lists, not one</h2><p>The book has 15 chapters and a 7 level learning track. They are different things and they are now drawn that way.</p>')
    b.append('<div class="tw"><table><thead><tr><th>Level</th><th>Name</th><th>Chapters in it</th></tr></thead><tbody>'
             '<tr><td>Level 0</td><td>What a light curve is</td><td class="num">1, 2, 3</td></tr><tr><td>Level 1</td><td>How big is the dip?</td><td>Lesson page, no chapter</td></tr>'
             '<tr><td>Level 2</td><td>From dip depth back to size</td><td>Parts of chapters 2 and 11</td></tr><tr><td>Level 3</td><td>Bright stars, faint stars, noise</td><td class="num">7, 8</td></tr>'
             '<tr><td>Level 4</td><td>Orbits, and why our dips wander</td><td class="num">4, 5, 6</td></tr><tr><td>Level 5</td><td>The fakes</td><td class="num">9, 10</td></tr>'
             '<tr><td>Level 6</td><td>Two-key vetting</td><td class="num">11, 12</td></tr><tr><td>After Level 6</td><td>Running the project</td><td class="num">13, 14, 15</td></tr></tbody></table></div>')
    b.append('<ul><li><b>Chapters</b> are topics with a fixed number, 1 to 15. The number never changes and never means order.</li><li><b>The track</b> says what to read next: 1, 2, 3, then 7, 8, then 4, 5, 6, and so on. \u201cStep 2 of 15\u201d counts chapters only, not the two lesson pages.</li>'
             '<li>On a phone the top card says both: \u201cChapter 7\u201d and \u201cLevel 3 \u00b7 step 4 of 15\u201d.</li></ul>')
    b.append('<h2>The changes, in short</h2><ol>'
             '<li><b>Type.</b> A reading face for text and headings, IBM Plex Sans for buttons and menus, Plex Mono for code and maybe plot labels. Sizes follow a scale: 17/18 px body, 30/38 px titles.</li>'
             '<li><b>Symbols.</b> A small self-hosted file so \u03c3 \u03bc \u0394 \u2248 \u221a \u2265 \u2192 \u2605 \u2713 are drawn by a font that has them, in the same shape on every device.</li>'
             '<li><b>PC chapter.</b> Three zones at 1100 px and wider: your place on the left, the reading column in the middle, a quiet note margin on the right. Never wider than 1400 px.</li>'
             '<li><b>Eyes.</b> A wide, shorter curve and the four answers in one row. Feedback and Next come after, and the page scrolls naturally if the window is short.</li>'
             '<li><b>Quieter pages.</b> Four callout styles only; colours stay as you approved.</li></ol>')
    b.append('<h2>What does not change</h2><ul><li>Every word, chapter, claim, question and page address.</li><li>Eyes scoring, saving and the cloud copy.</li><li>Chip shapes: solid verified, dashed likely, dotted unverified.</li><li>Listen, glossary pop-ups, Mark as read, search, offline reading and the day and night switch.</li></ul>')
    b.append('<h2>Decisions that are yours</h2>')
    b.append('<div class="dec"><h3>1. Reading face</h3><p>A: Atkinson Hyperlegible Next for text and headings. B: Literata. The interface is Plex Sans either way. Use the comparison page, on your phone first.</p></div>')
    b.append('<div class="dec"><h3>2. Label face for plot notes and scientific labels</h3><p>Plex Mono, Plex Sans with tabular figures, or the reading face. Plex Mono has no Greek, so it relies on the symbol file for \u03c3 and \u0394.</p></div>')
    b.append('<div class="dec"><h3>3. The right margin</h3><p>As drawn (contextual, one note open) or no margin at all with notes always inline. Inline works on every width and is the fallback in both cases.</p></div>')
    b.append('<div class="dec"><h3>4. Pinned Next on Eyes</h3><p>A bar at the bottom after you answer, or a plain Next button after the feedback.</p></div>')
    b.append('<div class="dec"><h3>5. Symbol font</h3><p>Noto Sans Math cut to 23 glyphs (%s KB) plus one glyph from Noto Sans Symbols 2 (%s KB). Say if you want a different one.</p></div>' % (f1(SZ['sym']), f1(SZ['cross'])))
    b.append('<h2>How it gets built, after your yes</h2><div class="tw"><table><thead><tr><th>Step</th><th>Work</th><th class="num">Points</th></tr></thead><tbody>'
             '<tr><td>1</td><td>Fonts, type scale, symbol files, offline test</td><td class="num">2 to 3</td></tr>'
             '<tr><td>2</td><td>Chapter page and margin notes on PC, track rail</td><td class="num">2 to 4</td></tr>'
             '<tr><td>3</td><td>Eyes layout on PC and zoom</td><td class="num">1 to 2</td></tr>'
             '<tr><td>4</td><td>Look pass, all tests, publish</td><td class="num">1.5 to 3</td></tr></tbody></table></div>'
             '<p class="small">About 6.5 to 12 weekly points in all, rough. I start only when you say so.</p>')
    b.append('<h2>What I checked, and what I did not</h2><div class="note">')
    chk = MEAS.get('checked')
    b.append(chk if chk else '<p>(filled after rendering)</p>')
    b.append('</div><h2>What I need from you</h2><p class="plain-lede" style="border-left:3px solid var(--brass);padding-left:14px;font-size:18px">Reply with your picks for decisions 1 to 5, or tell me what to change. Silence is not approval. Nothing is built until you say so.</p>')
    b.append('<p class="small">The 549 star search stays off.</p></div>')
    return ''.join(b)

# ================================================================ EMIT
BOARDS = [
 ('Main.dc.html', 'Second Sun redesign plan', board_main, '', 1100),
 ('Type-Compare.dc.html', 'Type comparison', board_type, '', 1100),
 ('Symbols.dc.html', 'Symbols', board_symbols, '', 1100),
 ('Phone.dc.html', 'Phone', board_phone, '', 1380),
 ('PC-Chapter.dc.html', 'PC chapter', board_pc_chapter, PC_GRID_CSS, 1366),
 ('PC-Eyes.dc.html', 'PC Eyes', board_pc_eyes, '', 1406),
 ('Zoomed.dc.html', '200% zoom', board_zoom, '', 1500),
]
if __name__ == '__main__':
    sizes = {}
    for fn, title, fnc, extra, w in BOARDS:
        body = fnc()
        hh = H.get(fn, 3000)
        sizes[fn] = (w, hh)
        open(os.path.join(PUB, fn), 'w', encoding='utf-8', newline='\n').write(dc_page(title, CSS + extra, body, w, hh))
        open(os.path.join(LOC, fn.replace('.dc.html', '.html')), 'w', encoding='utf-8', newline='\n').write(local_page(title, CSS + extra, body))
        print(fn, len(body), 'chars')
    # local copies of the symbol fonts
    os.makedirs(os.path.join(LOC, 'fonts'), exist_ok=True)
    import shutil
    for f in ('ss-symbols.woff2', 'ss-cross.woff2'):
        shutil.copy(os.path.join(OUT, f), os.path.join(LOC, 'fonts', f))
    # canvas.json
    x = 0; boards = {}; order = []
    layout = [('Main.dc.html', 0, 0, 'The plan', True), ('Type-Compare.dc.html', 1180, 0, 'Type comparison', True), ('Symbols.dc.html', 2360, 0, 'Symbols and glyph proof', True)]
    row2 = max(H.get(f, 3000) for f, *_ in layout) + 120
    layout += [('Phone.dc.html', 0, row2, 'Phone, life size', False), ('PC-Chapter.dc.html', 0, row2 + H.get('Phone.dc.html', 1800) + 120, 'PC: chapter', False)]
    y3 = row2 + H.get('Phone.dc.html', 1800) + 120 + H.get('PC-Chapter.dc.html', 1700) + 120
    layout += [('PC-Eyes.dc.html', 0, y3, 'PC: Eyes mode', False), ('Zoomed.dc.html', 0, y3 + H.get('PC-Eyes.dc.html', 1500) + 120, '200% zoom', False)]
    for fn, bx, by, tt, fill in layout:
        w, hh = sizes[fn]
        ent = {'x': bx, 'y': by, 'w': w, 'h': hh, 'title': tt, 'is_interactive': True}
        if fill: ent['expand'] = 'fill'
        boards[fn] = ent; order.append(fn)
    cj = {'v': 3, 'createdOnFiles': {'v': 1, 'at': '2026-10-27T13:00:00Z'}, 'title': 'Second Sun Redesign Plan', 'launch': {'view': 'focused', 'file': 'Main.dc.html'},
          'pages': [], 'boards': boards, 'order': order, 'notes': {}, 'designSystems': []}
    json.dump(cj, open(os.path.join(PUB, 'canvas.json'), 'w', encoding='utf-8', newline='\n'), indent=2)
    print('canvas.json written')
