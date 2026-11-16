"""Prepare a separate scorer for raw real-host controls; leave main job unchanged."""
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
S = ROOT / 'research/astra/scripts'


def main():
    text = (S / '026_score.py').read_text(encoding='utf-8')
    start = text.index('        records = []')
    end = text.index('    else:\n        records = list(D.t156_rows', start)
    text = text[:start] + '''        folder = H.OUT / 'controls-real'
        records = [(r, folder) for r in json.loads((folder / 'records.json').read_text(encoding='utf-8'))]
        assert all(str(r['star']) in guard.seen[campaign] for r, _ in records)
''' + text[end:]
    start = text.index('    identity = json.loads(')
    end = text.index('    for number, (record, folder)', start)
    text = text[:start] + '    identity = {}\n\n' + text[end:]
    old = "if mode != 'V0' and star in affected and (mode != 'V4' or (star, sec) in class_b):"
    assert old in text
    text = text.replace(old, 'if False:  # Control injections have their own common raw replay.')
    text = text.replace("brief = '003' if strict else '006'", "brief = '026'")
    text = text.replace("        if strict:\n            result.update(depth_ppm=record['depth_ppm'], duration_h=record['duration_h'])",
                        "        result['case'] = record['case']")
    old = "            hits = passing(after, star, arm, observed)"
    assert old in text
    text = text.replace(old, "            own_events = after[(after.tic == star) & after.primary & (after.kind == arm) & (after.snr >= 7)]\n            result[arm + '_hold'] = M.reason(own_events.to_dict('records'), radii.get(star)) if mode == 'V4' else None\n" + old)
    text = text.replace("choices=('planets', 'T156')", "choices=('controls',)")
    text = text.replace("choices=('V0', 'V2', 'V4')", "choices=('V2', 'V4')")
    text = '\n'.join(line.rstrip() for line in text.splitlines()) + '\n'
    compile(text, '026_control_score.py', 'exec')
    (S / '026_control_score.py').write_text(text, encoding='utf-8')
    print('Prepared independent control scorer entry point.')


if __name__ == '__main__':
    main()
