"""Wait for the full fixed sample, then run already specified analysis and design study."""
import json
from pathlib import Path
import subprocess
import time
ROOT=Path(r'D:\second-sun-astra');OUT=ROOT/'data/astra/003';PYTHON=r'D:\second-sun\.venv\Scripts\python.exe'
while True:
    if (OUT/'STOP.json').exists():raise SystemExit('Stop marker present; no follow-on work')
    try:state=json.loads((OUT/'progress.json').read_text(encoding='utf-8'))
    except json.JSONDecodeError:time.sleep(5);continue
    if state['phase']=='full' and state['status']=='complete':
        assert state['trials_done']==state['trials_planned']==2000;break
    if state['status'] in ('stopped','stopping'):raise SystemExit('Full run stopped')
    time.sleep(30)
commands=[('summary',['003_summarize.py']),('diagnosis-g2',['003_diagnose.py','--campaign','g2']),
          ('multiwindow',['003_study.py','--g2','2','--g3','1'])]
for name,args in commands:
    if (OUT/'STOP.json').exists():raise SystemExit('Stop marker present')
    # Read machine load before each follow-on job; the study uses at most three workers regardless.
    load=subprocess.run(['powershell','-NoProfile','-Command','@(Get-Process python -ErrorAction SilentlyContinue).Count'],capture_output=True,text=True,check=True)
    print('python_processes_before_'+name,load.stdout.strip(),flush=True)
    with (OUT/f'follow-{name}.log').open('w',encoding='utf-8') as stdout,(OUT/f'follow-{name}-error.log').open('w',encoding='utf-8') as stderr:
        subprocess.run([PYTHON,'-I','-B',str(ROOT/'research/astra/scripts'/args[0]),*args[1:]],cwd=ROOT,stdout=stdout,stderr=stderr,check=True)
print('Follow-on work complete',flush=True)
