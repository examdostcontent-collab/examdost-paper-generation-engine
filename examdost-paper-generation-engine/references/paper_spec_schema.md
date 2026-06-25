# `paper.json` — the generation spec every builder reads

One structured file describes a whole generated paper. All three builders
(`build_paper_docx.py`, `build_paper_pdf.py`, `build_paper_pptx.py`) and
`update_exclusion_log.py` read this shape. Keep it in the run's `_workspace/`
and grow it batch by batch during Phase 3.

```json
{
  "meta": {
    "exam": "GATE EE",
    "paper_title": "GATE EE — Full-Length Predictive Mock 01",
    "total_questions": 65,
    "total_marks": 100,
    "duration_min": 180,
    "generated_on": "2026-06-05",
    "organising_institute": "IIT Roorkee",
    "instructions": [
      "All questions are compulsory unless stated otherwise.",
      "1-mark MCQs: -1/3 negative marking. 2-mark MCQs: -2/3. No negative marking on NAT/MSQ."
    ],
    "metadata_tags": ["Subject", "Chapter", "Marks", "Type"],
    "layout": "split",
    "show_solutions": true
  },

  "sections": [
    {
      "section": "General Aptitude",
      "questions": [ /* question objects, in display order */ ]
    },
    {
      "section": "Technical",
      "questions": [ /* ... */ ]
    }
  ]
}
```

## `meta` fields

| field | meaning |
|-------|---------|
| `exam` | canonical exam name (drives the output folder + headers). |
| `paper_title` | shown on the cover/first page. |
| `total_questions`, `total_marks`, `duration_min` | header summary; should reconcile with the sections. |
| `organising_institute` | optional; set when the Institute Anchor applies. |
| `instructions` | list of strings → rendered as the instructions block. |
| `metadata_tags` | **Deprecated / ignored.** Per-question classification is no longer printed inline — it is delivered as the separate **Question Metadata Excel** (`build_metadata_xlsx.py`). The doc/PDF/PPTX builders no longer render an inline tag line. |
| `layout` | `"combined"` = answer key + concept + solution printed under each question. `"split"` = a clean question paper first, then a separate "Answer Key & Solutions" section. **Set from the Phase-2 answer.** |
| `show_solutions` | `true` normally. `false` prints questions + a compact answer key only (no worked solutions) — for a pure question paper. |
| `expected_wildcard_pct` | optional. The wildcard target (e.g. `10` for GATE). `validate_paper.py` warns if the actual share drifts >3 points. |
| `target_distribution` | optional but recommended — the **Phase-2 locked matrix**, so the validator can confirm the paper matches it. `{"subjects": {"Electrical Machines": 12, ...}, "marks": {"1": 35, "2": 30}, "formats": {"MCQ": 40, "NAT": 20, "MSQ": 5}}`. Any present sub-key is enforced as a hard count. |
| `structural_constraints` | optional — machine-checkable Part C hard-constraints, e.g. `[{"section": "General Aptitude", "forbid_types": ["NAT", "MSQ"]}]`. The validator errors on any violation. Populate from Part C when a constraint is mechanizable. |

## Question object

```json
{
  "number": 12,
  "text": "A 3-phase, 50 Hz induction motor runs at 1440 rpm on a 4-pole stator. The slip is ______ %.",
  "type": "NAT",
  "marks": 1,
  "options": [],
  "subject": "Electrical Machines",
  "chapter": "Induction Machines",
  "topic": "Slip and Speed",
  "is_wildcard": false,
  "diagram_prompts": [],
  "answer": "3.8 to 4.2",
  "solution": {
    "concept": "When a 3-phase induction motor runs, the rotor turns slightly slower than the stator's rotating field; slip measures that fractional lag and drives the rotor EMF and torque.",
    "formula": ["N_s = \\frac{120 f}{P}", "s = \\frac{N_s - N_r}{N_s} \\times 100"],
    "where": [
      {"sym": "N_s", "def": "synchronous (field) speed", "unit": "rpm"},
      {"sym": "N_r", "def": "rotor speed", "unit": "rpm"},
      {"sym": "s",   "def": "slip", "unit": "%"}
    ],
    "calculation": [
      "Identify the given values: f = 50 Hz, P = 4, N_r = 1440 rpm.",
      "N_s = \\frac{120 \\times 50}{4} = 1500 rpm",
      "s = \\frac{1500 - 1440}{1500} \\times 100 = 4.0"
    ],
    "final_answer": "Slip s = 4.0 %",
    "check": ["120*50/4", "(1500-1440)/1500*100"],
    "solution_diagram_prompts": []
  },
  "fingerprint": "Electrical Machines_Induction Machines_NAT_slip from Ns & Nr (4-pole, 50Hz)"
}
```

### The solution object (the ExamDost rich format)
This is the **preferred** structure — it renders as *Detailed Solution → 1. Core Concept & Formula → 2. Calculation Steps / Evaluating the Options → Final Answer*.

| field | meaning |
|-------|---------|
| `concept` | 2–4 sentence **plain-English** explanation of the principle (teach it). May name a symbol in passing, but the equation lives in `formula`. *(Replaces the old top-level `concept` line.)* |
| `formula` | list of governing equation(s) in LaTeX-style markup; each renders as a native, display equation. |
| `where` | the **glossary** — one entry per symbol: `{"sym": "N_s", "def": "synchronous speed", "unit": "rpm"}`. `unit` optional. `sym` is LaTeX-style and renders as an equation. |
| `calculation` | **numeric path** — ordered lines: identify givens, substitute, simplify. A line may be prose, an equation, or prose+inline-equation (e.g. `"N_s = \\frac{120 \\times 50}{4} = 1500 rpm"`). |
| `option_analysis` | **conceptual path** — one entry per option: `{"option": "A", "correct": false, "text": "why this is right/wrong + the trap"}`. The `correct: true` option(s) must match the answer key. |
| `final_answer` | terminal value with units, or the chosen option restated. |
| `check` | NAT only — arithmetic expression(s) executed by the validator (unchanged). |

Provide **`calculation` for numeric** items and **`option_analysis` for conceptual/recall MCQs** (a deep numeric MCQ may carry both). The validator requires either one plus a `final_answer`.

> **Legacy form still supported:** a solution with `given`/`formula`/`calculation`/`final_answer` (no `concept`/`where`/`option_analysis`) renders as the older 4-step block. New papers should use the rich form above.

### Field rules
- `type` ∈ `MCQ` · `MSQ` · `NAT` · `Assertion-Reason` · `Statement`. Drives how the answer renders.
- `options`: list of full option strings **including the leader** (`"(A) 1500 rpm"`). Empty `[]` for NAT. For MSQ, more than one may be correct.
- `answer`:
  - MCQ → a single letter, e.g. `"B"`.
  - MSQ → comma-separated letters, e.g. `"B, D"`.
  - NAT → an exact value `"4.0"` **or a range** `"3.8 to 4.2"` (always give a tolerance band for non-integer NATs).
  - Assertion-Reason/Statement → the option letter that captures the correct verdict.
- `marks`: `1` or `2` (or the exam's bands). Governs cognitive load — see `question_architecture.md`.
- `difficulty`: **`1` (Easy) / `2` (Moderate) / `3` (Difficult)** — assign per question from its cognitive load, matching the blueprint's difficulty profile. Drives the metadata Excel's *difficulty index*.
- `type_detail` *(MCQ only, optional)*: `"theory"` or `"numerical"` — splits MCQ into TheoryMCQ vs Numerical MCQ in the metadata Excel. If omitted, it's inferred (a `calculation`-based MCQ → Numerical MCQ; a conceptual `option_analysis` MCQ → TheoryMCQ).
- `subject` / `chapter` / `topic`: **verbatim canonical names from the Chapter & Topic master sheet** (`scripts/load_taxonomy.py` / `assets/chapter_topic_master.xlsx`) — the same vocabulary Skill-01 uses. `validate_paper.py` errors on a non-canonical subject and warns on non-canonical chapter/topic. General Aptitude is the subject `General Aptitude` with the area (Grammar/Analogy/Numbers/…) as the chapter. If a real topic isn't in the master, keep a clear tag and flag it as a candidate addition rather than inventing a canonical name. Don't paraphrase — fingerprints must line up across runs.
- `is_wildcard`: `true` for the 10% cross-subject lateral-thinking items. Wildcards render with a small "WILDCARD" badge.
- `diagram_prompts`: list of `"[GEMINI_FLASH_PROMPT: ...]"` strings attached to the **question** (rendered as placeholder boxes).
- `concept`: a ≤3-line **plain-English** explanation — **no formulas/symbols/subscripts/equations** (those go in `solution.formula`). The validator warns on math markup here.
- `solution.calculation`: list of strings, one per line — **never skip intermediate steps.**
- `solution.check`: **(NAT — strongly recommended)** a pure-arithmetic expression (or list of them; the last is the result) that **computes the answer**, e.g. `"(1500-1440)/1500*100"` or `["120*50/4", "(1500-1440)/1500*100"]`. `validate_paper.py` actually **executes** it (safe eval: `+ - * / ** %`, parentheses, and `sqrt sin cos tan log log10 exp abs radians degrees pi e` …) and ERRORS if the result lands outside the keyed `answer` band. This is the only genuinely code-verified arithmetic — include it for every numeric NAT. Use `pi`, `sqrt(3)`, etc.; no variable names.
- `solution.solution_diagram_prompts`: optional `[GEMINI_FLASH_PROMPT: ...]` for a final phasor/graph aid in the solution.
- `fingerprint`: the exclusion string `Subject_Chapter/Topic_Type_CoreVars/Concept` (see `exclusion_log.md`). Every question must carry one.

## Math notation (the light markup the builders render to Unicode)

Write math in `text`, `options`, `concept`, and `solution.*` using this constrained
markup — `paperlib.render_math` converts it to clean Unicode in all three formats
(so `\frac{N_s - N_r}{N_s}` reads like a real exam, not like code):

| You write | Renders | You write | Renders |
|-----------|---------|-----------|---------|
| `\omega \pi \theta \Omega \Delta` | ω π θ Ω Δ | `\times \cdot \div \pm` | × · ÷ ± |
| `\leq \geq \neq \approx \infty` | ≤ ≥ ≠ ≈ ∞ | `\int \sum \sqrt{x}` | ∫ ∑ √(x) |
| `x^2`, `x^{n+1}` | x², xⁿ⁺¹ | `V_{th}`, `I_2`, `P_o` | Vₜₕ, I₂, Pₒ |
| `\frac{a}{b}` | (a)/(b) | `\rightarrow -> \Rightarrow` | → → ⇒ |

Rules: **letter subscripts must be braced** (`R_{th}`, not `R_th`); bare works for a
single digit or single trailing letter (`I_2`, `P_o`). `\frac` may contain braced
sub/superscripts. Anything that won't render cleanly in inline Unicode (matrices,
multi-line derivations, complex diagrams) belongs in a `[GEMINI_FLASH_PROMPT: ...]` tag.

> ⚠️ **JSON escaping footgun:** a backslash command inside JSON must be written with a
> **double** backslash — `"\\frac{a}{b}"`, `"\\omega"`, `"2\\pi f"`. A single backslash
> (`"\frac"`) is an *invalid JSON escape* and the file won't parse. (If you hand-write
> `paper.json`, double every backslash; programmatic dumps via `json.dump` handle it.)

**Word output uses native equations.** When pandoc is available (`pypandoc_binary`), the
`.docx` builder renders this markup as **real, editable Word equations (OMML)** — stacked
fractions, radicals with vinculum, proper sub/superscripts. `solution.formula` lines are
treated as whole equations; inline `\frac`/`\sqrt`/`x^2`/`V_{th}` spans in stems, options,
concept and calculation are converted in place. Without pandoc it falls back to inline
Unicode. (PDF/PPTX use the Unicode rendering — OMML is a Word-only format.)

## Notes for the builders
- Questions render in array order; `number` is printed verbatim (keep it continuous across sections, or restart per section — your choice, just be consistent).
- A missing `solution` (or `show_solutions: false`) → that question prints with answer key only.
- Output filenames are auto-sanitised (`paperlib.safe_output_path`) so an exam name with `:` `/` `?` etc. won't break the path on Windows.
