"""Watch a Codex branch for Claude (14 Nov 2026). Replaces the inline bash loop.
Exits (so the background task wakes Claude) on the FIRST of:
  COMMIT  a new commit on the branch (prints hash, time, subject, files changed);
  STALL   the brief's progress file (data/astra/<NNN>/*progress*.json, key "updated") has not changed for --stall minutes
          while its status is "running", or no progress file and no commit for --stall minutes;
  ERROR   an error log under data/astra/<NNN>/ grew (prints its last lines);
  TIMEOUT --hours passed.
Reads only git metadata and Codex's own data/astra/<NNN> folder; never opens star data. Polls every --every seconds (machine time, free).
Usage: python watch_codex.py astra/014-dumps-ephemerides [--every 20] [--stall 45] [--hours 3] [--once]"""
import argparse, datetime as dt, json, pathlib, subprocess, sys, time

ASTRA = pathlib.Path(r"D:\second-sun-astra")


def git(*a):
    return subprocess.run(["git", "-C", str(ASTRA), *a], capture_output=True, text=True).stdout.strip()


def now():
    return dt.datetime.now().strftime("%I:%M %p").lstrip("0").lower()


def progress(folder):
    for p in sorted(folder.glob("*progress*.json")):
        try:
            return p, json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return p, {"status": "unreadable"}
    return None, None


def errsizes(folder):
    return {p: p.stat().st_size for p in folder.glob("*error*.log")} if folder.is_dir() else {}


def main():
    a = argparse.ArgumentParser()
    a.add_argument("branch"); a.add_argument("--every", type=int, default=20); a.add_argument("--stall", type=int, default=45)
    a.add_argument("--hours", type=float, default=3); a.add_argument("--once", action="store_true")
    o = a.parse_args()
    num = o.branch.split("/")[-1].split("-")[0]
    folder = ASTRA / "data" / "astra" / num
    head0 = git("rev-parse", "--verify", "--quiet", o.branch)
    if not head0:
        sys.exit(f"ERROR no such branch {o.branch}")
    err0 = errsizes(folder)
    p, pr = progress(folder)
    last_seen, last_val = time.time(), (pr or {}).get("updated")
    print(f"{now()} watching {o.branch} at {head0[:8]}; progress: {pr}", flush=True)
    end = time.time() + o.hours * 3600
    while True:
        head = git("rev-parse", "--verify", "--quiet", o.branch)
        if head != head0:
            print(f"COMMIT at {now()}: " + git("log", "-1", "--format=%h %ad %s", "--date=format:%I:%M %p", o.branch))
            print(git("show", "--stat", "--format=", o.branch)[-1500:])
            return
        for f, s in errsizes(folder).items():
            if s > err0.get(f, 0):
                tail = f.read_text(encoding="utf-8", errors="replace").splitlines()[-8:]
                print(f"ERROR at {now()}: {f.name} grew\n  " + "\n  ".join(tail))
                return
        p, pr = progress(folder)
        val = (pr or {}).get("updated")
        if val != last_val:
            last_val, last_seen = val, time.time()
        running = pr is None or pr.get("status") == "running"
        if running and time.time() - last_seen > o.stall * 60:
            print(f"STALL at {now()}: no commit and no progress update for {o.stall} min; last progress: {pr}")
            return
        if o.once:
            print(f"{now()} no change; progress: {pr}")
            return
        if time.time() > end:
            print(f"TIMEOUT at {now()} after {o.hours} h; last progress: {pr}")
            return
        time.sleep(o.every)


if __name__ == "__main__":
    main()
