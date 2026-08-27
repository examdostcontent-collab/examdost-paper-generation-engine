from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

from lxml import etree


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "v": "urn:schemas-microsoft-com:vml",
}
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def text_of(node: etree._Element) -> str:
    values = node.xpath(".//w:t/text()", namespaces=NS)
    return " ".join(v for v in values if v).strip()


def field_rows(table: etree._Element) -> dict[str, etree._Element]:
    result: dict[str, etree._Element] = {}
    for row in table.xpath("./w:tr", namespaces=NS):
        cells = row.xpath("./w:tc", namespaces=NS)
        if len(cells) >= 2:
            result[text_of(cells[0])] = cells[1]
    return result


def main() -> None:
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    with zipfile.ZipFile(source) as archive:
        document = etree.fromstring(archive.read("word/document.xml"))
        rels = etree.fromstring(archive.read("word/_rels/document.xml.rels"))
        rel_map = {
            rel.get("Id"): rel.get("Target")
            for rel in rels.findall(f"{{{REL_NS}}}Relationship")
        }
        records = []
        for table_index, table in enumerate(
            document.xpath(".//w:tbl", namespaces=NS), start=1
        ):
            rows = field_rows(table)
            body = rows.get("Body")
            if body is None:
                continue
            body_text = text_of(body)
            marker = re.search(r"\[\s*Image\s*[—-]\s*Gemini prompt\s*\]", body_text, re.I)
            if not marker:
                continue
            prompt_text = body_text[marker.end() :].strip()
            question = text_of(rows.get("Question")) if rows.get("Question") is not None else ""
            ots = text_of(rows.get("OTS ID")) if rows.get("OTS ID") is not None else ""
            rel_ids = []
            for value in body.xpath(".//@r:embed | .//@r:id", namespaces=NS):
                if value not in rel_ids:
                    rel_ids.append(value)
            images = [
                {"rid": rid, "target": rel_map.get(rid, "")}
                for rid in rel_ids
                if rel_map.get(rid, "").startswith("media/")
            ]
            records.append(
                {
                    "table": table_index,
                    "question": question,
                    "ots_id": ots,
                    "prompt": prompt_text,
                    "images": images,
                }
            )
    destination.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"prompts={len(records)} output={destination}")


if __name__ == "__main__":
    main()
