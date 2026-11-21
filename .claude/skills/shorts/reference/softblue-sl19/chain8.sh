#!/bin/zsh
cd /Volumes/Extreme/_edit_work/SL-19; export GATE_GROUP=SL-19
log(){ echo "$(date +%H:%M:%S) $*" >> chain.log; }
log "chain8 start (C A D review fixes)"
python3 batch.py audio C D > logs_audio8.txt 2>&1 && python3 batch.py words C D > logs_words8.txt 2>&1 && python3 batch.py plan C A D > logs_plan8.txt 2>&1 && python3 batch.py track C D > logs_track8.txt 2>&1 && python3 batch.py plan C A D > logs_plan8b.txt 2>&1 && python3 cues.py C A D >> logs_plan8b.txt 2>&1 || { log "prep failed"; exit 1; }
python3 batch.py gfx C A D > logs_gfx8.txt 2>&1 && python3 batch.py proof C A D > logs_proof8.txt 2>&1 && python3 batch.py render C A D > logs_render8.txt 2>&1 || { log "render failed"; exit 1; }; log "render done"
python3 deliver.py copy C A D > logs_deliver8.txt 2>&1 || { log "deliver failed"; exit 1; }; log "deliver done"
./runwatch.sh C; ./runwatch.sh A; ./runwatch.sh D; log "watch done"
python3 haircheck.py C A D > logs_hair8.txt 2>&1; log "hair done"
log ALLDONE8
