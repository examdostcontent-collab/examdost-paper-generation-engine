# The Lean Exclusion Log — fingerprint format & append procedure

The Exclusion Log is the memory that makes generation **non-repeating across
runs**. Each line is one condensed fingerprint of a question already used. You
read it in Phase 1 (to avoid repeats) and extend it in Phase 4 (to record what
you just made).

## The repeat rule (what counts as a duplicate)

There are **two** rules — a value rule and a structure-cap rule.

**1. Value rule — a same-concept question with FRESH numbers is NOT a duplicate; only an
EXACT-VALUE repeat is.** Asking another Thevenin / max-power-transfer question is fine
(the exam reuses concepts). What's forbidden is reusing the **exact numeric dataset**.
Two items collide on value only when they share the same **subject + chapter/topic +
type + identical set of numbers** (the *value signature*). `validate_paper.py` computes
this from the stem, options, and `solution.given` and ERRORS on an exact-value repeat —
within the paper and against the log.

**2. Structure-cap rule — a template may not be re-skinned across the whole series with
only new numbers.** The value rule alone let one question (especially one *diagram*) be
copied into every mock with rotated values — the single biggest student complaint. So
two number-free structure fingerprints are now capped across the cumulative series:
- **template_signature** — stem + diagram topology, all numbers stripped, with the
  subject/chapter/type folded in. A text template may appear **at most 2× across the
  series**; the 3rd is an ERROR.
- **diagram_signature** — the figure/circuit **topology** only (number-free, prose-noise
  removed). A diagram may appear **at most 1× across the series**; any reuse is an ERROR.
  Same circuit, new data, mock after mock → build fails.
To stay clear of the caps, vary the **structure** (configuration, given↔unknown, framing,
or — for figures — the topology itself: series↔parallel, add/move a source, bridge/ladder/
Y-Δ), not just the values. `coverage_report.py` prints a "STRUCTURES AT THE SERIES CAP"
list of what's already exhausted — avoid those. Pure-theory items (no numbers) aren't
value-deduped, but their template signature is still capped, so vary their framing by hand
too. (Caps live in `validate_paper.py`: `TEXT_TEMPLATE_CAP`, `FIGURE_TOPOLOGY_CAP`.)

## The fingerprint string (exact format)

```
[Subject]_[Chapter/Topic]_[Type]_[Core Variables / Key Concept Used]
```

- **Subject** — canonical subject name (verbatim from the blueprint).
- **Chapter/Topic** — the canonical chapter, optionally `>topic` for finer grain.
- **Type** — `MCQ` / `MSQ` / `NAT` / `AR` / `Statement`.
- **Core Variables / Key Concept** — the *specific* thing that makes this question
  this question: the variables solved for, the configuration, or the concept combo.
  This is the field that actually prevents repeats — make it descriptive enough that
  a near-duplicate would produce a near-identical string.

Examples:
```
Electrical Machines_Induction Machines>Slip and Speed_NAT_slip from Ns & Nr (4-pole, 50Hz)
Network Theory_Theorems_MCQ_Thevenin Rth + max power transfer
Power Systems_Fault Analysis_NAT_symmetrical 3-phase fault per-unit current
Control Systems_Stability_MCQ_Routh array with one row of zeros (edge case)
[WILDCARD] Control Systems x Electrical Machines_MCQ_motor TF closed-loop stability
```
Prefix cross-subject wildcards with `[WILDCARD]` and name both subjects.

## How non-repetition uses it
- In Phase 1, load the log. While generating, give each numeric question a numeric
  dataset **not already in the log** for that subject/topic/type. You may reuse the
  concept freely — just not the exact numbers/configuration.
- The deterministic check is the **value signature** (the multiset of numbers), enforced
  by `validate_paper.py`. The human-readable `fingerprint` string is the audit trail;
  the value signature is what actually blocks exact-value repeats.
- The log is "lean": one line per question, no full text. That keeps it small enough
  to carry forward indefinitely.

## Append procedure (Phase 4)

`update_exclusion_log.py` reads the user's **original** log (path, or `-` for an
empty/first run), pulls the `fingerprint` field from every question in `paper.json`,
appends the new lines, de-duplicates exact repeats, and writes a fresh file:

```
python scripts/update_exclusion_log.py "<original log path or '->" paper.json "<Exam> Exclusion Log.csv"
```

- **`.csv` output** (recommended): columns `subject,chapter_topic,type,core,value_signature,template_signature,diagram_signature,fingerprint,exam,added_on`.
  `value_signature` lets the next run detect exact-value repeats; `template_signature` and
  `diagram_signature` let it enforce the **structure caps** (text template ≤2×, diagram
  topology ≤1× across the series). Always carry the CSV forward, not the txt — the txt drops
  all three signatures. (Older CSVs without the two new columns still load fine; their rows
  just don't count toward the structure caps until regenerated.)
- **`.txt` output**: one raw fingerprint per line (lossy — no signatures, so future runs
  can't auto-detect value repeats OR enforce the structure caps). Use only if the user insists.
- De-dup on append skips only **exact-value repeats** of already-logged items; same-concept
  fresh-number questions are appended normally (the structure caps are enforced at generation
  time by `validate_paper.py`, not by dropping rows here). Existing entries are preserved
  verbatim, so the user can save the result straight over their master tracker for the next run.

## Rules
- **Every** generated question must carry a `fingerprint` in `paper.json`; the verifier
  checks this.
- Keep fingerprints in the **same canonical vocabulary** as the blueprint, or
  cross-run matching silently breaks.
- Don't shorten the core-concept field into uselessness — `MCQ_efficiency` is too vague;
  `MCQ_transformer efficiency at 3/4 load, iron/copper split` is a real fingerprint.
