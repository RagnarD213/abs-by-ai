#!/usr/bin/env python3
"""Deliver the Ad 1 SQUARE (full length + the <=0:59) beside the approved vertical, under the
editor-deliveries convention (`title | editor | aspect | number`, lowercase, single-spaced pipes).

Runs only after qc.py has passed on both work-dir masters. Copies are md5-verified; the audio
gate re-runs on the DELIVERED files in verbatim mode (stamp beside each); review copies are made
and their audio integrity is checked, because a re-encode inherits a broken master.
"""
import hashlib, os, shutil, subprocess, sys, json, wave
# PER-PROCESS TEMP FILE (skill A9.7): this script staged its review-copy decode at a
# FIXED path under /tmp. Two deliveries running at once would have measured each
# other's audio -- and a green row that measured the wrong file is what ships a defect.
import atexit, shutil as _sh, tempfile
_TMP = tempfile.mkdtemp(prefix='deliversq_')
atexit.register(_sh.rmtree, _TMP, True)
_RV = os.path.join(_TMP, 'rv.wav')
import numpy as np

FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FP = FF.replace('ffmpeg', 'ffprobe')
AUD = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio"
DEST = ("/Users/danielrose/Documents/Claude/Projects/Abs By AI/Muhammad Ad Videos/"
        "this picture got me abs - ad 1")
T = "this picture got me abs"
FILES = [  # (work file, delivered name, the mix the verbatim gate measures against)
    ('ad1_square_1x1.mp4',  f"{T} | claude | 1x1 | ad 1.mp4",     'his_mix.wav'),
    ('ad1_square_59s.mp4',  f"{T} | claude | 1x1 59s | ad 1.mp4", 'cut/his_mix.wav'),
]

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''): h.update(c)
    return h.hexdigest()

def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: raise SystemExit(' '.join(str(x) for x in c[:30]) + '\n' + r.stderr[-2000:])
    return r.stdout

def main():
    os.makedirs(DEST, exist_ok=True)
    for src, name, mix in FILES:
        assert os.path.exists(src), f'missing {src}'
        dst = os.path.join(DEST, name)
        shutil.copyfile(src, dst)
        assert md5(src) == md5(dst), 'md5 mismatch after copy'
        print('copied', name, 'md5', md5(dst))
        ab = os.path.join(DEST, name.replace('| claude |', '| AB audio approved-vertical-vs-square |'))
        r = subprocess.run(['python3', f'{AUD}/audio_gate.py', dst, '--reference-mix', mix,
                            '--verbatim', '--ab', ab], capture_output=True, text=True)
        print(r.stdout[-900:])
        if r.returncode:
            raise SystemExit('AUDIO GATE FAILED ON THE DELIVERED FILE ' + name)
        print(sh(['python3', f'{AUD}/require_stamp.py', dst]))
        # ⚠ THE DELIVERY-GATE STAMP TRAVELS WITH THE FILE (audit 3, 2026-09-12). The gate is run
        # from inside cut/ for the cutdown, so its sidecar sits beside THAT copy while the file that
        # actually ships is the build root's. A stamp that is not beside the delivered bytes is a
        # stamp nobody can check; `_shared/deliver/gate.py --check` looks for it next to the file.
        import glob as _g
        cand = [src + '.deliver_gate.json', os.path.join('cut', os.path.basename(src) + '.deliver_gate.json')]
        st = next((c for c in cand if os.path.exists(c)), None)
        assert st, f'NO DELIVERY GATE STAMP for {src} -- run _shared/deliver/gate.py --format ad1x1'
        g = json.load(open(st))
        assert g.get('verdict') == 'PASS', f'{src}: delivery gate stamp says {g.get("verdict")}'
        shutil.copyfile(st, dst + '.deliver_gate.json')
        if os.path.abspath(st) != os.path.abspath(src + '.deliver_gate.json'):
            shutil.copyfile(st, src + '.deliver_gate.json')
        print(f'  delivery gate {g["gate_version"]} {g["verdict"]} ({g.get("format")}) -> stamp delivered')
        for tag, vf, crf in (('REVIEW 540p 1x1', 'scale=540:540:flags=lanczos', '23'),
                             ('REVIEW 480p 1x1 phone', 'scale=480:480:flags=lanczos', '26')):
            rv = os.path.join(DEST, name.replace('| claude |', f'| {tag} |'))
            sh([FF, '-nostdin', '-v', 'error', '-y', '-i', dst, '-vf', vf, '-r', '30000/1001',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-pix_fmt', 'yuv420p',
                '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', rv])
            vd = float(sh([FP, '-v', 'error', '-select_streams', 'v', '-show_entries',
                           'stream=duration', '-of', 'csv=p=0', rv]).strip().split('\n')[0])
            ad = float(sh([FP, '-v', 'error', '-select_streams', 'a', '-show_entries',
                           'stream=duration', '-of', 'csv=p=0', rv]).strip().split('\n')[0])
            sh([FF, '-v', 'error', '-y', '-i', rv, '-vn', '-ac', '1', '-ar', '16000',
                '-c:a', 'pcm_s16le', _RV])
            x = np.frombuffer(wave.open(_RV).readframes(10**9), dtype='<i2').astype(np.float32)/32768
            sec = [20*np.log10(np.sqrt((x[i*16000:(i+1)*16000]**2).mean())+1e-12)
                   for i in range(int(len(x)//16000))]
            silent = sum(1 for v in sec if v < -50)
            print(f'  {tag}: video {vd:.3f}s audio {ad:.3f}s silent seconds {silent} '
                  f'quietest {min(sec):.1f} dBFS')
            assert abs(vd-ad) < 0.20 and silent == 0, 'REVIEW COPY AUDIO INTEGRITY FAILED'

    rec = os.path.join(DEST, 'recipe-square'); os.makedirs(rec, exist_ok=True)
    for f in ['sqlib.py', 'sqassets.py', 'render.py', 'captions.py', 'align_ctc.py',
              'caption_sync_check.py', 'sqmux.py', 'sqcutdown.py', 'beats.py', 'assets.py',
              'grade.py', 'watch.py', 'watch_mark.py', 'sqhairgate.py', 'sqlanding.py',
              'centering.py', 'jumpcuts.py', 'chain_final.sh', 'deliver_sq.py',
              'qc.json', 'cut_plan.json', 'words_ctc.json', 'cx_track.json',
              'edl_frames.json', 'logs/watch_pass.json', 'logs/hairgate.json',
              'logs/centering.json', 'logs/landing.json', 'logs/jumpcuts.json',
              'logs/capsync.log', 'logs/qc_master.log', 'logs/qc_cut.log',
              'logs/render_sq.log', 'logs/chain_final.log',
              'cut/logs/watch_pass.json', 'cut/qc.json', 'notes-square.md',
              'chain_cut3.sh', 'chain_final2.sh', 'cut_edl.py', 'plan_sq.py', 'plan.json',
              'cut/plan.json', 'sqcut_build.py', 'cut/edl_frames.json',
              'logs/chain_cut3.log', 'logs/chain_final2.log', 'logs/cutdown2.log',
              'ad1_square_1x1.mp4.deliver_gate.json', 'ad1_square_59s.mp4.deliver_gate.json']:
        if os.path.exists(f):
            shutil.copyfile(f, os.path.join(rec, f.replace('/', '__')))
    if os.path.exists('notes-square.md'):
        shutil.copyfile('notes-square.md', os.path.join(DEST, 'notes-square.md'))
    print('\ndelivered to', DEST)
    for n in sorted(os.listdir(DEST)): print('  ', n)


if __name__ == '__main__':
    main()
