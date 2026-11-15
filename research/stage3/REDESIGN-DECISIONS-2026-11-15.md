# Book and learning redesign: Ahmed's decisions (question rounds, 15 Nov 2026, from 2:16 am)

Build tasks this covers: T160 (Tree as home page), T59c (F4 redesign), FIX 73 (highlight clutter), FIX 74 (Back button), FIX 75 (voice), FIX 76 (formulas), T133 (Learning Space), T131 (content audit), T132 (dashboard), T57 (new findings into the track), T134 (Keystone exam), T147 (one name for his key role). Nothing is built until Ahmed says go.

## Tree
- Build it as Claude wants: bug-tested, logic-checked, transitions everywhere, looks great (Ahmed, 2:16 am). Design base: `research/tree/T160-DESIGN-DECISIONS.md` (round 1, 13 Nov).

## Learning track (round 1 to 3)
- **Goal:** all, in steps: explain the project first, then check the work (real second key), then broad astronomy toward engineer level.
- **Style:** a textbook he reads and learns from, very clear and easy; not "Claude teaching". Mix by topic: hands-on (plots, sliders) where it helps, reading elsewhere.
- **Length:** not time-boxed; must work for 5 minutes or 30+ minutes; always resumable.
- **Top summary paragraph:** removed. The last paragraph may sum up, but not as a bold highlighted one-liner.
- **Doubts cleared inside the book (no Claude):** margin notes beside hard sentences; worked examples with every step and real numbers from our stars.
- **Study tools:** notes and highlights (saved on device), continue where stopped and progress, practice problems with hidden worked answers, interactive plots, "and other things like these".
- **Maths:** full, built up from scratch, engineer level; formulas rendered properly (LaTeX quality).
- **Scope:** include the basics the project rests on (gravity, light, stars), not only project topics.
- **Old 15 chapters:** rewrite from scratch (old text only as raw material).
- **Hated (generic):** stacked bars like "In plain words", "Story", "1-minute summary"; pop-ups; tables on mobile; bad headings like "3.3 The technical explanation"; random highlighted clickable words; indexes and fact-check ledgers inside the track.
- **Checks:** end-of-chapter problems; the Keystone exam (T134). Not chosen: level exams, spaced re-ask.
- **Read-aloud:** keep; better voice if available, speed control, the features good read-aloud tools have (pause, skip, highlight current sentence and so on), formulas read properly.

## Eyes mode (practice, spotting real vs fake dips)
- "How it works" must be short and folded, not removed; he does not need it every time.
- After finishing an easy or hard test: the Back / try-again control is far down; returning lands at the bottom or random places (sometimes on "how it works") instead of where he was. Fix the scroll and navigation logic. Add transitions. (Never click the live Eyes page; test on a local build only.)
- Update diary pop-up: check it works, add a transition, improve it even if it works.

## Whole book (round 4)
- **Feel:** ~~research notebook~~ CORRECTED in round 6: stay with the night observatory look (the current look and colours, improved a lot, Claude has full control). He likes blue; other colours may be added; he really dislikes blue with orange or yellow. "Notebook" was about the teaching tone (clear, easy, textbook), not the visuals. Not fat, not generic; a record diary of our hours.
- **Main menu:** Tree (home) and Learning only. Everything else on a small folded Shelf.
- **Labs and Eyes:** a separate practice room beside the textbook, linked from chapters.
- **Tables:** keep on PC; on mobile use something better than a squeezed table (Claude's choice, e.g. stacked cards or a readable scroller). He corrected "fewer tables" to this at 2:30 am.
- **"How it works" style sections across the book:** short, folded behind a small label.

## Tree details (round 5)
- **Diary:** both: a timeline on the Tree (each day hangs on the branches it touched) and full entries on the Shelf.
- **Branch card:** plain status paragraph, full history (every fix, study, Codex job, newest first), what's next and what it waits for, link to the textbook chapter.
- **Top of the Tree page:** one short plain line: current stage and next big step.
- **Ids:** plain names first, the id small and grey beside it.

## Tree look and type (round 6)
- **Vine:** light blue glowing vine, brighter on the active path (round 7 replaced gold, because blue with yellow is out).
- **Phone:** thin vine down the left edge, full-width cards beside it.
- **Night mode:** not a paper theme at all; night observatory stays.
- **Fonts:** a classic book serif for reading text, clean sans for labels.

## Colour and motion (round 7)
- **Accent:** Claude's choice, never orange or yellow.
- **Motion:** rich: animated vine growth, starfield drift, card transitions, everywhere.
- **Background:** keep the starfield, cleaner and quieter behind reading text.

## Shelf and pages (round 8)
- **Delete:** Quests and Progress pages; the Story-so-far set (Start here, How to read, Story so far, First search, How it unfolded). The Tree and the textbook replace them. Claims register stays on the Shelf.
- **Search window:** on the Shelf; during a hunt the Tree's top line links to it.
- **Glossary:** meanings in margin notes where words first appear, plus a glossary page at the back. Opening a glossary word must bring him back to exactly where he was reading. The whole learning interface must keep his place.
- **Practice room name:** Training deck (Eyes mode and labs).

## Textbook reader (round 9) and run rules (2:46 am)
- **Phone reader:** full screen; menu hides while reading, tap the top edge to bring it back.
- **Structure:** units > lessons, one idea per lesson.
- **Our project:** main text is general physics; our stars and runs appear as worked examples and problems.
- **Order tonight:** build the learning interface FIRST (ask Ahmed about it so he knows what is being built), then as many lessons as fit; clear every doubt before building.
- **Run rules:** weekly cap 60% (was 30%, then 40%; raised to 60% at 3:16 am). When the 5-hour limit nears its end, set a Python wake script for 1 minute after the reset and continue. Keep working as context grows (auto-compact at 600K; carrying 500K is fine). Same for Codex: when its limit runs out, a script wakes Claude when it resets. Keep the usage ledger. Models: Claude Opus 5.5 medium; Codex GPT-6.1 Sol at medium. Rigorous bug testing after building; 5 to 6 hours is fine.
- **Codex:** a new chat per task (`codex exec`), not his onboarding chat.

## Learning interface (round 10)
- **Own app feel:** its own full-screen space with its own home, still part of the book site.
- **Learning home:** Continue (exact spot), unit map (done / not done), My notes (all highlights and notes), Problems due (skipped or wrong).
- **Saving:** sync phone and PC through the cloud store the Eyes answers already use (Claude checks how that store works and tests sync on a test record only, never on the live Eyes page).
- **Lesson page:** thin progress bar, side contents (PC; swipe-in on phone), next / previous controls that are minimal and cool, not big. No estimated time.

## Problems, plots, voice, exam (round 11)
- **Problems:** typed answers (numbers or choices), checked instantly, worked solution opens after.
- **Plots:** real TESS light of design stars only (never fence A/B or sealed stars).
- **Read-aloud:** follow-along sentence highlight with scrolling, tap a paragraph to start there, voice picker (remembered), sleep timer, plus speed control.
- **Keystone exam:** built later, after the units it tests exist.

## Content and Codex (round 12)
- **Unit order:** data first: start from a light curve on screen, pull in the physics as each idea is needed.
- **Facts:** check sources (NASA, papers, textbooks) before writing; slower, safer.
- **Tone:** conversational, like a good teacher talking, a bit of humour (still the textbook structure, no stacked summary bars).
- **Codex:** fact-checks lessons, drafts problems, tests the interface for bugs, drafts some lessons; Claude builds the big pieces, Codex the smaller ones that fit in; Claude checks everything.
- **Soul:** transitions on every part of the book; nothing just appears. Opening the site (link or home-screen icon) shows the Second Sun logo with a smooth, cool opening animation, then the Tree.
- **Testing:** rigorous: every piece built gets tested.

## Opening, safety, morning (round 13)
- **Opening animation:** full animation on the first open of the day, a quick fade otherwise.
- **Old book:** kept as a frozen backup copy he can still open.
- **If a page breaks after publish:** fix forward.
- **Morning:** Tree home page and the learning app with the first lessons, all live.

## Final round (round 14)
- **Version:** Book 3.0.
- **Recap / "where we are":** Ahmed (correcting round 5): it need not sit on top of the Tree; the Tree holds things together but not everything must be on it; some things can live on their own page. Claude decides the design.
- **Old links:** redirect to the Tree or the right new place.
- **Hunt pause snapshot:** `HUNT-PAUSED.md` at the repo root (beside COMING-BACK.md), plus a card on the Tree.

## Tree rounds (after the plan, 3:05 am)
### Tree round 1
- **Views:** both: the mission tree (root = find a planet around two suns; branches = what stops us, as TREE.md) and a journey view (the same items through time), with a toggle.
- **Alive:** grows on open; branches changed since the last visit pulse softly; zoom and pan (very high quality and smooth, research how the best do it, never a static generic zoom); search lights up matching branches.
- **Thickness / brightness:** importance (how much a branch matters for finding a planet).
- **Since last visit:** a small quiet "N new" badge; tap to see only the new things.
### Tree round 2
- **Status sign:** small icons on each branch end (active, parked, done, blocked).
- **Importance (thickness):** a weight per node written in TREE.md; Claude sets it, Ahmed can change it.
- **Journey view:** a vertical trunk through time with dates; each day's work as leaves, phases as big branches.
- **Leaf tap:** its card pops up (plain words, why it matters, result) with a quiet option to read the full report page; nothing forced in his face; calm and minimal.
### Tree round 3
- **Learning on the Tree:** linked leaves only: project branches link to their lesson; no separate learning tree.
- **PC card:** preferably opens right where the branch is on the Tree (anchored popover), not a side panel; Claude may choose a side panel if it works better.
- **Sound:** none.
- **Reports:** stay in chat as now; the Tree is extra.

## Last three rounds (3:16 am; the go is given once these are answered)
### Round 18
- **Maths today:** basic algebra (equations, fractions); powers, logs and trig rusty. The textbook builds maths from there.
- **Physics today:** school basics.
- **Device:** phone and PC equally.
- **Old progress:** start fresh; old results kept in a file.
### Round 19
- **App name:** Claude chooses (not The Textbook, Second Sun Academy or Field Guide); must be cool.
- **Logo:** refreshed by Claude: cleaner, two suns, blue theme, same idea; used in the opening animation and the app icon.
- **Hunt gate:** yes, a milestone: the hunt resumes once Ahmed finishes the units that explain the filter and the hunt (he decides when).
- **Diary:** Claude writes a short entry every work day, shown on the Tree timeline.
### Round 20
- **Handover:** a short in-app guided tour on the first open of 3.0 (Tree, Learning, Shelf), dismissible.
- **Unsettled project data:** left out of lessons; only settled things are taught.
- **Address:** "you", a general reader.
- **Tradeoff tonight:** Tree first (fully polished), fewer lessons if needed.

**GO given (Ahmed, 3:16 am): start as soon as round 20 is answered.**
