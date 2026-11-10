"""Book coverage audit (10 Nov 2026): for each concept of the filter and the science behind it, count hits in the TEACHING parts of the book
(chapters, labs, parts, start, learn, glossary) and in the DIARY parts (field notes, versions, claims, other pages)."""
import re, pathlib, sys, collections
B = pathlib.Path(r"D:\second-sun\book\docs")
GROUPS = {
    "chapters": list(B.glob("book/*.md")), "labs": list(B.glob("labs/*.md")), "parts": list(B.glob("parts/**/*.md")),
    "start": list(B.glob("start/*.md")), "learn": list(B.glob("learn/*.md")), "glossary": [B / "glossary.md"],
    "notes": list(B.glob("field-notes/*.md")), "other": [p for p in B.glob("*.md") if p.name != "glossary.md"],
}
TXT = {g: {p: p.read_text(encoding="utf-8", errors="replace") for p in ps} for g, ps in GROUPS.items()}
C = [
 # (area, concept, regex)
 ("filter", "Frozen version / settings hash / freeze", r"frozen|freez|settings hash|zero.difference"),
 ("filter", "Products: SPOC, TESS-SPOC, QLP, full-frame", r"\bQLP\b|TESS-SPOC|full.frame|\bFFI\b"),
 ("filter", "PDCSAP vs SAP flux", r"PDCSAP|\bSAP\b"),
 ("filter", "Quality flags / bitmask", r"quality (mask|flag|bit)|bitmask|hard mask"),
 ("filter", "Detrending (biweight, 2-day window)", r"biweight|wotan|detrend|flatten"),
 ("filter", "Box search over durations (3 to 20 h)", r"box (search|score)|box least|\bBLS\b|boxes of"),
 ("filter", "SNR 7 threshold", r"SNR (of )?7|signal.to.noise.{0,20}7|SNR ?>= ?7"),
 ("filter", "Upside-down control (flipped light, bumps)", r"upside.down|flipped|mirror|inverted"),
 ("filter", "Eclipse mask (blindfold)", r"eclipse mask|masks? (the )?eclipses?|masked eclipse|eclipse_mask"),
 ("filter", "Mask folds one sector at the binary period", r"fold(s|ed|ing)? (at|on) the (binary )?period|phase.fold"),
 ("filter", "Catalogue periods and eclipse widths (Prsa, TTC, Villanova)", r"Pr[sš]a|Ten Thousand|TTC|Villanova|KEBC|catalogue"),
 ("filter", "Second-product check", r"second product|second.key product|other product"),
 ("filter", "Tiers (tier 1, tier 2)", r"tier.?[12]|tier one|first tier"),
 ("filter", "Flags (gap edge, momentum dump, common moment, step, ramp, repeater)", r"momentum dump|common.moment|flip.match|repeater|ramp flag|step flag|dominated"),
 ("filter", "Orbit-locked check (c6)", r"orbit.locked|c6\b"),
 ("method", "False-alarm yardstick (upside-down per 1,000 star-sectors)", r"per 1,000 star.sectors|false alarm|false.alarm"),
 ("method", "Preregistration / sealed split / one-shot", r"preregist|sealed|one.shot|pre.regist"),
 ("method", "S1 / S2 / S3 pass criteria", r"\bS[123]\b"),
 ("method", "Injection and recovery (planted dips)", r"inject|fake (planet|dip)|recovery|planted"),
 ("method", "Depth in units of noise (K), K50, completeness", r"\bK50\b|\bK90\b|completeness|recovery fraction"),
 ("method", "Injection BEFORE the mask (order matters)", r"before the (eclipse )?mask|inject(ed)? before|after the mask"),
 ("method", "Reach map / expected number of planets (Horizon)", r"reach map|Horizon|expected (number of )?planets"),
 ("method", "Transit probability for circumbinary planets (coplanar, tilt)", r"transit probab|coplanar|mutual inclination"),
 ("method", "Occurrence rate (Armstrong, about 10 percent)", r"occurrence|Armstrong|10 ?%.{0,40}binar"),
 ("method", "Real versus upside-down excess (asymmetry)", r"excess|asymmetr"),
 ("method", "Noise statistics (red noise, scatter, p-value)", r"red noise|scatter|p.value|standard deviation|sigma"),
 ("science", "Eclipsing binaries: detached, eccentric, secondary eclipse", r"secondary eclipse|eccentric|detached|primary eclipse"),
 ("science", "Binary period vs sector length (slow binary, one visit per phase)", r"slow(er)? binar|one visit|once per sector|period longer than"),
 ("science", "Ephemeris (epoch, period, drift)", r"ephemeri|epoch|T0|BJD0"),
 ("science", "Time systems BTJD / BJD", r"BTJD|BJD"),
 ("science", "TTV and TDV (timing and duration variations)", r"\bTTVs?\b|\bTDVs?\b|timing variation|duration variation"),
 ("science", "Three-body orbits and the stability limit", r"stability limit|three.body|N.body|unstable"),
 ("science", "Pixel-level vetting, dilution, nearby stars", r"centroid|dilution|nearby star|neighbour|pixel"),
 ("science", "Known planets (Kepler-16, TOI-1338, TIC 172900988)", r"Kepler-16|TOI-1338|TIC ?172900988"),
 ("science", "Professionals' tools (STANLEY, Windemuth, mono-cbp)", r"STANLEY|Windemuth|mono-cbp|QATS"),
 ("science", "Gaia eclipsing-binary catalogue", r"Gaia"),
 ("science", "Sectors, cameras, scattered light", r"scattered light|camera|sector"),
 ("project", "Hunts G1, G2, G3 (what, how many stars)", r"\bG[123]\b"),
 ("project", "Census plan", r"Census"),
 ("project", "Two-key rule and leads", r"two.key|second key|lead"),
 ("project", "CTOI / ExoFOP / credit", r"CTOI|ExoFOP|credit"),
]
rows = []
for area, name, rx in C:
    r = re.compile(rx, re.I); per = {}
    for g, d in TXT.items():
        nf = nh = 0
        for p, t in d.items():
            h = len(r.findall(t))
            if h: nf += 1; nh += h
        per[g] = (nf, nh)
    ch, lb, pt, st, ln, gl = (per[k] for k in ("chapters", "labs", "parts", "start", "learn", "glossary"))
    teach_hits = ch[1] + lb[1] + pt[1] + st[1] + ln[1] + gl[1]
    if ch[1] >= 3 and (ln[1] + gl[1]) >= 1: v = "TAUGHT"
    elif ch[1] >= 3: v = "TAUGHT, no quiz/glossary"
    elif teach_hits >= 1: v = "MENTIONED"
    elif per["notes"][1] + per["other"][1] >= 1: v = "DIARY ONLY"
    else: v = "MISSING"
    rows.append((area, name, per, v))
out = ["area | concept | chapters(files/hits) | labs | parts+start | learn | glossary | notes | other | VERDICT"]
for area, name, per, v in rows:
    f = lambda k: f"{per[k][0]}/{per[k][1]}"
    out.append(f"{area} | {name} | {f('chapters')} | {f('labs')} | {per['parts'][0] + per['start'][0]}/{per['parts'][1] + per['start'][1]} | {f('learn')} | {f('glossary')} | {f('notes')} | {f('other')} | {v}")
cnt = collections.Counter(v for *_, v in rows)
out.append("\nTOTALS: " + ", ".join(f"{k} {n}" for k, n in cnt.most_common()))
sizes = {g: sum(len(t) for t in d.values()) // 1024 for g, d in TXT.items()}
out.append("KB by group: " + ", ".join(f"{g} {s}" for g, s in sizes.items()))
pathlib.Path(sys.argv[1]).write_text("\n".join(out), encoding="utf-8"); print("\n".join(out))
