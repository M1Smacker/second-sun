"""Read-only source checks plus guarded output-boundary runtime tests."""
import ast
import hashlib
import importlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
H = importlib.import_module('032_harness')


def main():
    scripts = Path(__file__).parent
    files = sorted(scripts.glob('032_*.py')) + sorted((scripts/'032_harness').glob('*.py'))
    for path in files:
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    guard = H.Guard()
    provenance = guard.start()
    denied = 0
    # Dispatch audit events directly: do not open or change forbidden files.
    for path, flags in [(H.OUT.with_name('031')/'probe.txt', os.O_WRONLY),
                        (H.DATA/'g1'/'probe.fits', os.O_RDONLY),
                        (H.ROOT/'AGENTS.md', os.O_WRONLY),
                        (H.OUT/'..'/'probe.txt', os.O_WRONLY)]:
        try:
            sys.audit('open', str(path), None, flags)
        except PermissionError:
            denied += 1
        else:
            raise AssertionError('Boundary test unexpectedly allowed')
    sample = json.loads((H.OUT/'fresh-controls.json').read_text(encoding='utf-8'))
    assert len(set(sample['selected'])) == 60
    assert all(str(s) in guard.seen['g2'] for s in sample['selected'])
    evidence = dict(parsed_files=len(files), copied_module_hashes=len(provenance),
                    rejected_access_events=denied, selected_design_stars=60,
                    code_sha256={p.relative_to(scripts).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
                    limitation='Source hashes recorded after launch; worker and timing code unchanged since launch. Hash equality is not semantic validation.')
    (H.OUT/'verification.json').write_text(json.dumps(evidence,indent=2), encoding='utf-8')
    print('Static parse',len(files),'files; verified',len(provenance),'copied module hashes;',denied,'access attempts rejected; 60 selected stars are design-seen.')


if __name__ == '__main__':
    main()
