"""Same-moment filter (deep review 2026-10-23, section 5.6; also how Davies et al. 2026 and STANLEY handle systematics).
A real circumbinary transit happens on ONE star. If events from several different stars on the same sector and camera
fall within WINDOW_D of each other, the cause is the spacecraft (pointing jitter, scattered light), so they are FLAGGED
(never deleted) for the human vetting sheet. Seen for real in the Kepler test: one 1% dip at the same moment on Kepler-16 and Kepler-34.
events: list of dicts with tic, sector, camera, center (BTJD). Returns the same dicts plus 'same_moment_stars' (the number of
OTHER stars with an event within WINDOW_D) and 'flags'."""
import numpy as np

# Flag when 3 or more OTHER stars show an event within 0.1 d. With about 50 events spread over a 25-day sector and camera, chance
# alone flags about 4% of events at 2 others and under 0.5% at 3 others (Poisson), so 3 is used. Flags never delete an event.
WINDOW_D, MIN_OTHER = 0.1, 3


def common_time_flags(events, window_d=WINDOW_D, min_other=MIN_OTHER):
    out = [dict(e, flags=list(e.get("flags", []))) for e in events]
    groups = {}
    for e in out:
        groups.setdefault((e["sector"], e["camera"]), []).append(e)
    for evs in groups.values():
        c = np.array([e["center"] for e in evs]); tic = np.array([e["tic"] for e in evs])
        for i, e in enumerate(evs):
            near = np.abs(c - c[i]) < window_d
            n = len(set(tic[near]) - {tic[i]})
            e["same_moment_stars"] = n
            if n >= min_other:
                e["flags"].append(f"same moment on {n} other stars (spacecraft, flag only)")
    return out
