from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps


W, H = 1200, 700
BLACK = "#000000"
WHITE = "#ffffff"
LINE = 4  # approximately 1 pt when inserted at the target Word width
FONT_PATH = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_BOLD_PATH = Path(r"C:\Windows\Fonts\segoeuib.ttf")
FONT_SIZE = 42  # approximately 11 pt at the generated resolution
FONT = ImageFont.truetype(str(FONT_PATH), FONT_SIZE)
FONT_SMALL = ImageFont.truetype(str(FONT_PATH), 29)
FONT_BOLD = ImageFont.truetype(str(FONT_BOLD_PATH), FONT_SIZE)


def new_canvas(height: int = H) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (W, height), WHITE)
    return image, ImageDraw.Draw(image)


def line(draw: ImageDraw.ImageDraw, points, width: int = LINE) -> None:
    draw.line(points, fill=BLACK, width=width, joint="curve")


def dot(draw: ImageDraw.ImageDraw, x: int, y: int, r: int = 9) -> None:
    draw.ellipse((x - r, y - r, x + r, y + r), fill=BLACK)


def text_width(draw: ImageDraw.ImageDraw, text: str, font=FONT) -> float:
    return draw.textlength(text, font=font)


def math_tokens(text: str):
    i = 0
    plain = ""
    while i < len(text):
        if text[i] not in "_^":
            plain += text[i]
            i += 1
            continue
        if plain:
            yield "base", plain
            plain = ""
        mode = "sub" if text[i] == "_" else "sup"
        i += 1
        if i < len(text) and text[i] == "{":
            end = text.find("}", i + 1)
            if end < 0:
                end = len(text)
            value = text[i + 1 : end]
            i = min(end + 1, len(text))
        elif i < len(text):
            value = text[i]
            i += 1
        else:
            value = ""
        yield mode, value
    if plain:
        yield "base", plain


def draw_math(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    *,
    anchor: str = "la",
    bold: bool = False,
) -> tuple[int, int, int, int]:
    base_font = FONT_BOLD if bold else FONT
    tokens = list(math_tokens(text))
    widths = [text_width(draw, value, FONT_SMALL if mode != "base" else base_font) for mode, value in tokens]
    total = sum(widths)
    x, y = xy
    if anchor.startswith("m"):
        x -= total / 2
    elif anchor.startswith("r"):
        x -= total
    start_x = x
    for (mode, value), width in zip(tokens, widths):
        if mode == "base":
            draw.text((x, y), value, font=base_font, fill=BLACK, anchor="la")
        elif mode == "sub":
            draw.text((x, y + 22), value, font=FONT_SMALL, fill=BLACK, anchor="la")
        else:
            draw.text((x, y - 12), value, font=FONT_SMALL, fill=BLACK, anchor="la")
        x += width
    return int(start_x), y - 14, int(start_x + total), y + 55


def ground(draw: ImageDraw.ImageDraw, x: int, y: int) -> None:
    line(draw, [(x, y - 40), (x, y)])
    line(draw, [(x - 32, y), (x + 32, y)])
    line(draw, [(x - 22, y + 11), (x + 22, y + 11)])
    line(draw, [(x - 11, y + 22), (x + 11, y + 22)])


def resistor_h(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int) -> None:
    lead = 48
    line(draw, [(x1, y), (x1 + lead, y)])
    line(draw, [(x2 - lead, y), (x2, y)])
    n = 8
    span = x2 - x1 - 2 * lead
    pts = [(x1 + lead, y)]
    for i in range(1, n + 1):
        x = x1 + lead + span * i / n
        yy = y + (-1 if i % 2 else 1) * 24
        pts.append((x, yy))
    pts.append((x2 - lead, y))
    line(draw, pts)


def resistor_v(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int) -> None:
    lead = 42
    line(draw, [(x, y1), (x, y1 + lead)])
    line(draw, [(x, y2 - lead), (x, y2)])
    n = 8
    span = y2 - y1 - 2 * lead
    pts = [(x, y1 + lead)]
    for i in range(1, n + 1):
        y = y1 + lead + span * i / n
        xx = x + (-1 if i % 2 else 1) * 24
        pts.append((xx, y))
    pts.append((x, y2 - lead))
    line(draw, pts)


def diode_h(draw: ImageDraw.ImageDraw, x1: int, x2: int, y: int) -> None:
    mid = (x1 + x2) // 2
    line(draw, [(x1, y), (mid - 40, y)])
    bar_x = mid + 26
    line(draw, [(bar_x, y), (x2, y)])
    line(draw, [(mid - 40, y - 32), (mid - 40, y + 32), (bar_x, y), (mid - 40, y - 32)])
    line(draw, [(bar_x, y - 34), (bar_x, y + 34)])


def diode_v(draw: ImageDraw.ImageDraw, x: int, y1: int, y2: int, reverse: bool = False, zener: bool = False) -> None:
    mid = (y1 + y2) // 2
    if not reverse:
        base_y = mid - 36
        bar_y = mid + 28
        line(draw, [(x, y1), (x, base_y)])
        line(draw, [(x - 34, base_y), (x + 34, base_y), (x, bar_y), (x - 34, base_y)])
        line(draw, [(x, bar_y), (x, y2)])
    else:
        base_y = mid + 36
        bar_y = mid - 28
        line(draw, [(x, y1), (x, bar_y)])
        line(draw, [(x - 34, base_y), (x + 34, base_y), (x, bar_y), (x - 34, base_y)])
        line(draw, [(x, base_y), (x, y2)])
    if zener:
        line(draw, [(x - 37, bar_y + 8), (x - 24, bar_y), (x + 24, bar_y), (x + 37, bar_y - 8)])
    else:
        line(draw, [(x - 36, bar_y), (x + 36, bar_y)])


def source_dc(draw: ImageDraw.ImageDraw, x: int, y: int, radius: int = 58) -> None:
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=BLACK, width=LINE)
    line(draw, [(x - 13, y - 22), (x + 13, y - 22)])
    line(draw, [(x, y - 35), (x, y - 9)])
    line(draw, [(x - 13, y + 25), (x + 13, y + 25)])


def source_ac(draw: ImageDraw.ImageDraw, x: int, y: int, radius: int = 58) -> None:
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline=BLACK, width=LINE)
    pts = []
    for i in range(41):
        xx = x - 35 + 70 * i / 40
        yy = y + 18 * math.sin(2 * math.pi * i / 40)
        pts.append((xx, yy))
    line(draw, pts)


def opamp(draw: ImageDraw.ImageDraw, cx: int, cy: int, width: int = 260, height: int = 250) -> dict[str, tuple[int, int]]:
    left = cx - width // 2
    right = cx + width // 2
    top = cy - height // 2
    bottom = cy + height // 2
    line(draw, [(left, top), (left, bottom), (right, cy), (left, top)])
    minus = (left, cy - 55)
    plus = (left, cy + 55)
    draw_math(draw, (left + 30, cy - 82), "−", bold=True)
    draw_math(draw, (left + 30, cy + 28), "+", bold=True)
    return {"minus": minus, "plus": plus, "out": (right, cy), "left": (left, cy)}


def trim(image: Image.Image, pad: int = 18) -> Image.Image:
    bg = Image.new("RGB", image.size, WHITE)
    bbox = ImageChops.difference(image, bg).getbbox()
    if not bbox:
        return image
    return ImageOps.expand(image.crop(bbox), border=pad, fill=WHITE)


def draw_series(v: str, r: str) -> Image.Image:
    img, d = new_canvas(560)
    left, right, top, bottom = 300, 1050, 150, 430
    source_dc(d, left, 290)
    line(d, [(left, top), (360, top)])
    diode_h(d, 360, 600, top)
    resistor_h(d, 690, 1000, top)
    line(d, [(600, top), (690, top)])
    line(d, [(1000, top), (right, top), (right, bottom), (left, bottom), (left, 348)])
    line(d, [(left, 232), (left, top)])
    draw_math(d, (left - 64, 270), f"{v} V", anchor="ra")
    draw_math(d, (480, 72), "Si", anchor="ma")
    draw_math(d, (845, 72), f"R = {r} kΩ", anchor="ma")
    return trim(img)


def draw_half_wave(vm: str, rl: str) -> Image.Image:
    img, d = new_canvas(560)
    left, right, top, bottom = 310, 1030, 150, 430
    source_ac(d, left, 290)
    line(d, [(left, 232), (left, top), (360, top)])
    diode_h(d, 360, 610, top)
    line(d, [(610, top), (right, top)])
    resistor_v(d, right, top, bottom)
    line(d, [(right, bottom), (left, bottom), (left, 348)])
    draw_math(d, (left - 64, 270), f"V_m = {vm} V", anchor="ra")
    draw_math(d, (485, 72), "D", anchor="ma")
    draw_math(d, (right - 80, 250), f"R_L = {rl} kΩ", anchor="ra")
    return trim(img)


def draw_clipper(vpk: str, r: str, battery: str) -> Image.Image:
    img, d = new_canvas(720)
    left, node, top, bottom = 300, 900, 160, 610
    source_ac(d, left, 360)
    line(d, [(left, 302), (left, top), (360, top)])
    resistor_h(d, 360, 690, top)
    line(d, [(690, top), (node, top)])
    dot(d, node, top)
    line(d, [(node, top), (1050, top)])
    line(d, [(node, top), (node, 210)])
    d.ellipse((1040, top - 10, 1060, top + 10), outline=BLACK, width=LINE)
    diode_v(d, node, 210, 390)
    source_dc(d, node, 485)
    line(d, [(node, 390), (node, 427)])
    line(d, [(node, 543), (node, bottom), (left, bottom), (left, 418)])
    draw_math(d, (left - 64, 330), f"V_{{in}} = ±{vpk} V", anchor="ra")
    draw_math(d, (510, 82), f"R = {r} kΩ", anchor="ma")
    draw_math(d, (1080, 125), "V_o", anchor="la")
    draw_math(d, (node + 65, 468), f"{battery} V", anchor="la")
    draw_math(d, (node + 65, 270), "D", anchor="la")
    return trim(img)


def draw_zener(vin: str, rs: str, vz: str, rl: str) -> Image.Image:
    img, d = new_canvas(620)
    left, node, load, top, bottom = 300, 690, 1040, 150, 485
    source_dc(d, left, 315)
    line(d, [(left, 257), (left, top), (380, top)])
    resistor_h(d, 380, 630, top)
    line(d, [(630, top), (node, top), (load, top)])
    dot(d, node, top)
    line(d, [(node, top), (node, 210)])
    diode_v(d, node, 210, 405, reverse=True, zener=True)
    resistor_v(d, load, top, bottom)
    line(d, [(load, bottom), (left, bottom), (left, 373)])
    dot(d, node, bottom)
    line(d, [(node, 405), (node, bottom)])
    draw_math(d, (left - 64, 292), f"V_{{in}} = {vin} V", anchor="ra")
    draw_math(d, (445, 72), f"R_S = {rs} Ω", anchor="ma")
    draw_math(d, (node, 505), f"V_Z = {vz} V", anchor="ma")
    draw_math(d, (load - 70, 260), f"R_L = {rl} Ω", anchor="ra")
    return trim(img)


def draw_bjt(vcc: str, r1: str, r2: str, rc: str, re_: str) -> Image.Image:
    img, d = new_canvas(780)
    top, bottom = 105, 690
    x_div, x_q = 345, 780
    # supply rail and divider
    line(d, [(x_div, top), (x_q, top)])
    line(d, [(x_q, top - 20), (x_q, top)])
    line(d, [(x_q - 35, top - 20), (x_q + 35, top - 20)])
    line(d, [(x_div, top), (x_div, 145)])
    resistor_v(d, x_div, 145, 360)
    resistor_v(d, x_div, 360, 610)
    dot(d, x_div, 360)
    line(d, [(x_div, 360), (650, 360)])
    ground(d, x_div, 650)
    line(d, [(x_div, 610), (x_div, 612)])
    # transistor in circle
    d.ellipse((650, 285, 860, 495), outline=BLACK, width=LINE)
    line(d, [(650, 360), (705, 360)])
    line(d, [(705, 320), (705, 440)])
    line(d, [(705, 330), (780, 255)])
    line(d, [(705, 430), (780, 505)])
    # emitter arrow (NPN, outward)
    line(d, [(754, 474), (780, 505)], width=LINE + 1)
    d.polygon([(780, 505), (754, 494), (770, 480)], fill=BLACK)
    # collector and emitter resistors
    resistor_v(d, x_q, top, 255)
    resistor_v(d, x_q, 505, 660)
    ground(d, x_q, 700)
    draw_math(d, (x_q, 28), f"V_{{CC}} = {vcc} V", anchor="ma")
    draw_math(d, (250, 225), f"R_1 = {r1} kΩ", anchor="ra")
    draw_math(d, (250, 485), f"R_2 = {r2} kΩ", anchor="ra")
    draw_math(d, (880, 165), f"R_C = {rc} kΩ", anchor="la")
    draw_math(d, (880, 570), f"R_E = {re_} kΩ", anchor="la")
    draw_math(d, (875, 352), "Q", anchor="la")
    return trim(img)


def draw_inverting(vin: str, rin: str, rf: str) -> Image.Image:
    img, d = new_canvas(660)
    amp = opamp(d, 760, 360)
    src_x, src_y = 285, 360
    source_dc(d, src_x, src_y)
    line(d, [(src_x, src_y - 58), (src_x, amp["minus"][1]), (345, amp["minus"][1])])
    resistor_h(d, 345, amp["minus"][0], amp["minus"][1])
    ground(d, src_x, 570)
    line(d, [(src_x, src_y + 58), (src_x, 532)])
    # plus input to ground
    line(d, [(amp["plus"][0], amp["plus"][1]), (575, amp["plus"][1]), (575, 540)])
    ground(d, 575, 540)
    # output and feedback
    out_x, out_y = amp["out"]
    line(d, [(out_x, out_y), (1100, out_y)])
    dot(d, out_x + 18, out_y)
    d.ellipse((1090, out_y - 10, 1110, out_y + 10), outline=BLACK, width=LINE)
    line(d, [(amp["minus"][0], amp["minus"][1]), (amp["minus"][0], 120)])
    resistor_h(d, amp["minus"][0], 900, 120)
    line(d, [(900, 120), (1000, 120), (1000, out_y)])
    draw_math(d, (src_x - 64, src_y - 20), f"V_{{in}} = {vin} V", anchor="ra")
    draw_math(d, (430, amp["minus"][1] - 85), f"R_{{in}} = {rin} kΩ", anchor="ma")
    draw_math(d, (765, 40), f"R_f = {rf} kΩ", anchor="ma")
    draw_math(d, (1125, out_y - 25), "V_o", anchor="la")
    return trim(img)


def draw_non_inverting(vin: str, r1: str, rf: str) -> Image.Image:
    img, d = new_canvas(700)
    amp = opamp(d, 760, 365)
    src_x, src_y = 260, 475
    source_dc(d, src_x, src_y)
    line(d, [(src_x, src_y - 58), (src_x, amp["plus"][1]), (amp["plus"][0], amp["plus"][1])])
    line(d, [(src_x, src_y + 58), (src_x, 625)])
    ground(d, src_x, 625)
    # R1 from minus node to ground
    minus_x, minus_y = amp["minus"]
    node_x = 420
    line(d, [(minus_x, minus_y), (node_x, minus_y)])
    dot(d, node_x, minus_y)
    resistor_v(d, node_x, minus_y, 560)
    ground(d, node_x, 600)
    # feedback
    out_x, out_y = amp["out"]
    line(d, [(out_x, out_y), (1110, out_y)])
    dot(d, out_x + 18, out_y)
    d.ellipse((1100, out_y - 10, 1120, out_y + 10), outline=BLACK, width=LINE)
    line(d, [(node_x, minus_y), (node_x, 105), (555, 105)])
    resistor_h(d, 555, 875, 105)
    line(d, [(875, 105), (1010, 105), (1010, out_y)])
    draw_math(d, (src_x - 64, src_y - 18), f"V_{{in}} = {vin} V", anchor="ra")
    draw_math(d, (455, 500), f"R_1 = {r1} kΩ", anchor="la")
    draw_math(d, (715, 28), f"R_f = {rf} kΩ", anchor="ma")
    draw_math(d, (1135, out_y - 25), "V_o", anchor="la")
    return trim(img)


def clean_prompt(prompt: str) -> str:
    return prompt.split("Font Family:", 1)[0].replace("$\\scriptstyle ", "").replace("$", "").strip()


def values(pattern: str, text: str):
    match = re.search(pattern, text, flags=re.I)
    if not match:
        raise ValueError(f"Could not parse: {text}")
    return match.groups()


def render_record(record: dict) -> Image.Image:
    q = int(record["question"])
    prompt = clean_prompt(record["prompt"])
    if 481 <= q <= 487:
        v, r = values(r"a ([\d.]+) V DC.*?R = ([\d.]+) kilo", prompt)
        return draw_series(v, r)
    if 488 <= q <= 494:
        vm, rl = values(r"peak ([\d.]+) V.*?R_L = ([\d.]+) kilo", prompt)
        return draw_half_wave(vm, rl)
    if 495 <= q <= 500:
        vpk, r, battery = values(r"source \(±([\d.]+) V\).*?R = ([\d.]+) kilo.*?a ([\d.]+) V battery", prompt)
        return draw_clipper(vpk, r, battery)
    if 501 <= q <= 506:
        vin, rs, vz, rl = values(r"V_\{in\} = ([\d.]+) V.*?R_S = ([\d.]+) ohm.*?V_Z = ([\d.]+) V.*?R_L = ([\d.]+) ohm", prompt)
        return draw_zener(vin, rs, vz, rl)
    if 507 <= q <= 515:
        r1, r2, vcc, rc, re_ = values(r"R_1 = ([\d.]+) kΩ / R_2 = ([\d.]+) kΩ.*?V_\{CC\} = ([\d.]+) V.*?R_C = ([\d.]+) kΩ.*?R_E = ([\d.]+) kΩ", prompt)
        return draw_bjt(vcc, r1, r2, rc, re_)
    if 516 <= q <= 523:
        vin, rin, rf = values(r"V_\{in\} = ([\d.]+) V.*?R_\{in\} = ([\d.]+) kΩ.*?R_f = ([\d.]+) kΩ", prompt)
        return draw_inverting(vin, rin, rf)
    if 524 <= q <= 530:
        vin, r1, rf = values(r"V_\{in\} = ([\d.]+) V.*?R_1 = ([\d.]+) kΩ.*?R_f = ([\d.]+) kΩ", prompt)
        return draw_non_inverting(vin, r1, rf)
    raise ValueError(f"Unsupported question: {q}")


def main() -> None:
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])
    destination.mkdir(parents=True, exist_ok=True)
    records = json.loads(source.read_text(encoding="utf-8"))
    for record in records:
        image = render_record(record)
        image.save(destination / f"q{record['question']}.png", dpi=(300, 300), optimize=True)
    print(f"rendered={len(records)} output={destination}")


if __name__ == "__main__":
    main()
