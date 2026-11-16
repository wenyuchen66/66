"""Check whether the first letters of a poem spell a given word."""

import re


def validate_poem(word: str, lines: list[str]) -> list[str]:
    """Return an empty list for a valid acrostic, or a list of errors.

    The word must contain 3 to 8 ASCII letters. Surrounding whitespace
    and letter case are ignored. Each list entry counts as one line,
    including blank entries. Leading whitespace in a line is ignored.
    """
    if not isinstance(word, str) or re.fullmatch(r"[A-Za-z]{3,8}", word.strip()) is None:
        return ["The acrostic word must contain 3 to 8 English letters."]
    if not isinstance(lines, list) or any(not isinstance(line, str) for line in lines):
        return ["Poem lines must be provided as a list of strings."]

    word = word.strip().upper()
    errors = []
    if len(lines) != len(word):
        errors.append(f"Expected {len(word)} lines, got {len(lines)}.")

    for number, (expected, line) in enumerate(zip(word, lines), start=1):
        first = line.lstrip()[:1]
        if not first:
            errors.append(f"Line {number}: expected {expected}, but the line is blank.")
        elif not first.isascii() or first.upper() != expected:
            errors.append(f"Line {number}: expected {expected}, got {first.upper()!r}.")

    return errors
