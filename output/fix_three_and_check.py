import csv, json, re, os, sys

DL = r"C:/Users/rahul/Downloads"
P = os.path.join(DL, "gate_ec_classified.csv")
rows = list(csv.DictReader(open(P, encoding="utf-8-sig")))
fix = {
    "69858": "Frequency Modulation and Demodulation",
    "69863": "Construction and Rotating Magnetic Field",
    "69895": "Z-Transform Calculation",
}
for r in rows:
    if r["id"] in fix and not r["sub_topic"]:
        r["sub_topic"] = fix[r["id"]]
with open(P, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["id", "year", "set", "q_no", "pyq_id", "subject", "topic", "sub_topic"])
    w.writeheader()
    w.writerows(rows)

tab = json.load(open(r"C:/Users/rahul/AppData/Local/Temp/sheet/tab2.json", encoding="utf-8"))
new = [r for r in rows if 69858 <= int(r["id"]) <= 69904]
print(len(new), "new rows; blank sub_topic:", [r["id"] for r in new if not r["sub_topic"]])
bad = []
for r in new:
    s = r["subject"]
    s = "Communication Systems" if s == "Communication System" else s
    ch = next((c for c in tab.get(s, {}) if c.lower() == r["topic"].lower()), None)
    ok = ch and r["sub_topic"] in tab[s][ch]
    if not ok:
        bad.append((r["id"], r["subject"], r["topic"], r["sub_topic"]))
print("rows where sub_topic is not in the portal chapter:", bad)
