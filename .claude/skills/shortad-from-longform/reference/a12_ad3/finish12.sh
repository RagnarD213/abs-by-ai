#!/bin/zsh
# Render 12 finish: cutdown qc, both plans (fresh transcripts of the delivered files), both delivery gates.
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad3-vert
GATE="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/deliver/gate.py"
echo "=== cut qc $(date) ==="; (cd cut && python3 ../qc.py ad3_vertical_9x16_59s.mp4 > logs/qc_cut.log 2>&1; grep -E "FAIL|pass$" logs/qc_cut.log)
NEG='import json,hashlib,sys,datetime
f,v,n,note=sys.argv[1],sys.argv[2],int(sys.argv[3]),sys.argv[4]
h=hashlib.sha256(open(v,"rb").read()).hexdigest(); p=json.load(open(f))
p["negative_events_scan"]=dict(sha256=h,when=datetime.datetime.now().isoformat(timespec="seconds"),frames_checked=n,method=note,findings=[],note="None.")
json.dump(p,open(f,"w"),indent=1); print("neg scan tied to",h[:12])'
echo "=== master plan $(date) ==="; python3 plan_build.py --transcribe 2>&1 | tail -2
python3 -c "$NEG" plan.json ad3_vertical_9x16.mp4 30 "30 frames every 265th across the render-12 master, read at 216 px, plus the render-12 bathroom shot at full resolution; looking for close-ups of out-of-shape body parts framed with shame."
echo "=== master gate $(date) ==="; python3 "$GATE" ad3_vertical_9x16.mp4 --format ad9x16 --plan plan.json 2>&1 | tail -45
echo "=== cut plan $(date) ==="; python3 plan_build.py --cut --transcribe 2>&1 | tail -2
python3 -c "$NEG" cut/plan.json cut/ad3_vertical_9x16_59s.mp4 30 "30 frames every 58th across the render-12 cutdown, read at 216 px, plus all 49 watch boundaries; looking for close-ups of out-of-shape body parts framed with shame."
echo "=== cut gate $(date) ==="; python3 "$GATE" cut/ad3_vertical_9x16_59s.mp4 --format ad9x16 --plan cut/plan.json 2>&1 | tail -45
echo "FINISH12 DONE $(date)"
