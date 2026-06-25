"""
coverage_report.py — the cross-mock DIVERSITY engine.

Reads the cumulative exclusion log (every question from all prior mocks of this exam)
plus the canonical master taxonomy, and prints GENERATION GUIDANCE so the next mock
rotates across the syllabus and varies archetypes instead of churning out the same
questions. Run it in Phase 2 (after the distribution is set) and follow its guidance
in Phase 3.

Usage:
    python coverage_report.py <exclusion_log.csv | -> [--taxonomy <master.xlsx>]
                              [--subjects "Power Systems:32,Electrical Machines:24,..."]

What it surfaces, per subject:
  - UNUSED in-syllabus types (never tested across prior mocks) -> draw here FIRST (breadth).
  - Least-used touched topics -> next preference.
  - OVER-USED archetypes (asked >=2x) -> avoid, or vary the angle/given-unknown/difficulty sharply.
  - A diversity target: keep the new mock's (chapter,type)-cell overlap with prior mocks low.

Dependencies: load_taxonomy (sibling), stdlib.
"""
from __future__ import annotations

import csv
import os
import re
import sys
from collections import Counter, defaultdict


def _norm(s):
    return re.sub(r"\s+", " ", str(s or "").strip()).lower()


def _strip_numbers(s):
    return re.sub(r"\s+", " ", re.sub(r"[-+]?\d*\.?\d+", "#", str(s or ""))).strip()


def _split_chap_topic(ct):
    ct = str(ct or "")
    if ">" in ct:
        a, b = ct.split(">", 1)
        return a.strip(), b.strip()
    return ct.strip(), ""


def load_log(path):
    """Return list of dicts: subject, chapter, topic, type, core, archetype."""
    rows = []
    if not path or path == "-" or not os.path.exists(path):
        return rows
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            subj = r.get("subject", "")
            chap, top = _split_chap_topic(r.get("chapter_topic", ""))
            core = r.get("core", "")
            if not core and r.get("fingerprint"):
                parts = r["fingerprint"].split("_", 3)
                core = parts[3] if len(parts) > 3 else ""
            rows.append({"subject": subj, "chapter": chap, "topic": top,
                         "type": r.get("type", ""), "core": core,
                         "archetype": _strip_numbers(core),
                         "template_signature": (r.get("template_signature") or "").strip(),
                         "diagram_signature": (r.get("diagram_signature") or "").strip()})
    return rows


# Caps mirror validate_paper.py — keep these in sync with it.
TEXT_TEMPLATE_CAP = 2
FIGURE_TOPOLOGY_CAP = 1


def taxonomy_cells(tax_path):
    """{subject_lower: {(chapter_lower, topic_lower): (chapter_name, topic_name)}}"""
    out = defaultdict(dict)
    if not tax_path or not os.path.exists(tax_path):
        return out
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import load_taxonomy as lt
    tax = lt.parse(tax_path)
    for subj, sd in (tax.get("subjects") or {}).items():
        for c in sd.get("chapters", []):
            cn = c.get("name", "")
            note = (c.get("note") or "").lower()
            for tp in c.get("topics") or []:
                tn = tp.get("name", "")
                if "not in syll" in (note + " " + (tp.get("note") or "").lower()):
                    continue
                out[_norm(subj)][(_norm(cn), _norm(tn))] = (cn, tn)
    return out


def parse_subjects(arg):
    out = {}
    for part in (arg or "").split(","):
        part = part.strip()
        if ":" in part:
            name, n = part.rsplit(":", 1)
            try:
                out[name.strip()] = int(n)
            except ValueError:
                pass
    return out


def main():
    args = sys.argv[1:]
    tax = None
    subjects_arg = None
    if "--taxonomy" in args:
        i = args.index("--taxonomy"); tax = args[i + 1]; del args[i:i + 2]
    if "--subjects" in args:
        i = args.index("--subjects"); subjects_arg = args[i + 1]; del args[i:i + 2]
    if not args:
        print(__doc__); sys.exit(1)
    log_path = args[0]
    if tax is None:
        tax = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "chapter_topic_master.xlsx")

    rows = load_log(log_path)
    cells = taxonomy_cells(tax)
    targets = parse_subjects(subjects_arg)

    # tally prior usage
    used_topic = Counter()                     # (subj, chap, topic) -> count
    arch_count = Counter()                      # (subj, chap, topic, type, archetype) -> count
    by_subject = defaultdict(int)
    for r in rows:
        k = (_norm(r["subject"]), _norm(r["chapter"]), _norm(r["topic"]))
        used_topic[k] += 1
        arch_count[(k[0], k[1], k[2], _norm(r["type"]), r["archetype"])] += 1
        by_subject[_norm(r["subject"])] += 1

    print("=" * 70)
    print(f"CROSS-MOCK COVERAGE GUIDANCE   (prior questions logged: {len(rows)})")
    print("=" * 70)
    if not rows:
        print("No prior mocks logged for this exam — this is the FIRST mock. Generate "
              "for breadth: spread each subject's quota across many different chapters/types, "
              "and carry the exclusion log forward so the NEXT mock can rotate off it.")
        return

    # --- TEMPLATE / DIAGRAM cap status: which structures are EXHAUSTED for this series ---
    tmpl_ct = Counter(r["template_signature"] for r in rows if r.get("template_signature"))
    dia_ct = Counter(r["diagram_signature"] for r in rows if r.get("diagram_signature"))
    # map a signature back to a human label (subject>topic + a sample core) for the printout
    tmpl_label, dia_label = {}, {}
    for r in rows:
        ts = r.get("template_signature")
        if ts and ts not in tmpl_label:
            tmpl_label[ts] = f"{r['subject']} > {r['topic'] or r['chapter']}: {r['core'][:60]}"
        ds = r.get("diagram_signature")
        if ds and ds not in dia_label:
            dia_label[ds] = f"{r['subject']} > {r['topic'] or r['chapter']}: {r['core'][:60]}"
    tmpl_full = [(c, tmpl_label[s]) for s, c in tmpl_ct.items() if c >= TEXT_TEMPLATE_CAP]
    dia_full = [(c, dia_label[s]) for s, c in dia_ct.items() if c >= FIGURE_TOPOLOGY_CAP]
    if tmpl_full or dia_full:
        print("\n" + "!" * 70)
        print("STRUCTURES AT THE SERIES CAP — the validator will REJECT another of these.")
        print("Do NOT re-skin them with new numbers; use a different configuration/diagram.")
        if dia_full:
            print(f"  DIAGRAM topologies at cap (max {FIGURE_TOPOLOGY_CAP} per series):")
            for c, lab in sorted(dia_full, reverse=True)[:20]:
                print(f"      - ({c}x) {lab}")
        if tmpl_full:
            print(f"  TEXT templates at cap (max {TEXT_TEMPLATE_CAP} per series):")
            for c, lab in sorted(tmpl_full, reverse=True)[:20]:
                print(f"      - ({c}x) {lab}")
        print("!" * 70)

    subj_list = list(targets) if targets else sorted({r["subject"] for r in rows if r["subject"]})
    for subj in subj_list:
        sl = _norm(subj)
        canon = cells.get(sl, {})
        used_here = {(c, t) for (s, c, t) in used_topic if s == sl}
        unused = [name for (c, t), name in canon.items() if (c, t) not in used_here]
        least = sorted(((used_topic[(sl, c, t)], canon.get((c, t), (c, t)))
                        for (c, t) in used_here if (c, t) in canon), key=lambda x: x[0])[:8]
        overused = sorted(((n, a) for a, n in arch_count.items() if a[0] == sl and n >= 2),
                          reverse=True)[:8]
        need = targets.get(subj)
        hdr = f"### {subj}" + (f"  (need {need} this mock)" if need else "")
        print("\n" + hdr)
        print(f"    prior questions in this subject: {by_subject.get(sl,0)} "
              f"| in-syllabus types: {len(canon)} | already touched: {len(used_here)} "
              f"| UNUSED: {len(unused)}")
        if unused:
            print("    DRAW FIRST — unused in-syllabus types:")
            for cn, tn in unused[:14]:
                print(f"        - {cn} > {tn}")
        if least:
            print("    THEN — least-used touched topics:")
            for cnt, (cn, tn) in least:
                print(f"        - {cn} > {tn}   (used {cnt}x)")
        if overused:
            print("    AVOID / VARY SHARPLY — over-used archetypes:")
            for cnt, a in overused:
                print(f"        - [{a[3]}] {a[1]} > {a[2]}: '{a[4]}'  (asked {cnt}x)")

    print("\n" + "-" * 70)
    print("RULE for this mock: keep the SAME subject weightage, but rotate WITHIN it —")
    print("  1) fill each subject FIRST from its UNUSED types, then least-used topics;")
    print("  2) for any archetype that must reappear, change the given<->unknown, the")
    print("     sub-case, the framing (direct/reverse/match/assertion-reason) AND the")
    print("     difficulty vs last time;")
    print("  3) aim for < 30% (chapter,type)-cell overlap with the most recent mock.")


if __name__ == "__main__":
    main()
