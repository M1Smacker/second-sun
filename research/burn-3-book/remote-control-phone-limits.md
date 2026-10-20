# What the Claude iPhone app can and cannot do over Remote Control (research, 2026-10-20)

Sources: Anthropic docs (Remote Control, Claude Code on mobile, Desktop, Artifacts, Channels), GitHub issue anthropics/claude-code#42156, this PC's power settings (measured), and delivery tests from this session. Labels as in the book: VERIFIED = read in the official doc or measured; LIKELY = secondary source or reasoned; UNVERIFIED = not yet seen working on Ahmed's phone.

## Works from the phone (VERIFIED, official docs)
- Read the live conversation, send messages, steer; sessions are in the Code tab with a computer icon and green dot when online (code.claude.com/docs/en/remote-control).
- Permission prompts and AskUserQuestion questions reach the phone and stay open until answered. Other forwarded dialogs expire after 5 minutes (same page, Limitations).
- Attach photos; other files are downloaded to the PC and passed to Claude as @ references (same page). Conflict: an April 2026 issue (#42156, v2.1.89) said only photos could be sent; it was closed "not planned" without a reply. The current doc is newer, so files probably work (LIKELY; test it).
- Pick model and effort; permission modes Manual, Accept edits, Plan and Auto, but never Bypass (docs/en/mobile, Limitations).
- Slash commands that work: /compact /clear /context /usage /recap /model /effort /fast /rename /mcp (text) /config key=value /output-style /focus /advisor /autocompact. Do not work: /plugin /resume and anything that opens a terminal picker.
- See the diff pane for git changes, see subagents and workflows, and stop them from the phone.
- Push notifications (docs/en/remote-control, Mobile push notifications): in a session run /config and enable "Push when Claude decides" and "Push when actions required". On iOS, Focus modes can delay them.

## Does not work from the phone
- Opening any file or folder on the PC, rendering local markdown, the Browser pane, the terminal, desktop panes (VERIFIED by absence in the docs; the Desktop doc lists these as desktop-only).
- The wrap_up next-step box and its buttons: this session's harness says the phone client "shows no next-step box" (VERIFIED, harness message).
- Starting a connector login (/mcp picker) from the phone; a "!" command is sent as chat, not run.

## The PC has to stay up (VERIFIED, docs + local measurement)
- The session is a window into a process on the PC. If the Claude Desktop app quits, the PC restarts (Windows Update counts), or it sleeps, the session goes offline until the PC is back; the app reconnects by itself after sleep (docs/en/desktop, docs/en/mobile). Closing a laptop lid counts as sleep.
- This PC: power plan High performance; sleep after idle = Never on AC; screen off = Never on AC; no battery (a desktop). So turning the monitor off is fine. "Keep computer awake while Claude works" is On. Windows active hours 11:00 to 05:00, so an automatic restart is possible between 05:00 and 11:00.
- Server mode (claude remote-control) gives up after about 10 minutes without network. An interactive session keeps retrying (docs, Limitations).

## Ways to get something readable onto the phone, best first
1. Put it in the chat message itself: rendered markdown (headings, lists, short tables). Always works. Keep long ones under about 300 words with the decision first.
2. GitHub link after commit and push: https://github.com/M1Smacker/second-sun/blob/main/<path>. GitHub renders markdown in Safari. The repo is public. Only works for pushed files (LIKELY; tap to confirm).
3. Artifact page: a private claude.ai page. Docs say sessions started by the user, including claude remote-control sessions, can publish artifacts; Desktop app 1.13576.0 or later; Markdown or HTML up to 16 MiB; a Copy box works for prompts (docs/en/artifacts). Viewing on the iPhone app is not documented (UNVERIFIED until Ahmed opens https://claude.ai/artifact/DijgKrdjxMbuh4wZuSYqef).
4. SendUserFile: this harness delivers a file to the phone as an attachment card, or inline for images (VERIFIED delivered; whether iOS previews a .md attachment is UNVERIFIED).
5. The book on GitHub Pages: https://m1smacker.github.io/second-sun/ (VERIFIED working; chapters only, after a republish).
6. Optional, not recommended now: Channels (Telegram, Discord or iMessage bridge). It needs a bot token, Bun, a restart with --channels, and it only works while the session is running (docs/en/channels).

## Not recommended
- Making the phone the only place a decision exists. Always put the decision and the options in the message text.
