#!/usr/bin/env python3
"""The reproduction's beat sheet: inserts (replace the frame) and overlay graphics.
All times are output-timeline seconds, measured off Muhammad's round-2 render."""

REF='/Volumes/Extreme/_edit_work/abwheel/mrepro/ref_hd.mp4'
ST='/Volumes/Extreme/_edit_work/abwheel/r2/stock/raw'
ST2='/Volumes/Extreme/_edit_work/abwheel/mrepro/assets/stock'
AIGEN='/Volumes/Extreme/_edit_work/abwheel/r2/aigen/infomercial.mp4'
APP=('/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/'
     '02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4')

# kind: lift (crop=full from ref), card_lift (ref interior in our glow card),
#       stock (full-bleed cover), card_stock, title, infomercial, endcard
INSERTS=[
 dict(t0=2.64,  t1=6.40,  kind='lift'),                       # hook rollout cut-ins (Dan)
 dict(t0=8.55,  t1=12.90, kind='infomercial'),                # his: TV scene; ours: AI clip in card, labeled
 dict(t0=16.10, t1=19.75, kind='title',
      lines=["WHY THE AB WHEEL IS","ONE OF THE BEST","EQUIPMENT FOR AB TRAINING"], hl=2),
 dict(t0=19.95, t1=22.16, kind='stock', src=f'{ST}/px_8027708.mp4', ss=0.5),   # wheel+dumbbell closeup
 dict(t0=29.50, t1=39.34, kind='card_lift'),                  # constant-tension card (his interior incl. whip to toe-touches)
 dict(t0=49.00, t1=52.00, kind='stock', src=f'{ST2}/px_8836753.mp4', ss=10.0), # beginner/heavier man at home (deviation: dumbbells not wheel)
 dict(t0=56.00, t1=59.90, kind='stock', src=f'{ST}/px_5319758.mp4', ss=1.0),   # ripped bodybuilder (his: blue-lit bench)
 dict(t0=62.00, t1=64.40, kind='card_lift'),                  # progression card
 dict(t0=70.50, t1=74.00, kind='stock', src=f'{ST}/px_4325592.mp4', ss=1.0),   # plank hold (core stabilising)
 dict(t0=75.50, t1=79.00, kind='stock', src=f'{ST}/px_6293127.mp4', ss=2.0),   # crunch (beach)
 dict(t0=79.00, t1=82.00, kind='stock', src=f'{ST}/px_4259064.mp4', ss=3.0),   # situps (blue shirt)
 dict(t0=86.50, t1=92.00, kind='stock', src=f'{ST}/px_8544669.mp4', ss=2.0),   # full rollout boardwalk (his: standing, yellow gym)
 dict(t0=104.50,t1=106.00,kind='stock', src=f'{ST}/px_6389051.mp4', ss=1.0),   # dumbbell rack
 dict(t0=109.00,t1=110.50,kind='stock', src=f'{ST}/px_8544638.mp4', ss=3.0),   # wheel rolling closeup (his: standing gym)
 dict(t0=110.70,t1=113.00,kind='title', lines=["HOW TO DO THE","AB WHEEL"], hl=1),
 dict(t0=271.00,t1=273.00,kind='stock', src=f'{ST}/px_8026520.mp4', ss=1.0),   # wheel overhead
 dict(t0=273.00,t1=275.00,kind='stock', src=f'{ST}/px_8027453.mp4', ss=1.0),   # wheel+shoes flatlay
 dict(t0=389.00,t1=391.00,kind='lift'),                       # Dan b-roll beat before CTA
 dict(t0=397.10,t1=408.90,kind='endcard'),
]

# overlay graphics: comp = orglib component name + args
GRAPHICS=[
 dict(t0=11.0,  t1=12.90, comp='ai_label'),
 dict(t0=23.0,  t1=26.3,  comp='pill2', line1="Why the ab wheel is so awesome &",
      line2="Why you need to be using it?", style='olive'),
 dict(t0=26.4,  t1=29.4,  comp='numchip', num="01", text="The Ab Wheel Has Constant Tension"),
 dict(t0=44.4,  t1=49.0,  comp='numchip', num="02", text="It Has A Built In Progression"),
 dict(t0=52.2,  t1=56.0,  comp='pill2', line1="How to modify this",
      line2="so It's possible for a beginner to do", style='olive'),
 dict(t0=64.7,  t1=70.4,  comp='stack', items=["Rectus Abdominis","Transverse Abdominis"]),
 dict(t0=74.0,  t1=75.5,  comp='stack', items=["Rectus Abdominis","Transverse Abdominis","Internal Obliques"], fast=True),
 dict(t0=82.0,  t1=85.2,  comp='stack', items=["Rectus Abdominis","Transverse Abdominis","Internal Obliques"], fast=True),
 dict(t0=86.0,  t1=92.0,  comp='pill2', line1="You're not just hitting your abs with the ab wheel",
      line2="You're also working on chest, shoulders & arms", style='olive', size1=48, size2=44),
 dict(t0=92.4,  t1=96.0,  comp='pill2', line1="It's A Great Total Body Exercise",
      line2="And A Great Total Abs Exercise", style='olive'),
 dict(t0=102.6, t1=106.0, comp='price', pre="You can buy it for", amount="$17"),
 dict(t0=118.8, t1=125.9, comp='thin', text="Start without your back excessively arched"),
 dict(t0=132.3, t1=136.2, comp='thin', text="Your arms need to be straight"),
 dict(t0=152.0, t1=156.0, comp='thin', text="Lock down arms and straight back"),
 dict(t0=157.0, t1=162.0, comp='thin', text="You have to rollout slowly with control"),
 dict(t0=199.5, t1=202.5, comp='pill2', line1="How to do this", line2="If you are a beginner", style='olive'),
 dict(t0=202.8, t1=224.0, comp='pillw', line1="How Beginners Should Do It"),
 dict(t0=224.5, t1=231.5, comp='pillw', line1="How Intermediate Guys Should Do It"),
 dict(t0=231.9, t1=247.5, comp='pillw', line1="How Advanced Guys Should Do It"),
 dict(t0=258.0, t1=271.0, comp='pillw', line1="How Intermediate Guys Should Do It"),
 dict(t0=275.0, t1=281.5, comp='pillw', line1="How Intermediate Guys Should Do It"),
 dict(t0=281.8, t1=285.5, comp='thin', text="Do as many reps as possible at a slow pace"),
 dict(t0=291.4, t1=311.4, comp='pillw', line1="How Advanced Guys Should Do It"),
 dict(t0=386.8, t1=392.0, comp='subscribe'),
 dict(t0=393.5, t1=397.1, comp='cta', text="AbsByAI.com"),
 dict(t0=412.3, t1=416.3, comp='cta', text="www.absbyai.com"),
]

FFWD=[(292.0,311.4),(326.1,342.8),(363.9,380.8)]
FLASHES=[2.34,12.71,19.72,39.34,43.41,59.86,64.36,110.34,338.04]
