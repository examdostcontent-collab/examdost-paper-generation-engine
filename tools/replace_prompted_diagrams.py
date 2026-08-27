from __future__ import annotations

import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

from lxml import etree
from PIL import Image


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}
W_NS = NS["w"]
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
TARGET_WIDTH_EMU = int(4.45 * 914400)


def text_of(node: etree._Element) -> str:
    return " ".join(node.xpath(".//w:t/text()", namespaces=NS)).strip()


def fields(table: etree._Element) -> dict[str, etree._Element]:
    result: dict[str, etree._Element] = {}
    for row in table.xpath("./w:tr", namespaces=NS):
        cells = row.xpath("./w:tc", namespaces=NS)
        if len(cells) >= 2:
            result[text_of(cells[0])] = cells[1]
    return result


def center_paragraph(paragraph: etree._Element) -> None:
    ppr = paragraph.find(f"{{{W_NS}}}pPr")
    if ppr is None:
        ppr = etree.Element(f"{{{W_NS}}}pPr")
        paragraph.insert(0, ppr)
    jc = ppr.find(f"{{{W_NS}}}jc")
    if jc is None:
        jc = etree.SubElement(ppr, f"{{{W_NS}}}jc")
    jc.set(f"{{{W_NS}}}val", "center")


def resize_picture(paragraph: etree._Element, width: int, height: int) -> None:
    for extent in paragraph.xpath(".//wp:extent | .//a:xfrm/a:ext", namespaces=NS):
        extent.set("cx", str(width))
        extent.set("cy", str(height))


def main() -> None:
    source = Path(sys.argv[1])
    prompt_json = Path(sys.argv[2])
    image_dir = Path(sys.argv[3])
    output = Path(sys.argv[4])
    records = json.loads(prompt_json.read_text(encoding="utf-8"))
    by_question = {str(item["question"]): item for item in records}

    with zipfile.ZipFile(source, "r") as zin:
        document = etree.fromstring(zin.read("word/document.xml"))
        relationships = etree.fromstring(zin.read("word/_rels/document.xml.rels"))
        rel_map = {
            rel.get("Id"): rel.get("Target")
            for rel in relationships.findall(f"{{{REL_NS}}}Relationship")
        }

        replacements: dict[str, bytes] = {}
        changed_questions: list[str] = []
        for table in document.xpath(".//w:tbl", namespaces=NS):
            rows = fields(table)
            body = rows.get("Body")
            question_cell = rows.get("Question")
            if body is None or question_cell is None:
                continue
            question = text_of(question_cell)
            if question not in by_question:
                continue

            prompt_paragraphs = [
                paragraph
                for paragraph in body.xpath("./w:p", namespaces=NS)
                if "gemini prompt" in text_of(paragraph).lower()
            ]
            if len(prompt_paragraphs) != 1:
                raise RuntimeError(
                    f"Question {question}: expected one Gemini prompt paragraph, found {len(prompt_paragraphs)}"
                )
            for paragraph in prompt_paragraphs:
                body.remove(paragraph)

            image_paragraphs = [
                paragraph
                for paragraph in body.xpath("./w:p", namespaces=NS)
                if paragraph.xpath(".//a:blip", namespaces=NS)
            ]
            if len(image_paragraphs) != 1:
                raise RuntimeError(
                    f"Question {question}: expected one existing diagram, found {len(image_paragraphs)}"
                )
            paragraph = image_paragraphs[0]
            rel_ids = paragraph.xpath(".//a:blip/@r:embed", namespaces=NS)
            if len(rel_ids) != 1:
                raise RuntimeError(f"Question {question}: diagram relationship is ambiguous")
            target = rel_map[rel_ids[0]]
            if not target.startswith("media/"):
                raise RuntimeError(f"Question {question}: unexpected diagram target {target}")

            replacement_path = image_dir / f"q{question}.png"
            replacement = replacement_path.read_bytes()
            with Image.open(io.BytesIO(replacement)) as image:
                ratio = image.height / image.width
            height = int(TARGET_WIDTH_EMU * ratio)
            center_paragraph(paragraph)
            resize_picture(paragraph, TARGET_WIDTH_EMU, height)
            replacements[f"word/{target}"] = replacement
            changed_questions.append(question)

        if len(changed_questions) != len(records):
            missing = sorted(set(by_question) - set(changed_questions), key=int)
            raise RuntimeError(f"Only replaced {len(changed_questions)} diagrams; missing {missing}")

        remaining_prompts = document.xpath(
            ".//w:t[contains(translate(., 'GEMINI PROMPT', 'gemini prompt'), 'gemini prompt')]",
            namespaces=NS,
        )
        if remaining_prompts:
            raise RuntimeError(f"Gemini prompt text remains in {len(remaining_prompts)} runs")

        document_bytes = etree.tostring(
            document,
            xml_declaration=True,
            encoding="UTF-8",
            standalone=True,
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for entry in zin.infolist():
                if entry.filename == "word/document.xml":
                    data = document_bytes
                elif entry.filename in replacements:
                    data = replacements[entry.filename]
                else:
                    data = zin.read(entry.filename)
                zout.writestr(entry, data)

    print(
        json.dumps(
            {
                "output": str(output),
                "diagrams_replaced": len(changed_questions),
                "prompt_paragraphs_removed": len(changed_questions),
                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
