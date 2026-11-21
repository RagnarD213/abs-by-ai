CONTENT (SFC). How To Do T-Bar Rows (DS-77). Cover review; setup waits for Dan's pick.

Updated: 2026-11-05

Review: http://127.0.0.1:9477/ (managed, starts on demand). Eight blind choices X1 to X8 (five Codex, three Google; key hidden in `Short-form video content/covers/review/ds77-t-bar-rows-20261105/blind/`). Log the pick with `blind.py pick`; map X to plate with `blind.py reveal` only for installing.

Film preserved: master SHA256 eddb7539ae03db9c853040f303ad6f7c6706ab4c48699d684a82a07171715d23 (project folder and Extreme re-hashed 2026-11-05). SRT a6911389...ae0.
Drive backup done: https://drive.google.com/open?id=1v8UqiC3NfwGVjJTvyy4ydiPiz1mauOAb (mp4 MD5 c849db8a2853e71f87ddb48658187746, SRT 139bee1f00079fd64453cbf32886ad0a, approval and finalization receipt; anyone with the link).

Designs (internal plates, same headline "How To Do / T-Bar Rows"): A AI Dan front-side, bottom title; B AI Dan shirtless back view, white/cyan Impact; C real studio-blue-247 photo (original person pixels) over a Codex T-bar machine plate, navy plaque; D retouched real 4K frame B0723 1.5 s, yellow band (DS-76 F style); E retouched B0723 13.0 s, white/gold serif; F/G/H Google twins of A, B, E prompts with A/D/B styles. Codex gpt-6.1-sol high, subscription. D first try replaced his face (kept as D-try1-face-changed.png); regenerated with the identity reference. Google: Flow Nano Banana Pro, 0 credits, no refusals, no visible mark. H keeps a strained expression.
Checks: check.py passes all except D's extra detected faces (gym mural cartoons, no text on them). Faces inspected against the identity reference.

Slot plan: phase 3 gym Short; first open slot in the calendar is Tue Jan 5 9 AM (10 days after DS-76, 7 after DS-63). Confirm against the live queue and waitlist at booking.

Next after pick: covers/approved-ds77/picks.json, TikTok cover-first copy, Blotato uploads with hash checks, config (gym true), pinned_comment, FB cover registry, cover_audit + ad_guard, schedule or waitlist, receipt.

## Round 2 (Dan, 2026-11-06)
Dan: "I like X4 the best, but I feel like we can do better with that touched-up screenshot. Give me four new designs with four new touched-up screenshots. All of them unique." Pick logged with blind.py (X4 = plate H).
Four new real 4K frames, retouched by Codex (gpt-6.1-sol high, subscription) with the identity reference as image 2 to hold the face; shown as N1..N4 (not blind; one maker):
- N1 = plate I: B0723 4.5 s, wide with mural and full machine; yellow band.
- N2 = plate J: B0724 1.5 s, low angle, plates in front, face visible; white/cyan Impact (X4's style).
- N3 = plate K: B0725 13.5 s, close side, shoulder and arm at the top of the pull; large bottom title.
- N4 = plate L: B0725 5.0 s, rear view, back squeeze (no face); navy plaque.
check.py (manifest-r2.json, cover-checks-r2.json): no text on faces, bounds safe, YouTube JPEGs 316-355 KB. Faces inspected. Review page reorders: N1-N4 first, X4 for comparison, then the first eight.

## Round 3 (Dan, 2026-11-06): real photos only
Dan on N1-N4: "this isn't what I asked for. These are AI-generated images. I want four touch-up screenshots, real images, not AI-generated." N1-N4 removed from the page (masters kept in ds77/ as plates I-L).
R1-R4 built by `scripts/covers/ds77-20261105/real_build.py`: real 16-bit frames from the finished Color C library masters, 9:16 crop (1215x2160) downscaled to 1080x1920, photo edits only (gamma 0.86, gentle S-curve, saturation 1.08, wide clarity 0.30, light sharpen 0.40, dither). No generative step; title space is flat colour blocks (R1, R2, R4) or a gradient (R3). Frames chosen for a focused, non-grimacing face.
- R1: B0723 5.0 s, front-side with mural; yellow band.
- R2: B0724 1.75 s, flags behind, face clear; white/cyan Impact.
- R3: B0725 12.25 s, close side profile, shoulder and arm; large bottom title.
- R4: B0725 5.0 s, rear back view; navy plaque.
Manifest and hashes: `Short-form video content/covers/review/ds77-t-bar-rows-20261105/ds77-real/manifest.json`. Page notes X4 itself was AI-retouched (no maker named).
