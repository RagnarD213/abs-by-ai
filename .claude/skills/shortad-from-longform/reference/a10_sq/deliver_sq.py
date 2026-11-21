#!/usr/bin/env python3
"""Deliver the 1:1 SQUARE beside Muhammad's 16:9 and the approved vertical, in the
editor-deliveries convention (`title | editor | aspect | number`).

Runs only after qc.py has passed on the work-dir master. Gates the DELIVERED file (stamp beside
it), md5-verifies the copy, makes the 540p and 480p review copies plus the audio A/B, and checks
the review copies' audio integrity too -- a re-encode inherits a broken master, and a mux once
truncated audio at 2:24 of a 3:52 video and exited 0.
"""
import hashlib, os, shutil, subprocess, sys
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
AUD = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
SRC = 'ad2_square_1x1.mp4'
DEST = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/"
        "stop wasting money on nutritionists - ad 2")
NAME    = "stop wasting money on nutritionists | claude | 1x1 | ad 2.mp4"
REVIEW  = "stop wasting money on nutritionists | REVIEW 540p 1x1 | ad 2.mp4"
REVIEW2 = "stop wasting money on nutritionists | REVIEW 480p 1x1 phone | ad 2.mp4"
AB      = "stop wasting money on nutritionists | AB audio his-vs-ours 1x1 | ad 2.mp4"

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()

def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2000:])
    return r.stdout

def audio_ok(path, label):
    import numpy as np, wave
    vd = float(sh([FP,'-v','error','-select_streams','v','-show_entries','stream=duration','-of','csv=p=0',path]).strip().split('\n')[0])
    ad = float(sh([FP,'-v','error','-select_streams','a','-show_entries','stream=duration','-of','csv=p=0',path]).strip().split('\n')[0])
    sh([FF,'-v','error','-y','-i',path,'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le','/tmp/_dsq.wav'])
    x = np.frombuffer(wave.open('/tmp/_dsq.wav').readframes(10**9), dtype='<i2').astype(np.float32)/32768
    sec = [20*np.log10(np.sqrt((x[i*16000:(i+1)*16000]**2).mean())+1e-12) for i in range(int(len(x)//16000))]
    silent = sum(1 for v in sec if v < -50)
    print(f'{label}: video {vd:.3f}s audio {ad:.3f}s silent seconds {silent} quietest {min(sec):.1f} dBFS')
    assert abs(vd-ad) < 0.15 and silent == 0, f'{label} AUDIO INTEGRITY FAILED'

os.makedirs(DEST, exist_ok=True)
dst = os.path.join(DEST, NAME)
shutil.copyfile(SRC, dst)
assert md5(SRC) == md5(dst), 'md5 mismatch after copy'
print('master copied, md5', md5(dst))

r = subprocess.run(['python3', f'{AUD}/audio_gate.py', dst, '--reference-mix', 'his_mix.wav',
                    '--ab', os.path.join(DEST, AB)], capture_output=True, text=True)
print(r.stdout[-1600:])
if r.returncode: raise SystemExit('AUDIO GATE FAILED ON THE DELIVERED FILE')
print(sh(['python3', f'{AUD}/require_stamp.py', dst]))

for name, size, crf, ab in ((REVIEW, '540:540', '23', '160k'), (REVIEW2, '480:480', '26', '128k')):
    rv = os.path.join(DEST, name)
    sh([FF,'-nostdin','-v','error','-y','-i',dst,'-vf',f'scale={size}:flags=lanczos','-r','30000/1001',
        '-c:v','libx264','-preset','medium','-crf',crf,'-pix_fmt','yuv420p',
        '-c:a','aac','-b:a',ab,'-movflags','+faststart',rv])
    audio_ok(rv, os.path.basename(name))
audio_ok(dst, 'master')

rec = os.path.join(DEST, 'recipe-square'); os.makedirs(rec, exist_ok=True)
for f in ['beats.py','assets.py','render.py','vlib.py','captions.py','muxsq.py','qc.py','qc.json',
          'watch.py','centering.py','landing_check.py','hairgate_sq.py','deliver_sq.py','sqstills.py',
          'facetrack.py','facetrack3.py','facetrack4.py','cover.py','edl_final.json','edl_picture.json',
          'facetrack.json','cover.json','grade.py','grade.txt','grade_curves.json','vignette.json',
          'words_ctc.json','logs/watch_pass.json','logs/centering.json','logs/caption_sync.json',
          'logs/hairgate_sq.json','notes-square.md']:
    if os.path.exists(f): shutil.copyfile(f, os.path.join(rec, os.path.basename(f)))
shutil.copyfile('notes-square.md', os.path.join(DEST, 'notes-square.md'))
print('delivered to', DEST)
for f in sorted(os.listdir(DEST)): print('   ', f)
