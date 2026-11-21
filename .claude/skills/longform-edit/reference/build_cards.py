#!/usr/bin/env python3
"""REV1 J2 fact cards (item 5, the "or some kind of graphic" half of Dan's rule).

Placed viewer-LEFT, clear of the lower-third chips: the card occupies
x 50..550, y 175..800 and every chip's eyebrow bar starts at y=796, so a card
and a chip can share the screen without colliding (longform-edit Step 7).
Constants are the J2 set, verbatim - BG, OLIVE, Impact, Copperplate, Manrope.
Camel-case names use Manrope: Copperplate is a SMALL-CAPS face and renders
"AbsByAI.com" as "ABSBYAI.COM", which breaks the J2 camel-case rule.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

B = Path("/Volumes/Extreme/_edit_work/spraytan")
OUT = B / "gfx"; OUT.mkdir(exist_ok=True)
APP = Path("/Users/danielrose/Documents/Claude/Projects/Abs By AI/app-store-assets/6.9-inch")
W, H = 1920, 1080
BG = (13, 14, 11); OLIVE = (140, 152, 88); WHITE = (255, 255, 255)
IMPACT = '/System/Library/Fonts/Supplemental/Impact.ttf'
COPPER = '/System/Library/Fonts/Supplemental/Copperplate.ttc'
MANROPE = '/Users/danielrose/Library/Fonts/Manrope.ttf'
X, Y, CW = 44, 168, 566

def spaced(d, xy, text, font, fill, gap=4):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill); x += font.getlength(ch) + gap
    return x - gap - xy[0]

def wrap(text, font, maxw, draw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw or not cur: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def appcard(key, eyebrow, title, bullets, img):
    """Full-frame outro card: phone screenshot left, copy right. Used only after
    18:02, where the CTA chip has already cleared, so nothing to collide with."""
    im = Image.new('RGBA', (W, H), BG + (252,)); d = ImageDraw.Draw(im)
    ph = Image.open(APP / img).convert("RGB")
    ph.thumbnail((520, 940), Image.LANCZOS)
    px, py = 210, (H - ph.height) // 2
    im.paste(ph, (px, py))
    d.rectangle([px - 4, py - 4, px + ph.width + 3, py + ph.height + 3], outline=OLIVE + (255,), width=4)
    tx = px + ph.width + 130
    f_eye = ImageFont.truetype(COPPER, 28)
    ew = spaced(d, (tx, 300), eyebrow, f_eye, OLIVE + (255,), 5)
    d.rectangle([tx, 348, tx + int(ew), 354], fill=OLIVE + (255,))
    f_ttl = ImageFont.truetype(IMPACT, 84)
    yy = 392
    for ln in wrap(title, f_ttl, W - tx - 120, d):
        d.text((tx, yy), ln, font=f_ttl, fill=WHITE + (255,)); yy += 92
    f_b = ImageFont.truetype(MANROPE, 30)
    yy += 26
    for b in bullets:
        for ln in wrap(b, f_b, W - tx - 140, d):
            d.rectangle([tx, yy + 13, tx + 11, yy + 24], fill=OLIVE + (255,))
            d.text((tx + 32, yy), ln, font=f_b, fill=(235, 238, 226, 255)); yy += 44
    p = OUT / f"card_{key}.png"; im.save(p)
    return p

def card(key, eyebrow, title, bullets=(), img=None, manrope_title=False):
    if img: return appcard(key, eyebrow, title, bullets, img)
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f_eye = ImageFont.truetype(COPPER, 24)
    ew = sum(f_eye.getlength(c) + 4 for c in eyebrow)
    d.rectangle([X, Y, X + int(ew) + 30, Y + 37], fill=BG + (228,))
    spaced(d, (X + 14, Y + 6), eyebrow, f_eye, OLIVE + (255,), 4)

    top = Y + 47
    pad = 26
    size = 62 if not manrope_title else 52
    while size > 26:
        f_ttl = ImageFont.truetype(MANROPE if manrope_title else IMPACT, size)
        tl = wrap(title, f_ttl, CW - pad * 2, d)
        if len(tl) <= 2: break
        size -= 3
    f_ttl = ImageFont.truetype(MANROPE if manrope_title else IMPACT, size)
    tl = wrap(title, f_ttl, CW - pad * 2, d)

    f_b = ImageFont.truetype(MANROPE, 25)
    blines = []
    for b in bullets: blines += wrap(b, f_b, CW - pad * 2 - 26, d)

    imgh = 0
    if img:
        ph = Image.open(APP / img).convert("RGB")
        ph.thumbnail((CW - pad * 2, 300), Image.LANCZOS)
        imgh = ph.height + 18

    boxh = pad + len(tl) * (size + 6) + (16 + len(blines) * 35 if blines else 0) + imgh + pad
    d.rectangle([X, top, X + CW, top + boxh], fill=BG + (240,), outline=OLIVE + (255,), width=3)
    yy = top + pad - (6 if not manrope_title else 0)
    for ln in tl:
        d.text((X + pad, yy), ln, font=f_ttl, fill=WHITE + (255,)); yy += size + 6
    if blines:
        yy += 16
        for ln in blines:
            d.rectangle([X + pad, yy + 11, X + pad + 9, yy + 20], fill=OLIVE + (255,))
            d.text((X + pad + 26, yy), ln, font=f_b, fill=(235, 238, 226, 255)); yy += 35
    if img:
        yy += 4
        px = X + (CW - ph.width) // 2
        im.paste(ph, (px, yy))
        d.rectangle([px - 2, yy - 2, px + ph.width + 1, yy + ph.height + 1], outline=OLIVE + (255,), width=2)
    p = OUT / f"card_{key}.png"; im.save(p)
    assert top + boxh < 790, f"{key}: card bottom {top+boxh} collides with the chip band at 796"
    return p

CARDS = [
 ("askai", "HOW TO FIND A STUDIO", "ASK YOUR AI",
  ["Claude, ChatGPT or Gemini", "“Find me the 3 best spray tan", "studios near me”", "Read the reviews it pulls"]),
 ("cost", "WHAT I PAID", "$100 ALL IN",
  ["$80   base spray tan", "$20   contouring (ab shadowing)", "~$50 if you skip the contouring"]),
 ("briefs", "BEFORE YOU GO", "WEAR BRIEFS",
  ["Boxers leave an untanned band", "all the way down your thigh", "A thong leaves even less line",
   "Wear a pair you can destroy"]),
 ("rededicate", "THE HIDDEN UPSIDE", "YOU'LL TRAIN HARDER",
  ["You stand there, near naked,", "being assessed — every time"]),
 ("drying", "DRYING TIME", "8 HOURS",
  ["Rapid dry tan     8 hours", "Standard tan       24 hours", "Rapid = you never sleep in it",
   "Longevity is about the same"]),
 ("firstshower", "THE FIRST SHOWER", "RINSE ONLY",
  ["No soap", "No washcloth", "No scrubbing, no exfoliating", "Brown water is normal"]),
 ("ongoing", "AFTER THAT FIRST SHOWER", "STAY GENTLE",
  ["No washcloths for the week", "No exfoliating face scrubs", "No glycolic or salicylic acid",
   "Minimum scrubbing, gentle soap"]),
 ("bryan", "THE WORLD'S HEALTHIEST MAN", "BRYAN JOHNSON",
  ["Goes out off-peak only", "Carries an umbrella in the sun", "Looks like an ultra-pale vampire",
   "— on purpose"]),
 ("cancer", "WHY DAN STOPPED SUN TANNING", "SUN = DAMAGE",
  ["Skin cancer is one of the", "most common cancers", "Sun damage visibly ages you",
   "A spray tan does neither"]),
 ("subtle", "IF YOU'RE VERY PALE", "GO SUBTLE",
  ["A little darker than you are now", "Not full bronze", "It also lasts noticeably longer"]),
 ("darkonpale", "HOW LONG IT LASTS", "3–4 DAYS",
  ["Dark tan on very white skin", "~7 days if you go subtle", "Every patch that wears off shows"]),
 ("order", "SPEND IN THIS ORDER", "TAN GOES LAST",
  ["1    Gym membership or home gym", "2    Meal prep / your food", "3    Then the spray tan"]),
 ("orange", "THE ORANGE PROBLEM", "CHEAP LOOKS FAKE",
  ["Home kits and cheap studios", "run orange and uneven", "Premium looks genuinely natural"]),
 ("whofor", "WHO IT'S FOR", "IT DEPENDS",
  ["Rich, ripped, on camera      yes", "Broke, not in shape yet      no", "Everyone else      sometimes"]),
 ("step1", "STEP ONE", "UPLOAD ONE PHOTO",
  ["One shirtless picture", "The AI generates YOU with the", "physique you're working toward"], "01-the-reveal.png"),
 ("realyou", "NOT A HEAD ON A STOCK BODY", "THE REAL YOU",
  ["Your face", "Your frame", "Your six-pack"]),
 ("trainer", "INCLUDED FREE", "AI PERSONAL TRAINER",
  ["Built from your before photo", "and the goal you picked"], "06-ai-trainer-workout.png"),
 ("nutrition", "INCLUDED FREE", "AI NUTRITIONIST",
  ["Your photo, your goal", "and what you actually eat"], "05-ai-nutritionist.png"),
 ("cta2", "START FREE", "AbsByAI.com",
  ["Generate your six-pack", "in about a minute"], None, True),
]
if __name__ == "__main__":
    for c in CARDS:
        p = card(*c); print("  ", p.name)
    print(len(CARDS), "cards ->", OUT)
