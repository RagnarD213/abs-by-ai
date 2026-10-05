#!/bin/zsh
source "${0:A:h}/env.sh"
cd $Q
[ -n "$SKIP_PIC" ] || python3 "$KL/sq_render_ad10.py" picture --cut --build $B --out $Q 2>&1 | tail -1 || exit 1
python3 "$KL/sq_render_ad10.py" mux --cut --build $B --out $Q --vertical "$VC" --name "$T | claude | 1x1 59s | ad 10" | tail -1 || exit 1
[ "$SQC" -nt cut_picture.mp4 ] || { echo "MUX IS OLDER THAN THE PICTURE"; exit 1; }
python3 "$A" "$SQC" --reference-mix $B/cut/his_mix.wav --verbatim 2>&1 | tail -1
rm -rf cut_audit/watch cut_audit/negscan cut_audit/logs; rm -f cut_audit/gate_pre.json
python3 "$KL/sq_plan_ad10.py" --cut --build $B --out $Q --video "$SQC" --vertical "$VC" && cd cut_audit && python3 "$D/watch.py" "$SQC" --plan plan.json --out watch --log logs/watch_pass.json > /dev/null 2>&1 && python3 "$K/kit_negscan.py" sheet --build $Q/cut_audit --video "$SQC" | tail -1
python3 "$D/gate.py" "$SQC" --format ad1x1 --plan plan.json --json gate_pre.json > gate_pre.log 2>&1
python3 -c "
import json;g=json.load(open('gate_pre.json'));print('SQCUT',g['verdict']);[print(' ',r['key'],str(r.get('detail',''))[:260]) for r in g['rows'] if r.get('ok') is not True]"
echo SQCUT DONE
