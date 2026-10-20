"""Mission readiness score (0 to 100) for the book's home page. Pure functions; hooks.py renders the result.

What the number means: how complete and how well built OUR PLAN is. It is not the chance of finding a planet.
Rules (all enforced at build time, a break fails `mkdocs build --strict`):
  - stage weights add up to 100; item weights add up to their stage's weight;
  - credit is 0 to 1; any credit above 0 needs evidence ("claim:F-054", "file:pipeline/detect_v2.py", "url:https://...");
    a claim id must exist in data/claims.csv and a file must exist in the repo;
  - `auto` items are computed from files (rows of a results file; the number of real candidates), never typed;
  - every change to a typed credit must be logged: the `changes` deltas must add up to the typed (non-auto) total.
"""
import datetime
from pathlib import Path


def _rows(path):
    """Data rows of a csv-like file: not blank, not a # comment, minus one header line. Missing file = 0."""
    if not path.is_file():
        return 0
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.lstrip().startswith("#")]
    return max(len(lines) - 1, 0)


def score(m, repo_root, claim_ids, n_candidates, today=None):
    """Validate the rubric `m` and return the score. Raises ValueError with a plain message on any rule break."""
    repo_root, today = Path(repo_root), today or datetime.date.today()
    stages, out_stages, typed, auto_total = m.get("stages") or [], [], 0.0, 0.0
    if abs(sum(s["weight"] for s in stages) - 100) > 1e-9:
        raise ValueError(f"mission.yml: stage weights add up to {sum(s['weight'] for s in stages)}, not 100")
    for s in stages:
        if abs(sum(i["weight"] for i in s["items"]) - s["weight"]) > 1e-9:
            raise ValueError(f"mission.yml: items of stage {s['id']!r} add up to {sum(i['weight'] for i in s['items'])}, not {s['weight']}")
        items, got = [], 0.0
        for i in s["items"]:
            auto = i.get("auto")
            if auto:
                if "rows_of" in auto:
                    credit = min(_rows(repo_root / auto["rows_of"]) / auto["of"], 1.0)
                elif "candidates_at_least" in auto:
                    credit = 1.0 if n_candidates >= auto["candidates_at_least"] else 0.0
                else:
                    raise ValueError(f"mission.yml: unknown auto rule in {i['what']!r}")
            else:
                credit = i.get("credit", 0)
                if not 0 <= credit <= 1:
                    raise ValueError(f"mission.yml: credit {credit} for {i['what']!r} is outside 0 to 1")
                if credit > 0 and not i.get("evidence"):
                    raise ValueError(f"mission.yml: {i['what']!r} has credit but no evidence (no proof, no points)")
            for ev in i.get("evidence") or []:
                kind, _, ref = str(ev).partition(":")
                if kind == "claim" and ref not in claim_ids:
                    raise ValueError(f"mission.yml: evidence {ev!r} for {i['what']!r} is not in data/claims.csv")
                elif kind == "file" and not (repo_root / ref).exists():
                    raise ValueError(f"mission.yml: evidence {ev!r} for {i['what']!r}: no such file in the repo")
                elif kind not in ("claim", "file", "url"):
                    raise ValueError(f"mission.yml: evidence {ev!r} must start with claim:, file: or url:")
            pts = i["weight"] * credit
            got += pts
            (auto_total, typed) = (auto_total + pts, typed) if auto else (auto_total, typed + pts)
            items.append(dict(what=i["what"], weight=i["weight"], credit=credit, points=pts, evidence=i.get("evidence") or [],
                              auto=bool(auto), note=i.get("note", "")))
        out_stages.append(dict(id=s["id"], name=s["name"], weight=s["weight"], points=got, items=items, blurb=s.get("blurb", "")))
    changes = m.get("changes") or []
    for c in changes:
        if not isinstance(c.get("date"), datetime.date) or c["date"] > today:
            raise ValueError(f"mission.yml: change {c!r} needs a date that is not in the future")
        if not str(c.get("why", "")).strip() or not isinstance(c.get("delta"), (int, float)):
            raise ValueError(f"mission.yml: change {c!r} needs a numeric delta and a reason")
    if abs(sum(c["delta"] for c in changes) - typed) > 0.011:
        raise ValueError(f"mission.yml: the logged changes add up to {sum(c['delta'] for c in changes):.2f} but the typed credits add up to "
                         f"{typed:.2f}. Log every change to a credit in `changes` (date, delta, why).")
    total = typed + auto_total
    return dict(total=total, typed=typed, auto=auto_total, stages=out_stages, changes=sorted(changes, key=lambda c: c["date"], reverse=True),
                updated=max((c["date"] for c in changes), default=None))
