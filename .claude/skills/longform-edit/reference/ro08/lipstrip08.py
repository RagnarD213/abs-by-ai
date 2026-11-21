"""Close-up strip of a synced character's mouth, every 2nd frame, the mouth followed with the face mesh, each crop labelled with the word
Dan is saying on that frame (from words_out.json) and a bar for the audio level. The look that goes with lipmeasure20.py's number.
usage: lipstrip08.py CLIP.mp4 AUDIO.wav <film time of the clip's first frame> OUT.jpg [fps=24] [every=2]"""
import sys, json, wave, numpy as np, cv2, mediapipe as mp
from PIL import Image, ImageDraw
clip, wav, t0, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]; fps = float(sys.argv[5]) if len(sys.argv) > 5 else 24.0; ev = int(sys.argv[6]) if len(sys.argv) > 6 else 2
WO = [w for w in json.load(open("/Volumes/Extreme/_edit_work/ro08/words_out.json")) if w["t0"] is not None]
w = wave.open(wav); sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32)/32768
cap = cv2.VideoCapture(clip); fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.3, min_tracking_confidence=0.3)
crops = []; k = 0; last = None; C = 150
while True:
    ok, f = cap.read()
    if not ok: break
    r = fm.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)); H, Wd = f.shape[:2]
    if r.multi_face_landmarks:
        L = r.multi_face_landmarks[0].landmark; p = lambda i: np.array([L[i].x*Wd, L[i].y*H])
        c = (p(13) + p(14))/2; s = np.linalg.norm(p(61) - p(291))*1.5; last = (c, max(s, 40))
    if k % ev == 0 and last is not None:
        c, s = last; x0, y0 = int(c[0]-s), int(c[1]-s*0.75); x1, y1 = int(c[0]+s), int(c[1]+s*0.75)
        pad = cv2.copyMakeBorder(f, 400, 400, 400, 400, cv2.BORDER_CONSTANT)[y0+400:y1+400, x0+400:x1+400]
        im = Image.fromarray(cv2.resize(pad, (C, int(C*0.75)))[:, :, ::-1]); d = ImageDraw.Draw(im); t = t0 + k/fps
        wd = next((q["w"].strip() for q in WO if q["t0"] <= t < q["t1"]), "")
        seg = x[int(k/fps*sr):int((k+1)/fps*sr)]; lv = 20*np.log10(np.sqrt(np.mean(seg**2) + 1e-12) + 1e-6) if len(seg) else -60
        d.rectangle((0, 0, C, 13), fill=(0, 0, 0)); d.text((2, 1), f"{k/fps:.2f} {wd}", fill=(255, 255, 0)); h = int(max(0, min(1, (lv+50)/35))*30); d.rectangle((C-6, int(C*0.75)-h, C, int(C*0.75)), fill=(80, 220, 120))
        crops.append(im)
    k += 1
per = 12; rows = -(-len(crops)//per); S = Image.new("RGB", (C*per, int(C*0.75)*rows))
for i, im in enumerate(crops): S.paste(im, ((i % per)*C, (i//per)*int(C*0.75)))
S.save(out, quality=88); print(len(crops), "crops ->", out)
