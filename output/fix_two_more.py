import csv, os

P = r"C:/Users/rahul/Downloads/gate_ec_classified.csv"
rows = list(csv.DictReader(open(P, encoding="utf-8-sig")))
for r in rows:
    if r["id"] == "69870":
        r["sub_topic"] = "Noise (Thermal, Shot, Flicker)"
    if r["id"] == "69858":
        r["topic"] = "Analog Communication"
with open(P, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=["id", "year", "set", "q_no", "pyq_id", "subject", "topic", "sub_topic"])
    w.writeheader()
    w.writerows(rows)

new = [r for r in rows if 69858 <= int(r["id"]) <= 69904]
import collections
print(len(rows), "rows;", len(new), "new rows")
print(collections.Counter(r["year"] for r in new))
for r in new[:6]:
    print(r)
