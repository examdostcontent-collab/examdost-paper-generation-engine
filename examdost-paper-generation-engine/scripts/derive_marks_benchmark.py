"""
derive_marks_benchmark.py — mine a Previous-Year-Questions (PYQ) document to learn
an exam's 1-mark vs 2-mark pattern for a subject, so new questions can be weighted
the way the real exam weights them.

Built for the ExamDost PYQ documents, where every question carries an inline tag
like `[2019: 1 Mark]` or `[2012: 2 Marks]` and chapters are headed
`Chapter N - <Name>`. Older GATE papers also have `5 Marks` items (pre-2003
format) — those are reported separately and ignored for the modern 1-vs-2 split.

Usage:
    python derive_marks_benchmark.py <pyq.pdf|.docx|.txt> [-o <out dir>]

It writes two files into the output dir (default: alongside the input):
    <stem>.marks_stats.txt    — counts by mark, by chapter, by 5-year window,
                                plus a sample of 1-mark and 2-mark question stems
                                per chapter (so a human/model can read the texture
                                and author the benchmark prose).
    <stem>.marks_records.json — every parsed record {chap, chap_name, year,
                                marks, stem} for further analysis.

The script does the *measuring*. Turning the numbers + sampled stems into the
short benchmark write-up (the 1-mark vs 2-mark signal lists + chapter priors +
difficulty calibration) is a judgement step — see SKILL.md / the existing
references/marks_benchmarks/*.md for the shape to follow.

Dependencies: extract_text (sibling) for .pdf/.docx; none for .txt.
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict

MARK_RE = re.compile(r"\[(\d{4})\s*[:\-]?\s*(\d+)\s*Marks?\]", re.I)
CHAP_RE = re.compile(r"^\s*Chapter\s+(\d+)\s*[–\-]\s*(.+?)\s*$")
NOISE = ("http", "QR code", "examdost", "Error in this")


def load_text(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return open(path, encoding="utf-8", errors="replace").read()
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, here)
    import extract_text as ex
    return ex.extract(path)


def parse(text):
    records = []
    cur_chap = None
    in_solutions = False
    buf = []
    for ln in text.splitlines():
        s = ln.strip()
        cm = CHAP_RE.match(ln)
        if cm:
            name = cm.group(2)
            in_solutions = bool(re.search(r"solution", name, re.I))
            if not in_solutions:
                cur_chap = (cm.group(1), name.strip())
            buf = []
            continue
        if re.match(r"^solutions\b", s, re.I):
            in_solutions = True
            buf = []
            continue
        mk = MARK_RE.search(ln)
        if mk and not in_solutions and cur_chap:
            records.append({
                "chap": cur_chap[0], "chap_name": cur_chap[1],
                "year": int(mk.group(1)), "marks": int(mk.group(2)),
                "stem": " ".join(buf)[-400:],
            })
            buf = []
            continue
        if s and not any(n in s for n in NOISE) and s.lower() != "network analysis":
            buf.append(s)
            buf = buf[-12:]
    return records


def report(records):
    out = []
    out.append(f"TOTAL questions with a marks tag: {len(records)}")
    by_marks = Counter(r["marks"] for r in records)
    out.append(f"By marks: {dict(sorted(by_marks.items()))}")
    n12 = sum(by_marks.get(m, 0) for m in (1, 2))
    if n12:
        out.append(f"1-vs-2 share: 1-mark {by_marks.get(1,0)/n12:.0%}  "
                   f"2-mark {by_marks.get(2,0)/n12:.0%}  (of {n12} modern items)")
    out.append("")
    out.append("By chapter (1-mark / 2-mark / share):")
    ch = defaultdict(Counter)
    for r in records:
        ch[(int(r["chap"]), r["chap_name"])][r["marks"]] += 1
    for key in sorted(ch):
        c = ch[key]
        n = c[1] + c[2]
        share = f"{c[1]/n:.0%}/{c[2]/n:.0%}" if n else "-"
        out.append(f"  {key[0]:>2}. {key[1][:38]:38s}  1mk={c[1]:3d}  2mk={c[2]:3d}  "
                   f"5mk={c[5]:2d}  (1:2 = {share})")
    out.append("")
    out.append("By 5-year window:")
    dec = defaultdict(Counter)
    for r in records:
        dec[(r["year"] // 5) * 5][r["marks"]] += 1
    for k in sorted(dec):
        out.append(f"  {k}-{k+4}: 1mk={dec[k][1]:3d}  2mk={dec[k][2]:3d}  5mk={dec[k][5]:2d}")
    out.append("")
    # sampled stems, newest first, per mark
    for marks in (1, 2):
        rs = sorted([r for r in records if r["marks"] == marks],
                    key=lambda r: -r["year"])
        out.append(f"===== sample {marks}-MARK stems (newest first, up to 30) =====")
        for r in rs[:30]:
            stem = r["stem"][-160:].replace("\n", " ")
            out.append(f"  [{r['year']}|C{r['chap']}] {stem}")
        out.append("")
    return "\n".join(out)


def main():
    args = list(sys.argv[1:])
    out_dir = None
    if "-o" in args:
        i = args.index("-o")
        out_dir = args[i + 1]
        del args[i:i + 2]
    if len(args) != 1:
        print(__doc__)
        sys.exit(1)
    path = args[0]
    stem = os.path.splitext(os.path.basename(path))[0]
    out_dir = out_dir or os.path.dirname(os.path.abspath(path))
    os.makedirs(out_dir, exist_ok=True)

    text = load_text(path)
    records = parse(text)
    if not records:
        print("  ! no [YEAR: N Mark] tags found — is this an ExamDost-format PYQ "
              "doc? (chapters headed 'Chapter N - Name', marks tagged per question)")
        sys.exit(2)

    stats = report(records)
    stats_path = os.path.join(out_dir, f"{stem}.marks_stats.txt")
    json_path = os.path.join(out_dir, f"{stem}.marks_records.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        f.write(stats)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
    print(f"Parsed {len(records)} PYQ items.")
    print(f"  stats   -> {stats_path}")
    print(f"  records -> {json_path}")
    print("Read the stats file (esp. the sampled stems) and distill the benchmark "
          "into references/marks_benchmarks/<subject>_<exam>.md")


if __name__ == "__main__":
    main()
