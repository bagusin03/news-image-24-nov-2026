#!/usr/bin/env python3
"""news-image-20261124: one front-page image summing up Tuesday 24 November 2026.

Pure Python 3.13 standard library only. No network, no files read, no randomness,
no clock: the same bytes come out of every run. Draws a newspaper front page
("THE WORLD TODAY") with the day's verified stories:

  * COP31 climate talks collapse in Antalya (no deal on fossil fuels)
  * Ukraine sinks Russian corvette Merkury off Libya (Benghazi)
  * Iran vows to counter a US naval blockade (Strait of Hormuz)
  * Factory fire in Banten, Indonesia (at least 24 dead)
  * Thousands march in Lisbon over the cost of living
  * NATO sends AWACS early-warning aircraft to Poland
  * India-Nepal Saryu-Kamala Express flagged off
  * World Chess Championship: Gukesh defends his title in Geneva
  * Asian regulators step in as the AI stock sell-off calms

Output: /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png), 1024x1024 PNG.
"""

import binascii
import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 227)
INK = (20, 33, 61)
RED = (193, 39, 45)
BLUE = (29, 111, 184)
SKY = (178, 216, 240)
TEAL = (14, 124, 123)
GOLD = (232, 163, 23)
ORANGE = (232, 106, 23)
FLAME = (245, 158, 11)
GREEN = (46, 125, 50)
GREY = (107, 114, 128)
LIGHTGREY = (210, 208, 198)
WHITE = (255, 255, 255)
BLACK = (12, 12, 12)
SEA = (23, 92, 140)
SEALIGHT = (64, 148, 196)
BROWN = (120, 72, 32)

# ------------------------------------------------------- hand-drawn 5x7 font
FONT = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ',': ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ':': ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    '-': ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    '%': ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    '+': ["00000", "00100", "00100", "01110", "00100", "00100", "00000"],
    '=': ["00000", "00000", "11111", "00000", "11111", "00000", "00000"],
    '*': ["00000", "10101", "01110", "11111", "01110", "10101", "00000"],
    '"': ["01010", "01010", "00000", "00000", "00000", "00000", "00000"],
}


def text_width(s, scale):
    return len(s) * 6 * scale - scale


def wrap_text(s, max_w, scale):
    """Greedy word wrap; returns list of lines fitting max_w pixels."""
    lines = []
    for raw in s.split("\n"):
        words = raw.split(" ")
        cur = ""
        for wd in words:
            trial = wd if not cur else cur + " " + wd
            if text_width(trial, scale) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
    return lines


# ------------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.buf = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.buf), 3):
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = r, g, b

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i], self.buf[i + 1], self.buf[i + 2] = c

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                j = base + (xx - x0) * 3
                self.buf[j], self.buf[j + 1], self.buf[j + 2] = c

    def border(self, x, y, w, h, c, t=3):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, wd=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err, x, y = dx - dy, x0, y0
        r = max(1, wd // 2)
        while True:
            self.circle(x, y, r, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy

    def circle(self, cx, cy, r, c):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for dy in range(-ry, ry + 1):
            dx = int(rx * math.sqrt(max(0.0, 1.0 - (dy * dy) / float(ry * ry))))
            self.rect(cx - dx, cy + dy, 2 * dx + 1, 1, c)

    def poly(self, pts, c):
        """Filled polygon via scanline."""
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if y0 == y1:
                    continue
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                self.rect(int(math.ceil(xs[k])), y,
                          int(math.floor(xs[k + 1])) - int(math.ceil(xs[k])) + 1, 1, c)

    def text(self, x, y, s, c, scale=2):
        cx = x
        for ch in s.upper():
            g = FONT.get(ch, FONT[' '])
            for row in range(7):
                for col in range(5):
                    if g[row][col] == '1':
                        self.rect(cx + col * scale, y + row * scale, scale, scale, c)
            cx += 6 * scale
        return cx

    def text_center(self, cx, y, s, c, scale=2):
        self.text(cx - text_width(s, scale) // 2, y, s, c, scale)

    def para(self, x, y, s, c, max_w, scale=2, leading=None):
        lh = leading if leading is not None else 9 * scale
        for line in wrap_text(s, max_w, scale):
            self.text(x, y, line, c, scale)
            y += lh
        return y


def panel(cv, x, y, w, h, tag, tag_color=RED):
    cv.rect(x, y, w, h, WHITE)
    cv.border(x, y, w, h, INK, 3)
    cv.rect(x, y, w, 26, INK)
    cv.text(x + 10, y + 5, tag, WHITE, 2)


# ------------------------------------------------------------------- scenes
def draw_globe(cv, cx, cy, r):
    cv.circle(cx, cy, r, BLUE)
    # land blobs
    cv.ellipse(cx - 38, cy - 30, 34, 20, GREEN)
    cv.ellipse(cx + 34, cy - 42, 26, 16, GREEN)
    cv.ellipse(cx + 44, cy + 34, 30, 18, GREEN)
    cv.ellipse(cx - 42, cy + 38, 24, 14, GREEN)
    cv.ellipse(cx - 4, cy + 8, 18, 26, GREEN)
    # clouds
    cv.ellipse(cx - 52, cy - 58, 26, 8, WHITE)
    cv.ellipse(cx + 48, cy + 2, 24, 7, WHITE)
    # crack: red zigzag across the globe
    cv.line(cx - r + 8, cy - 40, cx - 20, cy - 8, RED, 5)
    cv.line(cx - 20, cy - 8, cx + 6, cy + 22, RED, 5)
    cv.line(cx + 6, cy + 22, cx + 30, cy - 6, RED, 5)
    cv.line(cx + 30, cy - 6, cx + r - 6, cy + 34, RED, 5)
    # smoke puffs above
    for sx, sy, sr in ((cx - 70, cy - r - 6, 11), (cx - 46, cy - r - 16, 14),
                       (cx - 18, cy - r - 8, 10)):
        cv.circle(sx, sy, sr, GREY)
    # outline ring
    for a in range(0, 360, 2):
        rad = math.radians(a)
        cv.circle(int(cx + r * math.cos(rad)), int(cy + r * math.sin(rad)), 2, INK)


def draw_ship_scene(cv, x, y, w, h):
    """Warship scene sized for an h=80 art band."""
    cv.rect(x, y, w, h, SKY)
    cv.circle(x + w - 34, y + 16, 14, GOLD)  # sun
    cv.rect(x, y + h - 36, w, 36, SEA)
    cv.rect(x, y + h - 36, w, 4, SEALIGHT)
    # capsizing corvette: tilted grey hull
    cv.poly([(x + 24, y + h - 46), (x + 140, y + h - 56), (x + 156, y + h - 40),
             (x + 140, y + h - 28), (x + 36, y + h - 28)], GREY)
    cv.rect(x + 70, y + h - 64, 8, 20, GREY)  # mast
    cv.line(x + 70, y + h - 64, x + 88, y + h - 68, INK, 3)
    # explosion starburst
    ex, ey = x + 140, y + 26
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        cv.line(ex, ey, int(ex + 18 * math.cos(rad)), int(ey + 18 * math.sin(rad)), ORANGE, 5)
    cv.circle(ex, ey, 11, FLAME)
    cv.circle(ex, ey, 5, WHITE)
    # sea drones: small triangles with wakes
    for dx in (x + 18, x + 52, x + 196):
        cv.poly([(dx, y + h - 22), (dx + 16, y + h - 16), (dx, y + h - 10)], INK)
        cv.line(dx - 14, y + h - 16, dx - 2, y + h - 16, WHITE, 2)
    # smoke
    cv.circle(x + 124, y + 10, 9, GREY)
    cv.circle(x + 140, y + 4, 7, GREY)


def draw_hormuz_scene(cv, x, y, w, h):
    """Strait scene sized for an h=80 art band."""
    cv.rect(x, y, w, h, SKY)
    cv.circle(x + 36, y + 16, 13, GOLD)
    # cliffs both sides
    cv.poly([(x, y + h), (x, y + 48), (x + 44, y + 64), (x + 40, y + h)], BROWN)
    cv.poly([(x + w, y + h), (x + w, y + 48), (x + w - 44, y + 64), (x + w - 40, y + h)], BROWN)
    # strait water
    cv.rect(x, y + h - 36, w, 36, SEA)
    for wy in range(y + h - 28, y + h - 8, 12):
        cv.line(x + 60, wy, x + w - 60, wy, SEALIGHT, 2)
    # tanker silhouette
    cv.rect(x + 70, y + h - 58, 140, 24, BLACK)
    cv.rect(x + 182, y + h - 76, 22, 18, BLACK)
    cv.rect(x + 70, y + h - 64, 140, 6, RED)
    # small naval ship behind
    cv.poly([(x + 228, y + h - 44), (x + 288, y + h - 44), (x + 282, y + h - 32),
             (x + 234, y + h - 32)], GREY)
    cv.rect(x + 252, y + h - 56, 5, 12, GREY)


def draw_fire_scene(cv, x, y, w, h):
    """Factory-fire scene sized for an h=120 art band."""
    cv.rect(x, y, w, h, (250, 226, 190))
    # factory silhouette
    cv.rect(x + 24, y + h - 60, 150, 60, INK)
    cv.rect(x + 190, y + h - 44, 90, 44, INK)
    cv.rect(x + 40, y + h - 96, 18, 40, INK)  # chimney
    for wx in range(x + 38, x + 160, 34):
        cv.rect(wx, y + h - 44, 18, 18, GOLD)
    # flames on the roof (short enough to stay inside the band)
    for fx, fh in ((x + 52, 28), (x + 92, 36), (x + 132, 30), (x + 206, 24)):
        cv.poly([(fx - 16, y + h - 58), (fx, y + h - 58 - fh), (fx + 16, y + h - 58)], ORANGE)
        cv.poly([(fx - 9, y + h - 58), (fx, y + h - 58 - fh + 14), (fx + 9, y + h - 58)], FLAME)
    # smoke
    for sx, sy, sr in ((x + 48, y + 18, 10), (x + 74, y + 12, 11), (x + 100, y + 20, 9),
                       (x + 204, y + 14, 10)):
        cv.circle(sx, sy, sr, GREY)


def draw_protest_scene(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    cv.rect(x, y + h - 40, w, 40, LIGHTGREY)
    # crowd: rows of heads + bodies
    for i, hx in enumerate(range(x + 22, x + w - 20, 34)):
        hy = y + h - 78 - (14 if i % 2 else 0)
        cv.circle(hx, hy, 11, (232, 190, 150) if i % 3 else (190, 140, 110))
        cv.rect(hx - 12, hy + 11, 24, 30, RED if i % 4 == 0 else TEAL if i % 4 == 1 else BLUE)
    # placards
    cv.rect(x + 30, y + 22, 92, 34, WHITE)
    cv.border(x + 30, y + 22, 92, 34, INK, 2)
    cv.text(x + 38, y + 30, "PRICES", INK, 2)
    cv.rect(x + 150, y + 14, 110, 34, GOLD)
    cv.border(x + 150, y + 14, 110, 34, INK, 2)
    cv.text(x + 158, y + 22, "ENOUGH!", INK, 2)
    cv.line(x + 76, y + 56, x + 76, y + 84, INK, 3)
    cv.line(x + 205, y + 48, x + 205, y + 84, INK, 3)


def draw_awacs_scene(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    for cx, cy, cr in ((x + 40, y + 22, 10), (x + 66, y + 14, 13), (x + 96, y + 24, 9)):
        cv.circle(cx, cy, cr, WHITE)
    # AWACS: fuselage + radar disc on top
    cv.ellipse(x + w // 2, y + h - 62, 110, 16, WHITE)
    cv.poly([(x + w // 2 - 108, y + h - 62), (x + w // 2 - 140, y + h - 40),
             (x + w // 2 - 96, y + h - 52)], WHITE)
    cv.poly([(x + w // 2 + 108, y + h - 62), (x + w // 2 + 138, y + h - 44),
             (x + w // 2 + 96, y + h - 52)], WHITE)
    cv.rect(x + w // 2 - 14, y + h - 108, 8, 34, INK)
    cv.ellipse(x + w // 2, y + h - 108, 58, 9, INK)
    cv.rect(x + w // 2 + 66, y + h - 68, 20, 6, INK)  # cockpit windows
    cv.circle(x + w // 2 + 96, y + h - 62, 5, RED)
    # contrail
    cv.line(x + 16, y + h - 40, x + w // 2 - 120, y + h - 52, WHITE, 3)
    # ground + flag mast
    cv.rect(x, y + h - 22, w, 22, GREEN)
    cv.rect(x + w - 44, y + h - 58, 4, 36, INK)
    cv.rect(x + w - 40, y + h - 58, 30, 12, WHITE)
    cv.rect(x + w - 40, y + h - 46, 30, 12, RED)


def draw_train_icon(cv, x, y, w, h):
    """Train icon fitted to a 96-wide box."""
    cv.rect(x, y, w, h, SKY)
    cv.rect(x, y + h - 26, w, 26, (90, 90, 90))
    cv.line(x, y + h - 14, x + w, y + h - 14, INK, 3)
    # loco + car
    cv.rect(x + 8, y + 24, 56, 48, RED)
    cv.rect(x + 64, y + 34, 28, 38, TEAL)
    cv.rect(x + 52, y + 16, 8, 10, INK)  # chimney
    for wx in (x + 16, x + 36):
        cv.rect(wx, y + 32, 16, 16, WHITE)
    cv.rect(x + 70, y + 42, 14, 12, WHITE)
    for wx in (x + 22, x + 48, x + 78):
        cv.circle(wx, y + 78, 8, INK)


def draw_chess_icon(cv, x, y, w, h):
    cv.rect(x, y, w, h, WHITE)
    bs = 20
    ox, oy = x + 8, y + 8
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                cv.rect(ox + c * bs, oy + r * bs, bs, bs, INK)
    # king: gold disc with dark ring, cross on top
    kx, ky = ox + 40, oy + 40
    cv.circle(kx, ky, 15, INK)
    cv.circle(kx, ky, 11, GOLD)
    cv.rect(kx - 2, ky - 18, 4, 12, GOLD)
    cv.rect(kx - 8, ky - 14, 16, 4, GOLD)


def draw_chart_icon(cv, x, y, w, h):
    """Chart icon fitted to a 96-wide box."""
    cv.rect(x, y, w, h, WHITE)
    cv.line(x + 12, y + h - 18, x + w - 12, y + h - 18, INK, 3)
    cv.line(x + 12, y + 12, x + 12, y + h - 18, INK, 3)
    pts = [(x + 20, y + 36), (x + 38, y + 56), (x + 54, y + 48),
           (x + 68, y + 68), (x + 82, y + 38)]
    for a, b in zip(pts, pts[1:]):
        cv.line(a[0], a[1], b[0], b[1], TEAL, 4)
    cv.poly([(pts[-1][0] - 2, pts[-1][1]), (pts[-1][0] + 12, pts[-1][1] - 3),
             (pts[-1][0] + 2, pts[-1][1] + 10)], TEAL)


# ------------------------------------------------------------------- layout
def build():
    cv = Canvas(W, H, PAPER)
    # masthead
    cv.rect(0, 0, W, 8, RED)
    cv.text_center(W // 2, 18, "THE WORLD TODAY", INK, 6)
    cv.rect(12, 88, W - 24, 3, INK)
    cv.rect(12, 96, W - 24, 36, RED)
    cv.text_center(W // 2, 104, "TUESDAY 24 NOVEMBER 2026", WHITE, 3)
    cv.text_center(W // 2, 136, "THE DAY'S WORLD NEWS - IN ONE PICTURE", INK, 1)

    # ---- row 1: lead COP31 + Ukraine + Iran
    panel(cv, 12, 156, 600, 366, "CLIMATE - ANTALYA, TURKIYE")
    draw_globe(cv, 190, 320, 92)
    cv.rect(330, 236, 250, 62, RED)
    cv.text(348, 250, "NO DEAL", WHITE, 4)
    cv.text(348, 282, "FIRST COLLAPSE", WHITE, 2)
    cv.text(348, 300, "SINCE 2009", WHITE, 2)
    cv.text(330, 316, "COP31 ends in disarray.", INK, 2)
    cv.text(36, 436, "COP31 COLLAPSES", INK, 4)
    cv.para(36, 472, "Nearly 200 nations fail to agree a climate pact - no mention of fossil fuels in the final text.",
            INK, 552, 2)

    panel(cv, 624, 156, 388, 182, "WAR - LIBYA")
    draw_ship_scene(cv, 627, 185, 382, 80)
    cv.text(636, 270, "WARSHIP SUNK", INK, 3)
    cv.text(636, 298, "OFF LIBYA", INK, 3)
    cv.para(636, 326, "Ukraine drones sink Russian corvette Merkury in Benghazi.", INK, 364, 1)

    panel(cv, 624, 350, 388, 172, "GULF - STRAIT OF HORMUZ")
    draw_hormuz_scene(cv, 627, 379, 382, 80)
    cv.text(636, 464, "IRAN VOWS TO FIGHT", INK, 3)
    cv.para(636, 496, "Tehran: it will use all tools against a US naval blockade.", INK, 364, 1)

    # ---- row 2: Indonesia fire, Lisbon protest, NATO Poland
    panel(cv, 12, 534, 325, 266, "DISASTER - INDONESIA")
    draw_fire_scene(cv, 15, 563, 319, 120)
    cv.text(24, 690, "FACTORY FIRE", INK, 3)
    cv.text(24, 718, "KILLS 24+", INK, 3)
    cv.para(24, 748, "Blaze at a Banten candy factory - rescue search goes on for the missing.",
            INK, 301, 2)

    panel(cv, 349, 534, 326, 266, "PROTEST - LISBON")
    draw_protest_scene(cv, 352, 563, 320, 120)
    cv.text(361, 690, "LISBON MARCHES", INK, 3)
    cv.text(361, 718, "ON PRICES", INK, 3)
    cv.para(361, 748, "Thousands take to the streets over the rising cost of living.",
            INK, 302, 2)

    panel(cv, 687, 534, 325, 266, "SECURITY - POLAND")
    draw_awacs_scene(cv, 690, 563, 319, 120)
    cv.text(699, 690, "NATO SENDS", INK, 3)
    cv.text(699, 718, "AWACS TO POLAND", INK, 3)
    cv.para(699, 748, "Early-warning jets after Russian missiles land on NATO soil.",
            INK, 301, 2)

    # ---- row 3: train, chess, markets
    panel(cv, 12, 812, 325, 150, "ASIA")
    draw_train_icon(cv, 20, 844, 96, 96)
    cv.text(128, 852, "INDIA-NEPAL", INK, 2)
    cv.text(128, 872, "TRAIN ROLLS", INK, 2)
    cv.para(128, 900, "Saryu-Kamala Express flagged off, Ayodhya to Janakpur.", INK, 196, 1)

    panel(cv, 349, 812, 326, 150, "SPORT - GENEVA")
    draw_chess_icon(cv, 357, 844, 96, 96)
    cv.text(465, 852, "CHESS CROWN", INK, 2)
    cv.text(465, 872, "DEFENCE BEGINS", INK, 2)
    cv.para(465, 900, "Gukesh v Sindarov for the world title.", INK, 198, 1)

    panel(cv, 687, 812, 325, 150, "MARKETS")
    draw_chart_icon(cv, 695, 844, 96, 96)
    cv.text(803, 852, "AI SELL-OFF", INK, 2)
    cv.text(803, 872, "CALMS", INK, 2)
    cv.para(803, 900, "Asian regulators step in; stock futures rally.", INK, 198, 1)

    # footer
    cv.rect(12, 974, W - 24, 3, INK)
    cv.text_center(W // 2, 986, "COP31 - LIBYA - HORMUZ - BANTEN - LISBON - POLAND", INK, 2)
    return cv


# ---------------------------------------------------------------- PNG writer
def chunk(kind, data):
    out = struct.pack(">I", len(data)) + kind + data
    out += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw.extend(cv.buf[y * cv.w * 3:(y + 1) * cv.w * 3])
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = encode_png(build())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print(f"wrote {path}: {len(data)} bytes, {W}x{H}")


if __name__ == "__main__":
    main()
