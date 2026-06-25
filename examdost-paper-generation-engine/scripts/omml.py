"""
omml.py — convert the skill's LaTeX-style math markup into Office MathML (OMML)
so the Word builder can embed **native, editable Word equations** (stacked
fractions, radicals with vinculum, integrals, Greek, etc.).

Uses pandoc via pypandoc. All equations in a paper are converted in ONE pandoc
run (batched) and cached. If pandoc/pypandoc is unavailable or a conversion
fails, the caller falls back to the Unicode renderer (paperlib.render_math).

Public API:
    available() -> bool
    convert_batch(latex_list) -> {latex: omml_xml_or_None}
    split_math(text) -> [("text", s) | ("math", latex), ...]
    omath_elements(omml_xml) -> [lxml element, ...]   (ready to append to a w:p)
"""
from __future__ import annotations

import os
import re
import tempfile
import zipfile

try:
    import pypandoc
    _HAVE = True
except Exception:
    _HAVE = False

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

_OMATH_RE = re.compile(r"<m:oMath>.*?</m:oMath>", re.S)

# An inline math token in our authored markup: \frac{}{}, \sqrt, \cmd, x^{..}, x^2,
# V_{th}, I_2 / P_o. Used to pick math spans out of mixed prose.
# brace group allowing ONE level of nesting, e.g. {V_{total}}
_BR = r"\{(?:[^{}]|\{[^{}]*\})*\}"
# one sub/superscript fragment: _{..}, ^{..}, _x, ^2, ^{-6} ...
_SS = r"(?:[_^](?:" + _BR + r"|[-+]?[A-Za-z0-9]))"
_MATH_TOKEN = re.compile(r"""
    \\begin\{[A-Za-z*]+\}[\s\S]*?\\end\{[A-Za-z*]+\} # \begin{bmatrix}...\end{bmatrix} (whole environment, one token)
  | \\frac\s*""" + _BR + r"""\s*""" + _BR + r"""   # \frac{a}{b} (args may nest one level)
  | \\sqrt\s*(?:""" + _BR + r""")?                  # \sqrt{x} or \sqrt
  | \\[A-Za-z]+\s*""" + _BR + r"""(?:""" + _SS + r""")?  # \vec{E}, \hat{n}, \bar{H}, \overline{AB} (accent/unary cmd + braced arg)
  | \\[A-Za-z]+['′]*""" + _SS + r"""{1,2}          # \int_{0}^{\infty}, \omega_{n}, \mu_0, \phi^2
  | \\[A-Za-z]+                                      # \omega \times \leq ...
  | [A-Za-z0-9]+['′]*""" + _SS + r"""{1,2}         # x_i^2, V_{th}, x^{n+1}, I''_{f}
""", re.VERBOSE)


def mathify(s):
    """Normalise the authored markup into clean LaTeX before pandoc, so equations
    render with correct spacing and complete subscripts:
      - strip LaTeX thin-space commands
      - '*' multiplication -> \\cdot
      - brace multi-character sub/superscripts:  P_mech -> P_{mech}, x^abc -> x^{abc}
      - wrap prose words (2+ letters, incl. spaces) in \\text{...} so they stay upright
        and keep their spaces (LaTeX math mode would otherwise concatenate them)."""
    s = str(s)
    saved = []
    def _protect(m):
        saved.append(m.group(0))
        return f"\x00{len(saved) - 1}\x00"
    # protect whole LaTeX environments (matrices etc.) FIRST so their env name, row
    # separators (\\) and body survive verbatim (no \text wrap, no \\-collapse).
    s = re.sub(r"\\begin\{[A-Za-z*]+\}[\s\S]*?\\end\{[A-Za-z*]+\}", _protect, s)
    s = re.sub(r"\\[,;:!]", " ", s)
    s = re.sub(r"\\ ", " ", s)
    s = re.sub(r"\s*\*\s*", r" \\cdot ", s)
    # protect any author-supplied \text{...} so we don't wrap words inside it again
    s = re.sub(r"\\text\{[^{}]*\}", _protect, s)
    # brace multi-char sub/superscript args that aren't already braced
    s = re.sub(r"([_^])([A-Za-z0-9]{2,})", r"\1{\2}", s)
    # wrap word runs in \text{}; skip LaTeX command names (preceded by a backslash)
    s = re.sub(r"(?<![\\A-Za-z])[A-Za-z]{2,}(?:\s+[A-Za-z]{2,})*",
               lambda m: r"\text{" + m.group(0) + "}", s)
    for i, frag in enumerate(saved):                  # restore protected \text{...}
        s = s.replace(f"\x00{i}\x00", frag)
    return s


def is_equation(s):
    """True if the string really looks like math (worth sending to pandoc), not prose.
    Catches \\cmd, ^, _ markup, or an '=' followed by something containing a digit.
    A string with no alphanumeric operand at all (e.g. a stray '^' or '_') is NOT
    math — sending it to pandoc just yields a 'could not convert' warning."""
    s = str(s)
    if not re.search(r"[A-Za-z0-9]", s):
        return False
    return bool(re.search(r"[\\^_]", s) or re.search(r"=\s*[^=]*\d", s))


def available():
    if not _HAVE:
        return False
    try:
        pypandoc.get_pandoc_version()
        return True
    except Exception:
        return False


# Characters that may sit BETWEEN two math tokens without breaking the equation:
# whitespace, digits, and the usual math operators / grouping / sub-sup glue. A gap
# made only of these means the surrounding tokens are one expression (e.g. the
# "=9" between \frac{..} and \times in "...\frac{1}{4\pi\epsilon_0}=9\times10^{9}"),
# so they must be merged into ONE equation object instead of several tiny ones.
# Comma/letters are deliberately excluded — they usually separate, not connect.
_GLUE_GAP = re.compile(r"[\s0-9.+\-*/=()\[\]^_×·]*\Z")
# A math span ending on a dangling operator/command (e.g. "...\nabla \times",
# "...= -\nabla") should pull in a lone trailing variable letter so vector
# identities like  E = -∇V  render as ONE equation, not "[E = -∇] V".
_END_OP = re.compile(r"(?:\\[A-Za-z]+|[=+\-*/·×])\s*\Z")


def split_math(text):
    """Split mixed prose+markup into ordered ('text'|'math', value) chunks.

    Consecutive math tokens whose in-between text is pure 'glue' (operators,
    digits, spaces) are merged into a SINGLE math span, so an expression like
    9×10⁹×fraction renders as one native equation rather than being shattered
    into [×][10⁹][×][fraction] (the cause of 'messed up / unreadable' math)."""
    text = str(text)
    toks = list(_MATH_TOKEN.finditer(text))
    if not toks:
        return [("text", text)]
    spans, s, e = [], toks[0].start(), toks[0].end()
    for m in toks[1:]:
        if _GLUE_GAP.match(text[e:m.start()]):     # glue-only gap -> same equation
            e = m.end()
        else:
            spans.append((s, e)); s, e = m.start(), m.end()
    spans.append((s, e))
    # pull a lone trailing variable into a span that ends on a dangling operator
    fixed = []
    for s, e in spans:
        m = re.match(r"\s+[A-Za-z](?![A-Za-z0-9])", text[e:])
        if m and _END_OP.search(text[s:e]):
            e += m.end()
        fixed.append((s, e))
    spans = fixed
    out, last = [], 0
    for s, e in spans:
        if s > last:
            out.append(("text", text[last:s]))
        out.append(("math", text[s:e]))            # includes any glue between tokens
        last = e
    if last < len(text):
        out.append(("text", text[last:]))
    return out or [("text", text)]


def convert_batch(latex_list):
    """Convert many LaTeX strings in a single pandoc invocation. Returns
    {latex: omml_xml or None}. omml_xml may contain >1 <m:oMath> (concatenated)."""
    uniq = [s for s in dict.fromkeys(latex_list) if s and str(s).strip()]
    if not uniq or not available():
        return {}
    parts = []
    for i, s in enumerate(uniq):
        parts.append(f"SENT{i}SENT")          # ordering marker (plain text paragraph)
        parts.append("$" + mathify(s) + "$")
    md = "\n\n".join(parts)
    out = os.path.join(tempfile.gettempdir(), "paper_omml_batch.docx")
    try:
        pypandoc.convert_text(md, "docx", format="markdown", outputfile=out)
        with zipfile.ZipFile(out) as z:
            xml = z.read("word/document.xml").decode("utf-8")
    except Exception:
        return {}
    res = {}
    for i, s in enumerate(uniq):
        a = xml.find(f"SENT{i}SENT")
        b = xml.find(f"SENT{i+1}SENT") if i + 1 < len(uniq) else len(xml)
        window = xml[a:b] if a >= 0 else ""
        oms = _OMATH_RE.findall(window)
        res[s] = "".join(oms) if oms else None
    return res


def omath_elements(omml_xml):
    """Parse cached OMML into a list of lxml elements ready to append to a w:p.
    Namespaces are re-declared on each <m:oMath> so it parses standalone."""
    from docx.oxml import parse_xml
    els = []
    for om in _OMATH_RE.findall(omml_xml or ""):
        om = om.replace("<m:oMath>", f'<m:oMath xmlns:m="{M_NS}" xmlns:w="{W_NS}">', 1)
        try:
            els.append(parse_xml(om))
        except Exception:
            pass
    return els
