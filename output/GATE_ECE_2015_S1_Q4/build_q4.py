import os
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.dirname(os.path.abspath(__file__))
COL_LABEL, COL_BODY = 2200, 6826

S = r"\scriptstyle "

body_p1 = (
    "Operators $" + S + r"\square$, $" + S + r"\lozenge$ and $" + S + r"\rightarrow$ are defined by: $" + S + r"a\ \square\ b=\tfrac{a-b}{a+b}$; $" + S + r"a\ \lozenge\ b=\tfrac{a+b}{a-b}$; $" + S + r"a\rightarrow b=ab$."
)
body_p2 = "Find the value of $" + S + r"(66\ \square\ 6)\rightarrow(66\ \lozenge\ 6)$."

options = [
    "$" + S + r"-2$",
    "$" + S + r"-1$",
    "$" + S + r"1$",
    "$" + S + r"2$",
]

explanation = [
    "Given: $" + S + r"a\ \square\ b=\tfrac{a-b}{a+b}$, $" + S + r"a\ \lozenge\ b=\tfrac{a+b}{a-b}$ and $" + S + r"a\rightarrow b=ab$, to be evaluated for $" + S + r"a=66,\ b=6$.",
    "Step 1: $" + S + r"66\ \square\ 6=\tfrac{66-6}{66+6}=\tfrac{60}{72}=\tfrac{5}{6}$.",
    "Step 2: $" + S + r"66\ \lozenge\ 6=\tfrac{66+6}{66-6}=\tfrac{72}{60}=\tfrac{6}{5}$.",
    "Step 3: apply $" + S + r"\rightarrow$, which multiplies its two operands: $" + S + r"\tfrac{5}{6}\rightarrow\tfrac{6}{5}=\tfrac{5}{6}\times\tfrac{6}{5}=1$.",
    "Hence the correct option is (3).",
    "",
    "Tip: Evaluate each bracket separately first. Here $" + S + r"66\ \square\ 6$ and $" + S + r"66\ \lozenge\ 6$ are reciprocals of each other, because swapping the numerator and denominator of $" + S + r"\tfrac{a-b}{a+b}$ gives $" + S + r"\tfrac{a+b}{a-b}$, so their product under $" + S + r"\rightarrow$ is $" + S + r"1$ for any $" + S + r"a\neq b$.",
]

rows_after_options = [
    ("Correct", ["3"]),
    ("Explanation", explanation),
    ("Subject", ["Numerical Ability"]),
    ("Topic", ["Algebra (Algebraic Identities)"]),
    ("Correct Marks", ["1"]),
    ("Incorrect Marks", ["0.33"]),
    ("Hint", ["-"]),
    ("Video Solution", ["-"]),
    ("PYQ", ["GATE ECE 2015 - 1"]),
    ("OTS ID", [""]),
]


def set_cell_border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "AAAAAA")
        b.append(e)
    tcPr.append(b)


def set_cell_width(cell, w):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:tcW")):
        tcPr.remove(old)
    tcW = OxmlElement("w:tcW")
    tcW.set(qn("w:w"), str(w))
    tcW.set(qn("w:type"), "dxa")
    tcPr.insert(0, tcW)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), fill)
    tcPr.append(sh)


def fill_cell(cell, paras, label=False):
    first = True
    for t in paras:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        r = p.add_run(t)
        r.font.size = Pt(10.5)
        r.font.name = "Calibri"
        if label:
            r.bold = True


doc = Document()
sec = doc.sections[0]
sec.left_margin = sec.right_margin = Inches(0.8)

fields = [("Question", ["1"]), ("Type", ["MCQ"])]
n_rows = 2 + 1 + 4 + len(rows_after_options)
tbl = doc.add_table(rows=n_rows, cols=2)
tbl.autofit = False

tblPr = tbl._tbl.tblPr
for old in tblPr.findall(qn("w:tblW")):
    tblPr.remove(old)
tblW = OxmlElement("w:tblW")
tblW.set(qn("w:w"), str(COL_LABEL + COL_BODY))
tblW.set(qn("w:type"), "dxa")
tblPr.append(tblW)
lay = OxmlElement("w:tblLayout")
lay.set(qn("w:type"), "fixed")
tblPr.append(lay)
grid = tbl._tbl.tblGrid
for gc, w in zip(grid.findall(qn("w:gridCol")), (COL_LABEL, COL_BODY)):
    gc.set(qn("w:w"), str(w))

ri = 0


def add_row(label, paras, image=None):
    global ri
    row = tbl.rows[ri]
    ri += 1
    lc, vc = row.cells
    for c, w in ((lc, COL_LABEL), (vc, COL_BODY)):
        set_cell_width(c, w)
        set_cell_border(c)
    shade(lc, "F2F2F2")
    fill_cell(lc, [label], label=True)
    if image is None:
        fill_cell(vc, paras)
    else:
        fill_cell(vc, [paras[0]])
        pp = vc.add_paragraph()
        pp.add_run().add_picture(image, width=Inches(4.5))
        p3 = vc.add_paragraph()
        r = p3.add_run(paras[1])
        r.font.size = Pt(10.5)
        r.font.name = "Calibri"


add_row("Question", ["1"])
add_row("Type", ["MCQ"])
add_row("Body", [body_p1, body_p2])
for o in options:
    add_row("Option", [o])
for label, paras in rows_after_options:
    add_row(label, paras)

path = os.path.join(OUT, "GATE_ECE_2015_S1_Q4_box.docx")
doc.save(path)
print(path)
