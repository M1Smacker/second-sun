"""Independent saved-outcome recount, not a pipeline import."""
import json
from pathlib import Path

OUT = Path(r'D:\second-sun-astra\data/astra/030')


def main():
    summary = {}
    for bench in ('planets','T156'):
        docs = [json.loads((OUT/f'baseline-{bench}-{c}-V0.json').read_text(encoding='utf-8')) for c in ('g2','g3')]
        rows = [r for d in docs for r in d['rows']]
        assert len(rows) == (1098 if bench == 'planets' else 2000)
        if bench == 'T156':
            rows = [r for r in rows if 3000 <= r['depth_ppm'] <= 6000 and 6 <= r['duration_h'] <= 12]
            assert len(rows) == 222
        rate = sum(sum(r['real'][0] for r in rows if r['bin']==b)/sum(r['bin']==b for r in rows) for b in range(5))/5
        summary[bench] = dict(n=len(rows), B=rate)
        assert round(100*rate,3) == (48.105 if bench=='planets' else 34.207)
        if bench == 'planets':
            counts = {name: [sum(e['kind']==arm and e['options'][i] for d in docs for e in d['background']) for arm in ('real','flip')] for name,i in (('B',0),('K2',3))}
            assert counts == {'B':[174,79], 'K2':[158,63]}, 'Historical background differs'
            summary['background'] = counts
    (OUT/'baseline-check.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
