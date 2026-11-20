# Poemcard

Poemcard turns an English word and a theme into a printable acrostic card. For a coding club, for example, the word CODE can hide the club's message down the left edge while the poem describes Python programming. A local language model writes the verse. Poemcard checks the line count and initials before Pillow draws the card with the initials highlighted.

## Setup

Install Python 3.9 or later and [Ollama](https://ollama.com/). Start Ollama and run:

```sh
ollama pull qwen2.5:3b
python -m pip install poemcard
```

## Generate a card

```sh
python -m poemcard.Englishpoem CODE --theme "Python programming" --output code_poem.png
```

Choose a word of 3 to 8 English letters and a theme. Open the output PNG and read the highlighted initials from top to bottom. For a wildlife card, try the same word with the theme "pythons in the wild".

## Reuse the validator

Use the same check for poems written by students or produced by another generator. This step runs locally without starting Ollama.

```python
from poemcard import validate_poem

lines = ["Code lights the screen.", "Our loops hum.", "Tests greet the dawn.", "Each bug fades."]
errors = validate_poem("CODE", lines)
print(errors)  # ["Line 3: expected D, got 'T'."]
lines[2] = "Dawn finds the last bug."
print(validate_poem("CODE", lines))  # []
```

[GitHub repository](https://github.com/wenyuchen66/66) · [PyPI release](https://pypi.org/project/poemcard/0.1.1/)

## License

MIT License
