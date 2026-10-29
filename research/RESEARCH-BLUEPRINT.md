# Research blueprint: how to research deeply and keep only true results

Written 29 Oct 2026 after the Vesper study, at Ahmed's request. The first research pass that day took about 5 minutes and leaned on search-engine summaries; the second pass (about 10 minutes, primary pages opened and searched) found four things the first missed: our pass rule sat inside the measurement noise, a 2026 paper that solves our exact problem, a second failure mode of our smoothing, and that our planned test planet was in the sealed slice. This file is the method of the second pass. Use it for every research task in Second Sun.

## 1. Before searching: write the questions
- Write 3 to 6 questions. Each one names the **decision it feeds** ("this decides the smoothing window of C1"). A question that feeds no decision is dropped.
- Write what our own data already says on each question, with the file. **Cheapest check first:** our files and a script that can contradict me, then the web.
- Write what answer would change the plan. If no possible answer would change it, skip the question.

## 2. Check our own house first
- **Does the measurement have the precision for the claim?** Bootstrap the number before judging a change by it (the K50 was only good to +-6 to 10%, so "10% better" was noise). Prefer paired comparisons on identical inputs.
- **Does anything we plan to use cross a rule?** Check every star, file and dataset against the sealed list, the frozen settings and Ahmed's rules (TOI-1338 was in the sealed slice).
- Re-read the relevant result files, not memory or the summary.

## 3. Search wide, then go to the source
1. **Wide:** several searches in one go, different wordings; include the current year (new papers matter: the closest model for our work was 3 weeks old). Restrict to arxiv.org or official sites when the topic is technical.
2. **Primary:** open the paper itself. On arXiv use the abstract page (`arxiv.org/abs/ID`) and the HTML full text (`arxiv.org/html/IDvN`). **Never open a PDF, FITS, CSV or ZIP link in the browser pane** (it pops a save dialog on Ahmed's PC).
3. **Pull the exact sentence:** in the HTML page, search the text for the key words (a small JavaScript search for terms like "window", "threshold", "inject", "vett") and read the paragraph around each hit. A search-engine summary is a lead, never a source.
4. **Read the method, not only the result:** how they detrend, the threshold, how they vet, how they measured completeness. The method is where our design ideas come from.
5. **Follow one link deeper** when a paper cites the thing we need (the Oddo paper pointed to Martin and Fabrycky's variable-window detrend and to LEO-vetter).

## 4. Judge what is true
- Label every finding: **CONFIRMED** (I read it in the primary text or our own data shows it), **LIKELY** (a secondary page, or reasoned and partly checked), **UNCERTAIN** (not opened, or sources disagree), **NOT TESTED** (an idea).
- Cross-check important numbers against a second source or against our own data. If two sources disagree, write both and say which I trust and why.
- Never invent a citation, an arXiv number or a number from memory. If I could not open it, say so ("the arXiv entry was not found") and lift the label only after opening it.
- Separate what the paper measured from what it assumed (Oddo et al. assume a 6 Earth-radius planet at 6.27 x the binary period for their duration prediction: an assumption, not a measurement).

## 5. Turn findings into decisions
- For each question: the answer, its label, its link, and **what changes in our plan** (a new hypothesis, a changed design, an amended pass rule).
- Rules that judge experiments are fixed or amended, with the date, **before** the experiment runs, never after seeing results.
- New risks or doubts go into the fix queue at once.

## 6. When to stop
- Stop when every question has an answer that feeds its decision, at CONFIRMED or with a clear reason why not.
- Spend at least about 10 minutes on a serious question even if the first summary looks good; the first pass usually misses the method details.
- Do not pad: if a question is answered in our own data, the web is not needed.

## 7. File it
- One literature file per study (`research/stage3/<study>-literature-<date>.md`): one section per question, each with the source link, the label and the decision fed; an addendum for a second pass.
- Update the study plan's results section, the version notes if a baseline fact changed, the fix queue, the usage ledger (estimate first, measured after) and RESUME.
- Commit and push the same session.

## 8. Choosing the model
Deep research and design (reading methods, judging statistics, writing designs) on the strongest model Ahmed picks (Opus 5.5 on 29 Oct); building and long machine runs on Sonnet 5.5 extra. Stop and tell Ahmed at each switch point.
