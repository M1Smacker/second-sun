# Control room: live view of everything Claude, Codex and the machine do (PLAN ONLY, not built)

**Planned with Ahmed in 5 question rounds, 13 Nov 2026.** Build waits until G1 or Census is done (his choice), then Claude builds all of it. BUILD-QUEUE T159.

## What Ahmed asked for
"I want to see live coverage of whatever you, Claude or Codex is doing", both star hunts and other runs such as the recovery trials. He stays in charge (second key) and learns by watching.

## Decisions (his answers)
| Topic | Decision |
|---|---|
| Where | Phone summary from anywhere plus fuller detail; the whole book moves too |
| Host | Netlify, `second-sun.netlify.app` (name to be checked free at build time); the whole book plus the control room move there |
| Page | The Search window grows into the control room (not a separate page) |
| Overview | Brief: every job with a progress bar plus one plain line per worker; auto-updating |
| Drill-down | Per worker: every step in plain titles plus short thinking summaries (why the step), auto-updating; star ids and secrets filtered out |
| Lock | Secret link only for viewing (plus noindex) |
| Buttons | Stop buttons only (no approve buttons); Stop needs a short PIN |
| Deploy | From his PC after every check and browser test (publish script uploads to Netlify) |
| Feed path | Straight from his PC to Netlify's own storage, never through the public GitHub repo |
| Alerts | Phone push on finish, fail or stall, and when a decision waits for him; web push from the home-screen app |
| Meters | Claude's weekly and 5-hour bars, Codex's bars, and today's cap line |
| Old site | GitHub Pages address redirects to Netlify |
| Learning | Every card has a one-line "what is this and why" plus a link to the right lesson |
| History | Full steps for 30 days, then one line per job |
| Builder | Claude builds it all |

## Rules that stay, whatever the design
- Sealed runs stay blind on the page (counts only, real and upside-down pooled) as the Search window blueprint says. The blindness is scientific, not a privacy setting, so a secret link does not lift it.
- No star ids, event times or lead details in the feed. The filter runs on the PC before anything is sent.
- Never click the live Eyes page. Codex never publishes; Claude deploys.
- A page tap is never an instruction to an AI. Stop runs a fixed local script on his PC; anything new still goes through chat.

## Sketch of the build (to be sized when it starts)
1. **Watcher on the PC** (small Python, every 30 to 60 s): reads `research/jobs.md`, every run's progress file (for example `data\astra\003\progress.json`), Codex's history database (steps, plus reasoning summaries filtered), and Claude's own activity log (a Claude Code hook that records each tool call's plain description). Filters ids and secrets, then sends one small JSON to Netlify.
2. **Netlify side:** a small function plus storage that receives the feed (with a write key kept on the PC, never printed or committed), serves it to the page, keeps 30 days, and sends web pushes.
3. **Stop:** the page sends a PIN-checked stop request; the PC watcher picks it up on its next poll and writes the run's own stop marker (for example `STOP.json`), so the PC never opens a door to the internet.
4. **Pages:** the Search window becomes the control room (overview, worker drill-down, timeline, meters, learn links). The whole book is built by the existing publish script and uploaded to Netlify; GitHub Pages gets a redirect.
5. **Account steps that need Ahmed:** logging the Netlify command-line tool into his account once, creating the site name, allowing notifications on his iPhone.

## Open points for the build day
- Which Netlify plan features he has (functions, storage, build minutes): check at build time, NOT TESTED now.
- The exact iPhone web-push setup for a home-screen app: verify on his phone when building.
- Codex's reasoning text may mention star ids: the filter must be tested on real history before anything is sent.
