<!-- MODE: CODE — Question Number & OTS-ID Code Update -->
<!-- Workflow module of the merged `examdost-paper-generation-engine` skill.
     All scripts/..., references/..., assets/... paths resolve inside THIS skill folder.
     Read this file in full once the router selects this mode, then execute end-to-end. -->

# LaTeX Question Coder

## What this skill does

The user has **test papers already built** plus a **coding sheet** (a "Data
Analysis"-style `.csv`/`.xlsx`) that says, per test and per question: the
question's **new number** and its **Code**. For each test you, **in place, without
reordering**:

1. **Write the Code** into the question's **OTS ID** slot (currently blank).
2. **Renumber** the question — old number (Col A) → new number (Col B).

Then write a **new `_coded` copy** (originals are never overwritten) and an
**audit** proving every question matched 1:1.

You do **not** write or analyse questions. You apply a map the user already has.

## Two engines — pick by file type

| Paper format | Engine | How a question is found |
|--------------|--------|--------------------------|
| **`.docx` "Boxed"** (one 2-col table per question) — **the usual case** | `scripts/inject_codes_docx.py` | the `Question` row = old number; the `OTS ID` row = where the code goes |
| **`.tex`** (regex header) | `scripts/inject_codes.py` | a header preset captures the old number |

Both share the same Excel filtering + audit logic (`coder_common.py`).

## The coding sheet (default layout)

One row per question. Filter rows by the **test column** to get a single test.

| Col | Default header | Role |
|-----|----------------|------|
| A | `Question number` | **old** number — what the paper shows now (per-test 1…N) |
| B | `Masterfile Question number` | **new** number to write |
| I | `Code` | the code to inject into OTS ID (e.g. `AJEEEPSA212033`) |
| J | `2026` | **test filter**, e.g. `PGCIL EE 01`, `PGCIL EE 02` |

Headers match loosely; the test filter falls back to the last column if `2026`
isn't present. **Old numbers are the join key and must be unique within a test** —
the audit flags duplicates. The new number (Col B) is a per-subject serial, so it
may repeat within a test (1,2,3 restart each subject); that's expected because the
match is on the *old* number, which is unique.

> Folder → test mapping: a folder like `…/Mock 02/` corresponds to the sheet's
> `PGCIL EE 02`. Confirm the exact test string with the user if unsure; the script
> prints the available test values on a mismatch.

---

## WORKFLOW A — Boxed `.docx` (primary)

### A1. Identify the paper file and the test
The Boxed paper is the `… Boxed.docx`. There may also be a `… Boxed (LaTeX).docx`
(equations converted to `$…$`) under a `LaTeX/` subfolder — **same table
structure, so the script works on either/both.** Ask the user which to code, or do
both. Map the mock number to the sheet's test string (Mock 02 → `PGCIL EE 02`).

### A2. Dry-run audit (writes nothing to the docx)
```
python scripts/inject_codes_docx.py --excel "<sheet>" --test "<TEST>" --docx "<Boxed.docx>"
```
Read the audit. Verdict must be **CLEAN**: the three mismatch lists empty, and the
"Document scan" should show *Question tables = OTS ID cells to fill = renumbered =
question count*. The scan also warns if any OTS ID is already filled (those are
**skipped** unless `--overwrite-ots`).

### A3. Apply
```
python scripts/inject_codes_docx.py --excel "<sheet>" --test "<TEST>" --docx "<Boxed.docx>" --apply
```
Writes `<name>_coded.docx` + `<name>_coded.audit.md` next to the source. Run again
for the `(LaTeX)` variant if needed.

### A4. Report
Per file: matched/renumbered, OTS IDs filled, any skipped, output path. Don't claim
success unless the audit said CLEAN.

**docx flags:** `--no-renumber` (fill OTS ID only), `--overwrite-ots` (replace
non-blank OTS IDs), `--question-label`/`--ots-label` (if the row labels differ),
`--out`, plus the `--*-col` overrides. `--apply` to write (omit = dry run).

---

## WORKFLOW B — `.tex` (regex)

Use only when the paper is a real `.tex`. Find how a question header looks, pick a
`--header-preset` (`textbf-dot`, `textbf-q`, `item-bracket`, `que-macro`,
`line-num`, `bold-md`), then:
```
python scripts/inject_codes.py --excel "<sheet>" --test "<TEST>" --tex "<f.tex>" --header-preset <p> --list-headers   # verify count
python scripts/inject_codes.py --excel "<sheet>" --test "<TEST>" --tex "<f.tex>" --header-preset <p>                  # dry-run audit
python scripts/inject_codes.py --excel "<sheet>" --test "<TEST>" --tex "<f.tex>" --header-preset <p> --code-template ' \texttt{\footnotesize [{code}]}' --apply
```
See `references/latex_formats.md`. **Shell-backslash hazard:** Windows Git-Bash
collapses `\\`→`\` even in single quotes, corrupting a raw `--header-regex`; always
prefer a preset, or `--header-regex-file`. The `--code-template` placeholders
`{code}`/`{newnum}`/`{oldnum}` are replaced literally (safe with LaTeX braces).

---

## Behaviour guarantees (both engines)
- **Defaults to a dry run.** Nothing is written without `--apply`.
- **Never overwrites the original** — output is a new `_coded` copy.
- **No reordering.** Each question is edited where it sits.
- **Surgical edits.** docx: only the OTS ID + Question value cells change (cell
  styling/borders preserved); tex: only the captured number, plus the injected
  code, change.
- **Every run writes an audit** so a wrong key, a sheet/paper mismatch, or an
  already-filled OTS ID is caught before delivery.

## Multiple tests / files
Loop one invocation per `(test, file)` pair; collect the per-file audits and report
together.

## Setup
`pip install -r scripts/requirements.txt` (pandas, openpyxl, python-docx). Running
`python`/`pip` is pre-authorised here, so scripts run without prompts.
