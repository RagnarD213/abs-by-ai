"""A -30 dB silencedetect calls a trailing FRICATIVE silent -- it is the mirror of
the documented soft-ONSET trap. Re-measure at -45 dB and audit every EDL edge."""
import re, subprocess, json, sys
for b in ("C1630","C1631","C1632","C1633"):
    p = subprocess.run(["ffmpeg","-nostdin","-v","info","-i",f"{b}.wav","-af",
        "silencedetect=noise=-45dB:d=0.08","-f","null","-"],capture_output=True,text=True)
    st=[float(m) for m in re.findall(r"silence_start:\s*(-?[\d.]+)",p.stderr)]
    en=[float(m) for m in re.findall(r"silence_end:\s*(-?[\d.]+)",p.stderr)]
    n=min(len(st),len(en)); json.dump([[st[i],en[i]] for i in range(n)],open(f"sil45_{b}.json","w"))
    print(f"  {b}: {n} silences at -45dB")
