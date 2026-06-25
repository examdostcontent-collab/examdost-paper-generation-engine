# Building the `--header-regex` and `--code-template`

> **Try a `--header-preset` first.** Presets (`textbf-dot`, `textbf-q`,
> `item-bracket`, `que-macro`, `line-num`, `bold-md`) cover the common formats and
> carry zero backslashes through the shell, so they can't be corrupted. Only write
> a custom regex if no preset fits — and pass it via `--header-regex-file` (a file
> written with the Write tool), not as a raw shell argument, because some shells
> collapse `\\`→`\` and turn `\textbf` into a TAB.

The script is format-agnostic: you tell it how a question *header* looks via a
regex with a `(?P<num>...)` group capturing the current (old) question number.
The number inside that group is the only thing swapped; everything else in the
match is preserved.

## Step 1 — open the .tex and find ONE question header

Read the top of the file and locate how a question starts. Common shapes and the
regex + a safe code-template for each. Always test with `--list-headers` first.

### A. Bold manual number — `\textbf{1.}` / `\textbf{Q.1}` / `\textbf{Q1.}`
```
--header-regex '\\textbf\{(?:Q\.?\s*)?(?P<num>\d+)[\.\)]?\s*\}'
```

### B. `\item[1.]` inside an enumerate / custom list
```
--header-regex '\\item\[\s*(?P<num>\d+)[\.\)]?\s*\]'
```

### C. Custom macro `\question{1}{...}` or `\que{1}`
```
--header-regex '\\que[a-z]*\{\s*(?P<num>\d+)\s*\}'
```

### D. Line-leading `Q1.` or `1.` at start of a line (no macro)
```
--header-regex '(?m)^\s*Q?\.?\s*(?P<num>\d+)[\.\)]\s'
```

### E. exam-class `\question` with NO explicit number
The `exam`/`examdesign` classes auto-number, so there is no number to capture and
relabelling to repeated per-subject numbers is impossible without converting to
explicit numbers. If you see this, tell the user: the .tex must carry explicit
numbers for an A→B relabel. (Auto-numbered files can still get codes injected via
`--code-template`, but `--no-renumber` is then required.)

> The Whatever-the-format rule: the regex must match **exactly one header per
> question** and capture the number. Verify the count from `--list-headers`
> equals the question count before `--apply`.

## Step 2 — choose where the Code goes (`--code-template`)

The template string is inserted **immediately after** the matched header.
Placeholders: `{code}`, `{newnum}`, `{oldnum}`.

| Want | `--code-template` |
|------|-------------------|
| Small grey tag, right-aligned | `\\hfill{\\footnotesize\\texttt{[{code}]}}` |
| Tag right after the number | ` \\texttt{\\scriptsize ({code})}` |
| Margin note | `\\marginpar{\\tiny {code}}` |
| Nothing visible (comment only) | *(omit --code-template)* |

A `% qcode: <code> | old N -> new M` comment is added before every question by
default (suppress with `--no-comment`). It never prints in the PDF and gives you a
grep-able trail.

⚠️ If you use a macro the document doesn't define (e.g. a custom `\qcode`), the
PDF won't compile. Stick to primitives (`\texttt`, `\footnotesize`, `\hfill`,
`\marginpar`) unless you confirm the macro exists in the preamble.

## Step 3 — verify, then apply

1. `--list-headers` → confirm header count == expected questions, numbers look right.
2. Dry run (no flags beyond the regex) → read the audit: the three mismatch lists
   must be empty (or explained).
3. `--apply` → writes `<name>_coded.tex` + `<name>_coded.audit.md`.

## The coding sheet columns (defaults)

| Flag | Default header | Meaning |
|------|----------------|---------|
| `--old-col`  | `Question number`            | old per-test number (A) — what's in the .tex now |
| `--new-col`  | `Masterfile Question number` | new number to write (B) |
| `--code-col` | `Code`                       | code to inject (I) |
| `--test-col` | `2026`                       | test filter (J), e.g. `PGCIL EE 01` |

Headers are matched case/space-insensitively; the test column falls back to the
last column if `2026` isn't present. Old numbers must be unique within a test
(they are the join key); duplicates are reported in the audit.
