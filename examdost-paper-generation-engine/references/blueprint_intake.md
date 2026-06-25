# Blueprint Intake — reading the 4-Part Master Blueprint

Skill-01 (exam-psychometrician) emits the **Exam Master Blueprint** as a 4-sheet
`.xlsx` (and a chat text block). Those four parts are your entire generation
contract. Read all four — generation quality is bounded by how completely you
ingest them.

| Part | Sheet | What it gives you | How you use it |
|------|-------|-------------------|----------------|
| **A** | Weightage Matrix | Per subject/chapter: question count, marks, weight %, difficulty (+1–5), format mix. | Drives the **Phase-2 distribution** — how many questions per subject/chapter for the requested scope. |
| **B** | Exam DNA Profile | **Macro** (theory:numerical ratio, 1- vs 2-mark split, format mix, difficulty/time, cut-off calibration) + **Micro** per-subject (trap_logic, variable_types, calculation_steps, archetypes). | The **soul** of generation. Pull each subject's traps and number style from its **micro** row — never a paper-wide average. |
| **C** | Structural Template | `sections`, `question_matrix` (1- vs 2-mark per section), `format_matrix` (MCQ/MSQ/NAT/AR/Statement per segment), `hard_constraints`. | The **shape** every paper must obey. Reconcile your format split to it; obey every hard constraint exactly. |
| **D** | Generation Spec (Archetype Bank) | Per archetype: parameterized `template` with `{slots}`, `solution_path`, `distractor_rules`, `numeric_profile`, `phrasing_pattern`, format/difficulty/expected-count, and 2–3 **verbatim seed questions**. | Your **working material**. Instantiate templates with fresh values, build options from the distractor rules, and few-shot the examiner's voice from the seeds. |

## Two intake paths

### A. The `.xlsx` (preferred)
Run:
```
python scripts/parse_blueprint.py "<blueprint.xlsx>" "<workspace>/blueprint.json"
```
It maps the four sheets by name (case/spacing-tolerant) into one JSON:
`{ "meta", "weightage_matrix", "exam_dna": {macro, micro}, "structural_template", "generation_spec": {archetypes} }`.
It prints a coverage summary (which parts were found, row counts). If a sheet is
missing it leaves that key empty and warns — don't silently proceed as if it were there.

### B. Pasted text
If the user pastes the blueprint, parse the four parts from the markdown
yourself. Extract the same structure mentally; you don't need the JSON file, but
do confirm back to the user the subject list + the structural totals you read,
so a mis-paste is caught before generation.

## Using the parts together (the generation recipe)

1. **Quantity** comes from Part A + the scope: scale each subject/chapter's share
   to the requested number of questions, preserving relative weight.
2. **Shape** comes from Part C: split those questions into 1-/2-mark and into
   MCQ/MSQ/NAT/etc. per the format matrix; never violate a hard constraint
   (e.g. "General Aptitude never contains NATs").
3. **Texture** comes from Part B micro: for each question, apply *that subject's*
   trap logic, variable style, and calculation depth.
4. **Voice & options** come from Part D: instantiate the matching archetype's
   template with new numbers, write distractors from its distractor rules, and
   match the seed questions' phrasing — **without reproducing any seed verbatim**.

## Guard rails
- **Seeds are few-shot fuel, not output.** Never emit a seed question (or a logged
  question) as a generated item. Re-parameterize: new scenario, new numbers, new framing.
- **Canonical names are fixed.** Use the exact subject/chapter/topic names from the
  blueprint in every question's metadata and fingerprint — they must line up across runs.
- **Missing parts.** If Part C is absent you don't know the structure — ask the user
  for the section/mark/format breakdown rather than guessing. If Part D is thin for a
  subject, lean harder on Part B micro + the Part A format mix, and say confidence is lower there.
- **Cut-off calibration.** If Part B macro flags a high cut-off / zero-margin profile,
  bias toward accuracy-trap items (clean-looking questions with a precise distractor) over
  long multi-step grinds — that's what the real pressure looks like.
