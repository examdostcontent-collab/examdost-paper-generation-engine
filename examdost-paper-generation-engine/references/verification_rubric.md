# Verification — three layers, mandatory before any file is built

A question generator that emits a **wrong answer key** is worse than none — it
destroys student trust and poisons the doubt-resolution pipeline. Verification has
**three layers**, and *all* must pass before Phase 4 builds anything:

0. **Independent blind re-solve audit (answer-accuracy guarantee — every question, every type).**
   Re-solve **every** question from the **stem alone, without looking at the keyed answer
   or the written solution** (ideally a separate pass / fresh subagent, so there is no
   anchoring to the key), then compare the independently-derived answer to the key — they
   must agree. This is the **only** layer that can validate the key of a **conceptual /
   theory MCQ, Statement-type, or Assertion-Reason** item, which the deterministic gate
   cannot evaluate. Requirements: **100% coverage (no sampling)**; on any mismatch
   **quarantine and regenerate** (or correct the key if the audit shows the distractor
   logic was wrong) and **re-audit the replacement**; flag any item with two defensible
   answers, an ambiguous stem, or an **unverifiable factual / current-affairs claim**
   (especially GK/GS — confirm against the last-6-months / static-truth standard) as a
   FAIL. Accuracy means "the premise is true **and** the key matches", not just the latter.
   **Blind-audit agreement must reach 100% before the deterministic gate is run.**

1. **Deterministic gate — `validate_paper.py` (code, not judgment).**
   ```
   python scripts/validate_paper.py paper.json "<exclusion_log.csv>"
   ```
   It exits non-zero (RESULT: FAIL) on any ERROR and you must fix/regenerate until it
   passes. It catches what an LLM re-read misses: it **executes** every NAT's
   `solution.check` expression and fails if the computed value is outside the keyed
   band (real code-verified arithmetic — this is how a wrong key gets caught); it
   confirms counts vs `meta`/`target_distribution`, MCQ answer letters exist among the
   options, NAT answers are numeric, `answer` reconciles with `final_answer`, all four
   solution steps are present, `structural_constraints` are obeyed, **tags snap to the
   canonical master taxonomy** (non-canonical subject = ERROR; chapter/topic drift =
   WARNING), and there are **no exact-value repeats** (within the paper or vs the log).
   WARNINGS don't block but must be reviewed (e.g. "NAT has no solution.check — arithmetic
   not code-verified"; "topic not canonical — snap or flag as a candidate addition").

2. **Model self-review (the checklist below).** The gate can't judge whether a
   distractor is conceptually defensible or a stem is unambiguous — you do that. Run it
   as a distinct step, with fresh eyes, *after* drafting a batch and *before* the gate.

So every NAT should carry a `solution.check`; without it the arithmetic is only
self-reviewed, never code-verified.

## The mindset
Re-solve each question **from scratch**, as if you were the student — do not just
re-read your own solution and nod. Then reconcile your independent answer with the
keyed answer. If they differ, the question (not your re-solve) is suspect until proven.

## Per-question checklist

For **every** question, confirm:

1. **Answer correctness.** Independently re-derive the answer. It must equal both
   the `answer` field **and** the `solution.final_answer` (Step 4). All three agree.
2. **Solution integrity (rich format).** *Core Concept* genuinely explains the
   principle (not just names it); *formula* is correct and every symbol appears in the
   *Where:* glossary with units; *Calculation Steps* show every line and end in correct
   units; *Final Answer* agrees with the key.
3. **Option analysis (conceptual MCQ).** `option_analysis` addresses **every** option;
   exactly one is marked `correct` and it matches the answer key; each wrong option's
   text names the real misconception/trap. (For numeric MCQs, the worked calculation
   stands in for this, but no two options may be defensible.)
4. **MSQ correctness.** Every option marked correct is genuinely correct; every other
   is genuinely wrong; the count is unambiguous.
5. **NAT band.** The value (or range) is right, and the tolerance band is sensible
   for the precision implied. Units stated in Step 4.
6. **Cognitive load.** 1-mark = ≤2 steps / single concept; 2-mark = multi-step or a
   real conceptual intersection / deep trap. Demote or enrich if mismatched.
7. **Structural fidelity.** Type and marks are allowed by Part C; no hard constraint
   is violated (e.g. NAT where the section forbids it).
8. **Non-repetition.** The fingerprint collides with neither the Exclusion Log nor any
   other item in this paper (same framework + same dataset = collision).
9. **Diagram tags.** Any visual is a `[GEMINI_FLASH_PROMPT: ...]` tag (not prose, not
   an attempt to draw); the tag is self-contained.
10. **Canonical naming.** subject/chapter/topic match the blueprint verbatim.

## What to do with a failure
- **Fixable** (units missing, a skipped algebra line, a loose tolerance, a weak
  distractor): fix in place.
- **Answer-key wrong, or two defensible options, or a duplicate**: **regenerate the
  whole question.** Never patch a fundamentally broken item — replace it. Re-run the
  checklist on the replacement.

## Report
After the pass, state the outcome in one line, e.g.:
> Verification: 65/65 questions verified. Fixed 4 (units/tolerance); regenerated 3
> (2 answer-key conflicts, 1 duplicate of the exclusion log).

Only after the pass reports clean do you build the files in Phase 4.

## Scope note
This skill is configured for a **full mandatory pass** (every question, including
1-mark MCQs). If a run is explicitly set to "light spot-check", verify only NAT and
all 2-mark items and say so in the report — but the default is full.
