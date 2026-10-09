import os, sys, importlib.util
from docx import Document
from docx.shared import Pt, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import q2013_data as q13
import q2012_data as q12
import q2010_data as q10
import q2007_data as q07
import q2004_data as q04
import q2003_data as q03
import q2002_data as q02
import q2001_data as q01
import q1999_data as q99
import q1998_data as q98
import q1997_data as q97
import q1996_data as q96
import q1995_data as q95
import q1994_data as q94
import q1993_data as q93
import q1991_data as q91
COL_LABEL, COL_BODY = 2200, 6826


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


q4 = load(os.path.join(BASE, "GATE_ECE_2015_S1_Q4", "build_q4.py"), "q4")
q16 = load(os.path.join(BASE, "GATE_ECE_2016_S1_Q16", "build_q16.py"), "q16")
q25 = load(os.path.join(BASE, "GATE_ECE_2016_S2_Q25", "build_q25.py"), "q25")


def border(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    b = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement(f"w:{side}")
        e.set(qn("w:val"), "single"); e.set(qn("w:sz"), "4"); e.set(qn("w:color"), "AAAAAA")
        b.append(e)
    tcPr.append(b)


def width(cell, w):
    tcPr = cell._tc.get_or_add_tcPr()
    for old in tcPr.findall(qn("w:tcW")):
        tcPr.remove(old)
    e = OxmlElement("w:tcW"); e.set(qn("w:w"), str(w)); e.set(qn("w:type"), "dxa")
    tcPr.insert(0, e)


def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear"); sh.set(qn("w:color"), "auto"); sh.set(qn("w:fill"), fill)
    tcPr.append(sh)


def fill(cell, paras, label=False):
    first = True
    for t in paras:
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        r = p.add_run(t)
        r.font.size = Pt(10.5); r.font.name = "Calibri"
        if label:
            r.bold = True


doc = Document()
doc.sections[0].left_margin = doc.sections[0].right_margin = Inches(0.8)


def question_table(qno, qtype, body, image, image_w, options, rest, image_after=1):
    rows = [("Question", [str(qno)]), ("Type", [qtype]), ("Body", body)]
    rows += [("Option", [o]) for o in options]
    rows += rest
    tbl = doc.add_table(rows=len(rows), cols=2)
    tbl.autofit = False
    tblPr = tbl._tbl.tblPr
    for old in tblPr.findall(qn("w:tblW")):
        tblPr.remove(old)
    w = OxmlElement("w:tblW"); w.set(qn("w:w"), str(COL_LABEL + COL_BODY)); w.set(qn("w:type"), "dxa")
    tblPr.append(w)
    lay = OxmlElement("w:tblLayout"); lay.set(qn("w:type"), "fixed"); tblPr.append(lay)
    for gc, ww in zip(tbl._tbl.tblGrid.findall(qn("w:gridCol")), (COL_LABEL, COL_BODY)):
        gc.set(qn("w:w"), str(ww))
    for row, (label, paras) in zip(tbl.rows, rows):
        lc, vc = row.cells
        for c, ww in ((lc, COL_LABEL), (vc, COL_BODY)):
            width(c, ww); border(c)
        shade(lc, "F2F2F2")
        fill(lc, [label], label=True)
        if label == "Body" and image is None:
            fill(vc, paras)
        elif label == "Body":
            fill(vc, paras[:image_after])
            vc.add_paragraph().add_run().add_picture(image, width=Inches(image_w))
            for _t in paras[image_after:]:
                r = vc.add_paragraph().add_run(_t)
                r.font.size = Pt(10.5); r.font.name = "Calibri"
        else:
            fill(vc, paras)


def pb():
    doc.add_paragraph().add_run().add_break(__import__("docx").enum.text.WD_BREAK.PAGE)


_n = 0
for _q in (*q91.ALL, *q93.ALL, *q94.ALL, *q95.ALL, *q96.ALL, *q97.ALL, *q98.ALL, q99.Q9, *q01.ALL, q02.Q18, q02.Q20, q03.Q52, q04.Q86, q07.Q79, q07.Q80, q07.Q81, q10.Q22, q12.Q11, q12.Q18, q12.Q29, q12.Q31, q12.Q42, q13.Q3, q13.Q8, q13.Q16):
    _n += 1
    question_table(_n, _q.get("type", "MCQ"), _q["body"], _q.get("image"), _q.get("image_w", 4.5), _q["options"], _q["tail"], image_after=_q.get("image_after", 1))
    pb()
question_table(_n + 1, "MCQ", [q4.body_p1, q4.body_p2], None, 0, q4.options, q4.rows_after_options)
pb()
question_table(_n + 2, "MCQ", [q16.body_p1, q16.body_p2], os.path.join(BASE, "GATE_ECE_2016_S1_Q16", "q16_diagram.png"), 4.5,
               q16.options, q16.rows_after_options)
pb()
question_table(_n + 3, "NAT", [q25.body_p1, q25.body_p2], os.path.join(BASE, "GATE_ECE_2016_S2_Q25", "q25_diagram.png"), 4.8,
               [], q25.rows_after)

out = os.path.join(BASE, "GATE_ECE_missing_questions.docx")
doc.save(out)
print(out)
