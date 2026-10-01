#!/usr/bin/env python3
"""After deliver_all.sh: negative-events scan records bound to the delivered sha, gate plans, reviewer plan doc."""
import json, hashlib, datetime, subprocess
D="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content"
N={'S1':'short1_deadlifts-cause-more-injuries','S2':'short2_safer-lifts-build-more-muscle','S3':'short3_deadlifts-build-a-powerlifter-body','S4':'short4_two-back-exercises-instead-of-deadlifts','S5':'short5_train-legs-without-deadlifts'}
man=json.load(open('shots/manifest.json')); ov=json.load(open('overlays.json'))
note={'S1':"Zeeshan's stock photo of a man's hand on his lower back (pain, the injury point), from the approved parent: not an out-of-shape body part and not framed with shame. His AI clip of a clothed man sitting on a bench at the end.",
'S2':"Zeeshan's AI deadlift clip at the open, a clothed lifter. Dan talking for the rest.",
'S3':"Zeeshan's AI clip of a muscular powerlifter, whole body, clothed, shown as a strong lifter and not as a shame close-up; a stock close-up of a muscular chest; an AI fit shirtless man. No out-of-shape body part anywhere.",
'S4':"T-bar row stock, AI barbell row, lat pulldown stock: fit people training. Dan talking for the rest.",
'S5':"Leg press stock: a man training. Dan talking for the rest."}
import sys
IDS = sys.argv[1:] or list(N)
for S,n in [(a,b) for a,b in N.items() if a in IDS]:
    v=f"{D}/stop-deadlifting-{n}.mp4"; sha=hashlib.sha256(open(v,'rb').read()).hexdigest()
    n1=int(sum(m['frames'] for m in man if m['seg']==S)/29.97)
    json.dump({'sha256':sha,'when':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frames_checked':n1,'findings':[],
      'method':f"{n1} evenly spaced frames (every 1.0 s) of the delivered render, tiled at 160 px (gate/{S}/neg.jpg), plus every boundary pair and every shot's middle frame at 270 px (r2/look/{S}_joins.jpg, {S}_mids.jpg), inspected by the editing session (Claude, 2026-09-30): no close-up of an out-of-shape body part, no shame framing, no before/after. "+note[S]},
      open(f'gate/{S}/negative_events_scan.json','w'),indent=1)
    print(subprocess.run(['python3','make_plan.py',S,v],capture_output=True,text=True).stdout.strip().split('\n')[-1][:100])
o=["# SL-05 Stop Deadlifting shorts: the PLAN (what each short is meant to be)\n",
"Five vertical shorts (1080x1920, 29.97) cut from Zeeshan's finished 16:9 long-form 'Stop Deadlifting' (Dan approved the parent).",
"Delivered files: `Short-form video content/stop-deadlifting-<name>.mp4`.\n",
"## Locked by Dan in round 1 (not open for review, but check they were applied)",
"1. Colour: a grade on Dan's own talking footage only (target skin about 0.35 brightness / 0.39 saturation); Zeeshan's stock and AI clips keep his grade.",
"2. Title: the J2 band (eyebrow + two-line headline) held for the whole short on the black field; picture starts at y310. Title COPY is a draft Dan has not approved.",
"3. Audio: Zeeshan's mix untouched, cut only.",
"4. Hair touching the top edge of the picture is the camera's framing and Dan accepted it ('I'll accept the hair framing. I guess we have no choice about that.'). Do not report hair at the top edge.",
"\n## Layout rules of this build",
"- Dan talking is always a full-height window: FULL (724x1080 source, 1.49x) or PUNCH (527x786, 2.05x, a 1.37x step) or, twice, MID (1.2x).",
"- Zeeshan burned a lower-centre pill (KEY POINT / Exercise #n) into the parent at source rows 762-967. Any 9:16 window slices it, so OUR olive bar (full width, his colours, font and words, re-wrapped) covers exactly those rows for the whole time his pill is visible. His pill must never show sliced or as a ghost beside, above or below the bar, and the bar must be on before his pill fades in and off only after it is gone. In short 5 the bar reads 'Leg Presses' (his said 'Exercise #3: Leg Presses'; the short has no exercise 1 or 2).",
"- Captions sit above the bar (bottom about y1415) for the whole short.",
"- K card: a stock or AI clip that carries his pill, cropped above the pill, with the bar in its usual place. W card: the whole 16:9 frame (exercise demos, AI clips, Dan's lat demonstration in short 4). '*AI Generated' must be whole and readable on every AI clip.",
"- Every same-framing jump cut that Zeeshan left in the parent's talking footage is covered by a FULL<->PUNCH (or MID->FULL, or window->card) step on its exact frame. His animated zooms between medium and close are kept and the window glides sideways during them. His white one-frame flashes are kept. His zoom-blur transitions at the edges of our pieces were removed; mid-piece blurs that he placed between two takes while Dan is speaking are kept (short 3 about 29.6-30.2 s; short 4 about 53.4-54.1 s).",
"- Standing rule: when a short tells the viewer to do an exercise, complete reps of it must be on screen (short 4: T-bar row, barbell row, lat pulldown; short 5: leg press).",
"- No cover image in this job. Wordmark AbsByAI.com bottom left.\n"]
for S,n in N.items():
    o.append(f"## {S}: `stop-deadlifting-{n}.mp4`")
    for m in [m for m in man if m['seg']==S]:
        o.append(f"- {m['outStart']:6.2f}-{m['outStart']+m['dur']:6.2f} s  {m['t']}{' '+m['win'] if m.get('win') else ''}: {m['why']}")
    for p in ov.get(S,[]): o.append(f"- bar {p['id']} on screen {p['t0']:.2f}-{p['t1']:.2f} s at y{p['y']}-{p['y']+p['h']}")
    o.append('')
open('r2/PLAN-for-review.md','w').write('\n'.join(o))
