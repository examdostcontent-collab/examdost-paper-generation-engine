# Classification rules — the seven fields

Read this when you're unsure how to fill a column. The whole job is to put each
question in the right row with the right values, snapped to the master taxonomy
so the sheet lines up with the rest of the ExamDost library.

The honest default for every field: **if the upload already carries the answer,
use it.** Question banks exported from a system, or papers tagged by a setter,
often already state the subject, chapter, topic, marks, and difficulty. Trust
those tags first; only classify from scratch when a field is genuinely absent.
Your judgement is the fallback, not the first move.

---

## 1. Question number
**If the source numbers its questions, use those exact numbers** so the sheet
lines up with the original paper (e.g. a set running Q459–Q548 produces rows
459–548, not 1–90). Carry the source number into each question's `number` field
in `questions.json` and the builder will use it. Only when the source has no
usable numbering (pasted text, an untagged bank) do you fall back to a clean
running `1..N` in source order. Either way: no gaps, no renumbering by subject.

## 2. Subject Name
The canonical subject from the master taxonomy (one worksheet per subject). Use
the upload's subject tag if present; otherwise read the question and decide. Then
**snap the name to the master verbatim** — the lookup is case- and
space-tolerant but the words must match (e.g. the master's `EMFT EE`, not
"Electromagnetic Field Theory"). Load the vocabulary with
`load_taxonomy.py --flat` so you're choosing from real names, not inventing them.

## 3. Chapter number  &  4. type number
You do **not** write these by hand. You write the canonical **chapter name** and
**topic/type name** into `questions.json`; the builder looks up the chapter's
number and the topic's Type No from the master for that subject. So your job for
columns 3 and 4 is really: get the chapter name and topic name to match the
master exactly. If a name doesn't match, the number comes out blank and the row
is reported — that's the signal to fix the name or extend the master.

## 5. difficulty index — 1 / 2 / 3
`1 = Easy, 2 = Moderate, 3 = Difficult.` If the upload states a difficulty, map
it (Easy/Medium/Hard -> 1/2/3). Otherwise infer from **cognitive load** — the
number of distinct steps/concepts to reach the answer — not from how long the
text is:
- **1 (Easy):** single-concept recall or a direct one-liner — a formula stated,
  a definition, a standard fact, plug-one-number.
- **2 (Moderate):** a clean one-to-two-step application — pick the right idea and
  apply it once or twice with no trap.
- **3 (Difficult):** multi-step work, an intersection of two concepts, a
  derivation, or a deliberately planted trap/distractor that punishes the
  obvious move.

**For GATE, difficulty is calibrated against marks** (see
`marks_benchmarks/<subject>_gate.md`). The same effort scale drives both, so they
must agree: a **1-mark** item is difficulty **1–2** (1 if pure recall, 2 if a
formula is applied); a **2-mark** item is difficulty **2–3** (2 for a clean
two-step, 3 for multi-step / derivation / trap / linked-answer). A 2-mark GATE
question is essentially never Easy. Outside GATE, marks remain a hint, not a rule:
2-mark questions skew harder, but a wordy 1-mark recall is still a 1.

## 6. Marks
The marks for the question. Order of precedence:
1. **Marks on the question** → use them verbatim.
2. **No marks + exam is GATE** → assign **1 or 2** per question from the subject's
   GATE marks benchmark (`marks_benchmarks/<subject>_gate.md`). Marks track
   *solving effort, not answer format*: NAT and MCQ both span 1 and 2 marks. One
   move (recall / one formula / one reduction) → 1; a chain (multi-step numeric,
   concept intersection, full transient, locus, derivation) or any Linked-Answer /
   Common-Data item → 2. Chapter base-rates are only a tie-breaker. If there's **no
   benchmark for that subject yet, don't guess — ask for a PYQ file** and build one
   first (SKILL.md Step 1b).
3. **No marks + fixed-marks exam** → ask once ("marks per question? e.g. all 1, or
   1 for Section A and 2 for Section B") and apply it.

Never silently guess a GATE marks scheme — either the benchmark decides it or you
ask for the PYQ that lets you build the benchmark.

## 7. Question type — the fixed set
Map every question to **exactly one** of:
- **TheoryMCQ** — conceptual/recall MCQ, one correct option, no calculation.
- **Numerical MCQ** — MCQ whose answer comes from a calculation, one correct
  option.
- **NAT** — Numerical Answer Type: a number is typed in, there are no options.
- **MSQ** — Multiple Select: more than one option is correct.
- **StatementType** — "Which of the following statements is/are correct?", or
  numbered statements (S1, S2, ...) the student must evaluate.
- **Assertion-Reason** — the classic Assertion (A) + Reason (R) pair with the
  standard option set ("both true and R explains A", etc.).

Deciding the MCQ split: if a learner must *compute* to choose the option, it's
**Numerical MCQ**; if it's settled by knowing/understanding a concept, it's
**TheoryMCQ**. When options are numbers/quantities, it's almost always Numerical
MCQ. You may either write the final label straight into `type`, or write `"MCQ"`
plus `"type_detail": "numerical"` / `"theory"` and let the builder resolve it.

---

## When a question won't map
Leave the name as your best canonical guess and let the builder report the row as
unmapped — never invent a chapter/topic that isn't in the master just to fill the
cell. Collect the unmapped rows and show them to the user at the end so they can
either correct the tag or decide to add the entry to the master taxonomy. A blank
chapter/type number with an honest report beats a confidently wrong number.
