"""Append burn-1 downloads (sizes measured on disk) to research/downloads.csv."""
import json, datetime, pathlib
here = pathlib.Path(__file__).parent
d = json.loads((here / "recovery_results.json").read_text())
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
root = pathlib.Path(r"D:\second-sun")
lines = []
for s, size, path in d["sizes"]:
    rel = pathlib.Path(path).relative_to(root)
    lines.append(f"{now},SPOC 2-min LC TIC 260128333 S{s},MAST via lightkurve,{size},{rel},recovery test of published TOI-1338 b transits,burn-1")
s3 = next((root / "data/burn-1/lk/mastDownload/HLSP").glob("*eleanor-lite*s0003*/*.fits"))
lines.append(f"{now},GSFC-ELEANOR-LITE 30-min FFI LC TIC 260128333 S3,MAST via lightkurve,{s3.stat().st_size},{s3.relative_to(root)},"
             "S3 has no SPOC 2-min LC; checked FFI product (method not applicable at 30-min cadence),burn-1")
with open(here.parent / "downloads.csv", "a", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("\n".join(lines))
