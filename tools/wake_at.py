"""Sleep until a clock time, then exit, so a background task wakes Claude (Claude, 15 Nov 2026; Ahmed's overnight rule:
resume 1 minute after each 5-hour reset). Prints a heartbeat each hour. Never runs past the target time plus one minute.
Usage: python tools/wake_at.py 06:31 "reason" """
import datetime as dt, sys, time
h, m = map(int, sys.argv[1].split(":")); why = sys.argv[2] if len(sys.argv) > 2 else ""
t = dt.datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
if t <= dt.datetime.now():
    t += dt.timedelta(days=1)
print(f"waiting until {t:%I:%M %p} ({why})", flush=True)
while (left := (t - dt.datetime.now()).total_seconds()) > 0:
    time.sleep(min(left, 3600))
    if (t - dt.datetime.now()).total_seconds() > 60:
        print(f"{dt.datetime.now():%I:%M %p} still waiting", flush=True)
print(f"WAKE at {dt.datetime.now():%I:%M %p}: {why}. Resume from research/stage3/BOOK3-BUILD-PLAN-2026-11-15.md (log at the bottom) and RESUME.md.")
