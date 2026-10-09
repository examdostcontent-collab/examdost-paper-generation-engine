import csv, json, os, re, sys, difflib, importlib.util
from openpyxl import load_workbook

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OUT)
DL = r"C:/Users/rahul/Downloads"
FOLDER = r"E:/Office - Examdost/ExamDost/claude work files/PYQ Book/ECE missing questions"

import q2013_data as q13, q2012_data as q12, q2010_data as q10, q2007_data as q07, q2004_data as q04
import q2003_data as q03, q2002_data as q02, q2001_data as q01, q1999_data as q99, q1998_data as q98
import q1997_data as q97, q1996_data as q96, q1995_data as q95, q1994_data as q94, q1993_data as q93, q1991_data as q91


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


q4 = load(os.path.join(OUT, "GATE_ECE_2015_S1_Q4", "build_q4.py"), "q4")
q16 = load(os.path.join(OUT, "GATE_ECE_2016_S1_Q16", "build_q16.py"), "q16")
q25 = load(os.path.join(OUT, "GATE_ECE_2016_S2_Q25", "build_q25.py"), "q25")

labels = [("1991", "Q10"),
          ("1993", "Q1.4"), ("1993", "Q2.5"), ("1993", "Q2.7"), ("1993", "Q4.4"), ("1993", "Q4.5"),
          ("1994", "Q1.16"), ("1994", "Q2.12"), ("1995", "Q3.10 (coth question)"),
          ("1996", "Q1.4"), ("1996", "Q2.14"), ("1997", "Q5.4"), ("1997", "Q10"),
          ("1998", "Q1.23"), ("1998", "Q1.35"), ("1999", "Q9"),
          ("2001", "Q1.22"), ("2001", "Q1.23"), ("2001", "Q1.24"), ("2001", "Q1.25"),
          ("2001", "Q2.22"), ("2001", "Q2.23"), ("2001", "Q2.24"), ("2001", "Q2.25"),
          ("2001", "Q19"), ("2001", "Q20"), ("2001", "Q21"), ("2001", "Q22"),
          ("2002", "Q18"), ("2002", "Q20"), ("2003", "Q52"), ("2004", "Q86"),
          ("2007", "Q79"), ("2007", "Q80"), ("2007", "Q81"), ("2010", "Q22"),
          ("2012", "Q11"), ("2012", "Q18"), ("2012", "Q29"), ("2012", "Q31"), ("2012", "Q42"),
          ("2013", "Q3"), ("2013", "Q8"), ("2013", "Q16"),
          ("2015 Set 1", "Q4"), ("2016 Set 1", "Q16"), ("2016 Set 2", "Q25")]
mine = []
for q in (*q91.ALL, *q93.ALL, *q94.ALL, *q95.ALL, *q96.ALL, *q97.ALL, *q98.ALL, q99.Q9, *q01.ALL, q02.Q18, q02.Q20,
          q03.Q52, q04.Q86, q07.Q79, q07.Q80, q07.Q81, q10.Q22, q12.Q11, q12.Q18, q12.Q29, q12.Q31, q12.Q42,
          q13.Q3, q13.Q8, q13.Q16):
    mine.append((q["body"][0], q["tail"]))
mine.append((q4.body_p1, q4.rows_after_options))
mine.append((q16.body_p1, q16.rows_after_options))
mine.append((q25.body_p1, q25.rows_after))
assert len(mine) == len(labels) == 47


def plain(s):
    s = re.sub(r"\$[^$]*\$", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def pyq_paper(tail):
    for l, v in tail:
        if l == "PYQ":
            return v[0].replace("GATE ECE ", "").replace(" - ", "-")


admin = {x["id"]: x for x in json.load(open(os.path.join(DL, "gate_ec_admin_rows_3014.json"), encoding="utf-8"))}
mem = json.load(open(os.path.join(DL, "gate_paper_membership.json"), encoding="utf-8"))
old_ids = {r["id"] for r in csv.DictReader(open(os.path.join(DL, "gate_ec_classified.backup_before_3014.csv"), encoding="utf-8-sig"))}
new_ids = sorted(set(admin) - old_ids, key=int)

cands = [dict(label=labels[i], paper=pyq_paper(t), text=plain(b), used=False) for i, (b, t) in enumerate(mine)]
assign = {}
for i in new_ids:
    p = mem.get(i)
    pool = [c for c in cands if not c["used"] and c["paper"] == p]
    pv = plain(admin[i]["q"])
    best = max(pool, key=lambda c: difflib.SequenceMatcher(None, pv[:40], c["text"][:40]).ratio(), default=None)
    if best:
        best["used"] = True
        assign[best["label"]] = i
manual = {("1991", "Q10"): "69858", ("1993", "Q4.5"): "69863", ("2012", "Q18"): "69895"}
for k, v in manual.items():
    assign[k] = v
print("assigned", len(assign), "of 47; unassigned:", [c["label"] for c in cands if c["label"] not in assign])

wb = load_workbook(os.path.join(FOLDER, "GATE_ECE_book_change_log.xlsx"))
ws = wb["Changes"]
dup = {("1993", "Q2.7"): ("13930", "69861"), ("2015 Set 1", "Q4"): ("22454", "69902")}
for row in ws.iter_rows(min_row=2):
    action = row[1].value or ""
    if not action.startswith("ADD"):
        continue
    key = (row[0].value, row[3].value)
    if key in dup:
        keep, gone = dup[key]
        row[2].value = int(keep)
        row[1].value = "NO ACTION (already in portal)"
        row[6].value = f"Same question is already in the paper as ID {keep}; the duplicate copy {gone} was deleted from the portal."
    elif key in assign:
        row[2].value = int(assign[key])
        row[1].value = "ADD new question (added to portal)"
        row[6].value = "New portal ID shown. Full text and solution are in GATE_ECE_missing_questions.docx"
wb.save(os.path.join(FOLDER, "GATE_ECE_book_change_log.xlsx"))
print("change log updated")
