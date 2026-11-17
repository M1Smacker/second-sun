"""Adapt the reviewed scorer, preserving B and T156 novelty semantics."""
from pathlib import Path

S = Path(__file__).parent


def main():
    s = (S / '025_score.py').read_text(encoding='utf-8')
    s = s.replace('025', '027').replace("import_module('023_outputs')", "import_module('027_outputs')")
    s = s.replace("'B+C96+DS', 'B+C96+M1'", "'K2', 'B+C96+M1'")
    s = s.replace('    return [baseline, baseline and within_cap, shaped, shaped and within_cap]',
                  "    event['gap_dump'] = known or ('momentum dump' in flags and uneven)\n    r2 = tier_of(event) in S.TIERS\n    return [baseline, baseline and within_cap, shaped, r2 and within_cap]")
    s = s.replace("def main(campaign, bench, mode, limit=None, baseline_run=False):", "def main(campaign, bench, mode, limit=None, baseline_run=False, floor=7.):\n    assert mode == 'V0'")
    s = s.replace("    coverage = json.loads((generated / 'counts.json').read_text(encoding='utf-8'))", "    coverage = {} if baseline_run else json.loads((generated / 'counts.json').read_text(encoding='utf-8'))")
    s = s.replace("if strict and kind == 'groups':", "if (strict or not baseline_run) and kind == 'groups':")
    s = s.replace("            if path.exists():\n                group", "            assert path.is_file() == (source / kind / path.name).is_file(), 'Background coverage mismatch'\n            if path.exists():\n                group")
    s = s.replace('(events.snr >= 7)', '(events.snr >= floor)').replace('(ranked.snr >= 7)', '(ranked.snr >= floor)').replace('(after.snr >= 7)', '(after.snr >= floor)')
    s = s.replace('rows=[], background=[], identity_mismatches=0)', 'rows=[], background=[], candidates=[], identity_mismatches=0, floor=floor)')
    s = s.replace('            if any(accepted):', '            if True:')
    s = s.replace("        for index, accepted in flags.items():", "        diagnostic_pools = {key: g.to_dict('index') for key, g in ranked.groupby(['tic', 'sector', 'product'], sort=False)}\n        for index, accepted in flags.items():")
    s = s.replace("                output['background'].append(event)", "                pool = diagnostic_pools[event['tic'], event['sector'], event['product']]\n                event['holds'] = hold_details(ranked.loc[index].to_dict(), index, pool, intervals, C.tier_of, radii.get(event['tic']))\n                output['candidates'].append(event)\n                if any(accepted):\n                    output['background'].append(event)")
    s = s.replace('            if baseline_run:\n                expected', '            if baseline_run and floor == 7.:\n                expected')
    s = s.replace("    suffix = '-smoke' if limit is not None else ''", "    suffix = ('-smoke' if limit is not None else '') + (f'-floor{floor:g}' if floor != 7. else '')")
    # Match saved K2 trial by trial, not just its headline count.
    marker = "    for number, (record, folder) in enumerate(records):"
    insertion = """    k2_identity = None
    if baseline_run and not strict and floor == 7.:
        old = json.loads(D.read(guard, H.OUT.with_name('fable-f4') / f'x6-planets-{campaign}-V0.json', 'fable-f4'))
        col = old['configs'].index('B+C96*R2')
        k2_identity = {r['trial']: {arm: r[arm][col] for arm in ('real', 'flip')} for r in old['rows']}
"""
    s = s.replace(marker, insertion + '\n' + marker)
    s = s.replace("        output['rows'].append(result)", "        if k2_identity is not None:\n            assert all(result[arm][3] == k2_identity[trial][arm] for arm in ('real', 'flip')), 'K2 identity differs'\n        output['rows'].append(result)")
    s = s.replace("    parser.add_argument('--baseline', action='store_true')", "    parser.add_argument('--baseline', action='store_true')\n    parser.add_argument('--floor', type=float, default=7.)")
    s = s.replace('arguments.limit, arguments.baseline)', 'arguments.limit, arguments.baseline, arguments.floor)')
    # Diagnostic flags are recomputed with the same common OAE pool. Counts overlap.
    diag = '''
def hold_details(row, index, rivals, intervals, tier_of, cap):
    event = dict(row)
    event['dominated'] = any(other != index and rival['snr'] >= event['snr']
        and 1.5 * event['dur_h'] / 24 <= abs(event['center'] - rival['center']) <= 6.85
        and not any(truth(rival.get(flag)) for flag in LABELS) for other, rival in rivals.items())
    known = any(event['center'] + event['dur_h']/48 >= a and event['center'] - event['dur_h']/48 <= b
                for a, b in intervals.get(event['sector'], ()))
    text = str(event.get('flags') or '')
    uneven = any(not finite(v) or abs(v) > .25 for v in (event.get('lift_pre'), event.get('lift_post')))
    result = []
    for variant in ('B', 'K2'):
        e = dict(event)
        e['gap_dump'] = (e['gap_dump'] or known) if variant == 'B' else known or ('momentum dump' in text and uneven)
        holds = {f: truth(e.get(f)) for f in ('step', 'ramp', 'repeater', 'dominated')}
        holds.update(dump=('momentum dump' in text and (variant == 'B' or uneven)),
                     gap_edge=('gap edge' in text and variant == 'B'), known=known,
                     cap=(variant == 'K2' and cap is not None and e['depth_ppm'] > cap), tier=tier_of(e))
        result.append(holds)
    return result

'''
    s = s.replace('\ndef main(', diag + '\ndef main(')
    (S / '027_score.py').write_text(s, encoding='utf-8')
    print('Prepared B and K2 scorer with historical trial identity assertions.')


if __name__ == '__main__':
    main()
