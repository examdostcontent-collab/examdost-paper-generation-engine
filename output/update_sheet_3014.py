import csv, json, os, re, sys, shutil, difflib, importlib.util

OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, OUT)
DL = r"C:/Users/rahul/Downloads"

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

mine = []
for q in (*q91.ALL, *q93.ALL, *q94.ALL, *q95.ALL, *q96.ALL, *q97.ALL, *q98.ALL, q99.Q9, *q01.ALL, q02.Q18, q02.Q20,
          q03.Q52, q04.Q86, q07.Q79, q07.Q80, q07.Q81, q10.Q22, q12.Q11, q12.Q18, q12.Q29, q12.Q31, q12.Q42,
          q13.Q3, q13.Q8, q13.Q16):
    mine.append((q["body"][0], q["tail"]))
mine.append((q4.body_p1, q4.rows_after_options))
mine.append((q16.body_p1, q16.rows_after_options))
mine.append((q25.body_p1, q25.rows_after))


def plain(s):
    s = re.sub(r"\$[^$]*\$", " ", s)
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def row_of(tail, label):
    for l, v in tail:
        if l == label:
            return v[0]


cands = []
for body, tail in mine:
    pyq = row_of(tail, "PYQ")
    paper = pyq.replace("GATE ECE ", "").replace(" - ", "-")
    topic = row_of(tail, "Topic")
    m = re.match(r"^(.*) \((.*)\)$", topic)
    sub = m.group(2) if m else ""
    cands.append(dict(paper=paper, text=plain(body), sub=sub, subject=row_of(tail, "Subject"), topic=topic, used=False))

rows = list(csv.DictReader(open(os.path.join(DL, "gate_ec_classified.csv"), encoding="utf-8-sig")))
admin = {x["id"]: x for x in json.load(open(os.path.join(DL, "gate_ec_admin_rows_3014.json"), encoding="utf-8"))}
mem = json.load(open(os.path.join(DL, "gate_paper_membership.json"), encoding="utf-8"))

shutil.copy(os.path.join(DL, "gate_ec_classified.csv"), os.path.join(DL, "gate_ec_classified.backup_before_3014.csv"))

by_id = {r["id"]: r for r in rows}
moved = []
for r in rows:
    p = mem.get(r["id"])
    if not p:
        continue
    yr = p[:4]
    st = p.split("-")[1] if "-" in p else "1"
    if yr != r["year"]:
        moved.append((r["id"], r["year"], yr))
        r["year"] = yr
        r["set"] = st
        r["q_no"] = ""
        r["pyq_id"] = ""

new_ids = sorted(set(admin) - set(by_id), key=int)
report = []
for i in new_ids:
    a = admin[i]
    p = mem.get(i)
    pool = [c for c in cands if not c["used"] and (p is None or c["paper"] == p)]
    pv = plain(a["q"])
    best, bs = None, 0
    for c in pool:
        s = difflib.SequenceMatcher(None, pv[:40], c["text"][:40]).ratio()
        if s > bs:
            best, bs = c, s
    sub = ""
    if best and bs >= 0.55:
        best["used"] = True
        sub = best["sub"]
    else:
        report.append((i, p, round(bs, 2)))
    yr = p[:4] if p else ""
    st = p.split("-")[1] if (p and "-" in p) else "1"
    rows.append(dict(id=i, year=yr, set=st, q_no="", pyq_id="", subject=a["subject"], topic=a["topic"], sub_topic=sub))

rows.sort(key=lambda r: int(r["id"]), reverse=True)
with open(os.path.join(DL, "gate_ec_classified.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["id", "year", "set", "q_no", "pyq_id", "subject", "topic", "sub_topic"])
    w.writeheader()
    w.writerows(rows)

print("rows", len(rows), "new", len(new_ids), "moved", moved)
print("unmatched new rows (no sub_topic):", report)
print("unused candidate questions:", [(c["paper"], c["text"][:40]) for c in cands if not c["used"]])
print("new rows missing year:", [r["id"] for r in rows if r["id"] in new_ids and not r["year"]])
