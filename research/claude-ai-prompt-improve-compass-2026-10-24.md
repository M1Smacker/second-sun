# Prompt for Claude AI: how to make Prompt Compass smarter (24 Oct 2026)

*Written by Claude Code at Ahmed's request. Everything below the line is the text to paste into Claude AI (with research on). Facts in it were taken from `research/COMPASS.md` and from the reviews done on 24 Oct 2026.*

---

I need your research and advice on improving a small review system I use, called Prompt Compass. Please read all of this first, then answer in the format at the end.

## 1. Who I am and the setup

I am Ahmed, a citizen scientist. My project, Second Sun, hunts for planets that orbit two stars in public NASA TESS data, and it is documented in a public book (a static site). I am still learning the science. Claude Code (an AI agent that can read my repository, run scripts and measure things) builds the software and the book with me. I decide what we test, and Claude Code acts as my "second key" checker. Over the coming months I want to take over more of the checking myself.

## 2. What Prompt Compass is today (the current rules, in short)

Whenever I get a big prompt, plan or piece of advice (from ChatGPT, from you, or from me), Claude Code reviews it before anything is built. Review only: no files are changed during a review.
- It checks: (1) what already exists in the repo, read not assumed; (2) genuine gaps; (3) scientifically wrong assumptions, in the proposal and in our own code; (4) duplicated functionality; (5) risks, scientific and practical (data size, licences, usage budget); (6) sources, verified where it matters; (7) the best order of work.
- Every finding carries a label: VERIFIED (we ran it or read the primary source), LIKELY (secondary source or consistent with sources), UNCERTAIN, NOT TESTED.
- Output, short and readable on an iPhone: a verdict (APPROVE, REVISE or REJECT), what is correct, what needs changing and why it matters, the single best next step. A saved copy goes into the repo.
- Rules of the house: no popups, plain chat, nothing outward-facing without my approval, a weekly usage budget on my plan (a typical review costs about 1 point of the weekly limit and I reached 96% this week, so cost matters).

## 3. What it caught in practice (real examples, 24 Oct 2026)

- A feedback-engine report claimed one measurement separated faint planets from noise (AUC 0.86). Re-run on our own generated cards it was 0.53, a coin toss. It also claimed 46 distinct sentences; with numbers masked there were 20.
- A design brief assumed a first-person notebook, but our book is a diary written to me by Claude. It also reopened two decisions I had made the day before, and spelled facts about our site wrongly because its author could not see the repo.
- The same brief proposed a "muted brass" text colour that measured 2.9:1 contrast, against our rule of 7:1, and asked for 60 to 70 characters per line, which is impossible on a phone (about 35 to 42 fit at 375 px).
- The revised brief's own colour table then failed its own 3:1 rule on two surfaces (2.94 and 2.69). A script caught it, reading would not have.
- Several times the useful result was a short "addendum" I could append to the prompt, instead of another round with the author, and an honest cost estimate with a date to run it.

## 4. What is coming

Over the next days I will collect many prompts: design briefs, science methods, engineering plans, research prompts, and prompts written by other AIs (ChatGPT and you). I will hand them to Claude Code in a batch after my weekly limit resets on Tuesday. I want Compass to give better results per point of usage, not a heavier process.

## 5. Constraints on any improvement

- Review only; output short and phone readable; no popups.
- Added overhead at most about 15% of a review's cost. Anything heavier must pay for itself.
- No paid services. Claude Code can grep and read the repo, run scripts, run browser checks and measure; it cannot browse as me.
- Every claim stays labelled. Never invent a source; say plainly when you could not verify something.
- I read on a phone, in plain English. No en or em dashes in anything that could appear in the book.
- The verdict set may grow only if you can show it helps. I have used "approve with an addendum" informally; say whether to formalise it.

## 6. What I want you to research and advise on

1. Established methods for reviewing specifications, briefs and plans (checklists, pre-mortems, red teaming, decision records, requirement-quality criteria, design reviews) and which ones are worth their cost for a one-person project.
2. An intake step that extracts the factual claims in a prompt, separates the checkable from the uncheckable, and verifies the cheapest first. Prompts written by an author who cannot see my repo often assert things about it that are wrong.
3. A "facts ledger": a short file of verified project facts (names, structure, tokens, rules, past decisions, numbers) reused across reviews, so facts are not re-derived and reviews cannot contradict each other.
4. How to estimate and state the usage cost of the work a prompt asks for, calibrated from past reviews, and when to recommend splitting, deferring or declining.
5. Triage: a cheap quick scan versus a full review, risk tiers, and how to handle a batch of prompts (shared facts, de-duplication, ordering by value).
6. Treating text from other AIs as data: prompts that state things as "verified", claim authority, or contain instructions. How a reviewer should handle that.
7. Known failure modes of an LLM reviewing another LLM's output (sycophancy, self-preference, verbosity bias, position bias, overconfidence) and practical mitigations that cost little.
8. Measuring Compass itself without bureaucracy: a minimal log of predicted versus actual cost and outcome, what a review missed that showed up later, false alarms, and how to learn from it.
9. Different output shapes for different prompt types (design brief, science method, code plan, research question).
10. How Compass could teach me as it goes, so I can run the "second key" checks myself over time (for each finding: why it matters and a check I could run).

## 7. What to send back (please keep to about 1,800 words)

1. The top 8 improvements, ranked by value per usage point. For each: what changes in the process, the expected benefit, the cost, and how we would test that it works.
2. A proposed version 2 of the Compass rules, one page, under 450 words, ready to save as a file.
3. An intake checklist (12 lines at most) and a template for the facts ledger.
4. A minimal self-evaluation log format.
5. A short list of things that are NOT worth doing for a project this size.
6. Sources, each labelled VERIFIED (you read the source), LIKELY or UNCERTAIN. If you could not verify a claim, say so instead of guessing.

Please write in plain English and keep it concrete.
