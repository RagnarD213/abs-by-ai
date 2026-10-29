#!/bin/zsh
# RO-21 round 3: splice the two label-fix patches into the picture at existing IDR keyframes (stream copy, no re-encode):
# chunk0[0,2226) + patchA[2226,2853) + chunk1[2853,5400) + chunk2 + chunk3[8100,9133) + patchB[9133,9411) + chunk3[9411,9500) + chunk4..6
set -e
F=/Volumes/Expansion/_edit_work/RO-21/round3/film; FF="/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real"; cd $F
t() { python3 -c "print(f'{$1*1001/30000:.6f}')"; }
$FF -v error -y -i chunk0.mp4 -frames:v 2226 -c copy p0.mp4
$FF -v error -y -ss $(t 153) -i chunk1.mp4 -c copy p2.mp4          # chunk1 starts at film frame 2700; keyframe at 2853
$FF -v error -y -i chunk3.mp4 -frames:v 1033 -c copy p4.mp4         # chunk3 starts at 8100; 9133-8100
$FF -v error -y -ss $(t 1311) -i chunk3.mp4 -c copy p6.mp4          # keyframe at 9411
printf "file '%s'\n" p0.mp4 patchA.mp4 p2.mp4 chunk2.mp4 p4.mp4 patchB.mp4 p6.mp4 chunk4.mp4 chunk5.mp4 chunk6.mp4 > list2.txt
$FF -v error -y -f concat -safe 0 -i list2.txt -c copy ../final/picture.mp4
for f in p0 patchA p2 chunk2 p4 patchB p6 chunk4 chunk5 chunk6 ../final/picture; do
  echo "$f $("${FF%.real}"probe -v error -count_packets -show_entries stream=nb_read_packets -of csv=p=0 $f.mp4)"; done
python3 - <<PY
import json; runs=[]; hair=[]
for name, lo, hi in (('chunk0',0,2226),('patchA',2226,2853),('chunk1',2853,5400),('chunk2',5400,8100),('chunk3',8100,9133),('patchB',9133,9411),('chunk3',9411,9500),('chunk4',9500,9800),('chunk5',9800,11500),('chunk6',11500,10**9)):
    b=json.load(open(f'{name}.mp4.build.json'))
    for r in b['runs']:
        a,z=max(r['o0'],lo),min(r['o1'],hi)
        if a<z: runs.append(dict(r,o0=a,o1=z))
    hair+=[h for h in b['hair'] if lo<=h[0]<hi]
json.dump(dict(frames=max(r['o1'] for r in runs),g0=0,g1=max(r['o1'] for r in runs),grade='rich',runs=runs,hair=hair),open('../final/picture.build.json','w'))
print('runs',len(runs),'frames',max(r['o1'] for r in runs))
PY
echo SPLICE DONE
