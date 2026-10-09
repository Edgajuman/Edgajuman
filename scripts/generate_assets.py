"""Generate original SVG project covers and a restrained animated profile banner."""
from pathlib import Path
import math
from html import escape
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
WIDTH, HEIGHT = 1200, 360
BG = (8, 14, 24)
BLUE = (73, 135, 255)
CYAN = (88, 222, 213)
WHITE = (239, 245, 255)
MUTED = (135, 153, 176)


def font(size, bold=False):
    candidates = (
        ["C:/Windows/Fonts/seguisb.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold else
        ["C:/Windows/Fonts/segoeui.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    for candidate in candidates:
        if Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def corners(draw, box, color, length=18, width=2):
    x, y, right, bottom = box
    for px, py, dx, dy in [(x, y, 1, 1), (right, y, -1, 1), (x, bottom, 1, -1), (right, bottom, -1, -1)]:
        draw.line([(px + length * dx, py), (px, py), (px, py + length * dy)], fill=color, width=width)


def background():
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    for x in range(WIDTH):
        t = max(0, 1 - abs(x - 970) / 430)
        draw.line((x, 0, x, HEIGHT), fill=(8 + int(t * 3), 14 + int(t * 6), 24 + int(t * 13)))
    draw.rounded_rectangle((1, 1, WIDTH - 2, HEIGHT - 2), radius=22, outline=(35, 49, 69), width=2)
    draw.text((54, 43), "EDGAJUMAN / AKIOMAE", font=font(17, True), fill=CYAN)
    draw.text((49, 77), "Gabriel", font=font(99, True), fill=WHITE)
    draw.text((54, 208), "Software de escritorio. Interfaces. Herramientas creativas.", font=font(22), fill=MUTED)
    draw.line((54, 278, 696, 278), fill=(36, 51, 73), width=1)
    draw.text((54, 302), "RUST   /   WEB   /   PERSONALIZACIÓN", font=font(15, True), fill=(156, 177, 203))
    for x in range(807, 1140, 28):
        for y in range(53, 320, 28):
            draw.ellipse((x, y, x + 1, y + 1), fill=(37, 55, 76))
    corners(draw, (784, 45, 1147, 315), (59, 82, 112))
    return image


def animation_frame(base, phase):
    image = base.copy()
    draw = ImageDraw.Draw(image)
    projected = []
    for x, y, z in [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1), (-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]:
        theta = phase * 2 * math.pi
        rx, rz = x * math.cos(theta) + z * math.sin(theta), -x * math.sin(theta) + z * math.cos(theta)
        ry, rz = y * math.cos(.4) - rz * math.sin(.4), y * math.sin(.4) + rz * math.cos(.4)
        scale = 76 * 4 / (4 + rz)
        projected.append((966 + rx * scale, 175 + ry * scale))
    edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
    for index, (a, b) in enumerate(edges):
        draw.line([projected[a], projected[b]], fill=CYAN if index >= 8 else BLUE, width=3)
    for x, y in projected:
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=WHITE)
    for index in range(3):
        x = 943 + index * 23
        intensity = .3 + .7 * (1 + math.sin(phase * math.tau - index * .7)) / 2
        color = tuple(int(v * intensity) for v in CYAN)
        draw.ellipse((x, 285, x + 5, 290), fill=color)
    return image


def banner():
    base = background()
    frames = [animation_frame(base, index / 60) for index in range(60)]
    palette = frames[0].quantize(colors=256)
    frames = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]
    frames[0].save(ASSETS / "hero.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True, disposal=1)
    animation_frame(base, 0).save(ASSETS / "hero-preview.png")
    static = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 360" role="img" aria-labelledby="title desc">
<title id="title">Gabriel — Edgajuman / Akiomae</title><desc id="desc">Software de escritorio, interfaces y herramientas creativas.</desc>
<rect x="1" y="1" width="1198" height="358" rx="22" fill="#080e18" stroke="#233145" stroke-width="2"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="54" y="62" fill="#58ded5" font-size="17" font-weight="600" letter-spacing="2">EDGAJUMAN / AKIOMAE</text>
<text x="49" y="175" fill="#eff5ff" font-size="99" font-weight="600">Gabriel</text>
<text x="54" y="230" fill="#8799b0" font-size="22">Software de escritorio. Interfaces. Herramientas creativas.</text>
<path d="M54 278H696" stroke="#243349"/><text x="54" y="322" fill="#9cb1cb" font-size="15" letter-spacing="2">RUST / WEB / PERSONALIZACIÓN</text></g>
<path d="M886 117L977 71L1066 118L978 170Z M886 117V227L978 280L1066 227V118 M978 170V280" fill="none" stroke="#4987ff" stroke-width="3"/>
<path d="M784 63V45H802M1129 45H1147V63M784 297V315H802M1129 315H1147V297" fill="none" stroke="#3b5270" stroke-width="2"/>
</svg>'''
    (ASSETS / "hero-static.svg").write_text(static, encoding="utf-8")


def symbol(kind, accent):
    if kind == "screen":
        return f'<rect x="970" y="49" width="161" height="95" rx="9"/><path d="M990 160H1111M1050 144V160"/><path d="M1035 76L1070 96L1035 116Z" fill="{accent}" stroke="none"/>'
    if kind == "cube":
        return '<path d="M489 31L541 59L489 88L437 59Z M437 59V119L489 149L541 119V59 M489 88V149"/>'
    if kind == "themes":
        return f'<rect x="436" y="45" width="105" height="92" rx="12"/><circle cx="460" cy="70" r="10" fill="{accent}"/><circle cx="494" cy="70" r="10" fill="#f1b866"/><circle cx="460" cy="105" r="10" fill="#8e91ff"/><circle cx="494" cy="105" r="10" fill="#eff5ff"/>'
    if kind == "characters":
        return '<path d="M438 51Q438 35 455 35H522Q540 35 540 51V99Q540 116 522 116H481L459 141V116H455Q438 116 438 99Z"/><path d="M460 63H518M460 85H500"/>'
    return '<rect x="454" y="29" width="74" height="121" rx="13"/><path d="M475 45H507M482 135H500 M478 74L465 87L478 100 M504 74L517 87L504 100"/>'


def card(filename, title, subtitle, category, accent, kind, wide=False):
    width = 1200 if wide else 600
    title_size = 43 if wide else 32
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 180" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle)}</desc>
<rect x="1" y="1" width="{width-2}" height="178" rx="14" fill="#0b1320" stroke="#26364c"/>
<rect x="1" y="28" width="3" height="124" fill="{accent}"/>
<g font-family="Segoe UI,Arial,sans-serif"><text x="28" y="39" font-size="11" font-weight="600" letter-spacing="2" fill="{accent}">{escape(category)}</text>
<text x="26" y="94" font-size="{title_size}" font-weight="600" fill="#eff5ff">{escape(title)}</text>
<text x="28" y="132" font-size="16" fill="#94a8c2">{escape(subtitle)}</text></g>
<g fill="none" stroke="{accent}" stroke-width="2" stroke-linejoin="round">{symbol(kind,accent)}</g></svg>'''
    (ASSETS / filename).write_text(content, encoding="utf-8")


if __name__ == "__main__":
    banner()
    card("project-ak-screen.svg", "AK Screen", "Grabación de tutoriales / Edición de video / Composición", "PROYECTO ACTUAL", "#58ded5", "screen", True)
    card("project-themes.svg", "AK Screen Themes", "Personalización y catálogo comunitario", "ECOSISTEMA AK SCREEN", "#b29aff", "themes")
    card("project-cubic.svg", "CubicLauncher", "Minecraft / Instancias / Personalización", "FORK DE TRABAJO", "#73cbaa", "cube")
    card("project-characters.svg", "AkioCharacters", "Personajes e IA conversacional", "PROYECTO HISTÓRICO", "#f1b866", "characters")
    card("project-akiomae.svg", "AkiomaeCodes", "Compartir código y descubrir proyectos", "PUBLICADO EN GOOGLE PLAY", "#6eb8ff", "mobile")
    print("Generated banner, static fallback and five original project covers")
