# Wave 2 friction log

- 17:05 UTC: the scheduled queue runners froze on their first permission prompt, so wave 2 ran inline in the main session instead.
- 17:06: C: free space fluctuates (18 → 14.3 → 22 GB during the day); something else on C: writes and clears temp data. The pip cache already on C: is 4.1 GB.
- 17:08: the first ZTF query asked for g,r but returned only g. Not yet investigated.
- 17:09: HEASARC "the-tess-space-telescope.html" returned 404. The lightkurve TessQualityFlags docs page returned 404 too, so I read the installed source instead.
- 17:10: WebFetch of the TESS planning PDF returned binary; wave 1c's stdlib pdftext.py garbles it (custom font encoding).
- 17:11: **all 9 lightkurve downloads failed with SSL CERTIFICATE_VERIFY_FAILED.**
  - Root cause: Avast Web/Mail Shield's HTTPS scanning re-signs certificates with "Avast Web/Mail Shield Root", which Windows trusts but certifi doesn't. pip worked because it uses the system store.
  - Fix: `pip install truststore`, plus a `sitecustomize.py` in the venv calling `truststore.inject_into_ssl()`.
  - Re-run: 9/9 OK. No Avast or Windows settings changed.
- 17:13: a raw-string-ending-in-backslash syntax error in Claude's inline Python; rewrote it with forward slashes.
- 17:18: one bash heredoc batch failed to parse (quoting), so I wrote the files with the Write tool instead.
