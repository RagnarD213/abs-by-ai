#!/bin/zsh
# SL-18 round 1c: every reviewer fix (B: pause, graph title + lead, ending, captions; D: "rich" patch, one-frame flash, stacked-clip captions, cuts in gaps, phone speed, framing, key point, pauses)
cd /Volumes/Expansion/_edit_work/SL-18
rm -rf graph/proj
python3 "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/worktrees/reverent-cohen-1d87c9/.claude/skills/_shared/hyperframes/line-graph/build.py" graph/B_graph.json graph/proj --render > graph/render3.log 2>&1 || { echo GRAPH_FAIL > chain_r1c.done; exit 1; }
python3 sl18batch.py audio B D > logs_audio3.txt 2>&1 && python3 patch_audio.py D >> logs_audio3.txt 2>&1 || { echo AUDIO_FAIL > chain_r1c.done; exit 1; }
python3 sl18batch.py words B D > logs_words3.txt 2>&1 && python3 sl18batch.py plan B D > logs_plan3.txt 2>&1 && python3 sl18batch.py track B D > logs_track3.txt 2>&1 && python3 sl18batch.py plan B D >> logs_plan3.txt 2>&1 && python3 sl18batch.py words B D >> logs_words3.txt 2>&1 || { echo PLAN_FAIL > chain_r1c.done; exit 1; }
python3 sl18batch.py gfx B D > logs_gfx3.txt 2>&1 || { echo GFX_FAIL > chain_r1c.done; exit 1; }
python3 sl18batch.py proof B D > logs_proof3.txt 2>&1
python3 sl18batch.py render B D > logs_render3.txt 2>&1 || { echo RENDER_FAIL > chain_r1c.done; exit 1; }
python3 deliver.py copy B D > logs_deliver3.txt 2>&1 || { echo DELIVER_FAIL > chain_r1c.done; exit 1; }
./runwatch.sh B; ./runwatch.sh D
python3 haircheck_v.py B > logs_hairB3.txt 2>&1; python3 haircheck_v.py D > logs_hairD3.txt 2>&1
echo DONE > chain_r1c.done
