r"""Same-day lesson rule guard (2026-10-20): how many work commits has the book not taught yet?

Counts commits that touch pipeline/, research/, targets/ or labs/ made AFTER the newest commit that touched
book/docs/field-notes/. Run:  .venv-docs\Scripts\python.exe book\tools\teach_check.py
Exit code 0 always (it's a reminder, not a gate); prints "Book is N commits behind" and lists them.
"""
import pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[2]
git = lambda *a: subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, check=True).stdout.split("\n")
last_note = next(iter(git("log", "-1", "--format=%H", "--", "book/docs/field-notes")), "").strip()
rng = [f"{last_note}..HEAD"] if last_note else []
behind = [l for l in git("log", "--format=%h %ad %s", "--date=short", *rng, "--", "pipeline", "research", "targets", "labs") if l]
print(f"Book is {len(behind)} commit{'s' * (len(behind) != 1)} behind (last field note: {last_note[:7] or 'none'})")
for l in behind:
    print("  ", l)
# Readiness number: when was it last reviewed? (reminder only; edit book/progress/mission.yml and log the change)
last_mission = next(iter(git("log", "-1", "--format=%H", "--", "book/progress/mission.yml")), "").strip()
since = [l for l in git("log", "--format=%h %s", f"{last_mission}..HEAD", "--", "experiments", "pipeline", "targets", "labs") if l] if last_mission else []
print(f"Readiness number: {len(since)} work commit{'s' * (len(since) != 1)} since book/progress/mission.yml was last edited" + (" (does any credit, evidence or status cell need updating?)" if since else ""))
