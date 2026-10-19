# Mistakes register

Every slip by either of us: what happened, what it cost, the rule that prevents it.

| Date | Who | What happened | Cost | Rule from now on |
|---|---|---|---|---|
| 2026-10-19 | Claude | Framed the future story as "Kuwaiti discovers a planet" without asking; Ahmed is Pakistani, living in Kuwait. | One correction; no public harm. | Never assume nationality or identity from location. Credit line is fixed: "Ahmed Hanzala, independent citizen scientist (Pakistan), based in Kuwait". |
| 2026-10-19 | Claude | Relied on scheduled tasks for unattended research without first confirming they could run without permission prompts; both froze on their first command. | ~10 min of window A plus a confused check-in from Ahmed at the gym. | Before relying on any unattended mechanism, run one trivial end-to-end test of it while Ahmed can still intervene. Scheduled tasks start in default permission mode unless Ahmed sets Auto in the desktop app. |
| 2026-10-19 | Claude | The wave 2 Avast fix (a sitecustomize hook injecting truststore into every Python start) broke pip inside the venv (RecursionError); six installs failed before it was caught. | ~3 min; one re-run. | Any start-up hook must exclude pip. Test `pip --version` right after adding any interpreter-wide hook. |
| 2026-10-19 | Claude | `.gitignore` covered `.venv/` but not the new `.venv-tests/` (1.2 GB). Caught before `git add`, so nothing was pushed. | none (caught) | Use the pattern `.venv*/`; run `git status` and check for unexpected large paths before every `git add -A`. |
