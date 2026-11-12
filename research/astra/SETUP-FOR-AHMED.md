# Setting up Codex for Second Sun (Ahmed, about 10 minutes, once)

Claude already made: `AGENTS.md`, the Codex skills in `.agents/skills/`, this mailbox, the fence check, and Codex's own folder `D:\second-sun-astra` (a second checkout of the same repo; its `data` is a link to the real data). The Codex app is already installed on your PC (you used it in September).

## Before you buy (free, today if you like)
1. Open the Codex app, choose **Open folder** and pick `D:\second-sun-astra` (NOT `D:\second-sun`: that one is Claude's).
2. When asked, **trust** the folder.
3. Ask it, on the free model in your picker: "Read AGENTS.md and list the skills you can see. Do not change anything." It should name `second-sun-auditor`, `second-sun-mailbox`, `second-sun-research` and `my-take`. If it does, the kit loads. Tell Claude what it said.

## After you buy ChatGPT Plus ($20)
1. **Privacy first (before any Second Sun chat):** ChatGPT, Settings, Data Controls: turn OFF "Improve the model for everyone". In Codex settings: leave "Include environments" (training on full environments) OFF. Never use thumbs up or down on a Second Sun chat (a rating can send the whole chat for training even with the switch off). Check the switch again once a week (a user reported in Nov 2026 that it turned itself back on; not confirmed).
2. In the Codex app, sign in with the Plus account, open `D:\second-sun-astra` again.
3. **Model picker:** GPT-6 Astra should now appear. For brief 001 pick Astra, effort Medium. (If only older models show, update the app: Astra needs a recent Codex version.)
4. **Permissions (Ahmed's choice, 12 Nov 2026): Full access.** The app will not stop Codex, so the fence is AGENTS.md rule 12 (where Codex may go and what it may never run), plus two real checks: pushing from `D:\second-sun-astra` is switched off in git (its push address is a dummy), and `fence_check.py` reads Codex's history database after every brief and flags any forbidden folder, push, install, settings change or fenced star. If you ever want the hard wall back, switch to the default sandbox; nothing else changes.
5. **First message (one line):** "Read AGENTS.md, then do brief 001 in research/astra/inbox." When it says the report is ready, tell Claude: "Codex finished 001".
6. Then brief 002 the same way (Astra, effort High), likely over 2 or 3 sessions.

## Everyday
- You never copy text between us. Claude writes briefs, Codex writes reports, both in git.
- You can chat with Codex directly about Second Sun (questions, explanations, "your take"). Big changes still go through Claude.
- Use Astra only for big judgements; for small things pick Sol (normal) or Luna (chores). Each brief names the model.
