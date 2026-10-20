# Friction: burn-2-reading

- A `python - <<heredoc || py -3.12 - <<heredoc` one-liner hung for more than 2 minutes, probably because the bare `python` is the Windows Store stub waiting on stdin. Killed it and edited the file with sed and Edit instead.
- One sed edit turned a `\n` inside a Python string into a real newline (a syntax error). Fixed with the Edit tool before the next run.
- PowerShell 5.1 strips embedded double quotes from native-exe arguments, so `ads_watch.py --q 'abs:"x"'` failed with "unrecognized arguments". Ran it from Git Bash instead; the key comes via `powershell.exe [Environment]::GetEnvironmentVariable(...)` into a shell variable and is never printed.
- The first saved query used `author:"Davies, M"`; the first author is Benjamin D. R. Davies, so I changed it to `Davies, B`.
- The `abs:"circumbinary"` queries are noisy (circumbinary discs, CVs). The `entdate` filter also catches re-indexed old records (2019-2022 proposals showed up). These are documented in report §1.4.
- WebFetch of arXiv abstract pages does not include section text, and WebFetch cannot parse NTRS PDFs; it also saved the binary PDF to C: (tool-results). I deleted that copy, downloaded to D:\second-sun\data\burn-2-reading and used `pdftotext` (from Git's mingw64).
- The venv has no pypdf/fitz, and installs are not in this brief. pdftotext covered it.
- The WebFetch summary of the MAST TCE page came from a small model, so I cross-checked it by grepping the raw HTML. The two agreed.
- `gh api users/azibnorazman/repos` returned 404 (wrong username guess). The paper's own Data Availability gives `azibn/automated_exocomet_hunt`, which resolved.
- Norazman's pdftotext output is not valid UTF-8 (symbols lost: Greek letters, minus signs). The numbers were read from the text and are consistent with the abstract. Greek-letter symbols are reconstructed from context.
