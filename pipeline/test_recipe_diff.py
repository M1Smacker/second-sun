"""Test of the recipe diff gate on the two real run pairs of 2 Nov 2026 (needs the run folders on this PC): the 29 Oct development run against the 2 Nov one must be refused (manifest, best-product table and
code differ), the fresh 0.8.0 baseline against the 2 Nov one must pass with the options as the only difference. Usage: python test_recipe_diff.py"""
import contextlib, io
import recipe_diff as R

def run(a, b):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = R.main(a, b)
    return code, buf.getvalue()

code, out = run("dev_73f62615e365", "dev_8bbb1568d6a3")
assert code == 1 and "manifest:" in out and "best_product:" in out and "NOT LIKE FOR LIKE" in out, out
code, out = run("dev_428c5fb454cd", "dev_8bbb1568d6a3")
assert code == 0 and "DIFFERENCES OTHER THAN OPTIONS" not in out and "like for like" in out, out
code, out = run("dev_8bbb1568d6a3", "dev_8bbb1568d6a3")
assert code == 0 and "['c6', 'dg', 'fl', 'nd'] against ['c6', 'dg', 'fl', 'nd']" in out, out
print("recipe_diff tests passed: the 29 Oct baseline is refused, the fresh baseline passes, a run against itself passes")
