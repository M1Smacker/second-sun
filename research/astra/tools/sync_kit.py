"""Copy Claude's private know-how into the Codex kit (12 Nov 2026, Claude Opus 5.5).

Claude Code keeps three things outside the repo that Codex cannot see by default:
  1. the memory files      C:\\Users\\hanzl\\.claude\\projects\\D--second-sun\\memory\\*.md
  2. the auditor skill     C:\\Users\\hanzl\\.claude\\skills\\second-sun-auditor\\ (SKILL.md, examples.md)
  3. the my-take skill     D:\\second-sun\\.claude\\skills\\my-take\\SKILL.md (already in the repo, copied for Codex)
This script copies them into the repo: memory -> research/astra/claude-memory/, skills -> .agents/skills/ (the
folder Codex scans). The Claude originals stay the source of truth; Codex reads the copies. Claude reruns this
after any memory or skill change. It refuses to copy a file that looks like it holds a secret, and prints
every file it copied, skipped or refused (no silent skips).

Usage: D:\\second-sun\\.venv\\Scripts\\python.exe research\\astra\\tools\\sync_kit.py [--check]
  --check  copy nothing; exit 1 if any copy is out of date (for a quick 'is the kit current?' test)
"""
import re
import sys
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOME = Path.home()
MEM_SRC = HOME / ".claude" / "projects" / "D--second-sun" / "memory"
AUD_SRC = HOME / ".claude" / "skills" / "second-sun-auditor"
TAKE_SRC = ROOT / ".claude" / "skills" / "my-take" / "SKILL.md"
MEM_DST = ROOT / "research" / "astra" / "claude-memory"
SK_DST = ROOT / ".agents" / "skills"
SECRET = re.compile(rb"sk-[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{30,}|ghp_[A-Za-z0-9]{30,}|-----BEGIN [A-Z ]*PRIVATE KEY|"
                    rb"(api[_-]?key|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}", re.I)

CODEX_NOTE = """
> **Reading this as Codex (added by `research/astra/tools/sync_kit.py`; the original is Claude's skill).**
> This skill was written for Claude Code and is copied here unchanged below this box. Read it with these swaps:
> "the usage meter" / `get_usage` / "weekly points" means your own Codex usage panel (five-hour and weekly bars);
> log your rows in `research/astra/USAGE.md`, never in `research/usage-ledger.md` (that one is Claude's).
> "Opus", "Fable", "Sonnet" and "helpers" mean other models: you do not start helper agents unless the brief says so.
> "Flag for Opus or Fable" or "ask Ahmed" at a stop sign means: stop, write it under STOP SIGNS in your report, do not continue that line.
> Every rule marked [core] binds you exactly as it binds Claude. You never edit the frozen files, never push, never publish.
"""


def plan():
    """Return a list of (source bytes, destination path, label)."""
    jobs = []
    if not MEM_SRC.exists():
        print("WARNING: memory folder not found:", MEM_SRC)
    else:
        for p in sorted(MEM_SRC.glob("*.md")):
            jobs.append((p.read_bytes(), MEM_DST / p.name, "memory " + p.name))
    for name in ("SKILL.md", "examples.md"):
        p = AUD_SRC / name
        if not p.exists():
            print("WARNING: auditor skill file missing:", p)
            continue
        b = p.read_bytes()
        if name == "SKILL.md":
            t = b.decode("utf-8")
            m = re.match(r"(---\r?\n.*?\r?\n---\r?\n)", t, re.S)
            if not m:
                print("WARNING: auditor SKILL.md has no front matter; copied without the Codex note")
            else:
                t = m.group(1) + CODEX_NOTE + t[m.end():]
            b = t.encode("utf-8")
        jobs.append((b, SK_DST / "second-sun-auditor" / name, "skill second-sun-auditor/" + name))
    if TAKE_SRC.exists():
        jobs.append((TAKE_SRC.read_bytes(), SK_DST / "my-take" / "SKILL.md", "skill my-take/SKILL.md"))
    else:
        print("WARNING: my-take skill missing:", TAKE_SRC)
    return jobs


def main():
    check = "--check" in sys.argv
    jobs = plan()
    copied = same = refused = stale = 0
    for b, dst, label in jobs:
        if SECRET.search(b):
            print("REFUSED (looks like a secret):", label); refused += 1; continue
        old = dst.read_bytes() if dst.exists() else None
        if old == b:
            same += 1; continue
        if check:
            print("OUT OF DATE:", label); stale += 1; continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(b)
        print("copied:", label); copied += 1
    # memory files deleted on Claude's side are removed from the copy too (a stale rule is worse than none)
    if MEM_SRC.exists() and MEM_DST.exists():
        live = {p.name for p in MEM_SRC.glob("*.md")}
        for p in sorted(MEM_DST.glob("*.md")):
            if p.name not in live and p.name != "README.md":
                if check:
                    print("OUT OF DATE (deleted at source):", p.name); stale += 1
                else:
                    p.unlink(); print("removed (deleted at source):", p.name)
    if not check:
        MEM_DST.mkdir(parents=True, exist_ok=True)
        (MEM_DST / "README.md").write_bytes((
            "# Claude's memory, copied for Codex\n\n"
            "These files are Claude Code's private memory for Second Sun (rules Ahmed gave, decisions, lessons). "
            "They are copies; the originals live on Ahmed's PC under `C:\\Users\\hanzl\\.claude\\projects\\D--second-sun\\memory`. "
            "Start with `MEMORY.md` (the index). Older entries can be out of date: when a memory and `RESUME.md` disagree, RESUME.md wins; "
            "say so in your report.\n\n"
            f"Last synced: {datetime.datetime.now():%Y-%m-%d %H:%M} (Kuwait time on Ahmed's PC) by `research/astra/tools/sync_kit.py`.\n").encode("utf-8"))
    print(f"files: {len(jobs)}; copied {copied}; unchanged {same}; refused {refused}; out of date {stale}")
    if check and stale:
        sys.exit(1)


if __name__ == "__main__":
    main()
