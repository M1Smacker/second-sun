New standing rule from Ahmed for every message you send him.

Ahmed often reads and steers this session from the Claude iPhone app over Remote Control, in bed, with the PC monitor off. The phone is a window into this session, not into the PC. From the phone he CANNOT open files or folders on the PC, cannot render a local markdown file, and does not see the wrap_up next-step box or its buttons. He CAN read chat messages (headings, lists, bold, short tables render; wide tables do not), tap links, view images you send, answer permission prompts and AskUserQuestion questions, and attach photos or files to a message. So:

1. NEVER say "open the file at <path>". Put what he needs to read INSIDE the chat message. Summary first, in plain words, under about 300 words. Say what the decision or next step is in the first two lines.

2. If there is more than that (a report, a plan, a long prompt he must copy), you may still write the file on the PC for reference, but ALSO deliver it to the phone, in this order of preference:
   a. A tappable GitHub link, after the file is committed AND pushed: https://github.com/M1Smacker/second-sun/blob/main/<repo-relative path>  (the repo is public and GitHub renders markdown on iPhone). If it is not pushed yet, say so and do not give a dead link.
   b. A private Artifact page (a claude.ai link he can open from the phone) for anything formatted, long, or meant to be copied. For a prompt, put it in a read-only text box he can select and copy.
   c. SendUserFile for images, PDFs and short files (display "render" for images and HTML, "attach" for the rest).
   d. For book chapters: republish the book (research\burn-3-book\tools\publish_book.ps1) and give the live page link under https://m1smacker.github.io/second-sun/.

3. When he must copy something into another session, give the prompt inline in a fenced code block AND in an Artifact copy box. Never only as a file path.

4. Questions and approvals: permission prompts and AskUserQuestion reach his phone and wait for him. The wrap_up box does not. Open the closing message with the recap, then put any question and the options in the message text ("reply A, B or C"). Keep options short enough to type on a phone. Other pop-up dialogs expire after about 5 minutes, so do not rely on them.

5. Do not ask him to do anything that needs the PC (typing commands, opening folders, clicking in the desktop app). If something truly needs the PC, say "needs the PC, I will wait for it" and carry on with other work. Never leave a task blocked on a PC-only step without saying so.

6. Phone-friendly slash commands that work from the app: /compact, /clear, /context, /usage, /recap, /model, /effort, /fast, /rename, /mcp (text summary), /config key=value. Local-only commands such as /plugin and /resume do not.

7. Do not change power or sleep settings and do not restart Windows. The PC must stay awake with the lid open and the Claude desktop app running. If the machine or the app restarts, the session goes offline until it is resumed.

8. Keep alerts rare: one push when a long task finishes or a decision is needed, not progress chatter.
