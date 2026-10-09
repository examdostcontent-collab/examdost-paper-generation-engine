import os
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.dirname(os.path.abspath(__file__))
COL_LABEL, COL_BODY = 2200, 6826

S = r"\scriptstyle "

body_p1 = (
    "The block diagram of a frequency synthesizer consisting of a Phase Locked Loop (PLL) and a "
    "divide-by-$" + S + "N$ counter (comprising $" + S + r"\div 2,\ \div 4,\ \div 8,\ \div 16$ outputs) is sketched below. "
    "The synthesizer is excited with a $" + S + r"5\ \text{kHz}$ signal (Input 1). "
    "The free-running frequency of the PLL is set to $" + S + r"20\ \text{kHz}$. "
    "Assume that the commutator switch makes contacts repeatedly in the order 1-2-3-4."
)
body_p2 = "The corresponding frequencies synthesized are:"

options = [
    "$" + S + r"10\ \text{kHz},\ 20\ \text{kHz},\ 40\ \text{kHz},\ 80\ \text{kHz}$",
    "$" + S + r"20\ \text{kHz},\ 40\ \text{kHz},\ 80\ \text{kHz},\ 160\ \text{kHz}$",
    "$" + S + r"80\ \text{kHz},\ 40\ \text{kHz},\ 20\ \text{kHz},\ 10\ \text{kHz}$",
    "$" + S + r"160\ \text{kHz},\ 80\ \text{kHz},\ 40\ \text{kHz},\ 20\ \text{kHz}$",
]

explanation = [
    "Given: reference input $" + S + r"f_{in}=5\ \text{kHz}$; PLL free-running frequency $" + S + r"20\ \text{kHz}$; counter taps $" + S + r"\div 2,\ \div 4,\ \div 8,\ \div 16$ selected in the order 1-2-3-4.",
    "Concept: in this synthesizer the VCO output drives the divide-by-$" + S + "N$ counter, and the selected counter tap is fed back to the phase detector. "
    "The synthesizer output is the VCO output itself. When the loop is locked, the two inputs of the phase detector have the same frequency.",
    "Locked condition: $" + S + r"f_{fb}=\tfrac{f_{VCO}}{N}=f_{in}$, so $" + S + r"f_{VCO}=N\,f_{in}$.",
    "Tap 1 ($" + S + r"N=2$): $" + S + r"f_{VCO}=2\times 5=10\ \text{kHz}$.",
    "Tap 2 ($" + S + r"N=4$): $" + S + r"f_{VCO}=4\times 5=20\ \text{kHz}$.",
    "Tap 3 ($" + S + r"N=8$): $" + S + r"f_{VCO}=8\times 5=40\ \text{kHz}$.",
    "Tap 4 ($" + S + r"N=16$): $" + S + r"f_{VCO}=16\times 5=80\ \text{kHz}$.",
    "So the synthesized frequencies in the order 1-2-3-4 are $" + S + r"10\ \text{kHz},\ 20\ \text{kHz},\ 40\ \text{kHz},\ 80\ \text{kHz}$.",
    "Hence the correct option is (1).",
    "",
    "Tip: The free-running frequency of $" + S + r"20\ \text{kHz}$ only sets where the VCO starts; once the loop locks, the output is fixed by the reference as $" + S + r"f_{out}=N\,f_{ref}$, so moving the switch from tap 1 to tap 4 doubles the output at every step.",
]

rows_after_options = [
    ("Correct", ["1"]),
    ("Explanation", explanation),
    ("Subject", ["Analog Electronics"]),
    ("Topic", ["Signal Conditioning, Noise and Interference (VCO and PLL)"]),
    ("Correct Marks", ["1"]),
    ("Incorrect Marks", ["0.33"]),
    ("Hint", ["-"]),
    ("Video Solution", ["-"]),
    ("PYQ", ["GATE ECE 2016 - 1"]),
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
add_row("Body", [body_p1, body_p2], image=os.path.join(OUT, "q16_diagram.png"))
for o in options:
    add_row("Option", [o])
for label, paras in rows_after_options:
    add_row(label, paras)

path = os.path.join(OUT, "GATE_ECE_2016_S1_Q16_box.docx")
doc.save(path)
print(path)
