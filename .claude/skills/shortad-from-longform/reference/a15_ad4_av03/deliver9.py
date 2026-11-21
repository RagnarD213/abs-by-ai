#!/usr/bin/env python3
"""Deliver the four Ad 4 files beside Muhammad's 16:9 under the /editor-deliveries naming, each with its stamps, a REVIEW
540p copy and its audio A/B, plus the audio exception note, the notes and the recipe. Nothing is uploaded anywhere.

A stamp counts only if its sha256 is the delivered bytes (skill S1 C): asserted here for both stamps of every file.
The audio stamp is allowed to FAIL on the `tp` row ONLY (Muhammad's own export peaks at -0.90 dBTP; Dan accepted that
audio on 2026-09-11) -- any other failing audio row refuses the delivery.

  python3 deliver9.py [--dry]
"""
import hashlib, json, os, shutil, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
DEST = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/stop wasting money on supplements - ad 4"
T = "stop wasting money on supplements"
FILES = [('.', 'ad4_9x16.mp4', '9x16', '9x16', ''), ('cut', 'ad4_9x16_59s.mp4', '9x16 59s', '9x16', ''),
         ('.', 'ad4_1x1.mp4', '1x1', '1x1', '_sq'), ('cut_sq', 'ad4_1x1_59s.mp4', '1x1 59s', '1x1', '_sq')]
DRY = '--dry' in sys.argv
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
old = os.path.join(DEST, '_superseded 2026-09-11 review copies (BT.601 colour)')
if not DRY:
    os.makedirs(old, exist_ok=True)
    for f in os.listdir(DEST):                      # the 09-11 review copies carry the colour fault: set aside, never deleted
        if ('REVIEW 4' in f or 'REVIEW 5' in f or 'AB audio' in f) and f.endswith('.mp4') and os.path.getmtime(os.path.join(DEST, f)) < 1790000000:
            shutil.move(os.path.join(DEST, f), os.path.join(old, f))
rows = []
for d, v, label, aspect, sfx in FILES:
    src = os.path.join(d, v); s = sha(src)
    ag = json.load(open(src + '.audio_gate.json')); dg = json.load(open(src + '.deliver_gate.json'))
    assert ag.get('sha256') == s, f'{src}: the audio stamp is for other bytes'
    assert dg.get('sha256') == s, f'{src}: the delivery stamp is for other bytes'
    bad = [r['key'] for r in ag['rows'] if r.get('gated', True) and not r.get('ok')] if isinstance(ag['rows'], list) else \
          [k for k, r in ag['rows'].items() if r.get('gated', True) and not r.get('ok')]
    assert set(bad) <= {'tp'}, f'{src}: audio rows failing besides the accepted true peak: {bad}'
    name = f'{T} | claude | {label} | ad 4.mp4'
    rows.append((src, name, s, ag['verdict'], bad, dg['verdict']))
    if DRY: print('would deliver', name, s[:12], 'audio', ag['verdict'], bad, 'gate', dg['verdict']); continue
    shutil.copyfile(src, os.path.join(DEST, name))
    shutil.copyfile(src + '.audio_gate.json', os.path.join(DEST, name + '.audio_gate.json'))
    shutil.copyfile(src + '.deliver_gate.json', os.path.join(DEST, name + '.deliver_gate.json'))
    rv = os.path.join(DEST, f'{T} | REVIEW 540p {label} | ad 4.mp4')
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', src, '-vf', 'scale=540:-2', '-c:v', 'h264_videotoolbox', '-b:v', '2600k', '-pix_fmt', 'yuv420p',
                    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-c:a', 'copy', '-movflags', '+faststart', rv], check=True)
    ab = os.path.join(d, f"AB_audio_his-vs-ours_{aspect}{'_59s' if '59s' in label else ''}.mp4")
    if os.path.exists(ab): shutil.copyfile(ab, os.path.join(DEST, f'{T} | AB audio his-vs-ours {label} | ad 4.mp4'))
    assert sha(os.path.join(DEST, name)) == s
    print('delivered', name, s[:12])
if not DRY:
    for f in ('AUDIO_EXCEPTION.md', 'notes-vertical-and-square-AV-03.md'):
        if os.path.exists(f): shutil.copyfile(f, os.path.join(DEST, f if f.startswith('notes') else f'{T} | claude | ad 4.AUDIO_EXCEPTION.md'))
    rec = os.path.join(DEST, 'recipe-AV-03'); os.makedirs(rec, exist_ok=True)
    keep = [f for f in os.listdir('.') if f.endswith(('.py', '.sh', '.md')) or (f.endswith('.json') and os.path.getsize(f) < 3_000_000) or f.endswith('.cube')]
    for f in keep: shutil.copyfile(f, os.path.join(rec, f))
    for d in ('cut', 'cut_sq'):
        os.makedirs(os.path.join(rec, d), exist_ok=True)
        for f in os.listdir(d):
            p = os.path.join(d, f)
            if os.path.isfile(p) and f.endswith(('.py', '.json')) and os.path.getsize(p) < 3_000_000: shutil.copyfile(p, os.path.join(rec, d, f))
    json.dump([dict(file=n, sha256=s, audio=a, audio_failing=b, gate=g) for _, n, s, a, b, g in rows], open(os.path.join(DEST, 'delivery-AV-03.json'), 'w'), indent=1)
    print('recipe + notes + delivery-AV-03.json written')
