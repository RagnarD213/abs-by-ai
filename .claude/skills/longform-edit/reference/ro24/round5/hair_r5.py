"""Hair clearance report from an assemble_r3 build (every presenter frame, measured on the rendered picture before the
graphics; VIDEO-RULES 2026-10-20 needs >= 20 px at 1080p), with native-scale proof crops of the tightest frames.
  hair_r3.py <out.mp4.build.json> <report.json> [<proof.jpg> <export.mp4>]"""
import json, sys, subprocess, numpy as np, cv2
B = json.load(open(sys.argv[1])); H = B['hair']
valid = [h for h in H if h[1] is not None]; none = [h for h in H if h[1] is None]
fails = [h for h in valid if h[1] < 20]
by = {}
for f, top, fr, mode in valid: by.setdefault(f'{mode}/{fr}', []).append(top)
rep = dict(frames_checked=len(H), none_detected=len(none), min_top=min(h[1] for h in valid) if valid else None,
           by_placement={k: dict(min=min(v), median=float(np.median(v)), n=len(v)) for k, v in by.items()},
           worst=[dict(frame=h[0], t=round(h[0] * 1001 / 30000, 2), top=h[1], framing=h[2], placement=h[3]) for h in sorted(valid, key=lambda h: h[1])[:8]],
           fails=fails[:40], verdict='PASS' if not fails and not none else ('FAIL' if fails else 'CHECK'))
json.dump(rep, open(sys.argv[2], 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k != 'fails'}, indent=1))
if len(sys.argv) > 4:
    FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg.real'; tiles = []
    for w in rep['worst'][:5]:
        i = w['frame'] - B['g0']
        raw = subprocess.check_output([FF, '-v', 'error', '-i', sys.argv[4], '-vf', f'select=eq(n\\,{i}),scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24', '-vsync', '0', '-frames:v', '1', '-f', 'rawvideo', '-'])
        fr = np.frombuffer(raw, np.uint8).reshape(1080, 1920, 3).copy()
        x0 = 400 if w['placement'] != 'right' else 760; t = fr[:300, x0:x0 + 900].copy()
        cv2.line(t, (0, 20), (899, 20), (255, 0, 0), 1)
        cv2.putText(t, f"{w['t']}s {w['placement']}/{w['framing']} top {w['top']}px", (8, 290), cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 0, 0), 2); tiles.append(t)
    cv2.imwrite(sys.argv[3], np.concatenate(tiles, 0)[:, :, ::-1])
