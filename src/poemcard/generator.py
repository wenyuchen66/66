"""Generate English acrostics with a local Ollama language model.

Public interface: generate_poem(word, theme) -> list[str].
Requires Python 3.9+ and a running Ollama server with the chosen model.
"""

import json
import os
import re
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_MODEL = "qwen2.5:3b"
_INSTRUCTIONS = (
    "Write English acrostic poems in simple, natural language. "
    "Use concrete details about the theme to tell a small, coherent story. "
    "Each verse should be a meaningful phrase of about 6 to 12 words. "
    "Start each verse with a normal English word beginning with the requested letter. "
    "Rhyme is optional. Return a JSON object with one verse per requested field. "
    "Exclude headings, numbering, Markdown, and isolated acrostic letters."
)


def _request_poem(messages: list[dict], schema: dict) -> str:
    model = os.environ.get("POEM_MODEL", DEFAULT_MODEL)
    base_url = os.environ.get("POEM_OLLAMA_URL", "http://127.0.0.1:11434")
    request = Request(
        base_url.rstrip("/") + "/api/chat",
        data=json.dumps({
            "model": model,
            "messages": messages,
            "stream": False,
            "format": schema,
            "options": {"temperature": 0.7, "num_predict": 800},
        }).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urlopen(request, timeout=120) as response:
            content = json.load(response)["message"]["content"]
    except HTTPError as exc:
        if exc.code == 404:
            raise RuntimeError(f"Model unavailable. Download it with: ollama pull {model}") from exc
        raise RuntimeError(f"Ollama returned HTTP {exc.code}. Check the Ollama server.") from exc
    except (URLError, OSError) as exc:
        raise RuntimeError(
            "Could not connect to Ollama or generation timed out. "
            "Start Ollama and check POEM_OLLAMA_URL."
        ) from exc
    except (KeyError, TypeError, ValueError) as exc:
        raise RuntimeError("Ollama returned an invalid response.") from exc
    if not isinstance(content, str):
        raise RuntimeError("Ollama returned invalid poem content.")
    return content


def generate_poem(word: str, theme: str) -> list[str]:
    """Return an English acrostic about a freely supplied theme.

    word must contain 3–8 ASCII letters, ignoring surrounding whitespace.
    Letter comparisons ignore case. theme must be a nonempty string.
    Returns a list containing one verse per letter, in order.
    Raises ValueError for invalid input and RuntimeError if generation fails.
    """
    if not isinstance(word, str) or not re.fullmatch(r"[A-Za-z]{3,8}", word.strip()):
        raise ValueError("word must contain 3 to 8 English letters (A–Z).")
    if not isinstance(theme, str) or not theme.strip():
        raise ValueError("theme must be a nonempty string.")

    initials = word.strip().upper()
    fields = [f"line_{index}" for index in range(1, len(initials) + 1)]
    schema = {
        "type": "object",
        "properties": {
            field: {
                "type": "string",
                "description": f"A verse starting with an English word beginning with {letter}.",
                "pattern": rf"^[{letter}{letter.lower()}][^\r\n]+$",
            }
            for field, letter in zip(fields, initials)
        },
        "required": fields,
        "additionalProperties": False,
    }
    prompt = (
        f"Write an English poem specifically about {json.dumps(theme.strip(), ensure_ascii=False)}. "
        "Show someone experiencing this theme through concrete actions and details. "
        f"Write exactly {len(initials)} lines.\n"
        "Return a JSON object with the following verses in order:\n"
        + "\n".join(
            f"{field} must begin with an English word starting with {letter}."
            for field, letter in zip(fields, initials)
        )
    )
    messages = [
        {"role": "system", "content": _INSTRUCTIONS},
        {"role": "user", "content": prompt},
    ]
    for attempt in range(3):
        content = _request_poem(messages, schema)
        try:
            poem = json.loads(content)
        except json.JSONDecodeError:
            poem = None
        if isinstance(poem, dict) and poem.keys() == schema["properties"].keys():
            lines = [poem[field].strip() if isinstance(poem[field], str) else "" for field in fields]
            if all(
                len(line.splitlines()) == 1
                and len(line.split()) > 1
                and line[0].isascii()
                and line[0].upper() == letter
                for line, letter in zip(lines, initials)
            ):
                return lines
        if attempt < 2:
            messages.append({
                "role": "user",
                "content": (
                    "The previous output had an invalid structure. Generate the whole poem again. "
                    f"Return exactly these fields in order: {', '.join(fields)}. "
                    f"Their first letters must be {', '.join(initials)}. "
                    "Each field must contain one complete line."
                ),
            })
    raise RuntimeError(f"The model failed to produce a valid {initials} poem after 3 attempts.")


def _main() -> None:
    print("英文藏头诗生成器\n")
    while True:
        try:
            word = input("藏头词（3–8 个英文字母，直接回车退出）> ")
            if not word.strip():
                return
            theme = input("主题（自由填写）> ")
            print("正在写诗…", flush=True)
            lines = generate_poem(word, theme)
        except (EOFError, KeyboardInterrupt):
            print()
            return
        except ValueError as error:
            print(f"输入有误。{error}\n")
        except RuntimeError as error:
            print(f"生成失败。{error}\n")
        else:
            print(f"\n{word.strip().upper()} / {theme.strip()}")
            print(*lines, sep="\n", end="\n\n")


if __name__ == "__main__":
    _main()
