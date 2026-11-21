#!/usr/bin/env python3
"""SL-05 round 2 key-point BARS in ZEESHAN'S style: olive fill (77,86,49), text (230,237,216), Manrope SemiBold 46 px,
his wording (read off his frames, r1/pills/all.png). Full width (1080) and exactly as tall as his pill's rows in a FULL
window (pill/bar_geo.json, written by plan_shots.py), so it covers his sliced pill whole. usage: make_pill5.py"""
from PIL import Image, ImageDraw, ImageFont
import os, json
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/ad-factory/the-upload/assembly/fonts/Manrope.ttf'
PILLS = {
    'S1-kp1': ['KEY POINT: Deadlifts Cause More', 'Injuries Than Every Other', 'Lift Combined!'],
    'S1-kp2': ['KEY POINT: An Injury Costs', 'You Months Of Progress,', 'Not Days'],
    'S1-kp3': ['KEY POINT: Most People Who', 'Quit The Gym Quit Because', 'Of An INJURY'],
    'S2-kp1': ['KEY POINT: Over 40, One Bad', 'Injury Can End Your', 'Training For GOOD'],
    'S2-kp2': ['KEY POINT: Lower Risk Exercises', 'Build MORE MUSCLE Over The', 'Long Term When Accounting', 'For Injuries'],
    'S3-kp1': ['KEY POINT: Deadlifts Build A', 'Thick POWERLIFTER Body,', 'Not An Aesthetic One'],
    'S3-kp2': ['KEY POINT: You Do Not Need', 'Deadlifts To Look Good', 'With Your Shirt Off'],
    'S4-ex2': ['Exercise #2: Lat Pulldowns'],
    'S4-kp1': ['KEY POINT: Wide Grip Builds', 'WIDTH. Narrow Grip Builds', 'Powerlifter THICKNESS.'],
    'S5-kp1': ['KEY POINT: Leg Presses Build', 'Nearly The Same Legs With', 'Almost NONE Of The Risk'],
    # his pill reads "Exercise #3: Leg Presses"; the short has no exercise 1 or 2 (round-1 review), so the number is dropped
    'S5-ex3': ['Leg Presses'],
}
GEO = json.load(open(os.path.join(HERE, 'bar_geo.json')))
# his words re-wrapped for the bar: the largest size (<= 60 px) at which every line fits 1010 px and the block fits the bar
for name, lines in PILLS.items():
    y, h = GEO[name]; w = 1080
    for size in range(60, 40, -1):
        f = ImageFont.truetype(FONT, size); f.set_variation_by_name(b'SemiBold'); lh = round(size * 1.24)
        if max(f.getlength(l) for l in lines) <= 1010 and lh * len(lines) <= h - 20: break
    else: raise SystemExit(f'{name} does not fit')
    im = Image.new('RGBA', (w, h), (77, 86, 49, 255)); d = ImageDraw.Draw(im)
    cap = f.getbbox('H'); top = (h - lh * len(lines)) / 2
    for i, l in enumerate(lines):
        yy = top + i * lh + (lh - (cap[3] - cap[1])) / 2 - cap[1]
        d.text(((w - f.getlength(l)) / 2, yy), l, font=f, fill=(230, 237, 216, 255))
    out = os.path.join(HERE, '..', 'assets', f'pill-{name}.png'); im.save(out); print(name, im.size, 'y', y, 'font', size)
