p = "build_combined_missing.py"
s = open(p, encoding="utf-8").read()

if "import q1991_data" not in s:
    s = s.replace("import q1993_data as q93", "import q1993_data as q93\nimport q1991_data as q91", 1)
    s = s.replace("for _q in (*q93.ALL,", "for _q in (*q91.ALL, *q93.ALL,", 1)

s = s.replace("def question_table(qno, qtype, body, image, image_w, options, rest):",
              "def question_table(qno, qtype, body, image, image_w, options, rest, image_after=1):", 1)

old = '''        elif label == "Body":
            fill(vc, [paras[0]])
            vc.add_paragraph().add_run().add_picture(image, width=Inches(image_w))
            r = vc.add_paragraph().add_run(paras[1])
            r.font.size = Pt(10.5); r.font.name = "Calibri"
'''
new = '''        elif label == "Body":
            fill(vc, paras[:image_after])
            vc.add_paragraph().add_run().add_picture(image, width=Inches(image_w))
            for _t in paras[image_after:]:
                r = vc.add_paragraph().add_run(_t)
                r.font.size = Pt(10.5); r.font.name = "Calibri"
'''
assert old in s
s = s.replace(old, new, 1)

s = s.replace('_q.get("image_w", 4.5), _q["options"], _q["tail"])',
              '_q.get("image_w", 4.5), _q["options"], _q["tail"], image_after=_q.get("image_after", 1))', 1)
open(p, "w", encoding="utf-8").write(s)
print("patched")
