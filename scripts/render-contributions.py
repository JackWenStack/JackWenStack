"""Frame real Platane/snk contribution cells as a looping scanner. Stdlib only."""

import argparse
from datetime import datetime, timezone
from html import escape
from pathlib import Path
import re
from xml.etree import ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
COLORS = ("#172233", "#29476f", "#3c6da8", "#639de7", "#a7ceff")


def read_cells(source):
    root = ET.fromstring(source)
    css = "".join(e.text or "" for e in root.iter(NS + "style"))
    levels = dict(re.findall(r"\.c\.(\w+)\{fill:var\(--c([0-4])\)", css))
    cells = []
    for rect in root.iter(NS + "rect"):
        classes = rect.get("class", "").split()
        if "c" not in classes:
            continue
        extra = [name for name in classes if name != "c"]
        if len(extra) > 1 or any(name not in levels for name in extra):
            raise ValueError(f"Unrecognized contribution class: {classes}")
        x, y = int(rect.get("x", "-1")), int(rect.get("y", "-1"))
        if x < 2 or y < 2 or (x - 2) % 16 or (y - 2) % 16 or y > 98:
            raise ValueError("Unexpected upstream cell coordinates")
        cells.append(((x - 2) // 16, (y - 2) // 16, int(levels[extra[0]]) if extra else 0))
    if not cells or len(cells) != len({(x, y) for x, y, _ in cells}):
        raise ValueError("Missing or duplicate contribution cells")
    if not 50 <= max(x for x, _, _ in cells) + 1 <= 54:
        raise ValueError("Expected a yearly contribution grid")
    return cells


def label(x, y, value, size=18, color="#a4afc0", weight=400):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" font-family="Arial,Helvetica,sans-serif">'
            f'{escape(value)}</text>')


def render(cells, updated, mobile=False, motion=True):
    width, height = (640, 520) if mobile else (1200, 232)
    columns = max(x for x, _, _ in cells) + 1
    split = (columns + 1) // 2
    step = 21 if mobile else 1104 / columns
    size = 15 if mobile else 15.5
    travel = split * step if mobile else columns * step
    grid_height = step * 6 + size
    body = f'<rect width="{width}" height="{height}" rx="12" fill="#0b0f16"/>'
    groups = [(0, split, 32, 72), (split, columns, 32, 265)] if mobile else [(0, columns, 48, 32)]
    if mobile:
        body += label(32, 50, "Earlier", 25)
        body += label(32, 243, "Recent", 25)
    for index, (start, end, left, top) in enumerate(groups):
        base, lit = [], []
        for x, y, level in cells:
            if not start <= x < end:
                continue
            attrs = f'x="{(x-start)*step:.2f}" y="{y*step:.2f}" width="{size}" height="{size}" rx="1.5"'
            base.append(f'<rect {attrs} fill="{COLORS[level]}" data-level="{level}"/>')
            if level:
                lit.append(f'<rect {attrs} fill="#e6f1ff"/>')
        body += (
            f'<g transform="translate({left} {top})">'
            f'<defs><clipPath id="bounds-{index}"><rect width="{travel}" height="{grid_height}"/></clipPath>'
            f'<mask id="scan-{index}" maskUnits="userSpaceOnUse" x="0" y="0" width="{travel}" height="{grid_height}">'
            f'<rect class="scan" x="-90" width="90" height="{grid_height}" fill="url(#beam)"/></mask></defs>'
            + "".join(base)
            + f'<g mask="url(#scan-{index})" opacity=".9">{"".join(lit)}</g>'
            + f'<g clip-path="url(#bounds-{index})" class="beam-line"><g class="scan">'
            f'<rect x="-44" width="44" height="{grid_height}" fill="url(#glow)"/>'
            f'<rect x="-1" width="2" height="{grid_height}" fill="#6ca5ff" opacity=".8"/></g></g></g>'
        )
    footer_y = 487 if mobile else 210
    body += label(32 if mobile else 48, footer_y, f"Updated {updated} UTC", 24 if mobile else 16)
    legend_x, legend_y = (362, 445) if mobile else (980, 195)
    body += label(legend_x - 49, legend_y + 12, "Less", 20 if mobile else 14)
    for i, color in enumerate(COLORS):
        body += f'<rect x="{legend_x+i*22}" y="{legend_y}" width="15" height="15" rx="1.5" fill="{color}"/>'
    body += label(legend_x + 116, legend_y + 12, "More", 20 if mobile else 14)
    style = (
        f'.scan{{animation:scan 12s linear infinite}}'
        f'@keyframes scan{{from{{transform:translateX(0)}}to{{transform:translateX({travel+100}px)}}}}'
    )
    if not motion:
        style = ".scan{animation:none}.beam-line{display:none}"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
        '<title id="title">Jack Wen — Contribution signal</title>'
        '<desc id="desc">Real GitHub contribution levels from Platane/snk. '
        'A decorative scan highlights activity without changing the underlying data. '
        'Motion follows your system preference.</desc>'
        f'<style>{style}</style><defs><linearGradient id="beam">'
        '<stop stop-color="black"/><stop offset="1" stop-color="white"/></linearGradient>'
        '<linearGradient id="glow"><stop stop-color="#5294ff" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#5294ff" stop-opacity=".22"/></linearGradient></defs>{body}</svg>\n'
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--mobile-output", type=Path, required=True)
    args = parser.parse_args()
    cells = read_cells(args.source.read_text(encoding="utf-8"))
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    for target, mobile in [(args.output, False), (args.mobile_output, True)]:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(cells, today, mobile), encoding="utf-8")
        # Select at the embedding <picture>: media emulation inside external SVG
        # images is inconsistent across browsers. Both variants use fresh data.
        still = target.with_name(target.stem + "-still.svg")
        still.write_text(render(cells, today, mobile, motion=False), encoding="utf-8")
    print(f"Rendered {len(cells)} cells; {sum(level > 0 for _, _, level in cells)} active days.")


if __name__ == "__main__":
    main()
