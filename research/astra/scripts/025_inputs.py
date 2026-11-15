"""Guarded inputs for the saved replays."""
import importlib
import json

H=importlib.import_module('025_harness')
KINDS=('groups','groups_sap')


def read(guard,path,brief):
    root=guard.data/'astra'/brief
    if not path.resolve().is_relative_to(root):
        raise PermissionError('Saved input escapes its brief directory')
    guard.reads.add(path.resolve())
    return path.read_text(encoding='utf-8')


def t156_rows(guard,campaign):
    root=H.OUT.with_name('003')
    for path in sorted(root.glob(f'workers/{campaign}-*/results-*.jsonl')):
        for line in read(guard,path,'003').splitlines():
            row=json.loads(line)
            if row['campaign']!=campaign or str(row['star']) not in guard.seen[campaign]:
                raise PermissionError('T156 draw outside design')
            yield row,path.parent
