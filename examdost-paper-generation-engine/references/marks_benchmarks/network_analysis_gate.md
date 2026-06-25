# GATE marks benchmark — Network Analysis

**Exam:** GATE (EE/EC) · **Subject:** Network Analysis
**Derived from:** ExamDost GATE PYQ compilation `01-Network Analysis-F(2025)` —
200 tagged questions, 1992–2025 (78 one-mark, 110 two-mark, 12 legacy five-mark).
**Use this** to decide whether a *new* GATE Network Analysis question is worth
**1 or 2 marks**, and to set its **difficulty (1/2/3)**, when the question doesn't
already carry marks. (Modern GATE uses only 1- and 2-mark items; the old 5-mark
format ended ~2002 and is ignored.)

---

## The core rule: marks track *solving effort*, not answer format

The single biggest finding: **NAT vs MCQ does not decide marks.** "Round off to N
decimal places" NAT items appear in both 1-mark and 2-mark questions, and so do
4-option MCQs. What decides marks is **how much work it takes to get from the stem
to the answer.** Count the distinct steps and concepts.

### → 1 MARK when the question is *one move*
A single concept applied once, or a fact recalled. Signals seen in the PYQs:
- **Pure recall / property / definition.** "An ideal voltage source will charge an
  ideal capacitor (…instantaneously)"; "a practical current source is represented
  by"; "a nullator + resistor behaves as"; "the I–V characteristic is best
  depicted by".
- **Counting / topology one-liners.** "the number of junctions in the circuit";
  "number of chords in the graph"; "branches of a graph with 8 nodes and 5 loops"
  (one formula: B = N + L − 1).
- **One standard formula, plugged once.** Q-factor = f₀/BW; time constant τ = RC or
  L/R after reading R,C/L off the circuit; RMS/average/form-factor of a standard
  waveform; max-power load = conjugate of source impedance (state the value);
  series/parallel reduction to one equivalent R/L/C.
- **One-step phasor read-off.** "phasor representation of the current"; a single
  voltage/current from one nodal or KVL equation.

### → 2 MARKS when the question is a *chain*
Two or more linked steps, two concepts intersecting, or a derivation. Signals:
- **Multi-step numerics.** Solve a nonlinear V–I then find power; full nodal/mesh
  with simultaneous equations; integrate a current profile to get charge/voltage.
- **Full transient solutions.** i_L(t)/v_C(t) *for t > 0* (not just the t=0⁺
  value); "time required for the voltage to reach …"; second-order circuits;
  capacitor-combination voltage at t=0⁺ with redistribution.
- **Two-output / design questions.** "find the current **and** identify the change
  to double it"; "find the load R for max power **and** the load voltage & current".
- **Concept intersections.** Combined Q-factor of two coupled stages; Thévenin/Norton
  of a network *with dependent sources* needing a test source; two-port parameters
  then a derived quantity (e.g. Thévenin across the load of a Z-parameter block).
- **Locus / waveform identification** (admittance locus vs frequency, phasor locus
  as R varies, output-waveform shape) — these need reasoning across a range, →2.
- **Linked-Answer / Common-Data / "Statement for Linked Answer Questions" sets are
  ALWAYS 2 marks each** in GATE. If a stem belongs to such a group, weight it 2.

### Tie-breaker
If it's genuinely between 1 and 2, ask: *can a prepared student finish it in well
under a minute with no scratch work?* Yes → 1. Needs a line or two of working,
simultaneous equations, or a second idea → 2.

---

## Chapter priors (base rate of 2-mark items, from the PYQs)

Use as a gentle prior, not an override — the per-question step count above wins.
Some chapters simply ask harder questions on average:

| Chapter | 1-mk : 2-mk | Lean |
|---|---|---|
| 1 Network Basics | 19 : 22 (~46% : 54%) | balanced |
| 2 Network Theorems | 8 : 11 (~42% : 58%) | slightly 2-mark |
| 3 Transient Analysis | 11 : 21 (~34% : 66%) | **2-mark-heavy** (multi-step) |
| 4 Sinusoidal Steady State | 27 : 33 (~45% : 55%) | balanced |
| 5 Two Port Network | 4 : 9 (~31% : 69%) | **2-mark-heavy** |
| 6 Graph Theory | 4 : 2 (~67% : 33%) | **1-mark-heavy** (counting) |
| 7 Three Phase Circuits | 3 : 6 (~33% : 67%) | 2-mark-heavy |
| 8 Magnetically Coupled | 2 : 6 (~22% : 78%) | **2-mark-heavy** |

So a transient/two-port/coupled-circuit item that *looks* borderline leans 2; a
graph-theory counting item leans 1.

---

## Difficulty (1/2/3) recalibrated against GATE marks

Tie difficulty to the same effort scale, so difficulty and marks agree:

- **1 = Easy** — a **1-mark recall/definition/direct-lookup** item. One fact, no
  working. (e.g. "ideal source charges a capacitor …", "number of junctions".)
- **2 = Moderate** — a **1-mark single-formula application** *or* a clean **2-mark
  two-step** numeric with no trap. The bulk of the paper sits here. (e.g. τ = L/R
  after a reduction; conjugate-match max power; one nodal equation.)
- **3 = Difficult** — a **2-mark multi-step / multi-concept / derivation / trap /
  locus / linked-answer** item. Needs a plan, simultaneous equations, a second
  concept, or guards a classic trap. (e.g. dependent-source Thévenin via test
  source; full t>0 transient; "double the current — what changes"; combined Q.)

Practical mapping while tagging: **1-mark ⇒ difficulty 1 or 2** (1 if pure recall,
2 if a formula is applied); **2-mark ⇒ difficulty 2 or 3** (2 if a clean two-step,
3 if multi-step/derivation/trap). A 2-mark item is essentially never difficulty 1.

---

## Worked calls (from the PYQs)

- *"How many 200W/220V lamps in series equal one 100W/220V lamp?"* → one
  power-ratio step → **1 mark, difficulty 2.**
- *"Number of chords in the graph of the given circuit."* → recall L = B − N + 1 →
  **1 mark, difficulty 1.**
- *"Thévenin resistance across A–B"* for a network **with a dependent source**
  (apply a 1 A test source, solve) → **2 marks, difficulty 3.**
- *"i_L(t) for t > 0 after the switch opens."* → full first-order solution →
  **2 marks, difficulty 2–3** (3 if initial conditions need work).
- *"Find the current AND the change needed to double it."* → two-output design →
  **2 marks, difficulty 3.**
- *"Q-factor of a network with f₀ = 150 kHz, BW = 600 Hz."* → one formula →
  **1 mark, difficulty 2.**
