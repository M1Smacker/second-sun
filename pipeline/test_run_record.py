"""Checks for run_record (T142): python test_run_record.py (prints ok). Each check is one that a broken record would fail."""
import json, pathlib, tempfile
import run_record as R

d = pathlib.Path(tempfile.mkdtemp())
a = d / "table.csv"; a.write_text("tic,p\n1,2.5\n", encoding="utf-8")
sub = d / "folder"; sub.mkdir(); (sub / "x.json").write_text("{}", encoding="utf-8"); (sub / "y.json").write_text("[1]", encoding="utf-8")
run = d / "run"
rec = R.write(run, {"table": a, "folder": sub}, frozen_hash="abc", extra=dict(note="test"))
on_disk = json.loads((run / R.NAME).read_text(encoding="utf-8"))
assert on_disk["inputs"]["table"]["size"] == a.stat().st_size and len(on_disk["inputs"]["table"]["sha256"]) == 64
assert on_disk["inputs"]["folder"]["files"] == 2 and on_disk["frozen_hash"] == "abc" and on_disk["packages"]["numpy"] != "not installed"
assert len(on_disk["git_head"]) == 40, on_disk["git_head"]                      # the record names the exact code
assert R.verify(run) == []                                                        # nothing changed yet
a.write_text("tic,p\n1,2.6\n", encoding="utf-8")                                  # same size, one character changed
assert any(x.startswith("table: sha256") for x in R.verify(run)), R.verify(run)   # a silent edit is caught by the hash, not the size
(sub / "z.json").write_text("{}", encoding="utf-8")
assert any(x.startswith("folder: files") for x in R.verify(run))                  # a file added to an input folder is caught
try:
    R.write(run, {"table": a}); raise AssertionError("overwrote an existing record")
except FileExistsError:
    pass
try:
    R.write(d / "run2", {"gone": d / "nope.csv"}); raise AssertionError("wrote a record with a missing input")
except FileNotFoundError:
    assert not (d / "run2" / R.NAME).exists()
print("test_run_record ok")
