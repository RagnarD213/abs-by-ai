from pathlib import Path
import subprocess,io
from PIL import Image,ImageDraw
R=Path('/Volumes/Extreme/_edit_work/SL-11/round2'); FF='/Users/danielrose/Projects/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
LIB=Path('/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed')
items=[('current-demo',Path('/Volumes/Extreme/_edit_work/SL-11/round1/build/A/source_picture.mp4'),13.5135,22.72)]
for id in ['B0419','B0420','B0428','B0429']:
 p=next(LIB.glob(id+'*.mp4'));dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(p)]));items.append((id,p,0,dur))
for id,p,start,dur in items:
 ts=[i*.5 for i in range(int(dur*2))]; sheet=Image.new('RGB',(6*230,((len(ts)+5)//6)*390),'#eeeeee'); dr=ImageDraw.Draw(sheet)
 for i,t in enumerate(ts):
  b=subprocess.check_output([FF,'-v','error','-ss',str(start+t),'-i',str(p),'-frames:v','1','-vf','scale=220:360:force_original_aspect_ratio=decrease','-f','image2pipe','-vcodec','mjpeg','-']);im=Image.open(io.BytesIO(b));x=(i%6)*230;y=(i//6)*390;sheet.paste(im,(x,y+24));dr.text((x,y),f'{id} {t:.2f}s',fill='black')
 sheet.save(R/'source-qa'/f'{id}.jpg',quality=90);print(id,flush=True)
