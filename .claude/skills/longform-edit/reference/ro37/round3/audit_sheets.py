"""Zoom sheets from r3/audit/key.json: each shot's worst frame, the whole of him beside a 3x crop of the longest edge fault."""
import json, cv2, numpy as np
d = json.load(open("r3/audit/key.json")); keys = sorted(d, key=int)
TW, TH = 400, 460; PER = 4; sheets = []
def tc(f): t = f * 1001 / 30000; return f"{int(t//60)}:{t%60:04.1f}"
for s in range(0, len(keys), PER):
    canvas = np.full((TH * 2 + 8, TW * 4 + 24, 3), 40, np.uint8)
    for i, k in enumerate(keys[s:s + PER]):
        r = d[k]; img = cv2.imread(f"r3/audit/s{int(k):03d}.jpg")
        x, y, w, h = r["rect"]; X0 = max(0, x); X1 = min(1920, x + w); Y1 = 1080
        body = img[0:Y1, X0:X1]; sc = min(TW / body.shape[1], TH / body.shape[0]); body = cv2.resize(body, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        cands = [r[n] for n in ("w_bl", "w_dl") if r[n][1]]; c = max(cands, key=lambda z: z[0])[1] if cands else (x + w // 2, 200)
        zw, zh = TW // 3, TH // 3; zx = int(np.clip(c[0] - zw // 2, 0, 1920 - zw)); zy = int(np.clip(c[1] - zh // 2, 0, 1080 - zh))
        zoom = cv2.resize(img[zy:zy + zh, zx:zx + zw], (TW, TH), interpolation=cv2.INTER_CUBIC)
        ox = (i % 2) * (2 * TW + 16); oy = (i // 2) * (TH + 8)
        canvas[oy:oy + body.shape[0], ox:ox + body.shape[1]] = body; canvas[oy:oy + TH, ox + TW + 4:ox + 2 * TW + 4] = zoom
        cv2.putText(canvas, f"#{k} {tc(r['wf'])} {r['framing']}/{r['placement']}/{r['bg_type']} {r['shot']}", (ox + 6, oy + 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1, cv2.LINE_AA)
    p = f"r3/audit/sheet{s // PER:02d}.jpg"; cv2.imwrite(p, canvas, [cv2.IMWRITE_JPEG_QUALITY, 90]); sheets.append(p)
print(len(sheets))
