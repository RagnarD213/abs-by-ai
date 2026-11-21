#!/usr/bin/env python3
"""median luma / median HSV saturation / luma p95 / clipped fraction, BT.709 decode.
meas.py FILE T0 T1 [CROP w:h:x:y] [GRADE ffmpeg-filter]"""
import sys, subprocess, numpy as np
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
def meas(f, t0, t1, crop=None, grade=None, fps=2):
    vf = []
    if crop: vf.append(f'crop={crop}')
    vf.append('scale=480:-2:in_color_matrix=bt709:in_range=tv')
    if grade: vf.insert(len(vf) - 1 if crop else 0, grade) if False else None
    chain = ','.join(([f'crop={crop}'] if crop else []) + ([grade] if grade else []) +
                     [f'fps={fps}', 'scale=480:270:force_original_aspect_ratio=decrease:in_color_matrix=bt709:in_range=tv,format=rgb24'])
    raw = subprocess.run([FF, '-v', 'error', '-ss', str(t0), '-i', f, '-t', str(t1 - t0), '-vf', chain,
                          '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
    # infer dims
    w, h = 480, None
    probe = subprocess.run([FF, '-v', 'error', '-ss', str(t0), '-i', f, '-frames:v', '1', '-vf', chain, '-f', 'image2pipe', '-c:v', 'png', '-'], capture_output=True).stdout
    from PIL import Image; import io
    im = Image.open(io.BytesIO(probe)); w, h = im.size
    a = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32) / 255
    Y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx = a.max(-1); mn = a.min(-1); S = np.where(mx > 0.02, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return dict(luma=float(np.median(Y)), sat=float(np.median(S)), p95=float(np.percentile(Y, 95)),
                clip=float((mx > 0.97).mean()), n=a.shape[0])
if __name__ == '__main__':
    f, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    crop = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
    grade = sys.argv[5] if len(sys.argv) > 5 else None
    r = meas(f, t0, t1, crop, grade)
    print(f"luma {r['luma']:.3f} sat {r['sat']:.3f} p95 {r['p95']:.3f} clip {r['clip']*100:.1f}% (n={r['n']})")
