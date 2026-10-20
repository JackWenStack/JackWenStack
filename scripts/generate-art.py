"""Regenerate the original profile artwork. Python 3; no dependencies."""
from html import escape
from math import cos, sin, pi, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
INK, LIME, WHITE, MUTED = "#111411", "#d5ff70", "#f4f5ef", "#b6beb0"
FONT, MONO = "Arial, Helvetica, sans-serif", "'Courier New', monospace"


def text(x, y, value, size=20, color=WHITE, weight=400, spacing=0, family=FONT):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" '
            f'font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">'
            f'{escape(value)}</text>')


def rotate(p):
    x, y, z = p
    a, b = 0.88, -0.35
    y, z = y*cos(a)-z*sin(a), y*sin(a)+z*cos(a)
    x, z = x*cos(b)+z*sin(b), -x*sin(b)+z*cos(b)
    return x, y, z


def center(t):
    r = 2 + 0.68*cos(3*t)
    return r*cos(2*t), r*sin(2*t), 0.92*sin(3*t)


def norm(p):
    length = sqrt(sum(v*v for v in p))
    return tuple(v/length for v in p)


def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def knot_point(t, angle):
    c = center(t)
    ahead, behind = center(t+0.001), center(t-0.001)
    tangent = norm(tuple(a-b for a, b in zip(ahead, behind)))
    normal = norm(cross(tangent, (0, 0, 1)))
    binormal = cross(tangent, normal)
    return rotate(tuple(c[i]+0.36*(normal[i]*cos(angle)+binormal[i]*sin(angle)) for i in range(3)))


def sculpture(cx, cy, scale):
    """Depth-sorted wireframe tube: original mathematical trefoil artwork."""
    parts = []
    n, rings = 150, 16
    for i in range(n):
        t0, t1 = 2*pi*i/n, 2*pi*(i+1)/n
        for j in range(rings):
            a0, a1 = 2*pi*j/rings, 2*pi*(j+1)/rings
            points = [knot_point(t0, a0), knot_point(t1, a0),
                      knot_point(t1, a1), knot_point(t0, a1)]
            depth = sum(p[2] for p in points)/4
            brightness = max(0, min(1, (depth+2.7)/5.4))
            rgb = tuple(round(v*(0.27+brightness*0.73)) for v in (213, 255, 112))
            stroke = "#%02x%02x%02x" % rgb
            xy = " ".join(f"{cx+x*scale:.1f},{cy+y*scale:.1f}" for x, y, z in points)
            parts.append((depth, f'<polygon points="{xy}" fill="{INK}" stroke="{stroke}" stroke-width=".65" stroke-linejoin="round"/>'))
    return '<g aria-hidden="true">'+"".join(p for _, p in sorted(parts))+"</g>"


def svg(width, height, title, desc, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" fill="none" role="img" aria-labelledby="title desc">'
            f'<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
            + body + "</svg>\n")


def hero(mobile=False):
    width, height = (640, 840) if mobile else (1200, 480)
    body = f'<rect width="{width}" height="{height}" rx="4" fill="{INK}"/>'
    if mobile:
        body += text(36, 47, "JACKWENSTACK", 18, MUTED, 400, 2, MONO)
        body += text(36, 182, "JACK", 140, WHITE, 900, -7)
        body += text(30, 302, "WEN", 140, LIME, 900, -7)
        body += text(39, 351, "Full-stack developer", 36, WHITE)
        body += sculpture(360, 522, 58)
        body += text(40, 714, "Clear thinking. Solid engineering.", 32, MUTED)
        body += '<path d="M36 748H604" stroke="#3d4637"/>'
        body += text(40, 797, "JAVA  /  SPRING BOOT  /  VUE", 32, LIME, 400, 0, MONO)
    else:
        body += text(52, 47, "JACKWENSTACK", 16, MUTED, 400, 2, MONO)
        body += text(52, 188, "JACK", 136, WHITE, 900, -7)
        body += text(46, 306, "WEN", 136, LIME, 900, -7)
        body += text(56, 353, "Clear thinking. Solid engineering.", 23, MUTED)
        body += sculpture(901, 210, 70)
        body += '<path d="M56 405H1144" stroke="#3d4637"/>'
        body += text(56, 449, "Full-stack developer", 19, WHITE)
        body += text(810, 449, "JAVA / SPRING BOOT / VUE", 18, LIME, 400, 0, MONO)
    return svg(width, height, "Jack Wen — Full-stack developer",
               "Graphite and lime typography with an original three-dimensional woven knot. Clear thinking. Solid engineering.", body)


def signoff(mobile=False):
    width, height = (640, 200) if mobile else (1200, 132)
    body = f'<rect width="{width}" height="{height}" rx="4" fill="{INK}"/>'
    if mobile:
        body += text(32, 60, "Stay curious.", 40, WHITE, 700, -0.5)
        body += text(32, 112, "Build with intent.", 40, LIME, 700, -0.5)
        body += text(34, 172, "github.com/JackWenStack", 30, MUTED, family=MONO)
        body += text(524, 114, "↗", 96, LIME)
    else:
        body += text(48, 56, "Stay curious. Build with intent.", 28, WHITE, 700, -0.5)
        body += text(50, 94, "github.com/JackWenStack", 16, MUTED, family=MONO)
        body += text(1050, 98, "↗", 96, LIME)
    return svg(width, height, "Stay curious. Build with intent.",
               "Find Jack Wen at github.com/JackWenStack.", body)


if __name__ == "__main__":
    for name, content in [
        ("hero.svg", hero()), ("hero-mobile.svg", hero(True)),
        ("signoff.svg", signoff()), ("signoff-mobile.svg", signoff(True)),
    ]:
        (ASSETS/name).write_text(content, encoding="utf-8")
        print(f"{name}: {len(content.encode()):,} bytes")
