"""
paperlib.py — shared helpers for the ExamDost paper-generator builders/validator.

Importable by any sibling script (when a script is run as `python scripts/X.py`,
its own directory is on sys.path, so `from paperlib import ...` works).

Provides:
  render_math(text)          -> light math markup -> clean Unicode (subscripts,
                                superscripts, Greek, operators, roots, fractions).
  value_signature(question)  -> canonical string of the EXACT numeric dataset used
                                (so an exact-value repeat is detectable; a same-concept
                                question with fresh numbers is NOT a repeat).
  repeat_key(question)        -> (subject, chapter/topic, type, value_signature) tuple
                                used to detect exact-value duplicates.
  template_signature(question)-> number-free STRUCTURAL fingerprint (stem + diagram
                                topology) so "same question, fresh numbers" collides.
  template_key(question)      -> (subject, chapter/topic, type, template_signature)
                                used to CAP template over-reuse across a mock series.
  diagram_signature(question) -> number-free DIAGRAM TOPOLOGY fingerprint (figures only),
                                capped harder so the same circuit isn't redrawn each mock.
  safe_eval_number(expr)     -> evaluate an arithmetic check expression safely (no names
                                except whitelisted math), returns float.
  option_letters(options)    -> the letters actually present, e.g. {"A","B","C","D"}.
  answer_letters(answer)     -> the letters claimed by an answer string.
  parse_range(answer)        -> (lo, hi) numeric band for a NAT answer, or None.
  first_number(text)         -> first numeric literal in a string as float, or None.
  safe_output_path(path)     -> sanitise the FILENAME part for the OS (keeps the dir).
"""
from __future__ import annotations

import ast
import math
import os
import re

# ----------------------------- math rendering -----------------------------
_GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "zeta": "ζ", "eta": "η", "theta": "θ", "iota": "ι", "kappa": "κ",
    "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π", "rho": "ρ",
    "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ", "chi": "χ",
    "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
}
_SYMBOL = {
    r"\times": "×", r"\cdot": "·", r"\div": "÷", r"\pm": "±", r"\mp": "∓",
    r"\leq": "≤", r"\geq": "≥", r"\neq": "≠", r"\approx": "≈", r"\equiv": "≡",
    r"\infty": "∞", r"\partial": "∂", r"\nabla": "∇", r"\int": "∫", r"\oint": "∮",
    r"\sum": "∑", r"\prod": "∏", r"\degree": "°", r"\deg": "°", r"\angle": "∠",
    r"\propto": "∝", r"\in": "∈", r"\notin": "∉", r"\cdots": "⋯", r"\ldots": "…",
    r"\Rightarrow": "⇒", r"\Leftarrow": "⇐", r"\rightarrow": "→", r"\leftarrow": "←",
    r"\to": "→", r"\ohm": "Ω", r"\parallel": "∥", r"\perp": "⊥", r"\angstrom": "Å",
}
# Accent commands -> Unicode combining marks (applied to the braced/next char). The
# mark sits AFTER the letter so it combines onto it: \vec{E} -> E⃗, \hat{n} -> n̂.
_ACCENTS = {"vec": "⃗", "hat": "̂", "bar": "̄", "overline": "̄",
            "dot": "̇", "ddot": "̈", "tilde": "̃"}
_SUP = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
        "7": "⁷", "8": "⁸", "9": "⁹", "+": "⁺", "-": "⁻", "=": "⁼", "(": "⁽",
        ")": "⁾", "n": "ⁿ", "i": "ⁱ", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
        "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "j": "ʲ", "k": "ᵏ", "l": "ˡ",
        "m": "ᵐ", "o": "ᵒ", "p": "ᵖ", "r": "ʳ", "s": "ˢ", "t": "ᵗ", "u": "ᵘ",
        "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ", "z": "ᶻ", "T": "ᵀ"}
_SUB = {"0": "₀", "1": "₁", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆",
        "7": "₇", "8": "₈", "9": "₉", "+": "₊", "-": "₋", "=": "₌", "(": "₍",
        ")": "₎", "a": "ₐ", "e": "ₑ", "h": "ₕ", "i": "ᵢ", "j": "ⱼ", "k": "ₖ",
        "l": "ₗ", "m": "ₘ", "n": "ₙ", "o": "ₒ", "p": "ₚ", "r": "ᵣ", "s": "ₛ",
        "t": "ₜ", "u": "ᵤ", "v": "ᵥ", "x": "ₓ"}


def _to_script(group, table):
    out = []
    for ch in group:
        if ch in table:
            out.append(table[ch])
        else:
            return None  # un-mappable -> caller keeps a readable fallback
    return "".join(out)


# Solution/question fields that MUST be lists-of-strings. If a generator emits one
# as a bare string, naive `for x in field` iterates it CHARACTER-BY-CHARACTER — the
# formula renders one glyph per line ("messed up / unreadable"). normalize_paper
# coerces them so every builder is immune regardless of how the JSON was authored.
_STR_LIST_FIELDS_SOL = ("formula", "calculation", "given", "check",
                        "solution_diagram_prompts")
_STR_LIST_FIELDS_Q = ("options", "diagram_prompts")


def _repair_where(where):
    """`where` must be a list of {sym, def, unit} dicts. Generators sometimes mangle
    it: a bare string, a list of plain strings, or — the nasty one — a string
    EXPLODED into one dict PER CHARACTER ([{def:'r'},{def:' '},{def:'i'},...]) which
    renders as a column of single-letter bullets. Normalise all three back."""
    if isinstance(where, str):
        return [{"sym": "", "def": where, "unit": ""}]
    if not isinstance(where, list) or not where:
        return where
    if all(isinstance(x, str) for x in where):                  # list of plain strings
        return [{"sym": "", "def": x, "unit": ""} for x in where]
    if all(isinstance(x, dict) for x in where) and len(where) >= 5:
        short = sum(1 for e in where
                    if len(str(e.get("def", "")).strip()) <= 1 and not str(e.get("sym", "")).strip())
        if short >= len(where) * 0.6:                           # per-character explosion
            joined = "".join(str(e.get("def", "")) for e in where).strip()
            return [{"sym": "", "def": joined, "unit": ""}]
    return where


def normalize_paper(spec):
    """In-place: wrap any list-typed field authored as a bare string into [string],
    and repair mangled `where` fields. Call once at the top of each builder's
    build() (covers _collect_math too)."""
    for sec in (spec.get("sections") or []):
        for q in (sec.get("questions") or []):
            for f in _STR_LIST_FIELDS_Q:
                if isinstance(q.get(f), str):
                    q[f] = [q[f]]
            sol = q.get("solution")
            if isinstance(sol, dict):
                for f in _STR_LIST_FIELDS_SOL:
                    if isinstance(sol.get(f), str):
                        sol[f] = [sol[f]]
                if sol.get("where") is not None:
                    sol["where"] = _repair_where(sol["where"])
    return spec


def render_math(text):
    """Convert a light, constrained math markup into clean Unicode.

    Supported (documented in references/question_architecture.md):
      \\frac{a}{b} -> (a)/(b)     \\sqrt{x} -> √(x)      \\omega, \\Omega ... -> Greek
      x^{ab} / x^2 -> superscript     V_{th} / I_2 -> subscript
      \\times \\cdot \\div \\pm \\leq \\geq \\neq \\approx \\infty \\int \\sum ... -> symbols
    Plain prose with none of these tokens is returned unchanged.
    """
    if not text:
        return text
    s = str(text)

    # LaTeX spacing commands (\, \; \: \! and backslash-space) -> a normal space
    s = re.sub(r"\\[,;:!]", " ", s)
    s = re.sub(r"\\ ", " ", s)
    # multiplication asterisk -> × ; brace multi-char sub/superscripts so they render whole
    s = re.sub(r"(?<=[\w)])\s*\*\s*(?=[\w(\\])", " × ", s)
    s = re.sub(r"([_^])([A-Za-z0-9]{2,})", r"\1{\2}", s)

    # BRACED sub/superscripts FIRST — this collapses inner braces (e.g. N_{s}) to
    # Unicode, so a later \frac{N_s - N_r}{N_s} sees brace-free groups and matches.
    s = re.sub(r"\^\{([^{}]*)\}", lambda m: (_to_script(m.group(1), _SUP) or f"^({m.group(1)})"), s)
    s = re.sub(r"_\{([^{}]*)\}", lambda m: (_to_script(m.group(1), _SUB) or f"_{m.group(1)}"), s)

    # Symbols + Greek BEFORE accents/fractions. Accents collapse brace boundaries
    # (\mu\vec{H} -> \muH), and the Greek lookahead (?![A-Za-z]) would then refuse to
    # convert \mu because it is glued to a letter. Converting here (while \mu is still
    # followed by '\') keeps it working: \mu\vec{H} -> μ\vec{H} -> μH⃗.
    for cmd, rep in sorted(_SYMBOL.items(), key=lambda kv: -len(kv[0])):
        s = s.replace(cmd, rep)
    # use a not-a-letter lookahead (not \b): '_' is a word char, so \eta_0 / \eta_{s}
    # would fail with \b — the lookahead lets the Greek letter convert regardless.
    for name, rep in sorted(_GREEK.items(), key=lambda kv: -len(kv[0])):
        s = re.sub(r"\\" + name + r"(?![A-Za-z])", rep, s)

    # accents BEFORE fractions: \vec{E} -> E⃗, \hat{n} -> n̂, \bar{x} -> x̄ (mark after the
    # char). Must run before \frac/\sqrt so their braces are gone and the frac groups
    # below stay brace-free (e.g. \frac{Id\vec{l}\times\hat{r}}{r^2}).
    for _cmd, _mk in _ACCENTS.items():
        s = re.sub(r"\\" + _cmd + r"\s*\{([^{}]*)\}", lambda m, k=_mk: m.group(1) + k, s)
        s = re.sub(r"\\" + _cmd + r"(?![A-Za-z])\s*([A-Za-z])", lambda m, k=_mk: m.group(1) + k, s)

    # fractions: \frac{a}{b} -> (a)/(b)  (groups are now brace-free)
    s = re.sub(r"\\frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}",
               lambda m: f"({m.group(1)})/({m.group(2)})", s)
    # roots: \sqrt{x} -> √(x) ; \sqrt x -> √x
    s = re.sub(r"\\sqrt\s*\{([^{}]*)\}", lambda m: f"√({m.group(1)})", s)
    s = re.sub(r"\\sqrt\s+(\w+)", lambda m: f"√{m.group(1)}", s)

    # bare super/subscripts: ^2, ^n, ^-, and P_o / I_2 at a word boundary
    # ('per_unit' is left alone since 'u' is followed by more letters).
    s = re.sub(r"\^(-?\w)", lambda m: (_to_script(m.group(1), _SUP) or f"^{m.group(1)}"), s)
    s = re.sub(r"_([A-Za-z0-9])(?![A-Za-z0-9])",
               lambda m: _SUB.get(m.group(1), f"_{m.group(1)}"), s)

    return s


# ----------------------------- value signature ----------------------------
_NUM = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")


def _numbers(*texts):
    found = []
    for t in texts:
        if t is None:
            continue
        if isinstance(t, (list, tuple)):
            found += _numbers(*t)
            continue
        for tok in _NUM.findall(str(t)):
            try:
                f = float(tok)
            except ValueError:
                continue
            # normalise -0.0, and to a short repr so 4 and 4.0 collide
            f = round(f, 6) + 0.0
            found.append(f)
    return found


def value_signature(q):
    """Canonical signature of the EXACT numeric dataset of a question.

    Built from the stem text, the options, and the solution's given data — the
    numbers a student actually works with. Same concept + different numbers ->
    different signature (allowed). Same numbers -> same signature (a repeat)."""
    sol = q.get("solution") or {}
    nums = _numbers(q.get("text"), q.get("options"), sol.get("given"))
    if not nums:
        return ""  # no numeric dataset (pure-theory item) -> not value-deduped
    nums_sorted = sorted(nums)
    return "|".join(f"{n:g}" for n in nums_sorted)


def repeat_key(q):
    """Granularity at which an EXACT-VALUE repeat is judged: same subject + chapter/topic
    + type + identical number multiset. Returns None for pure-theory items (no numbers)."""
    sig = value_signature(q)
    if not sig:
        return None
    subj = (q.get("subject") or "").strip().lower()
    chap = (q.get("chapter") or q.get("topic") or "").strip().lower()
    typ = (q.get("type") or "").strip().upper()
    return (subj, chap, typ, sig)


# --------------------------- template / structure signature ----------------
# The VALUE signature above blocks only EXACT-NUMBER repeats. It deliberately
# treats "same question, fresh numbers" as fine. That is exactly the loophole
# that lets one template (especially one diagram) be re-skinned across an entire
# mock series. The TEMPLATE signature closes it: it captures the question's
# *structure* with all numbers removed, so "4Ohm in series with 6||3" and
# "5Ohm in series with 10||10" collapse to the SAME signature. The validator
# then caps how many times a template may recur across the series.
_WORD = re.compile(r"[a-z]+")
# structural words that define a circuit/figure topology (kept) vs prose noise (dropped)
_TOPOLOGY_STOP = {
    "the", "a", "an", "of", "in", "on", "at", "to", "and", "or", "with", "from",
    "is", "are", "be", "as", "by", "for", "shown", "figure", "diagram", "circuit",
    "create", "clean", "labelled", "labeled", "showing", "show", "draw", "image",
    "below", "above", "following", "given", "find", "value", "values", "clear",
    "neat", "schematic", "please", "such", "that", "which", "this", "these",
}


def _structural_skeleton(text):
    """Lowercase a string, drop ALL numbers/units/punctuation, keep the ordered
    alphabetic word stream — the structural skeleton independent of values."""
    s = str(text or "").lower()
    s = re.sub(r"\$[^$]*\$", " ", s)          # strip inline math blocks wholesale
    s = re.sub(r"\\[a-z]+", " ", s)           # latex commands
    s = re.sub(r"[-+]?\d[\d,\.]*", " ", s)     # every number
    return " ".join(_WORD.findall(s))


def _diagram_text(q):
    """All diagram-prompt content attached to a question (question + solution),
    concatenated. Empty string for non-figure questions."""
    tags = list(q.get("diagram_prompts") or [])
    sol = q.get("solution") or {}
    tags += list(sol.get("solution_diagram_prompts") or [])
    return " ".join(gemini_inner(t) for t in tags).strip()


def has_diagram(q):
    """True if the question carries any [GEMINI_FLASH_PROMPT] diagram."""
    return bool(_diagram_text(q))


def template_signature(q):
    """Structural fingerprint of a question with ALL numbers removed.

    Built from the stem text AND any diagram-prompt topology, with the
    subject/chapter/type identity folded INTO the hash, so two questions that
    differ only in their numeric values (same wording, same circuit, same tag)
    share ONE bare-string signature. Folding the identity in (rather than
    returning a tuple) makes the signature format-independent: the value stored
    in the log and the value recomputed at validation time match exactly, with
    no chapter-name-format drift. This is what catches "same template, different
    values" — the thing the value signature is designed to ignore. Returns "" if
    there is no structural content to hash."""
    skeleton = _structural_skeleton(q.get("text"))
    dia = _structural_skeleton(_diagram_text(q))
    combined = (skeleton + " || " + dia).strip(" |")
    if not combined:
        return ""
    subj = (q.get("subject") or "").strip().lower()
    chap = (q.get("chapter") or q.get("topic") or "").strip().lower()
    typ = (q.get("type") or "").strip().upper()
    import hashlib
    key = subj + "|" + chap + "|" + typ + "|" + combined
    return hashlib.md5(key.encode("utf-8")).hexdigest()[:16]


def template_key(q):
    """The bare template_signature (identity already folded in) — the granularity
    at which TEMPLATE over-reuse is judged across a mock series. None if empty."""
    return template_signature(q) or None


def diagram_signature(q):
    """Structural fingerprint of a question's DIAGRAM TOPOLOGY only — number-free,
    prose-noise stripped down to the connective structure words (series, parallel,
    bridge, source, node ...). Two figure questions that show the same circuit with
    different values share ONE diagram signature. Returns "" for non-figure items."""
    dia = _diagram_text(q)
    if not dia:
        return ""
    words = [w for w in _structural_skeleton(dia).split() if w not in _TOPOLOGY_STOP]
    if not words:
        return ""
    import hashlib
    # order-independent topology: the SET of structural words (a relabelled but
    # identical circuit still collides) keyed under subject/topic.
    subj = (q.get("subject") or "").strip().lower()
    chap = (q.get("chapter") or q.get("topic") or "").strip().lower()
    body = " ".join(sorted(set(words)))
    return hashlib.md5((subj + "|" + chap + "|" + body).encode("utf-8")).hexdigest()[:16]


# ----------------------------- safe arithmetic eval ------------------------
_ALLOWED_FUNCS = {
    "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
    "log": math.log, "log10": math.log10, "log2": math.log2, "exp": math.exp,
    "abs": abs, "radians": math.radians, "degrees": math.degrees,
    "floor": math.floor, "ceil": math.ceil, "pow": pow, "round": round,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh, "hypot": math.hypot,
    "max": max, "min": min,
}
_ALLOWED_NAMES = {"pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf}


def safe_eval_number(expr):
    """Evaluate a pure-arithmetic expression. Allows + - * / // % ** , parentheses,
    a whitelist of math functions, and the constants pi/e/tau. Raises ValueError on
    anything else (names, attributes, calls to non-whitelisted funcs)."""
    expr = str(expr).strip()
    node = ast.parse(expr, mode="eval")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError(f"non-numeric constant: {n.value!r}")
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            op = n.op
            if isinstance(op, ast.Add):
                return a + b
            if isinstance(op, ast.Sub):
                return a - b
            if isinstance(op, ast.Mult):
                return a * b
            if isinstance(op, ast.Div):
                return a / b
            if isinstance(op, ast.FloorDiv):
                return a // b
            if isinstance(op, ast.Mod):
                return a % b
            if isinstance(op, ast.Pow):
                return a ** b
            raise ValueError(f"operator not allowed: {type(op).__name__}")
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            if isinstance(n.op, ast.UAdd):
                return +v
            if isinstance(n.op, ast.USub):
                return -v
            raise ValueError("unary op not allowed")
        if isinstance(n, ast.Call):
            if not isinstance(n.func, ast.Name) or n.func.id not in _ALLOWED_FUNCS:
                raise ValueError("only whitelisted math functions allowed")
            return _ALLOWED_FUNCS[n.func.id](*[ev(a) for a in n.args])
        if isinstance(n, ast.Name):
            if n.id in _ALLOWED_NAMES:
                return _ALLOWED_NAMES[n.id]
            raise ValueError(f"name not allowed: {n.id}")
        raise ValueError(f"syntax not allowed: {type(n).__name__}")

    return float(ev(node))


# ----------------------------- answer helpers ------------------------------
def option_letters(options):
    """Letters actually present in an options list. Accepts '(A) ...', 'A) ...',
    'A. ...', 'A ...'."""
    out = []
    for opt in options or []:
        m = re.match(r"\s*\(?([A-Za-z])\)?[\.\)]?\s+", str(opt))
        if m:
            out.append(m.group(1).upper())
    return out


_OPT_LABEL = re.compile(r"^\s*\(?\s*[A-Za-z]\s*[\)\.]\s*")


def option_value(opt):
    """Strip a leading option label ('(A) ', 'A) ', 'A. ') -> just the option value."""
    return _OPT_LABEL.sub("", str(opt)).strip()


def answer_letters(answer):
    """Letters claimed by an answer like 'B' or 'B, D' or 'A and C'."""
    return [c.upper() for c in re.findall(r"[A-Za-z]", str(answer or ""))
            if c.upper() in "ABCDEFGH"]


def parse_range(answer):
    """NAT answer band. 'x to y' / 'x - y' / 'x–y' -> (x,y); single 'x' -> (x,x).
    Returns None if no number found."""
    a = str(answer or "").strip()
    m = re.search(r"([-+]?\d*\.?\d+)\s*(?:to|–|—|-)\s*([-+]?\d*\.?\d+)", a)
    if m:
        lo, hi = float(m.group(1)), float(m.group(2))
        return (min(lo, hi), max(lo, hi))
    n = first_number(a)
    if n is None:
        return None
    return (n, n)


def first_number(text):
    m = _NUM.search(str(text or ""))
    return float(m.group()) if m else None


# ----------------------------- gemini image prompts ------------------------
# Uniform style guidance appended to EVERY diagram prompt so all generated images
# look consistent. Authors write only the diagram content; builders append this.
GEMINI_STYLE = (
    "Font Family: Segoe UI (apply to all text, labels, legends and titles). "
    "Font Size: 11 pt exactly. "
    "Line Weight/Thickness: 1 pt exactly (apply to all borders, connecting lines, arrows and shapes). "
    "Colors: use a clean, high-contrast palette and render in crisp black and white. "
    "Clarity: ensure all text is legible and does not overlap with lines or shapes; "
    "ensure all arrows and connectors point exactly where described. "
    "Output Format: generate the final output as JPEG."
)


def gemini_inner(tag):
    """Strip the [GEMINI_FLASH_PROMPT: ...] wrapper, return the inner content."""
    inner = str(tag).strip()
    if inner.upper().startswith("[GEMINI_FLASH_PROMPT") and inner.endswith("]"):
        inner = inner[inner.find(":") + 1: -1].strip()
    return inner


def gemini_prompt(tag):
    """Full, ready-to-paste Gemini prompt = the diagram content + the uniform style block."""
    inner = gemini_inner(tag).rstrip()
    if inner and inner[-1] not in ".!?":
        inner += "."
    return (inner + " " + GEMINI_STYLE).strip()


# ----------------------------- fs helpers ----------------------------------
_BAD = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def safe_output_path(path):
    """Sanitise only the filename part (Windows-illegal chars -> '-'); keep the dir."""
    d, base = os.path.split(str(path))
    base = _BAD.sub("-", base).strip().rstrip(". ")
    if not base:
        base = "output"
    return os.path.join(d, base) if d else base
