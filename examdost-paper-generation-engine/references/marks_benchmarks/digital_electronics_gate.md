# GATE marks benchmark — Digital Electronics

**Exam:** GATE (EE) · **Subject:** Digital Electronics
**Derived from:** ExamDost GATE PYQ compilation `2. EE - Digital Electronics-(2025)` —
115 tagged questions (46 one-mark, 59 two-mark, 9 legacy five-mark, 1 stray).
**Use this** to weight a *new* GATE Digital Electronics question **1 or 2 marks**
and set its **difficulty (1/2/3)** when marks aren't supplied. Modern GATE uses
only 1/2 marks; the 5-mark items are the pre-2003 format and are ignored.

Overall modern split: **44% one-mark / 56% two-mark.** Same governing rule as
every subject: **marks track solving effort, not answer format** — NAT and MCQ
both span 1 and 2 marks.

---

## → 1 MARK when it's one move
- **Simplify / evaluate one Boolean expression**, or read the **output of a small
  combinational circuit** directly.
- **One standard formula, plugged once:** ripple-counter f_max = 1/(n·t_pd); MOD of
  cascaded counters = product of MODs; DAC resolution ↔ bit size / step; ADC
  resolution = V_ref/2ⁿ; ADC conversion-time ↔ max input frequency; "max distinct
  Boolean functions of n vars = 2^(2ⁿ)"; min flip-flops = ⌈log₂(states)⌉; smallest
  12-bit 2's-complement integer = −2ⁿ⁻¹.
- **Sign-extension / single 2's-complement fact**; radix value of one number.
- **Identify / recall:** which gate/function, fastest/slowest ADC, memory
  speed-order, open-collector use, noise-margin/logic-level read-off.
- **A single microprocessor instruction's effect.**

## → 2 MARKS when it's a chain
- **Multi-step sequential analysis:** counter state after k clocks; sequence /
  pattern detector output for a data stream; waveform period / output frequency
  through a circuit; ring-counter/shift-register evolution.
- **K-map with don't-cares, then realize the circuit**; enumerate prime / essential
  prime implicants from a full map; minimum-gate (NAND/NOR/MUX-only)
  implementation worked out, not recalled.
- **Implement a function with a MUX / decoder** (work out the input connections).
- **Critical-path / hazard timing** down a chain of gate delays (longest delay,
  glitch analysis).
- **Multi-instruction 8085 program tracing**; multi-step 2's-complement arithmetic
  correctness.
- **Linked-Answer / Common-Data sets are always 2 marks each.**

### Tie-breaker
Can a prepared student finish with essentially no scratch work (one identity, one
formula, one look-up)? → 1. Needs a K-map worked, a counter stepped, a program
traced, or a connection table built? → 2.

---

## Chapter priors (2-mark share, from the PYQs)
Gentle prior only — the per-question step count decides:

| Chapter | 1-mk : 2-mk | Lean |
|---|---|---|
| Number Systems | small sample | (treat by effort) |
| Boolean Algebra and Logic Gates | 7 : 8 (~47/53) | balanced |
| Combinational Circuits | 5 : 9 (~36/64) | **2-mark-heavy** |
| Sequential Circuits | 9 : 13 (~41/59) | 2-mark-leaning |
| Data Converters | 9 : 9 (50/50) | balanced |
| Logic Family | 4 : 3 (~57/43) | **1-mark-leaning** |
| Microprocessor | 12 : 16 (~43/57) | 2-mark-leaning |

So a combinational "implement-this-function" item leans 2; a logic-family
recall/noise-margin item leans 1.

---

## Difficulty (1/2/3) — tied to marks (same as [[network_analysis_gate]])
- **1 = Easy** — a 1-mark recall / identity / direct read-off (one fact).
- **2 = Moderate** — a 1-mark single-formula application *or* a clean 2-mark
  two-step. Most of the paper.
- **3 = Difficult** — a 2-mark multi-step / critical-path-timing / sequence-detector
  / full-K-map-realization / program-trace / linked-answer item.
Mapping while tagging: **1-mark ⇒ difficulty 1–2; 2-mark ⇒ difficulty 2–3.** A
2-mark item is never Easy.

## Worked calls (from the PYQs)
- *"MOD-2 ⊗ MOD-5 cascaded = MOD ___ counter."* → one product → **1 mark, diff 2.**
- *"Smallest integer in 12-bit signed 2's complement."* → −2¹¹ → **1 mark, diff 1.**
- *"4-stage ripple counter, t_pd = 20 ns, max clock freq."* → one formula →
  **1 mark, diff 2.**
- *"Sequence detector output for input stream (1,1,0,1,0,…)."* → step the FSM →
  **2 marks, diff 3.**
- *"K-map with a don't-care — which circuit realizes F?"* → minimize + map to gates
  → **2 marks, diff 2–3.**
- *"8085: after this program, the flag/register contents are ___."* → trace → **2
  marks, diff 3** (linked-answer sets always 2).
