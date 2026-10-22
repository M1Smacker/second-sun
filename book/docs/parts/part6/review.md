# Review: Part 6, How the project runs

<p class="ss-meta">Check yourself · about 5 minutes · no scores, nothing is saved</p>

!!! plain "In plain words"
    Try each question before you tap it. The answer opens underneath. If one surprises you, the chapter is one tap away.

## Chapter 13: Your workshop

[Read the chapter](../../book/13-your-workshop.md)

??? quiz "1. Why isn't the data folder in git?"
    It's large, and NASA's MAST keeps the originals, so anyone can download it again. Git holds the code, the lists and the records that say exactly which files we used.

??? quiz "2. Where would you look to find out why we chose G1?"
    `research/decisions.md` (dated, with your words), and the field note of [19 October](../../field-notes/2026-10-19.md).

??? quiz "3. What does 'Book is 3 commits behind' mean?"
    Three changes to code or research were saved after the last field note. The same-day rule says a field note should be written before the work is called finished.

## Chapter 15: Our mistakes, as lessons

[Read the chapter](../../book/15-mistakes-as-lessons.md)

??? quiz "1. Three of the number mistakes were caught while writing labs. Why do labs catch mistakes?"
    A lab must print real output from real data. A wrong assumption in a report can sit unnoticed; in a lab it produces output that doesn't make sense (a period off the grid, a star with no eclipses), and someone has to explain it.

??? quiz "2. Which lesson does the morph = −1 mistake belong to, and what's the general rule?"
    Lesson 1. Catalogues use codes like −1, 0 or "nan" for "missing". Any cut like "less than 0.5" must decide on purpose what happens to them.

??? quiz "3. Why log mistakes at all? It's embarrassing."
    So the next person (or session) doesn't repeat them, so you can judge how much to trust the work, and because a hidden mistake keeps doing damage. A logged one turns into a rule.

---

[Try it yourself: Part 6](labs.md) · [Back to the chapters](../../start/index.md)
