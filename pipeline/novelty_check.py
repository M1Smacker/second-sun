"""Wider novelty check for a lead (BUILD T127; Claude, 14 Nov 2026). Lead stage 4 used only data/xmatch/toi.csv and cbp.csv; this asks the public
archives at lead time and writes one dated UTC sentence. NOT in the frozen hash list; it judges no event, it only says whether the star is already known.

Sources (each returns hit / no hit / error with its evidence):
  local      data/xmatch/toi.csv and cbp.csv (the old stage 4)
  nea_ps     NASA Exoplanet Archive, Planetary Systems (any planet with this TIC), with the circumbinary flag
  nea_toi    NASA Exoplanet Archive, TOI table (any TOI on this TIC, with its disposition)
  exofop     ExoFOP-TESS target page (TOIs and community TOIs, CTOIs; Planet Hunters TESS submits through CTOIs)
  simbad     SIMBAD TAP: object type and number of references for the identifier "TIC n"
  arxiv      arXiv API: papers whose text fields contain "TIC n" exactly
NOT BUILT (said, not hidden): ADS (needs a personal key; the key folder is never opened by Claude), VizieR catalogue-by-catalogue, TESS TCE bulk tables on MAST.
Verdict rule: KNOWN if any source hits; NO HIT only if every source answered and none hit; a source that failed makes it INCOMPLETE, never "novel".
Privacy: the queries send only the TIC number to public archives; the result is written under data\\ (git-ignored) by the caller, never published.
Usage: python novelty_check.py <tic>   (prints the result as JSON)"""
import datetime
import json
import pathlib
import sys

ROOT = pathlib.Path(r"D:\second-sun")
XM = ROOT / "data" / "xmatch"
TIMEOUT = 30
UA = {"User-Agent": "second-sun-novelty-check/1.0 (research script)"}


def _get(url, params=None):
    import requests
    r = requests.get(url, params=params, headers=UA, timeout=TIMEOUT)
    r.raise_for_status()
    return r


def src_local(tic):
    import pandas as pd
    toi = pd.read_csv(XM / "toi.csv")
    cbp = pd.read_csv(XM / "cbp.csv")
    t = toi[toi.tid == tic]
    c = cbp[pd.to_numeric(cbp.tic_id.astype(str).str.replace("TIC ", ""), errors="coerce") == tic]
    hits = [f"TOI {x}" for x in t.toi.tolist()] + [str(x) for x in c.get("pl_name", c.tic_id).tolist()]
    return dict(hit=bool(hits), evidence=hits)


def src_nea_ps(tic):
    q = f"select pl_name,cb_flag,disc_facility,disc_year from ps where tic_id='TIC {tic}' and default_flag=1"
    rows = _get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync", dict(query=q, format="json")).json()
    return dict(hit=bool(rows), evidence=[f"{r['pl_name']} (cb_flag {r['cb_flag']}, {r['disc_facility']} {r['disc_year']})" for r in rows])


def src_nea_toi(tic):
    q = f"select toi,tfopwg_disp from toi where tid={tic}"
    rows = _get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync", dict(query=q, format="json")).json()
    return dict(hit=bool(rows), evidence=[f"TOI {r['toi']} ({r['tfopwg_disp']})" for r in rows])


def src_exofop(tic):
    j = _get("https://exofop.ipac.caltech.edu/tess/target.php", dict(id=tic, json="")).json()
    tois = [f"TOI {str(t.get('toi')).replace('TOI', '').strip()}" for t in (j.get("tois") or [])]
    ctois = [f"CTOI {c.get('ctoi')} by {c.get('user') or c.get('source') or '?'}" for c in (j.get("ctois") or [])]
    return dict(hit=bool(tois or ctois), evidence=tois + ctois)


SIMBAD_TAP = ("https://simbad.cds.unistra.fr/simbad/sim-tap", "https://simbad.harvard.edu/simbad/sim-tap")   # main site, then the Harvard mirror (main returned 404 on 14 Nov 2026)


def src_simbad(tic):
    import pyvo
    q = f"SELECT b.main_id, b.otype, b.nbref FROM basic AS b JOIN ident AS i ON i.oidref = b.oid WHERE i.id = 'TIC {tic}'"
    last = None
    for base in SIMBAD_TAP:
        try:
            t = pyvo.dal.TAPService(base).run_sync(q).to_table()
            rows = [(str(r["main_id"]), str(r["otype"]), int(r["nbref"])) for r in t]
            break
        except Exception as exc:
            last = exc
    else:
        raise last
    # a SIMBAD entry alone is not "known as a planet host"; it is evidence to read. Hit = the object type or references mention planets.
    ev = [f"{r[0]} otype {r[1]} refs {r[2]}" for r in rows]
    planety = any(str(r[1]).strip() in ("Pl", "Pl?", "PlH") for r in rows)     # SIMBAD object types for planets and planet hosts are checked loosely
    return dict(hit=planety, evidence=ev, note="entry found (read the references)" if rows and not planety else "")


def src_arxiv(tic, names=()):
    """arXiv searches titles, abstracts and comments, not full texts, so a paper naming the star only inside the text is missed: the TIC is
    searched together with every name the other sources found (TOI numbers, planet names, the SIMBAD main identifier)."""
    import re
    import xml.etree.ElementTree as ET
    terms = [f"TIC {tic}"] + [n for n in dict.fromkeys(names) if n]
    query = " OR ".join(f'all:"{t}"' for t in terms[:8])
    r = _get("http://export.arxiv.org/api/query", dict(search_query=query, max_results=20))
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entries = ET.fromstring(r.text).findall("a:entry", ns)
    ev = [f"{e.find('a:id', ns).text.rsplit('/', 1)[-1]}: {' '.join(e.find('a:title', ns).text.split())[:90]}" for e in entries]
    return dict(hit=bool(ev), evidence=ev, searched=terms[:8])


def names_from(res):
    """Search names the other sources produced: 'TOI-1338' from 'TOI 1338.01', planet host names, the SIMBAD main identifier."""
    import re
    out = []
    for v in res.values():
        for e in v.get("evidence", []):
            m = re.match(r"(?:TOI\s*-?)?TOI\s*-?(\d+)", e) or re.match(r"TOI\s*(\d+)", e)
            if m:
                out.append(f"TOI-{m.group(1)}")
            m = re.match(r"(.+?) [a-z] \(cb_flag", e)
            if m:
                out.append(m.group(1))
            m = re.match(r"(.+?) otype ", e)
            if m and not m.group(1).startswith("TIC"):
                out.append(m.group(1).strip())
    return out


SOURCES = dict(local=src_local, nea_ps=src_nea_ps, nea_toi=src_nea_toi, exofop=src_exofop, simbad=src_simbad, arxiv=src_arxiv)   # arxiv last: it uses the names found
NOT_BUILT = ["ADS (needs a personal key)", "VizieR catalogue by catalogue", "TESS TCE bulk tables (MAST)"]


def check(tic, sources=None):
    tic = int(tic)
    res = {}
    for name, fn in (sources or SOURCES).items():
        try:
            res[name] = dict(status="ok", **(fn(tic, names_from(res)) if name == "arxiv" else fn(tic)))
        except Exception as exc:
            res[name] = dict(status="error", hit=False, evidence=[], error=f"{type(exc).__name__}: {str(exc)[:120]}")
    when = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    hits = [k for k, v in res.items() if v["hit"]]
    failed = [k for k, v in res.items() if v["status"] != "ok"]
    if hits:
        verdict = "KNOWN"
    elif failed:
        verdict = "INCOMPLETE"
    else:
        verdict = "NO HIT"
    asked = ", ".join(res)
    sentence = (f"Novelty check {when}: {verdict}. Asked {asked}." + (f" Hits: {', '.join(hits)}." if hits else "") +
                (f" Failed (not counted as no hit): {', '.join(failed)}." if failed else "") + f" Not asked: {'; '.join(NOT_BUILT)}.")
    return dict(tic=tic, when_utc=when, verdict=verdict, hits=hits, failed=failed, sources=res, sentence=sentence)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    print(json.dumps(check(sys.argv[1]), indent=1))
