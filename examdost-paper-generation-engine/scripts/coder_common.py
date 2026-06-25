"""Shared helpers for the LaTeX Question Coder skill.

Used by both engines:
  * inject_codes.py       -> .tex files (regex header matching)
  * inject_codes_docx.py  -> .docx files (one table per question, Question + OTS ID cells)
"""
from pathlib import Path

DEFAULT_OLD_COL = "Question number"
DEFAULT_NEW_COL = "Masterfile Question number"
DEFAULT_CODE_COL = "Code"
DEFAULT_TEST_COL = "2026"


def load_rows(path: Path, sheet=None):
    """Return (list-of-dict rows, list-of-column-names) with stripped headers.

    `sheet` (name or index) selects a worksheet in a multi-sheet .xlsx; ignored for csv.

    .xlsx is read via openpyxl (not pandas): pandas silently drops trailing columns
    when the header row has header-less cells after a named one (seen in the CIL
    mapping workbook, where the 'Code' column sits before 3 unnamed columns).
    """
    path = Path(path)
    if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
        import openpyxl

        # NOTE: do NOT use read_only=True — it trusts a cached worksheet dimension
        # that can be too narrow and drops real trailing columns (e.g. 'Code').
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.worksheets[0] if sheet is None else (
            wb[sheet] if isinstance(sheet, str) else wb.worksheets[int(sheet)]
        )
        it = ws.iter_rows(values_only=True)
        try:
            header_raw = next(it)
        except StopIteration:
            return [], []
        # keep only columns that have a real header; remember their positions
        cols, idxs = [], []
        for i, h in enumerate(header_raw):
            if h is not None and str(h).strip() != "":
                cols.append(str(h).strip())
                idxs.append(i)
        rows = []
        for raw in it:
            rec = {}
            for c, i in zip(cols, idxs):
                v = raw[i] if i < len(raw) else None
                rec[c] = "" if v is None else str(v).strip()
            rows.append(rec)
        return rows, cols

    import pandas as pd

    df = pd.read_csv(path, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]  # e.g. "Masterfile Question number "
    df = df.fillna("")
    return df.to_dict(orient="records"), list(df.columns)


def resolve_col(requested, columns, fallback_to_last=False, role=""):
    """Match a requested column name case/space-insensitively against real columns."""
    if requested in columns:
        return requested
    norm = {c.strip().lower(): c for c in columns}
    if requested and requested.strip().lower() in norm:
        return norm[requested.strip().lower()]
    if fallback_to_last and columns:
        return columns[-1]
    raise SystemExit(
        f"ERROR: could not find the {role or requested!r} column.\n"
        f"  Looked for: {requested!r}\n  Available:  {columns}"
    )


def as_int_str(v):
    """Normalize a number-ish cell to a clean string ('33', not '33.0')."""
    s = str(v).strip()
    if s == "":
        return ""
    try:
        f = float(s)
        if f.is_integer():
            return str(int(f))
    except ValueError:
        pass
    return s


def _key(x):
    return int(x) if str(x).isdigit() else 1 << 30


def build_map(rows, old_col, new_col, code_col, test_col, test_value):
    """Return (mapping, problems, matched_rows). mapping[old]={'new','code','row'}."""
    mapping, problems, seen_old, matched_rows = {}, [], {}, 0
    for i, r in enumerate(rows, start=2):  # +2: header is row 1
        # test_value=None  -> no test filtering (whole sheet is one document)
        if test_value is not None and str(r.get(test_col, "")).strip() != test_value:
            continue
        old_raw = as_int_str(r.get(old_col, ""))
        if old_raw == "" and all(str(v).strip() == "" for v in r.values()):
            continue  # skip fully-blank trailing rows
        matched_rows += 1
        old = as_int_str(r.get(old_col, ""))
        new = as_int_str(r.get(new_col, ""))
        code = str(r.get(code_col, "")).strip()
        if old == "":
            problems.append(f"row {i}: blank old number ({old_col})")
            continue
        if old in seen_old:
            problems.append(f"row {i}: duplicate old number {old} (first seen row {seen_old[old]})")
            continue
        seen_old[old] = i
        if new == "":
            problems.append(f"row {i}: old {old} has blank new number ({new_col})")
        if code == "":
            problems.append(f"row {i}: old {old} has blank code ({code_col})")
        mapping[old] = {"new": new, "code": code, "row": i}
    return mapping, problems, matched_rows


def available_tests(rows, test_col):
    return sorted({str(r.get(test_col, "")).strip() for r in rows if str(r.get(test_col, "")).strip()})


def write_audit(path, title, test_value, mapping, found_old, problems,
                matched_rows, applied, out_path, extra_notes=None):
    """Generic audit. found_old = list of old numbers located in the document."""
    found_set = set(found_old)
    map_set = set(mapping)
    in_excel_not_doc = sorted(map_set - found_set, key=_key)
    in_doc_not_excel = sorted(found_set - map_set, key=_key)
    dup_in_doc = sorted({n for n in found_old if found_old.count(n) > 1}, key=_key)

    L = [f"# {title} — audit: {test_value}\n",
         f"- Mode: {'APPLIED -> ' + str(out_path) if applied else 'DRY RUN (no file written)'}",
         f"- Excel rows for this test: **{matched_rows}**",
         f"- Unique questions mapped from Excel: **{len(mapping)}**",
         f"- Questions located in document: **{len(found_old)}**",
         f"- Matched & updated: **{len(map_set & found_set)}**\n"]

    def block(t, items):
        L.append(f"## {t}: {len(items)}")
        L.append("`" + ", ".join(items) + "`" if items else "_none_ ✓")
        L.append("")

    block("In Excel but NOT found in document (did NOT get coded)", in_excel_not_doc)
    block("In document but NOT in Excel (left untouched)", in_doc_not_excel)
    block("Duplicate question numbers in document", dup_in_doc)

    for note in (extra_notes or []):
        L.append(note)
    if extra_notes:
        L.append("")

    if problems:
        L.append(f"## Data problems in the sheet: {len(problems)}")
        L += [f"- {p}" for p in problems]
        L.append("")

    ok = not in_excel_not_doc and not in_doc_not_excel and not dup_in_doc
    L.append("## Verdict")
    L.append("**CLEAN — every Excel question matched a document question 1:1.** ✓" if ok
             else "**REVIEW NEEDED — mismatches above. Fix before --apply.**")
    Path(path).write_text("\n".join(L), encoding="utf-8")
    return "\n".join(L)
