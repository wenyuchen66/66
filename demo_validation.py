"""Run three examples with python demo_validation.py."""

from validation import validate_poem


def main() -> None:
    poem = [
        "Clean functions make the logic clear,",
        "One loop can bring the answer near.",
        "Debug each step to see what's wrong,",
        "Each passing test moves us along.",
    ]
    wrong_initial = poem.copy()
    wrong_initial[2] = "Trace each step to see what's wrong,"

    examples = [
        ("Valid poem", poem, []),
        ("Wrong first letter", wrong_initial, ["Line 3: expected D, got 'T'."]),
        ("Missing line", poem[:3], ["Expected 4 lines, got 3."]),
    ]

    for label, lines, expected in examples:
        errors = validate_poem("CODE", lines)
        if errors != expected:
            raise AssertionError(f"{label}: expected {expected!r}, got {errors!r}")
        print(f"{label}: {'; '.join(errors) if errors else 'OK'}")


if __name__ == "__main__":
    main()
