"""Tests for codex_run.py's limit detection and reset parsing (Claude, 15 Nov 2026). Run: python test_codex_run.py"""
import importlib.util, pathlib, tempfile
spec = importlib.util.spec_from_file_location("cr", pathlib.Path(__file__).with_name("codex_run.py")); cr = importlib.util.module_from_spec(spec); spec.loader.exec_module(cr)
assert cr.LIMIT_RE.search("You've hit your usage limit. Try again in 2 hours 5 minutes.")
assert cr.LIMIT_RE.search("rate limit reached")
assert not cr.LIMIT_RE.search("DONE: all tests pass")
w = cr.parse_reset("You've hit your usage limit. Try again in 2 hours 5 minutes."); assert w == 2 * 3600 + 5 * 60 + 60, w
w = cr.parse_reset("limit reached, try again in 45 minutes"); assert w == 45 * 60 + 60, w
w = cr.parse_reset("usage limit; resets at 4:05 AM"); assert w is not None and 60 <= w <= 86400 + 60, w
assert cr.parse_reset("usage limit reached") is None
p = pathlib.Path(tempfile.mkdtemp()) / "x.log"
p.write_text("ERROR rmcp::transport::worker: Transport channel closed\nreal line\n\n" + "ERROR rmcp::transport x\n" * 5, encoding="utf-8")
assert cr.real_lines(p) == 1
print("test_codex_run: 8 checks passed")
