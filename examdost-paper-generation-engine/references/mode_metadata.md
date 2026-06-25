<!-- MODE: TAG — Per-Question Metadata & Excel Classification -->
<!-- Workflow module of the merged `examdost-paper-generation-engine` skill.
     All scripts/..., references/..., assets/... paths resolve inside THIS skill folder.
     Read this file in full once the router selects this mode, then execute end-to-end. -->

# Metadata Tagger — the per-question classification sheet

## What this skill does

You take **a set of exam questions the user already has** — in any format — and
produce one downloadable Excel: the **"Mock-01 Metadata"-style sheet**, one row
per question, seven fixed columns. That sheet is how every ExamDost question gets
filed against the canonical taxonomy so it lines up with the paper analyses
(Skill-01) and the generated papers (Skill-02).

You do **not** write questions and you do **not** analyse a paper for weightage.
You read questions that exist and you classify them. That's the whole job, and
the bar is simple: **right question, right row, right values, names snapped to
the master** so the numbers come out clean.

## The output — exactly these 7 columns, in this order

| # | Header | What goes in it |
|---|--------|-----------------|
| 1 | `Question number` | the source's own number if it has one (e.g. 459–548), else running `1..N` |
| 2 | `Subject Name` | canonical subject (master taxonomy) |
| 3 | `Chapter number` | the chapter's number in the master, for that subject |
| 4 | `type number` | the Type No of the question's topic within that chapter |
| 5 | `difficulty index` | `1` Easy / `2` Moderate / `3` Difficult |
| 6 | `Marks` | marks for the question (e.g. 1 or 2) |
| 7 | `TheoryMCQ/Numerical MCQ/NAT/MSQ/StatementType/Assertion-Reason` | the question type |

These headers and the 1/2/3 difficulty scale are fixed — they must match the
existing template, so do not rename, reorder, or recolour them. The builder
script owns the exact headers; you just feed it clean data.

**Where the chapter & type numbers come from:** you never type them by hand. You
write the canonical **chapter name** and **topic name** for each question; the
builder looks up the chapter number and Type No from the master taxonomy. Get the
names right and the numbers take care of themselves.

**Aptitude & GK subjects (master update 2026-06):** the master has **no
`General Aptitude` sheet** — never use that as a Subject Name. Classify every
aptitude question into the specific sheet it belongs to: `Verbal Ability`
(grammar, vocabulary, idioms, sentence work), `Numerical Ability` (arithmetic,
algebra, mensuration, DI, modern maths), or `Reasoning` (verbal / non-verbal /
analytical reasoning). Classify by **content**, not by which exam section the
question sat in — e.g. an age/work-rate puzzle from a "reasoning" section is
`Numerical Ability`, a number-series question is `Reasoning > Verbal Reasoning >
Series - Number and Alphabet`. GK questions likewise go to `General Awareness`
or `General Science` — never a generic "GK"/"General Knowledge" subject.

## Where to write the output

This is a global skill that runs in any chat. **Always write the finished sheet
to its own dedicated folder, `~/Desktop/Question Metadata/`** — never into the
current working/project directory, never into this skill's own folder, and
**never alongside the upload.** That last point matters: the input is often a
`paper.json` (or a paper) that lives inside `~/Desktop/Generated Papers/...`, and
the user does not want metadata sheets landing in there — keep them cleanly
separate in `Question Metadata/`. Only use a different location if the user names
one explicitly.

Name the file after the set, e.g. `Mock-01 Metadata.xlsx` or
`<Set name> Metadata.xlsx`. Keep the intermediate `questions.json` in a
`~/Desktop/Question Metadata/_workspace/` scratch subfolder.

---

# THE WORKFLOW

Four steps, one hard halt at the start. Don't auto-advance past the intake gate.

## STEP 1 — Intake gate

Open by asking for the inputs, then **HALT and wait**:

```
To build your metadata sheet I need:

 1. The questions — a file path (.docx, .pdf, .xlsx, .csv, .txt) or pasted text,
    or a paper.json from the generator. Whatever you've got.
 2. The target exam — e.g. GATE EE, ESE, SSC JE. (This sets how marks are
    weighted; for GATE I weight each question 1 or 2 marks from the PYQ pattern.)
 3. (Optional) A newer master taxonomy sheet — otherwise I use the bundled
    ExamDost "Type List Master Sheet".

Marks: if the questions already state marks, I'll use them. If not and the exam
is GATE, I'll assign 1/2 marks from the marks benchmark for that subject — and if
I don't yet have a benchmark for the subject, I'll ask you for a Previous-Year-
Questions file to build one. For a fixed-marks exam, just tell me the scheme
(e.g. all 1 mark).
```

Don't proceed until you have the questions and know the exam. The taxonomy has a
bundled default, so that one is genuinely optional.

**Marks — decide the source before you classify:**
1. **Marks are on the questions** → use them verbatim, don't ask, don't override.
2. **No marks, exam is GATE** → this is the new behaviour. Marks are **1 or 2**
   and you decide per question from the **GATE marks benchmark** for the subject
   (see Step 3 and `references/marks_benchmarks/`). If a benchmark file exists for
   the subject, load it and apply it. **If no benchmark exists for the subject,
   STOP and ask the user for a PYQ file** so you can build one first:
   ```
   I don't have a GATE marks benchmark for <subject> yet. Send me a Previous-Year-
   Questions file for it (e.g. the ExamDost GATE PYQ PDF, with the [year: N Mark]
   tags) and I'll learn the 1-vs-2-mark pattern before tagging your set.
   ```
   Then build the benchmark (Step 1b) before continuing.
3. **No marks, fixed-marks exam** (e.g. all 1 mark) → ask the scheme once, apply it.

## STEP 1b — Build a GATE marks benchmark (only when one is missing)

When the user gives a PYQ file for a subject you don't yet have a benchmark for:
```
python scripts/derive_marks_benchmark.py "<pyq.pdf>" -o "~/Desktop/Question Metadata/_workspace"
```
This parses every `[year: N Mark]`-tagged PYQ and writes a `*.marks_stats.txt`
(counts by chapter and year + sampled 1-mark and 2-mark stems) and a records
JSON. **Read the stats file** — especially the sampled stems — and distill it into
a short benchmark at `references/marks_benchmarks/<subject>_<exam>.md`, following
the shape of the existing `network_analysis_gate.md`: the 1-vs-2-mark decision
signals, the per-chapter base rates, the difficulty calibration, and a few worked
calls. That file is reusable for every future set in that subject, so it's worth
getting right once. Then continue to Step 2.

## STEP 2 — Parse the questions

Get the questions into text you can read, then read **all** of them.

- **paper.json** (from paper-generator): skip parsing — feed it straight to the
  builder in Step 4, it already has subject/chapter/topic/difficulty/marks/type.
- **pasted text:** read it directly.
- **a file:** run the extractor to pull faithful text out of any format:
  ```
  python scripts/extract_text.py "<path-to-questions>" -o "<workspace>/raw.txt"
  ```
  It handles .docx (paragraphs + tables), .pdf (page by page), .xlsx/.csv (row
  per line), and plain text. Read the result.

For each question, pull out: the **statement**, the **options** (if any), the
**correct answer**, the **marks**, and **any tags already present** (subject /
chapter / topic / difficulty). Existing tags are gold — prefer them over your own
classification (see the rules file). Don't lose questions: a paper with 65 items
must yield 65 rows.

## STEP 3 — Classify & map → write `questions.json`

**First, sync the master from the live Google Sheet** (the offline
`assets/chapter_topic_master.xlsx` is just a cache of it):
```
python scripts/sync_master.py     # refresh the taxonomy from the live sheet (safe every run)
```
It prints any subject added/removed and is a no-op when unchanged. **If it exits
non-zero** the sheet is unreachable or not shared — tell the user it must be
shared *Anyone with the link → Viewer*, then **carry on with the cached master**
(don't block). Then load the canonical vocabulary so you snap names to real
entries instead of inventing them:
```
python scripts/load_taxonomy.py --flat                 # all subjects
python scripts/load_taxonomy.py --flat --subject "Network"   # one subject
```
This prints `Subject > Chapter > Topic` lines — choose from these.

Then classify each question into the seven fields and write a flat
`questions.json` in the workspace:

```json
{
  "set_name": "Mock-01",
  "questions": [
    {
      "number":     459,
      "subject":    "Network Theory",
      "chapter":    "Network Theorems",
      "topic":      "Maximum Power Transfer",
      "difficulty": 2,
      "marks":      1,
      "type":       "Numerical MCQ"
    }
  ]
}
```

The classification rules — difficulty 1/2/3, the six-way type split, how to snap
names, what to do when the upload already has tags, and when to ask about marks —
live in **`references/classification_rules.md`**. Read it before you classify your
first set; it's the substance of the judgement calls.

**Applying the GATE marks benchmark (when marks aren't on the questions).** For a
GATE set, read the subject's benchmark in `references/marks_benchmarks/` and set
each question's `marks` to **1 or 2** by it: marks track *solving effort*, not
answer format (a NAT can be 1 or 2; an MCQ can be 1 or 2). One concept applied
once / pure recall → 1; a chain of steps, a concept intersection, a derivation, a
locus, or a linked-answer item → 2. Use the chapter base-rates only as a
tie-breaker. Crucially, **difficulty and marks must agree** under the benchmark's
calibration: a 1-mark item is difficulty 1–2, a 2-mark item is difficulty 2–3 —
never tag a 2-mark question as Easy. The benchmark spells this out per subject.

Snap `subject` / `chapter` / `topic` to the master names **verbatim** (the lookup
is case/space-tolerant but the words must match). If a question genuinely doesn't
fit any master entry, write your best canonical guess and let Step 4 report it as
unmapped — never invent a chapter or topic just to fill a cell.

## STEP 4 — Build the Excel & report

Run the deterministic builder (never hand-build the .xlsx):
```
python scripts/build_metadata_xlsx.py "~/Desktop/Question Metadata/_workspace/questions.json" "~/Desktop/Question Metadata/<Set name> Metadata.xlsx"
```
Add `--taxonomy "<path>"` if the user gave a newer master. The builder writes the
exact 7 headers, a styled frozen header row, one row per question, looks up the
chapter & type numbers, prints the **difficulty spread**, and prints **every row
whose subject/chapter/topic didn't fully map** (chapter/type left blank).

Then report back to the user, plainly:
- N questions written, and the file path.
- The difficulty spread (how many 1 / 2 / 3).
- Any unmapped rows — surface them so the user can fix the tag or extend the
  master. Don't bury this; a blank number with an honest report is the correct
  outcome, a confidently wrong number is not.

If there are unmapped rows the user wants to keep clean, offer to either re-tag
them to a closer master entry or, if the topic is genuinely missing, note it as a
candidate addition to the master (the same `chapter_topic_master.xlsx` shared
across the ExamDost skills).

---

## Bundled resources

- `scripts/extract_text.py` — pull readable text from .docx/.pdf/.xlsx/.csv/.txt.
- `scripts/load_taxonomy.py` — parse the master into canonical
  `Subject > Chapter > Topic` names + chapter/type numbers (`--flat`, `--subject`).
- `scripts/build_metadata_xlsx.py` — write the styled 7-column sheet, map the
  numbers, report the difficulty spread and unmapped rows.
- `scripts/derive_marks_benchmark.py` — mine a PYQ doc for an exam's 1-vs-2-mark
  pattern (used in Step 1b to build a new subject's marks benchmark).
- `assets/chapter_topic_master.xlsx` — the bundled ExamDost "Type List Master
  Sheet" (one worksheet per subject: `Chapter No. | Chapter Name | Type No |
  Type Name`). The user can pass a newer one with `--taxonomy`.
- `references/classification_rules.md` — the per-field judgement rules.
- `references/marks_benchmarks/<subject>_<exam>.md` — per-subject GATE marks
  benchmarks (1-vs-2-mark signals, chapter priors, difficulty calibration). Ships
  with `network_analysis_gate.md`; grows as you build more.
- `scripts/requirements.txt` — `openpyxl`, `python-docx`, `pdfplumber`/`PyMuPDF`.

This skill shares its taxonomy and tagging logic with **paper-generator**
(Skill-02), which produces the same sheet for questions it generates. Here you do
the same thing for questions that already exist, whatever format they arrive in.
