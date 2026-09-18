#!/bin/bash
# ROUND 2, final pass: the caption fix (no blank between lines), both pictures re-rendered from the
# EXISTING Dan segments (the crops and the grade did not change, so stage 1 is skipped), the mix
# locked to the picture, both masters re-muxed, and every piece of delivered evidence remade.
set -e
cd /Volumes/Extreme/_edit_work/ra01
AG="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/audio_gate.py"
python3 s07_captions.py 9x16
python3 s07_captions.py 16x9
SKIP1=1 python3 s10_render.py 9x16
SKIP1=1 python3 s10_render.py 16x9
cp -p mix.wav r2/mix_before_lock.wav
LOCK=picture_9x16.mp4 BED=music/Realizer.mp3 BED_DB=-32 python3 s08_audio.py
python3 - <<'PY'
import wave, numpy as np
def rd(p):
    w=wave.open(p); a=np.frombuffer(w.readframes(w.getnframes()),np.int16); return a.reshape(-1,w.getnchannels())
a=rd('r2/mix_before_lock.wav'); b=rd('mix.wav')
n=min(len(a),len(b),int(55.0*48000))
d=np.abs(a[:n].astype(np.int32)-b[:n].astype(np.int32))
print(f"MIXCHECK first {n/48000:.1f}s: max sample delta {int(d.max())}  identical={bool(d.max()==0)}")
print(f"MIXCHECK old {len(a)/48000:.6f}s  new {len(b)/48000:.6f}s")
PY
for K in 9x16 16x9; do
  python3 s14_deliver.py mux $K | tail -3
  if [ "$K" = "9x16" ]; then python3 "$AG" master_$K.mp4 --ab AB_ref-vs-ours.mp4 || true
  else python3 "$AG" master_$K.mp4 || true; fi
  python3 s15_txmaster.py $K master_$K.mp4 | head -1
  python3 s09_align.py master_$K.mp4 speech_$K.json | tail -1
  python3 s13_watch.py neg $K master_$K.mp4 | tail -1
done
echo FINALPASS_DONE
