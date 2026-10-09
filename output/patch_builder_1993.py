p = "build_combined_missing.py"
s = open(p, encoding="utf-8").read()
if "import q1993_data" not in s:
    s = s.replace("import q1994_data as q94", "import q1994_data as q94\nimport q1993_data as q93", 1)
    s = s.replace("for _q in (*q94.ALL,", "for _q in (*q93.ALL, *q94.ALL,", 1)
    open(p, "w", encoding="utf-8").write(s)
print("patched")
