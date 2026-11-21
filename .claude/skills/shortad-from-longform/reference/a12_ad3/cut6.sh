#!/bin/zsh
# The cutdown, re-SELECTED (render 9). The r8 plan said the CTA twice -- "tap the button below ... stubborn stomach
# fat" AND "so generate your future self ..." -- 19.0 s of a 57 s ad (33 %) on a talking head repeating one
# instruction. It measured 44.5 % insert coverage against the 55 % bound and HIS OWN 62.2 %. Fixed in the SELECTION,
# never the bound: the first CTA is dropped, the walkthrough runs on through the motivation phonecard, and the
# AI-trainer-at-every-workout beat takes its place. 57.92 s, 63.0 % coverage, one CTA and it is at the end.
# cut/ is a forked build dir (its own beats.py, g3.py, g5.py, embedded phonecard time map), so a master fix does NOT
# reach it -- regenerate from the fixed master beats and refresh the graphics forks. (memory: shared-fix-may-not-reach-the-pipeline)
export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH"
cd /Volumes/Extreme/_edit_work/ad3-vert
while true; do n=$(for p in $(pgrep -f "whisper|ffmpeg|render|zbase|scan.py"); do lsof -a -p $p -d cwd -Fn 2>/dev/null | grep ^n | cut -c2-; done | grep -v ad3-vert | grep -E "_edit_work|Abs By AI" | sort -u | wc -l); [ $n -lt 2 ] && break; echo "waiting: $n other builds"; sleep 30; done
echo "cut6 start $(date)"
python3 zcutdown3.py --short > logs/cutplan6.log 2>&1 && tail -3 logs/cutplan6.log || { echo CUTPLAN FAILED; tail -6 logs/cutplan6.log; exit 1; }
# ⚠ The SHARED caption files go in on every rebuild. This build carried a caption_sync_check.py that was 89 lines
# against the skill's 175 (missing the per-process temp files, the CAP_Y derivation, the in-span sampling and the
# least-washed-frame retry) and a captions.py whose trailing concat entry RE-SHOWED the last caption state --
# the defect that printed a caption across the closing CTA pill on the approved Ad 1 and Ad 2 verticals.
# captions.py is the MASTER's copy (it carries Ad 3's FIX dict and its `import g5 as vlib`), not the skill's raw one.
cp -f g3.py g5.py captions.py cut/ || exit 1
cp -f "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/shortad-from-longform/reference/caption_sync_check.py" cut/ || exit 1
python3 zcut_build3.py > logs/cut_build6.log 2>&1 && echo "cut/ rebuilt $(date)" || { echo CUTBUILD FAILED; tail -8 logs/cut_build6.log; exit 1; }
python3 -c "
import json
d=json.load(open('cut/cut_timeline.json'))
tm=[b['tmap'] for b in d['beats'] if isinstance(b,dict) and b['kind']=='phonecard' and b.get('tmap')]
assert tm, 'no phonecard tmap in the cut timeline'
lo=min(x[1] for t in tm for x in t)
assert lo >= 5.84, f'cut timeline opens an app card at {lo}s -- the stranger photo is back'
print(f'cut timeline app-card floor OK: {lo:.3f}s')
N=d['NTOT']; FPS=30000/1001
ins=sum(b['n1']-b['n0'] for b in d['beats'] if b['kind']!='talk')
print(f'cutdown {N} fr = {N/FPS:.2f}s   insert {ins} = {ins/N*100:.1f}%')
assert N/FPS <= 59.0, 'over 0:59'
assert ins/N >= 0.55, f'insert coverage {ins/N*100:.1f}% under the 55% bound'
" || exit 1
python3 render3.py --cutplan cut_plan.json --out cut/picture.mp4 > logs/cut_render6.log 2>&1 \
  && tail -1 logs/cut_render6.log || { echo CUTRENDER FAILED; tail -5 logs/cut_render6.log; exit 1; }
python3 zmux.py cut/picture.mp4 cut/ad3_vertical_9x16_59s.mp4 cut/his_mix.wav > cut/logs/mux.log 2>&1 && cat cut/logs/mux.log || { echo CUTMUX FAILED; tail cut/logs/mux.log; exit 1; }
echo "CUT6 DONE $(date)"
