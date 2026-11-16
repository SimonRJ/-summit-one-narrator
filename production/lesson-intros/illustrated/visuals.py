"""Drawing primitives for the narrated Summit One films. Coordinates refer to a 1280 × 720 frame."""
from functools import lru_cache
from math import hypot

from PIL import Image, ImageDraw, ImageFont

PAPER = "#101c2a"
WHITE = "#f2f7f6"
SOFT = "#b6c6ce"
AQUA = "#72e5da"
BLUE = "#7fb6ff"
GOLD = "#ffd27c"
PINK = "#ffa6a9"
VIOLET = "#c4affd"


def clamp(u):
    return max(0.0, min(u, 1.0))


def ease(u):
    t = clamp(u)
    return t * t * (3 - 2 * t)


def mix(a, b, t):
    return a + (b - a) * t


def point(p, q, t):
    return mix(p[0], q[0], t), mix(p[1], q[1], t)


def tone(colour, amount, base=PAPER):
    return tuple(round(mix(int(base[k:k + 2], 16), int(colour[k:k + 2], 16), amount))
                 for k in (1, 3, 5))


@lru_cache(maxsize=500)
def typeface(size, bold, display):
    prefix = "DejaVuSerif" if display else "DejaVuSans"
    return ImageFont.truetype(prefix + ("-Bold.ttf" if bold else ".ttf"), size)


@lru_cache(maxsize=1200)
def lettering(value, size, bold, display):
    face = typeface(size, bold, display)
    left, top, right, bottom = face.getbbox(value)
    icon = Image.new("L", (max(1, right - left + 2), max(1, bottom - top + 2)))
    ImageDraw.Draw(icon).text((1 - left, 1 - top), value, font=face, fill=255)
    return icon


@lru_cache(maxsize=6)
def background(scale, theme):
    width, height = round(1280 * scale), round(720 * scale)
    if theme == "area":
        top, bottom = "#122d38", "#101c2a"
    elif theme == "edge":
        top, bottom = "#1e2838", "#111927"
    elif theme == "digits":
        top, bottom = "#122838", "#101b2c"
    else:
        top, bottom = "#34293a", "#201d31"
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        draw.line(((0, y), (width, y)), fill=tone(bottom, y / height, top))
    if theme not in ("fraction", "digits"):
        gaps = round(24 * scale)
        for x in range(gaps, width, gaps):
            for y in range(gaps, height, gaps):
                draw.point((x, y), fill="#39505b" if theme == "area" else "#354355")
    return image


class Art:
    def __init__(self, scale, theme):
        self.scale = scale
        self.image = background(scale, theme).copy()
        self.draw = ImageDraw.Draw(self.image)
        self.paper = "#222031" if theme == "fraction" else PAPER

    def px(self, value):
        return round(value * self.scale)

    def coords(self, p):
        return self.px(p[0]), self.px(p[1])

    def label(self, text, x, y, size=32, colour=WHITE, alpha=1, *, align="center", bold=False, display=False):
        if alpha <= 0:
            return
        icon = lettering(str(text), self.px(size), bold, display)
        left, top = self.coords((x, y))
        left -= {"center": icon.width // 2, "right": icon.width, "left": 0}[align]
        top -= icon.height // 2
        if alpha < .999:
            icon = icon.point([round(a * alpha) for a in range(256)])
        self.image.paste(colour, (left, top, left + icon.width, top + icon.height), icon)

    def path(self, points, colour=WHITE, width=3, alpha=1):
        if alpha > 0 and len(points) > 1:
            ink = colour if alpha >= .999 else tone(colour, alpha, self.paper)
            self.draw.line([self.coords(p) for p in points], fill=ink,
                           width=max(1, self.px(width)), joint="curve")

    def dashed(self, p, q, colour=SOFT, width=2, alpha=1, dash=8):
        distance = hypot(q[0] - p[0], q[1] - p[1])
        if not distance or alpha <= 0:
            return
        for index in range(0, int(distance), 2 * dash):
            self.path((point(p, q, index / distance), point(p, q, min(1, (index + dash) / distance))),
                      colour, width, alpha)

    def polygon(self, points, colour, alpha=1):
        if alpha > 0:
            ink = colour if alpha >= .999 else tone(colour, alpha, self.paper)
            self.draw.polygon([self.coords(p) for p in points], fill=ink)

    def rect(self, x, y, w, h, colour, alpha=1):
        if w > 0 and h > 0:
            self.polygon(((x, y), (x + w, y), (x + w, y + h), (x, y + h)), colour, alpha)

    def circle(self, p, radius, colour, alpha=1):
        if alpha <= 0:
            return
        x, y = p
        self.draw.ellipse((*self.coords((x-radius, y-radius)), *self.coords((x+radius, y+radius))),
                          fill=colour if alpha >= .999 else tone(colour, alpha, self.paper))

    def rounded(self, x, y, w, h, radius, colour, alpha=1):
        if alpha > 0:
            self.draw.rounded_rectangle((*self.coords((x,y)), *self.coords((x+w,y+h))),
                                        self.px(radius), fill=tone(colour, alpha, self.paper))

    def trace(self, points, progress, colour=AQUA, width=5, cursor=True):
        if progress <= 0:
            return
        sizes = [hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(points, points[1:])]
        travel = progress * sum(sizes)
        end = points[0]
        visible = [end]
        for p, q, length in zip(points, points[1:], sizes):
            if length == 0:
                continue
            end = point(p, q, min(1.0, travel / length))
            visible.append(end)
            if travel <= length:
                break
            travel -= length
        self.path(visible, colour, width)
        if cursor and progress < 1:
            self.circle(end, width * 1.5, colour, .4)
            self.circle(end, width * .73, WHITE)

    def arrow(self, p, q, colour, progress=1):
        if progress <= 0:
            return
        end = point(p, q, progress)
        self.path((p, end), colour, 3)
        length = hypot(q[0] - p[0], q[1] - p[1])
        ux, uy = (q[0] - p[0])/length, (q[1] - p[1])/length
        tip = 12 * min(1, progress * 3)
        x, y = end
        self.path(((x-tip*(ux+uy/2), y-tip*(uy-ux/2)), end,
                   (x-tip*(ux-uy/2), y-tip*(uy+ux/2))), colour, 3)

    def dimension(self, p, q, text, colour=SOFT, alpha=1, offset=19, size=26):
        """Draw endpoints and a centred label. Endpoints refer to exact model coordinates."""
        if alpha <= 0:
            return
        x, y = point(p, q, .5)
        if p[1] == q[1]:
            self.path((p, q), colour, 2, alpha)
            for tx, ty in (p,q):
                self.path(((tx,ty-6),(tx,ty+6)), colour, 2, alpha)
            self.label(text, x, y-offset, size, colour, alpha, bold=True)
        elif p[0] == q[0]:
            self.path((p, q), colour, 2, alpha)
            for tx, ty in (p,q):
                self.path(((tx-6,ty),(tx+6,ty)), colour, 2, alpha)
            self.label(text, x-offset, y, size, colour, alpha, bold=True)
        else:
            raise ValueError("A dimension must be horizontal or vertical")

    def heading(self, title, colour, subtitle=None):
        self.label(title, 640, 77, 49, WHITE, bold=True, display=True)
        if subtitle:
            self.label(subtitle, 640, 132, 26, colour)

    def caption(self, caption, time):
        alpha = min(ease((time - caption["start"]) / .12), ease((caption["end"] - time) / .12))
        if alpha <= 0:
            return
        size = 45
        words = caption["text"].split()
        while True:
            lines = ['']
            for word in words:
                trial = (lines[-1] + ' ' + word).strip()
                if lines[-1] and lettering(trial, self.px(size), True, False).width > self.px(1160):
                    lines.append(word)
                else:
                    lines[-1] = trial
            if len(lines) <= 2 or size <= 32:
                break
            size -= 1
        width = max(lettering(line, self.px(size), True, False).width for line in lines) / self.scale + 42
        if len(lines) == 1:
            self.rounded(640-width/2, 648, width, 59, 11, "#0b1420", alpha)
            self.label(lines[0], 640, 678, size, WHITE, alpha, bold=True)
        else:
            self.rounded(640-width/2, 606, width, 102, 11, "#0b1420", alpha)
            self.label(lines[0], 640, 631, size, WHITE, alpha, bold=True)
            self.label(lines[1], 640, 681, size, WHITE, alpha, bold=True)


class Cues:
    """Match authored visual actions against the reviewed voice recording."""
    def __init__(self, scene, time):
        self.scene = scene
        self.t = time
        self.local = time - scene["start"]

    def find(self, phrase):
        return find_words(tuple(word["text"] for word in self.scene["words"]), phrase)

    def after(self, phrase, duration=.62, delay=0):
        words = self.scene["words"]
        first, _ = self.find(phrase)
        return ease((self.t - words[first]["start"] - delay) / duration)

    def says(self, phrase, delay=0):
        """Reveal after the spoken number has been heard."""
        words = self.scene["words"]
        _, final = self.find(phrase)
        return ease((self.t - words[final]["end"] - delay) / .38)

    def opening(self, duration=.55):
        return ease(self.local / duration)


@lru_cache(maxsize=800)
def find_words(words, phrase):
    def tokens(text):
        return tuple("".join(c for c in term.lower() if c.isalnum()) for term in text.split())

    haystack, needle = tokens(" ".join(words)), tokens(phrase)
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i+len(needle)] == needle:
            return i, i + len(needle) - 1
    raise ValueError(f"Missing narration cue: {phrase}")


def bounds(x, y, w, h):
    """Clockwise corners using screen coordinates."""
    return [(x,y), (x+w,y), (x+w,y+h), (x,y+h), (x,y)]


def grid(art, x, y, cols, rows, unit, colour=SOFT, alpha=.36):
    for i in range(cols + 1):
        art.path(((x + i*unit,y), (x + i*unit,y + rows*unit)), colour, 1.4, alpha)
    for j in range(rows + 1):
        art.path(((x,y + j*unit), (x + cols*unit,y + j*unit)), colour, 1.4, alpha)
