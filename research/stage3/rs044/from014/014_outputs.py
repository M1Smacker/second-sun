"""Output layout shared by replay generation, preflight and scoring."""
import json


def worker_results(root, mode, campaign, slots):
    """Validate all expected workers before scoring any events."""
    results = []
    for index in range(slots):
        folder = root / f'{mode}-{campaign}-{index}'
        counts = folder / 'counts.json'
        if folder.resolve() != root.resolve() / folder.name or not counts.is_file():
            raise RuntimeError(f'Missing completed worker results: {folder.name}')
        if counts.resolve() != folder.resolve() / 'counts.json':
            raise PermissionError(f'Worker completion record escapes folder: {folder.name}')
        results.append((folder, json.loads(counts.read_text(encoding='utf-8'))))
    return results


def write_json(path, data, **kwargs):
    pending = path.with_suffix('.pending.json')
    pending.write_text(json.dumps(data, **kwargs), encoding='utf-8')
    pending.replace(path)
