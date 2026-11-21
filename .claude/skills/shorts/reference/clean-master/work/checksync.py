#!/usr/bin/env python3
"""Transcribe a DELIVERED short and compare its word times to the burned captions.

This is the only test that measures what a viewer actually experiences. Everything upstream
(word timestamps, gaps, cut points) lives on the extracted-WAV timeline; the cuts and the
picture live on the MP4 container timeline. If those two disagree, it shows up here.
"""
import json, re, sys, wave
import numpy as np, whisper, subprocess
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
m = whisper.load_model('base.en')
for sid, f in (('E','out/e_stop-buying-a-big-supplement-stack.mp4'),
               ('C','out/c_if-you-take-one-take-fish-oil.mp4'),
               ('B','out/b_the-3-supplements-that-matter.mp4')):
    p = subprocess.run([FF,'-v','error','-i',f,'-vn','-ac','1','-ar','16000','-f','s16le','-'],
                       capture_output=True)
    x = np.frombuffer(p.stdout, dtype=np.int16).astype(np.float32)/32768.0
    r = m.transcribe(x, language='en', word_timestamps=True, verbose=False)
    words = [(w['word'].strip(), w['start']) for s in r['segments'] for w in s.get('words',[])]
    ass = [l for l in open(f'build/{sid}.ass') if l.startswith('Dialogue:')]
    def t(s):
        h,mm,rest = s.split(':'); return int(h)*3600+int(mm)*60+float(rest)
    cues = [(t(re.match(r'Dialogue: 0,([^,]+),', l).group(1)),
             l.rsplit(',,',1)[1].strip()) for l in ass]
    print(f"\n=== {sid} ===")
    print(f"  heard first : {' '.join(w for w,_ in words[:9])!r} @ {words[0][1]:.2f}s")
    print(f"  caption 1   : {cues[0][1]!r} @ {cues[0][0]:.2f}s")
    # align: for each of the first 6 cues, find the heard word matching its first token
    errs=[]
    for ct, txt in cues[:40]:
        first = re.sub(r'[^a-z0-9]','', txt.split()[0].lower())
        if not first: continue
        cands=[ws for w,ws in words if re.sub(r'[^a-z0-9]','',w.lower())==first]
        if not cands: continue
        near=min(cands, key=lambda s: abs(s-ct))
        if abs(near-ct) < 2.5: errs.append(near-ct)
    if errs:
        e=np.array(errs)
        print(f"  caption vs heard audio over {len(e)} cues: median {np.median(e)*1000:+.0f} ms, "
              f"mean {e.mean()*1000:+.0f} ms, sd {e.std()*1000:.0f} ms")
        print(f"    (positive = the audio says the word AFTER the caption appears, i.e. caption early)")
