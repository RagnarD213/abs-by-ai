#!/usr/bin/env python3
"""Deliver the Ad 5 vertical (full length + the <=0:59) beside Muhammad's V3 HD under the editor-deliveries convention
(`title | editor | aspect | number`, lowercase, punctuation dropped). Runs only after qc.py has passed on both work-dir
masters. Copies are md5-verified; the audio gate re-runs on the DELIVERED files in verbatim mode (stamp beside each);
review copies are made and their audio integrity is checked (a re-encode inherits a broken master)."""
import hashlib, os, shutil, subprocess, sys, json
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
AUD = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
DEST = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/every diet youve tried failed for the same reason - ad 5"
T = "every diet youve tried failed for the same reason"
HIS_SRC = 'ref/ad5_v3_hd.mp4'
FILES = [  # (work file, delivered name, his mix for the verbatim gate)
    ('ad5_vertical_9x16.mp4',         f"{T} | claude | 9x16 | ad 5.mp4",      'his_mix.wav'),
    ('cut/ad5_vertical_9x16_59s.mp4', f"{T} | claude | 9x16 59s | ad 5.mp4",  'cut/his_mix.wav'),
]
def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()
def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise SystemExit(r.stderr[-2000:])
    return r.stdout
os.makedirs(DEST, exist_ok=True)
# Muhammad's own HD export, filed beside ours under the convention (the /editor-deliveries rule)
his = os.path.join(DEST, f"{T} | muhammad | 16x9 | ad 5.mp4")
if not os.path.exists(his): shutil.copyfile(HIS_SRC, his); print('filed his V3 HD as', os.path.basename(his))
import numpy as np, wave
for src, name, mix in FILES:
    dst = os.path.join(DEST, name); shutil.copyfile(src, dst)
    assert md5(src) == md5(dst), 'md5 mismatch after copy'; print('copied', name, 'md5', md5(dst))
    ab = os.path.join(DEST, name.replace('| claude |', '| AB audio his-vs-ours |'))
    r = subprocess.run(['python3', f'{AUD}/audio_gate.py', dst, '--reference-mix', mix, '--verbatim', '--ab', ab], capture_output=True, text=True)
    print(r.stdout[-600:])
    if r.returncode: raise SystemExit('AUDIO GATE FAILED ON THE DELIVERED FILE ' + name)
    print(sh(['python3', f'{AUD}/require_stamp.py', dst]))
    for tag, vf, crf in (('REVIEW 540p 9x16', 'scale=540:960:flags=lanczos', '23'), ('REVIEW 480p 9x16 phone', 'scale=480:854:flags=lanczos', '26')):
        rv = os.path.join(DEST, name.replace('| claude |', f'| {tag} |'))
        sh([FF, '-nostdin', '-v', 'error', '-y', '-i', dst, '-vf', vf, '-r', '30000/1001', '-c:v', 'libx264', '-preset', 'medium', '-crf', crf,
            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', rv])
        vd = float(sh([FP, '-v', 'error', '-select_streams', 'v', '-show_entries', 'stream=duration', '-of', 'csv=p=0', rv]).strip().split('\n')[0])
        ad = float(sh([FP, '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=duration', '-of', 'csv=p=0', rv]).strip().split('\n')[0])
        sh([FF, '-v', 'error', '-y', '-i', rv, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', '/tmp/_rv.wav'])
        x = np.frombuffer(wave.open('/tmp/_rv.wav').readframes(10**9), dtype='<i2').astype(np.float32)/32768
        sec = [20*np.log10(np.sqrt((x[i*16000:(i+1)*16000]**2).mean())+1e-12) for i in range(int(len(x)//16000))]
        silent = sum(1 for v in sec if v < -50)
        print(f'  {tag}: video {vd:.3f}s audio {ad:.3f}s silent seconds {silent} quietest {min(sec):.1f} dBFS')
        assert abs(vd-ad) < 0.15 and silent == 0, 'REVIEW COPY AUDIO INTEGRITY FAILED'
rec = os.path.join(DEST, 'recipe-vertical'); os.makedirs(rec, exist_ok=True)
for f in ['beats.py', 'g5.py', 'render5.py', 'captions.py', 'align_ctc.py', 'caption_sync_check.py', 'zmux.py', 'zalign.py', 'zprofile2.py',
          'zfit.py', 'zfit_right.py', 'zpic2.py', 'zedl.py', 'zedl3.py', 'zlut.py', 'zvig.py', 'zbase.py', 'zmeasure.py', 'zhair.py', 'zcrop.py',
          'zhairgate2.py', 'zassets5.py', 'zmatch5.py', 'zcutdown.py', 'zcut_build.py', 'watch.py', 'landing_check.py', 'centering.py',
          'deliver5.py', 'edl_picture.json', 'crop.json', 'fit.json', 'offset_profile.json', 'vignette.json', 'his.cube', 'cut_plan.json',
          'qc.json', 'words_ctc.json', 'media_map.json', 'logs/watch_pass.json', 'logs/hairgate2.json', 'logs/qc_master.log', 'logs/qc_cut.log',
          'cut/logs/watch_pass.json', 'notes.md']:
    if os.path.exists(f):
        out = os.path.join(rec, f.replace('/', '__')); shutil.copyfile(f, out)
shutil.copyfile('notes.md', os.path.join(DEST, 'notes-vertical.md'))
print('delivered to', DEST); print('\n'.join(sorted(os.listdir(DEST))))
