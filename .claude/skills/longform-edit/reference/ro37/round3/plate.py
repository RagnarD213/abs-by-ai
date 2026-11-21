"""Round 3 second key pass, step 1: the empty background of each roll. The camera sat on a tripod, so a median of the pixels his cut-out
does not cover (200 frames across the roll, colour F, matte size) gives the pool and hedge behind him; plate/<roll>.png + seen count."""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, cv2, r2
from PIL import Image
def main(roll):
    need = r2.needed_frames(0, r2.END_F, r2.shots2()).get(roll, [])
    ks = sorted(k for k in need if os.path.exists(r2.mpath(roll, k)))
    pick = ks[::max(1, len(ks) // 200)]; S = []; M = []
    for k in pick:
        raw = subprocess.run([r2.FF, "-nostdin", "-v", "error", "-ss", f"{(k - 0.5) / r2.FPS:.6f}", "-i", r2.F.ROLLS[roll], "-frames:v", "1", "-fps_mode", "passthrough", "-vf",
                              f"{r2.F.DEC},{r2.F.GRADES['F'][1]},scale={r2.MW}:{r2.MH}:flags=lanczos:in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
        if len(raw) < r2.MW * r2.MH * 3: continue
        S.append(np.frombuffer(raw, np.uint8).reshape(r2.MH, r2.MW, 3))
        a = np.asarray(Image.open(r2.mpath(roll, k)), np.uint8)
        M.append(cv2.dilate((a > 8).astype(np.uint8), np.ones((31, 31), np.uint8)) == 0)
    S = np.stack(S).astype(np.float32); M = np.stack(M); print(roll, len(S), "frames", flush=True)
    S[~M] = np.nan; plate = np.nanmedian(S, 0); seen = M.sum(0)
    plate = np.nan_to_num(plate, nan=0)
    Image.fromarray(plate.astype(np.uint8)).save(f"plate/{roll}.png"); np.save(f"plate/{roll}.seen.npy", seen.astype(np.uint16))
    print(roll, "seen>=5:", round(float((seen >= 5).mean()), 3), flush=True)
for r in sys.argv[1:]: main(r)
