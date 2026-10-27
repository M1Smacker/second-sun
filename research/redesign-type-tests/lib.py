"""Shared pieces for the Second Sun redesign canvas v2: data, CSS, fragments. No site files are touched."""
import json, os, re, sys, html as _h
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
DL = os.path.join(HERE, 'dl')
V1 = os.path.join(HERE, '..', 'redesign-canvas', 'v1')

def jload(p, default=None):
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return default

PROOF = jload(os.path.join(OUT, 'proof.json'))
CHAINS = jload(os.path.join(OUT, 'chains.json'))
FB = jload(os.path.join(HERE, 'fb_sample.json'))['dip']
MEAS = jload(os.path.join(HERE, 'measured.json'), {})
FONT_URLS = jload(os.path.join(HERE, 'font_urls.json'), {})

# ---------------------------------------------------------------- fonts
GOOGLE = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400..700;1,400..700'
          '&family=Literata:ital,wght@0,400..700;1,400..700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400'
          '&family=IBM+Plex+Mono:wght@400;500&display=swap">')

SYM_RANGE = ','.join('U+%04X' % ord(r['ch']) for r in PROOF['rows']
                     if r['cells']['sym']['d'] is not None and not (r['ch'] in '·×÷°§±−²³̄'))

def fontface(mode):
    if mode == 'publish':
        u1 = FONT_URLS.get('ss-symbols.woff2', 'ss-symbols.woff2')
        u2 = FONT_URLS.get('ss-cross.woff2', 'ss-cross.woff2')
    else:
        u1, u2 = 'fonts/ss-symbols.woff2', 'fonts/ss-cross.woff2'
    return ("@font-face{font-family:'SS Symbols';src:url(%s) format('woff2');font-weight:100 900;font-style:normal;font-display:swap;unicode-range:%s}"
            "@font-face{font-family:'SS Cross';src:url(%s) format('woff2');font-weight:100 900;font-style:normal;font-display:swap;unicode-range:U+2717}") % (u1, SYM_RANGE, u2)

# ---------------------------------------------------------------- css
CSS = r"""
:root{--bg:#0c1018;--surf:#131a27;--raised:#1a2233;--tx:#f2f4f9;--tx2:#c3c9d6;--tx3:#9aa3b6;--acc:#eebf6a;--brass:#eebf6a;--rule:#2a3448;
--ffA:'Atkinson Hyperlegible Next','SS Symbols','SS Cross',system-ui,sans-serif;
--ffB:'Literata','SS Symbols','SS Cross',Georgia,'Times New Roman',serif;
--ffU:'IBM Plex Sans','SS Symbols','SS Cross',system-ui,sans-serif;
--ffM:'IBM Plex Mono','SS Symbols','SS Cross',ui-monospace,Menlo,Consolas,monospace}
@media (prefers-color-scheme: light){:root{--bg:#faf9f6;--surf:#f1efe9;--raised:#ffffff;--tx:#10141b;--tx2:#3a4251;--tx3:#566070;--acc:#6f4608;--brass:#9a7a3c;--rule:#d9d5cb}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx)}
.sr{position:absolute;opacity:0;width:1px;height:1px;pointer-events:none}
a{color:inherit}
:focus-visible{outline:3px solid var(--acc);outline-offset:2px}

/* ---- reading face, size set, scale ---- */
.rA{--read:var(--ffA);--hw:700}
.rB{--read:var(--ffB);--hw:600}
.ph{--b:17px;--lh:1.6;--h1:30px;--h2:23px;--h3:19px;--eq:20px;--plain:18px}
.pcw{--b:18px;--lh:1.65;--h1:38px;--h2:26px;--h3:21px;--eq:22px;--plain:19px}
.sp{--k:1;font-family:var(--read);font-size:calc(var(--b) * var(--k));line-height:var(--lh);color:var(--tx);font-weight:400;overflow-wrap:break-word;font-kerning:normal}
.sp h1,.sp h2,.sp h3{font-family:var(--read);font-weight:var(--hw);text-wrap:balance;color:var(--tx)}
.sp h1{font-size:calc(var(--h1) * var(--k));line-height:1.15;letter-spacing:-.01em;margin:10px 0 8px}
.sp h2{font-size:calc(var(--h2) * var(--k));line-height:1.25;margin:30px 0 10px}
.sp h3{font-size:calc(var(--h3) * var(--k));line-height:1.3;margin:22px 0 6px}
.sp p{margin:0 0 .8em}
.sp ul{margin:0 0 .8em;padding-left:1.2em}
.sp li{margin:0 0 .35em}
.sp b{font-weight:700}
.sp sub{font-size:.7em;line-height:0}
.eyebrow{font-family:var(--ffU);font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2);margin:0 0 6px;line-height:1.4}
.meta{font-family:var(--ffU);font-size:14px;line-height:1.5;color:var(--tx2);margin:0 0 14px}
.plain{border-left:3px solid var(--brass);padding:2px 0 2px 14px;margin:14px 0 18px;font-size:calc(var(--plain) * var(--k))}
.plain .eyebrow{margin-bottom:3px}
.plain p{margin:0}
.term{border-bottom:1.5px dotted var(--tx2)}
.chip{font-family:var(--ffU);font-size:13px;font-weight:600;line-height:1.4;border:1.5px solid var(--tx2);border-radius:6px;padding:1px 8px;white-space:nowrap;color:var(--tx);display:inline-block}
.chip.l{border-style:dashed}.chip.u{border-style:dotted}
.row3{padding:10px 0;border-top:1px solid var(--rule)}
.row3:last-of-type{border-bottom:1px solid var(--rule)}
.row3 b{display:block}
.row3 .k{font-family:var(--ffU);font-size:12.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2);margin-right:6px}
.row3 span.v{display:block;font-size:.95em;line-height:1.5}
.eq{margin:16px 0;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);text-align:center;font-size:calc(var(--eq) * var(--k));line-height:1.45}
.eq .c{display:block;font-family:var(--ffU);font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2);margin-bottom:4px}
.eq i{font-style:italic}
.cap{font-size:calc(15px * var(--k));line-height:1.5;color:var(--tx2);margin:8px 0 4px}
.src{font-family:var(--ffU);font-size:13px;line-height:1.45;color:var(--tx2);margin:0 0 10px}
code,.code{font-family:var(--ffM);font-size:14.5px;background:var(--surf);border:1px solid var(--rule);border-radius:4px;padding:1px 5px}
.btn{font-family:var(--ffU);font-size:16px;font-weight:600;line-height:1.2;min-height:48px;padding:0 18px;border:1.5px solid var(--tx3);border-radius:6px;background:var(--surf);color:var(--tx);display:inline-flex;align-items:center;justify-content:center;gap:8px;text-decoration:none;cursor:pointer}
.btn.pri{background:var(--acc);border-color:var(--acc);color:var(--bg)}
.btns{display:flex;flex-wrap:wrap;gap:12px;margin:18px 0 8px}
.sci{font-family:var(--ffM);font-size:13px;line-height:1.5;color:var(--tx2)}

/* ---- page chrome for the fluid pages ---- */
.page{max-width:1240px;margin:0 auto;padding:28px 16px 72px;font-family:var(--ffU);font-size:16px;line-height:1.6;color:var(--tx)}
.page h1{font-family:var(--ffU);font-size:34px;line-height:1.15;font-weight:700;margin:6px 0 12px;text-wrap:balance}
.page h2{font-family:var(--ffU);font-size:24px;line-height:1.25;font-weight:700;margin:52px 0 12px;padding-top:22px;border-top:1px solid var(--rule);text-wrap:balance}
.page h3{font-family:var(--ffU);font-size:18px;line-height:1.3;font-weight:700;margin:22px 0 6px}
.page p{margin:0 0 12px;max-width:68ch}
.page ul,.page ol{margin:0 0 12px;padding-left:22px;max-width:68ch}
.page li{margin:0 0 8px}
.lede{font-size:18px;color:var(--tx2)}
.small{font-size:14.5px;color:var(--tx2)}
.lab{font-family:var(--ffU);font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2);margin:0 0 6px}
.nav{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}
.tw{overflow-x:auto;margin:0 0 14px}
.page table{border-collapse:collapse;width:100%;font-size:15px;min-width:340px}
.page th,.page td{text-align:left;vertical-align:top;padding:9px 12px 9px 0;border-bottom:1px solid var(--rule);line-height:1.45}
.page th{font-size:12.5px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:var(--tx2)}
.num{font-variant-numeric:tabular-nums}
.note{background:var(--surf);border:1px solid var(--tx3);border-radius:6px;padding:16px;margin:0 0 16px}
.note p:last-child{margin-bottom:0}
.dec{border-top:1px solid var(--rule);padding:16px 0}
.dec h3{margin-top:0}
.pill{display:inline-block;font-size:12.5px;font-weight:600;letter-spacing:.04em;border:1.5px solid var(--tx2);border-radius:999px;padding:1px 10px;color:var(--tx)}
.good{color:var(--tx)}

/* ---- controls (CSS only, :has) ---- */
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--rule);padding:10px 0;margin:18px 0 0;display:flex;flex-wrap:wrap;gap:10px 22px;align-items:center}
.seg{display:inline-flex;border:1.5px solid var(--tx3);border-radius:8px;overflow:hidden}
.seg label{font-family:var(--ffU);font-size:15px;font-weight:600;padding:0 14px;min-height:44px;display:inline-flex;align-items:center;cursor:pointer;color:var(--tx2);background:var(--surf);border-right:1px solid var(--rule)}
.seg label:last-child{border-right:0}
.bar .gl{font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2)}
.wrap:has(#v1:checked) label[for=v1],.wrap:has(#v2:checked) label[for=v2],.wrap:has(#v3:checked) label[for=v3],
.wrap:has(#k1:checked) label[for=k1],.wrap:has(#k2:checked) label[for=k2]{background:var(--acc);color:var(--bg)}
.wrap:has(#v1:focus-visible) label[for=v1],.wrap:has(#v2:focus-visible) label[for=v2],.wrap:has(#v3:focus-visible) label[for=v3],
.wrap:has(#k1:focus-visible) label[for=k1],.wrap:has(#k2:focus-visible) label[for=k2]{outline:3px solid var(--tx);outline-offset:-3px}
.wrap:has(#v2:checked) .optB{display:none}
.wrap:has(#v3:checked) .optA{display:none}
.wrap:has(#k2:checked) .sp{--k:1.15}

/* ---- comparison frames ---- */
.pair{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start;justify-content:center;margin:18px 0 0}
.frame{border:1.5px solid var(--rule);border-radius:14px;background:var(--bg);overflow:hidden;width:min(100%,390px)}
.frame.wide{width:min(100%,572px);border-radius:8px}
.frame .fh{font-family:var(--ffU);font-size:13px;font-weight:600;padding:8px 16px;background:var(--surf);border-bottom:1px solid var(--rule);color:var(--tx);display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap}
.frame .fb{padding:6px 16px 22px}
.frame.wide .fb{padding:6px 16px 26px}
@media (max-width:520px){.bar .gl{display:none}.bar{gap:8px 10px;padding:8px 0}.seg label{padding:0 11px;font-size:14px}}
@media (max-width:440px){
  .frame{width:calc(100% + 32px);margin-left:-16px;margin-right:-16px;border-radius:0;border-left:0;border-right:0}
  .frame.wide,.onlywide{display:none}
}
.fig svg{display:block;width:100%;height:auto}
.fig text{font-family:var(--lf,var(--ffM));font-size:13px;fill:var(--tx2);font-variant-numeric:tabular-nums}
.fig text.call{fill:var(--tx);font-weight:500}
.fig .ax{stroke:var(--tx3);stroke-width:1;fill:none}
.fig .gr{stroke:var(--rule);stroke-width:1;fill:none}
.fig .cv{stroke:var(--acc);stroke-width:1.5;fill:none;stroke-linejoin:round}
.fig .ld{stroke:var(--tx);stroke-width:1.2;fill:none}
.fig .wl{stroke:var(--tx3);stroke-width:1;stroke-dasharray:3 4;fill:none}
.labstrip{display:flex;flex-wrap:wrap;gap:6px 16px;font-family:var(--lf,var(--ffM));font-size:13px;line-height:1.5;color:var(--tx2);margin:6px 0 4px}
.labstrip span{white-space:nowrap}
.labstrip sub{font-size:.75em;line-height:0}

/* ---- glyph proof ---- */
.gp{display:grid;grid-template-columns:minmax(78px,1fr) repeat(6,40px);gap:2px 4px;align-items:center;min-width:360px}
.gp .hd{font-size:12.5px;font-weight:600;color:var(--tx2);line-height:1;writing-mode:vertical-rl;transform:rotate(180deg);height:92px;white-space:nowrap;text-align:left;justify-self:center}
.gp .lbl{font-size:13px;line-height:1.3;color:var(--tx2);padding:2px 0;border-top:1px solid var(--rule)}
.gp .lbl b{font-size:16px;color:var(--tx);margin-right:4px}
.gp .c{display:flex;align-items:center;justify-content:center;height:44px;border-top:1px solid var(--rule)}
.gp .c svg{width:30px;height:42px;display:block;fill:var(--tx)}
.gp .c.no{color:var(--tx3);font-size:14px}
.gp .c.hl{background:var(--surf)}
.gp .sec{grid-column:1 / -1;font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2);padding:18px 0 4px}
@media (max-width:520px){.gp .gname{display:none}}

/* ---- fixed-size boards ---- */
.board{--read:var(--ffA);--hw:700;font-family:var(--ffU);color:var(--tx);background:var(--bg);font-size:16px;line-height:1.5}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:56px;padding:6px 40px;border-bottom:1px solid var(--rule)}
.top .t{font-size:12.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2)}
.tog{display:inline-flex;border:1.5px solid var(--tx3);border-radius:8px;overflow:hidden}
.tog label{font-size:14px;font-weight:600;min-height:40px;padding:0 12px;display:inline-flex;align-items:center;cursor:pointer;color:var(--tx2);background:var(--surf);border-right:1px solid var(--rule)}
.tog label:last-child{border-right:0}
#fa:checked ~ .board label[for=fa],#fb:checked ~ .board label[for=fb]{background:var(--acc);color:var(--bg)}
#fa:focus-visible ~ .board label[for=fa],#fb:focus-visible ~ .board label[for=fb]{outline:3px solid var(--tx);outline-offset:-3px}
#fb:checked ~ .board{--read:var(--ffB);--hw:600}
.ans{font-family:var(--ffU);font-size:18px;font-weight:700;min-height:56px;border:2px solid var(--tx2);border-radius:6px;background:var(--surf);color:var(--tx);cursor:pointer}
.ans.on{background:var(--raised);border-color:var(--acc);color:var(--acc)}
.ans.off{border-style:dashed;color:var(--tx2)}
.fbk{font-family:var(--read);font-size:calc(var(--b) * 1);line-height:var(--lh);color:var(--tx)}
.fbk p{margin:0 0 .7em}
.banner{border-top:2px solid var(--brass);border-bottom:1px solid var(--rule);padding:10px 0 4px;margin:14px 0 12px}
.nextbar{position:sticky;bottom:0;background:var(--bg);border-top:1px solid var(--rule);padding:10px 16px;display:flex;justify-content:center}
.nextbar .btn{width:100%;max-width:520px;min-height:56px;font-size:18px}
.mn{font-family:var(--ffU);font-size:13.5px;line-height:1.5;color:var(--tx2);border-left:1px solid var(--rule);padding:0 0 0 12px;margin:0 0 20px}
.mn .t{display:block;font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--tx2);margin-bottom:2px}
.mn p{margin:0 0 6px}
.mn.on{border-left:2px solid var(--brass);color:var(--tx)}
.mn.off p.more{margin:0}
.mn .why{font-size:12px;color:var(--tx2);font-style:italic}
.railp{font-family:var(--ffU);font-size:14.5px;line-height:1.4}
.railp .lab{margin:20px 0 6px}
.railp .here{margin:0 0 4px;font-size:16px}
.railp .here small{display:block;font-size:14px;color:var(--tx2);margin-top:2px}
.track{list-style:none;margin:0;padding:0}
.track>li{margin:0;padding:7px 0 7px 12px;border-left:2px solid var(--rule);color:var(--tx2)}
.track>li.cur{border-left-color:var(--brass);color:var(--tx)}
.track .tag{display:inline-block;min-width:26px;font-size:12px;font-weight:700;letter-spacing:.04em;color:var(--acc);margin-right:4px}
.track em{display:block;font-style:normal;font-size:13px;color:var(--tx2);padding-left:32px}
.track ul{list-style:none;margin:4px 0 0;padding:0 0 0 32px}
.track ul li{padding:3px 0;color:var(--tx2)}
.track ul li.cur{color:var(--tx);font-weight:700}
.nums{display:grid;grid-template-columns:repeat(5,1fr);gap:4px;margin:0 0 6px}
.nums span{display:flex;align-items:center;justify-content:center;min-height:34px;border:1.5px solid var(--rule);border-radius:6px;font-size:14px;color:var(--tx2)}
.nums span.cur{border-color:var(--brass);color:var(--tx);font-weight:700}
.dots{display:flex;align-items:center;gap:3px;flex-wrap:nowrap;margin:8px 0 4px}
.dots i{width:11px;height:11px;flex:0 0 auto;border-radius:50%;border:1.5px solid var(--tx3);display:inline-block}
.dots i.d{background:var(--tx2);border-color:var(--tx2)}
.dots i.c{background:var(--acc);border-color:var(--acc);box-shadow:0 0 0 3px var(--bg),0 0 0 4.5px var(--acc)}
.dots b{width:8px;height:1px;background:var(--rule);display:inline-block;margin:0 2px;flex:0 0 auto}
details.inl{font-family:var(--ffU);font-size:14.5px;line-height:1.5;color:var(--tx2);border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin:8px 0 14px}
details.inl summary{min-height:44px;display:flex;align-items:center;gap:8px;cursor:pointer;font-weight:600;color:var(--tx)}
details.inl p{margin:0 0 8px}
"""

# ---------------------------------------------------------------- figure helpers
def pctl(arr, lo, hi, a, b, v):
    return a + (v - lo) / (hi - lo) * (b - a)

def card_points():
    return FB['y']

def curve_svg(W, H, lf='var(--ffM)', ann=True, label='A stretch of brightness readings, 36 hours long', L=50, R=12, T=14, B=40, call='strength 7.3 ≥ 7'):
    y = card_points(); n = len(y)
    x0, x1, y0, y1 = L, W - R, T, H - B
    X = lambda i: x0 + i / (n - 1) * (x1 - x0)
    Y = lambda v: y0 + (4000 - v) / 8000 * (y1 - y0)
    d = 'M' + 'L'.join('%.1f %.1f' % (X(i), Y(v)) for i, v in enumerate(y))
    jmin = min(range(n), key=lambda k: y[k])
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s" style="--lf:%s">' % (W, H, label, lf)]
    s.append('<line class="gr" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (x0, Y(4000), x1, Y(4000)))
    s.append('<line class="gr" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (x0, Y(-4000), x1, Y(-4000)))
    s.append('<line class="wl" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (x0, Y(0), x1, Y(0)))
    s.append('<path class="cv" d="%s"/>' % d)
    for v, t in ((4000, '+4000'), (0, '0 ppm'), (-4000, '-4000')):
        s.append('<text x="%d" y="%.1f" text-anchor="end">%s</text>' % (x0 - 6, Y(v) + 4.5, t))
    for hrs in (0, 12, 24, 36):
        xx = x0 + hrs / 36 * (x1 - x0)
        s.append('<line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (xx, y1, xx, y1 + 5))
        anchor = 'start' if hrs == 0 else ('end' if hrs == 36 else 'middle')
        s.append('<text x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (xx, y1 + 22, anchor, '%d h' % hrs))
    if ann:
        px, py = X(jmin), Y(y[jmin])
        ty = Y(-3350)
        s.append('<line class="ld" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (px - 24, ty - 4, px - 2, py - 3))
        s.append('<text class="call" x="%.1f" y="%.1f" text-anchor="end">%s</text>' % (px - 28, ty, call))
    s.append('</svg>')
    return ''.join(s)

def labstrip(lf):
    return ('<div class="labstrip" style="--lf:%s"><span>σ ≈ 1.4826 × MAD</span><span>SNR = depth / σ<sub>D</sub></span>'
            '<span>2,015 / √30 ≈ 368 ppm</span><span>7σ</span><span>Δ<i>x̄</i> ≈ δ × <i>d</i></span></div>') % lf

# ---------------------------------------------------------------- the specimen (identical for A and B)
def specimen(size, face, eyebrow='Chapter 2 · Light curves', meta2='Level 0 · step 2 of 15 on your track', buttons=True, long=True):
    s = []
    s.append('<div class="sp %s %s">' % (('r'+face) if face else '', size))
    s.append('<p class="eyebrow">%s</p>' % eyebrow)
    s.append('<h1>2. Light curves: seeing planets as shadows</h1>')
    s.append('<p class="meta">%s<br>about 25 min · Maths: fractions, percentages, ppm, squares, averages</p>' % meta2)
    s.append('<div class="plain"><p class="eyebrow">In plain words</p><p>We cannot photograph these planets, so we watch a star’s brightness over time. When a planet passes in front, the star dims a little: that is a transit.</p></div>')
    s.append('<h2>2.2 The scientific meaning</h2>')
    s.append('<p>A <span class="term">light curve</span> is a list of (time, brightness) pairs. For a star with no planet and no partner, it’s roughly flat, with random jitter (noise). A <span class="term">transit</span> shows as a dip with a flat bottom: the planet slides on, sits fully in front, slides off.</p>')
    s.append('<p>Three numbers describe a transit:</p>')
    rows = [('Depth', 'how much dimmer the star gets', 'the planet’s size compared with the star'),
            ('Duration', 'how long the dip lasts', 'how fast the planet moves across, and the path it takes'),
            ('Time (mid-point)', 'when it happens', 'for single-star planets, the period; for two-sun planets, a timing pattern (Chapter 5)')]
    for a, b, c in rows:
        s.append('<div class="row3"><b>%s</b><span class="v"><span class="k">Meaning</span>%s</span><span class="v"><span class="k">Tells us</span>%s</span></div>' % (a, b, c))
    s.append('<h3>Depth and size</h3>')
    s.append('<p>The planet blocks a disc of light. The fraction blocked is the planet’s disc area divided by the star’s disc area. Area grows with radius squared, so <span class="chip">F-013 verified</span>:</p>')
    s.append('<div class="eq"><span class="c">Eq. 2.1 · transit depth</span>depth ≈ (<i>R</i><sub>p</sub> / <i>R</i><sub>★</sub>)²</div>')
    s.append('<p>Depths are tiny, so we use <b>ppm</b> (parts per million): 1% = 10,000 ppm. Earth crossing the Sun: (1/109)² ≈ 0.000084 = <b>84 ppm</b>. Jupiter crossing the Sun: about 1% = <b>10,000 ppm</b>.</p>')
    if long:
        s.append('<p class="eyebrow" style="margin-top:26px">From Chapter 7 · Noise and statistics</p>')
        s.append('<h3 style="margin-top:4px">Measuring the wobble robustly</h3>')
        s.append('<p>The <b>standard deviation</b> (σ) is the usual measure of spread, but one wild point can inflate it. We use a <b>robust</b> version that ignores a few outliers:</p>')
        s.append('<div class="eq"><span class="c">Eq. 7.1 · robust spread</span>σ ≈ 1.4826 × median( | <i>x</i> − median(<i>x</i>) | )</div>')
        s.append('<h3>Averaging</h3>')
        s.append('<div class="eq"><span class="c">Eq. 7.2 · white-noise averaging</span>σ<sub><i>N</i></sub> = σ<sub>1</sub> / √<i>N</i></div>')
        s.append('<ul><li>σ<sub>1</sub>: the wobble of one measurement. σ<sub><i>N</i></sub>: the wobble of an average of <i>N</i> measurements.</li>'
                 '<li>Example: 2,015 ppm per 2-minute point, averaged over 1 hour (<i>N</i> = 30): 2,015 / √30 ≈ <b>368 ppm</b>, <b>if</b> the noise were white.</li></ul>')
        s.append('<p>For pure bell-curve noise, the chance of one average falling 7σ below normal is about <b>1 in 780 billion</b>.</p>')
        s.append('<p><code>find_events()</code> keeps boxes with SNR ≥ 7.</p>')
    if buttons:
        s.append('<div class="btns"><a class="btn">Mark as read</a><a class="btn">Next: Chapter 3 →</a></div>')
    s.append('</div>')
    return ''.join(s)

# ---------------------------------------------------------------- wrappers
def dc_page(title, css, body, w, h, interactive=True):
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>\n%s\n%s\n</style>\n</helmet>\n%s\n</x-dc>\n'
            '<script type="text/x-dc" data-dc-script data-props=\'{"$preview":{"width":%d,"height":%d}}\'>\nclass Component extends DCLogic {\n  renderVals() { return {}; }\n}\n</script>\n</body>\n</html>\n'
            % (title, GOOGLE, fontface('publish'), css, body, w, h))

def local_page(title, css, body):
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>%s</title>\n%s\n<style>\n%s\n%s\n</style></head>\n<body>%s</body></html>\n'
            % (title, GOOGLE, fontface('local'), css, body))
