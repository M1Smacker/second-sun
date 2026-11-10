"""Watchdog for unattended runs (11 Nov 2026, Ahmed: "check if something is stuck or idle without me telling you").
Exits (which wakes the session through the background-task notice) when: a done condition is true, no watched log has changed for STALL seconds, no python process is running for more than 2 minutes, or MAX seconds passed (heartbeat).
Usage: WD_LOGS="a.log;b.log" WD_DONE="file::regex;;file2::" python watchdog.py MAX_SECONDS STALL_SECONDS     (a done entry with an empty regex means: the file exists)
Prints one line saying why it exited. Reads no event, no star id."""
import os, re, subprocess, sys, time

max_s, stall = int(sys.argv[1]), int(sys.argv[2])
logs = [x for x in os.environ.get("WD_LOGS", "").split(";") if x]
dones = [d.split("::", 1) for d in os.environ.get("WD_DONE", "").split(";;") if d]
t0 = time.time()


def nproc():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq python.exe"], capture_output=True, text=True).stdout
    return out.count("python.exe")


idle_since = None
while True:
    now = time.time()
    for f, pat in dones:
        if os.path.exists(f):
            txt = open(f, errors="ignore").read().replace("\0", "") if pat else ""
            if not pat or re.search(pat, txt):
                print(f"EVENT done: {f} {pat}"); sys.exit(0)
    m = max((os.path.getmtime(l) for l in logs if os.path.exists(l)), default=0)
    if logs and now - m > stall:
        print(f"STALL: no watched log changed for {int(now - m)} s; python processes {nproc()}"); sys.exit(0)
    if nproc() == 0:
        idle_since = idle_since or now
        if now - idle_since > 120:
            print("IDLE: no python process has been running for 2 minutes and nothing is marked done"); sys.exit(0)
    else:
        idle_since = None
    if now - t0 > max_s:
        print(f"HEARTBEAT after {int(now - t0)} s; newest log change {int(now - m)} s ago; python processes {nproc()}"); sys.exit(0)
    time.sleep(30)
