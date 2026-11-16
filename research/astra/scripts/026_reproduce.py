"""One-command reproduction. Use only after the existing background jobs end."""
import importlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
R = importlib.import_module('026_run')


if __name__ == '__main__':
    for script in ('026_prepare.py', '026_controls.py', '026_run.py',
                   '026_control_run.py', '026_verify.py', '026_recount.py',
                   '026_report.py'):
        R.run(script)
