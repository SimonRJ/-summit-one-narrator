"""Draw exact shapes, angle sectors and perpendicular markers."""

import math

from stage import BG, MINT, RIM, blend
from studio_diagrams import fit


def polar(point, degrees, radius):
    angle = math.radians(degrees)
    return point[0] + radius * math.cos(angle), point[1] + radius * math.sin(angle)


def direction(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))


def region(stage, points, colour, *, opacity=1, tint=.25, outline=True):
    if opacity <= 0:
        return
    coords = [(stage.px(x), stage.px(y)) for x, y in points]
    stage.draw.polygon(coords, fill=blend(BG, colour, tint * opacity))
    if outline:
        stage.line([*points, points[0]], colour, 3, opacity)


def sector(stage, vertex, start, sweep, radius, colour, *, opacity=1, label="", at=None):
    if opacity <= 0:
        return
    points = [polar(vertex, start + i * sweep / 24, radius) for i in range(25)]
    region(stage, [vertex, *points], colour, opacity=opacity, tint=.18, outline=False)
    stage.line(points, colour, 3, opacity)
    if label:
        x, y = at or polar(vertex, start + sweep / 2, radius + 21)
        fit(stage, label, x, y, 29, 194, colour, opacity)


def corner(stage, vertex, a, b, radius, colour, *, opacity=1, label="", at=None):
    first, second = direction(vertex, a), direction(vertex, b)
    sweep = (second - first + 180) % 360 - 180
    sector(stage, vertex, first, sweep, radius, colour, opacity=opacity, label=label, at=at)


def dashed(stage, a, b, colour=RIM, opacity=1):
    length=math.hypot(b[0]-a[0], b[1]-a[1])
    if length==0:
        return
    ux,uy=(b[0]-a[0])/length,(b[1]-a[1])/length
    for q in range(0,round(length),15):
        p=min(length,q+8)
        stage.line([(a[0]+q*ux,a[1]+q*uy),(a[0]+p*ux,a[1]+p*uy)],colour,2,opacity)


def right_mark(stage, base, x_sign=1, y_sign=-1, colour=MINT, opacity=1, size=17):
    x,y=base
    stage.line([(x+x_sign*size,y),(x+x_sign*size,y+y_sign*size),(x,y+y_sign*size)],colour,2,opacity)
