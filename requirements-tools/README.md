# Requirements for the tool test environments

Each file is `pip freeze` of one environment under `.venv-tests/` (all built on Python 3.12.10). The main pipeline environment is `requirements.txt` at the repo root, the book is `book/requirements-docs.txt`.

- `ellc.txt`, `phoebe.txt`, `stanley_cbp.txt`: the packages each third-party tool was tested with.
- `LEO-Vetter` and `mono-cbp`: those two environments contain only pip, so there is nothing to record.

Rebuild one: `py -3.12 -m venv .venv-tests/<name>` then `.venv-tests/<name>/Scripts/python -m pip install -r requirements-tools/<name>.txt`.
