"""Three deterministic design-seen group replays. All detailed evidence stays local."""
import importlib
import json
import os
from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module("002_harness")


def canonical(events):
    return sorted(json.dumps(e, sort_keys=True, allow_nan=True) for e in events)


def main():
    # Child-process settings required for this explicitly authorized run.
    os.environ["NUMBA_NUM_THREADS"] = "2"
    os.environ["SS_SET"] = "g3"
    os.environ["VESPER_OPTS"] = "c6,p1"
    guard = H.Guard()
    guard.start()
    references = guard.allow_machine_inputs("g3")
    import stage3 as S3
    import stage2_search as S2
    import stage3_core as C

    stored = H.DATA / "stage3_g3" / ("r1dev_g3_seen_" + H.DEVELOPMENT_HASH)
    selected = [p for p in sorted((stored / "groups").glob("*.json"))
                if p.stem.split("_")[0] in guard.seen["g3"]][:3]
    if len(selected) != 3:
        raise RuntimeError("Insufficient eligible groups")
    destination = H.OUT / ("replay_" + uuid.uuid4().hex[:8])
    destination.mkdir()
    results = []
    for index, path in enumerate(selected, 1):
        guard.allow_design_file(path)
        expected = json.loads(path.read_text(encoding="utf-8"))
        star, sector = map(int, path.stem.split("_"))
        paths = [H.DATA / "g3" / str(star) / m["file"] for m in expected["meta"]]
        for light in paths:
            guard.allow_design_file(light)
        group_dir = destination / str(index) / "groups"
        group_dir.mkdir(parents=True)
        S3._init3(group_dir, "g3", C.GRID_V5)
        S2.S["spoc_by_sector"] = {s: str(p) for s, p in references.items()}
        output = Path(S3.do_group3((star, sector, list(map(str, paths)))))
        actual = json.loads(output.read_text(encoding="utf-8"))
        equal = canonical(actual["events"]) == canonical(expected["events"])
        errors = sum(str(m.get("status", "")).startswith("ERROR") for m in actual["meta"])
        results.append(dict(group=index, expected_events=len(expected["events"]),
                            actual_events=len(actual["events"]), equal=equal, errors=errors))
        print(json.dumps(results[-1]), flush=True)
        if not equal or errors:
            break
    (destination / "summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    if len(results) != 3 or not all(r["equal"] and not r["errors"] for r in results):
        raise RuntimeError("Replay failed; stop sign")
    print("Primary group events identical in 3 of 3; SAP and final union pending.", flush=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Replay stopped: {type(error).__name__}", flush=True)
        raise SystemExit(1)
