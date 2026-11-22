"""Anchored adaptation of the already-reviewed raw replay and tier scorer."""
import ast
from pathlib import Path

S = Path(__file__).parent


def replace(text, old, new, count=1):
    assert text.count(old)==count, (old[:100], text.count(old), count)
    return text.replace(old,new)


def write(name,text):
    ast.parse(text)
    (S/name).write_text(text,encoding='utf-8')


def main():
    text=(S/'030_generate.py').read_text(encoding='utf-8').replace('030','031')
    text=replace(text,'phase, identity=False):','phase, version, identity=False):')
    text=replace(text,"    N.install(S2, enabled=not identity, floor=4.5)",
                 "    C.use_grid(S2, C.GRID_V5)\n    M = importlib.import_module('031_detector')\n    M.install(S2, S3, {'B':0., 'N1':21., 'D1':8.}[version])")
    text=replace(text,"out = H.OUT / f'generated-{campaign}'","out = H.OUT / f'generated-{version}-{campaign}'")
    start=text.index("    if phase in ('planets', 'fresh'):")
    stop=text.index('    source = H.DATA',start)
    text=text[:start]+'''    if phase != 'background':
        rows = json.loads((H.OUT/'records'/f'{phase}-{campaign}.json').read_text(encoding='utf-8'))
        for r in rows:
            assert str(r['star']) in guard.seen[campaign]
            if phase.startswith('T156'):
                draws[r['star'],r['sector']].append(r)
            elif r['observed']:
                for sec in r['changed']:
                    draws[r['star'],sec].append(r)
'''+text[stop:]
    text=replace(text,"if phase == 'T156' else r['observed']", "if phase.startswith('T156') else r['observed']")
    text=replace(text,"choices=('planets', 'fresh', 'background', 'T156')", "choices=('choosing','fresh_old','T156_old','fresh_new','T156_new','background')")
    text=replace(text,"    p.add_argument('--identity', action='store_true')", "    p.add_argument('version', choices=('B','N1','D1'))\n    p.add_argument('--identity', action='store_true')")
    text=replace(text,'a.phase, a.identity)', 'a.phase, a.version, a.identity)')
    write('031_generate.py',text)

    text=(S/'030_n1_score.py').read_text(encoding='utf-8').replace('030','031')
    text=replace(text,'background_only=False):','background_only=False, version="D1", phase="choosing"):')
    text=replace(text,"    assert not baseline_run, 'Use unchanged 031_score.py for B'", "    assert version in ('B','N1','D1')\n    floor = 7. if version == 'B' else 6.5")
    text=replace(text,"    replay_phase = 'fresh' if fresh else bench", "    replay_phase = phase")
    text=replace(text,"    strict = bench == 'T156'", "    strict = phase.startswith('T156')")
    text=replace(text,"        events = [e for e in events if e[\"snr\"] >= floor]",
                 "        events = [e for e in events if e['snr'] >= (6.5 if version == 'N1' or (version == 'D1' and e['dur_h'] <= 8) else 7.)]")
    start=text.index('            opposite = buckets.get(')
    stop=text.index('                temporary = dict(revised)',start)
    text=text[:start]+'''            opposite = buckets.get(('flip' if kind == 'real' else 'real', product), [])
            flips = set()
            if version == 'B' and kind == 'flip' and strict:
                flips, uncertain = S.symmetric_matches(opposite, group, FLIP_D)
                if uncertain:
                    raise RuntimeError('Unresolved rounded coincidence')
            for i,event in enumerate(group):
                if version == 'N1' or (version == 'D1' and event['dur_h'] <= 8):
                    mirrored = N.mirrored(event, opposite)
                elif version == 'D1':
                    mirrored = event['flipmatch']  # exact pre-serialization mirror
                elif kind == 'flip':
                    mirrored = i in flips if strict else any(abs(event['center']-r['center']) < FLIP_D for r in opposite)
                else:
                    mirrored = event['flipmatch']
                revised = dict(event, repeater=i in repeated, flipmatch=mirrored)
'''+text[stop:]
    text=replace(text,"    generated = H.OUT / f'generated-{campaign}'", "    generated = H.OUT / f'generated-{version}-{campaign}'")
    text=replace(text,"            if (strict or not baseline_run) and kind == 'groups':", "            if (strict or version != 'B') and kind == 'groups':")
    text=replace(text,"    coverage = {} if baseline_run else json.loads((generated / 'counts.json').read_text(encoding='utf-8'))\n    changed_keys = set() if baseline_run else {tuple(key) for key in coverage['affected']}",
                 "    coverage = {} if version == 'B' else json.loads((generated / 'counts.json').read_text(encoding='utf-8'))\n    changed_keys = set() if version == 'B' else {tuple(key) for key in coverage['affected']}")
    start=text.index('        records = []\n        for journal')
    stop=text.index('    if background_only:',start)
    text=text[:start]+'''    records = [(r,H.OUT) for r in json.loads((H.OUT/'records'/f'{phase}-{campaign}.json').read_text(encoding='utf-8'))
               if strict or r['observed']]
    assert len(records)==len({r['trial'] for r,_ in records})
    k2_identity = None
'''+text[stop:]
    # All new trials have their own complete raw replay, including B.
    start=text.index("                brief = '003' if strict else draw_brief")
    stop=text.index('                    if path.is_file():',start)
    text=text[:start]+'''                location = generated / replay_phase / f'trial-{trial}' / str(sign)
                brief = '031'
                if version == 'B' and phase in ('choosing','fresh_old','T156_old'):
                    brief = {'choosing':'006','fresh_old':'fable-fresh','T156_old':'003'}[phase]
                    location = Path(record['_archive_folder']) / (f'trial-{trial}-{sign}' if strict else f'trial-{trial}/{sign}')
                elif version == 'N1' and phase in ('choosing','fresh_old','T156_old'):
                    brief = '030'
                    old_phase = {'choosing':'planets','fresh_old':'fresh','T156_old':'T156'}[phase]
                    location = H.OUT.with_name('030')/f'generated-{campaign}'/old_phase/f'trial-{trial}'/str(sign)
                for kind in D.KINDS:
                    path = location / kind / f'{star}_{sec}.json'
                    expected_kind = source / kind / f'{star}_{sec}.json'
                    assert path.is_file() == expected_kind.is_file(), 'Injection coverage mismatch'
'''+text[stop:]
    text=replace(text,"        variant_prior = tiers(context[own | near]) if strict and not baseline_run else None", "        variant_prior = tiers(context[own | near]) if strict and version != 'B' else None")
    text=replace(text,"    suffix = ('-fresh'", "    suffix = ('-fresh'",1)  # anchor output region below
    start=text.index('    suffix = (')
    stop=text.index("\n\nif __name__",start)
    text=text[:start]+'''    O.write_json(H.OUT / 'scored' / f'{phase}-{campaign}-{version}{"-background" if background_only else ""}.json', output,
                 default=lambda value: value.item() if isinstance(value,np.generic) else str(value))
    print(campaign,phase,version,len(output['rows']),'scored',flush=True)
'''+text[stop:]
    text=text[:text.index("if __name__")]+'''if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('campaign',choices=('g2','g3'))
    p.add_argument('phase',choices=('choosing','fresh_old','T156_old','fresh_new','T156_new'))
    p.add_argument('version',choices=('B','N1','D1'))
    p.add_argument('--background-only',action='store_true')
    a=p.parse_args()
    main(a.campaign,'T156' if a.phase.startswith('T156') else 'planets','V0',background_only=a.background_only,version=a.version,phase=a.phase)
'''
    write('031_mixed_score.py',text)
    text=(S/'030_t109.py').read_text(encoding='utf-8').replace('030','031')
    text=replace(text,"    floor = json.loads((H.OUT / 'chosen.json').read_text(encoding='utf-8'))['threshold']", "    floor = 6.5")
    text=replace(text,"generated = H.OUT / 'generated-g2/background'", "generated = H.OUT / 'generated-D1-g2/background'")
    text=replace(text,"        events = scope['bench'](events, period, C)",
                 "        key = lambda e: (e['product'],e['kind'],e['center'],e['dur_h'])\n        saved_mirrors = {key(e):e['flipmatch'] for e in events}\n        events = scope['bench'](events, period, C)")
    text=replace(text,"                e['flipmatch'] = N.mirrored(e, opposite)", "                e['flipmatch'] = N.mirrored(e, opposite) if e['dur_h'] <= 8 else saved_mirrors[key(e)]")
    start=text.index("    result = json.loads(path.read_text(encoding='utf-8'))")
    stop=text.index('    result.update(',start)
    text=text[:start]+"    result = {}\n"+text[stop:]
    text=text.replace("'N1'","'D1'").replace('N1=n1','D1=n1').replace('T109 N1:', 'T109 D1:')
    text=text.replace("note='Completed raw-light N1 groups reused, no heavy phase rerun'", "note='New D1 raw-light design-background groups, same T109 windows'")
    write('031_t109.py',text)
    print('Prepared duration replay and mixed-statistic tier scorer.')


if __name__=='__main__':
    main()
