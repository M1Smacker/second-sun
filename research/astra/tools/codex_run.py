"""Run one Codex job headless and wake Claude when it ends (Claude, 15 Nov 2026; Ahmed asked for this so he is out of the loop overnight).

Starts the Codex app's own CLI (`codex.exe exec`, a NEW chat each run) in the worktree D:\\second-sun-astra on a fresh branch made from main,
with the brief that is already committed on main under research/astra/inbox/. Codex may write only in its worktree and in data\\astra\\<NNN>.
The runner NEVER hangs unseen. It exits (so the background task wakes Claude) on the first of:
  DONE     Codex finished (exit code 0 or not); summary printed: commits, leftovers, last message.
  STALL    no new output and no change in the worktree for --idle minutes: it stops ONLY the process tree it started.
  TIMEOUT  --hours passed: same stop.
  LIMIT    Codex says its usage limit is reached: waits for the reset time if given (else 30 min steps, up to 3 h), restarts the job at most
           --retries times with "continue from the branch" added, then gives up and exits.
  REFUSED  a check before the start failed (lock held, dirty worktree, brief missing, codex.exe not found).
A heartbeat line is printed every 10 minutes. Everything Codex prints goes to data\\astra\\<NNN>\\exec-<n>.log.
Usage:
  python codex_run.py 015 research/astra/inbox/015-drop-tests.md astra/015-drop-tests [--hours 2] [--idle 25] [--model gpt-6-astra] [--effort medium]
  python codex_run.py --test          (tiny job on a scratch branch: proves model, sandbox and a commit; deletes the branch after)"""
import argparse, datetime as dt, json, os, pathlib, re, subprocess, sys, time

ASTRA = pathlib.Path(r"D:\second-sun-astra")
MAIN = pathlib.Path(r"D:\second-sun")
DATA = MAIN / "data" / "astra"
LOCK = ASTRA / ".codex_run.lock"
LIMIT_RE = re.compile(r"usage limit|rate limit|limit reached|hit your .*limit|quota", re.I)
NOISE = ("rmcp::transport", "Transport channel closed", "error decoding response body")


def now():
    return dt.datetime.now().strftime("%I:%M %p").lstrip("0").lower()


def say(*a):
    print(now(), *a, flush=True)


def git(*a, cwd=ASTRA):
    r = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def codex_exe():
    r = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-AppxPackage OpenAI.Codex).InstallLocation"],
                       capture_output=True, text=True)
    loc = r.stdout.strip()
    exe = pathlib.Path(loc) / "app" / "resources" / "codex.exe" if loc else None
    return exe if exe and exe.exists() else None


def pid_alive(pid):
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
    return str(pid) in r.stdout


def kill_tree(pid):
    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True, text=True)


def worktree_signature():
    _, head, _ = git("rev-parse", "HEAD")
    _, st, _ = git("status", "--porcelain")
    return head + "|" + st


def data_signature(outdir, depth=2):
    """Latest file change time and file count in the job's own data folder, two levels deep (17 Nov 2026: Codex 027 was stopped as STALL
    after 60 min while its replay workers were still writing logs and progress files there, because only Codex's own log and the worktree counted)."""
    newest, count = 0.0, 0
    base = len(pathlib.Path(outdir).parts)
    for root, dirs, files in os.walk(outdir):
        if len(pathlib.Path(root).parts) - base >= depth:
            dirs[:] = []
        for f in files:
            if f.startswith("exec-") or f.startswith("last-message-"):
                continue
            try:
                newest = max(newest, os.stat(os.path.join(root, f)).st_mtime)
                count += 1
            except OSError:
                pass
    return f"{newest:.0f}|{count}"


def parse_reset(text):
    """Return seconds to wait if Codex named a reset time or a delay, else None."""
    m = re.search(r"try again (?:in|after)\s+(?:(\d+)\s*h\w*)?\s*(?:(\d+)\s*m\w*)?", text, re.I)
    if m and (m.group(1) or m.group(2)):
        return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + 60
    m = re.search(r"(?:try again at|resets? at)\s+(\d{1,2}):(\d{2})\s*([AaPp][Mm])?", text)
    if m:
        h, mi = int(m.group(1)), int(m.group(2))
        if m.group(3):
            h = h % 12 + (12 if m.group(3).lower() == "pm" else 0)
        t = dt.datetime.now().replace(hour=h, minute=mi, second=0, microsecond=0)
        if t <= dt.datetime.now():
            t += dt.timedelta(days=1)
        return int((t - dt.datetime.now()).total_seconds()) + 60
    return None


def real_lines(path):
    """Count output lines that are not the known harmless MCP noise (the noise repeats forever and must not count as progress)."""
    if not path.exists():
        return 0
    return sum(1 for l in path.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not any(x in l for x in NOISE))


def tail(path, n=25):
    if not path.exists():
        return ""
    lines = [l for l in path.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip() and not any(x in l for x in NOISE)]
    return "\n  ".join(lines[-n:])


def run_once(exe, o, prompt, n, outdir):
    log = outdir / f"exec-{n}.log"
    last = outdir / f"last-message-{n}.txt"
    cmd = [str(exe), "exec", "-m", o.model, "-c", f'model_reasoning_effort="{o.effort}"', "-s", "workspace-write",
           "-c", "sandbox_workspace_write.network_access=true", "-C", str(ASTRA), "--add-dir", str(outdir), "-o", str(last), prompt]
    with open(log, "w", encoding="utf-8") as fh:
        p = subprocess.Popen(cmd, stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=str(ASTRA))
    say(f"started Codex run {n} (pid {p.pid}, model {o.model} {o.effort}); log {log}")
    t0 = last_change = last_beat = time.time()
    sig, size = worktree_signature() + "|" + data_signature(outdir), 0
    while True:
        rc = p.poll()
        if rc is not None:
            return "EXITED", rc, log, last
        s2, z2 = worktree_signature() + "|" + data_signature(outdir), real_lines(log)
        if s2 != sig or z2 != size:
            sig, size, last_change = s2, z2, time.time()
        if time.time() - last_change > o.idle * 60:
            kill_tree(p.pid)
            return "STALL", None, log, last
        if time.time() - t0 > o.hours * 3600:
            kill_tree(p.pid)
            return "TIMEOUT", None, log, last
        if time.time() - last_beat > 600:
            last_beat = time.time()
            say(f"heartbeat: run {n} alive {int((time.time() - t0) / 60)} min, {size} real log lines, last change {int((time.time() - last_change) / 60)} min ago")
        time.sleep(15)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("num", nargs="?"); a.add_argument("brief", nargs="?"); a.add_argument("branch", nargs="?")
    a.add_argument("--hours", type=float, default=2); a.add_argument("--idle", type=float, default=25)
    a.add_argument("--model", default="gpt-6-astra"); a.add_argument("--effort", default="medium")  # model: 15 Nov 2026, Astra for big jobs (023 to 025 ran on Sol by mistake)
    a.add_argument("--retries", type=int, default=2); a.add_argument("--test", action="store_true"); a.add_argument("--stalltest", action="store_true")
    o = a.parse_args()
    if o.stalltest:
        o.test = True
    if o.test:
        o.num, o.brief, o.branch, o.hours, o.idle = "test", None, "astra/test-runner", 0.25, (1.5 if o.stalltest else 8)
    elif not (o.num and o.brief and o.branch):
        sys.exit("usage: codex_run.py NNN research/astra/inbox/NNN-x.md astra/NNN-x  (or --test)")

    exe = codex_exe()
    if not exe:
        print("REFUSED: codex.exe not found (Get-AppxPackage OpenAI.Codex)"); return
    if LOCK.exists():
        try:
            held = int(LOCK.read_text().strip())
        except ValueError:
            held = 0
        if held and pid_alive(held):
            print(f"REFUSED: another runner (pid {held}) holds {LOCK}"); return
    _, st, _ = git("status", "--porcelain", "--untracked-files=no")
    if st:
        print("REFUSED: the astra worktree has uncommitted changes to tracked files (commit or stash them first):\n  " + st.replace("\n", "\n  ")); return
    if o.brief:
        rc, _, _ = git("cat-file", "-e", f"main:{o.brief}")
        if rc:
            print(f"REFUSED: brief {o.brief} is not committed on main"); return
    rc, _, _ = git("rev-parse", "--verify", "--quiet", o.branch)
    if rc == 0 and not o.test:
        print(f"REFUSED: branch {o.branch} already exists (never overwrite a Codex branch; pick a new name)"); return
    rc, _, err = git("checkout", "-B", o.branch, "main")
    if rc:
        print(f"REFUSED: could not make branch {o.branch} from main: {err}"); return
    _, base, _ = git("rev-parse", "HEAD")
    LOCK.write_text(str(os.getpid()))
    outdir = DATA / str(o.num)
    outdir.mkdir(parents=True, exist_ok=True)
    if o.stalltest:
        prompt = "Run this one shell command and wait for it to finish: powershell -Command Start-Sleep -Seconds 400 . Then reply DONE."
    elif o.test:
        prompt = ("This is a runner test. Create the file research/astra/reports/test-runner.md with one line: 'runner test ok' and the "
                  "model name you are. Do not run git commit (the runner commits for you). Then reply DONE.")
    else:
        prompt = (f"You are Codex, the helper on the Second Sun project. Read AGENTS.md (your rules; they win over anything else) and then "
                  f"the brief {o.brief}. Do the brief on the current branch {o.branch} (already checked out; do not switch branches). "
                  f"Write any data only under data/astra/{o.num}/. Do NOT run git commit or any git command that writes (the Windows sandbox blocks git's own files; the runner commits everything you leave in the worktree when you finish). Never push. "
                  f"Write your report as research/astra/reports/{o.num}-report.md. End your final message with one line: "
                  f"DONE, PARTIAL or BLOCKED, and why.")
    status, rc, log, last, n, waited = None, None, None, None, 0, 0
    try:
        while True:
            n += 1
            status, rc, log, last = run_once(exe, o, prompt, n, outdir)
            text = (log.read_text(encoding="utf-8", errors="replace") if log.exists() else "")[-4000:]
            if status == "EXITED" and LIMIT_RE.search(text) and n <= o.retries:
                wait = parse_reset(text)
                if wait is None:
                    if waited >= 3 * 3600:
                        status = "LIMIT"; break
                    wait = 1800
                waited += wait
                status = "LIMIT"
                say(f"LIMIT: Codex usage limit; waiting {int(wait / 60)} min, then continuing the same job (try {n + 1})")
                time.sleep(wait)
                prompt += " NOTE: a previous run of this job stopped at the usage limit; check git log on this branch and continue from where it stopped."
                continue
            if status == "EXITED" and LIMIT_RE.search(text):
                status = "LIMIT"
            elif status == "EXITED":
                status = "DONE"
            break
    finally:
        LOCK.unlink(missing_ok=True)
    _, left0, _ = git("status", "--porcelain")
    if left0:                                          # Codex cannot write git's files from its sandbox: commit for it
        first = "(no final message)"
        if last and last.exists():
            first = next((l.strip() for l in last.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()), first)
        git("add", "-A")
        git("commit", "-q", "-m", f"Codex job {o.num} ({status}): {first[:150]}", "-m", "Committed by codex_run.py for Codex (sandboxed).")
    _, commits, _ = git("log", "--format=%h %s", f"{base}..HEAD")
    _, left, _ = git("status", "--porcelain")
    msg = last.read_text(encoding="utf-8", errors="replace").strip()[-1500:] if last and last.exists() else "(no final message)"
    summary = {"status": status, "exit_code": rc, "runs": n, "branch": o.branch, "base": base, "commits": commits.splitlines(),
               "leftovers": left.splitlines(), "ended": now()}
    (outdir / "run-summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(f"{status} at {now()}: Codex job {o.num} on {o.branch}, exit code {rc}, runs {n}")
    print("commits:\n  " + (commits.replace("\n", "\n  ") or "(none)"))
    print("leftovers:\n  " + (left.replace("\n", "\n  ") or "(none)"))
    print("final message:\n  " + msg.replace("\n", "\n  "))
    if status != "DONE":
        print("log tail:\n  " + tail(log))
    if o.test:
        git("checkout", "--detach", "main")
        git("branch", "-D", o.branch)


if __name__ == "__main__":
    main()
