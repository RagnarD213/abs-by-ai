#!/usr/bin/env python3
"""TikTok cover-first copies for the SL-17 picks: tiktok_cover.build() with the approved Instagram cover as frame 0, then checks
(frame count +1, audio packets identical, frame 0 matches the cover). Usage: python3 tiktok.py s2 s5"""
import sys,json,subprocess,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here));sys.path.insert(0,str(here.parents[1]/'blotato'))
from root import P
import tiktok_cover as tc
tc.FFMPEG=str(P/'Media/video_edit/bin/ffmpeg');tc.FFPROBE=str(P/'Media/video_edit/bin/ffprobe')
from build import COPY
OUT=Path('/Volumes/Expansion/_edit_work/sl17-publish');AP=P/'Short-form video content/covers/approved-sl17'
picks=json.loads((AP/'picks.json').read_text())['covers']
def count(f,sel):
 return int(subprocess.run([tc.FFPROBE,'-v','error','-select_streams',sel,'-count_packets','-show_entries','stream=nb_read_packets','-of','csv=p=0',str(f)],capture_output=True,text=True).stdout.strip())
for k in sys.argv[1:]:
 slug=COPY[k][1];src=P/'Short-form video content'/f'{slug}.mp4';cov=Path(picks[slug]['instagram']);dst=OUT/f'{slug}_tiktok.mp4'
 tc.build(str(src),str(cov),str(dst))
 v0,v1,a0,a1=count(src,'v:0'),count(dst,'v:0'),count(src,'a:0'),count(dst,'a:0')
 fr=OUT/f'{slug}_tiktok_frame0.png';subprocess.run([tc.FFMPEG,'-loglevel','error','-y','-i',str(dst),'-frames:v','1',str(fr)],check=True)
 a=np.asarray(Image.open(fr).convert('RGB'),dtype=float);c=np.asarray(Image.open(cov).convert('RGB').resize((a.shape[1],a.shape[0])),dtype=float)
 psnr=10*np.log10(255**2/max(((a-c)**2).mean(),1e-9))
 print(k,'video',v0,'->',v1,'audio',a0,'->',a1,'frame0 PSNR %.1f dB'%psnr,hashlib.sha256(dst.read_bytes()).hexdigest()[:8],dst.stat().st_size)
 assert v1==v0+1 and a1==a0 and psnr>33,k   # 33 dB: the yellow and red type loses a little in 4:2:0 colour; looked at side by side, identical (2026-10-21)
