"""Adapt the reviewed raw replay, with explicit changes and no execution on import."""
import ast
from pathlib import Path

S=Path(__file__).parent


def main():
    s=(S/'027_generate.py').read_text(encoding='utf-8').replace('027','028')
    s=s.replace("'c6,p1' + ('' if identity else ',c1a')", "'c6,p1'")
    s=s.replace("assert ('c1a' in V.ON) != identity", "assert 'c1a' not in V.ON\n    original_events = S2.Prod.events\n    if not identity:\n        S2.Prod.events = lambda self, thr=7.: original_events(self, thr=4.)")
    s=s.replace("'c1a-off raw replay identity failed'", "'Orbit-off raw replay identity failed'")
    s=s.replace("else 'c1a'", "else 'SNR4 bank'")
    s=s.replace('phase, identity=False):', 'phase, identity=False, pilot=False):')
    s=s.replace("out = H.OUT / f'generated-{campaign}'", "out = H.OUT / f'{\"pilot-\" if pilot else \"\"}generated-{campaign}'")
    s=s.replace('    if identity:\n        work = work[:25]', '    if identity:\n        work = work[:25]\n    elif pilot:\n        work = work[:2]')
    s=s.replace("    p.add_argument('--identity', action='store_true')", "    p.add_argument('--identity', action='store_true')\n    p.add_argument('--pilot', action='store_true')")
    s=s.replace('a.phase, a.identity)', 'a.phase, a.identity, a.pilot)')
    s=s.replace('dict(affected=list(sectors))', 'dict(affected=[key for key, _ in work] if pilot else list(sectors))')
    s=s.replace('    completed, generated = 0, 0', '    completed, generated = 0, 0\n    import time\n    last_print = time.monotonic()\n    marks = out / ("marks-"+phase+("-identity" if identity else ""))\n    marks.mkdir(exist_ok=True)')
    s=s.replace('            raw.clear()', '''            mark = marks / f'{star}_{sec}.json'
            if mark.exists():
                completed += 1
                continue
            raw.clear()''')
    s=s.replace('            completed += 1\n            progress.update', '''            mark.write_text(json.dumps(dict(complete=True)), encoding='utf-8')
            completed += 1
            if time.monotonic()-last_print >= 60:
                print(campaign, phase, slot, completed, '/', len(work), flush=True)
                last_print=time.monotonic()
            progress.update''')
    ast.parse(s)
    (S/'028_generate.py').write_text(s,encoding='utf-8')
    print('Prepared resumable SNR4 raw replay, baseline filter options preserved.')


if __name__=='__main__': main()
