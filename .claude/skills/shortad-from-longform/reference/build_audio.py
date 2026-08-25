#!/usr/bin/env python3
"""Voice + music bed + SFX for the 9:16 cut.

VOICE IS THE RIGHT CHANNEL ONLY, AS MONO. C1591 is not a stereo recording: it carries two
different microphones ~7.8 ms apart with the far one polarity-inverted. Summing them is a
comb filter no EQ can undo. Right = the lav.

The voice is then EQ-fitted to MUHAMMAD'S FINISHED MIX, band by band -- his cut is the
reference Dan approved, so the target is his voice, not a generic curve.
"""
import json, os, subprocess, sys, wave
import numpy as np
sys.path.insert(0, '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared')
import sfxlib
import beats as BT

FF  = "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
SRC = "/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/C1591.MP4"
HIS = "/private/tmp/claude-501/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/a678794d-8af3-46ab-b2f9-4d2420a9b104/scratchpad/vertad/muhammad_v3.mp4"
MUSIC = "/Volumes/Extreme/_edit_work/ad1-8-14/rev5/music/acoustic_bg.mp3"
FPS = 30000/1001; SR = 48000
BANDS = [(80,150),(150,250),(250,400),(400,700),(700,1200),(1200,2000),
         (2000,3200),(3200,5000),(5000,8000),(8000,10500)]
MUSIC_DB = -21.0

def sh(c):
    r = subprocess.run(c, capture_output=True, text=True)
    if r.returncode: print(r.stderr[-1200:]); raise SystemExit(1)
    return r

# ---------------------------------------------------------------- 1. conform voice
def conform():
    if os.path.exists('voice_raw.wav'): return
    S = json.load(open('edl_frames.json'))
    os.makedirs('aud', exist_ok=True)
    with open('aud/list.txt','w') as f:
        for s in S:
            o = f'aud/a{s["i"]:03d}.wav'
            n = int(round(s['frames']*SR*1001/30000))
            if not os.path.exists(o):
                sh([FF,'-v','error','-y','-ss',f'{s["src_in"]:.4f}','-i',SRC,
                    '-af',f'pan=mono|c0=c1,atrim=end_sample={n},asetpts=N/SR/TB',
                    '-ar',str(SR),'-ac','1','-c:a','pcm_s16le',o])
            f.write(f"file a{s['i']:03d}.wav\n")
    sh([FF,'-v','error','-y','-f','concat','-safe','0','-i','aud/list.txt','-c','copy','voice_raw.wav'])

# ---------------------------------------------------------------- 2. fit EQ to his voice
def spec_of(path, af, wins):
    parts=[]
    for i,(ss,d) in enumerate(wins):
        p=f'_s{i}.wav'
        sh([FF,'-v','error','-y','-ss',str(ss),'-t',str(d),'-i',path,'-af',af,
            '-ac','1','-ar','22050','-c:a','pcm_s16le',p]); parts.append(p)
    a=np.concatenate([np.frombuffer(wave.open(p).readframes(10**9),dtype='<i2').astype(float)/32768 for p in parts])
    N=2048; fr=np.array([a[i:i+N]*np.hanning(N) for i in range(0,len(a)-N,512)])
    S=np.abs(np.fft.rfft(fr,axis=1)); f=np.fft.rfftfreq(N,1/22050)
    rms=np.sqrt((fr**2).mean(1)); keep=rms>np.percentile(rms,55)
    m=S[keep].mean(0)+1e-12
    return f, 20*np.log10(m/m.sum()*len(m))

WINS = [(30.0,4),(60.0,4),(95.0,4),(145.0,4),(200.0,4)]
def fit_eq():
    if os.path.exists('eq.json'): return json.load(open('eq.json'))
    F, H = spec_of(HIS, 'pan=mono|c0=0.5*c0+0.5*c1', WINS)
    _, O = spec_of('voice_raw.wav', 'anull', WINS)
    errs = [float(H[(F>=lo)&(F<hi)].mean() - O[(F>=lo)&(F<hi)].mean()) for lo,hi in BANDS]
    json.dump(errs, open('eq.json','w'))
    print('band error before fit (his - ours), dB:', ' '.join(f'{e:+.1f}' for e in errs))
    return errs

def eq_chain(errs):
    out=[]
    for (lo,hi),g in zip(BANDS, errs):
        fc=(lo*hi)**0.5; w=hi/lo
        g=max(-9.0, min(6.0, g))   # capping the top: the raw fit wants +8.8 dB at 9 kHz, which lifts lav hiss with the air
        if abs(g) < 0.35: continue
        out.append(f'equalizer=f={fc:.0f}:t=q:w={1.6/np.log2(w):.2f}:g={g:.2f}')
    return ','.join(out)

# ---------------------------------------------------------------- 3. SFX bed
def sfx_bed(dur):
    if os.path.exists('sfx.wav'): return
    tl, ov = BT.timeline()
    y = np.zeros(int(dur*SR)+SR, dtype=np.float32)
    def put(t, s, g):
        i=int(t*SR)
        if i<0 or i>=len(y): return
        n=min(len(s), len(y)-i); y[i:i+n]+=s[:n].astype(np.float32)*g
    wh   = sfxlib.whoosh(0.42); who = sfxlib.whoosh(0.34, f0=2600, f1=500, f2=380)
    sub  = sfxlib.sub_drop(0.55); pop = sfxlib.pop(); ris = sfxlib.riser(0.9)
    for b in tl:
        if b['kind'] == 'talk': continue
        put(b['t0']-0.06, wh, 0.30)
        put(b['t1']-0.20, who, 0.20)
        if b['kind'] in ('window','title','statement'):
            put(b['t0']-0.06, sub, 0.22)
        if b['kind'] == 'title':
            put(b['t0']-0.75, ris, 0.20)
        if b['kind'] == 'window':
            for n in range(len(b['bullets'])):
                put(b['t0']+0.35+n*0.55, pop, 0.16)
    for b in ov:
        put(b['t0']-0.05, wh, 0.26)
    sfxlib.save('sfx.wav', y[:int(dur*SR)], stereo=False)

# ---------------------------------------------------------------- 4. mix
def main():
    conform()
    dur = json.load(open('edl_frames.json'))
    dur = sum(s['frames'] for s in dur)/FPS
    errs = fit_eq(); eq = eq_chain(errs)
    print('EQ:', eq or '(flat)')
    sfx_bed(dur)
    voice = ('agate=threshold=0.010:ratio=3:attack=6:release=180,' + (eq+',' if eq else '') +
             'acompressor=threshold=0.10:ratio=3:attack=8:release=180:makeup=2,'
             'alimiter=limit=0.95')
    fc = (f'[0:a]{voice},aformat=channel_layouts=mono,asplit=2[v][vsc];'
          f'[1:a]aformat=channel_layouts=stereo,volume={MUSIC_DB}dB,'
          f'afade=t=in:st=0:d=1.6,afade=t=out:st={dur-2.2:.2f}:d=2.0[mus];'
          f'[mus][vsc]sidechaincompress=threshold=0.030:ratio=7:attack=8:release=340[musd];'
          f'[2:a]volume=-3dB[sfx];'
          f'[v][musd][sfx]amix=inputs=3:duration=first:normalize=0[mx];'
          f'[mx]loudnorm=I=-14:TP=-1.5:LRA=9[out]')
    sh([FF,'-v','error','-y','-i','voice_raw.wav','-stream_loop','-1','-i',MUSIC,'-i','sfx.wav',
        '-filter_complex',fc,'-map','[out]','-t',f'{dur:.4f}',
        '-ar',str(SR),'-ac','2','-c:a','pcm_s24le','audio.wav'])
    r = subprocess.run([FF,'-nostats','-hide_banner','-i','audio.wav','-af',
                        'loudnorm=print_format=summary','-f','null','-'],
                       capture_output=True, text=True).stderr
    print('\n'.join(l for l in r.split('\n') if 'Input' in l))

if __name__ == '__main__':
    main()
