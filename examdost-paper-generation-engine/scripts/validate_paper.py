"""
validate_paper.py — the HARD GATE that runs before any paper file is built.

Usage:
    python validate_paper.py <paper.json> [exclusion_log.csv|.txt] [--taxonomy <master.xlsx>] [--no-tax]

Deterministically checks structural & answer integrity so a broken paper can
NEVER ship. Prints a report and exits NON-ZERO if any ERROR is found (so the
skill must fix/regenerate before Phase 4 building). WARNINGS don't block but
must be reviewed.

What it enforces
  COUNTS      total questions == meta.total_questions; per-section/mark/format vs
              meta.target_distribution (if provided); wildcard share ~10% (if expected).
  STRUCTURE   every question has number/type/marks; MCQ has >=2 options; MCQ/MSQ
              answer letters all exist among the options; NAT has a numeric answer.
  ANSWER      answer reconciles with solution.final_answer; all 4 solution steps
              present (when show_solutions); NAT solution.check expression (if given)
              is EXECUTED and must land in the answer band — real code-checked math.
  REPEAT      exact-VALUE duplicates (same subject+chapter+type+identical numbers)
              inside the paper AND against the exclusion log. (Same concept with
              fresh numbers is allowed by design — only exact value repeats fail.)
  TEMPLATE    cumulative-series STRUCTURE caps (the backstop for "same question, only
              the numbers differ"): a text template may recur at most TEXT_TEMPLATE_CAP
              times and a diagram/circuit TOPOLOGY at most FIGURE_TOPOLOGY_CAP times
              across the whole series (log + this paper). Over the cap is an ERROR.
  CONSTRAINTS meta.structural_constraints (optional) e.g. forbid NAT/MSQ in a section.
  TAXONOMY    Subject/Chapter/Topic snap to the canonical master sheet (auto-loaded from
              assets/chapter_topic_master.xlsx, or --taxonomy <path>; --no-tax to skip):
              non-canonical SUBJECT is an ERROR; chapter/topic drift is a WARNING.
  METADATA    subject/chapter present; fingerprint present.

Dependencies: paperlib (sibling), stdlib only.
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys

import paperlib as P


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def err(self, qno, msg):
        self.errors.append((qno, msg))

    def warn(self, qno, msg):
        self.warnings.append((qno, msg))


def iter_q(paper):
    for sec in paper.get("sections", []):
        sname = sec.get("section", "")
        for q in sec.get("questions", []):
            yield sname, q


def load_log_keys(path):
    """Return a set of repeat-keys from an existing exclusion log (csv with a
    'value_signature' or 'fingerprint' column, or a txt of fingerprints).
    We reconstruct (subject,chapter,type,sig) where possible."""
    keys = set()
    sigs = set()
    if not path or path == "-" or not os.path.exists(path):
        return keys, sigs
    if path.lower().endswith(".csv"):
        with open(path, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                sig = (r.get("value_signature") or "").strip()
                if sig:
                    sigs.add(sig)
                    subj = (r.get("subject") or "").strip().lower()
                    chap = (r.get("chapter_topic") or "").strip().lower()
                    typ = (r.get("type") or "").strip().upper()
                    keys.add((subj, chap, typ, sig))
    return keys, sigs


def check_structure(sname, q, rep):
    qno = q.get("number", "?")
    typ = (q.get("type") or "").strip().upper()
    if q.get("number") in (None, ""):
        rep.err(qno, "missing question number")
    if not typ:
        rep.err(qno, "missing type")
    if q.get("marks") in (None, ""):
        rep.err(qno, "missing marks")
    if not str(q.get("text", "")).strip():
        rep.err(qno, "empty question text")
    if not q.get("subject"):
        rep.warn(qno, "missing subject (metadata/fingerprint will be weak)")
    if not q.get("fingerprint"):
        rep.err(qno, "missing fingerprint")
    diff = q.get("difficulty")
    if diff in (None, ""):
        rep.warn(qno, "no difficulty set (1=Easy/2=Moderate/3=Difficult) — needed for the metadata Excel")
    elif str(diff) not in ("1", "2", "3"):
        rep.err(qno, f"difficulty must be 1, 2 or 3 (got {diff!r})")

    opts = q.get("options") or []
    ans = q.get("answer", "")
    if typ in ("MCQ", "ASSERTION-REASON", "STATEMENT"):
        if len(opts) < 2:
            rep.err(qno, f"{typ} has < 2 options")
        letters = set(P.option_letters(opts))
        claimed = P.answer_letters(ans)
        if not claimed:
            rep.err(qno, "MCQ-type answer has no option letter")
        for c in claimed:
            if letters and c not in letters:
                rep.err(qno, f"answer letter '{c}' is not among the options {sorted(letters)}")
        if typ == "MCQ" and len(claimed) > 1:
            rep.warn(qno, "MCQ has multiple answer letters — should this be MSQ?")
    elif typ == "MSQ":
        if len(opts) < 2:
            rep.err(qno, "MSQ has < 2 options")
        letters = set(P.option_letters(opts))
        claimed = P.answer_letters(ans)
        if not claimed:
            rep.err(qno, "MSQ answer has no option letters")
        for c in claimed:
            if letters and c not in letters:
                rep.err(qno, f"answer letter '{c}' is not among the options {sorted(letters)}")
    elif typ == "NAT":
        if opts:
            rep.warn(qno, "NAT should not have options")
        if P.parse_range(ans) is None:
            rep.err(qno, f"NAT answer is not numeric: {ans!r}")


def check_answer_solution(q, rep, show_solutions):
    qno = q.get("number", "?")
    typ = (q.get("type") or "").strip().upper()
    sol = q.get("solution") or {}
    if not show_solutions:
        return
    if not sol:
        rep.err(qno, "show_solutions is on but solution is missing")
        return
    rich = bool(sol.get("concept") or sol.get("where") or sol.get("option_analysis"))
    if rich:
        # Rich ExamDost format: Core Concept & Formula -> Calculation/Options -> Final Answer
        if not (sol.get("concept") or sol.get("formula")):
            rep.warn(qno, "rich solution has no concept text or formula in 'Core Concept & Formula'")
        if not (sol.get("calculation") or sol.get("option_analysis")):
            rep.err(qno, "rich solution needs either 'calculation' (numeric) or 'option_analysis' (conceptual)")
        if not sol.get("final_answer"):
            rep.err(qno, "rich solution missing 'final_answer'")
        # option_analysis sanity: exactly one verdict matches the answer key
        oa = sol.get("option_analysis") or []
        if oa:
            claimed = set(P.answer_letters(q.get("answer", "")))
            correct = {str(o.get("option", "")).upper() for o in oa if o.get("correct")}
            if claimed and correct and claimed != correct:
                rep.err(qno, f"option_analysis marks {sorted(correct)} correct but answer key is {sorted(claimed)}")
    else:
        for step in ("given", "formula", "calculation", "final_answer"):
            if sol.get(step) in (None, "", []):
                rep.err(qno, f"solution missing Step '{step}'")

    # answer <-> final_answer reconciliation
    fa = sol.get("final_answer", "")
    if typ == "NAT":
        band = P.parse_range(q.get("answer", ""))
        fan = P.first_number(fa)
        if band and fan is not None and not (band[0] - 1e-9 <= fan <= band[1] + 1e-9):
            rep.err(qno, f"final_answer ({fan}) is outside the keyed NAT band {band}")
        # EXECUTE the check expression — genuine code-verified arithmetic
        chk = sol.get("check")
        if chk:
            exprs = chk if isinstance(chk, list) else [chk]
            try:
                val = P.safe_eval_number(exprs[-1])
            except Exception as e:
                rep.warn(qno, f"solution.check did not evaluate ({e}) — verify by hand")
            else:
                if band and not (band[0] - 1e-6 <= round(val, 6) <= band[1] + 1e-6):
                    rep.err(qno, f"solution.check computes {val:g}, OUTSIDE keyed band {band} — answer key is wrong")
        else:
            rep.warn(qno, "NAT has no solution.check expression — arithmetic is not code-verified")
    # For MCQ/MSQ the structural check already confirms the keyed letter(s) are valid
    # options; final_answer is usually the value, so we don't letter-match it here.


_CONCEPT_MATH = re.compile(r"[\\^_]|=\s*\S*\d|\\frac|\\sqrt")


def check_concept(q, rep):
    """Concept must be plain English — flag formulas/symbols/subscripts (they belong
    in Step 2 — Governing Formula)."""
    c = q.get("concept") or ""
    if _CONCEPT_MATH.search(str(c)):
        rep.warn(q.get("number", "?"),
                 "concept contains a formula/symbol — keep concept plain-English, move math to Step 2")


def check_diagram(q, rep):
    qno = q.get("number", "?")
    txt = str(q.get("text", "")).lower()
    has_tag = bool(q.get("diagram_prompts"))
    needs = any(w in txt for w in ("shown in the figure", "in the figure", "circuit shown",
                                   "the circuit below", "the figure below", "shown below",
                                   "given circuit", "waveform shown", "as shown"))
    if needs and not has_tag:
        rep.err(qno, "text refers to a figure/circuit but has no [GEMINI_FLASH_PROMPT] diagram_prompt")


def check_repeats(paper, rep, log_keys, log_sigs):
    seen = {}
    for _, q in iter_q(paper):
        key = P.repeat_key(q)
        if key is None:
            continue  # pure-theory item; not value-deduped
        qno = q.get("number", "?")
        if key in seen:
            rep.err(qno, f"EXACT-VALUE repeat of Q{seen[key]} (same subject/topic/type and identical numbers)")
        else:
            seen[key] = qno
        if key in log_keys:
            rep.err(qno, "EXACT-VALUE repeat of an item already in the exclusion log")
        elif P.value_signature(q) in log_sigs:
            rep.warn(qno, "numbers match a logged item (different subject/topic) — double-check it's not a reused dataset")


def _archetype(q):
    """Number-stripped concept signature: (subject, chapter, topic, type, core-no-digits)."""
    fp = str(q.get("fingerprint") or "")
    parts = fp.split("_", 3)
    core = parts[3] if len(parts) > 3 else ""
    core = re.sub(r"\s+", " ", re.sub(r"[-+]?\d*\.?\d+", "#", core)).strip()
    return ((q.get("subject") or "").lower(), (q.get("chapter") or "").lower(),
            (q.get("topic") or "").lower(), (q.get("type") or "").upper(), core)


def load_log_archetypes(path):
    archs = set()
    if not path or path == "-" or not os.path.exists(path) or not path.lower().endswith(".csv"):
        return archs
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            chap, _, top = (r.get("chapter_topic", "") or "").partition(">")
            archs.add(_archetype({"fingerprint": r.get("fingerprint", ""),
                                  "subject": r.get("subject", ""),
                                  "chapter": chap.strip(), "topic": top.strip(),
                                  "type": r.get("type", "")}))
    return archs


# --- TEMPLATE / DIAGRAM reuse caps (the hard backstop for "same Q, new numbers") ---
# A text/structure template may recur at most this many times ACROSS THE WHOLE SERIES;
# a diagram (circuit/figure) topology, harder still. Beyond the cap -> build-blocking
# ERROR, so a template can't be re-skinned across every mock with only fresh values.
TEXT_TEMPLATE_CAP = 2     # same wording, numbers-only difference: allowed 2x over the series
FIGURE_TOPOLOGY_CAP = 1   # same diagram drawn with different data: allowed once over the series


def load_log_template_counts(path):
    """Cumulative occurrence counts from the log: template_signature keys and
    diagram_signature keys already used across prior mocks. Empty for old logs
    that predate these columns (so history isn't retroactively blocked)."""
    from collections import Counter
    tmpl, dia = Counter(), Counter()
    if not path or path == "-" or not os.path.exists(path) or not path.lower().endswith(".csv"):
        return tmpl, dia
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            ts = (r.get("template_signature") or "").strip()
            if ts:
                tmpl[ts] += 1            # bare signature (identity folded in) — format-independent
            ds = (r.get("diagram_signature") or "").strip()
            if ds:
                dia[ds] += 1
    return tmpl, dia


def check_template_caps(paper, rep, log_tmpl, log_dia):
    """ERROR when a structure/diagram would exceed its cumulative-series cap. This is
    what the value-signature gate cannot see: same template, fresh numbers. Counts the
    paper's own questions on top of the log so the over-the-line item is pinpointed."""
    tmpl_run = dict(log_tmpl)
    dia_run = dict(log_dia)
    for _, q in iter_q(paper):
        qno = q.get("number", "?")
        tkey = P.template_signature(q)
        if tkey:
            tmpl_run[tkey] = tmpl_run.get(tkey, 0) + 1
            if tmpl_run[tkey] > TEXT_TEMPLATE_CAP:
                rep.err(qno, f"TEMPLATE over-reuse: this question structure (same wording — only the "
                             f"numbers differ) would appear {tmpl_run[tkey]}x across the series "
                             f"(cap {TEXT_TEMPLATE_CAP}). Re-author it with a different configuration / "
                             f"given<->unknown / framing, not just new values.")
        if P.has_diagram(q):
            dsig = P.diagram_signature(q)
            if dsig:
                dia_run[dsig] = dia_run.get(dsig, 0) + 1
                if dia_run[dsig] > FIGURE_TOPOLOGY_CAP:
                    rep.err(qno, f"DIAGRAM over-reuse: this circuit/figure TOPOLOGY would appear "
                                 f"{dia_run[dsig]}x across the series (cap {FIGURE_TOPOLOGY_CAP}). "
                                 f"Same diagram with different data is the #1 repetition source — change "
                                 f"the topology (series<->parallel, add/move a source, bridge/ladder/Y-delta), "
                                 f"not just the values.")


def check_diversity(paper, rep, log_archs):
    """Cross-mock variety: WARN if too many questions reuse an archetype from prior mocks
    (same concept, just new numbers/wording) — that's the 'near-identical mock' failure."""
    if not log_archs:
        return
    qs = [q for _, q in iter_q(paper)]
    if not qs:
        return
    reused = sum(1 for q in qs if _archetype(q) in log_archs)
    pct = 100.0 * reused / len(qs)
    if pct >= 40:
        rep.warn("diversity", f"{reused}/{len(qs)} questions ({pct:.0f}%) reuse an archetype from "
                 "prior mocks — rotate into unused syllabus types (run coverage_report.py) and vary "
                 "the angle/difficulty so this isn't a re-skin of the last mock")


def check_counts(paper, rep):
    meta = paper.get("meta", {})
    allq = [q for _, q in iter_q(paper)]
    n = len(allq)
    declared = meta.get("total_questions")
    if declared not in (None, "") and int(declared) != n:
        rep.err("counts", f"generated {n} questions but meta.total_questions = {declared}")

    # marks total
    declared_marks = meta.get("total_marks")
    try:
        tot_marks = sum(float(q.get("marks") or 0) for q in allq)
        if declared_marks not in (None, "") and abs(float(declared_marks) - tot_marks) > 0.5:
            rep.err("counts", f"marks sum to {tot_marks:g} but meta.total_marks = {declared_marks}")
    except (TypeError, ValueError):
        pass

    # wildcard share (expected ~10% if meta.expected_wildcard_pct given, default check only warns)
    exp = meta.get("expected_wildcard_pct")
    if exp:
        wc = sum(1 for q in allq if q.get("is_wildcard"))
        share = 100.0 * wc / n if n else 0
        if abs(share - float(exp)) > 3:  # +/-3 percentage points tolerance
            rep.warn("counts", f"wildcards are {share:.0f}% ({wc}/{n}); expected ~{exp}%")

    # target distribution (optional): {"subjects": {name: count}, "marks": {"1": n,"2": m},
    #                                   "formats": {"MCQ": n, "NAT": m, ...}}
    td = meta.get("target_distribution") or {}
    if td.get("subjects"):
        got = {}
        for q in allq:
            got[q.get("subject", "")] = got.get(q.get("subject", ""), 0) + 1
        for subj, want in td["subjects"].items():
            if got.get(subj, 0) != want:
                rep.err("dist", f"subject '{subj}': got {got.get(subj,0)}, locked matrix wants {want}")
    if td.get("marks"):
        got = {}
        for q in allq:
            got[str(q.get("marks"))] = got.get(str(q.get("marks")), 0) + 1
        for mk, want in td["marks"].items():
            if got.get(str(mk), 0) != want:
                rep.err("dist", f"{mk}-mark questions: got {got.get(str(mk),0)}, locked matrix wants {want}")
    if td.get("formats"):
        got = {}
        for q in allq:
            t = (q.get("type") or "").upper()
            got[t] = got.get(t, 0) + 1
        for fmt, want in td["formats"].items():
            if got.get(fmt.upper(), 0) != want:
                rep.err("dist", f"format '{fmt}': got {got.get(fmt.upper(),0)}, locked matrix wants {want}")
    if td.get("sections"):
        got = {}
        for sec in paper.get("sections", []):
            got[sec.get("section", "")] = len(sec.get("questions", []))
        for sec, want in td["sections"].items():
            if got.get(sec, 0) != want:
                rep.err("dist", f"section '{sec}': got {got.get(sec,0)}, locked matrix wants {want}")


def check_constraints(paper, rep):
    """meta.structural_constraints: list of {"section": str, "forbid_types": [..]}."""
    cons = (paper.get("meta") or {}).get("structural_constraints") or []
    if not cons:
        return
    by_sec = {}
    for c in cons:
        by_sec.setdefault(c.get("section", "").strip().lower(), set()).update(
            t.upper() for t in c.get("forbid_types", []))
    for sname, q in iter_q(paper):
        forbid = by_sec.get(sname.strip().lower())
        if forbid and (q.get("type") or "").upper() in forbid:
            rep.err(q.get("number", "?"),
                    f"type {q.get('type')} is forbidden in section '{sname}' by structural_constraints")


def load_taxonomy_maps(path):
    """Build canonical lookup sets from the master sheet via load_taxonomy.parse().
    Returns (subjects, chapters, topics, not_in_syllabus) of lowercased keys, or
    None if the taxonomy can't be loaded."""
    try:
        import load_taxonomy as lt
        tax = lt.parse(path)
    except Exception as e:
        print(f"  (taxonomy check skipped — could not load master: {e})")
        return None
    subjects, chaps, topics, nosyll = set(), set(), set(), set()
    for subj, sd in (tax.get("subjects") or {}).items():
        s = subj.strip().lower()
        subjects.add(s)
        for ch in sd.get("chapters", []):
            c = (ch.get("name") or "").strip().lower()
            cnote = (ch.get("note") or "").lower()
            chaps.add((s, c))
            for tp in ch.get("topics", []):
                t = (tp.get("name") or "").strip().lower()
                topics.add((s, c, t))
                if "not in syll" in (cnote + " " + (tp.get("note") or "").lower()):
                    nosyll.add((s, c, t))
    return subjects, chaps, topics, nosyll


def check_taxonomy(paper, rep, maps):
    """Snap-to-canonical: subject MUST be in the master (ERROR); chapter/topic
    drift is flagged (WARN) so it gets snapped or recorded as a candidate addition."""
    subjects, chaps, topics, nosyll = maps
    for _, q in iter_q(paper):
        qno = q.get("number", "?")
        s = (q.get("subject") or "").strip().lower()
        c = (q.get("chapter") or "").strip().lower()
        t = (q.get("topic") or "").strip().lower()
        if s and s not in subjects:
            rep.err(qno, f"subject '{q.get('subject')}' is not a canonical subject in the master taxonomy")
            continue
        if c and (s, c) not in chaps:
            rep.warn(qno, f"chapter '{q.get('chapter')}' is not canonical under '{q.get('subject')}' — snap to the master or flag as a candidate addition")
            continue
        if t and (s, c, t) not in topics:
            rep.warn(qno, f"topic '{q.get('topic')}' is not canonical under {q.get('subject')} > {q.get('chapter')} — snap to the master or flag as a candidate addition")
        elif (s, c, t) in nosyll:
            rep.warn(qno, f"topic '{q.get('topic')}' is marked 'Not in Syllabus' in the master")


def main():
    args = [a for a in sys.argv[1:]]
    no_tax = "--no-tax" in args
    args = [a for a in args if a != "--no-tax"]
    tax_path = None
    if "--taxonomy" in args:
        i = args.index("--taxonomy")
        tax_path = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        sys.exit(2)
    paper_path = args[0]
    log_path = args[1] if len(args) > 1 else None

    with open(paper_path, encoding="utf-8") as f:
        paper = json.load(f)
    log_keys, log_sigs = load_log_keys(log_path)
    log_archs = load_log_archetypes(log_path)
    log_tmpl, log_dia = load_log_template_counts(log_path)

    meta = paper.get("meta", {})
    show_solutions = meta.get("show_solutions", True)
    rep = Report()

    for sname, q in iter_q(paper):
        check_structure(sname, q, rep)
        check_answer_solution(q, rep, show_solutions)
        check_concept(q, rep)
        check_diagram(q, rep)
    check_counts(paper, rep)
    check_constraints(paper, rep)
    check_repeats(paper, rep, log_keys, log_sigs)
    check_template_caps(paper, rep, log_tmpl, log_dia)
    check_diversity(paper, rep, log_archs)

    # taxonomy (Subject/Chapter/Topic must come from the master sheet)
    if not no_tax:
        default_tax = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "assets", "chapter_topic_master.xlsx")
        path = tax_path or default_tax
        if os.path.exists(path):
            maps = load_taxonomy_maps(path)
            if maps:
                check_taxonomy(paper, rep, maps)
        elif tax_path:
            rep.err("tax", f"taxonomy file not found: {tax_path}")

    nq = sum(1 for _ in iter_q(paper))
    print(f"Validated {nq} questions in {paper_path}")
    if rep.warnings:
        print(f"\n  {len(rep.warnings)} WARNING(S):")
        for qno, m in rep.warnings:
            print(f"    [Q{qno}] {m}")
    if rep.errors:
        print(f"\n  {len(rep.errors)} ERROR(S) — must fix/regenerate before building:")
        for qno, m in rep.errors:
            print(f"    [Q{qno}] {m}")
        print("\nRESULT: FAIL")
        sys.exit(1)
    print("\nRESULT: PASS" + (f" ({len(rep.warnings)} warning(s) to review)" if rep.warnings else " — clean"))
    sys.exit(0)


if __name__ == "__main__":
    main()
