#!/usr/bin/env python3
"""0:59 shorts-ad cutdown, built by INTERVAL SELECTION over the finished vertical master.

Selecting from the approved master (rather than re-cutting from source) carries every
decision through unchanged -- take choice, grade, graphics, framing. Only the caption
timing, the music bed and the SFX are rebuilt, because those are the three things that
cannot survive having time removed from under them.

Content follows Dan's settled shorts-ad doctrine: sell the GENERATION almost exclusively,
give the trainer/nutritionist exactly one beat near the end, and say the CTA twice.
"""
import json, os, subprocess, sys
sys.path.insert(0, '.')
import beats as BT, captions as CAP
FF = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
FPS = 30000/1001
at, end = BT.at, BT.end

RANGES = [
 (0.0,                                            end('and its not even real')),
 (at('i generated this picture'),                 end('when i was 200 pounds')),
 (at('i made it my phone lock screen'),           end('and this is where im at today')),
 (at('with ai you can create a picture'),          end('youve always wanted')),
 (at('and once you see yourself with abs'),        end('everything changes')),
 (at('and right now you can generate'),            end('to see yourself with abs')),
 (at('youre more attractive to women'),            end('you feel better')),
 (at('generating an image of yourself with abs is just'), end('helps you make it real')),
 (at('to start losing your belly fat'),            BT.DUR),
]

def snap(t, tol=0.30):
    """Pull a range edge onto the nearest beat boundary. A range that starts 80 ms inside
    a card shows that card already half-open, which reads as a dropped frame."""
    edges = sorted({0.0, BT.DUR} | {x for b in BT.timeline()[0] for x in (b['t0'], b['t1'])})
    n = min(edges, key=lambda e: abs(e-t))
    return n if abs(n-t) <= tol else t

def plan():
    out, t = [], 0.0
    for a, b in [(snap(a), snap(b)) for a, b in RANGES]:
        assert b > a, (a, b)
        out.append(dict(src0=a, src1=b, dst0=t, dst1=t+(b-a))); t += b-a
    return out, t

def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1200:]); raise SystemExit(1)

def main():
    P, dur = plan()
    print(f'{len(P)} ranges, total {dur:.2f}s')
    for p in P: print(f'   {p["src0"]:7.2f}-{p["src1"]:7.2f}  ({p["src1"]-p["src0"]:5.2f}s)')
    assert dur <= 59.0, f'CUTDOWN IS {dur:.2f}s -- Shorts ads must never exceed 0:59'
    os.makedirs('cut', exist_ok=True)
    # --- picture + voice -----------------------------------------------------
    prev = 0
    with open('cut/vlist.txt','w') as vf, open('cut/alist.txt','w') as af:
        for i, p in enumerate(P):
            cum = round(p['dst1']*FPS); n = cum-prev; prev = cum
            v, a = f'cut/v{i:02d}.mp4', f'cut/a{i:02d}.wav'
            if not os.path.exists(v):
                sh([FF,'-v','error','-y','-ss',f'{p["src0"]:.4f}','-i','picture.mp4',
                    '-frames:v',str(n),'-r','30000/1001','-c:v','libx264','-preset','medium',
                    '-crf','16','-pix_fmt','yuv420p','-an',v])
            if not os.path.exists(a):
                ns = int(round(n*48000*1001/30000))
                sh([FF,'-v','error','-y','-ss',f'{p["src0"]:.4f}','-i','voice_raw.wav',
                    '-af',f'atrim=end_sample={ns},asetpts=N/SR/TB','-ar','48000','-ac','1',
                    '-c:a','pcm_s16le',a])
            vf.write(f'file v{i:02d}.mp4\n'); af.write(f'file a{i:02d}.wav\n')
    sh([FF,'-v','error','-y','-f','concat','-safe','0','-i','cut/vlist.txt','-c','copy','cut/picture.mp4'])
    sh([FF,'-v','error','-y','-f','concat','-safe','0','-i','cut/alist.txt','-c','copy','cut/voice.wav'])
    # --- captions, re-timed --------------------------------------------------
    def m(t):
        for p in P:
            if p['src0'] <= t <= p['src1']: return p['dst0'] + (t-p['src0'])
        return None
    words = [(w, m(s), m(e)) for w, s, e in CAP.load_words()]
    words = [w for w in words if w[1] is not None and w[2] is not None]
    mute = [(m(a), m(b)) for a, b in CAP.suppressed()]
    mute = [x for x in mute if x[0] is not None and x[1] is not None]
    gs = CAP.groups(words, mute)
    CAP.render(gs, out='cut/captions.mov', capdir='cut/cap')
    # --- bed + sfx over the NEW duration -------------------------------------
    import build_audio as BA
    if os.path.exists('sfx.wav'): os.rename('sfx.wav', '_sfx_full.wav')
    BA.sfx_bed(dur); os.rename('sfx.wav', 'cut/sfx.wav')
    if os.path.exists('_sfx_full.wav'): os.rename('_sfx_full.wav', 'sfx.wav')
    errs = json.load(open('eq.json')); eq = BA.eq_chain(errs)
    voice = ('agate=threshold=0.010:ratio=3:attack=6:release=180,' + (eq+',' if eq else '') +
             'acompressor=threshold=0.10:ratio=3:attack=8:release=180:makeup=2,alimiter=limit=0.95')
    fc = (f'[0:a]{voice},aformat=channel_layouts=mono,asplit=2[v][vsc];'
          f'[1:a]aformat=channel_layouts=stereo,volume={BA.MUSIC_DB}dB,'
          f'afade=t=in:st=0:d=1.2,afade=t=out:st={dur-1.8:.2f}:d=1.6[mus];'
          f'[mus][vsc]sidechaincompress=threshold=0.030:ratio=7:attack=8:release=340[musd];'
          f'[2:a]volume=-3dB[sfx];[v][musd][sfx]amix=inputs=3:duration=first:normalize=0[mx];'
          f'[mx]loudnorm=I=-14:TP=-1.5:LRA=9[out]')
    sh([FF,'-v','error','-y','-i','cut/voice.wav','-stream_loop','-1','-i',BA.MUSIC,'-i','cut/sfx.wav',
        '-filter_complex',fc,'-map','[out]','-t',f'{dur:.4f}','-ar','48000','-ac','2',
        '-c:a','pcm_s24le','cut/audio.wav'])
    sh([FF,'-v','error','-y','-i','cut/picture.mp4','-i','cut/captions.mov','-i','cut/audio.wav',
        '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass[v]','-map','[v]','-map','2:a',
        '-r','30000/1001','-c:v','libx264','-preset','slow','-crf','17','-pix_fmt','yuv420p',
        '-profile:v','high','-level','4.2','-c:a','aac','-b:a','256k','-ar','48000','-ac','2',
        '-movflags','+faststart','ad1_vertical_59s.mp4'])
    print('ad1_vertical_59s.mp4 done', f'{dur:.2f}s')

if __name__ == '__main__':
    main()
