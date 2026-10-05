#!/bin/zsh
# square full: MUX FIRST, then audio gate, plan, watch, negscan, gate (never gate a file muxed from an older picture)
source "${0:A:h}/env.sh"
cd $Q || exit 1
rm -rf watch negscan; find logs -maxdepth 1 -type f \( -name 'findings_part*.json' -o -name 'rejudge*.json' -o -name 'negscan_findings.json' -o -name 'watch_pass.json' \) -delete 2>/dev/null; mkdir -p logs; rm -f gate_pre.json
python3 "$KL/sq_render_ad10.py" mux --build $B --out $Q --vertical "$V" --name "$T | claude | 1x1 | ad 10" | tail -1 || exit 1
[ "$SQV" -nt picture.mp4 ] || { echo "MUX IS OLDER THAN THE PICTURE"; exit 1; }
python3 "$A" "$SQV" --reference-mix $B/his_mix.wav --verbatim 2>&1 | tail -1
python3 "$KL/sq_plan_ad10.py" --build $B --out $Q --video "$SQV" --vertical "$V" || exit 1
python3 - <<'PY'
# the vertical's cue "years younger." runs 5 frames into the square's phone card (the square cuts to the card at 172.506, the
# vertical's card grid 10 frames later); the square does not draw those 5 frames of it (sq_copy mute_caption_frames), so its cue
# ends at the cut: a copy of the srt with that one end time, named in the square's plan
import json, re, os
Q = os.path.expanduser("~/abs-review/as06-ad10/sq"); p = json.load(open(Q + "/plan.json")); src = p["srt"]
t = open(src).read().replace("00:02:51,776 --> 00:02:52,689", "00:02:51,776 --> 00:02:52,500")
dst = Q + "/captions_square.srt"; open(dst, "w").write(t); p["srt"] = dst
json.dump(p, open(Q + "/plan.json", "w"), indent=1); print("srt ->", dst)
PY
python3 "$D/watch.py" "$SQV" --plan plan.json --out watch --log logs/watch_pass.json > /dev/null 2>&1 || exit 1
python3 "$K/kit_negscan.py" sheet --build $Q --video "$SQV" | tail -1
python3 "$D/gate.py" "$SQV" --format ad1x1 --plan plan.json --json gate_pre.json > gate_pre.log 2>&1
python3 -c "
import json;g=json.load(open('gate_pre.json'));print('SQFULL',g['verdict']);[print(' ',r['key'],str(r.get('detail',''))[:260]) for r in g['rows'] if r.get('ok') is not True]"
echo SQFULL DONE
