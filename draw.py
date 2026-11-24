#!/usr/bin/env python3
"""news-23 b28 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
31 stories. 1024x1024. PIL only in this file (main.py is stdlib-only)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

DJ = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DJB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DJS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def f(size, bold=False, serif=False):
    path = DJS if serif else (DJB if bold else DJ)
    return ImageFont.truetype(path, size)

# palette
INK = (17, 17, 17)
PAPER = (250, 248, 240)
RED = (178, 24, 24)
GOLD = (212, 160, 32)
TEAL = (0, 122, 110)
NAVY = (16, 42, 90)
GREY = (110, 110, 110)
LGREY = (228, 226, 218)
DBLUE = (8, 24, 64)
GREEN = (110, 160, 60)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text(x, y, s, font, fill=INK, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

def wrap(s, font, maxw):
    words = s.split()
    lines, cur = [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def chip(x, y, label, color):
    """small pill, right-aligned at x; returns left edge."""
    fw = d.textlength(label, font=f(8, True)) + 10
    x0 = x - fw
    d.rounded_rectangle([x0, y, x, y + 13], radius=6, fill=color)
    d.text((x0 + 5, y + 2), label, font=f(8, True), fill=(255, 255, 255))
    return x0

# ---------------- masthead ----------------
d.rectangle([0, 0, W, 54], fill=INK)
text(12, 8, "THE WORLD TODAY", f(34, serif=True), fill=(255, 255, 255))
text(W - 12, 16, "MONDAY  23 NOVEMBER 2026", f(17, True), fill=GOLD, anchor="ra")

# ---------------- kicker ----------------
text(12, 58, "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
     f(12, True), fill=RED)

# ---------------- number strip (2 rows x 5 cols) ----------------
nums = [
    ("-3.3%", RED, "KOSPI"),
    ("5.3", NAVY, "US-CHINA POWER GAP"),
    ("11,762", (120, 90, 0), "EBOLA CASES, DRC"),
    ("10T won", (140, 100, 0), "SEOUL STABILISATION FUND"),
    ("2%", (150, 0, 130), "BILLIONAIRE TAX IN PARIS"),
    ("$450M", (150, 0, 130), "SKUBAL DEAL"),
    ("165", RED, "RUSSIAN MISSILES IN A WEEK"),
    ("12,000", (0, 90, 180), "CLEARED IN MANCHESTER"),
    ("264 kg", (140, 100, 0), "EXPLOSIVES SEIZED IN LEBANON"),
    ("$107.3B", (150, 0, 130), "ANTHROPIC IPO — LARGEST EVER"),
]
colw = (W - 24) // 5
for i, (num, col, lab) in enumerate(nums):
    cx = 12 + (i % 5) * colw
    cy = 74 if i < 5 else 108
    text(cx, cy, num, f(21, True), fill=col)
    text(cx, cy + 23, lab, f(8, True), fill=INK)
d.line([12, 140, W - 12, 140], fill=INK, width=2)

# ---------------- region bar ----------------
regs = [("ASIA-PACIFIC 7", 7, TEAL), ("AMERICAS 8", 8, NAVY), ("MIDDLE EAST 6", 6, (150, 110, 30)),
        ("EUROPE 5", 5, (110, 60, 160)), ("AFRICA 3", 3, (160, 40, 40)), ("WORLD 2", 2, GREY)]
rx = 12
tot = 31
for name, n, col in regs:
    wseg = int((W - 24) * n / tot)
    d.rectangle([rx, 144, rx + wseg - 1, 158], fill=col)
    text(rx + 4, 147, name, f(9, True), fill=(255, 255, 255))
    rx += wseg

# ---------------- UTC strip ----------------
d.rectangle([0, 162, W, 178], fill=DBLUE)
text(12, 166, "THE DAY IN UTC", f(10, True), fill=GOLD)
text(120, 166, "~00:00 Kospi dives  ·  ~06:30 Guterres opens  ·  ~09:00 Power Index  ·  ~12:00 Paris 2% tax  ·  ~15:00 Kyiv missiles  ·  ~18:00 Anthropic $97.17",
     f(10), fill=(255, 255, 255))
text(W - 12, 166, "~ APPROX", f(10), fill=(200, 200, 200), anchor="ra")

# ---------------- heroes ----------------
HX = [12, 348, 684]
HW = 328
HY = 182
# hero 1: Kospi skyline + chart
x0 = HX[0]
d.rectangle([x0, HY, x0 + HW, HY + 118], fill=DBLUE)
# skyline
import random
random.seed(23)
bx = x0 + 8
while bx < x0 + HW - 20:
    bw = random.randint(16, 30)
    bh = random.randint(28, 78)
    by = HY + 118 - bh
    d.rectangle([bx, by, bx + bw, HY + 118], fill=(24, 48, 96))
    for wy in range(by + 6, HY + 112, 12):
        for wx in range(bx + 4, bx + bw - 3, 9):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 210, 90))
    bx += bw + 4
# chart line, kept below the -3.3% text (text occupies y HY+6..HY+30)
pts = []
for i in range(9):
    px = x0 + 30 + i * 34
    py = HY + 52 + i * 6 + (4 if i % 2 else 0)
    pts.append((px, py))
d.line(pts, fill=(255, 80, 60), width=3)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 200, 60))
text(x0 + 10, HY + 6, "-3.3%", f(26, True), fill=(255, 80, 60))
# black label bar
d.rectangle([x0, HY + 118, x0 + HW, HY + 136], fill=INK)
text(x0 + 8, HY + 122, "KOSPI  4,708.54   ·   -161 PTS", f(11, True), fill=(255, 255, 255))
# headline / body / source
text(x0, HY + 142, "1", f(15, True), fill=(255, 255, 255))
d.ellipse([x0, HY + 142, x0 + 18, HY + 160], fill=RED)
text(x0 + 9, HY + 143, "1", f(11, True), fill=(255, 255, 255), anchor="mm")
hl = wrap("AI ROUT HITS ASIA", f(17, True), HW - 26)
yy = HY + 142
for ln in hl:
    text(x0 + 24, yy, ln, f(17, True))
    yy += 20
body = wrap("Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
            f(11), HW - 4)
yy += 2
for ln in body[:2]:
    text(x0, yy, ln, f(11))
    yy += 14
text(x0, yy + 2, "KOREA EXCHANGE", f(9), fill=GREY)
chip(x0 + HW, yy + 1, "REPORTED", NAVY)

# hero 2: Guterres teal panel
x0 = HX[1]
d.rectangle([x0, HY, x0 + HW, HY + 118], fill=(0, 128, 118))
# globe, small, far right, clear of text (text max width HW-70)
gx, gy, gr = x0 + HW - 34, HY + 88, 17
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(170, 220, 200))
d.ellipse([gx - 8, gy - 6, gx + 2, gy + 4], fill=(90, 170, 120))
d.ellipse([gx - 2, gy + 4, gx + 10, gy + 12], fill=(90, 170, 120))
# flags row along bottom of scene, above black bar
for i, fc in enumerate([(200, 40, 40), (40, 90, 200), (240, 200, 40), (40, 160, 90), (220, 120, 40)]):
    fx = x0 + 14 + i * 26
    d.polygon([(fx, HY + 96), (fx + 18, HY + 101), (fx, HY + 106)], fill=fc)
h2 = ["150 DELEGATES", "BACK A RISK", "FRAMEWORK"]
yy = HY + 8
for ln in h2:
    text(x0 + 10, yy, ln, f(24, True), fill=(255, 230, 60) if yy == HY + 8 else (255, 255, 255))
    yy += 27
d.rectangle([x0, HY + 118, x0 + HW, HY + 136], fill=INK)
text(x0 + 8, HY + 122, "UN  ·  BRIDGETOWN", f(11, True), fill=(255, 255, 255))
text(x0, HY + 142, "2", f(15, True), fill=(255, 255, 255))
d.ellipse([x0, HY + 142, x0 + 18, HY + 160], fill=RED)
text(x0 + 9, HY + 143, "2", f(11, True), fill=(255, 255, 255), anchor="mm")
hl = wrap("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE", f(17, True), HW - 26)
yy = HY + 142
for ln in hl:
    text(x0 + 24, yy, ln, f(17, True))
    yy += 20
body = wrap("UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
            f(11), HW - 4)
yy += 2
for ln in body[:2]:
    text(x0, yy, ln, f(11))
    yy += 14
text(x0, yy + 2, "UNITED NATIONS", f(9), fill=GREY)
chip(x0 + HW, yy + 1, "REPORTED", NAVY)

# hero 3: Asia Power Index bars
x0 = HX[2]
d.rectangle([x0, HY, x0 + HW, HY + 118], fill=(245, 242, 232))
text(x0 + 8, HY + 6, "NARROWEST SINCE 2018", f(11, True))
text(x0 + HW - 8, HY + 6, "GAP 5.3", f(11, True), fill=(150, 110, 0), anchor="ra")
bars = [("78.9", 78.9, NAVY, "US"), ("73.6", 73.6, RED, "CHINA"), ("40.5", 40.5, GOLD, "INDIA")]
base = HY + 100
for i, (val, v, col, lab) in enumerate(bars):
    bx0 = x0 + 22 + i * 104
    bh = int(v * 0.62)
    d.rectangle([bx0, base - bh, bx0 + 56, base], fill=col)
    text(bx0 + 28, base - bh - 16, val, f(12, True), anchor="ma")
    text(bx0 + 28, base + 4, lab, f(10, True), anchor="ma")
# NOTE: labels sit just above black bar (base+4 = HY+110, bar ends HY+118) - ok
d.rectangle([x0, HY + 118, x0 + HW, HY + 136], fill=INK)
text(x0 + 8, HY + 122, "ASIA POWER INDEX 2026", f(11, True), fill=(255, 255, 255))
text(x0, HY + 142, "3", f(15, True), fill=(255, 255, 255))
d.ellipse([x0, HY + 142, x0 + 18, HY + 160], fill=RED)
text(x0 + 9, HY + 143, "3", f(11, True), fill=(255, 255, 255), anchor="mm")
hl = wrap("US LEAD OVER CHINA AT RECORD LOW", f(17, True), HW - 26)
yy = HY + 142
for ln in hl:
    text(x0 + 24, yy, ln, f(17, True))
    yy += 20
body = wrap("Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
            f(11), HW - 4)
yy += 2
for ln in body[:2]:
    text(x0, yy, ln, f(11))
    yy += 14
text(x0, yy + 2, "LOWY INSTITUTE", f(9), fill=GREY)
chip(x0 + HW, yy + 1, "REPORTED", NAVY)

# ---------------- MORE OF THE DAY ----------------
MY = 404
text(12, MY, "MORE OF THE DAY  —  10 STORIES", f(14, True))
d.line([12, MY + 20, W - 12, MY + 20], fill=INK, width=2)

cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED", NAVY),
    ("FBI", (110, 60, 160), "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED", NAVY),
    ("WHITE HOUSE", (150, 110, 30), "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED", NAVY),
    ("MARKETS", TEAL, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED", NAVY),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED", NAVY),
    ("SPORT", TEAL, "TOM JACKSON DIES AT 75", "Broncos LB turned ESPN voice.", "ESPN", "REPORTED", NAVY),
    ("LEGAL", (110, 60, 160), "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED", NAVY),
    ("TECH", (0, 90, 180), "ANTHROPIC IPO: $107.3B", "Raised at $83, closes $97.17.", "WSJ", "REPORTED", NAVY),
    ("EUROPE", RED, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Three Kh-101s crossed airspace.", "AP", "CLAIM", RED),
    ("SPACE", GREY, "RUSSIAN NUCLEAR SATELLITE", "Intel: built to carry a nuke.", "Reuters", "CLAIM", RED),
]
cw = (W - 24 - 4 * 5) // 5
ch = 80
for i, (cat, ccol, head, body, src, chp, chcol) in enumerate(cards):
    cx = 12 + (i % 5) * (cw + 5)
    cy = 428 + (i // 5) * (ch + 6)
    d.rectangle([cx, cy, cx + cw, cy + ch], outline=(180, 178, 170), width=1)
    d.rectangle([cx, cy, cx + cw, cy + 15], fill=ccol)
    text(cx + 5, cy + 2, cat, f(9, True), fill=(255, 255, 255))
    text(cx + cw - 5, cy + 2, str(i + 4), f(9, True), fill=(255, 255, 255), anchor="ra")
    hl = wrap(head, f(11, True), cw - 10)
    yy = cy + 19
    for ln in hl[:2]:
        text(cx + 5, yy, ln, f(11, True))
        yy += 13
    text(cx + 5, cy + 48, body, f(9))
    text(cx + 5, cy + 65, src, f(9), fill=GREY)
    chip(cx + cw - 4, cy + 64, chp, chcol)

# ---------------- map + ALSO ----------------
AY = 596
text(12, AY, "WHERE IT HAPPENED", f(14, True))
text(440, AY, "ALSO ON MONDAY", f(14, True))
d.line([12, AY + 20, W - 12, AY + 20], fill=INK, width=2)
mapx, mapy, mapw, maph = 12, 620, 412, 190
d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=(205, 225, 245))
for gx in range(mapx, mapx + mapw, 16):
    d.line([gx, mapy, gx, mapy + maph], fill=(185, 208, 235), width=1)
for gy in range(mapy, mapy + maph, 16):
    d.line([mapx, gy, mapx + mapw, gy], fill=(185, 208, 235), width=1)
# simplified continents
d.polygon([(mapx + 18, mapy + 30), (mapx + 120, mapy + 18), (mapx + 150, mapy + 55), (mapx + 110, mapy + 95),
           (mapx + 60, mapy + 110), (mapx + 22, mapy + 80)], fill=GREEN)  # N America
d.polygon([(mapx + 95, mapy + 118), (mapx + 130, mapy + 122), (mapx + 128, mapy + 168), (mapx + 100, mapy + 178),
           (mapx + 88, mapy + 150)], fill=GREEN)  # S America
d.polygon([(mapx + 185, mapy + 28), (mapx + 250, mapy + 20), (mapx + 262, mapy + 62), (mapx + 225, mapy + 92),
           (mapx + 195, mapy + 70)], fill=GREEN)  # Europe
d.polygon([(mapx + 255, mapy + 78), (mapx + 300, mapy + 72), (mapx + 312, mapy + 120), (mapx + 280, mapy + 150),
           (mapx + 258, mapy + 118)], fill=GREEN)  # Africa
d.polygon([(mapx + 300, mapy + 25), (mapx + 395, mapy + 18), (mapx + 405, mapy + 70), (mapx + 360, mapy + 105),
           (mapx + 315, mapy + 80)], fill=GREEN)  # Asia
d.polygon([(mapx + 345, mapy + 150), (mapx + 385, mapy + 148), (mapx + 388, mapy + 172), (mapx + 352, mapy + 176)],
          fill=GREEN)  # Oceania
pins = {1: (348, 668), 2: (128, 756), 3: (378, 648), 4: (78, 668), 5: (102, 682), 6: (262, 668),
        7: (62, 652), 8: (38, 668), 9: (72, 700), 10: (88, 706), 11: (228, 648), 12: (244, 656), 13: (262, 640)}
for n, (px, py) in pins.items():
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
    d.text((px, py - 1), str(n), font=f(8, True), fill=(255, 255, 255), anchor="mm")

also = [
    "14. Paris: 100+ back 2% billionaire tax", "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week", "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe", "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike", "21. West Bank settler attacks",
    "22. Iran war: no deal in sight", "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt", "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams", "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row", "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules", "31. Seoul readies 10T-won fund",
]
for i, a in enumerate(also):
    ax = 440 if i < 9 else 732
    ay = 624 + (i % 9) * 20
    text(ax, ay, a, f(11))

# pin legend (2 lines)
leg1 = "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing · 4 Washington · 5 New York · 6 Tehran · 7 Chicago · 8 San Francisco"
leg2 = "9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow"
text(12, 816, leg1, f(10), fill=GREY)
text(12, 832, leg2, f(10), fill=GREY)

# ---------------- DATE CHECK ----------------
DY = 852
d.rectangle([12, DY, W - 12, DY + 66], outline=RED, width=2)
text(20, DY + 5, "DATE CHECK", f(13, True), fill=RED)
text(W - 20, DY + 5, "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", f(9, True), anchor="ra")
text(20, DY + 24, "LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) ·",
     f(10))
text(20, DY + 38, "EU-Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)", f(10))
text(20, DY + 52, "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
     f(10))

# ---------------- footer ----------------
text(12, 928, "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).",
     f(10), fill=GREY)
text(12, 942, "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing",
     f(10), fill=GREY)
d.rectangle([0, 962, W, 1024], fill=INK)
text(W // 2, 984, "Scenes are drawn illustrations, not photographs.  ·  THE WORLD TODAY — Monday 23 November 2026  ·  31 stories  ·  6 regions",
     f(11, True), fill=GOLD, anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
