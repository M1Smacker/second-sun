"""Generate guarded replay and N1 scorer from the historical 027 harness.

Every semantic edit is anchored and counted. Baseline scorer stays untouched.
"""
import ast
from pathlib import Path

S = Path(__file__).parent


def replace(source, old, new, count=1):
    assert source.count(old) == count, (old[:100], source.count(old), count)
    return source.replace(old, new)


def write(name, source):
    ast.parse(source)
    (S / name).write_text(source, encoding='utf-8')


def main():
    g = (S / '027_generate.py').read_text(encoding='utf-8').replace('027', '030')
    g = replace(g, "VESPER_OPTS='c6,p1' + ('' if identity else ',c1a')", "VESPER_OPTS='c6,p1'")
    g = replace(g, "    assert ('c1a' in V.ON) != identity", "    N = importlib.import_module('030_notch')\n    N.install(S2, enabled=not identity, floor=4.5)")
    g = replace(g, "    if phase == 'planets':", "    if phase in ('planets', 'fresh'):")
    g = replace(g, "        for p in sorted((H.DATA / 'astra/006').glob", "        draw_brief = '006' if phase == 'planets' else 'fable-fresh'\n        for p in sorted((H.DATA / 'astra' / draw_brief).glob")
    g = replace(g, "D.read(guard, p, '006')", "D.read(guard, p, draw_brief)")
    g = replace(g, "        work = work[:25]", "        work = work[:25]")
    # Existing journal sectors are shared by workers, so mkdir runs only before launch.
    g = replace(g, '            S2.GROUPS.mkdir(parents=True, exist_ok=True)', "            assert S2.GROUPS.is_dir(), 'Output folders must be pre-created'")
    g = replace(g, "            if identity:\n                canon", "            if phase == 'background' and not identity:\n                def metadata(rows):\n                    return sorted(json.dumps(dict(m, file=Path(m['file']).name), sort_keys=True) for m in rows)\n                assert metadata(group['meta']) == metadata(old['meta']), 'N1 changed untouched preprocessing metadata'\n            if identity:\n                canon")
    g = replace(g, "choices=('planets', 'background', 'T156')", "choices=('planets', 'fresh', 'background', 'T156')")
    g = g.replace('c1a', 'N1')
    write('030_generate.py', g)

    s = (S / '030_score.py').read_text(encoding='utf-8')
    s = replace(s, 'baseline_run=False, floor=7.):', 'baseline_run=False, floor=7., fresh=False, background_only=False):')
    s = replace(s, "    assert mode == 'V0'", "    assert mode == 'V0'\n    assert not baseline_run, 'Use unchanged 030_score.py for B'\n    N = importlib.import_module('030_notch')\n    draw_brief = 'fable-fresh' if fresh else '006'\n    replay_phase = 'fresh' if fresh else bench")
    s = replace(s, '    def retier(events):\n        buckets', '    def retier(events):\n        events = [e for e in events if e["snr"] >= floor]\n        buckets')
    start = s.index('            flips = set()')
    stop = s.index('                temporary = dict(revised)', start)
    s = s[:start] + '''            opposite = buckets.get(('flip' if kind == 'real' else 'real', product), [])
            for i, event in enumerate(group):
                mirrored = N.mirrored(event, opposite)
                text = [x for x in str(event.get('flags') or '').split('; ') if x != 'matched in flipped data']
                if mirrored:
                    text.append('matched in flipped data')
                revised = dict(event, repeater=i in repeated, flipmatch=mirrored, flags='; '.join(text))
''' + s[stop:]
    s = replace(s, "H.OUT.with_name('006').glob", "H.OUT.with_name(draw_brief).glob")
    s = replace(s, "D.read(guard, journal, '006')", "D.read(guard, journal, draw_brief)")
    s = replace(s, "brief = '003' if strict else '006'", "brief = '003' if strict else draw_brief")
    s = replace(s, "generation_for((star, sec)) / bench /", "generation_for((star, sec)) / replay_phase /")
    s = replace(s, "    if mode == 'V0':\n        assert identity.keys()", "    if mode == 'V0' and not fresh:\n        assert identity.keys()")
    s = replace(s, "                output['candidates'].append(event)", "                event['holds'][0].update({f: truth(ranked.loc[index].get(f)) for f in ('flipmatch', 'ecl_overlap', 'c5', 'common', 'p1_veto', 'orbit_lock')})\n                output['candidates'].append(event)")
    # Background calibration must not read any fresh outcomes or require injections.
    s = replace(s, "    for number, (record, folder) in enumerate(records):", "    if background_only:\n        records = []\n    for number, (record, folder) in enumerate(records):")
    # Save all novel crossing indices, not just an any-crossing planet boolean.
    s = replace(s, "            result[arm] = [bool(hit - pre) for hit, pre in zip(hits, prior)]",
                "            result[arm] = [bool(hit - pre) for hit, pre in zip(hits, prior)]\n            result[arm + '_crossings'] = sorted(hits[0] - prior[0])\n            result['n_crossings'] = len(observed)")
    # Retain diagnostic tier flags on all detections matching an injected crossing.
    s = replace(s, "            result[arm + '_found'] =", "            matched = detected[[any(abs(r.center - t) <= d/2 for t, d in observed) for r in detected.itertuples()]] if len(detected) else detected\n            result[arm + '_holds'] = []\n            for ix, e in matched.iterrows():\n                pool = after[(after.tic == star) & (after.sector == e['sector']) & (after['product'] == e['product'])].to_dict('index')\n                h = hold_details(e.to_dict(), ix, pool, intervals, C.tier_of, radii.get(star))[0]\n                h.update({f: truth(e.get(f)) for f in ('flipmatch', 'ecl_overlap', 'c5', 'common', 'p1_veto', 'orbit_lock')})\n                h['second_product'] = (finite(e.get('c8_best')) and e.get('c8_n', 0) > 0 and e['c8_best'] < 3) or (finite(e.get('pdc_snr')) and e['pdc_snr'] < 3)\n                result[arm + '_holds'].append(h)\n            result[arm + '_found'] =")
    s = replace(s, "    suffix = ('-smoke'", "    suffix = ('-fresh' if fresh else '') + ('-background' if background_only else '') + ('-smoke'")
    s = replace(s, "    parser.add_argument('--floor', type=float, default=7.)", "    parser.add_argument('--floor', type=float, default=7.)\n    parser.add_argument('--fresh', action='store_true')\n    parser.add_argument('--background-only', action='store_true')")
    s = replace(s, 'arguments.baseline, arguments.floor)', 'arguments.baseline, arguments.floor, arguments.fresh, arguments.background_only)')
    write('030_n1_score.py', s)
    print('Prepared N1 generator and threshold-aware scorer. No experiments run.')


if __name__ == '__main__':
    main()
