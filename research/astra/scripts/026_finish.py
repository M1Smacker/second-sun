"""Wait once for our own supervisor, then run controls and producer verification."""
import ctypes
from datetime import datetime, timedelta, timezone
import importlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
R = importlib.import_module('026_run')


def main(pid):
    now = datetime.now(timezone(timedelta(hours=3)))
    progress = dict(status='waiting', started=now.isoformat(), expected_finish=(now + timedelta(hours=3)).isoformat())
    def save():
        (R.OUT / 'progress-finish.json').write_text(json.dumps(progress, indent=2), encoding='utf-8')
    save()
    try:
        # Synchronization only, no signal, terminate, or process mutation rights.
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        kernel.OpenProcess.argtypes = (ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.WaitForSingleObject.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
        kernel.CloseHandle.argtypes = (ctypes.c_void_p,)
        handle = kernel.OpenProcess(0x00100000, 0, pid)
        if handle:
            try:
                code = kernel.WaitForSingleObject(handle, 3600000)
            finally:
                kernel.CloseHandle(handle)
            if code != 0:
                raise RuntimeError('One-hour supervisor wait exhausted or failed; no process stopped')
        state = json.loads((R.OUT / 'progress-m4.json').read_text(encoding='utf-8'))
        if state['status'] != 'complete':
            raise RuntimeError('Main M4 job is not complete: ' + state.get('error', state['status']))
        progress['status'] = 'running_controls'; save()
        R.run('026_control_run.py')
        progress['status'] = 'verifying'; save()
        R.run('026_verify.py')
        progress['status'] = 'complete'
    except Exception as error:
        progress.update(status='failed', error=str(error))
        raise
    finally:
        progress['finished'] = datetime.now(timezone(timedelta(hours=3))).isoformat(); save()
    print('Machine work and producer checks complete; review the saved counts for the final report.')


if __name__ == '__main__':
    main(int(sys.argv[1]))
