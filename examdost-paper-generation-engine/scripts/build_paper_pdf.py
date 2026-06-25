"""
build_paper_pdf.py — render a generated paper (paper.json) as a branded PDF
question bank.

Usage:
    python build_paper_pdf.py <paper.json> <output.pdf>

Honours meta.layout ("combined" | "split"), meta.metadata_tags, meta.show_solutions,
and renders [GEMINI_FLASH_PROMPT: ...] tags as labelled placeholder boxes. Schema:
references/paper_spec_schema.md.

Dependencies: reportlab.
"""
from __future__ import annotations

import json
import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Flowable, Frame, KeepTogether, PageBreak,
    PageTemplate, Paragraph, Spacer, Table, TableStyle,
)

import paperlib as P


def _register_unicode_font():
    """Embed a Unicode TTF (DejaVu Sans) so Greek/subscripts/√/Ω/≈ render instead of
    boxes. reportlab's built-in Helvetica is Latin-only. Falls back to Helvetica."""
    fam = {"normal": "DejaVuSans.ttf", "bold": "DejaVuSans-Bold.ttf",
           "italic": "DejaVuSans-Oblique.ttf", "bolditalic": "DejaVuSans-BoldOblique.ttf"}
    dirs = []
    try:
        import matplotlib
        dirs.append(os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf"))
    except Exception:
        pass
    dirs += [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/dejavu",
             "/usr/share/fonts", "/Library/Fonts"]
    found = {}
    for style, fn in fam.items():
        for d in dirs:
            pth = os.path.join(d, fn)
            if os.path.exists(pth):
                found[style] = pth
                break
    if "normal" not in found:
        return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"
    nrm, bold = found["normal"], found.get("bold", found["normal"])
    ital, bi = found.get("italic", found["normal"]), found.get("bolditalic", found.get("bold", found["normal"]))
    pdfmetrics.registerFont(TTFont("UFont", nrm))
    pdfmetrics.registerFont(TTFont("UFont-Bold", bold))
    pdfmetrics.registerFont(TTFont("UFont-Italic", ital))
    pdfmetrics.registerFont(TTFont("UFont-BoldItalic", bi))
    pdfmetrics.registerFontFamily("UFont", normal="UFont", bold="UFont-Bold",
                                  italic="UFont-Italic", boldItalic="UFont-BoldItalic")
    return "UFont", "UFont-Bold", "UFont-Italic"


_BASE, _BOLD, _ITAL = _register_unicode_font()

TEAL = colors.HexColor("#0F8B8D")
NAVY = colors.HexColor("#1F2A44")
AMBER = colors.HexColor("#D97706")
GREEN = colors.HexColor("#16A34A")
GREY = colors.HexColor("#6B7280")
INK = colors.HexColor("#2A2F3A")
TINT_TEAL = colors.HexColor("#E6F4F4")
TINT_GREY = colors.HexColor("#F4F4F6")
TINT_AMBER = colors.HexColor("#FFF4E0")
WHITE = colors.white

PAGE_W, PAGE_H = A4
MARGIN = 16 * mm
CONTENT_W = PAGE_W - 2 * MARGIN


def _styles():
    s = {}
    s["kicker"] = ParagraphStyle("k", fontName=_BOLD, fontSize=9,
                                 textColor=TEAL, leading=11)
    s["title"] = ParagraphStyle("t", fontName=_BOLD, fontSize=19,
                                textColor=NAVY, leading=22, spaceAfter=2)
    s["meta"] = ParagraphStyle("m", fontName=_BASE, fontSize=9, textColor=GREY,
                               leading=12)
    s["secband"] = ParagraphStyle("sb", fontName=_BOLD, fontSize=12.5,
                                  textColor=WHITE, leading=15)
    s["part"] = ParagraphStyle("pt", fontName=_BOLD, fontSize=13.5,
                              textColor=TEAL, leading=16, spaceBefore=2, spaceAfter=3)
    s["stem"] = ParagraphStyle("st", fontName=_BASE, fontSize=10.5, textColor=INK,
                              leading=14, spaceBefore=3, spaceAfter=1)
    s["opt"] = ParagraphStyle("o", fontName=_BASE, fontSize=10.5, textColor=INK,
                             leading=13.5, leftIndent=10)
    s["meta_q"] = ParagraphStyle("mq", fontName=_ITAL, fontSize=8.5,
                                textColor=GREY, leading=11, leftIndent=10)
    s["ans"] = ParagraphStyle("a", fontName=_BASE, fontSize=10, textColor=INK,
                             leading=13, leftIndent=6, spaceBefore=2)
    s["solhdr"] = ParagraphStyle("sh", fontName=_BOLD, fontSize=9.5,
                                textColor=NAVY, leading=12.5, leftIndent=14)
    s["solline"] = ParagraphStyle("sl", fontName=_BASE, fontSize=9.5, textColor=INK,
                                 leading=12.5, leftIndent=24)
    s["box"] = ParagraphStyle("bx", fontName=_ITAL, fontSize=9, textColor=INK,
                             leading=12)
    s["instr"] = ParagraphStyle("in", fontName=_BASE, fontSize=10, textColor=INK,
                               leading=13, leftIndent=8)
    return s


S = _styles()


# Authored literal "\n" line breaks (statement / assertion-reason stems) -> <br/>.
# Only before an uppercase letter, digit, or space — \nabla, \nu (lowercase) are
# real commands (already turned to symbols by render_math) and stay untouched.
_PDF_BREAK = re.compile(r"\\n(?=[A-Z0-9]|\s)")


def _esc(t):
    t = str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return _PDF_BREAK.sub("<br/>", t)


class Rule(Flowable):
    def __init__(self, width, colour=TEAL, thickness=1.4):
        super().__init__()
        self.width, self.colour, self.thickness = width, colour, thickness

    def wrap(self, *a):
        return (self.width, self.thickness + 4)

    def draw(self):
        self.canv.setStrokeColor(self.colour)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 2, self.width, 2)


def section_band(title):
    t = Table([[Paragraph("&nbsp;" + _esc(title), S["secband"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [Spacer(1, 4), t, Spacer(1, 3)]


def diagram_box(prompt, label="[ DIAGRAM — Gemini prompt ]"):
    inner = P.gemini_prompt(prompt)
    body = f"<b><font color='#D97706'>{label}</font></b>&nbsp; {_esc(inner)}"
    t = Table([[Paragraph(body, S["box"])]], colWidths=[CONTENT_W - 8])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TINT_AMBER),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBEFORE", (0, 0), (0, -1), 3, AMBER),
    ]))
    return [Spacer(1, 2), t, Spacer(1, 2)]


def _diagrams(prompts):
    out = []
    for p in prompts or []:
        out += diagram_box(p)
    return out


def meta_line(q, tags):
    if not tags:
        return []
    label_map = {"Subject": "subject", "Chapter": "chapter", "Topic": "topic",
                 "Marks": "marks", "Type": "type"}
    parts = []
    for tag in tags:
        key = label_map.get(tag)
        if key and q.get(key) not in (None, ""):
            parts.append(f"{tag}: {q.get(key)}")
    if not parts:
        return []
    return [Paragraph(_esc("   ".join(parts)), S["meta_q"])]


def stem_flow(q):
    wild = "<b><font color='#D97706'>[WILDCARD]</font></b> " if q.get("is_wildcard") else ""
    mk = q.get("marks")
    mtxt = ""
    if mk not in (None, ""):
        mtxt = f"&nbsp;&nbsp;<font color='#6B7280' size=8><b>[{mk} mark{'s' if str(mk) != '1' else ''}]</b></font>"
    head = (f"<b><font color='#0F8B8D'>Q{q.get('number','')}.</font></b>&nbsp; "
            f"{wild}{_esc(P.render_math(q.get('text','')))}{mtxt}")
    flow = [Paragraph(head, S["stem"])]
    flow += _diagrams(q.get("diagram_prompts"))
    flow += _image_flow(q.get("image"))
    for opt in q.get("options") or []:
        flow.append(Paragraph(_esc(P.render_math(opt)), S["opt"]))
    return flow


def _image_flow(path, width_mm=110):
    """Embed an actual rendered diagram image (PNG), centred, sized to width."""
    if not path or not os.path.exists(path):
        return []
    try:
        from reportlab.platypus import Image as RLImage
        from PIL import Image as PILImage
        iw, ih = PILImage.open(path).size
        w = width_mm * mm
        h = w * ih / iw
        img = RLImage(path, width=w, height=h)
        img.hAlign = "CENTER"
        return [Spacer(1, 3), img, Spacer(1, 3)]
    except Exception:
        return []


def answer_solution_flow(q, show_solutions):
    flow = [Paragraph(f"<b><font color='#16A34A'>Answer Key:</font></b>&nbsp; "
                      f"<b>{_esc(P.render_math(q.get('answer','')))}</b>", S["ans"])]
    sol = q.get("solution") or {}
    rich = bool(sol.get("concept") or sol.get("where") or sol.get("option_analysis"))
    if not rich and q.get("concept"):
        flow.append(Paragraph(f"<b><font color='#0F8B8D'>Concept:</font></b>&nbsp; "
                              f"{_esc(P.render_math(q['concept']))}", S["ans"]))
    if not show_solutions or not sol:
        return flow
    flow += (_rich_solution_flow(q, sol) if rich else _legacy_solution_flow(sol))
    flow += _diagrams(sol.get("solution_diagram_prompts"))
    return flow


def _rich_solution_flow(q, sol):
    flow = [Paragraph("<b><font color='#1F2A44'>Detailed Solution</font></b>", S["ans"]),
            Paragraph("<b><font color='#0F8B8D'>1. Core Concept &amp; Formula</font></b>", S["solhdr"])]
    concept = sol.get("concept") or q.get("concept")
    if concept:
        flow.append(Paragraph(_esc(P.render_math(concept)), S["solline"]))
    for f in sol.get("formula") or []:
        flow.append(Paragraph(_esc(P.render_math(f)), S["solline"]))
    where = sol.get("where") or []
    if where:
        flow.append(Paragraph("<b>Where:</b>", S["solhdr"]))
        for g in where:
            unit = f"&nbsp;({_esc(g['unit'])})" if g.get("unit") else ""
            sym = str(g.get("sym", "")).strip()
            lead = f"<b>{_esc(P.render_math(sym))}</b> = " if sym else ""
            flow.append(Paragraph(f"•&nbsp; {lead}"
                                  f"{_esc(P.render_math(g.get('def','')))}{unit}", S["solline"]))
    opts = sol.get("option_analysis") or []
    calc = sol.get("calculation") or []
    if opts:
        flow.append(Paragraph("<b><font color='#0F8B8D'>2. Evaluating the Options</font></b>", S["solhdr"]))
        for o in opts:
            col = "#16A34A" if o.get("correct") else "#C0392B"
            flow.append(Paragraph(f"<b><font color='{col}'>({_esc(o.get('option',''))})</font></b> "
                                  f"{_esc(P.render_math(o.get('text','')))}", S["solline"]))
    elif calc:
        flow.append(Paragraph("<b><font color='#0F8B8D'>2. Calculation Steps</font></b>", S["solhdr"]))
        for line in calc:
            flow.append(Paragraph(_esc(P.render_math(line)), S["solline"]))
    if sol.get("final_answer"):
        flow.append(Paragraph(f"<b><font color='#16A34A'>Final Answer:</font></b>&nbsp; "
                              f"<b>{_esc(P.render_math(sol['final_answer']))}</b>", S["ans"]))
    return flow


def _legacy_solution_flow(sol):
    flow = [Paragraph("<b><font color='#1F2A44'>Solution:</font></b>", S["ans"])]
    flow += _step("Step 1 — Given Data", sol.get("given"))
    flow += _step("Step 2 — Governing Formula", sol.get("formula"))
    flow += _step("Step 3 — Line-by-Line Calculation", sol.get("calculation"))
    if sol.get("final_answer"):
        flow.append(Paragraph(f"<b><font color='#16A34A'>Step 4 — Final Answer:</font></b>&nbsp; "
                              f"<b>{_esc(P.render_math(sol['final_answer']))}</b>", S["solhdr"]))
    return flow


def _step(label, payload):
    if payload in (None, "", []):
        return []
    out = [Paragraph(f"{_esc(label)}:", S["solhdr"])]
    items = payload if isinstance(payload, list) else [payload]
    for it in items:
        out.append(Paragraph(_esc(P.render_math(it)), S["solline"]))
    return out


def answer_key_table(questions):
    flow = [Paragraph("Quick Answer Key", S["part"])]
    ncols = 4
    cells = [[f"Q{q.get('number','')}", str(q.get("answer", ""))] for q in questions]
    rows = (len(cells) + ncols - 1) // ncols
    grid = [["", "", "", "", "", "", "", ""] for _ in range(rows)]
    for idx, (qn_, an) in enumerate(cells):
        r = idx % rows
        c = (idx // rows) * 2
        grid[r][c] = Paragraph(f"<b>{_esc(qn_)}</b>", S["box"])
        grid[r][c + 1] = Paragraph(_esc(an), S["box"])
    cw = CONTENT_W / 8
    t = Table(grid, colWidths=[cw * 0.8, cw * 1.2] * 4)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8E6E6")),
        ("BACKGROUND", (0, 0), (0, -1), TINT_TEAL),
        ("BACKGROUND", (2, 0), (2, -1), TINT_TEAL),
        ("BACKGROUND", (4, 0), (4, -1), TINT_TEAL),
        ("BACKGROUND", (6, 0), (6, -1), TINT_TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ]))
    flow.append(t)
    flow.append(Spacer(1, 6))
    return flow


def header_flow(meta):
    flow = [Paragraph("EXAMDOST &nbsp;·&nbsp; GENERATED QUESTION BANK", S["kicker"])]
    flow.append(Paragraph(_esc(P.render_math(meta.get("paper_title") or meta.get("exam", "Question Paper"))), S["title"]))
    bits = []
    for k, suf in [("exam", ""), ("total_questions", " Questions"), ("total_marks", " Marks"),
                   ("duration_min", " min")]:
        if meta.get(k):
            bits.append(f"{meta[k]}{suf}")
    if meta.get("organising_institute"):
        bits.append(f"Organising: {meta['organising_institute']}")
    if meta.get("generated_on"):
        bits.append(f"Generated {meta['generated_on']}")
    flow.append(Paragraph(_esc("    |    ".join(str(b) for b in bits)), S["meta"]))
    instr = meta.get("instructions") or []
    if instr:
        flow.append(Spacer(1, 3))
        flow.append(Paragraph("<b><font color='#0F8B8D'>Instructions</font></b>", S["ans"]))
        for line in instr:
            flow.append(Paragraph("•&nbsp; " + _esc(P.render_math(line)), S["instr"]))
    flow.append(Rule(CONTENT_W))
    return flow


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(TINT_GREY)
    canvas.setLineWidth(0.6)
    canvas.line(MARGIN, 11 * mm, PAGE_W - MARGIN, 11 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont(_BASE, 7.5)
    canvas.drawString(MARGIN, 7 * mm, f"ExamDost — {_footer.exam}")
    canvas.drawRightString(PAGE_W - MARGIN, 7 * mm, f"Page {doc.page}")
    canvas.restoreState()


_footer.exam = "Generated Paper"


def build(spec, out_path):
    P.normalize_paper(spec)        # coerce string formula/calc fields -> lists
    out_path = P.safe_output_path(out_path)
    meta = spec.get("meta", {})
    _footer.exam = meta.get("exam", "Generated Paper")
    layout = (meta.get("layout") or "combined").lower()
    show_solutions = meta.get("show_solutions", True)
    tags = meta.get("metadata_tags") or []
    sections = spec.get("sections", [])

    doc = BaseDocTemplate(out_path, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=15 * mm,
                          title=meta.get("paper_title", "Question Bank"), author="ExamDost")
    frame = Frame(MARGIN, 15 * mm, CONTENT_W, PAGE_H - MARGIN - 15 * mm, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=_footer)])

    story = header_flow(meta)

    if layout == "split":
        story.append(Paragraph("QUESTION PAPER", S["part"]))
        all_q = []
        for sec in sections:
            story += section_band(sec.get("section", "Section"))
            for q in sec.get("questions", []):
                story.append(KeepTogether(stem_flow(q) + [Spacer(1, 3)]))
                all_q.append(q)
        story.append(PageBreak())
        story.append(Paragraph("ANSWER KEY &amp; SOLUTIONS", S["part"]))
        story += answer_key_table(all_q)
        story.append(Rule(CONTENT_W))
        for sec in sections:
            story += section_band(sec.get("section", "Section") + " — Solutions")
            for q in sec.get("questions", []):
                head = (f"<b><font color='#0F8B8D'>Q{q.get('number','')}.</font></b>&nbsp; "
                        f"{_esc(P.render_math(q.get('text','')))}")
                blk = [Paragraph(head, S["stem"])] + answer_solution_flow(q, show_solutions) + [Spacer(1, 4)]
                story.append(KeepTogether(blk))
    else:
        for sec in sections:
            story += section_band(sec.get("section", "Section"))
            for q in sec.get("questions", []):
                blk = stem_flow(q) + answer_solution_flow(q, show_solutions) + [Spacer(1, 5)]
                story.append(KeepTogether(blk))

    doc.build(story)
    nq = sum(len(s.get("questions", [])) for s in sections)
    print(f"Wrote {out_path}  ({nq} questions, layout={layout}, solutions={'on' if show_solutions else 'off'})")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    build(spec, sys.argv[2])


if __name__ == "__main__":
    main()
