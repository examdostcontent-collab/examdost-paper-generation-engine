# -*- coding: utf-8 -*-
r"""latexmode.py -- emit equations as inline LaTeX ($...$) instead of native Word OMML.

The builders normally turn the authored math markup into OMML via pandoc
(omml.py), and the user then runs the separate word-to-latex skill to get
$...$ for their MathJax/KaTeX platform. That round-trip (markup -> OMML ->
LaTeX) is wasteful and lossy. This module lets the builder emit the LaTeX
form DIRECTLY from the same source markup, so no pandoc and no conversion are
needed:

    inline(r"Z_{c}=\sqrt{\frac{L}{C}}")  ->  r"$\scriptstyle Z_{c}=\sqrt{\frac{L}{C}}$"

It reuses omml.mathify() for the normalisation (brace multi-char sub/sups,
\cdot, \text{} around prose) so the dialect matches the previous pipeline, and
ships the same spacing pass that keeps adjacent spans / numbers from colliding
($\times$$10^4$ -> $\times$ $10^4$, 9.01$x$ -> 9.01 $x$, \DeltaV -> \Delta V).

Default size wrapper is \scriptstyle (~70%, the size the platform honours for
inline math); pass size="" for full size or "\\scriptscriptstyle" for ~50%.
"""
from __future__ import annotations
import re
import omml as OM

DEFAULT_SIZE = r"\scriptstyle"

# control words that must keep a space before a following bare letter.
# Sorted LONGEST-FIRST so the regex alternation never matches a short word as a
# prefix of a longer one (e.g. '\int' must not match '\in', '\simeq' not '\sim').
_CW_LIST = (
    "Delta Gamma Omega Lambda Sigma Phi Theta Pi Psi Xi "
    "alpha beta gamma delta epsilon varepsilon zeta eta theta iota kappa lambda mu nu xi "
    "pi rho sigma tau upsilon phi varphi chi psi omega "
    "approx propto times cdot div pm mp leq geq neq equiv cong simeq sim ll gg "
    "Rightarrow Leftarrow rightarrow leftarrow leftrightarrow to mapsto "
    "infty partial nabla forall exists notin in subset cup cap "
    "sum int oint prod angle perp parallel degree circ prime"
).split()
_CW_SET = frozenset(_CW_LIST)
_CW_BY_LEN = sorted(_CW_LIST, key=len, reverse=True)
_CMD_WORD = re.compile(r"\\([A-Za-z]+)")


def _cw_prefix(word):
    """If `word` is NOT itself a control word but STARTS with one (a CW glued to
    extra letters, e.g. 'omegab'), return that CW prefix; else None. Complete CWs
    ('int', 'simeq') return None so '\\int x' / '\\simeq y' are left untouched."""
    if word in _CW_SET:
        return None
    for p in _CW_BY_LEN:
        if len(word) > len(p) and word.startswith(p):
            return p
    return None


def inline(markup, size=DEFAULT_SIZE):
    """Authored math markup -> a single inline-LaTeX string `$<size> <latex>$`."""
    latex = OM.mathify(markup)
    return f"${size} {latex}$" if size else f"${latex}$"


# --------------------------- spacing pass (shared) -------------------------
def _split_cw(m):
    w = m.group(1)
    p = _cw_prefix(w)
    return "\\" + p + " " + w[len(p):] if p else m.group(0)


def fix_inner(s):
    s = _CMD_WORD.sub(_split_cw, s)
    return s.replace("$$", "$ $")


def _ascii_textish(ch):
    return ch.isascii() and (ch.isalnum() or ch in "([")


def _ascii_textish_left(ch):
    return ch.isascii() and (ch.isalnum() or ch in ")]%")


def need_space(left, right):
    if not left or not right:
        return False
    if left.endswith((" ", "\t")) or right.startswith((" ", "\t")):
        return False
    la, fb = left[-1], right[0]
    lm, rm = left.endswith("$"), right.startswith("$")
    if lm and rm:
        return True
    if lm and _ascii_textish(fb):
        return True
    if rm and _ascii_textish_left(la):
        return True
    return False


def fix_paragraph(p):
    """In-place: fix run-boundary collisions + within-run control-word gluing."""
    n = 0
    for r in p.runs:
        nt = fix_inner(r.text)
        if nt != r.text:
            r.text = nt
            n += 1
    runs = p.runs
    for i in range(len(runs) - 1):
        if need_space(runs[i].text, runs[i + 1].text):
            runs[i].text = runs[i].text + " "
            n += 1
    return n


def fix_doc(doc):
    """Run the spacing pass over every paragraph and table cell of a python-docx doc."""
    n = 0
    for p in doc.paragraphs:
        n += fix_paragraph(p)
    for t in doc.tables:
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    n += fix_paragraph(p)
    return n
