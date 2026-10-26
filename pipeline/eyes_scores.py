"""Claude's reader for Ahmed's Eyes rounds: pulls every round from the private Firebase project with the service-account key, saves them, prints the scores.
Ahmed never sends anything: rounds arrive by themselves when he finishes them (book/docs/assets/eyes-cloud.js). Run whenever he says "look at my eye test scores".
  practice and test rounds  -> research/eyes-scores/rounds.jsonl   (fake data, safe to publish; the repo copy is the permanent record)
  real-candidate rounds     -> data/eyes-real/rounds.jsonl          (git-ignored until Ahmed and Claude decide otherwise)
Rounds from end-to-end tests (device label or source starting with 'e2e') are ignored.
Usage: python eyes_scores.py [--commit]     (--commit also commits and pushes research/eyes-scores when something is new; used by the daily task)"""
import json, pathlib, subprocess, sys
import eyes_firestore as F

ROOT = pathlib.Path(r"D:\second-sun")
PUBLIC, LOCAL = ROOT / "research" / "eyes-scores" / "rounds.jsonl", ROOT / "data" / "eyes-real" / "rounds.jsonl"


# Devices that are Claude's own browser, not Ahmed's phone. The cloud copy is create-only, so a test round that reached it cannot be deleted; it is ignored here instead.
# g5hko8: Claude's in-app browser on 24 Oct 2026, two abandoned hard-practice rounds (one answer each) made while checking the live page.
TEST_DEVICES = {"g5hko8"}


def is_test(r):
    return (str(r.get("source", "")).startswith("e2e") or str((r.get("device") or {}).get("label", "")).lower().startswith("e2e")
            or str((r.get("device") or {}).get("id", "")) in TEST_DEVICES)


def save(path, rounds):
    """Deterministic file (sorted), so an unchanged cloud gives an unchanged file. Returns True if the file changed."""
    text = "".join(json.dumps(r, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n" for r in sorted(rounds, key=lambda r: (r["t0"], r["id"])))
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == text or (old is None and not rounds):             # unchanged, or nothing to save yet: never create an empty file
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def git(*a):
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)


def main():
    rounds = [r for r in F.list_rounds() if not is_test(r)]
    real = [r for r in rounds if r.get("mode") == "real"]
    plain = [r for r in rounds if r.get("mode") != "real"]
    changed_public = save(PUBLIC, plain)
    save(LOCAL, real) if real or LOCAL.exists() else None
    print(f"read {len(rounds)} round(s) from the cloud: {len(plain)} practice/test, {len(real)} real. Public file {'updated' if changed_public else 'unchanged'}.")
    devs = {}
    for r in rounds:                                            # the book only uploads from Ahmed's devices; a device that is not his would show up here
        d = str((r.get("device") or {}).get("id", "?")); devs[d] = devs.get(d, 0) + 1
    print("devices that uploaded: " + ", ".join(f"{d} ({n})" for d, n in sorted(devs.items())) + "\n")
    rep = subprocess.run(["node", str(ROOT / "book" / "tools" / "eyes_report.mjs"), str(PUBLIC)], capture_output=True, text=True, encoding="utf-8")
    print(rep.stdout or rep.stderr)
    if "--commit" in sys.argv and changed_public:
        git("add", str(PUBLIC.relative_to(ROOT)))
        c = git("commit", "-m", f"Eyes scores: {len(plain)} round(s) pulled from the cloud\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>")
        p = git("push", "origin", "main")
        print("committed and pushed" if p.returncode == 0 else f"commit/push problem: {c.stderr.strip()} {p.stderr.strip()}")


if __name__ == "__main__":
    main()
