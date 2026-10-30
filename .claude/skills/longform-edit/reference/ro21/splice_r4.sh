#!/bin/zsh
# RO-21 round 4: only the changed ranges are re-rendered and spliced into round 3's picture at its IDR keyframes (stream copy). Audio, subtitles
# and everything after 6:37 stay exactly as round 3. Ranges (all before the recap cut): BG01, BG03, BG04, BG06, BG11, BG14, BG15+B07, BG16, BG18,
# BG25+B11+BG26+BG27.  r0..r9 render in parallel (each through the render queue), then the splice.
set -e
B=/Volumes/Expansion/_edit_work/RO-21; R=$B/round4; F=$R/film; mkdir -p $F $R/final; FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"; cd $F
RANGES=("175 475 r0" "991 1491 r1" "1587 2079 r2" "2226 2853 r3" "4478 5024 r4" "5927 6168 r5" "6408 6916 r6" "7132 7381 r7" "8100 8503 r8" "10849 11909 r9")
for r in $RANGES; do set -- ${=r}
  ( [ -f $3.ok ] || { python3 $B/recipe/assemble_r1.py $F/$3.mp4 --g0 $1 --g1 $2 --stills $(( ($1 + $2) / 2 )) --grade rich --plan $R/bg_plan.json --manifest $R/film_manifest.json > $3.log 2>&1 && touch $3.ok; } ) &
done; wait
for r in $RANGES; do set -- ${=r}; [ -f $3.ok ] || { echo "FAILED $3"; exit 1; }; done
SRC=$B/round3/final/picture.mp4; cp $B/round3/final/picture.build.json src.build.json
t() { python3 -c "print(f'{$1*1001/30000:.6f}')"; }
cut() { if [ $1 -eq 0 ]; then $FF -v error -y -i $SRC -frames:v $2 -c copy $3; else $FF -v error -y -ss $(t $1) -i $SRC -frames:v $(( $2 - $1 )) -c copy $3; fi; }
rm -f list.txt; prev=0; i=0
for r in $RANGES; do set -- ${=r}
  cut $prev $1 s$i.mp4; echo "file 's$i.mp4'" >> list.txt; echo "file '$3.mp4'" >> list.txt; prev=$2; i=$((i+1))
done
cut $prev 13410 s$i.mp4; echo "file 's$i.mp4'" >> list.txt
$FF -v error -y -f concat -safe 0 -i list.txt -c copy $R/final/picture.mp4
python3 - <<PY
import json
old=json.load(open('src.build.json')); runs=[]; hair=[]
R=[tuple(x.split()) for x in """175 475 r0|991 1491 r1|1587 2079 r2|2226 2853 r3|4478 5024 r4|5927 6168 r5|6408 6916 r6|7132 7381 r7|8100 8503 r8|10849 11909 r9""".split('|')]
segs=[]; p=0
for a,b,n in R: segs+= [('old',p,int(a)),(n,int(a),int(b))]; p=int(b)
segs.append(('old',p,10**9))
for name,lo,hi in segs:
    b=old if name=='old' else json.load(open(f'{name}.mp4.build.json'))
    for r in b['runs']:
        a,z=max(r['o0'],lo),min(r['o1'],hi)
        if a<z: runs.append(dict(r,o0=a,o1=z))
    hair+=[h for h in b['hair'] if lo<=h[0]<hi]
json.dump(dict(frames=max(r['o1'] for r in runs),g0=0,g1=max(r['o1'] for r in runs),grade='rich',runs=runs,hair=hair),open('$R/final/picture.build.json','w'))
print('runs',len(runs),'frames',max(r['o1'] for r in runs))
PY
echo "picture packets: $("/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffprobe" -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 $R/final/picture.mp4)"
echo SPLICE_R4_DONE
