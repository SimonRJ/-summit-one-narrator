"""Add the independently worked variation to each published companion film."""
from html import escape
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VARIATIONS = json.loads(Path(__file__).with_name("companion_variations.json").read_text())
TRANSCRIPT = '<details class="transcript">'
EXPECTED = {f"T{number:02}.{suffix}" for number in range(1, 19) for suffix in "123E"}


def variation_section(lesson):
    question, answer = (VARIATIONS[lesson][field] for field in ("question", "answer"))
    return (
        '<section class="exercise companion-variation" aria-labelledby="variation-title">\n'
        '<h2 id="variation-title">Try a variation</h2>\n'
        f'<p>{escape(question)}</p>\n'
        f'<details><summary>See the worked answer</summary><p>{escape(answer)}</p></details>\n'
        '</section>\n'
    )


def install():
    if set(VARIATIONS) != EXPECTED or len({v["question"] for v in VARIATIONS.values()}) != 72:
        raise ValueError("Expected a distinct variation for each of the 72 companion films")
    for lesson in sorted(VARIATIONS):
        name = "watch-" + lesson.lower().replace(".", "-") + ".html"
        paths = [ROOT / name]
        if lesson in ("T02.1", "T02.2"):
            paths.append(ROOT / "production" / ("t021-studio" if lesson == "T02.1" else "t022-studio") / name)
        for path in paths:
            page = path.read_text()
            variation = variation_section(lesson)
            if variation in page:
                continue
            if page.count(TRANSCRIPT) != 1 or 'class="exercise companion-variation"' in page:
                raise ValueError(f"Check the existing transcript or variation on {path}")
            path.write_text(page.replace(TRANSCRIPT, variation + TRANSCRIPT))


if __name__ == "__main__":
    install()
