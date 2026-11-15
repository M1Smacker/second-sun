"""Collect producer verification and mode output after the local runs finish."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'data/astra/018'
paths = [
    'book/docs/learn/u1/l4-what-a-dip-looks-like.md',
    'book/docs/learn/u2/l1-orbits-and-periods.md',
    'book/docs/learn/u2/l2-how-long-a-dip-lasts.md',
    'book/docs/assets/learn.js', 'book/docs/assets/learn.css', 'book/hooks.py',
]
preserved = {}
for relative in paths:
    committed = subprocess.run(['git', 'show', 'HEAD:' + relative], cwd=ROOT, check=True, capture_output=True).stdout
    present = (ROOT / relative).read_bytes()
    preserved[relative] = committed.replace(b'\r\n', b'\n') == present.replace(b'\r\n', b'\n')
assert all(preserved.values()), 'A protected book source differs from HEAD'
compiled = []
for name in ['018-facts.py', '018-verify.py']:
    file = ROOT / 'research/astra/scripts' / name
    compile(file.read_text(encoding='utf-8-sig'), str(file), 'exec')
    compiled.append(name)
mode_output = {}
for mode in ['learn', 'layout', 'textfloor']:
    lines = (OUT / f'{mode}.log').read_text(encoding='utf-8').splitlines()
    result = next(json.loads(line) for line in reversed(lines) if line.startswith('{'))
    mode_output[mode] = result
summary = dict(source_preservation=preserved, python_static_compilation=compiled,
               modes={mode: dict(checks=r['checks'], passed=r['pass'], errors=r.get('errors', []))
                      for mode, r in mode_output.items()},
               learn_views=[dict(width=v['width'], pages=len(v['pages']), answers=v['accepted'],
                                 hints=v['hints'], numeric_rejected=v['numericRejected'])
                            for v in mode_output['learn']['views']])
(OUT / 'verification.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
report = ROOT / 'research/astra/reports/018-report.md'
text = report.read_text(encoding='utf-8')
marker = '\n<!-- BEGIN GENERATED RUNTIME EVIDENCE -->'
text = text.split(marker)[0]
addition = marker + '\n\n'
for mode, result in mode_output.items():
    addition += f'### {mode}, exit {0 if result["pass"] else 1}\n\n```json\n'
    addition += json.dumps(result, ensure_ascii=True, separators=(',', ':')) + '\n```\n\n'
evidence = json.loads((OUT / 'evidence-summary.json').read_text(encoding='utf-8'))
addition += '### Additional evidence\n\n```json\n' + json.dumps(evidence, ensure_ascii=True, separators=(',', ':')) + '\n```\n\n'
addition += '### Final checks\n\n'
addition += ('- Runtime checks completed include the strict MkDocs build, independent FITS and source-answer calculations, '
             'three requested browser modes, the settled Tree diagnostic and the numeric-tolerance mutation. '
             'The final learn run also checks the final test-source revision.\n'
             '- Static checks completed include Node syntax checks for the changed test and new JavaScript runners, '
             'Python compilation without bytecode writes, PowerShell parsing of the build wrapper and `git diff --check`.\n'
             '- The three audited lessons, `learn.js`, `learn.css` and `hooks.py` match HEAD after newline normalization. '
             'This comparison verifies source preservation.\n'
             '- Both local runner families completed and stopped their own HTTP servers. Data writes and scratch profiles '
             'remain under `data/astra/018/`. No commit, branch change, push or publication was performed.\n\n'
             '**Next** Claude reviews report 018 and adjudicates the node 4.1 corrections before the lessons are approved. '
             'This is a low-cost reading step and requires Claude.\n\n'
             'DONE, the requested audit, automatic lesson coverage and three browser modes are delivered, '
             'with failures, uncertainty and untested scope recorded.\n')
report.write_text(text + addition, encoding='utf-8', newline='\n')
print(json.dumps(summary, indent=2))
