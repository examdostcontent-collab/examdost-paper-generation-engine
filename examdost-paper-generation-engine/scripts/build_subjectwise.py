"""build_subjectwise.py — SUBJECT-WISE output packaging (output option 2).

Instead of one set of files per TEST, this regroups every question across a set of
tests BY CANONICAL SUBJECT and emits ONE set of the 4 deliverables per subject
(all of a subject's questions, across all tests, in one file), plus ONE test-mapping
Excel (a sheet per subject: combined Q-no -> source test + original Q-no) so the
content team knows which test each uploaded question belongs to.

Usage:
    python build_subjectwise.py <config.json>

config.json:
{
  "exam": "CIL MT Electrical",
  "out_dir": ".../Generated Papers/CIL MT Electrical/_Subjectwise",
  "workspace": ".../_workspace/_subjectwise",
  "marking": {"correct": 1, "incorrect": 0},
  "tests": [
    {"json": ".../tests/em_t01.json", "display": "Electrical Machines - Test 01"},
    ...
  ],
  "merge": {"Analog Electronics": "Electronics", ...}   # OPTIONAL subject-merge map
}
Builds <out_dir>/<Subject>/<Exam> - <Subject> (All Tests).{docx,pdf,boxed.docx,metadata.xlsx}
and <out_dir>/<Exam> - Test Mapping.xlsx (one sheet per subject).
"""
import json, os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def _run(script, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([PY, os.path.join(HERE, script), *args],
                       capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def safe(name):
    for ch in '\\/:*?"<>|':
        name = name.replace(ch, "-")
    return name.strip()


def main(cfg_path):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    exam = cfg["exam"]
    out_dir = cfg["out_dir"]
    ws = cfg.get("workspace", os.path.join(out_dir, "_ws"))
    merge = cfg.get("merge", {})
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(ws, exist_ok=True)

    # 1) gather questions by subject, with provenance
    groups = {}     # subject -> [(question, source_display, orig_no)]
    for t in cfg["tests"]:
        paper = json.load(open(t["json"], encoding="utf-8"))
        disp = t["display"]
        for sec in paper["sections"]:
            for q in sec["questions"]:
                subj = q.get("subject", "Unknown")
                subj = merge.get(subj, subj)
                groups.setdefault(subj, []).append((q, disp, q.get("number")))

    # taxonomy lookup (chapter number / type number) — same source as the Metadata sheet
    sys.path.insert(0, HERE)
    import load_taxonomy as lt
    import build_metadata_xlsx as MD
    tax_path = cfg.get("taxonomy") or os.path.join(HERE, "..", "assets", "chapter_topic_master.xlsx")
    chap_lk, typ_lk = ({}, {})
    if os.path.exists(tax_path):
        chap_lk, typ_lk = MD.build_lookup(lt.parse(tax_path))
    else:
        print(f"  ! taxonomy not found at {tax_path} — chapter/type numbers left blank")

    # 2) per subject: build combined paper.json + 4 deliverables
    import openpyxl
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    unmapped = 0
    summary = []
    for subj in sorted(groups):
        items = groups[subj]
        qs = []
        mapping = []
        from collections import Counter
        fmt = Counter()
        for i, (q, disp, orig) in enumerate(items, 1):
            qq = dict(q)
            qq["number"] = i
            qs.append(qq)
            fmt[qq.get("type", "MCQ")] += 1
            sl, cl = MD._norm(qq.get("subject")), MD._norm(qq.get("chapter"))
            cno = chap_lk.get((sl, cl))
            tno = typ_lk.get((sl, cl, MD._norm(qq.get("topic"))))
            if cno is None or tno is None:
                unmapped += 1

            def _num(x):  # store digit codes as real numbers, not text
                s = str(x).strip()
                return int(s) if s.lstrip("-").isdigit() else (x if x is not None else "")
            mapping.append((i, disp, orig, qq.get("subject", ""),
                            _num(cno), _num(tno),
                            MD.difficulty(qq), qq.get("marks", 1), MD.excel_type(qq)))
        meta = {
            "exam": exam,
            "paper_title": f"{exam} — {subj} (All Tests Combined)",
            "total_questions": len(qs), "total_marks": len(qs), "duration_min": 0,
            "generated_on": cfg.get("generated_on", ""),
            "instructions": [f"All {subj} questions compiled across all tests. Each carries 1 mark.",
                             "Marking: +1 correct, no negative."],
            "layout": "combined", "show_solutions": True,
            "marking": cfg.get("marking", {"correct": 1, "incorrect": 0}),
            "target_distribution": {"marks": {"1": len(qs)}, "formats": dict(fmt)},
        }
        paper = {"meta": meta, "sections": [{"section": subj, "questions": qs}]}
        pj = os.path.join(ws, safe(subj) + ".json")
        json.dump(paper, open(pj, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

        sub_out = os.path.join(out_dir, safe(subj))
        os.makedirs(sub_out, exist_ok=True)
        base = os.path.join(sub_out, f"{safe(exam)} - {safe(subj)} (All Tests)")
        _run("build_paper_docx.py", pj, base + ".docx")
        _run("build_paper_pdf.py", pj, base + ".pdf")
        _run("build_paper_boxed_docx.py", pj, base + " Boxed.docx", "--latex")
        _run("build_metadata_xlsx.py", pj, base + " Metadata.xlsx")

        # mapping sheet for this subject
        wsname = safe(subj)[:31]
        sh = wb.create_sheet(wsname)
        sh.append(["Combined Q No", "Source Test", "Original Q No", "Subject Name",
                   "Chapter number", "type number", "difficulty index", "Marks",
                   "TheoryMCQ/Numerical MCQ/NAT/MSQ/StatementType/Assertion-Reason"])
        for row in mapping:
            sh.append(list(row))
        summary.append((subj, len(qs)))
        print(f"  {subj}: {len(qs)} questions -> {sub_out}")

    map_path = os.path.join(out_dir, f"{safe(exam)} - Test Mapping.xlsx")
    wb.save(map_path)
    print(f"\nSUBJECT-WISE DONE: {len(summary)} subjects, mapping -> {map_path}")
    if unmapped:
        print(f"  ! {unmapped} mapping row(s) had no taxonomy match (chapter/type number blank)")
    for s, n in summary:
        print(f"   {s:32s} {n}")


if __name__ == "__main__":
    main(sys.argv[1])
