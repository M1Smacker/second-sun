"""Attach exact source statements to the private case roster without pipeline imports."""
import ast
from collections import Counter
import json
from pathlib import Path

ROOT = Path(r'D:\second-sun-astra')
OUT = ROOT / 'data/astra/025'


def find_statement(filename, function, fragment):
    source = (ROOT / 'pipeline' / filename).read_text(encoding='utf-8')
    tree = ast.parse(source)
    method = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == function)
    lines = source.splitlines()
    matches = [(number + 1, line.strip()) for number, line in enumerate(lines)
               if method.lineno <= number + 1 <= method.end_lineno and fragment in line]
    assert len(matches) == 1
    number, statement = matches[0]
    return dict(file='pipeline/' + filename, function=function, line=number, statement=statement)


def main():
    sites = {
        'quality': find_statement('detect_v2.py', 'load', 'lc = lk.read(path'),
        'QLP_finite': find_statement('detect_v2.py', 'load', 'good = np.isfinite(q)'),
        'SAP_finite': find_statement('detect_v2.py', 'load', 'good = np.isfinite(s)'),
        'filled_PDC_finite': find_statement('detect_v2.py', 'load', 'good = np.isfinite(f)'),
        'own_windows': find_statement('stage2_search.py', 'prepare', 'k = in_windows(t, good_windows'),
        'neighbour_windows': find_statement('stage2_search.py', 'prepare', 'k = in_windows(t, nbw)'),
        'no_safe_windows': find_statement('stage2_search.py', 'prepare', '"status": "no safe windows"'),
        'too_little_data': find_statement('stage2_search.py', 'prepare', '"status": "too little data"'),
        'too_little_after_mask': find_statement('stage2_search.py', 'prepare', '"status": "too little data after masking"'),
        'intersect_and_trim': find_statement('detect_v2.py', 'intersect_windows', 'return [(a + trim_start_d'),
        'drift': find_statement('petrova_mask.py', 'windows', 'half = padf'),
    }
    roster = json.loads((OUT / 'roster.json').read_text(encoding='utf-8'))
    ids = {(r['campaign'], r['trial']) for r in roster}
    trace = sum((json.loads((OUT / f'trace-{c}.json').read_text(encoding='utf-8'))['rows']
                 for c in ('g2', 'g3')), [])
    rows = []
    for row in trace:
        if (row['campaign'], row['trial']) not in ids:
            continue
        record = dict(row)
        record['source_evidence'] = []
        for file in row['files']:
            cause = file['cause']
            if cause == 'no recorded cadence':
                site = dict(file=file['file'], function='archive cadence support', line=None,
                            statement='No recorded TIME within the fixed 1.5-cadence centre tolerance')
            elif cause.endswith('load'):
                quality_first = any(int(word) & file['effective_quality_mask'] for word in file['quality_words'])
                site = sites['quality'] if quality_first else sites[
                    'QLP_finite' if file['product'] == 'QLP' else
                    'SAP_finite' if file['column'] == 'sap_flux' else 'filled_PDC_finite']
            elif cause == 'recorded, no safe windows':
                site = sites['no_safe_windows']
            elif file['window_detail'] == 'own SPOC':
                site = sites['own_windows']
            else:
                site = sites['intersect_and_trim']
            record['source_evidence'].append(dict(file=file['file'], site=site,
                recorded_near=file['recorded_near'], finite_near=file['finite_near'],
                loaded_near=file['loaded_near'], quality_words=file['quality_words']))
        rows.append(record)
    assert len(rows) == 52
    result = dict(sites=sites, cases=rows, observed_first_sites=dict(Counter(
        evidence['site']['file'] + ':' + str(evidence['site']['line'])
        for row in rows for evidence in row['source_evidence'])))
    (OUT / 'case-evidence.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print('Attached exact source statements to', len(rows), 'private roster cases.')
    print('Quality read statement line', sites['quality']['line'])


if __name__ == '__main__':
    main()
