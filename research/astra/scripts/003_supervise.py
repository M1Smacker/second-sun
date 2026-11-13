"""Launch scoped workers and maintain the book-readable progress file."""
import argparse
import json
from pathlib import Path
import subprocess
import time
from datetime import datetime,timezone
ROOT=Path(r'D:\second-sun-astra'); OUT=ROOT/'data/astra/003'
PYTHON=r'D:\second-sun\.venv\Scripts\python.exe'
def main(args):
    configurations=[('g2',i,args.g2) for i in range(args.g2)]+[('g3',i,args.g3) for i in range(args.g3)]
    assert len(configurations)<=4
    processes=[]; streams=[]
    for campaign,slot,slots in configurations:
        label=f'{args.start}-{args.limit}-{campaign}-{slot}'
        stdout=(OUT/f'{label}.log').open('w',encoding='utf-8'); stderr=(OUT/f'{label}-error.log').open('w',encoding='utf-8')
        streams.extend([stdout,stderr])
        command=[PYTHON,'-I','-B',str(ROOT/'research/astra/scripts/003_worker.py'),'--campaign',campaign,
                 '--slot',str(slot),'--slots',str(slots),'--start',str(args.start),'--limit',str(args.limit)]
        processes.append(subprocess.Popen(command,cwd=ROOT,stdout=stdout,stderr=stderr,creationflags=subprocess.CREATE_NO_WINDOW))
    while True:
        statuses=[]
        for campaign,slot,_ in configurations:
            path=OUT/'workers'/f'{campaign}-{slot}'/'progress.json'
            try: statuses.append(json.loads(path.read_text(encoding='utf-8')))
            except (FileNotFoundError,json.JSONDecodeError): pass
        running=any(p.poll() is None for p in processes)
        progress=dict(phase='timing' if args.limit==20 else 'full',trials_done=args.start+sum(x['trials_done'] for x in statuses),
            trials_planned=args.limit,paired_arms_planned=2*args.limit,status='running' if running else 'complete',
            last_update_utc=datetime.now(timezone.utc).isoformat(),workers=statuses)
        if (OUT/'STOP.json').exists(): progress['status']='stopping'
        (OUT/'progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8')
        if not running:
            codes=[p.returncode for p in processes]; progress['exit_codes']=codes
            progress['status']='stopped' if (OUT/'STOP.json').exists() or any(codes) else 'complete'
            (OUT/'progress.json').write_text(json.dumps(progress,indent=2),encoding='utf-8'); break
        time.sleep(15)
    for stream in streams: stream.close()
    print(json.dumps(progress))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--start',type=int,default=0); p.add_argument('--limit',type=int,default=20)
    p.add_argument('--g2',type=int,default=1); p.add_argument('--g3',type=int,default=1)
    main(p.parse_args())
