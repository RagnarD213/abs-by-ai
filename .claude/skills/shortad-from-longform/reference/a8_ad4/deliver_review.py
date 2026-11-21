#!/usr/bin/env python3
"""Deliver the REVIEW copies (not the masters) of the Ad 4 vertical + cutdown into the Ad 4 folder, under the
/editor-deliveries convention, plus the A/B audio clip, the notes and the recipe.

Why not `deliver4.py`: it refuses a file whose audio gate has no PASS stamp, and on this build the EDITOR'S OWN export
misses Dan's true-peak rule by 0.1 dB (-0.90 dBTP against -1.0). His audio is not ours to trim (skill Step 4 / AGENTS.md),
so the full-resolution masters stay in the work dir until Dan chooses: accept it, or a -1.0 re-export from Muhammad and a
5-minute re-mux. The review copies carry the same picture and the same audio, so he can approve the cut meanwhile.
Every copy is md5-verified and its audio stream checked for length and silence."""
import hashlib, json, os, shutil, subprocess, wave
import numpy as np
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
DEST = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/stop wasting money on supplements - ad 4"
T = "stop wasting money on supplements"
FILES = [
    ('review/review_full_540p.mp4', f"{T} | REVIEW 540p 9x16 | ad 4.mp4"),
    ('review/review_full_480p.mp4', f"{T} | REVIEW 480p 9x16 phone | ad 4.mp4"),
    ('review/review_59s_540p.mp4',  f"{T} | REVIEW 540p 9x16 | 9x16 59s | ad 4.mp4"),
    ('review/review_59s_480p.mp4',  f"{T} | REVIEW 480p 9x16 phone | 9x16 59s | ad 4.mp4"),
    ('AB_audio_his-vs-ours.mp4',    f"{T} | AB audio his-vs-ours | ad 4.mp4"),
    ('cut/AB_audio_his-vs-ours_59s.mp4', f"{T} | AB audio his-vs-ours | 9x16 59s | ad 4.mp4"),
]
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
def probe(p, sel, entries):
    out = subprocess.run([FP, '-v', 'error', '-select_streams', sel, '-show_entries', f'stream={entries}',
                          '-of', 'csv=p=0', p], capture_output=True, text=True).stdout.strip().split('\n')[0]
    return out
os.makedirs(DEST, exist_ok=True)
for src, name in FILES:
    if not os.path.exists(src): print('MISSING', src); continue
    dst = os.path.join(DEST, name); shutil.copyfile(src, dst)
    assert md5(src) == md5(dst), f'md5 mismatch after copying {name}'
    vd, ad = float(probe(dst, 'v', 'duration')), float(probe(dst, 'a', 'duration'))
    subprocess.run([FF, '-v', 'error', '-y', '-i', dst, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', '/tmp/_dv.wav'], check=True)
    x = np.frombuffer(wave.open('/tmp/_dv.wav').readframes(10**9), dtype='<i2').astype(np.float32)/32768
    sec = [20*np.log10(np.sqrt((x[i*16000:(i+1)*16000]**2).mean())+1e-12) for i in range(int(len(x)//16000))]
    silent = sum(1 for v in sec if v < -50)
    assert abs(vd-ad) < 0.15 and silent == 0, f'{name}: audio integrity failed (video {vd} audio {ad}, {silent} silent s)'
    print(f'{name}  video {vd:.3f}s audio {ad:.3f}s silent {silent} quietest {min(sec):.1f} dBFS  md5 {md5(dst)[:12]}')
shutil.copyfile('notes.md', os.path.join(DEST, 'notes-vertical.md'))
rec = os.path.join(DEST, 'recipe-vertical'); os.makedirs(rec, exist_ok=True)
for f in ['beats.py', 'g5.py', 'g8.py', 'render8.py', 'captions.py', 'align_ctc.py', 'caption_sync_check.py', 'zmux.py',
          'zalign.py', 'zprofile2.py', 'zfit.py', 'zfit_right.py', 'zpic2.py', 'zedl.py', 'zedl3.py', 'zlut.py', 'zvig.py',
          'zbase.py', 'zmeasure.py', 'zhair.py', 'zcrop.py', 'zhairgate2.py', 'zassets4.py', 'zmatch4.py', 'zmatch4b.py',
          'zmatch4c.py', 'zcutdown.py', 'zcut_build.py', 'watch.py', 'landing_check.py', 'centering.py', 'deliver4.py',
          'deliver_review.py', 'edl_picture.json', 'crop.json', 'fit.json', 'offset_profile.json', 'vignette.json',
          'his.cube', 'cut_plan.json', 'qc.json', 'words_ctc.json', 'media_map.json', 'hdcheck2/hd_vs_draft.json',
          'logs/watch_pass.json', 'logs/qc_master4.log', 'cut/logs/qc_cut4.log', 'cut/logs/watch_pass.json',
          'logs/hairgate2_4.log', 'logs/landing4.log', 'logs/capsync4.log', 'logs/audio_gate4.log',
          'audit/AUDIT.md', 'audit2/AUDIT2.md', 'audit3/AUDIT3.md', 'notes.md']:
    if os.path.exists(f): shutil.copyfile(f, os.path.join(rec, f.replace('/', '__')))
print('\ndelivered (review copies only -- masters held for Dan\'s true-peak call) to', DEST)
print('\n'.join(sorted(os.listdir(DEST))))
