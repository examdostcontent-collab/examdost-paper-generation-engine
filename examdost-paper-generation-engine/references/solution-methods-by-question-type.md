# Solution Methods by Question Type

Use this guide after the question is correct but before writing its final solution.
The GATE Test Series shows that `MCQ`, `MSQ`, and `NAT` are only answer-input formats;
they are not sufficient solution methods. Route every item twice:

1. **Input format:** MCQ, MSQ, NAT, Statement, Assertion-Reason, Match/Table, or linked item.
2. **Reasoning archetype:** recall/concept, numerical application, multi-stage derivation,
   diagram interpretation, transient/state change, geometry/region, transformation or
   equivalent model, proof/counterexample, or data/table interpretation.

Write the solution using both routes. For example, a numerical MCQ should be solved as a
numerical problem first and matched to an option only at the end; a conceptual MSQ must
test every statement independently rather than searching for a single best choice.

## Universal solution spine

Every full solution should make these moves visible, omitting only genuinely unnecessary
ones:

1. **Identify the task and givens.** State what is known, required, and constrained.
2. **Core concept.** Explain why the governing law/test applies here.
3. **Model or representation.** Write the equation, truth condition, matrix, region,
   equivalent circuit, state table, or other representation.
4. **Execute in auditable steps.** One logical or algebraic move per line. Show the
   intermediate quantity that justifies the next move.
5. **Decision.** Match the result to the option(s), NAT band, statement verdict, or map.
6. **Verification.** Use units, sign, limiting case, substitution-back, conservation,
   determinant/trace identity, total probability/area, or another independent check.
7. **Exam insight.** Name the shortest safe route or the specific trap only when it is
   useful and question-specific.

Do not pad a one-step question into seven artificial headings. Preserve the logic, not a
fixed word count.

## MCQ

### Conceptual or recall MCQ

- State the governing fact in plain English and its condition of validity.
- Evaluate **every option**, not only the keyed one. Say why the correct option satisfies
  the rule and name the misconception or missing condition in each wrong option.
- If two options look similar, identify the exact discriminating word, sign, direction,
  domain, or assumption.
- End by restating the selected option, not merely its letter.

### Numerical MCQ

- Solve from the stem without looking at the options first; options must not anchor the
  method.
- Show givens with units, governing equation, substitution, simplification and units.
- Match the independently obtained result to the option only at the end.
- Briefly explain a distractor only when it corresponds to a real likely error (RMS vs
  peak, line vs phase, sign, missing square/root, wrong base, early rounding, etc.).
- If no option matches, recheck assumptions and arithmetic; never bend the derivation to
  force a listed option.

## MSQ

- Treat each statement/option as an independent true/false claim. Do not assume only one
  must be correct or that options are mutually exclusive.
- Build an internal truth vector such as `A=T, B=F, C=T, D=F` after checking each item
  against the governing definition, equation, counterexample, or calculation.
- For dependent statements, establish the base result once and reuse it explicitly; do
  not repeat a long derivation four times.
- State why every rejected option fails. A single counterexample is sufficient to reject
  an absolute claim such as "always" or "for all".
- End with the complete selected set and confirm it matches the answer field exactly.

## NAT

- Derive the value independently; there are no options to provide scale or sign hints.
- Carry adequate precision until the end and show the requested rounding or tolerance.
- Put only a plain number or `minimum to maximum` in the platform answer field; keep units
  and explanatory text in the solution.
- For a non-integer answer, give a defensible band consistent with the stem's precision.
- Include `solution.check` arithmetic for machine verification and an independent human
  check such as units, substitution-back, conservation, sign, order of magnitude, or a
  limiting case.

## Statement-combination questions

For questions with Statement I/II/III and combination options:

- rewrite each statement as a separate proposition;
- evaluate each proposition independently and record the truth pattern;
- only then map that pattern to the combination option;
- distinguish a false premise from a true statement used in the wrong context.

Do not reason backward from the four combinations; that can hide an unchecked statement.

## Assertion-Reason

Use a strict three-test sequence:

1. Is the Assertion true?
2. Is the Reason true?
3. If both are true, does the Reason actually explain the Assertion rather than merely
   discuss the same topic?

Then map the resulting verdict to the exam's exact option convention. State all three
verdicts explicitly so a correct option cannot result from an accidental convention mix-up.

## Match-the-following, tables and data interpretation

- Normalize units and definitions before matching.
- Solve each left-side item independently; record a compact mapping table.
- Use one-to-one constraints only when the question states them.
- For data tables/graphs, state the row/column/axis and denominator used before computing.
- Check that every source item and destination has been accounted for before selecting
  the encoded option.

## Diagram-dependent questions

First decode the figure before calculating:

1. list nodes, branches, axes, states, labels, directions, polarities and reference frame;
2. state what the diagram gives and what must be inferred;
3. mark the exact substructure or region used in the next step; and
4. redraw successive states/equivalents when topology or interpretation changes.

Use `solution-writing-with-diagrams.md` for staged placement and QA. Never rely on the
student mentally transforming the original figure while following equations.

## Transient, switching and state-change questions

Organize the solution by physical time/state:

- `t < 0`: identify the pre-switch steady state and stored energy;
- `t = 0+`: enforce continuity laws (`i_L` and `v_C` cannot jump unless the model permits);
- `t > 0`: draw/use the new topology, find the time constant or state equation, and solve;
- `t -> infinity`: verify the final steady state.

Include a state/equivalent diagram at each topology change when it materially clarifies
the reasoning.

## Equivalent-model and transformation questions

For Thevenin/Norton, source transformation, Laplace-domain conversion, block reduction,
sequence networks, per-unit conversion, star-delta, or similar methods:

- state the transformation and its validity conditions;
- show the representation before and after the transformation;
- preserve terminal variables, reference directions and bases;
- derive equations from the transformed model, not from an unexplained final formula; and
- transform back to the requested physical quantity if necessary.

## Geometry, vector and integration-region questions

- identify intersections, boundaries, orientation and symmetry before integrating;
- sketch/mark the region when bounds change or the sign of area matters;
- explain why the region must be split and write each limit from the drawing;
- for vectors, distinguish direction vector from unit vector and show normalization;
- verify that component areas/probabilities sum to the whole when applicable.

## Matrices, determinants and eigenvalue questions

- first look for invariant shortcuts: trace, determinant, rank, symmetry, triangular form,
  Cayley-Hamilton, repeated/dependent rows, or a special row/column operation;
- show row/column operations explicitly and never change a determinant without accounting
  for the operation;
- for MSQ, derive the shared matrix identity once, then test each statement;
- verify with a nonzero minor, trace/determinant relation, multiplication by the proposed
  inverse, or substitution into the characteristic polynomial.

## Proof, "always/never" and counterexample questions

- identify the quantifier and conditions;
- prove a universal claim from the definition/theorem, or disprove it with one valid
  counterexample;
- do not present several examples as a proof of an "always" statement;
- state which missing condition makes a tempting option false.

## Linked or common-data questions

- solve and label shared data once;
- keep each sub-question's answer path separate;
- do not let an error in a later part alter an earlier result;
- if a later part depends on a previous computed value, state the dependency explicitly
  and, when possible, verify it independently.

## Final type-specific audit

Before delivery, confirm:

- **MCQ:** exactly one defensible option; result matched only after solving.
- **MSQ:** every option independently tested; complete answer set matches the key.
- **NAT:** numerical value/range is platform-parseable, precision justified and checked.
- **Statement/AR:** truth values and causal relation evaluated before option mapping.
- **Diagram:** technical content and placement agree with the solution.
- **All types:** final answer, units, sign, assumptions and answer field agree.
