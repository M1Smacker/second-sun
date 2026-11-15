"""Apply the brief's folds while keeping the existing detailed rules verbatim."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SHORT = {
    "eyes.md": """- Look for a dip that comes back up. Choose Dip, No dip, Odd or Not sure.
- Practice reveals the truth after each answer. Tests reveal it at the end.
- Answers are locked and saved after every card. Use Review to look back.
- Standard, hard and rehearsal results each have their own pass line.
""",
    "rehearsal.md": """- Look at the whole sector, the event up close and its place in the binary orbit.
- Choose an answer and optionally your confidence, then lock it to see the truth.
- Every locked answer is saved. Back to the start returns to the session controls.
""",
}

for name, short in SHORT.items():
    file = ROOT / "book/docs" / name
    text = file.read_text(encoding="utf-8")
    if '<details class="ss-eyes-help"' in text:
        continue
    before, guidance = text.split("## How it works\n\n", 1)
    tail = ""
    if "\n## Honest limits" in guidance:
        guidance, tail = guidance.split("\n## Honest limits", 1)
        tail = "\n## Honest limits" + tail
    fold = '<details class="ss-eyes-help" markdown="1">\n<summary>How it works</summary>\n<div markdown="1">\n\n'
    fold += short + '\n<details markdown="1">\n<summary>Full guidance and test rules</summary>\n\n'
    fold += guidance.rstrip() + '\n\n</details>\n</div>\n</details>\n'
    file.write_text(before + fold + tail, encoding="utf-8", newline="\n")
print("Folded help on 2 pages. Original detailed rules retained.")
