"""Watchdog v2 for unattended runs (11 Nov 2026, Ahmed: "check if something is stuck or idle without me telling you", then "make it follow the exact python processes").
It follows named JOBS. A job is one command line fragment (for example "r1_gate.py"): the watchdog finds the python processes whose command line contains it, adds all their descendants (the multiprocessing
workers), and measures the CPU seconds of that whole tree. That separates four cases that a log file time alone cannot:
  RUNNING        the tree exists and its CPU time advances (a quiet log is fine: the job is working)
  STUCK          the tree exists, its CPU time has been flat for CPU_STALL seconds AND no watched log changed for STALL seconds
  ENDED_UNMARKED the tree is gone for more than GONE seconds and no done condition is true (crashed, killed, or finished without its mark)
  DONE           a done condition is true (file exists, or file matches a regex)
Machine checks: free disk space on the data drive, free memory, and a time jump (the loop was paused more than 2.5 x its step: the PC slept or the session froze).
It exits (which wakes the session through the background-task notice) on DONE, STUCK, ENDED_UNMARKED, a machine warning, a time jump, or the heartbeat (MAX seconds), and prints one block of state for every job.
Decisions are appended to data\\watchdog.log. It reads no event and no star id.
Usage:  python watchdog.py CONFIG.json [--once]        (--once prints the state now and exits: use it at every wake)
Config: {"max": 1800, "step": 60, "disk_gb_min": 5, "mem_gb_min": 1.0, "drive": "D:/",
         "jobs": [{"name": "G2 gates", "match": "r1_gate.py" (or a list of scripts for a chain), "logs": ["D:/.../r1_gates.log"], "done": [["D:/.../R1-GATE-RESULT-g2.txt", ""]], "stall": 1200, "cpu_stall": 600, "gone": 120, "must_run": true}]}
`must_run` false means: a missing tree is not an error until the first time it is seen (a job that has not started yet). `done` entries are [file, regex]; an empty regex means the file exists."""
import ctypes, json, os, re, shutil, subprocess, sys, time
from datetime import datetime

LOG = r"D:\second-sun\data\watchdog.log"


def say(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
    return line


def python_processes():
    """[(pid, parent pid, command line, cpu seconds)] of every python.exe, read from the Windows process table (one PowerShell call)."""
    cmd = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Select-Object ProcessId,ParentProcessId,CommandLine,UserModeTime,KernelModeTime | ConvertTo-Json -Compress")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=60).stdout.strip()
    if not out:
        return []
    data = json.loads(out)
    data = data if isinstance(data, list) else [data]
    return [(d["ProcessId"], d["ParentProcessId"], d.get("CommandLine") or "", (d["UserModeTime"] + d["KernelModeTime"]) / 1e7) for d in data]


def tree(procs, match):
    """Processes whose command line contains `match` (but not this watchdog itself) and all their descendants."""
    me = os.getpid()
    ms = match if isinstance(match, list) else [match]                  # a job can be a chain of scripts: any of them counts
    roots = {p[0] for p in procs if any(m in p[2] for m in ms) and p[0] != me and "watchdog.py" not in p[2]}
    keep, grew = set(roots), True
    while grew:
        grew = False
        for pid, ppid, _, _ in procs:
            if ppid in keep and pid not in keep and pid != me:
                keep.add(pid); grew = True
    return [p for p in procs if p[0] in keep]


def free_memory_gb():
    class MS(ctypes.Structure):
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    m = MS(); m.dwLength = ctypes.sizeof(MS)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ullAvailPhys / 2 ** 30


def done_now(job):
    for f, pat in job.get("done", []):
        if os.path.exists(f):
            if not pat:
                return f"{os.path.basename(f)} exists"
            if re.search(pat, open(f, errors="ignore").read().replace("\0", "")):
                return f"{os.path.basename(f)} matches {pat}"
    return ""


def log_age(job, now):
    ms = [os.path.getmtime(l) for l in job.get("logs", []) if os.path.exists(l)]
    return now - max(ms) if ms else None


class Job:
    def __init__(self, cfg):
        self.cfg, self.name = cfg, cfg["name"]
        self.step = cfg.get("_step", 60)
        self.seen = False                 # the tree has existed at least once
        self.gone_since = None
        self.cpu_hist = []                # (time, cpu seconds of the whole tree)
        self.state = "WAITING"
        self.note = ""

    def update(self, procs, now):
        c = self.cfg
        d = done_now(c)
        t = tree(procs, c["match"])
        cpu = sum(p[3] for p in t)
        if t:
            self.seen = True; self.gone_since = None
            self.cpu_hist.append((now, cpu)); self.cpu_hist = [h for h in self.cpu_hist if now - h[0] <= c.get("cpu_stall", 600) + 120]
        else:
            self.gone_since = self.gone_since or now
        la = log_age(c, now)
        info = f"{len(t)} processes, tree CPU {cpu:.0f} s" + (f", newest log change {int(la)} s ago" if la is not None else "")
        if d:
            self.state, self.note = "DONE", f"{d}; {info}"
        elif t:
            old = [h for h in self.cpu_hist if now - h[0] >= c.get("cpu_stall", 600) - 5]
            flat = bool(old) and (cpu - old[0][1]) < 5.0
            quiet = la is not None and la > c.get("stall", 1200)
            if flat and quiet:
                self.state, self.note = "STUCK", f"CPU flat for {int(now - old[0][0])} s (added {cpu - old[0][1]:.1f} s) and no log change for {int(la)} s; {info}"
            else:
                span = [h for h in self.cpu_hist if now - h[0] >= 0.9 * self.step]
                rate = (cpu - span[-1][1]) / (now - span[-1][0]) if span else None
                self.state, self.note = "RUNNING", (f"about {rate:.1f} cores busy; " if rate is not None else "first sample, rate not known yet; ") + info
        elif self.seen and now - self.gone_since > c.get("gone", 120):
            self.state, self.note = "ENDED_UNMARKED", f"no process for {int(now - self.gone_since)} s and no done mark; {info}"
        elif not self.seen and c.get("must_run", True) and self.gone_since and now - self.gone_since > c.get("gone", 120) + 240:
            self.state, self.note = "ENDED_UNMARKED", f"never seen running after {int(now - self.gone_since)} s; {info}"
        else:
            self.state, self.note = "WAITING", info
        return self.state


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    once = "--once" in sys.argv
    step, mx = cfg.get("step", 60), cfg.get("max", 1800)
    jobs = [Job(dict(j, _step=step)) for j in cfg["jobs"]]
    t0, last = time.time(), time.time()
    prev = {}
    while True:
        now = time.time()
        gap = now - last
        procs = python_processes()
        for j in jobs:
            j.update(procs, now)
        warn = []
        gb = shutil.disk_usage(cfg.get("drive", "D:/")).free / 2 ** 30
        if gb < cfg.get("disk_gb_min", 5):
            warn.append(f"DISK LOW: {gb:.1f} GB free")
        mem = free_memory_gb()
        if mem < cfg.get("mem_gb_min", 1.0):
            warn.append(f"MEMORY LOW: {mem:.1f} GB free")
        if gap > 2.5 * step and not once and now - t0 > step:
            warn.append(f"TIME JUMP: {int(gap)} s since the last check (the PC slept or the session froze)")
        last = now
        for j in jobs:
            if prev.get(j.name) != j.state:
                say(f"{j.name}: {prev.get(j.name, '-')} -> {j.state} ({j.note})")
                prev[j.name] = j.state
        attention = [j for j in jobs if j.state in ("DONE", "STUCK", "ENDED_UNMARKED")]
        if once or attention or warn or now - t0 > mx:
            reason = "STATE NOW" if once else ("EVENT" if attention or warn else f"HEARTBEAT after {int(now - t0)} s")
            lines = [f"{datetime.now():%H:%M:%S} watchdog {reason}: disk {gb:.0f} GB free, memory {mem:.1f} GB free, python processes {len(procs)}"]
            lines += [f"  {j.name}: {j.state}; {j.note}" for j in jobs] + [f"  WARNING: {w}" for w in warn]
            print("\n".join(lines))
            if not once:
                say(f"exit {reason}: " + " | ".join(f"{j.name} {j.state}" for j in jobs) + (" | " + "; ".join(warn) if warn else ""))
            return
        time.sleep(step)


if __name__ == "__main__":
    main()
