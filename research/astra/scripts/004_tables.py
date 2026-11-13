"""Render counts-only tables from completed bench summaries."""
import json
from pathlib import Path

OUT = Path(r'D:\second-sun-astra\data\astra\004')
LABELS = ['5 to 10', '10 to 14', '14 to 20', '20 to 27.4', '27.4 and above']


def pair(values):
    return f'{values[0]} to {values[1]}'


def ci(values):
    return f'[{100 * values[0]:.2f}, {100 * values[1]:.2f}]'


def render(variant):
    s = json.loads((OUT / f'{variant}-summary.json').read_text(encoding='utf-8'))
    name = 'Binary-locked repeater' if variant == 'repeater' else 'FIX 91 alone'
    out = [f'## {name}', '', f'Reference R {100 * s["R"][0]:.2f}% to {100 * s["R"][1]:.2f}%. '
           f'Whole-star bootstrap 95% intervals {ci(s["ci95"][0])}% to {ci(s["ci95"][1])}%.', '',
           '| Binary period (days) | Reference dip recovered (old to new) | Reference dip R (old to new) | Reference R 95% intervals (%) | All dips (old to new) | All bumps (old to new) | New paired 99% CI (points) |',
           '|---|---|---|---|---|---|---|']
    for label, b in zip(LABELS, s['bins']):
        count = b['ref_n']
        rates = [f'{100 * v / count:.2f}%' for v in b['ref_dip']]
        out.append(f'| {label} | {pair(b["ref_dip"])} / {count} | {pair(rates)} | {pair(list(map(ci, b["ref_ci95"])))} | '
                   f'{pair(b["dip"])} | {pair(b["bump"])} | {ci(b["paired_ci99"][1])} |')
    out += ['', 'All-depth columns have 400 pairs per bin. The paired interval is dip recovery minus bump recovery.', '',
            '| Sample and arm | Old to new | Gained | Lost |', '|---|---:|---:|---:|']
    for field in ('ref_dip', 'ref_bump', 'dip', 'bump'):
        counts = [sum(b[field][i] for b in s['bins']) for i in range(2)]
        gain = sum(b[field + '_gain'] for b in s['bins'])
        loss = sum(b[field + '_loss'] for b in s['bins'])
        assert counts[1] - counts[0] == gain - loss
        out.append(f'| {field.replace("ref_", "Reference ")} | {pair(counts)} | {gain} | {loss} |')
    old, new = s['background_old'], s['background_new']
    out += ['', f'Background primary tier-1 at SNR at least 7: real {old.get("real", 0)} to {new.get("real", 0)}, upside-down '
            f'{old.get("flip", 0)} to {new.get("flip", 0)}. Upside-down ceiling {s["flip_cap"]:.2f}.', '',
            '| Acceptance condition | Verdict |', '|---|---|']
    conditions = ['R rises' if variant == 'repeater' else 'R does not fall',
                  'Background upside-down count at or below ceiling', 'All paired 99% intervals contain zero']
    out.extend(f'| {condition} | {"PASS" if ok else "FAIL"} |' for condition, ok in zip(conditions, s['pass_conditions']))
    return '\n'.join(out)


if __name__ == '__main__':
    (OUT / 'report-tables.md').write_text('\n\n'.join(render(v) for v in ('repeater', 'fix91')) + '\n', encoding='utf-8')
