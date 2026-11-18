"""Lock the lowest threshold meeting BOTH pre-written background limits."""
import json
from pathlib import Path

OUT = Path(r'D:\second-sun-astra\data/astra/030')
FLOORS = (4.5, 5., 5.5, 6., 6.5, 7.)


def choose(rows):
    assert [r['floor'] for r in rows] == list(FLOORS)
    return next((r['floor'] for r in rows if r['real'] <= 174 and r['upside_down'] <= 79), None)


def main():
    rows = []
    for floor in FLOORS:
        suffix = '-background' + (f'-floor{floor:g}' if floor != 7 else '')
        docs = [json.loads((OUT / f'planets-{c}-V0{suffix}.json').read_text(encoding='utf-8')) for c in ('g2', 'g3')]
        assert all(not d['rows'] and d['floor'] == floor for d in docs)
        counts = [sum(e['kind'] == arm and e['options'][0] for d in docs for e in d['background']) for arm in ('real', 'flip')]
        rows.append(dict(floor=floor, real=counts[0], upside_down=counts[1], eligible=counts[0] <= 174 and counts[1] <= 79))
    chosen = choose(rows)
    result = dict(threshold=chosen, alarm_curve=rows, rule='lowest threshold with real <= 174 AND upside_down <= 79')
    target = OUT / 'chosen.json'
    if target.exists():
        assert json.loads(target.read_text(encoding='utf-8')) == result, 'Existing threshold decision differs; STOP'
    else:
        target.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
