"""Generate a small personal greeting banner using Jack's saved GitHub avatar."""
import base64
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
FONT = 'Arial, Helvetica, sans-serif'


def text(x, y, value, size=24, color='#234366', weight=400):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
            f'font-size="{size}" font-weight="{weight}">{escape(value)}</text>')


def hero(avatar, mobile=False):
    width, height = (640, 300) if mobile else (1200, 240)
    cx, cy, radius = (524, 96, 64) if mobile else (1036, 120, 82)
    body = f'<rect width="{width}" height="{height}" rx="16" fill="#eaf2ff"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="{radius+12}" fill="#d5e5fb"/>'
    body += f'<defs><clipPath id="avatar"><circle cx="{cx}" cy="{cy}" r="{radius}"/></clipPath></defs>'
    body += (f'<image x="{cx-radius}" y="{cy-radius}" width="{radius*2}" height="{radius*2}" '
             f'href="data:image/png;base64,{avatar}" clip-path="url(#avatar)"/>')
    if mobile:
        body += text(32, 88, "Hi, I'm Jack.", 60, '#1c385c', 600)
        body += text(34, 153, 'Full-stack developer', 32)
        body += text(34, 199, 'Java / Vue', 32)
        body += text(34, 267, '@JackWenStack', 28, '#4c6685')
    else:
        body += text(52, 107, "Hi, I'm Jack.", 72, '#1c385c', 600)
        body += text(56, 160, 'Full-stack developer · Java & Vue', 28)
        body += text(56, 204, '@JackWenStack', 24, '#4c6685')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
            '<title id="title">Hi, I\'m Jack.</title>'
            '<desc id="desc">Jack Wen, a full-stack developer working with Java and Vue. Includes his GitHub avatar.</desc>'
            + body + '</svg>\n')


if __name__ == '__main__':
    avatar = base64.b64encode((ASSETS/'avatar.png').read_bytes()).decode('ascii')
    for name, mobile in [('hero.svg', False), ('hero-mobile.svg', True)]:
        content = hero(avatar, mobile)
        (ASSETS/name).write_text(content, encoding='utf-8')
        print(f'{name}: {len(content.encode()):,} bytes')
