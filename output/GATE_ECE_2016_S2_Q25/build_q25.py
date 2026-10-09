import os
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = os.path.dirname(os.path.abspath(__file__))
COL_LABEL, COL_BODY = 2200, 6826
S = r"\scriptstyle "

body_p1 = (
    "Light from free space is incident at an angle $" + S + r"\theta_i$ to the normal of the facet of a step-index large core optical fibre. "
    "The core and cladding refractive indices are $" + S + r"n_1=1.5$ and $" + S + r"n_2=1.4$, respectively."
)
body_p2 = (
    "The maximum value of $" + S + r"\theta_i$ (in degrees) for which the incident light will be guided in the core of the fibre is ________"
)

explanation = [
    "Given: free-space index $" + S + r"n_0=1$, core index $" + S + r"n_1=1.5$, cladding index $" + S + r"n_2=1.4$.",
    "Concept: light stays guided only when it undergoes total internal reflection at the core-cladding boundary. "
    "Let $" + S + r"\theta_r$ be the refraction angle inside the core at the fibre facet. The ray then meets the core-cladding boundary at an angle of incidence $" + S + r"90^{\circ}-\theta_r$.",
    "Refraction at the facet (Snell's law): $" + S + r"\sin\theta_i=n_1\sin\theta_r$.",
    "Limiting case of total internal reflection: $" + S + r"\sin(90^{\circ}-\theta_r)=\cos\theta_r=\tfrac{n_2}{n_1}$.",
    "Then $" + S + r"\sin\theta_r=\sqrt{1-\left(\tfrac{n_2}{n_1}\right)^2}=\tfrac{\sqrt{n_1^2-n_2^2}}{n_1}$.",
    "Substituting in Snell's law: $" + S + r"\sin\theta_{i,max}=n_1\sin\theta_r=\sqrt{n_1^2-n_2^2}=\sqrt{1.5^2-1.4^2}=\sqrt{0.29}=0.5385$.",
    "So $" + S + r"\theta_{i,max}=\sin^{-1}(0.5385)\approx 32.6^{\circ}$.",
    "Hence the maximum angle of incidence is about $" + S + r"32.6^{\circ}$.",
    "",
    "Tip: For a ray coming from free space, the core index cancels out and only $" + S + r"\sqrt{n_1^2-n_2^2}=\sqrt{0.29}$ matters (the numerical aperture of this fibre), so any larger angle than this lets the ray hit the cladding below the critical angle and leak out.",
]

rows_after = [
    ("Correct", ["32.5 to 32.7"]),
    ("Explanation", explanation),
    ("Subject", ["EMFT - ECE"]),
    ("Topic", ["Plane Waves (Normal and Oblique incidence of Plane Waves)"]),
    ("Correct Marks", ["1"]),
    ("Incorrect Marks", ["0"]),
    ("PYQ", ["GATE ECE 2016 - 2"]),
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
doc.sections[0].left_margin = doc.sections[0].right_margin = Inches(0.8)

n_rows = 3 + len(rows_after)
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
for gc, w in zip(tbl._tbl.tblGrid.findall(qn("w:gridCol")), (COL_LABEL, COL_BODY)):
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
        vc.add_paragraph().add_run().add_picture(image, width=Inches(4.8))
        r = vc.add_paragraph().add_run(paras[1])
        r.font.size = Pt(10.5)
        r.font.name = "Calibri"


add_row("Question", ["1"])
add_row("Type", ["NAT"])
add_row("Body", [body_p1, body_p2], image=os.path.join(OUT, "q25_diagram.png"))
for label, paras in rows_after:
    add_row(label, paras)

path = os.path.join(OUT, "GATE_ECE_2016_S2_Q25_box.docx")
doc.save(path)
print(path)
