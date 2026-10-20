"""Shared original JW geometry for the cover, signoff and contribution panel."""

INK, WHITE, BLUE, MUTED = "#0b0f16", "#f2f5fa", "#5294ff", "#a4afc0"
J = [(0,0),(170,0),(170,160),(130,210),(40,210),(0,170),(0,115),
     (48,115),(48,148),(64,164),(109,164),(122,148),(122,46),(0,46)]
W = [(188,0),(240,0),(269,137),(311,40),(347,40),(390,137),(420,0),
     (472,0),(425,210),(373,210),(329,112),(285,210),(233,210)]


def polygon(points, **attrs):
    coords = " ".join(f"{x:.2f},{y:.2f}" for x,y in points)
    properties = " ".join(f'{k.replace("_","-")}="{v}"' for k,v in attrs.items())
    return f'<polygon points="{coords}" {properties}/>'


def mark(x, y, scale, color=BLUE):
    return (f'<g transform="translate({x} {y}) scale({scale})">'
            + "".join(polygon(p, fill=color) for p in (J,W)) + "</g>")
