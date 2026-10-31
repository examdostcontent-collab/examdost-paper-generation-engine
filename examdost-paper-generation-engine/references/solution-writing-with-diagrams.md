# Solution Writing with Explanatory Diagrams

Use this guide for every newly generated worked solution. It captures the teaching
method used in the approved ExamDost PYQ books: the diagram is part of the reasoning,
not decoration placed after the answer.

## The target reading experience

A student should be able to follow the solution in this order:

1. identify the governing idea;
2. see the current physical/logical state;
3. perform one meaningful transformation;
4. see the transformed state immediately;
5. write the equation justified by that state; and
6. repeat until the final answer is obvious and verifiable.

The Network Analysis books are the clearest model: an original network is followed by
successive equivalent networks after each series/parallel reduction. Control Systems
uses a time-domain circuit followed by its Laplace-domain equivalent before KVL. Digital
Electronics places a K-map or gate diagram beside the simplification it supports. Power
Systems places the compensation circuit beside the reactive-power calculation. Replicate
this causal placement, not the exact drawings.

## Mandatory visual-decision pass

Before finalising each solution, ask:

> Would a learner understand a change of state, topology, direction, region, grouping,
> or physical relationship faster and more accurately by seeing it?

If yes, add a solution diagram. If no, keep the solution textual; do not force a picture
for direct recall or a one-line substitution. "Wherever possible" means wherever the
visual removes genuine mental reconstruction, not wherever blank space exists.

Strong triggers include:

- a circuit is reduced, transformed, source-converted, opened/shorted, switched, or
  replaced by a Thevenin/Norton/Laplace equivalent;
- current direction, voltage polarity, loop/mesh, node, or reference direction matters;
- a block diagram or signal-flow graph is reduced;
- a K-map grouping, logic-gate path, state transition, timing diagram, or waveform is
  part of the reasoning;
- a phasor, vector, field direction, magnetic path, torque-speed curve, root locus,
  Bode/Nyquist plot, or geometric construction explains the result;
- an area/region, probability tree, Venn diagram, number line, free-body diagram, or
  coordinate sketch prevents an interpretation error; or
- the problem has multiple operating intervals or states such as `t < 0`, `t = 0+`,
  and steady state.

Usually skip a diagram when the item is pure definition/recall, the formula is applied
once with no spatial or state change, or the proposed image merely repeats the stem.

## Stage-by-stage rule

- One meaningful transformation per stage. Do not jump from the original figure to the
  final equivalent if intermediate topology is where students commonly make mistakes.
- Place the visual immediately after the sentence that introduces that stage and before
  the equation derived from it.
- Use an action caption such as "After opening the capacitor at DC steady state" or
  "After combining R2 and R3 in parallel". Avoid empty captions such as "Figure 1".
- Keep variable names, numeric values, units, directions, polarities, node names, option
  labels, and colour meaning identical to the stem and calculations.
- Show only information needed for that stage. Preserve unchanged geometry between
  consecutive figures when possible so the student can see exactly what changed.
- For a multi-stage solution, write one ordered `solution_diagram_prompts` entry per
  stage, in the same order as the calculation steps. Begin each prompt's content with
  `Stage N — place after calculation step M:` so the downstream image/insertion pass
  can place it beside the correct reasoning step.

The existing builders currently render prompt placeholders. The downstream diagram
creation/insertion pass must replace each placeholder with the generated image at the
stated placement; do not leave the prompts in a student-facing final file.

## Prompt content

Every solution-diagram prompt must be self-contained and specify:

1. the diagram type and pedagogical purpose;
2. the exact topology/geometry/state to draw;
3. every required label, value, unit, arrow, polarity, axis, scale, and operating state;
4. what changed from the preceding stage and what must remain unchanged; and
5. the action caption.

Describe content only. The builders append the ExamDost house style automatically.
Never ask the image model to calculate, infer missing values, or choose a topology. The
solution author must settle all technical content first and encode it explicitly.

Example sequence:

```json
"solution_diagram_prompts": [
  "[GEMINI_FLASH_PROMPT: Stage 1 — place after calculation step 1: redraw the given network and highlight only R2 and R3 as a parallel pair between nodes A and B; retain every original label and polarity; caption: Identify the first reducible pair.]",
  "[GEMINI_FLASH_PROMPT: Stage 2 — place after calculation step 3: replace R2 and R3 by their verified equivalent R23 while leaving the remaining network unchanged; label nodes A and B and current I; caption: Network after the first reduction.]",
  "[GEMINI_FLASH_PROMPT: Stage 3 — place after calculation step 5: show the final source and single equivalent resistance Req with the same current direction I; caption: Final equivalent circuit used for I = V/Req.]"
]
```

## Subject-specific visual choices

- **Network / Machines / Power / Analog:** original state, marked directions and
  polarities, then each equivalent or operating state; use phasors or characteristic
  curves when they carry the argument.
- **Control / Signals:** transformed model, block reduction, signal-flow loops, pole-zero
  map, root locus, Bode/Nyquist, waveform, or convolution overlap at the step used.
- **Digital:** K-map with valid Gray-code ordering and visible groups, gate-by-gate
  intermediate signals, truth/state table, timing waveform, or state diagram.
- **EMFT:** geometry with coordinate system, surface normal, field/current direction,
  boundary, integration path, and region labels.
- **Engineering Mathematics:** sketch the region, contour, vector geometry, graph,
  number line, or transformation only when it explains a bound, sign, intersection,
  multiplicity, or limiting behaviour.
- **Aptitude / reasoning:** use a table, Venn diagram, family/tree relation, route map,
  or number line when it reduces verbal ambiguity.

## Technical and visual QA

Audit every explanatory diagram against the solved mathematics before delivery:

- topology/connectivity and component count are exact;
- arrow directions and polarity signs agree with the equations;
- all labels, values, units, subscripts, superscripts, decimal points, and option letters
  are present and legible;
- axes, origin, scale, phase sequence, Gray-code order, switching state, and time interval
  are correct where applicable;
- each stage reflects exactly one stated transformation and does not silently change any
  other part of the problem;
- the caption explains why the visual appears at that point;
- the sequence plus equations leads to the keyed answer; and
- the final rendered Word and PDF are checked at normal reading size for clipping,
  overlap, blur, tiny labels, and accidental page separation from the relevant step.

If an image cannot be verified confidently, fix/regenerate it or remove it and make the
text self-sufficient. Never ship an attractive but technically uncertain diagram.
