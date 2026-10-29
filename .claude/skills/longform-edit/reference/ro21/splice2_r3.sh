#!/bin/zsh
# RO-21 round 3, second fix: four single-picture TV spots re-rendered and spliced into the current picture at its IDR keyframes
# (stream copy). Patches: q1 [3510,3661) BG09, q2 [4478,5024) BG11, q3 [5744,5841) BG13, q4 [9133,9411) BG20.
set -e
B=/Volumes/Expansion/_edit_work/RO-21; F=$B/round3/film; FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"; cd $F
cp ../final/picture.mp4 pic_v2.mp4; cp ../final/picture.build.json pic_v2.build.json
for r in "3510 3661 q1" "4478 5024 q2" "5744 5841 q3" "9133 9411 q4"; do set -- ${=r}
  [ -f $3.mp4 ] || python3 $B/recipe/assemble_r1.py $F/$3.mp4 --g0 $1 --g1 $2 --stills $(( ($1 + $2) / 2 )) --grade rich --plan $B/round3/bg_plan.json --manifest $B/round3/film_manifest.json
done
t() { python3 -c "print(f'{$1*1001/30000:.6f}')"; }
cut() { if [ $1 -eq 0 ]; then $FF -v error -y -i pic_v2.mp4 -frames:v $2 -c copy $3; else $FF -v error -y -ss $(t $1) -i pic_v2.mp4 -frames:v $(( $2 - $1 )) -c copy $3; fi; }
cut 0 3510 s0.mp4; cut 3661 4478 s1.mp4; cut 5024 5744 s2.mp4; cut 5841 9133 s3.mp4; cut 9411 13556 s4.mp4
printf "file '%s'\n" s0.mp4 q1.mp4 s1.mp4 q2.mp4 s2.mp4 q3.mp4 s3.mp4 q4.mp4 s4.mp4 > list3.txt
$FF -v error -y -f concat -safe 0 -i list3.txt -c copy ../final/picture.mp4
python3 - <<PY
import json
old=json.load(open('pic_v2.build.json')); runs=[]; hair=[]
segs=[('old',0,3510),('q1',3510,3661),('old',3661,4478),('q2',4478,5024),('old',5024,5744),('q3',5744,5841),('old',5841,9133),('q4',9133,9411),('old',9411,10**9)]
for name,lo,hi in segs:
    b=old if name=='old' else json.load(open(f'{name}.mp4.build.json'))
    for r in b['runs']:
        a,z=max(r['o0'],lo),min(r['o1'],hi)
        if a<z: runs.append(dict(r,o0=a,o1=z))
    hair+=[h for h in b['hair'] if lo<=h[0]<hi]
json.dump(dict(frames=max(r['o1'] for r in runs),g0=0,g1=max(r['o1'] for r in runs),grade='rich',runs=runs,hair=hair),open('../final/picture.build.json','w'))
print('runs',len(runs),'frames',max(r['o1'] for r in runs))
PY
echo "picture packets: $(/Users/danielrose/Projects/Claude/Projects/Abs\ By\ AI/Media/video_edit/bin/ffprobe -v error -count_packets -select_streams v -show_entries stream=nb_read_packets -of csv=p=0 ../final/picture.mp4)"
echo SPLICE2 DONE
