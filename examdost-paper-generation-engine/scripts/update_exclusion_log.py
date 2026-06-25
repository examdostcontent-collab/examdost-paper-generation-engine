"""
update_exclusion_log.py — append new-question fingerprints to the user's Lean
Exclusion Log and write a fresh, save-over-able file.

Usage:
    python update_exclusion_log.py <original_log | -> <paper.json> <output.csv|.txt>

- <original_log>  the user's existing log (.csv or .txt). Use "-" for a first run.
- <paper.json>    the generated paper; each question contributes a fingerprint, a
                  VALUE SIGNATURE (the exact numbers used), a TEMPLATE SIGNATURE
                  (number-free structure) and a DIAGRAM SIGNATURE (figure topology).
- <output>        .csv -> structured columns incl. value/template/diagram signatures
                  (recommended: lets future runs detect EXACT-VALUE repeats AND cap
                  template/diagram over-reuse across the series). .txt -> raw fingerprints.

De-dup policy matches the design rule: **a same-concept question with fresh numbers
is NOT a duplicate — only an EXACT-VALUE repeat is** (same subject + chapter/topic +
type + identical number multiset). Existing entries are preserved verbatim; only true
exact-value repeats are skipped. Fingerprint format:
    [Subject]_[Chapter/Topic]_[Type]_[Core Variables / Key Concept Used]
(see references/exclusion_log.md).

Dependencies: paperlib (sibling), stdlib.
"""
from __future__ import annotations

import csv
import json
import os
import sys

import paperlib as P

CSV_COLS = ["subject", "chapter_topic", "type", "core", "value_signature",
            "template_signature", "diagram_signature",
            "fingerprint", "exam", "added_on"]


def split_fingerprint(fp):
    parts = fp.split("_", 3)
    while len(parts) < 4:
        parts.append("")
    return {"subject": parts[0], "chapter_topic": parts[1], "type": parts[2], "core": parts[3]}


def load_existing(path):
    """Return (rows, fp_set, key_set). rows are dicts; key_set holds exact-value
    repeat keys (subject,chapter_topic,type,value_signature) where reconstructable."""
    rows, fps, keys = [], set(), set()
    if not path or path == "-" or not os.path.exists(path):
        return rows, fps, keys
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                fp = (r.get("fingerprint") or "").strip()
                if not fp:
                    continue
                if fp not in fps:
                    fps.add(fp)
                    rows.append(r)
                sig = (r.get("value_signature") or "").strip()
                if sig:
                    keys.add(((r.get("subject") or "").strip().lower(),
                              (r.get("chapter_topic") or "").strip().lower(),
                              (r.get("type") or "").strip().upper(), sig))
    else:
        with open(path, encoding="utf-8") as f:
            for line in f:
                fp = line.strip()
                if fp and not fp.startswith("#") and fp not in fps:
                    fps.add(fp)
                    rows.append({"fingerprint": fp})
    return rows, fps, keys


def iter_questions(paper):
    for sec in paper.get("sections", []):
        for q in sec.get("questions", []):
            yield q


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    orig, paper_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(paper_path, encoding="utf-8") as f:
        paper = json.load(f)
    meta = paper.get("meta") or {}
    exam, added_on = meta.get("exam", ""), meta.get("generated_on", "")

    rows, fps, keys = load_existing(orig)
    existing_count = len(rows)

    new_count = skipped = missing = 0
    for q in iter_questions(paper):
        fp = (q.get("fingerprint") or "").strip()
        if not fp:
            missing += 1
            continue
        sig = P.value_signature(q)
        key = P.repeat_key(q)            # None for pure-theory items
        if key and key in keys:
            skipped += 1                 # EXACT-VALUE repeat of a logged item
            continue
        if fp in fps and not sig:
            skipped += 1                 # identical pure-theory fingerprint
            continue
        fps.add(fp)
        if key:
            keys.add(key)
        rec = split_fingerprint(fp)
        rec.update({"value_signature": sig,
                    "template_signature": P.template_signature(q),
                    "diagram_signature": P.diagram_signature(q),
                    "fingerprint": fp, "exam": exam, "added_on": added_on})
        rows.append(rec)
        new_count += 1

    if out_path.lower().endswith(".txt"):
        with open(out_path, "w", encoding="utf-8") as f:
            for r in rows:
                f.write(r.get("fingerprint", "") + "\n")
    else:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                if "subject" not in r and r.get("fingerprint"):
                    r = {**split_fingerprint(r["fingerprint"]), **r}
                w.writerow(r)

    print(f"Wrote {out_path}")
    print(f"  Existing fingerprints     : {existing_count}")
    print(f"  New appended              : {new_count}")
    print(f"  Exact-value repeats skipped: {skipped}")
    if missing:
        print(f"  ! {missing} question(s) had no fingerprint — fix paper.json.")
    print(f"  Total now                 : {len(rows)}")


if __name__ == "__main__":
    main()
