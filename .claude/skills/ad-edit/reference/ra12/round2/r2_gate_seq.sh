#!/bin/bash
# RA-12 round 2: master -> per-file measurements -> chips/phone rects. Then (by hand) neg scan, gate plan, watch pass + judge, gate.
cd /Volumes/Expansion/_edit_work/ra12
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
M="deliver_r2/the first step to getting abs isnt a workout | claude | 9x16 | RA-12 R2.mp4"
set -e
rm -rf deliver_r2/logs deliver_r2/watch; rm -f "$M" "$M".*.json
ffmpeg -nostdin -y -v error -i round2/work/picture_9x16.mp4 -i mix_bass_r1.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart "$M"
python3 "$SH/audio/audio_gate.py" "$M" --untreated mix_fit_b1.5.wav.audio_untreated.json --ab "deliver_r2/the first step to getting abs isnt a workout | AB audio ref-vs-ours 9x16 | RA-12 R2.mp4" > round2/logs/g_agate.log 2>&1 || true
python3 r2_s88_checks.py > round2/logs/g_s88.log 2>&1
python3 s09_align.py "$M" round2/gate/speech_9x16.json > round2/logs/g_align.log 2>&1
ffmpeg -nostdin -v error -y -i "$M" -vn -ac 1 -b:a 96k round2/gate/master.mp3
node "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference/replicate_words.js" round2/gate/master.mp3 0 round2/gate/tx_master.json > round2/logs/g_tx.log 2>&1
python3 - <<'PY'
import json
d=json.load(open('round2/gate/tx_master.json'))['segments'][0]['words']; out=[]; drop=[]
for i,x in enumerate(d):
    nx=d[i+1] if i+1<len(d) else None
    if nx and abs(nx['start']-x['start'])<0.05 and nx['word'].strip().lower().startswith(x['word'].strip().lower()) and x['word'].strip()!=nx['word'].strip():
        drop.append((x['word'],x['start'])); continue
    out.append(x['word'].strip())
json.dump({'words':out,'text':' '.join(out),'source':'replicate large-v3 on the delivered master','dropped_asr_duplicates':drop},open('round2/gate/transcript_9x16.json','w'),indent=1)
print('tx', len(out), 'dropped', drop)
PY
python3 "$SH/cut/junk.py" "$M" --out round2/gate/junk_9x16.json > round2/logs/g_junk.log 2>&1
ffmpeg -nostdin -v error -y -i "$M" -vf "fps=1,scale=216:384,tile=12x4" -frames:v 1 round2/gate/neg_sheet.jpg
python3 r2_s92_chips.py > round2/logs/g_chips.log 2>&1
python3 r2_s94_phonebox.py > round2/logs/g_phone.log 2>&1
echo "MASTER_READY $(shasum -a 256 "$M" | cut -c1-12)"
