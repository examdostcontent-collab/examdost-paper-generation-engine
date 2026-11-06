from copy import deepcopy
from io import BytesIO
from pathlib import Path
import shutil

from docx import Document
from docx.shared import Emu


SOURCE = Path(r"E:\Office - Examdost\ExamDost\Temp Work\Done\Signals and Systems (517 - 626).docx")
TARGET = Path(r"E:\Office - Examdost\ExamDost\claude work files\GATE Test Series\Signals and Systems (517 - 626) (final).docx")
BACKUP = TARGET.with_name(TARGET.stem + " - before missing visuals merge.docx")

# These source visuals are equations that are already present as LaTeX in the
# target, so they must not be inserted a second time as screenshots.
LATEX_ALREADY_PRESENT = {524, 530, 548, 549, 554, 625}


def image_runs(cell):
    """Return (paragraph index, relationship id, width, height) per inline image."""
    found = []
    for p_index, paragraph in enumerate(cell.paragraphs):
        for run in paragraph.runs:
            for inline in run._element.xpath('.//wp:inline'):
                blip = inline.xpath('.//a:blip')[0]
                extent = inline.xpath('./wp:extent')[0]
                found.append((p_index, blip.embed, int(extent.cx), int(extent.cy)))
    return found


source = Document(SOURCE)
target = Document(TARGET)
if len(source.tables) != len(target.tables):
    raise RuntimeError("The two files do not contain the same number of question tables.")

shutil.copy2(TARGET, BACKUP)
inserted = []
for table_index, (source_table, target_table) in enumerate(zip(source.tables, target.tables)):
    question_number = 517 + table_index
    if question_number in LATEX_ALREADY_PRESENT:
        continue

    for row_index, source_row in enumerate(source_table.rows):
        source_cell = source_row.cells[-1]
        target_cell = target_table.rows[row_index].cells[-1]
        source_images = image_runs(source_cell)
        target_images = image_runs(target_cell)

        # The final document may contain converted LaTeX, but it has no matching
        # inline visual in this field. Add only the surplus source visuals.
        for paragraph_index, relationship_id, width, height in source_images[len(target_images):]:
            image_part = source.part.related_parts[relationship_id]
            destination_paragraph = target_cell.paragraphs[
                min(paragraph_index, len(target_cell.paragraphs) - 1)
            ]
            destination_paragraph.add_run().add_picture(
                BytesIO(image_part.blob), width=Emu(width), height=Emu(height)
            )
            inserted.append((question_number, source_row.cells[0].text.strip()))

target.save(TARGET)
print(f"Backup: {BACKUP}")
print(f"Inserted {len(inserted)} missing visuals across {len(set(inserted))} question fields.")
print("Questions:", ", ".join(str(q) for q, _ in inserted))
