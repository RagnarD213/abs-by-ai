"""RO-37 picture: four portrait rolls (10/23 pool set, Sony 4K S-Cinetone, 2160x3840 after rotation, decoded as BT.709).
Presentations for a 16:9 long-form from portrait footage (round-1 choice):
  T  = full-frame 16:9 window 2160x1215 (hair -> chest), 4 % headroom above the highest hair in the shot
  W  = the portrait picture hair -> waistband as a rounded panel (height PH) over a background:
       bg "soft" = the same picture blurred, darkened, navy-tinted (the locked green-screen 'soft' treatment numbers)
       bg "field" = the moving Soft Blue Light field
  panel x: centre, or right (PX_RIGHT) while a left-third card is up.
Colour: the pool set's approved grades (DS-84/DS-76 look-options: F Deep And Vivid picked by Dan on this set)."""
import json, os, subprocess
P = "/Users/danielrose/Projects/Claude/Projects/Abs By AI"
W = "/Volumes/Expansion/_edit_work/RO-37/round1"; FPS = 30000/1001
FF = f"{P}/Media/video_edit/bin/ffmpeg"
RD = "/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content"
ROLLS = {r: f"{RD}/{r}.MP4" for r in ["C1893", "C1894", "C1895", "C1897"]}
GRADES = {
    "F": ("Deep And Vivid", "eq=contrast=1.25:gamma=1.14:brightness=0.003:saturation=1.75"),
    "E": ("Vivid, Softer", "eq=contrast=1.22:gamma=1.16:brightness=0.000:saturation=1.58"),
    "B": ("Richer Contrast", "eq=contrast=1.13:gamma=1.20:brightness=0.015:saturation=1.18"),
}
GRADE_KEY = os.environ.get("RO37_GRADE", "F")
GRADE = GRADES[GRADE_KEY][1]
DEC = "scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv"
HAIR = json.load(open(f"{W}/framing/hair_roll.json")) if os.path.exists(f"{W}/framing/hair_roll.json") else {}
def hair_min(roll, t0=None, t1=None):
    v = [r[1] for r in HAIR.get(roll, []) if r[1] is not None and (t0 is None or t0 - 0.5 <= r[0] <= t1 + 0.5)]
    return min(v) if v else 200
TW, TH = 2160, 1215
T2W, T2H = 1728, 972
def body_cx(roll, t0=None, t1=None):
    v = [(r[2] + r[3]) / 2 for r in HAIR.get(roll, []) if r[1] is not None and (t0 is None or t0 - 0.5 <= r[0] <= t1 + 0.5)]
    return int(sorted(v)[len(v) // 2]) if v else 1080
WH = 2640                     # panel source height: hair -> waistband
PH, PW = 1000, round(2160 * 1000 / 2640)      # panel on screen 864x1000, 40 px top/bottom
PX_CENTER, PX_RIGHT = (1920 - PW) // 2, 1920 - PW - 120
def t_y(roll, t0=None, t1=None): return max(0, hair_min(roll, t0, t1) - round(0.04 * TH) - 8)
def w_y(roll, t0=None, t1=None): return max(0, hair_min(roll, t0, t1) - round(0.04 * WH) - 8)
NAVY = "lutrgb=r='val*0.465+1.3':g='val*0.465+3.3':b='val*0.465+7.0',vignette=angle=0.5"
def graph(framing, roll, t0=None, t1=None, bg="soft", px="center", grade=None):
    """ffmpeg filter graph from [0:v] (the source roll) to [v] 1920x1080 rgb24-ready yuv. For W with bg=field, input 1 is the field video."""
    g = grade or GRADE
    if framing == "T":
        y = t_y(roll, t0, t1)
        return f"[0:v]{DEC},crop={TW}:{TH}:0:{y},scale=1920:1080:flags=lanczos,{g},format=yuv420p[v]"
    if framing == "T2":                        # the tighter close-up (1.25x), for a take join under a lower third
        y = max(0, hair_min(roll, t0, t1) - round(0.04 * T2H) - 8); x = min(TW - T2W, max(0, body_cx(roll, t0, t1) - T2W // 2))
        return f"[0:v]{DEC},crop={T2W}:{T2H}:{x}:{y},scale=1920:1080:flags=lanczos,{g},format=yuv420p[v]"
    y = w_y(roll, t0, t1)
    if isinstance(px, (list, tuple)):          # ("slide", from, to, frames): the panel eases across as a side card comes or goes
        x0, x1, n = {"center": PX_CENTER, "right": PX_RIGHT}[px[1]], {"center": PX_CENTER, "right": PX_RIGHT}[px[2]], px[3]
        x = f"'{x0}+({x1 - x0})*(1-cos(PI*min(n/{n},1)))/2'"
    else: x = PX_CENTER if px == "center" else PX_RIGHT
    fg = (f"[s1]crop=2160:{WH}:0:{y},scale={PW}:{PH}:flags=lanczos,format=yuva420p[fgr];[1:v]format=gray[mk];"
          f"[fgr][mk]alphamerge[fg];")
    if bg == "soft":
        b = f"[s0]scale=1920:-2:flags=bilinear,crop=1920:1080:0:{max(0, round(y*1920/2160) + 120)},gblur=sigma=24,{NAVY}[bg];"
    else:
        b = "[2:v]scale=1920:1080,format=yuv420p[bg];"
    mask_in = "[1:v]"
    head = f"[0:v]{DEC},{g},split[s0][s1];" if bg == "soft" else f"[0:v]{DEC},{g}[s1];"
    return head + b + fg + f"[bg][fg]overlay=x={x}:y=40:eval=frame,format=yuv420p[v]"
def ensure_mask():
    """Rounded-corner alpha mask for the panel (radius 28)."""
    m = f"{W}/framing/panel_mask.png"
    if not os.path.exists(m):
        from PIL import Image, ImageDraw
        im = Image.new("L", (PW, PH), 0); ImageDraw.Draw(im).rounded_rectangle([0, 0, PW - 1, PH - 1], 28, fill=255); im.save(m)
    return m
