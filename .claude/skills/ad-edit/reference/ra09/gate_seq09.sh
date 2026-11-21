#!/bin/bash
# RA-09 round 1: master -> per-file measurements -> chips/phone rects. Then (by hand) neg scan, gate plan, watch pass + judge, gate.
cd /Volumes/Expansion/_edit_work/RA-09
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
SH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
M="deliver_r1/do you think ai is changing the world | claude | 9x16 | RA-09 R1.mp4"
set -e
mkdir -p deliver_r1 r1/gate r1/logs; rm -rf deliver_r1/logs deliver_r1/watch; rm -f "$M" "$M".*.json
ffmpeg -nostdin -y -v error -i r1/work/picture_9x16.mp4 -i mix_r1.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -movflags +faststart "$M"
python3 "$SH/audio/audio_gate.py" "$M" --untreated mix_b15.wav.audio_untreated.json --ab "deliver_r1/do you think ai is changing the world | AB audio ref-vs-ours 9x16 | RA-09 R1.mp4" > r1/logs/g_agate.log 2>&1 || true
python3 r1_s88_checks.py > r1/logs/g_s88.log 2>&1
python3 s09_align.py "$M" r1/gate/speech_9x16.json > r1/logs/g_align.log 2>&1
ffmpeg -nostdin -v error -y -i "$M" -vn -ac 1 -b:a 96k r1/gate/master.mp3
node "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/ad-edit/reference/replicate_words.js" r1/gate/master.mp3 0 r1/gate/tx_master.json > r1/logs/g_tx.log 2>&1
python3 - <<'PY'
import json
d=json.load(open('r1/gate/tx_master.json'))['segments'][0]['words']; out=[]; drop=[]
for i,x in enumerate(d):
    nx=d[i+1] if i+1<len(d) else None
    if nx and abs(nx['start']-x['start'])<0.05 and nx['word'].strip().lower().startswith(x['word'].strip().lower()) and x['word'].strip()!=nx['word'].strip():
        drop.append((x['word'],x['start'])); continue
    out.append(x['word'].strip())
json.dump({'words':out,'text':' '.join(out),'source':'replicate large-v3 on the delivered master','dropped_asr_duplicates':drop},open('r1/gate/transcript_9x16.json','w'),indent=1)
print('tx', len(out), 'dropped', drop)
PY
python3 "$SH/cut/junk.py" "$M" --out r1/gate/junk_9x16.json > r1/logs/g_junk.log 2>&1
ffmpeg -nostdin -v error -y -i "$M" -vf "fps=1,scale=216:384,tile=12x4" -frames:v 1 r1/gate/neg_sheet.jpg
python3 r1_chips.py > r1/logs/g_chips.log 2>&1
python3 r1_s94_phonebox.py > r1/logs/g_phone.log 2>&1
echo "MASTER_READY $(shasum -a 256 "$M" | cut -c1-12)"
cp "$M" "/Users/danielrose/Documents/Claude/Projects/Abs By AI/Videos to Review/Do You Think AI Is Changing The World AD R1 - whole ad 9x16.mp4"
echo "VLC_COPIED"
