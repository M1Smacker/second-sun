# 13. Your workshop: a tour of the project

<p class="ss-meta">Chapter 13 · about 15 min · no maths</p>

!!! plain "In plain words"
    Everything we do lives in one folder, `D:\second-sun`, and a public copy on GitHub. This chapter is the map: which folder holds what, which files record our decisions and mistakes, how a working day flows from an idea to this book, and the rules that keep it safe. If you ever want to find something yourself, start here.

**What this chapter answers:** where is everything, and how does a day of work turn into a page you can read?

## 13.1 The folders

| Folder | What's in it | In git? |
|---|---|---|
| `book/` | this book: chapters (`docs/`), the facts register (`data/claims.csv`), your progress (`progress/`), build tools | yes |
| `labs/` | the lab scripts you run | yes (pictures in `labs/out/` are not) |
| `pipeline/` | our search code: the detector (`detect_v2.py`), tests, timing, stability, the STANLEY wrappers | yes |
| `targets/` | the frozen G1 list and its data coverage | yes |
| `research/` | reports, reviews, the registers (below) | yes |
| `data/` | every downloaded file: light curves, pixel files, STANLEY's output | **no** (too big; NASA keeps the originals) |
| `.venv`, `.venv-docs`, `.venv-tests` | the Python workbenches: main, book-building, STANLEY | no |
| `.cache` | temporary files, kept on D: | no |

"In git" means the file's whole history is saved and copied to GitHub. Data stays out because it's big and anyone can download it again from MAST.

## 13.2 The registers: the project's memory

| File | What it records |
|---|---|
| `RESEARCH-PLAN.md` | the founding plan, every early decision, research principles |
| `research/decisions.md` | every decision, dated, with your words; open decisions marked PENDING |
| `research/mistakes.md` | every mistake, its cost, and the rule it created (Chapter 15) |
| `research/predictions.md` | predictions made **before** checking, then scored right or wrong |
| `research/downloads.csv` | every file downloaded: when, from where, how big, why |
| `book/data/claims.csv` | every fact in this book, its label and source |
| `research/COMPASS.md` | your review system for big ideas |
| `research/compass-reviews/` | each Compass review |
| `OVERNIGHT.md`, `MORNING-REPORT.md` | the overnight run's queue, log and report |

## 13.3 How a working day flows

1. **An idea or a request** (yours, or from a review).
2. **Compass**, if it's big: what exists already, what's wrong with the idea, what to do first. Verdict before building.
3. **Build and test.** Code gets a self-check; results are measured, not eyeballed.
4. **Record.** Results into a report; facts into the claims register with labels; decisions and mistakes into their registers.
5. **Teach.** A field note, the same day (your rule of 20 October). Bigger new ideas get a chapter section.
6. **Publish.** Commit to git, push to GitHub, rebuild this site. The guard script `book/tools/teach_check.py` prints "Book is N commits behind" during publishing; it should say 0.

## 13.4 Git and GitHub in five sentences

**Git** keeps every saved version of every file. A **commit** is one saved snapshot with a message saying what changed and why. **Pushing** copies commits to **GitHub**, where the project is public at github.com/M1Smacker/second-sun. Because every change is a commit, nothing is ever truly lost, and anyone can check what we did and when. This book is built from the committed files only, in a fresh copy, so what you read is exactly what's saved.

## 13.5 The safety rules (and why)

| Rule | Why |
|---|---|
| Nothing written to C: | it's nearly full; every cache is forced to D: |
| No passwords, keys or tokens in the repo, ever | it's public. The ADS key lives only in your Windows user settings |
| Downloads over 20 GB need your OK; every download logged | so storage never surprises us |
| Nothing outward-facing without your explicit OK | no posts, emails or ExoFOP uploads in your name |
| Two keys before any submission | Claude and you both check a candidate independently |
| No copying of GPL-licensed code into our MIT project | licences; importing such tools is fine |
| Ask before using helper sessions | your rule: each time |
| Never touch Avast, Windows security, power or sleep settings | your PC, your settings |

## 13.6 Talking to Claude about the project

| You say | What happens |
|---|---|
| "Lab 3 done" + your result | I check it and set the level's date in `progress/levels.yml` |
| "L2 read" | I quiz you on that level |
| "Compass this: ..." | a review-only pass with a verdict, before anything is built |
| "Where are we?" | a short status; the long version is [The story so far](../start/story-so-far.md) |

## 13.7 Check your understanding

??? quiz "1. Why isn't the data folder in git?"
    It's large, and NASA's MAST keeps the originals, so anyone can download it again. Git holds the code, the lists and the records that say exactly which files we used.

??? quiz "2. Where would you look to find out why we chose G1?"
    `research/decisions.md` (dated, with your words), and the field note of [19 October](../field-notes/2026-10-19.md).

??? quiz "3. What does 'Book is 3 commits behind' mean?"
    Three changes to code or research were saved after the last field note. The same-day rule says a field note should be written before the work is called finished.

**Next:** [Chapter 14: credit and publishing](14-credit-and-publishing.md).
