"""RO-37 round 2 colour options in the new layout: the same two moments (wide on the field beside a side list; tight in
front of his softened gym footage) in each grade, F (recommended), E and B."""
import os, subprocess, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r2
O = f"{r2.W2}/review/options/colour"; os.makedirs(O, exist_ok=True)
MOMENTS = {"wide": 163.0, "tight": 33.0}
for g in ("F", "E", "B"):
    for name, t in MOMENTS.items():
        subprocess.run(["python3", "assemble.py", f"{O}/colour-{g}-{name}.jpg", "--frame", str(r2.fr(t))], check=True,
                       env=dict(os.environ, RO37_GRADE=g), capture_output=True)
    src = f"{r2.R1}/review/options/colour/colour-{g} - REVIEW 540p.mp4"     # round 1's moving sample: same grade on the same pixels
    if os.path.exists(src): shutil.copy(src, f"{O}/colour-{g} - R1 moving sample - REVIEW 540p.mp4")
print("colour stills ok")
