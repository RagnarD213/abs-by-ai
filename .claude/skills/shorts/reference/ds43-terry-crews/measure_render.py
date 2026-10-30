"""Key check renders for DS-43 (python3 measure_render.py VERSION T0 OUTDIR; from DS-44) in the DS-40 R2 measuring geometry: 9.35 s of piece A (roll T0..T0+9.35), the final key cache
(c2_A, house stage 2 despeckle + haze clip, B_warmvivid grade) scaled to 1080 wide (0.5 of the source), source row 0 at output y 175,
over the pale backdrop (216,225,235), navy and saturated pink. mcflicker.py / measure_r2.py read these with SRC start = T0.
    python3 measure_render.py T0 OUTDIR"""
import sys, subprocess, numpy as np, cv2
from pathlib import Path
VERSION, T0, OUT = sys.argv[1], float(sys.argv[2]), Path(sys.argv[3]); OUT.mkdir(exist_ok=True)
sys.argv = [sys.argv[0], VERSION]
sys.path.insert(0, str(Path(__file__).resolve().parent)); import assemble as AS
N = int(round(9.35*AS.FPS)); OY = 175
BGS = {'pale': np.array([216, 225, 235])/255, 'navy': np.array([20, 30, 60])/255, 'pink': np.array([0.95, 0.25, 0.62])}
enc = {k: subprocess.Popen([AS.F, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', '30000/1001', '-i', '-',
       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14',
       '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', str(OUT/f'{k}.mp4')], stdin=subprocess.PIPE) for k in BGS}
for i in range(N):
    Fp, a = AS.key_frame('T', T0 + i/AS.FPS)          # this version's talk piece
    for k, bg in BGS.items():
        out = np.ones((1920, 1080, 3), np.float32)*bg.astype(np.float32)
        out = AS.place(out, Fp, a, 1080/1620, 0, OY)
        enc[k].stdin.write(AS.u8(out).tobytes())
for p in enc.values(): p.stdin.close(); p.wait()
print('MEASURE RENDERS', OUT, N)
