# Question Architecture — the mandatory shape of every item

Every generated question is one object in `paper.json` (schema:
`paper_spec_schema.md`) and renders to the **ExamDost rich solution standard**. This
file is the quality bar for *what goes inside* each field.

## The mandatory parts (rich solution standard)

```
Q[N]. <full question text + any [GEMINI_FLASH_PROMPT: ...] diagram tags>
      <metadata line, only the tags the user asked for: Subject | Chapter | Topic | Marks | Type>
Answer Key: <letter(s) / NAT value or range>
Detailed Solution
  1. Core Concept & Formula
       • concept   — 2–4 sentences of PLAIN-ENGLISH teaching of the principle.
       • formula   — the governing equation(s), as real math (rendered natively).
       • Where:    — a glossary defining EVERY symbol used, with units.
  2. Calculation Steps        (numeric)      OR      Evaluating the Options (conceptual)
       numeric:  identify givens → substitute → simplify, line by line.
       options:  analyse EACH option A–D — why right, and the exact trap each wrong one encodes.
  Final Answer: <terminal value WITH units, or the chosen option restated>.
```

Maps to the `solution` object: `concept`, `formula[]`, `where[]`, then
`calculation[]` (numeric) **or** `option_analysis[]` (conceptual), and `final_answer`
(+ `check` for NATs). Full field spec: `paper_spec_schema.md`.

**Teach, don't just answer.** The Core Concept is the differentiator — explain *why*,
the way the reference solutions do ("the fault current is limited solely by the
machine's sub-transient reactance"), not just "use this formula". The glossary and the
per-option trap analysis are what make it ExamDost-grade.

**Concept = plain English.** Keep `concept` to 2–4 readable sentences; the equation
lives in `formula` (not stuffed into the concept sentence). Naming a symbol in passing
is fine.

**Calculation vs Options — pick by question type.** Numeric items get `calculation`;
conceptual / recall MCQs get `option_analysis` (every option addressed). A genuinely
deep numeric MCQ may carry both. Don't give a recall MCQ a bare one-line solution —
walk the options.

## Cognitive-load split (the most important fidelity rule)

| | 1-mark | 2-mark |
|---|--------|--------|
| **Concept** | single concept, direct recall or one relationship | conceptual **intersection** of 2+ ideas |
| **Steps** | 1–2 steps | multi-step derivation |
| **Trap** | at most a light distractor | a **deep** psychological trap or an edge-case exception |
| **Feel** | "do you know it / can you apply it once" | "can you chain it under pressure without falling for the trap" |

A 2-mark question that is just a 1-mark question with bigger numbers is a
**failed** 2-mark question. Add a genuine second concept or a real trap.

## Difficulty by design — never by tedium

Manufacture difficulty through, in order of preference:
1. **Conceptual edge-case** — a case where the naive rule breaks and an exception applies.
2. **Visual misdirection** — a diagram drawn so the obvious reading is wrong (state this in the `[GEMINI_FLASH_PROMPT]`).
3. **Non-standard variable names** — force understanding, not pattern-matching on symbols.
4. **Conceptual intersection** — two subtopics that must be combined.

Never: ugly decimals, deliberately heavy hand-arithmetic, or "gotcha" wording
that tests reading speed instead of the concept.

## Distractor engineering (MCQ / MSQ)

Each wrong option must catch a **specific, nameable** student error — drive these
from Part B trap_logic and the matching Part D distractor_rules. Typical recipes:
- the answer with one law mis-applied (peak vs RMS ×√2, forgot a √3, dropped a load² scaling);
- the reciprocal / the complement / off-by-a-factor;
- the adjacent-concept swap (iron vs copper loss, PT vs CT, stator vs rotor);
- the right method on the wrong given.

Verify (in the verification pass) that **exactly one** option is defensible for an
MCQ. For MSQ, be explicit about how many are correct and ensure each "correct" one
truly is.

## NAT conventions
- Give an **answer range with tolerance** for any non-integer result (e.g. `"3.8 to 4.2"`),
  matching how the real exam marks NAT. Integers can be exact.
- State units in Step 4 even though the NAT box itself is unitless.
- Keep the numeric profile clean per Part D (`numeric_profile`) — difficulty is conceptual, not arithmetic.
- **Always include a `solution.check`** arithmetic expression that computes the answer
  (e.g. `"(1500-1440)/1500*100"`). The validator *executes* it and fails the paper if the
  result falls outside your keyed band — this is what catches a wrong answer key
  mechanically, rather than trusting a re-read. See `paper_spec_schema.md`.

## Math notation
Write equations in the light markup (`\frac{a}{b}`, `\omega`, `x^2`, `V_{th}`, `\sqrt{}`,
`\leq` …) — the builders render it to clean Unicode so the paper reads like the real
exam. Full table + the JSON `\\` double-backslash rule are in `paper_spec_schema.md`.
Matrices / multi-line derivations / anything that won't render inline go in a
`[GEMINI_FLASH_PROMPT: ...]` tag.

## Assertion-Reason / Statement types
- Write a clear Assertion (A) and Reason (R); the answer letter encodes the standard
  verdict set ("both true, R explains A", "both true, R doesn't explain A", "A true R false", …).
  Render the exact option set the blueprint's exam uses.
- For Statement types, list the statements (I, II, …) and ask which are correct.

## Diagram tags
- Attach to the **question** via `diagram_prompts`, to the **solution** via
  `solution.solution_diagram_prompts`.
- Be precise and self-contained — the image tool sees only the bracket text:
  `[GEMINI_FLASH_PROMPT: Create a clean vector-style circuit diagram: a 10V DC source in series with R1=2Ω, feeding two parallel branches R2=4Ω and R3=4Ω; label nodes A and B across R3; white background, thin black strokes, no shading.]`
- Never describe a diagram in prose where a tag belongs, and never attempt to draw it.
- **Write only the diagram content** — a uniform style block (Segoe UI 11 pt, 1 pt line weight, crisp black-and-white high-contrast, legible/no-overlap, JPEG output) is **appended automatically** to every prompt by the builders (`paperlib.gemini_prompt`). Don't restate fonts/line-weight/output format in each prompt; just describe the circuit/graph and its labels.

## Wildcards (GATE, 10% of volume)
- Blend **two distinct subjects'** core concepts in one item (e.g. a control-systems
  stability question whose plant is an electrical-machine transfer function).
- Set `is_wildcard: true`. Still obey the cognitive-load rule for its mark value.

## Non-repetition (per item)
**Reusing a concept is fine; reusing the exact numbers is not.** Before finalising a
numeric question, make sure its exact dataset (the *value signature* — the set of numbers
in the stem + given) isn't already in the Exclusion Log or another item in this paper for
the same subject/topic/type. If it is, **change the numbers/configuration** (you can keep
the concept). `validate_paper.py` enforces this mechanically. See `exclusion_log.md`.

## Variation axes (so a mock series isn't the same paper twice)
Value-dedup stops number repeats; these axes stop *archetype* repeats. The subject
weightage stays fixed (it mirrors the exam), but **within it** each new mock must move.
Run `scripts/coverage_report.py` to see where, then vary along these axes:

1. **Syllabus rotation (the biggest lever).** Cover the FULL type list, not the 4–5
   high-yield archetypes. A subject with 30 in-syllabus types but only ~15 ever tested
   means half the syllabus is unseen — rotate the new mock into the unused types first.
2. **Given ↔ unknown swap.** From the same relation, ask for a different quantity
   (e.g. slip→speed becomes speed→poles, or efficiency→losses becomes losses→efficiency).
3. **Sub-case / configuration.** Star vs delta, lap vs wave, short vs medium line,
   series vs parallel, single-phase vs three-phase, with/without an edge condition.
4. **Framing.** Direct compute · reverse (find the input) · "which is NOT / least / always" ·
   match-the-columns · assertion-reason · statement-correctness · compare-two-options.
5. **Difficulty tier.** Same topic as a 1 (recall), a 2 (one-step apply), or a 3
   (multi-step / two-concept / edge-case). Spread these; keep a small curveball quota.
6. **Numeric spread.** Sample the topic's realistic range, not one canonical setup.

Rule of thumb: if a question could be matched to a prior-mock question by "same archetype,
just different numbers," it has failed the variation test — change at least two axes above.
