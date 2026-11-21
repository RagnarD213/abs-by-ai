import sys, re, subprocess
pats = [("blk", r"Black point \(1%\):\s+([\d.]+)"), ("med", r"Median luminance:\s+([\d.]+)"),
        ("gam", r"Gamma correction:\s+([\d.]+)"), ("WBdev", r"Deviation:\s+([\d.]+)"),
        ("skinD", r"Hue delta:\s+([\d.]+)"), ("milky", r"Milky blacks:\s+(\w+)"),
        ("colorf", r"Colorfulness:\s+([\d.]+)")]
rows=[]
for t in sys.argv[1:]:
    out = subprocess.run(["python3","auto_grade.py","/tmp/sc/f_%s.png"%t],
                         cwd="/tmp/sc/color-grade-ai",capture_output=True,text=True).stdout
    vals=[]
    for name,p in pats:
        m=re.search(p,out); vals.append(m.group(1) if m else "-")
    rows.append((t,vals))
    print("t=%-5s blk %-7s med %-7s gam %-7s WBdev %-7s skinD %-5s milky %-4s colorf %s" % tuple([t]+vals))
import statistics as st
for i,(name,_) in enumerate(pats):
    nums=[float(v[i]) for _,v in rows if v[i] not in ("-","YES","NO")]
    if nums: print("  %-7s median %.4f  range %.4f..%.4f" % (name, st.median(nums), min(nums), max(nums)))
