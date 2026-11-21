"""Voice track: lav (channel 1, verified per roll) sliced sample-exact to timeline.json."""
import json,subprocess,numpy as np,wave,os
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg";M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
SR=48000;TL=json.load(open('timeline.json'));P=TL['pieces']
LAV={}  # channel per roll: pick_lav sidecar, overridden where the tone test proved the lav is ch1 (see notes)
for p in P:
    r=p['source']
    if r in LAV:continue
    ch=json.load(open(f"{M}{r}.roll.json"))['audio']['lav']['lav']['channel']
    if r in ('C1538','C1550'):ch=1
    LAV[r]=ch;f=f'lav/{r}.npy'
    if not os.path.exists(f):
        b=subprocess.run([FF,'-nostdin','-v','error','-i',M+r+'.MP4','-vn','-af',f'pan=mono|c0=c{ch}','-ar','48000','-f','s16le','-'],capture_output=True,check=True).stdout
        np.save(f,np.frombuffer(b,np.int16))
def s(fr):return round(fr*1001/30000*SR)
N=s(TL['total_frames']+round(4.0*30000/1001));out=np.zeros(N,np.float32);fade=int(.03*SR);ramp=np.linspace(0,1,fade,dtype=np.float32)
for p in P:
    a,b=s(p['out_f0']),s(p['out_f1']);n=b-a
    if p['speed']!=1:continue
    x=np.load(f"lav/{p['source']}.npy",mmap_mode='r');i=round(p['src_in']*SR)
    seg=np.asarray(x[i:i+n],np.float32)/32768
    if len(seg)<n:seg=np.pad(seg,(0,n-len(seg)))
    seg=seg.copy();seg[:fade]*=ramp;seg[-fade:]*=ramp[::-1]
    out[a:b]=seg
# declared transient softening: clipped lid-clamp snaps (object noise, not speech) that overshoot after AAC
SOFTEN=[('C1548',81.964,-6.0,0.07)]
for p in P:
    if p['speed']!=1:continue
    for src,t,db,hw in SOFTEN:
        if p['source']==src and p['src_in']<=t<p['src_in']+p['src_dur']:
            c=s(p['out_f0'])+round((t-p['src_in'])*SR);h=int(hw*SR);win=np.hanning(2*h)
            out[c-h:c+h]*=(1-(1-10**(db/20))*win).astype(np.float32)
w=wave.open('audio/voice_raw.wav','w');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
w.writeframes((np.clip(out,-1,1)*32767).astype('<i2').tobytes());w.close()
json.dump(LAV,open('audio/lav_channels.json','w'));print('voice',N/SR,'s',LAV)
