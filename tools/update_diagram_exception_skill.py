from __future__ import annotations

import sys
from pathlib import Path


HEADING = "### Explicit Prompt-to-Diagram Replacement Exception"
SECTION = r'''### Explicit Prompt-to-Diagram Replacement Exception

When the user explicitly supplies a Word file containing Gemini diagram prompts and asks for those
prompts to be turned into diagrams, this instruction overrides the normal copy-as-is rule below:

1. Read each prompt and redraw only its associated diagram.
2. Remove both the prompt paragraph and the existing diagram, then insert the new diagram at the
   same position. Do not change any question, option, answer, solution, mark, code, or other text.
3. Use a tightly cropped canvas: the circuit/figure must occupy the available diagram area with only
   a small even safety margin and no large unused blank region, so it remains clearly visible in Word.
4. Preserve every label exactly, including uppercase/lowercase, values, units, polarity marks,
   superscripts, and subscripts (for example, `V_{in}`, `R_S`, `V_{CC}`, and `R_L`).
5. Unless the embedded prompt states otherwise, use Segoe UI 11 pt, 1 pt black linework, a white
   background, high contrast, and no title, border, watermark, shading, or decorative content.
6. Validate every generated diagram visually before insertion, and visually verify the final Word
   pages after replacement.

This exception applies only after an explicit user request to redraw/replace prompted diagrams.
Otherwise, follow the copy-as-is rule below.
'''


def main() -> None:
    path = Path(sys.argv[1])
    text = path.read_text(encoding="utf-8")
    if HEADING in text:
        print("already-present")
        return
    marker = "## Diagram Handling\n"
    if marker not in text:
        raise RuntimeError("Diagram Handling section not found")
    text = text.replace(marker, marker + "\n" + SECTION + "\n", 1)
    path.write_text(text, encoding="utf-8")
    print("updated")


if __name__ == "__main__":
    main()
