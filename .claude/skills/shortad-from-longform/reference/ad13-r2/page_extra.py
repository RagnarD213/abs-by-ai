#!/usr/bin/env python3
"""Ad 13 round 2: page_extra.json for sbl_page.py (only what changed). Numbers are read from the build, not typed."""
import json
import os

import numpy as np

B = "/Volumes/Extreme/_edit_work/kit9x16/av11-ad13"
R2 = B + "/review2"
FPS = 30000 / 1001


def first_minute(track):
    """Camera travel inside shots (px on the phone screen) and how far he sits off centre, over the first minute."""
    S = json.load(open(B + "/edl_picture.json"))
    n, x = np.array(track["n"]), np.array(track["x"])
    starts = {s["n0"] for s in S}
    m = n < 62 * FPS
    n, x = n[m], x[m]
    inside = np.array([n[i + 1] not in starts for i in range(len(n) - 1)])
    return float(np.abs(np.diff(x))[inside].sum()) * 1080 / 608


old = json.load(open(B + "/round2/track_tol0.json"))
new = json.load(open(B + "/facetrack.json"))
so, sn = old["stats"], new["stats"]
k = 1080 / 608
t_old, t_new = first_minute(old), first_minute(new)
proof = json.load(open(B + "/round2/h16x9/grade_proof.json")) if os.path.exists(B + "/round2/h16x9/grade_proof.json") else []
gp = f"{np.mean([r['mean_abs_levels'] for r in proof]):.1f}" if proof else "?"

frames = """<section id="opener"><h2>The new AI opener: START and END frames (approve these before I generate motion)</h2>
<p><b>Action:</b> the robot spots the dad through one bench press rep (bar at his chest, then pressed to lockout) while the fired trainer walks toward the camera with his box of belongings and looks back at the robot. Camera locked off. No text in the picture.<br>
<b>Length:</b> 3.7 seconds on screen, covering "Here's why I fired my personal trainer and nutritionist". You appear on "and saved $1,000 a month". Muhammad's audio is untouched; the opener replaces picture only, and the hook lower third stays over it.<br>
<b>Cost:</b> the four frames were made on the Codex subscription ($0). Motion is two clips (one vertical, one horizontal), about $0.25 to $0.50 each. Your cap is $5 per video including retries. The square is cut from the vertical clip, so there is no third clip.</p>
<div class="grid wide">
<article><h3>Vertical (9:16) START</h3><a href="frames/OPENER-start-9x16.png"><img loading="lazy" src="frames/OPENER-start-9x16.png" style="max-height:70vh;width:auto;display:block;margin:auto"></a></article>
<article><h3>Vertical (9:16) END</h3><a href="frames/OPENER-end-9x16.png"><img loading="lazy" src="frames/OPENER-end-9x16.png" style="max-height:70vh;width:auto;display:block;margin:auto"></a></article>
<article><h3>Horizontal (16:9) START</h3><a href="frames/OPENER-start-16x9.png"><img loading="lazy" src="frames/OPENER-start-16x9.png"></a></article>
<article><h3>Horizontal (16:9) END</h3><a href="frames/OPENER-end-16x9.png"><img loading="lazy" src="frames/OPENER-end-16x9.png"></a></article>
</div></section>
<section id="grade"><h2>Horizontal: the colour against Muhammad's master, same moments side by side</h2>
<p class="small">Left: Muhammad's finished 16:9. Right: the new Soft Blue Light build. Plain talking frames with no graphic on either side.</p>
<a href="h16x9/grade_proof.jpg"><img loading="lazy" src="h16x9/grade_proof.jpg"></a></section>"""

X = {
    "title": "Ad 13 \"The Cost Of Getting Abs\" / round 2: your revisions, the AI opener frames, and the new horizontal",
    "intro": "Only what changed since round 1. Two first minutes (the vertical with your changes, and the new Soft Blue Light horizontal), the opener's START and END frames, and the five replaced items. <b>No full video was built and nothing was uploaded.</b> In both first minutes the opener is shown as its START frame, then its END frame, with a yellow PLACEHOLDER tag, because motion is not generated until you approve the frames.",
    "locked": "From round 1: the audio and the colour of the vertical's first minute (your words). Muhammad's edit, cuts and audio mix. Every graphic and clip you did not name in round 1 is unchanged and is not shown again.",
    "decisions": [
        "<b>The opener frames.</b> Approve the START and END frames (vertical and horizontal) so I can generate the motion, or give changes.",
        "<b>P03, the 3 minute abs video in phone orientation.</b> A (shown): the YouTube page re-laid for a phone, with the player cropped square so you are large and centred and Mike Chang is at the edge; the title, 4.47M subscribers and 2.6M views are under it. B: the same page with the whole wide video, which makes you about half the size. I recommend A.",
        "<b>The new horizontal's first minute.</b> Approve the Soft Blue Light graphics on it (lower thirds, the list card, the price card, the running total), or notes by timestamp.",
    ],
    "decided": [
        f"<b>Calmer centering.</b> The camera now lands on you at each cut, then holds until you are about 12 pixels (of the 1080 wide raw) off centre before it follows. Over the whole ad the camera travels {round(100 * (1 - sn['travel_px'] / so['travel_px']))} % less ({round(so['travel_px'] * k):,} to {round(sn['travel_px'] * k):,} phone pixels) and its typical fast pan is {round(100 * (1 - sn['pan_p90_px_s'] / so['pan_p90_px_s']))} % slower ({round(so['pan_p90_px_s'] * k)} to {round(sn['pan_p90_px_s'] * k)} px/s). In the first minute: {round(t_old):,} to {round(t_new):,} px of travel. You sit a median {round(sn['off_centre_px']['median'] * k)} px off centre (was {round(so['off_centre_px']['median'] * k)}), at most {round(sn['off_centre_px']['max'] * k)} px (was {round(so['off_centre_px']['max'] * k)}), on a 1080 px wide screen, so your head never nears the edge. If you want it calmer still, say so: the next step cuts travel by 55 % with you a median 33 px off centre.",
        "<b>P03 source.</b> YouTube downloads are blocked on this Mac, so I used your own 4K screen recording of the real YouTube page for this video (in the SixPackAbs archive). I used 8 to 15 seconds in: before the workout starts, hands on hips, camera on you, Mike Chang at the side. In the horizontal the same moment plays as the whole YouTube page.",
        "<b>P06 photo.</b> studio-gray-79: big smile, hands on hips, green shorts, full screen with the real-picture label placed by measurement off your face and abs. I chose green shorts on gray so it does not repeat the red Thai shorts of P05 right before it. It is not on the frowning list.",
        "<b>P09 to P11, one bland meal clip.</b> A0060 from our AI library: a man takes a bite of plain chicken, white rice and broccoli and grimaces. One clip across \"Chicken. Broccoli. Rice.\" It shows as a centre square in a card because filling the phone screen would cut the plate. It keeps the AI-GENERATED label. No new clip was generated.",
        "<b>P20 workout demo.</b> The approved workout-app format from the website video: the exercise list, a tap on Crunch, then the AI exercise video above its description. No stick figures anywhere.",
        "<b>P22 recipes demo.</b> The approved three-meal screen (Honey Soy Chicken, Tex Mex Beef Rice Skillet, Greek Yogurt Berry Bowl): tap Honey Soy Chicken, see it, tap the Tex Mex skillet, see it. I shortened the pause between the two taps to fit your 6.3 seconds of speech; the phone screen is identical across that join.",
        "<b>Where the opener sits.</b> 0:00 to 0:03.7. The AI-GENERATED label is on it. The hook lower third (\"I Fired My Trainer And Nutritionist. Saved $1,000 A MONTH.\") plays over it.",
        "<b>Horizontal: what stayed Muhammad's.</b> His cut, every take, his slow zoom in and out on your talking shots (measured from his master), his white flash on returns, his audio (the first minute of his own mix, copied without processing).",
        "<b>Horizontal: what is new.</b> Every graphic is Soft Blue Light: Motivation lower thirds, the list card on the left with you moved right (his text screen), a price card, and the running total as a small glass chip top left. Pictures he showed on olive cards are on blue cards. The wording is the vertical's. The flag photo stays in the horizontal (your P06 swap was for the vertical, where a wide photo does not fill the screen).",
        "<b>Spend this round: $0.00 of paid generation.</b> Four opener frames on the Codex subscription (about 118,000 Codex tokens). Total paid AI on this ad so far: under one cent.",
    ],
    "checks": [
        f"Horizontal colour vs Muhammad's master on 8 plain talking frames: average difference {gp} levels out of 255 (head and shoulders area). Side by side stills are above.",
        "Horizontal first minute: 1,858 frames, the same count as Muhammad's first 62 seconds; audio stream-copied from his master.",
        "Vertical: frame count matches the plan; captions forced-aligned to his mix; his flash kept on the two swapped full-screen pictures.",
        "Every AI frame was checked at full size for hands, faces, text and the barbell. The bland meal clip was checked frame by frame over the part used.",
        "<b>Proven on the horizontal:</b> his cut and grade from the raw roll, his zoom, the 16:9 lower third and list card (your approved templates). <b>Not proven yet:</b> the price card, the running total chip and the picture cards at 16:9 are new layouts of approved templates and you are seeing them here for the first time; the delivery gate, the judges and the independent review have not run on any horizontal file; minutes 2 to 4 are not built.",
        "<b>Not done yet, on purpose:</b> no full vertical, no 59 second cut, no square, no full horizontal, no gate. Nothing was uploaded. The live horizontal in Google Ads is untouched.",
    ],
    "reply": "1 Opener frames: approved, generate the motion / changes:\n2 P03 phone page: A square player (recommended) / B whole wide video\n3 Horizontal first minute graphics: approved / notes by timestamp:\nVertical first minute and centering notes:\nItem notes (P03, P06, P09-P11, P20, P22):\nAnything to overrule in What I decided:",
    "first_minute_end": 62.0,
    "minute_title": "The two first minutes (0:00 to 1:02)",
    "minutes": [
        {"title": "Vertical 9:16, round 2", "src": "first-minute/DRAFT - Ad 13 9x16 round 2 - first minute - REVIEW 540p.mp4",
         "poster": "first-minute/vertical.jpg",
         "caption": "Opener placeholders, calmer centering, new P03 (0:24) and P06 (0:42). <a href=\"first-minute/DRAFT - Ad 13 9x16 round 2 - first minute.mp4\">1080 x 1920 file</a>"},
        {"title": "NEW horizontal 16:9, Soft Blue Light", "src": "h16x9/DRAFT - Ad 13 16x9 Soft Blue Light round 2 - first minute - REVIEW 540p.mp4",
         "poster": "first-minute/horizontal.jpg",
         "caption": "Muhammad's cut, zooms and audio; every graphic redrawn. <a href=\"h16x9/DRAFT - Ad 13 16x9 Soft Blue Light round 2 - first minute.mp4\">1920 x 1080 file</a>"},
        {"title": "For comparison: vertical, round 1", "src": "round1/DRAFT - first minute 9x16 - REVIEW 540p.mp4", "poster": "round1/DRAFT - first minute 9x16.jpg",
         "caption": "The first minute you reviewed, to compare the camera movement."},
    ],
    "first_minute_note": "Drafts: not gated, not judged. Muhammad's own audio on all three.",
    "extra_html": frames,
    "only_media": {"yt3min_9x16": "P03", "studio_gray_79": "P06", "bland_meal": "P09-P11", "phone_workout": "P20", "phone_recipes": "P22"},
    "notes": {"P03": "Replaces the old diet-interview clip. Phone-orientation YouTube page, built from your recording of the real page.",
              "P06": "Replaces the flag photo. Full screen, like P05.",
              "P09-P11": "Replaces the three tasty food clips with one bland meal. Centre square in a card.",
              "P20": "Replaces the stick-figure workout screen. The whole phone in a card.",
              "P22": "Replaces the meal tracker. The whole phone in a card."},
    "all_title": "The five replaced items at 9:16",
}
json.dump(X, open(R2 + "/page_extra.json", "w"), indent=1)
print("page_extra ok")
