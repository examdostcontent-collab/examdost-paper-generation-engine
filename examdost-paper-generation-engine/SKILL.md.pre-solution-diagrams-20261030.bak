---
name: examdost-paper-generation-engine
description: ExamDost end-to-end question pipeline — one skill with THREE modes the user picks at the start. (1) GENERATE — ingest a Skill-01 Exam Master Blueprint and mass-produce accurate, non-repeating practice questions / full mock tests with answer keys, rich 4-step solutions, self-verification, and branded .docx/.pdf/boxed-docx/metadata outputs ("make a GATE mock", "generate N questions for <topic>", "build a paper/mock from this blueprint"). (2) TAG — turn any existing question set (.docx/.pdf/.xlsx/.csv/.txt/pasted/paper.json) into the "Mock-01 Metadata"-style 7-column classification Excel mapped to the master taxonomy ("tag/classify these questions", "metadata sheet", "per-question difficulty/type/chapter Excel"). (3) CODE — stamp question CODES into the OTS ID cell and RENUMBER questions inside already-built Boxed .docx / .tex papers from a coding/mapping sheet ("put the codes into the OTS ID", "apply the coding sheet", "update the question numbers from the excel"). USE THIS whenever the user wants to generate questions/mocks, build a question-metadata/tagging spreadsheet, or apply a code/number map to existing papers. If the user doesn't say which, ASK them which of the three jobs they want. Do NOT use for: ANALYSING papers for weightage / exam DNA / PYQ trends (that is exam-psychometrician / Skill-01, which produces the blueprint this skill consumes); reviewing/grading a LECTURE .pptx (teaching-assistant); rebuilding last year's lecture deck (content-studio); a mentoring transcript → student plan (student-blueprint); or converting Word equations to LaTeX (word-to-latex).
---

# Examdost Paper Generation Engine

A single skill that covers the three downstream jobs of the ExamDost question
pipeline. It is a **router**: at the start you pick (or the user tells you) which
of the three modes to run, then you read that mode's workflow file and execute it
end to end. The modes share one master taxonomy and one set of scripts.

| Mode | What it does | Read this file |
|------|--------------|----------------|
| **GENERATE** | Blueprint → fresh, verified questions / full mock + 4 branded files (Rich Word · PDF · Boxed Word · Metadata Excel) + exclusion log | `references/mode_generate.md` |
| **TAG** | Any existing question set → the 7-column "Mock-01 Metadata" classification Excel, snapped to the master taxonomy | `references/mode_metadata.md` |
| **CODE** | A coding/mapping sheet → stamp Codes into OTS ID + renumber questions inside existing Boxed `.docx` / `.tex` papers, in place, with an audit | `references/mode_code_update.md` |

---

## STEP 0 — Route the request (do this first, every time)

**If the user already made the job clear, skip the question and go.** Detect from
what they sent:

- A **Master Blueprint** (`.xlsx` from Skill-01) and/or "generate / make a mock /
  N questions / build a paper" → **GENERATE**.
- A **question set** (paper, mock, bank, PYQ in any format) plus "tag / classify /
  metadata / per-question Excel" → **TAG**.
- A **coding/mapping sheet** (columns like Question number, Code, a test column)
  **plus test paper(s)** and "put codes in OTS ID / apply the sheet / update the
  numbers" → **CODE**.

**If it's ambiguous or unspecified, ask once and HALT:**

```
This is the ExamDost Paper Generation Engine. Which job do you want?

  1. GENERATE — produce new questions / a full mock test from an Exam Master
     Blueprint (4 branded files + exclusion log).
  2. TAG — build the per-question Metadata classification Excel for a set of
     questions you already have.
  3. CODE — apply a coding sheet to existing papers: stamp the question Codes
     into the OTS ID cells and update the question numbers.

Reply 1, 2, or 3 (and attach the relevant file/blueprint/sheet).
```

Once the mode is known, **read the corresponding `references/mode_*.md` in full
and follow it exactly** — those files carry the complete, unabridged workflow
(intake gates, halts, verification, builders, and failure modes) for each job.
Don't paraphrase them from memory; open the file.

---

## Shared foundation (GENERATE and TAG)

Both the GENERATE and TAG modes tag against the **same canonical master taxonomy**
(`assets/chapter_topic_master.xlsx`), which is a cache of a live Google Sheet. At
the start of those two modes, refresh and load it:

```
python scripts/sync_master.py          # refresh the taxonomy cache (safe every run; no-op if unchanged)
python scripts/load_taxonomy.py --flat # the canonical Subject > Chapter > Topic vocabulary to snap names to
```

If `sync_master.py` exits non-zero, the sheet is unreachable or not shared — tell
the user it must be shared *Anyone with the link → Viewer*, then **carry on with
the cached master** (don't block). Aptitude questions are never tagged
`General Aptitude` (retired); GK never a generic "GK" — use the specific master
sheets (`Verbal Ability` / `Numerical Ability` / `Reasoning`, `General Awareness` /
`General Science`).

The **CODE** mode does **not** use the taxonomy — it only applies a map the user
already has, so it skips this step.

---

## Setup

`pip install -r scripts/requirements.txt` (covers all three modes: python-docx,
openpyxl, pandas, reportlab, python-pptx, pdfplumber/PyMuPDF, pypandoc_binary).
Running `python`/`pip` is pre-authorised here, so scripts run without prompts.

## What's in this skill

- `references/mode_generate.md` · `references/mode_metadata.md` ·
  `references/mode_code_update.md` — the three full workflows.
- `references/` also holds the GENERATE deep-dives (`blueprint_intake.md`,
  `question_architecture.md`, `verification_rubric.md`, `paper_spec_schema.md`,
  `exclusion_log.md`), the TAG rules (`classification_rules.md`,
  `marks_benchmarks/`), and the CODE formats (`latex_formats.md`).
- `scripts/` — the consolidated engine for all three modes (generation builders &
  validator, taxonomy + metadata tooling, the code-injection engines).
- `assets/chapter_topic_master.xlsx` + `master_source.json` — the shared taxonomy
  and its live-sheet sync config.
