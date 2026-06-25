#!/usr/bin/env python3
"""
inject_codes.py  -- LaTeX Question Coder

Reads a "Data Analysis"-style coding sheet (.csv / .xlsx), filters the rows for ONE
test (by the Test-Number column), then rewrites that test's LaTeX file so that each
question is:

  1. RENUMBERED   old number (Col A) -> new number (Col B)
  2. CODE-INJECTED the question Code (Col I) is added next to / above the question

The script does NOT reorder questions. It finds each question *in place* by its
current (old) number and relabels it.

DEFAULT IS A DRY RUN (audit only). Pass --apply to actually write the output file.

Typical use
-----------
  # 1) Inspect what headers the regex is catching (verify before committing):
  python inject_codes.py --excel sheet.csv --test "PGCIL EE 01" --tex EE01.tex \
         --header-regex '...' --list-headers

  # 2) Dry-run audit (matched / missing / extra):
  python inject_codes.py --excel sheet.csv --test "PGCIL EE 01" --tex EE01.tex \
         --header-regex '...'

  # 3) Apply -> writes EE01_coded.tex (+ EE01_coded.audit.md):
  python inject_codes.py --excel sheet.csv --test "PGCIL EE 01" --tex EE01.tex \
         --header-regex '...' --code-template '\\hfill{\\footnotesize\\texttt{[{code}]}}' --apply

The --header-regex MUST contain a named group (?P<num>...) that captures the old
question number inside each question's header. Everything else in the match is left
untouched except that captured number, which is swapped for the new number.
"""
import argparse
import json
import re
import sys
from pathlib import Path


# ---- Excel / CSV loading -------------------------------------------------

DEFAULT_OLD_COL = "Question number"
DEFAULT_NEW_COL = "Masterfile Question number"
DEFAULT_CODE_COL = "Code"
DEFAULT_TEST_COL = "2026"

# Built-in header patterns. Use these via --header-preset so NO backslashes need to
# travel through the shell (some shells, e.g. Git-Bash on Windows, collapse "\\"->"\"
# even inside single quotes, which silently corrupts a regex). Each captures the old
# question number in the (?P<num>...) group.
HEADER_PRESETS = {
    # \textbf{1.}  /  \textbf{1)}
    "textbf-dot": r"\\textbf\{\s*(?P<num>\d+)\s*[.)]\s*\}",
    # \textbf{Q.1} / \textbf{Q1.} / \textbf{Q 1}
    "textbf-q": r"\\textbf\{\s*Q\.?\s*(?P<num>\d+)\s*[.)]?\s*\}",
    # \item[1.] / \item[1)]
    "item-bracket": r"\\item\[\s*(?P<num>\d+)\s*[.)]?\s*\]",
    # \que{1} / \question{1} / \qno{1}
    "que-macro": r"\\q(?:ue|uestion|no)\{\s*(?P<num>\d+)\s*\}",
    # line-leading  "1." / "Q1)" at the start of a line
    "line-num": r"(?m)^\s*Q?\.?\s*(?P<num>\d+)\s*[.)]\s",
    # **1.** markdown-ish bold sometimes seen in converted files
    "bold-md": r"\*\*\s*(?P<num>\d+)\s*[.)]\s*\*\*",
}


def load_rows(path: Path):
    """Return (list-of-dict rows, list-of-column-names) with stripped headers."""
    import pandas as pd

    if path.suffix.lower() in (".xlsx", ".xlsm", ".xls"):
        df = pd.read_excel(path, dtype=str)
    else:
        df = pd.read_csv(path, dtype=str)
    # strip whitespace from headers (the source has e.g. "Masterfile Question number ")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.fillna("")
    rows = df.to_dict(orient="records")
    return rows, list(df.columns)


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
        f"  Looked for: {requested!r}\n"
        f"  Available:  {columns}"
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


# ---- core --------------------------------------------------------------

def build_map(rows, old_col, new_col, code_col, test_col, test_value):
    """Return (mapping, problems) where mapping[old_num_str] = {'new':..,'code':..}."""
    mapping = {}
    problems = []
    seen_old = {}
    matched_rows = 0
    for i, r in enumerate(rows, start=2):  # +2 ~ header is row 1
        if str(r.get(test_col, "")).strip() != test_value:
            continue
        matched_rows += 1
        old = as_int_str(r.get(old_col, ""))
        new = as_int_str(r.get(new_col, ""))
        code = str(r.get(code_col, "")).strip()
        if old == "":
            problems.append(f"row {i}: blank old number ({old_col})")
            continue
        if old in seen_old:
            problems.append(
                f"row {i}: duplicate old number {old} (first seen row {seen_old[old]})"
            )
            continue
        seen_old[old] = i
        if new == "":
            problems.append(f"row {i}: old {old} has blank new number ({new_col})")
        if code == "":
            problems.append(f"row {i}: old {old} has blank code ({code_col})")
        mapping[old] = {"new": new, "code": code, "row": i}
    return mapping, problems, matched_rows


def find_headers(text, header_re):
    """Yield (match, old_num_str) for every question header."""
    out = []
    for m in header_re.finditer(text):
        if "num" not in m.groupdict():
            raise SystemExit("ERROR: --header-regex must contain a (?P<num>...) group.")
        out.append((m, as_int_str(m.group("num"))))
    return out


def rewrite(text, header_re, mapping, code_template, code_comment,
            renumber=True):
    """Return (new_text, stats). Replaces number + injects code per question header."""
    found_old = []
    used = set()

    def repl(m):
        old = as_int_str(m.group("num"))
        found_old.append(old)
        info = mapping.get(old)
        header = m.group(0)
        if info is None:
            return header  # leave untouched; reported as "extra" in audit
        used.add(old)
        new = info["new"] or old
        code = info["code"]

        # swap only the captured number span inside the header
        if renumber and new != old:
            s, e = m.span("num")
            hs = m.start()
            header = header[: s - hs] + new + header[e - hs :]

        # visible code, inserted right after the header.
        # NOTE: plain str.replace (NOT str.format) — LaTeX is full of { } braces
        # that str.format would misread as fields.
        if code_template:
            tpl = (code_template
                   .replace("{code}", code)
                   .replace("{newnum}", new)
                   .replace("{oldnum}", old))
            header = header + tpl

        # tracking comment, inserted on its own line *before* the header
        if code_comment:
            comment = f"% qcode: {code} | old {old} -> new {new}\n"
            header = comment + header
        return header

    new_text = header_re.sub(repl, text)
    stats = {
        "found_old": found_old,
        "used_old": sorted(used, key=lambda x: int(x) if x.isdigit() else 1 << 30),
    }
    return new_text, stats


# ---- audit -------------------------------------------------------------

def write_audit(path, test_value, mapping, found_old, problems, matched_rows,
                applied, out_path):
    found_set = set(found_old)
    map_set = set(mapping)
    in_excel_not_tex = sorted(map_set - found_set, key=lambda x: int(x) if x.isdigit() else 1 << 30)
    in_tex_not_excel = sorted(found_set - map_set, key=lambda x: int(x) if x.isdigit() else 1 << 30)
    dup_in_tex = sorted({n for n in found_old if found_old.count(n) > 1},
                        key=lambda x: int(x) if x.isdigit() else 1 << 30)

    lines = []
    lines.append(f"# LaTeX Question Coder — audit: {test_value}\n")
    lines.append(f"- Mode: {'APPLIED -> ' + str(out_path) if applied else 'DRY RUN (no file written)'}")
    lines.append(f"- Excel rows for this test: **{matched_rows}**")
    lines.append(f"- Unique questions mapped from Excel: **{len(mapping)}**")
    lines.append(f"- Question headers found in .tex: **{len(found_old)}**")
    lines.append(f"- Matched & rewritten: **{len(map_set & found_set)}**\n")

    def block(title, items):
        lines.append(f"## {title}: {len(items)}")
        if items:
            lines.append("`" + ", ".join(items) + "`")
        else:
            lines.append("_none_ ✓")
        lines.append("")

    block("In Excel but NOT found in .tex (these did NOT get coded)", in_excel_not_tex)
    block("In .tex but NOT in Excel (left untouched)", in_tex_not_excel)
    block("Duplicate question numbers detected in .tex", dup_in_tex)

    if problems:
        lines.append(f"## Data problems in the sheet: {len(problems)}")
        for p in problems:
            lines.append(f"- {p}")
        lines.append("")

    ok = not in_excel_not_tex and not in_tex_not_excel and not dup_in_tex
    lines.append("## Verdict")
    lines.append("**CLEAN — every Excel question matched a .tex question 1:1.** ✓"
                 if ok else
                 "**REVIEW NEEDED — mismatches above. Fix the regex or the data before --apply.**")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


# ---- cli ---------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Renumber + inject question codes into a test's LaTeX file.")
    ap.add_argument("--excel", required=True, help="Path to the coding sheet (.csv or .xlsx)")
    ap.add_argument("--test", required=True, help='Test value to filter on, e.g. "PGCIL EE 01"')
    ap.add_argument("--tex", required=True, help="Path to the test's .tex file")
    ap.add_argument("--out", help="Output .tex path (default: <tex>_coded.tex)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--header-preset", choices=sorted(HEADER_PRESETS),
                   help="Built-in header pattern (preferred — no shell backslash issues)")
    g.add_argument("--header-regex",
                   help=r"Custom regex with (?P<num>...). WARNING: backslashes may be mangled "
                        r"by the shell; prefer --header-preset or --header-regex-file")
    g.add_argument("--header-regex-file",
                   help="Path to a file whose contents are the regex (safe for backslashes)")
    ap.add_argument("--code-template", default="",
                    help=r'Visible code text inserted after the header. Placeholders: {code},{newnum},{oldnum}. '
                         r'e.g. "\\hfill{\\footnotesize\\texttt{[{code}]}}"')
    ap.add_argument("--no-comment", action="store_true",
                    help="Do NOT insert the '% qcode:' tracking comment before each question")
    ap.add_argument("--no-renumber", action="store_true",
                    help="Keep the existing question number; only inject the code")
    ap.add_argument("--old-col", default=DEFAULT_OLD_COL)
    ap.add_argument("--new-col", default=DEFAULT_NEW_COL)
    ap.add_argument("--code-col", default=DEFAULT_CODE_COL)
    ap.add_argument("--test-col", default=DEFAULT_TEST_COL)
    ap.add_argument("--list-headers", action="store_true",
                    help="Just print the first 40 headers the regex matches, then exit")
    ap.add_argument("--apply", action="store_true", help="Write the output file (default: dry run)")
    args = ap.parse_args()

    excel = Path(args.excel)
    tex = Path(args.tex)
    if not excel.exists():
        raise SystemExit(f"ERROR: excel not found: {excel}")
    if not tex.exists():
        raise SystemExit(f"ERROR: tex not found: {tex}")

    text = tex.read_text(encoding="utf-8")

    if args.header_preset:
        pattern = HEADER_PRESETS[args.header_preset]
    elif args.header_regex_file:
        pattern = Path(args.header_regex_file).read_text(encoding="utf-8").strip("\r\n")
    else:
        pattern = args.header_regex
    if "(?P<num>" not in pattern:
        raise SystemExit("ERROR: the header pattern must contain a (?P<num>...) group.")
    try:
        header_re = re.compile(pattern)
    except re.error as e:
        raise SystemExit(f"ERROR: bad header pattern: {e}\n  pattern was: {pattern!r}")

    if args.list_headers:
        hits = find_headers(text, header_re)
        print(f"{len(hits)} header(s) matched. First 40:")
        for m, num in hits[:40]:
            snippet = m.group(0).replace("\n", "\\n")
            if len(snippet) > 80:
                snippet = snippet[:77] + "..."
            print(f"  old#={num:>4}   {snippet}")
        return

    rows, columns = load_rows(excel)
    old_col = resolve_col(args.old_col, columns, role="old number")
    new_col = resolve_col(args.new_col, columns, role="new number")
    code_col = resolve_col(args.code_col, columns, role="code")
    test_col = resolve_col(args.test_col, columns, fallback_to_last=True, role="test number")

    mapping, problems, matched_rows = build_map(
        rows, old_col, new_col, code_col, test_col, args.test
    )
    if matched_rows == 0:
        # help the user see valid test values
        vals = sorted({str(r.get(test_col, "")).strip() for r in rows if str(r.get(test_col, "")).strip()})
        raise SystemExit(
            f"ERROR: no rows where {test_col!r} == {args.test!r}.\n"
            f"  Available test values: {vals}"
        )

    new_text, stats = rewrite(
        text, header_re, mapping,
        code_template=args.code_template,
        code_comment=not args.no_comment,
        renumber=not args.no_renumber,
    )

    out_path = Path(args.out) if args.out else tex.with_name(tex.stem + "_coded.tex")
    audit_path = out_path.with_suffix(".audit.md")

    if args.apply:
        out_path.write_text(new_text, encoding="utf-8")

    report = write_audit(
        audit_path, args.test, mapping, stats["found_old"], problems,
        matched_rows, args.apply, out_path,
    )
    print(report)
    print(f"\n[audit written to] {audit_path}")
    if args.apply:
        print(f"[coded tex written to] {out_path}")
    else:
        print("\nDRY RUN — re-run with --apply to write the coded .tex.")


if __name__ == "__main__":
    main()
