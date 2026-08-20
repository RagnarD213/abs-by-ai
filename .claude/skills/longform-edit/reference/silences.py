import re,subprocess,sys,json
wav,out=sys.argv[1],sys.argv[2]
best=None
for thr,d in [("-30dB",0.10),("-26dB",0.08),("-34dB",0.12)]:
    p=subprocess.run(["ffmpeg","-nostdin","-v","info","-i",wav,"-af",
        f"silencedetect=noise={thr}:d={d}","-f","null","-"],capture_output=True,text=True)
    s=p.stderr
    starts=[float(m) for m in re.findall(r"silence_start:\s*(-?[\d.]+)",s)]
    ends=[float(m) for m in re.findall(r"silence_end:\s*(-?[\d.]+)",s)]
    print(f"  {thr} d={d}: {len(starts)} starts / {len(ends)} ends")
    if thr=="-30dB":
        n=min(len(starts),len(ends)); best=[[starts[i],ends[i]] for i in range(n)]
json.dump(best,open(out,"w"))
tot=sum(b-a for a,b in best)
print(f"wrote {out}: {len(best)} silences, {tot:.0f}s total silence")
