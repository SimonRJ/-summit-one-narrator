"""The Summit One studio palette, staged diagrams and speech cue timing."""

from functools import lru_cache
from pathlib import Path
import math
import re

import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont


WIDTH = 1280
HEIGHT = 720
BG = "#111821"
WHITE = "#f2f1ed"
MUTED = "#a8b3bf"
GOLD = "#eeb765"
BLUE = "#7eb5f3"
MINT = "#9cdbbc"
RED = "#f39299"
SLATE = "#283747"
PANEL = "#1a2532"
RIM = "#3c4b59"
ROOT = Path(__file__).resolve().parents[2]


def clamp(value):
    return min(1.0, max(0.0, value))


def ease(value):
    t = clamp(value)
    return t * t * (3.0 - 2.0 * t)


def mix(start, end, t):
    return start + (end - start) * t


def between(t, start, duration=0.6):
    return ease((t - start) / duration)


@lru_cache(maxsize=128)
def rgb(color):
    return ImageColor.getrgb(color) if isinstance(color, str) else color


def blend(first, second, amount):
    return tuple(round(mix(x, y, amount)) for x, y in zip(rgb(first), rgb(second)))


def phrase_words(text):
    return [re.sub(r"[^a-z0-9]", "", word.lower()) for word in text.split()]


class Moment:
    def __init__(self, scene, t):
        self.scene = scene
        self.t = t
        self.start = scene["start"]
        self.local = t - self.start
        self.words = scene["words"]
        self.tokens = tuple(phrase_words(" ".join(word["text"] for word in self.words)))

    def at(self, phrase):
        needle = tuple(phrase_words(phrase))
        for index in range(len(self.tokens) - len(needle) + 1):
            if self.tokens[index:index + len(needle)] == needle:
                return self.words[index]["start"]
        raise ValueError(f"Scene {self.scene['n']} has no spoken cue {phrase!r}")

    def reveal(self, phrase, duration=0.55, offset=0.0):
        return between(self.t, self.at(phrase) + offset, duration)


@lru_cache(maxsize=96)
def font(px, bold):
    suffix = "Bold" if bold else "Regular"
    path = Path(f"/usr/share/fonts/truetype/open-sans/OpenSans-{suffix}.ttf")
    if path.exists():
        return ImageFont.truetype(str(path), px)
    fallback = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(fallback, px)


@lru_cache(maxsize=620)
def lettering(text, size, color, bold):
    face = font(size, bold)
    left, top, right, bottom = face.getbbox(text, stroke_width=0)
    im = Image.new("RGBA", (max(1, right - left + 4), max(1, bottom - top + 4)))
    ImageDraw.Draw(im).text((2 - left, 2 - top), text, font=face, fill=(*rgb(color), 255))
    return im


@lru_cache(maxsize=3)
def background(scale):
    width, height = round(WIDTH * scale), round(HEIGHT * scale)
    yy, xx = np.ogrid[:height, :width]
    radial = np.clip(1.0 - np.sqrt(((xx / width - 0.5) * 1.3)**2 + (yy / height - 0.42)**2), 0, 1)**2
    cold = np.asarray((14, 20, 28))
    light = np.asarray((13, 17, 23))
    return Image.fromarray((cold[None, None, :] + radial[:, :, None] * light[None, None, :]).astype("uint8"), "RGB")


@lru_cache(maxsize=90)
def counter_asset(colour, size):
    image = Image.open(ROOT / f"production/t021-studio/assets/{colour}.png").convert("RGBA")
    bounds = image.getbbox()
    image = image.crop(bounds)
    height = round(size * image.height / image.width)
    return image.resize((size, height), Image.Resampling.LANCZOS)


class Stage:
    def __init__(self, scale):
        self.image = background(scale).copy()
        self.scale = scale
        self.draw = ImageDraw.Draw(self.image)

    def px(self, value):
        return round(value * self.scale)

    def text(self, text, x, y, size=30, color=WHITE, *, bold=False, opacity=1.0, align="center"):
        if opacity <= 0:
            return
        icon = lettering(text, self.px(size), color, bold)
        position = self.px(x)
        if align == "center":
            position -= icon.width // 2
        elif align == "right":
            position -= icon.width
        self.paste(icon, position, self.px(y) - icon.height // 2, opacity)

    def paste(self, source, x, y, opacity=1.0):
        if opacity <= 0:
            return
        alpha = source.getchannel("A")
        if opacity < 0.999:
            alpha = alpha.point([round(i * clamp(opacity)) for i in range(256)])
        self.image.paste(source, (x, y), alpha)

    def line(self, points, color=RIM, width=2, opacity=1.0):
        if opacity > 0:
            self.draw.line(
                [(self.px(x), self.px(y)) for x, y in points],
                fill=blend(BG, color, clamp(opacity)), width=max(1, self.px(width)), joint="curve",
            )

    def box(self, x, y, width, height, *, radius=14, fill=PANEL, edge=None, stroke=2, opacity=1.0):
        if opacity <= 0:
            return
        self.draw.rounded_rectangle(
            tuple(self.px(value) for value in (x, y, x + width, y + height)),
            self.px(min(radius, width / 2, height / 2)),
            fill=blend(BG, fill, opacity) if fill else None,
            outline=blend(BG, edge, opacity) if edge else None,
            width=max(1, self.px(stroke)),
        )

    def dot(self, x, y, radius, color, opacity=1.0):
        if opacity > 0:
            self.draw.ellipse(
                tuple(self.px(v) for v in (x - radius, y - radius, x + radius, y + radius)),
                fill=blend(BG, color, clamp(opacity)),
            )

    def arrow(self, p, q, color=GOLD, progress=1.0, width=3):
        if progress <= 0:
            return
        x, y = mix(p[0], q[0], progress), mix(p[1], q[1], progress)
        angle = math.atan2(q[1] - p[1], q[0] - p[0])
        self.line((p, (x, y)), color, width)
        if progress > 0.7:
            length = 11
            self.line(
                [(x - length * math.cos(angle - 0.5), y - length * math.sin(angle - 0.5)), (x, y),
                 (x - length * math.cos(angle + 0.5), y - length * math.sin(angle + 0.5))],
                color, width, clamp((progress - 0.7) / 0.3),
            )

    def coin(self, x, y, colour="gold", width=52, opacity=1.0):
        if opacity <= 0:
            return
        image = counter_asset(colour, self.px(width))
        self.paste(image, self.px(x) - image.width // 2, self.px(y) - image.height // 2, opacity)

    def heading(self, title, subtitle=None, *, opacity=1.0):
        size = 48 if len(title) < 40 else 43
        self.text(title, 640, 87, size, bold=True, opacity=opacity)
        if subtitle:
            self.text(subtitle, 640, 143, 26, MUTED, opacity=opacity)

    def bracket(self, x0, x1, y, label, colour, opacity=1.0):
        self.line([(x0, y - 8), (x0, y), (x1, y), (x1, y - 8)], colour, 2, opacity)
        self.text(label, (x0 + x1) / 2, y + 28, 25, colour, bold=True, opacity=opacity)

    def terms(self, parts, y, size=44):
        """Place an aligned equation without shifting existing terms when others appear."""
        labels = [lettering(text, self.px(size), color, True) for text, color, _ in parts]
        gap = self.px(12)
        row_width = sum(label.width for label in labels) + gap * (len(labels) - 1)
        x = (self.image.width - row_width) // 2
        for (_, _, opacity), label in zip(parts, labels):
            self.paste(label, x, self.px(y) - label.height // 2, opacity)
            x += label.width + gap

    def caption(self, caption, t):
        opacity = min(ease((t - caption["start"]) / 0.12), ease((caption["end"] - t) / 0.14))
        if opacity <= 0:
            return
        text = caption["text"]
        size = 34
        while lettering(text, self.px(size), WHITE, True).width > self.px(1130) and size > 28:
            size -= 1
        caption_width = lettering(text, self.px(size), WHITE, True).width / self.scale
        width = caption_width + 42
        self.box((1280 - width) / 2, 636, width, 60, fill="#101720", radius=13, opacity=opacity)
        self.text(text, 640, 667, size, WHITE, bold=True, opacity=opacity)
