#!/usr/bin/env python3
"""BODY SCIENCE — NAYA ANIMATED engine (purana static-photo engine DELETED).
Har video me asli hilta-hua animation: characters, drawings, arrows, particles, diagrams.
8 topics (body ke 'kyun hota hai' raaz). Voice: edge-tts MadhurNeural -> gTTS fallback.
Usage: python cloud_body_science.py --index N [--upload]
"""
import os, sys, subprocess, shutil, asyncio, datetime, math, glob
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests

W, H, FPS = 1080, 1920, 30
BASE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(BASE, "output"), exist_ok=True)
TMP = "/tmp/bodyv3"
os.makedirs(TMP, exist_ok=True)

FF = shutil.which("ffmpeg")
if not FF:
    try:
        import imageio_ffmpeg
        FF = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        FF = "ffmpeg"
FP = shutil.which("ffprobe")

def _find_font(bold):
    names = [f"/usr/share/fonts/truetype/dejavu/DejaVuSans{'-Bold' if bold else ''}.ttf",
             f"/usr/share/fonts/truetype/DejaVu/DejaVuSans{'-Bold' if bold else ''}.ttf"]
    names += glob.glob(f"/usr/share/fonts/**/DejaVuSans{'-Bold' if bold else ''}.ttf", recursive=True)
    for c in names:
        if os.path.exists(c):
            return c
    return None
FB = _find_font(True); FN = _find_font(False) or FB
_FC = {}
def font(bold, size):
    key = (FB if bold else FN, size)
    if key not in _FC:
        _FC[key] = ImageFont.truetype(key[0], size)
    return _FC[key]

# ---------------- helpers ----------------
def seg(p, a, b):
    if b <= a:
        return 1.0 if p >= b else 0.0
    return max(0.0, min(1.0, (p - a) / (b - a)))

def dot(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)

def rr(d, box, rad, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=rad, fill=fill, outline=outline, width=width)

def sine(d, x0, x1, y, amp, wl, ph, color, w=6):
    pts = []
    x = x0
    while x <= x1:
        pts.append((x, y + amp * math.sin((x / wl) * 2 * math.pi + ph)))
        x += 10
    if len(pts) > 1:
        d.line(pts, fill=color, width=w, joint="curve")

def label(d, cx, cy, text, accent, size=40):
    while size > 26 and d.textlength(text, font=font(True, size)) + 90 > 990:
        size -= 2
    f = font(True, size)
    tw = d.textlength(text, font=f)
    rr(d, [cx - tw / 2 - 30, cy - size * 0.85, cx + tw / 2 + 30, cy + size * 0.85],
       int(size * 0.95), fill=(8, 12, 24, 235), outline=accent + (255,), width=3)
    d.text((cx, cy), text, font=f, fill=(255, 255, 255, 255), anchor="mm")

def wrap(d, text, f, maxw, maxlines=2):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t2 = (cur + " " + wd).strip()
        if d.textlength(t2, font=f) <= maxw:
            cur = t2
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        last = lines[-1]
        while d.textlength(last + "...", font=f) > maxw and len(last) > 4:
            last = last[:-2]
        lines[-1] = last + "..."
    return lines

def hair(d, x, y, adeg, ln, color, w=9):
    a = math.radians(adeg)
    x2 = x + ln * math.sin(a); y2 = y - ln * math.cos(a)
    d.line([(x, y), (x2, y2)], fill=color, width=w)

def tear(d, x, y, r, col):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.polygon([(x - 0.8 * r, y - 0.2 * r), (x + 0.8 * r, y - 0.2 * r), (x, y - 2.1 * r)], fill=col)

def soft_sprite(r, color, alpha):
    yy, xx = np.mgrid[-r:r, -r:r]
    dist = np.sqrt(xx * xx + yy * yy) / max(1, r)
    a = (np.clip(1 - dist, 0, 1) ** 2 * alpha).astype(np.uint8)
    arr = np.zeros((2 * r, 2 * r, 4), dtype=np.uint8)
    arr[..., 0] = color[0]; arr[..., 1] = color[1]; arr[..., 2] = color[2]; arr[..., 3] = a
    return Image.fromarray(arr, "RGBA")

def make_grad(c1, c2):
    a = np.linspace(0, 1, H).reshape(-1, 1, 1)
    top = np.array(c1, dtype=float); bot = np.array(c2, dtype=float)
    arr = (top * (1 - a) + bot * a).astype(np.uint8)
    arr = np.repeat(arr, W, axis=1)
    return Image.fromarray(arr, "RGB")

# ---------------- 8 ANIMATED TOPICS ----------------
def dt_wrinkles(d, A, bi, p, t):
    ac = (110, 225, 255)
    cx = A["cx"]
    wy = A["y1"] - 250
    d.rectangle([80, wy, 1000, A["y1"] - 18], fill=(14, 52, 96, 235))
    sine(d, 90, 990, wy + 16, 12, 240, t * 1.8, (80, 170, 250, 190), 6)
    sine(d, 90, 990, wy + 44, 9, 200, t * 1.8 + 2.1, (56, 130, 220, 160), 5)
    for k in range(2):
        r = 90 + k * 46 + 16 * math.sin(t * 2.6 + k)
        d.ellipse([cx - r, wy - r * 0.26, cx + r, wy + r * 0.26], outline=(120, 200, 255, 110), width=4)
    top = wy - 470
    rr(d, [cx - 72, top, cx + 72, wy + 40], 64, fill=(242, 196, 155, 255))
    rr(d, [cx - 74, top + 120, cx + 74, top + 152], 16, fill=(230, 180, 140, 180))
    rr(d, [cx - 74, top + 250, cx + 74, top + 282], 16, fill=(230, 180, 140, 180))
    rr(d, [cx - 42, top + 16, cx + 42, top + 112], 40, fill=(255, 232, 214, 255), outline=(235, 200, 180, 255), width=3)
    if bi == 0:
        d.text((cx, top - 74), "PAANI MEIN 5 MINUTE...", font=font(True, 42), fill=ac + (255,), anchor="mm")
        dp = (t * 0.8) % 1.4
        if dp < 1:
            dot(d, cx + 170 + 30 * math.sin(t * 2), top - 150 + dp * (wy - top + 130), 14, (120, 200, 255, 220))
        d.text((cx + 250, top + 30), "?", font=font(True, 90), fill=(255, 209, 102, 255), anchor="mm")
    if bi == 1:
        wr = seg(p, 0.02, 0.45)
        for i, yy in enumerate([top + 180, top + 226, top + 272]):
            wob = 5 * math.sin(t * 3 + i)
            d.arc([cx - 58 + wob, yy - 26, cx - 12 + wob, yy + 26], -80, 80, fill=(160, 95, 60, int(235 * wr)), width=7)
            d.arc([cx + 12 + wob, yy - 26, cx + 58 + wob, yy + 26], 100, 260, fill=(160, 95, 60, int(235 * wr)), width=7)
        d.line([(cx, top + 34), (cx, wy + 10)], fill=(255, 90, 120, 230), width=9)
        for k in range(3):
            pp = (t * 0.75 + k / 3.0) % 1.0
            dot(d, cx, top + 44 + pp * (wy - top - 40), 11, (255, 255, 255, 235))
        ax = cx - 150 - 12 * math.sin(t * 4)
        d.line([(ax, top + 210), (ax + 66, top + 210)], fill=ac + (255,), width=8)
        d.polygon([(ax + 72, top + 210), (ax + 40, top + 193), (ax + 40, top + 227)], fill=ac + (255,))
        ax2 = cx + 150 + 12 * math.sin(t * 4)
        d.line([(ax2, top + 210), (ax2 - 66, top + 210)], fill=ac + (255,), width=8)
        d.polygon([(ax2 - 72, top + 210), (ax2 - 40, top + 193), (ax2 - 40, top + 227)], fill=ac + (255,))
        label(d, cx, top - 74, "Nerves ungli sikodte hain!", ac, 42)
    if bi == 2:
        d.line([(cx, top + 34), (cx, top + 160)], fill=(255, 90, 120, 230), width=9)
        d.line([(cx, top + 245), (cx, wy + 10)], fill=(255, 90, 120, 70), width=9)
        d.line([(cx - 42, top + 205), (cx + 42, top + 160)], fill=(255, 80, 80, 235), width=12)
        d.line([(cx + 42, top + 205), (cx - 42, top + 160)], fill=(255, 80, 80, 235), width=12)
        label(d, cx, top - 74, "Nerve kharab = jhurriyan NAHI!", (126, 231, 135), 42)

def _face_side(d, cx, cy, r, mopen, t, seed=0):
    dot(d, cx, cy, r, (242, 196, 155, 255))
    ey = cy - 0.25 * r
    if int(t * 1.3 + seed) % 4 == 3:
        d.line([(cx + 0.28 * r, ey), (cx + 0.62 * r, ey)], fill=(60, 40, 30, 255), width=6)
    else:
        dot(d, cx + 0.44 * r, ey, 0.1 * r, (60, 40, 30, 255))
    d.line([(cx + 0.2 * r, cy - 0.52 * r), (cx + 0.62 * r, cy - 0.58 * r)], fill=(70, 50, 40, 255), width=7)
    mh = r * (0.10 + 0.55 * mopen)
    d.ellipse([cx + 0.22 * r, cy + 0.22 * r, cx + 0.88 * r, cy + 0.22 * r + mh], fill=(95, 40, 45, 255))
    if mopen > 0.4:
        d.ellipse([cx + 0.3 * r, cy + 0.3 * r, cx + 0.72 * r, cy + 0.3 * r + mh * 0.5], fill=(200, 90, 95, 255))

def dt_yawn(d, A, bi, p, t):
    ac = (178, 141, 255)
    cx = A["cx"]
    if bi == 0:
        m = 0.5 + 0.5 * math.sin(t * 2.2)
        _face_side(d, cx - 120, 900, 200, m, t)
        for k in range(3):
            yy = 640 - ((t * 60 + k * 80) % 240)
            d.text((cx + 120 + 20 * math.sin(t * 2 + k), yy), "YAAAAWN!", font=font(True, 34 + k * 6), fill=(255, 209, 102, 220), anchor="mm")
        label(d, cx, 1240, "Dekhte hi yaad aa jati hai...", ac, 42)
    if bi == 1:
        _face_side(d, cx - 260, 860, 170, 0.9 if p > 0.15 else 0.1, t)
        _face_side(d, cx + 260, 860, 170, 0.9 if p > 0.72 else 0.15 + 0.6 * seg(p, 0.5, 0.72), t, seed=2)
        for k in range(5):
            pp = (p * 1.6 - k * 0.16) % 1.0
            xx = (cx - 120) + (240) * pp
            yy = 900 - 260 * math.sin(math.pi * pp)
            if 0.05 < pp < 0.98:
                dot(d, xx, yy, 13, (255, 209, 102, int(60 + 195 * min(1, p * 3))))
        label(d, cx, 1240, "Contagion = 'sympathy' effect!", ac, 42)
        d.text((cx, 540), "*brain cooling*", font=font(True, 36), fill=(150, 220, 255, 230), anchor="mm")
        for k in range(3):
            dot(d, cx - 90 + k * 90, 585 + 8 * math.sin(t * 2 + k), 7, (190, 230, 255, 200))
    if bi == 2:
        dot(d, cx - 150, 900, 150, (242, 196, 155, 255))  # dog head
        rr(d, [cx - 300, 880, cx - 180, 920], 20, fill=(200, 150, 110, 255))  # snout
        m = 0.4 + 0.5 * abs(math.sin(t * 1.8))
        d.ellipse([cx - 320, 900, cx - 220, 900 + 10 + 55 * m], fill=(95, 40, 45, 255))
        dot(d, cx + 120, 900, 130, (242, 196, 155, 255))
        rr(d, [cx + 20, 884, cx + 110, 916], 16, fill=(200, 150, 110, 255))
        d.ellipse([cx + 10, 900, cx + 95, 900 + 10 + 50 * max(0, math.sin(t * 1.8 + 0.6))], fill=(95, 40, 45, 255))
        label(d, cx, 1180, "KUTTA bhi jamhai leta hai!", ac, 42)

def dt_goose(d, A, bi, p, t):
    ac = (255, 154, 213)
    cx = A["cx"]
    if bi == 0:
        skin_x0, skin_x1, skin_y = 110, 970, 870
        rr(d, [skin_x0, skin_y, skin_x1, skin_y + 300], 60, fill=(236, 186, 150, 255))
        for r_ in range(3):
            rr(d, [skin_x0 + 30 + r_ * 300, skin_y + 40, skin_x0 + 250 + r_ * 300, skin_y + 260], 80, fill=(240, 196, 160, 255))
        for k in range(6):
            xx = 160 + k * 160
            a = 95 - 96 * min(1, max(0, (p - 0.12 * k) * 1.5))
            hair(d, xx, skin_y + 6, a, 180 - 70 * math.cos(math.radians(a)), (95, 62, 45, 255), 14)
            dot(d, xx, skin_y + 14, 15, (205, 130, 120, 230))
        for k in range(3):
            xx = 1080 - ((t * 260 + k * 300) % 1000)
            sine(d, xx, xx + 120, 800 + k * 30, 10, 90, t * 6, (150, 220, 255, 200), 6)
        label(d, cx, 1290, "Thand lagi... ya darr laga!", ac, 42)
        label(d, cx, 1390, "Dekho - baal seedhe khade ho gaye!", ac, 36)
    if bi == 1:
        skin_x0, skin_x1, skin_y = 110, 970, 950
        rr(d, [skin_x0, skin_y, skin_x1, skin_y + 260], 60, fill=(236, 186, 150, 255))
        for r_ in range(3):
            rr(d, [skin_x0 + 30 + r_ * 300, skin_y + 30, skin_x0 + 250 + r_ * 300, skin_y + 230], 80, fill=(240, 196, 160, 255))
        fx = 420
        a = 92 - 88 * seg(p, 0.05, 0.55)
        hair(d, fx, skin_y + 6, a, 240, (95, 62, 45, 255), 16)
        dot(d, fx, skin_y + 18, 26, (215, 120, 110, 245))
        d.arc([fx - 60, skin_y - 34 - 40, fx + 60, skin_y - 34 + 40], 0, 360, fill=(228, 170, 140, 255), width=18)
        mx = fx - 250; my = skin_y + 60
        d.ellipse([mx - 60, my - 60, mx + 100, my + 100], fill=(205, 90, 100, 255))
        for k in range(2):
            xx = mx + 20 + 60 * k + 6 * math.sin(t * 5 + k)
            d.line([(xx, my + 50 + k * 46), (xx + 34, my + 28 + k * 46)], fill=ac + (255,), width=8)
        for k in range(5):
            rr(d, [skin_x0 + 120 + k * 150, skin_y + 120, skin_x0 + 190 + k * 150, skin_y + 210], 28, fill=(228, 176, 140, 255))
        label(d, cx, 1290, "Chhoti muscle sikudti hai = hair khada!", ac, 40)
        label(d, cx, 1390, "Janwaron mein bachav ke liye - insaan mein purana reflex", ac, 34)
    if bi == 2:
        rr(d, [330, 700, 750, 1180], 60, fill=(60, 90, 160, 255))
        wv = seg(p, 0.0, 0.6)
        for r_ in range(5):
            for c_ in range(4):
                if wv > (r_ * 4 + c_) / 20.0:
                    dot(d, 390 + c_ * 100, 760 + r_ * 100, 12, (236, 186, 150, 255))
        d.ellipse([790, 780, 890, 880], fill=(30, 30, 40, 255))
        d.line([(840, 780), (840, 700)], fill=(30, 30, 40, 255), width=14)
        d.line([(840, 700), (880, 660)], fill=(30, 30, 40, 255), width=14)
        label(d, cx, 1260, "Music/khoobsurti se bhi rongte!", ac, 40)

def dt_teeth(d, A, bi, p, t):
    ac = (255, 176, 102)
    cx = A["cx"]
    for k in range(7):
        xx = (cx - 460 + k * 150 + 3 * t * 30) % 1060 + 60
        yy = 420 + ((t * 90 + k * 130) % 500)
        dot(d, xx, yy, 8, (200, 230, 255, 190))
    if bi == 0:
        dot(d, cx, 830, 210, (242, 196, 155, 255))
        rr(d, [cx + 130, 810, cx + 260, 860], 22, fill=(200, 150, 110, 255))
        j = 10 * math.sin(t * 26)
        for k in range(4):
            rr(d, [cx + 30 + k * 30, 940 + j, cx + 52 + k * 30, 985 + j], 6, fill=(255, 255, 255, 255))
            rr(d, [cx + 30 + k * 30, 905, cx + 52 + k * 30, 935], 6, fill=(255, 255, 255, 255))
        d.line([(cx + 20, 990 + j), (cx + 190, 990 + j)], fill=(95, 40, 45, 255), width=8)
        label(d, cx, 1230, "BRRR... kitni thand!", ac, 44)
    if bi == 1:
        for k in range(6):
            r = 20 + k * 20
            d.arc([cx - 300 - r * 0.2, 760 - r * 0.5, cx + 60 + r * 0.2, 1100 + r * 0.5], 200, 340, fill=(255, 176, 102, max(0, 160 - k * 24)), width=6)
        for k in range(4):
            sine(d, 150 + k * 200 + 8 * math.sin(t * 3 + k), 250 + k * 200, 1150, 12, 70, t * 7 + k, (255, 150, 90, 200), 6)
        j = 8 * math.sin(t * 30)
        for k in range(5):
            rr(d, [cx - 260 + k * 80, 940 + j, cx - 220 + k * 80, 990 + j], 8, fill=(255, 255, 255, 255))
            rr(d, [cx - 260 + k * 80, 880, cx - 220 + k * 80, 930], 8, fill=(255, 255, 255, 255))
        rr(d, [820, 700, 900, 1150], 40, fill=(20, 26, 40, 240), outline=(255, 176, 102, 255), width=5)
        fillh = int(430 * seg(p, 0.1, 0.85))
        if fillh > 10:
            rr(d, [828, 1142 - fillh, 892, 1142], 30, fill=(255, 90, 90, 255))
        label(d, cx, 1250, "Muscles kaanpte = garmi banti!", ac, 40)
    if bi == 2:
        rr(d, [480, 620, 600, 1120], 50, fill=(20, 26, 40, 240), outline=(126, 231, 135, 255), width=6)
        rr(d, [492, 640, 588, 1100], 45, fill=(255, 90, 90, 255))
        d.text((540, 1200), "37 C — NORMAL!", font=font(True, 46), fill=(126, 231, 135, 255), anchor="mm")
        for k in range(3):
            yy = 560 - ((t * 70 + k * 90) % 260)
            d.text((cx - 260 + k * 40, yy), "*", font=font(True, 60), fill=(126, 231, 135, 220), anchor="mm")
        label(d, cx, 1260, "Kapkapi = body ka heater!", ac, 42)

def dt_onion(d, A, bi, p, t):
    ac = (255, 209, 102)
    cx = A["cx"]
    if bi == 0:
        for k in range(4):
            r = 60 + k * 46
            d.ellipse([cx - 300 - r, 880 - r * 0.85, cx - 300 + r, 880 + r * 0.85], outline=(220, 160, 220, 255), width=10)
        ky = 640 + 90 * abs(math.sin(t * 4))
        d.polygon([(cx - 300, ky - 120), (cx - 210, ky - 120), (cx - 255, ky + 40)], fill=(190, 200, 220, 255))
        rr(d, [cx - 330, ky - 150, cx - 190, ky - 118], 14, fill=(120, 130, 150, 255))
        for k in range(4):
            d.line([(cx - 360, 940 + k * 70), (cx - 240, 940 + k * 70)], fill=(255, 255, 255, 90), width=5)
        for k in range(6):
            pp = (t * 0.7 + k * 0.17) % 1.0
            dot(d, cx - 300 + 60 * math.sin(t * 3 + k), 820 - pp * 380, 10, (255, 230, 150, 160))
        label(d, cx, 1250, "Kyunnn... aankhon mein kuch hai!", ac, 42)
    if bi == 1:
        d.ellipse([cx - 420, 760, cx + 120, 1120], fill=(250, 250, 250, 255))
        d.ellipse([cx - 160, 810, cx + 60, 1070], fill=(120, 80, 50, 255))
        d.ellipse([cx - 110, 860, cx + 10, 1020], fill=(20, 20, 30, 255))
        dot(d, cx - 70, 930, 34, (255, 255, 255, 255))
        lid = 0.5 + 0.5 * math.sin(t * 1.6)
        d.rectangle([cx - 420, 760, cx + 120, 760 + 40 * lid], fill=(230, 190, 160, 255))
        for k in range(6):
            pp = (p * 1.8 + k * 0.15) % 1.0
            xx = 940 - 380 * pp
            yy = 640 + 60 * math.sin(pp * 6 + k)
            if pp < 0.95:
                dot(d, xx, yy, 12, (255, 230, 150, 190))
                d.line([(xx, yy), (xx + 40, yy - 8)], fill=(255, 230, 150, 90), width=6)
        for k in range(3):
            yy = 1120 + ((t * 300 + k * 120) % 400)
            if yy < 1500:
                tear(d, cx - 170 + k * 40, yy, 16, (110, 200, 255, 230))
        label(d, cx, 1250, "Gas aankh mein = aansu!", ac, 42)
    if bi == 2:
        rr(d, [200, 680, 560, 1180], 40, fill=(210, 225, 240, 255), outline=(160, 180, 200, 255), width=6)
        d.line([(380, 680), (380, 1180)], fill=(180, 195, 215, 255), width=6)
        rr(d, [240, 1000, 330, 1120], 16, fill=(160, 180, 200, 255))
        rr(d, [600, 880, 900, 1160], 50, fill=(70, 130, 200, 255))
        sine(d, 610, 890, 900, 12, 200, t * 2, (150, 220, 255, 230), 7)
        for k in range(3):
            pp = (t * 0.5 + k * 0.3) % 1.0
            dot(d, 750 + 40 * math.sin(t + k), 860 - pp * 100, 7, (255, 255, 255, 150))
        label(d, cx, 1260, "Fridge/paani = 15-20 min mein aaram!", ac, 38)

def dt_limb(d, A, bi, p, t):
    ac = (126, 231, 135)
    cx = A["cx"]
    if bi == 0:
        rr(d, [120, 980, 960, 1070], 24, fill=(120, 90, 60, 255))
        rr(d, [120, 1070, 160, 1120], 12, fill=(100, 75, 50, 255))
        rr(d, [920, 1070, 960, 1120], 12, fill=(100, 75, 50, 255))
        rr(d, [200, 850, 780, 980], 38, fill=(70, 100, 170, 255))
        dot(d, 830, 916, 84, (242, 196, 155, 255))
        d.line([(812, 900), (818, 912)], fill=(60, 40, 30, 255), width=7)
        for k in range(3):
            z = 56 + k * 18 + 10 * math.sin(t * 2 + k)
            yy = 780 - ((t * 70 + k * 90) % 300)
            d.text((880 + k * 30, yy), "z", font=font(True, z), fill=(180, 220, 255, 200), anchor="mm")
        label(d, cx, 1230, "Sote waqt... haath dab gaya!", ac, 42)
    if bi == 1:
        rr(d, [140, 850, 940, 1060], 100, fill=(236, 186, 150, 255))
        pinch = 620
        d.line([(200, 950), (pinch, 950)], fill=(255, 90, 120, 240), width=12)
        d.line([(pinch + 70, 950), (880, 950)], fill=(120, 120, 140, 160), width=12)
        for k in range(3):
            pp = (t * 0.9 + k / 3.0) % 1.0
            xx = 200 + pp * (pinch - 200)
            dot(d, xx, 950, 11, (255, 255, 255, 220))
        d.polygon([(pinch + 4, 950 - 8), (pinch - 60, 950 - 60), (pinch - 60, 950 - 18)], fill=ac + (255,))
        d.polygon([(pinch + 4, 950 + 8), (pinch - 60, 950 + 60), (pinch - 60, 950 + 18)], fill=ac + (255,))
        d.polygon([(pinch + 66, 950 - 8), (pinch + 130, 950 - 60), (pinch + 130, 950 - 18)], fill=ac + (255,))
        d.polygon([(pinch + 66, 950 + 8), (pinch + 130, 950 + 60), (pinch + 130, 950 + 18)], fill=ac + (255,))
        label(d, cx, 1230, "Dabaav = nerve signals band!", ac, 42)
    if bi == 2:
        rr(d, [140, 850, 940, 1060], 100, fill=(236, 186, 150, 255))
        d.line([(200, 950), (880, 950)], fill=(255, 90, 120, 240), width=12)
        npx = 260 + (t * 260) % 640
        dot(d, npx, 950, 12, (255, 255, 255, 235))
        for k in range(8):
            a = (k * 45 + t * 160) % 360
            rr_ = 90 + 40 * math.sin(t * 5 + k)
            xx = 540 + rr_ * math.cos(math.radians(a)); yy = 950 + rr_ * math.sin(math.radians(a))
            dot(d, xx, yy, 8, ac + (200,))
        d.text((540, 1210), "JHAN-JHAN!", font=font(True, 54), fill=ac + (255,), anchor="mm")
        label(d, cx, 1300, "Hilane par signals wapas aate hain", ac, 40)

def dt_mirror(d, A, bi, p, t):
    ac = (127, 178, 255)
    cx = A["cx"]
    def fface(x, y, r, mole_left):
        dot(d, x, y, r, (242, 196, 155, 255))
        dot(d, x - r * 0.34, y - r * 0.22, r * 0.1, (60, 40, 30, 255))
        dot(d, x + r * 0.34, y - r * 0.22, r * 0.1, (60, 40, 30, 255))
        d.arc([x - r * 0.3, y + r * 0.1, x + r * 0.3, y + r * 0.55], 20, 160, fill=(120, 60, 50, 255), width=8)
        dot(d, x + (-r * 0.55 if mole_left else r * 0.55), y + r * 0.3, r * 0.09, (90, 60, 50, 255))
    if bi == 0 or bi == 1:
        rr(d, [140, 760, 500, 1240], 40, fill=(190, 220, 255, 200), outline=(240, 240, 250, 255), width=14)
        fface(320, 1000, 130, True)
        d.line([(170, 1160), (470, 800)], fill=(255, 255, 255, 70), width=40)
        nose = 1.0 if bi == 0 else 1.0 + 0.9 * seg(p, 0.1, 0.7)
        rr(d, [560, 760, 940, 1240], 24, fill=(250, 250, 250, 255), outline=(60, 70, 90, 255), width=8)
        fface(750, 1000, 130, False)
        d.polygon([(750, 950), (750, 970), (750 - 30 * nose, 1010)], fill=(214, 158, 120, 255))
        if bi == 1:
            dot(d, cx, 590, 90, (30, 36, 54, 255))
            dot(d, cx, 590, 62, (90, 120, 190, 255))
            dot(d, cx, 590, 30, (20, 24, 40, 255))
            for k in range(4):
                a = math.radians(35 + k * 30)
                d.line([(cx + 90 * math.cos(a), 590 + 90 * math.sin(a)), (740 * 1 + cx + 200 * math.cos(a), 590 + 200 * math.sin(a))], fill=ac + (110,), width=6)
            label(d, cx, 1300, "Camera lens = chehra badal jata hai", ac, 40)
        else:
            label(d, cx, 1300, "Aaina ULTA, camera SEEDHA!", ac, 42)
    if bi == 2:
        rr(d, [200, 760, 480, 1180], 36, fill=(190, 220, 255, 210), outline=(240, 240, 250, 255), width=12)
        fface(340, 950, 110, True)
        for k in range(2):
            s = 0.8 + 0.2 * math.sin(t * 3 + k)
            heart = (255, 120, 150, 230)
            hx, hy = 540 + k * 130, 820
            d.ellipse([hx - 26 * s, hy - 26 * s, hx, hy + 4 * s], fill=heart)
            d.ellipse([hx, hy - 26 * s, hx + 26 * s, hy + 4 * s], fill=heart)
            d.polygon([(hx - 26 * s, hy - 8 * s), (hx + 26 * s, hy - 8 * s), (hx, hy + 40 * s)], fill=heart)
        rr(d, [660, 900, 900, 1160], 20, fill=(250, 250, 250, 255), outline=(60, 70, 90, 255), width=6)
        fface(780, 1030, 80, False)
        d.text((780, 1220), "?", font=font(True, 64), fill=ac + (255,), anchor="mm")
        label(d, cx, 1320, "Roz aaine wala chehra hi 'apna' lagta hai", ac, 38)

def dt_glass(d, A, bi, p, t):
    ac = (139, 233, 253)
    cx = A["cx"]
    gx0, gx1, gy0, gy1 = cx - 150, cx + 150, 700, 1250
    if bi == 0 or bi == 1 or bi == 2:
        rr(d, [gx0, gy0, gx1, gy1], 30, fill=(200, 235, 250, 70), outline=(220, 240, 255, 220), width=8)
        d.rectangle([gx0 + 10, 860, gx1 - 10, gy1 - 8], fill=(120, 190, 235, 200))
        for k in range(2):
            icx = cx - 60 + k * 120
            icy = 900 + 30 * math.sin(t * 1.4 + k * 2)
            d.polygon([(icx - 46, icy - 46), (icx + 46, icy - 40), (icx + 42, icy + 46), (icx - 40, icy + 42)], fill=(230, 250, 255, 235))
        d.line([(cx + 90, 720), (cx + 60, 880)], fill=(255, 120, 120, 235), width=14)
    if bi == 0:
        spots = [(gx0 - 26, 800), (gx1 + 26, 860), (gx0 - 24, 980), (gx1 + 24, 1040), (gx0 - 26, 1140)]
        for k, (spx, spy) in enumerate(spots):
            q = seg(p, 0.08 * k, 0.08 * k + 0.25)
            if q > 0:
                dot(d, spx, spy, 14 * q, (150, 220, 255, int(235 * q)))
        label(d, cx, 560, "Boond... boond... boond?", ac, 44)
    if bi == 1:
        for k in range(10):
            ph = k / 10.0
            xx = cx + 520 * math.cos(ph * 6.28 + t * 0.6)
            yy = 980 + 420 * math.sin(ph * 6.28 + t * 0.6)
            tx = gx0 - 20 if xx < cx else gx1 + 20
            q = seg(p, 0.02 * k, 0.02 * k + 0.4)
            if q > 0:
                px = xx + (tx - xx) * q; py = yy + (1000 - yy) * q * 0.3
                dot(d, px, py, 9, (170, 230, 255, 200))
        gr = 16 + 26 * seg(p, 0.3, 0.75)
        slide = 60 * seg(p, 0.75, 1.0)
        dot(d, gx0 - 30, 890 + slide, gr, (150, 220, 255, 240))
        dot(d, gx1 + 30, 970 + slide, gr * 0.8, (150, 220, 255, 220))
        label(d, cx, 560, "Hawa ki nami jamti hai!", ac, 44)
    if bi == 2:
        d.arc([250, 640, 830, 1220], 90, 270, fill=(220, 240, 255, 255), width=16)
        for k in range(9):
            a = 90 + k * 22.5
            xx = 540 + 290 * math.cos(math.radians(a)); yy = 930 + 290 * math.sin(math.radians(a))
            dot(d, xx, yy, 6, (200, 230, 255, 230))
        na = 90 + 180 * seg(p, 0.05, 0.6)
        d.line([(540, 930), (540 + 240 * math.cos(math.radians(na)), 930 + 240 * math.sin(math.radians(na)))], fill=(255, 120, 120, 245), width=12)
        dot(d, 540, 930, 20, (255, 200, 90, 255))
        label(d, cx, 560, "Glass nahi rista — hawa mein nami hai!", ac, 38)

TOPICS = [
 dict(key="wrinkles", num=1, accent=(110, 225, 255), grad=((10, 26, 46), (6, 12, 30)), draw=dt_wrinkles,
      title="Paani se UNGLIYAN jhurridar kyun?",
      yt="Paani se Ungliyan Jhurridar Kyun Hoti Hain?",
      vo=["पानी में देर तक रहने पर उँगलियों पर झुर्रियाँ क्यों पड़ जाती हैं? ज़रा सोचो...",
          "ये सिर्फ़ त्वचा का सूखना नहीं है! हमारे शरीर की नसें, उँगलियों की रक्त-नलियों को सिकोड़ देती हैं — इससे उँगलियाँ झुर्रीदार हो जाती हैं। वैज्ञानिक मानते हैं, इससे गीली चीज़ें पकड़ने में मदद मिलती है।",
          "और सबसे मज़ेदार बात — जिनके हाथ की नसें ख़राब होती हैं, उनके पानी में रहने पर भी झुर्रियाँ नहीं पड़तीं! शरीर के ऐसे रहस्यों के लिए फ़ॉलो करो!"],
      cap=["Paani se ungliyan jhurridar?", "Nerves hain iske peeche!", "Nerve kharab = jhurriyan nahi!"]),
 dict(key="yawn", num=2, accent=(178, 141, 255), grad=((24, 16, 48), (10, 8, 26)), draw=dt_yawn,
      title="JAMHAI sankramak kyun hai?",
      yt="Jamhai Sankramak Kyun Hoti Hai?",
      vo=["किसी को जम्हाई लेते देखकर, हमें भी जम्हाई क्यों आने लगती है? सोचो...",
          "वैज्ञानिकों ने पाया — जम्हाई एक से दूसरे तक पहुँचती है! कई अध्ययन कहते हैं, ये sympathy की निशानी है — हम बिना जाने, सामने वाले की हालत अपना लेते हैं। कुछ वैज्ञानिक मानते हैं, जम्हाई दिमाग़ को ठंडा रखती है।",
          "और सबसे प्यारी बात — जम्हाई कुत्तों में भी फैलती है! वैज्ञानिकों ने देखा, कुत्ते अपने मालिक की जम्हाई देखकर जम्हाई ले लेते हैं। फ़ॉलो करो!"],
      cap=["Jamhai sankramak kyun?", "Sympathy + brain cooling", "Kutta bhi jamhai leta hai!"]),
 dict(key="goosebumps", num=3, accent=(255, 154, 213), grad=((44, 14, 38), (14, 8, 22)), draw=dt_goose,
      title="RONGTE khade kyun hote hain?",
      yt="Thand Mein Rongte Khade Kyun Hote Hain?",
      vo=["डर लगने या ठंड में शरीर पर रोंगटे खड़े क्यों हो जाते हैं? सोचो...",
          "हर बाल की जड़ में एक बहुत छोटी मसल होती है। ठंड या डर में वो सिकुड़ जाती है — और बाल सीधा खड़ा हो जाता है। जानवरों में इससे बाल फूले रहते हैं — गर्मी और बचाव के लिए!",
          "लेकिन इंसानों में ये अब बचा हुआ पुराना रिफ़्लेक्स है। और सुनो — जब कोई गाना या नज़ारा दिल को छू जाता है, तब भी रोंगटे खड़े होते हैं! फ़ॉलो करो!"],
      cap=["Rongte khade kyun hote?", "Chhoti muscle sikudti hai!", "Music se bhi rongte!"]),
 dict(key="teeth", num=4, accent=(255, 176, 102), grad=((40, 24, 10), (16, 10, 8)), draw=dt_teeth,
      title="Thand mein DAANT kyun bajte hain?",
      yt="Thand Mein Daant Kyun Bajte Hain?",
      vo=["ठंड में दाँत अपने आप क्यों बजने लगते हैं? सोचो...",
          "शरीर का थर्मामीटर कंपकंपी चालू कर देता है — मसलें बहुत तेज़ी से सिकुड़ती और खुलती हैं, और रगड़ से गर्मी बनती है। जबड़े की मसलें भी काँपती हैं — और दाँत बजने लगते हैं!",
          "यानी कपकंपी एक हीटर है — जो शरीर को गर्म रखने के लिए ख़ुद चल पड़ता है! ऐसे ही मज़ेदार facts के लिए फ़ॉलो करो!"],
      cap=["Thand mein daant bajte kyun?", "Muscles ka heater!", "Kapkapi = body ka heater"]),
 dict(key="onion", num=5, accent=(255, 209, 102), grad=((44, 36, 8), (18, 14, 8)), draw=dt_onion,
      title="PYAZ se aansu kyun aate hain?",
      yt="Pyaz Katne Par Aansu Kyun Aate Hain?",
      vo=["प्याज़ काटते ही आँखों से आँसू क्यों निकलने लगते हैं? सोचो...",
          "प्याज़ काटते समय उसके अंदर के रस मिलते हैं — और एक गैस बनती है। वो गैस हवा में उड़कर सीधे आँखों तक पहुँचती है। आँख को लगता है — कुछ चुभा है! और दिमाग़ तुरंत आँसू भेज देता है।",
          "तरकीब तो तुम जानते ही हो — काटने से पहले प्याज़ को ठंडे पानी में या फ़्रिज में रख लो, गैस कम बनेगी और आँसू भी कम! फ़ॉलो करो!"],
      cap=["Pyaz se aansu kyun?", "Gas aankh mein jaati hai", "Fridge/paani = aansu kam!"]),
 dict(key="limb", num=6, accent=(126, 231, 135), grad=((10, 36, 24), (6, 16, 12)), draw=dt_limb,
      title="Haath-pair 'so' kyun jate hain?",
      yt="Haath Ya Pair So Kyun Jata Hai?",
      vo=["बैठे-बैठे हाथ या पैर अचानक 'सो' क्यों जाता है? सोचो...",
          "लगातार दबाव पड़ने से हाथ की नसें दब जाती हैं। नसों का संदेश आना-जाना बंद — और हाथ सुन्न। जैसे ही दबाव हटता है, नसें अचानक जागती हैं — और झनझनाहट शुरू हो जाती है!",
          "ये शरीर का अलार्म है — मुझे आराम दो! इसलिए ज़्यादा देर एक ही अंदाज़ में मत बैठो। ऐसे ही शरीर के रहस्यों के लिए फ़ॉलो करो!"],
      cap=["Haath 'so' kyun jata hai?", "Dabaav = signals band", "Jhanjhanahat = nerves jagti hain"]),
 dict(key="mirror", num=7, accent=(127, 178, 255), grad=((16, 26, 50), (8, 12, 28)), draw=dt_mirror,
      title="Aaine vs photo: chehra alag kyun?",
      yt="Aaine Mein Chehra Normal, Photo Mein Alag Kyun?",
      vo=["आईने में अपना चेहरा सामान्य लगता है — पर फ़ोटो में अजीब क्यों? सोचो...",
          "आईना हमारा चेहरा उल्टा दिखाता है — और हम उसी उल्टे चेहरे को रोज़ देखते हैं। कैमरा चेहरा सीधा दिखाता है, और कैमरे का लेंस चेहरे की शक्ल थोड़ी बदल भी देता है — जैसे नाक बड़ी लगना।",
          "मतलब फ़ोटो में तुम 'असली' लगते हो — और आईने का उल्टा चेहरा तुम्हें ज़्यादा जाना-पहचाना लगता है! मज़ेदार ना? फ़ॉलो करो!"],
      cap=["Aaina ulta, camera seedha", "Lens chehra badal deta hai", "Aaine wala chehra hi 'apna'"]),
 dict(key="glass", num=8, accent=(139, 233, 253), grad=((8, 34, 44), (6, 14, 22)), draw=dt_glass,
      title="Glass par boondein kahan se aati hain?",
      yt="Thande Glass Ke Bahar Paani Ki Boondein Kahan Se Aati Hain?",
      vo=["ठंडे गिलास के बाहर पानी की बूँदें कहाँ से आती हैं? सोचो...",
          "हवा में हमेशा पानी की भाप छिपी रहती है। ठंडा गिलास छूते ही वो भाप ठंडी होती है — और छोटी-छोटी बूँदों में बदल जाती है। ये बूँदें हवा से आती हैं, गिलास से पानी नहीं रिसता!",
          "इसीलिए गर्मियों में बाहर से आई ठंडी बोतल के बाहर भी बूँदें दिखती हैं — घर की हवा में उमस ज़्यादा होती है! फ़ॉलो करो!"],
      cap=["Glass par boondein kahan se?", "Hawa ki nami jamti hai", "Glass se paani nahi rista!"]),
]

# ---------------- FRAME ENGINE ----------------
def make_frame(topic, idx):
    ac = topic["accent"]
    grad = make_grad(*topic["grad"])
    rnd = np.random.RandomState(11 + idx)
    blobs = []
    for _ in range(12):
        r = int(rnd.randint(120, 320))
        blobs.append(dict(x=rnd.randint(0, W), y=rnd.randint(0, H), r=r,
                          sx=rnd.uniform(8, 30), sy=rnd.uniform(10, 44), ph=rnd.uniform(0, 6.28)))
    sprites = [soft_sprite(b["r"], ac, 46) for b in blobs]
    A = dict(x0=60, y0=370, x1=1020, y1=1580, cx=540, cy=970)
    draw_t = topic["draw"]

    def frame(bi, p, t):
        img = grad.copy()
        for b, sp in zip(blobs, sprites):
            x = (b["x"] + t * b["sx"]) % (W + 2 * b["r"]) - b["r"]
            y = (b["y"] - t * b["sy"]) % (H + 2 * b["r"]) - b["r"]
            img.paste(sp, (int(x), int(y)), sp)
        d = ImageDraw.Draw(img, "RGBA")
        tp = (bi + p) / 3.0
        d.rectangle([0, 0, int(W * tp), 12], fill=(255, 209, 102, 255))
        tf = font(True, 46)
        tlines = wrap(d, topic["title"], tf, 880, 1)
        d.text((W // 2, 222), tlines[0], font=tf, fill=(255, 255, 255, 255), anchor="mm")
        f = font(True, 44)
        txt = "BODY SCIENCE"
        tw = d.textlength(txt, font=f)
        rr(d, [W // 2 - tw / 2 - 56, 74, W // 2 + tw / 2 + 56, 168], 47, fill=ac + (255,))
        d.text((W // 2, 121), txt, font=f, fill=(12, 14, 24, 255), anchor="mm")
        f2 = font(True, 36)
        rr(d, [W - 168, 82, W - 64, 160], 39, fill=(0, 0, 0, 150), outline=ac + (220,), width=3)
        d.text((W - 116, 121), f"{topic['num']}/8", font=f2, fill=ac + (255,), anchor="mm")
        d.rectangle([60, 300, 1020, 300], fill=(0, 0, 0, 0))
        rr(d, [60, 296, 1020, 306], 5, outline=(255, 255, 255, 70), width=2)
        rr(d, [62, 298, 62 + int((956) * tp), 304], 3, fill=ac + (230,))
        rr(d, [60, A["y0"], A["x1"], A["y1"]], 44, fill=(9, 13, 26, 185), outline=ac + (80,), width=3)
        draw_t(d, A, bi, p, t)
        if bi == 2 and p > 0.55:
            q = seg(p, 0.55, 0.8)
            rr(d, [170, 1400, 910, 1520], 60, fill=(255, 190, 40, int(255 * q)))
            d.text((540, 1460), "FOLLOW KARO - ROZ NAYI VIDEO!", font=font(True, 40),
                   fill=(18, 18, 28, int(255 * q)), anchor="mm")
        if p < 0.10:
            wfrac = 1 - p / 0.10
            d.rectangle([60, A["y0"], 60 + 960 * wfrac, A["y1"]], fill=(6, 8, 16, int(220 * wfrac)))
        cf = font(True, 40)
        clines = wrap(d, topic["cap"][bi], cf, 880, 2)
        bandh = 60 + len(clines) * 54
        rr(d, [40, 1832 - bandh, 1040, 1836], 30, fill=(0, 0, 0, 190))
        yy = 1836 - bandh + (bandh - len(clines) * 54) // 2 + 8
        for ln in clines:
            d.text((W // 2, yy), ln, font=cf, fill=(255, 255, 255, 255), anchor="ma")
            yy += 54
        return img
    return frame

# ---------------- AUDIO ----------------
async def _tts(text, out):
    import edge_tts
    await edge_tts.Communicate(text, "hi-IN-MadhurNeural", rate="-4%").save(out)

def synth(text, name):
    out = os.path.join(TMP, name)
    try:
        asyncio.run(_tts(text, out))
        if os.path.getsize(out) < 3000:
            raise RuntimeError("tiny")
    except Exception as e:
        print("edge-tts fail, gTTS fallback:", e)
        from gtts import gTTS
        gTTS(text=text, lang="hi", slow=False).save(out)
    return out

def dur(path):
    try:
        if FP:
            out = subprocess.run([FP, "-v", "error", "-show_entries", "format=duration",
                                  "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
            if out:
                return float(out)
    except Exception:
        pass
    try:
        import re
        err = subprocess.run([FF, "-i", path], capture_output=True, text=True).stderr
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", err)
        if m:
            return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    except Exception:
        pass
    return 5.0

# ---------------- MAIN ----------------
def main():
    args = sys.argv[1:]
    idx = None
    if "--index" in args:
        idx = int(args[args.index("--index") + 1])
    if idx is None:
        env = os.environ.get("SHORT_INDEX", "").strip()
        base = int(env) if env.isdigit() else datetime.date.today().toordinal()
        shift = int(os.environ.get("SHORT_SHIFT", "0") or 0)
        idx = (base + shift) % len(TOPICS)
    idx = idx % len(TOPICS)
    topic = TOPICS[idx]
    print(f"BODY SCIENCE index={idx} key={topic['key']} | {topic['title']}")

    if "--stills" in args:
        frame = make_frame(topic, idx)
        for bi in range(3):
            for tag, pp in [("a", 0.4), ("b", 0.8)]:
                frame(bi, pp, bi * 5 + pp * 4).save(f"{TMP}/still_{idx}_{bi}{tag}.png")
        print("STILLS DONE ->", TMP)
        return

    clips = [synth(t, f"{topic['key']}_{i}.mp3") for i, t in enumerate(topic["vo"])]
    durs = [dur(c) for c in clips]
    print("voice durations:", [round(x, 1) for x in durs])
    frame = make_frame(topic, idx)
    aud = os.path.join(TMP, "a.m4a"); lst = os.path.join(TMP, "list.txt")
    with open(lst, "w") as fh:
        for c in clips:
            fh.write(f"file '{c}'\n")
    subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-af", "apad=pad_dur=2", "-c:a", "aac", "-b:a", "160k", aud], check=True)
    out = os.path.join(BASE, "output", f"body_science_{idx:02d}_{topic['key']}.mp4")
    cmd = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", aud, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", os.path.join(TMP, "v.mp4")]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    fi = 0
    for bi, ds in enumerate(durs):
        nf = int((ds + 0.35) * FPS)
        for k in range(nf):
            proc.stdin.write(np.asarray(frame(bi, k / max(1, nf - 1), fi / FPS), dtype=np.uint8).tobytes())
            fi += 1
        if bi == 1:
            frame(bi, 0.6, 0).save(os.path.join(TMP, "thumb.jpg"), quality=88)
    proc.stdin.close(); proc.wait()
    shutil.move(os.path.join(TMP, "v.mp4"), out)
    print("VIDEO:", out, f"{os.path.getsize(out)/1e6:.1f} MB", f"{dur(out):.1f}s")

    if "--upload" in args:
        sys.path.insert(0, BASE)
        from youtube_uploader import upload_to_youtube
        plan = {"title": f"{topic['yt']} | Body Science #shorts",
                "description": f"{topic['title']}\n\n{topic['cap'][1]}\n{topic['cap'][2]}\n\nRoz nayi Body Science video — follow karo!\n#shorts #bodyscience #sciencefacts #hindi",
                "tags": ["body science hindi", "science facts hindi", "kyun hota hai", "human body facts", "shorts"]}
        vid = upload_to_youtube(out, os.path.join(TMP, "thumb.jpg"), plan, "shorts")
        print("YOUTUBE_VIDEO_ID:", vid)
        print("YOUTUBE_URL: https://youtube.com/watch?v=" + str(vid))

if __name__ == "__main__":
    main()
