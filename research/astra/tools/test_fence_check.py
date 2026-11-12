"""Test that fence_check.py can FAIL (a check that cannot fail proves nothing). 12 Nov 2026.
Builds two fake Codex session folders in a temp dir: a clean one and one with a fenced id and a search command.
Usage: D:\\second-sun\\.venv\\Scripts\\python.exe research\\astra\\tools\\test_fence_check.py
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fence_check as F  # noqa: E402

fa, fb, every = F.fences()
assert len(fa) >= 500 and len(fb) >= 700, (len(fa), len(fb))
one_a = next(iter(fa))
with tempfile.TemporaryDirectory() as td:
    clean = Path(td) / "clean"; clean.mkdir()
    (clean / "s.jsonl").write_text(json.dumps({"cmd": "python research/astra/scripts/count.py", "out": "rows 704"}) + "\n", encoding="utf-8")
    dirty = Path(td) / "dirty"; dirty.mkdir()
    (dirty / "s.jsonl").write_text(json.dumps({"cmd": "SS_SET=g1 python pipeline/stage2_search.py", "out": f"star {one_a}"}) + "\n", encoding="utf-8")
    v1 = F.main(["--since", "2000-01-01", "--sessions", str(clean), "--no-data-scan", "--no-branches"])
    v2 = F.main(["--since", "2000-01-01", "--sessions", str(dirty), "--no-data-scan", "--no-branches"])
assert v1 == "CLEAN", v1
assert v2 == "NEEDS A LOOK", v2
print("TEST PASSED: clean log -> CLEAN, log with a fenced id and a search command -> NEEDS A LOOK")
