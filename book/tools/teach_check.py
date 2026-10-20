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
