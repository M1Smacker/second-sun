# Real-time updates on the book: research report (30 Oct 2026, research blueprint; Ahmed: "I need simultaneous real-time updates")

Method: `RESEARCH-BLUEPRINT.md`. Own data first, then searches, then the primary pages opened in the browser pane (HTML only, no file links). A search summary is a lead; every CONFIRMED line below was read on the page named.

## 1. Questions, and the decision each one feeds
1. Why is the Search window 1 to 2 minutes behind, and can that be cut to about a second on GitHub Pages? Feeds: how the page gets its numbers.
2. Which realtime channel fits a static book read mostly from an iPhone? Feeds: the choice and what Ahmed has to set up.
3. What does a live channel cost, limit or expose? Feeds: whether it is safe for the sealed (blind) run.
4. What must the downloader and the search write so the page can show smooth, honest live numbers? Feeds: the status format.
5. How do phones behave when the page is in the background? Feeds: reconnect rules.

## 2. Our own house first
- **The lag is our design, not a limit of the web.** MEASURED 30 Oct: the page polls GitHub's file API every 60 s; GitHub caches that answer up to 60 s (`cache-control: public, max-age=60, s-maxage=60`); the raw file host caches 300 s (`max-age=300`, MEASURED, and 5 minutes behind in the test). A push-to-GitHub design cannot get below about a minute.
- **A real-time channel already exists in our world:** Eyes mode talks to the Firebase project `second-sun-faea5` (Firestore, create-only rules, public web key; `eyes-cloud.js`, `research/firebase-setup-steps.md`). So a Firebase account and project are already there.
- **A live stream works from a plain page.** MEASURED 30 Oct with a throwaway server (standard library only) and a page using the browser's `EventSource`: 11 events in 10 s, delay 1 to 2 ms (same computer). It proves the page side; it does not prove the network path from the PC to a phone.

## 3. Findings
**F1. How websites do it (CONFIRMED, MDN "Using server-sent events").** The server keeps one connection open and pushes each change; the browser object `EventSource` receives it. WebSockets do the same both ways. Plain polling (what we do) can never be faster than its interval. MDN warns that over HTTP/1.1 a browser allows only about 6 open SSE connections per domain across all tabs ("Won't fix" in Chrome and Firefox); over HTTP/2 the limit is negotiated (default 100). So: one stream per page, not one per number.

**F2. Firebase Realtime Database streams to a plain page (CONFIRMED, firebase.google.com/docs/database/rest/retrieve-data).** "Firebase REST endpoints support the EventSource / Server-Sent Events protocol": set `Accept: text/event-stream`, follow the 307 redirect, add `auth` if reads need permission. The server sends `put` and `patch` events (a path and the new data), `keep-alive`, `cancel` (rules no longer allow the read) and `auth_revoked`. No library is needed, which suits a book that serves only its own scripts.

**F3. The free plan is enough for this job (CONFIRMED, Realtime Database limits and billing pages).** Spark plan: 1 GB stored, 10 GB a month downloaded, simultaneous connections capped at 100; one connection is one browser tab or server app. Writes: more than 1,000 a second may be rate-limited; plain REST requests do not count as connections. Open SSE connections do count toward connection usage (search summary of the billing page; the exact sentence was not re-read, so LIKELY). My estimate, not a measurement: one update a second of about 300 bytes is about 26 MB a day per open tab, against about 330 MB a day available. The Spark limits are hard: over a limit the app is turned off until the month ends (search summary of Firebase docs, LIKELY).

**F4. Writing safely (CONFIRMED, "Authenticate REST requests" and the Admin SDK pages).** A server can write with a Google OAuth2 access token made from a service account; that access ignores the security rules. The rules can then say "everyone may read `/live`, nobody may write": `".read": true, ".write": false` at that path is a valid, documented pattern, and a child rule cannot take away a read granted by its parent. Legacy database secrets still work but are discouraged.

**F5. Cloudflare Quick Tunnels do NOT fit (CONFIRMED, developers.cloudflare.com/tunnel/get-started/quick-tunnels).** "Quick Tunnels do not support Server-Sent Events (SSE)"; 200 in-flight requests at most; no uptime guarantee; the address changes every time. A named tunnel avoids these but needs a domain we do not have (cost UNCERTAIN, not researched).

**F6. Other hosted channels exist (UNCERTAIN: only third-party comparison pages were read).** Supabase Realtime free plan: 200 concurrent connections, 100 messages a second, 2 million messages (CONFIRMED on supabase.com docs via search result, page not opened). Pusher, Ably and PartyKit have free tiers (secondary pages only, no verified numbers). All need a new account, a vendor script on the page and a key; none beats Firebase for us, because Firebase is already ours and needs no script.

**F7. Cloud Firestore can also push, but through its JavaScript library (LIKELY).** Its docs describe `onSnapshot` listeners that stay open for hours. I did not find a plain-page (library-free) streaming route for Firestore (NOT FOUND, not the same as "does not exist"). Using it would mean loading Google's library from the outside into a book that is built to work offline.

**F8. Phones kill background streams quietly (LIKELY: GitHub issues from Flarum, Mitzo, agentboard, May 2026; no Apple documentation found).** iOS Safari can close a WebSocket or EventSource when the tab loses focus or the phone sleeps, without any error event, so the page believes it is still connected. Coming back through the back-forward cache fires `pageshow` (persisted) and not `visibilitychange`. The consistent fix: reconnect on both events, plus a heartbeat check ("no event for 3 x the interval means reconnect").

## 4. Options compared
| Option | Delay | Works on iPhone away from home | Account or install | Fits blind sealed run | Verdict |
|---|---|---|---|---|---|
| A. Now: GitHub file polled each minute | 1 to 2 min | yes | none | yes | too slow for Ahmed |
| B. Firebase Realtime Database stream (SSE), PC writes with a service account | about 1 s (expected; NOT yet measured on our setup) | yes | Ahmed creates the database and a service-account key; one Python package (google-auth) | yes, if only the same aggregates and blind pictures are written | **Recommended** |
| C. Live page served by the PC itself over SSE (same Wi-Fi) | milliseconds (MEASURED locally) | only on home Wi-Fi, page opens from the PC's address | none | yes | good free extra, no cloud; not for use outside the home |
| D. Cloudflare Quick Tunnel to the PC | not possible for SSE | n/a | install cloudflared | n/a | rejected (F5) |
| E. Firestore onSnapshot | about 1 s (LIKELY) | yes | same project, Google library on the page | yes | second choice if B is refused |
| F. Pusher, Ably, Supabase, PartyKit | about 1 s | yes | new account, vendor library | yes | not needed |

## 5. What the sender must write so the page feels live (Ahmed: "improve this further")
The page should be able to look smooth even when messages arrive once a second, so:
1. **One status document per job**, rewritten as a whole 1 time a second while something changes (atomic: write a temp file, then rename), with `schema` (a version number), `job_id`, `seq` (counts up, so the page can tell a missed update), `sent_at` (the sender's clock) and `state` (waiting, running, finishing, done, failed, paused).
2. **Bytes in flight, not only finished files.** Each worker reports the bytes received so far of its current file; the page sums finished and in-flight bytes, so the bar moves between file completions.
3. **Counts that cannot disagree:** done, running, waiting, failed, skipped (each with a reason code), the total expected, and the total bytes expected with a label saying whether it is measured or estimated.
4. **A short event log** (last 20 events: started, finished, retried, failed) so the page can say what is happening in words.
5. **Speed and the time left computed on the page**, from a smoothed rate (exponential average over about 30 s) and ticking every second in the browser, so the estimate does not jump with every sample; the sender only supplies facts.
6. **A heartbeat:** the page marks the job NOT UPDATING when no message arrives for three intervals, and reconnects on `visibilitychange` and `pageshow` (F8).
7. **Blind rule:** for the sealed run only aggregates and the blind pictures already approved go into the channel; nothing about real versus upside-down.

## 6. Recommendation and what I need from Ahmed
Use **B** (Firebase Realtime Database over SSE) for both the Search window and a new Downloads page, keep **A** as the automatic fallback when the stream is unreachable, and offer **C** as a free local extra. Steps only Ahmed can do (I will write them into `research/firebase-realtime-steps.md`, like the Eyes steps): in the existing Firebase project create a Realtime Database; paste the two-line rules (`/live` readable by everyone, writable by nobody); create a service-account key and save it to a folder outside the repository; tell me the file path (I never need to open it). On my side: a small `live_push.py` (1 Hz, fall back to GitHub if the stream is down), the page code (EventSource with the reconnect rules of F8, bar animation between samples), tests on a fake run, and the registry of jobs described in section 7. Estimated 2 to 3 points of usage. NOT tested: the real network path to an iPhone, Firebase's actual delay from our PC, and the rules in practice.

## 7. The automatic rule (Ahmed, 30 Oct: "I should not be reminding you")
Every download and every long machine job gets, at the moment it starts, a row in the job list on the Downloads page (what it is, where it comes from, why, expected size, state) and I tell Ahmed to publish if the page itself changed; no reminder needed. Until the page exists the interim is a line in `research/jobs.md` and a sentence to Ahmed. Saved as a standing rule in CLAUDE.md and memory.

## 8. Open doubts
Whether Firebase uses HTTP/2 for these streams on iOS (the 6-connection limit would then not matter): UNCERTAIN, not checked. Firestore without a library: not found. Pricing pages of Pusher and Ably: not opened. Tailscale Funnel as another tunnel: NOT researched.

Sources read: [Firebase REST streaming](https://firebase.google.com/docs/database/rest/retrieve-data), [RTDB limits](https://firebase.google.com/docs/database/usage/limits), [RTDB billing](https://firebase.google.com/docs/database/usage/billing), [REST authentication](https://firebase.google.com/docs/database/rest/auth), [Cloudflare Quick Tunnels](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/), [MDN server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events). Search summaries only: Supabase Realtime limits, Firestore listeners, the iOS GitHub reports, the Admin SDK and rules pages.
