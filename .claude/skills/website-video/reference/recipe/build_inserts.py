#!/usr/bin/env python3
"""REV 4 inserts (2026-09-08):
  tag      gfx/tag15.png -- the AI-GENERATED chip at 1.5x for full-frame AI clips (lesson 17: upper-left, 40:40)
  ai_X     gfx/ai_X.mov  -- the Veo clip trimmed to its beat, scaled to 1920x1080, the tag burned upper-left (H.264;
                            layout.mix() adds the alpha fades in-graph, so no 2-GB alpha intermediates)
  macro    gfx/pip_macro.mov -- the REAL Macro Tracker recording (macro2/record_macro.py on absbyai.com, salmon plate ->
                            775 cal itemised -> Log Meal -> logged) assembled to the MACRO beat: photo -> Analyze ->
                            analysing -> the itemised list with the total -> logged, through the phone mask + plate
  hub      gfx/pip_hub.mov -- the members' home screen (hub/hub_capture.py), one slow continuous scroll top -> bottom
Each PiP also writes gfx/<name>.json {"marks": [...]} -- its state-change times on the tight timeline, for the watch pass.
  python3 build_inserts.py tag ai_a ai_b ... macro hub
"""
import glob, importlib.util, json, os, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image, ImageDraw
SK="/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared"
spec=importlib.util.spec_from_file_location("ml",f"{SK}/motionlib.py"); ml=importlib.util.module_from_spec(spec); spec.loader.exec_module(ml)
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
import beats as B
FF="/Volumes/Extreme/_edit_work/bin/ffmpeg"; FFP=FF.replace("ffmpeg","ffprobe")
FPS=30000/1001; FPSS="30000/1001"
G=f"{HERE}/gfx"; AI=f"{HERE}/ai"; M2=f"{HERE}/macro2"; HUB=f"{HERE}/hub"
PIP_BOX=[150,130,583,950]; PW,PH=433,820; VW,VH=1170,2214            # phone box; capture viewport (390x738 CSS @3x)
ease=lambda t: 0.0 if t<=0 else (1.0 if t>=1 else (3*t*t-2*t*t*t))    # smoothstep

def tag():
    f=ml.font(45,"ExtraBold")
    t=Image.new("RGBA",(1920,1080),(0,0,0,0)); ml.chip(t,(0,0),"AI-GENERATED",f,(18,18,18,235),(255,255,255,255),radius=12,padx=27,pady=15)
    t=t.crop(t.getbbox()); t.save(f"{G}/tag15.png"); print(f"  tag15.png {t.size}")

# clip in-points (s): Veo's first frames are the still itself; skip the static opening
INPOINT={"ai_a":0.2,"ai_b":0.3,"ai_c1":0.3,"ai_c2":0.3,"ai_d1":0.3,"ai_d2":0.3,"ai_d3":0.2}   # REV 5: d3 needs 7.68 s
# Veo baked a cross-DISSOLVE between two shots into D2 at 3.9-4.6 s (pv/veoD2_check.jpg). A dissolve inside a b-roll clip
# reads as an edit inside the AI clip; a straight CUT between the two shots does not. So D2 is the two clean shots on
# either side of it, cut together: [1.0, 3.85) + [4.7, end) (a second dissolve sits at 0.5-0.9 s). Any clip can be edited this way (spans in source seconds).
# REV 5 (Dan's rev-4 review, both artifacts measured on frame strips at 0.1 s -- pv/rev5_D1_lean.jpg,
# pv/rev5_D2_610_790.jpg, pv/rev5_D3_tail.jpg):
#   D1 -- the man leans in toward the pans from 4.4 s and a puff of "smoke" appears at his mouth 5.0-5.4 s (my own
#         prompt asked him to breathe in the smell). Cut at 4.08 (the builder trims to beat+0.10 = 3.78 s from 0.3).
#   D2 -- the row of containers in the WIDE shot starts to drift at ~7.0-7.1 s and is displaced by 7.6-7.95 s. The
#         wide shot now ends at 7.05.
# REV 6: all three meal clips REGENERATED with steak (ai/rev6/D1s|D2s|D3s.mp4) plus the toe-touch clip (C1t) -- the rev-5
# trims above belonged to the old footage and are NOT carried over; every span below was re-derived from frame strips
# of the new clips (pv/rev6_*_first/tail.jpg). D1s: the man turns to grin at the camera from 3.9 s -> use 0.1-3.88.
# D2s: Veo baked a cross-dissolve at 2.5-2.9 s (pv/rev6_D2s_x1.jpg) between the mid shot and the closer counter shot;
# 5.5-7.0 is one continuous shot (pv/rev6_D2s_x2.jpg). Cut the two clean shots together: [0.2,2.45) + [2.95, ...) --
# the builder trims the second span to the beat, so the insert never reaches the clip's tail.
EDIT={"ai_d1":[(0.1,3.88)], "ai_d2":[(0.2,2.45),(2.95,8.0)]}
CLIP={"ai_c1":"rev6/C1t.mp4","ai_d1":"rev6/D1s.mp4","ai_d2":"rev6/D2s.mp4","ai_d3":"rev6/D3s.mp4"}   # REV 6 sources; the rest stay clips/<X>.mp4
def ai(name):
    a,b=B.BEATS[name.upper()]; D=round(b-a+0.10,3); clip=f"{AI}/"+CLIP.get(name, f"clips/{name[3:].upper()}.mp4")
    dur=float(subprocess.run([FFP,"-v","error","-show_entries","format=duration","-of","csv=p=0",clip],capture_output=True,text=True).stdout)
    spans=EDIT.get(name) or [(INPOINT.get(name,0.2),dur)]
    spans=[(x,min(y,dur)) for x,y in spans]; avail=sum(y-x for x,y in spans)
    assert avail>=D-0.05, f"{name}: usable {avail:.2f}s is shorter than the beat {D:.2f}s"
    parts=f"[0:v]split={len(spans)}"+"".join(f"[s{i}]" for i in range(len(spans)))+";"+"".join(f"[s{i}]trim=start={x}:end={y},setpts=PTS-STARTPTS[p{i}];" for i,(x,y) in enumerate(spans))
    cat="".join(f"[p{i}]" for i in range(len(spans)))
    fc=(f"{parts}{cat}concat=n={len(spans)}:v=1:a=0,fps={FPSS},scale=1920:1080:flags=lanczos,setsar=1,trim=duration={D},setpts=PTS-STARTPTS[v];"
        f"[v][1:v]overlay=40:40:format=auto:shortest=1[o]")
    subprocess.run([FF,"-nostdin","-y","-v","error","-i",clip,
        "-loop","1","-framerate",FPSS,"-t",str(D+0.5),"-i",f"{G}/tag15.png",
        "-filter_complex",fc,"-map","[o]","-an","-c:v","libx264","-preset","medium","-crf","16","-pix_fmt","yuv420p","-t",str(D),f"{G}/{name}.mov"],check=True)
    print(f"  {name}.mov  {D:.2f}s from {clip.split('/')[-1]} spans {spans}")

# ---- PiP machinery ----------------------------------------------------------------------------
def _load(p): return np.asarray(Image.open(p).convert("RGB"))
def _offset(full, view, rows=(300,420)):
    """where a viewport screenshot sits inside the full-page screenshot of the same render (exact pixels), coarse-to-fine"""
    v=view[rows[0]:rows[1]].astype(np.int16); H=full.shape[0]-VH
    def err(y): return np.abs(full[y+rows[0]:y+rows[1]].astype(np.int16)-v).mean()
    ys=range(0,H+1,8); best=min(ys,key=err); best=min(range(max(0,best-8),min(H,best+8)+1),key=err)
    return best, err(best)
def _win(full,y): y=int(round(max(0,min(full.shape[0]-VH,y)))); return Image.fromarray(full[y:y+VH]).resize((PW,PH),Image.LANCZOS)
def _view(p): return Image.open(p).convert("RGB").resize((PW,PH),Image.LANCZOS)
def _encode(frames, D, out, marks):
    tmp=tempfile.mkdtemp(prefix="pip_")
    for i,f in enumerate(frames): f.save(f"{tmp}/{i:04d}.png")
    fc=(f"[0:v]format=rgba[rec];[1:v]format=gray[m];[rec][m]alphamerge=shortest=1[recm];"
        f"color=c=black@0.0:s=1920x1080:r={FPSS}:d={D},format=rgba[bg];"
        f"[bg][recm]overlay={PIP_BOX[0]}:{PIP_BOX[1]}:format=rgb:shortest=1[o1];"
        f"[o1][2:v]overlay=0:0:format=rgb:shortest=1,fade=t=in:st=0:d=0.45:alpha=1,fade=t=out:st={D-0.40:.3f}:d=0.40:alpha=1,format=argb[out]")
    subprocess.run([FF,"-nostdin","-y","-v","error","-framerate",FPSS,"-i",f"{tmp}/%04d.png",
        "-loop","1","-framerate",FPSS,"-t",str(D),"-i",f"{G}/pip_mask.png","-loop","1","-framerate",FPSS,"-t",str(D),"-i",f"{G}/pip_plate.png",
        "-filter_complex",fc,"-map","[out]","-t",str(D),"-c:v","qtrle","-pix_fmt","argb",out],check=True)
    shutil.rmtree(tmp); json.dump({"marks":[round(m,3) for m in marks]},open(out.replace(".mov",".json"),"w"))
    print(f"  {os.path.basename(out)}  {len(frames)} frames  {D:.2f}s  marks {[round(m,2) for m in marks]}")
def _xfade(frames, X=4):
    """4-frame crossfade wherever the state changes (a hard screenshot switch reads as a glitch)"""
    out=[]; prev=None
    for f,sw in frames:
        if sw and prev is not None:
            a,b=np.asarray(prev,dtype=np.float32),np.asarray(f,dtype=np.float32)
            for k in range(X):
                p=(k+1)/(X+1); out[-X+k]=Image.fromarray(((1-p)*np.asarray(out[-X+k],dtype=np.float32)+p*b).astype(np.uint8)) if len(out)>=X else out[-1]
        out.append(f); prev=f
    return out

def macro():
    a,b=B.MACRO; D=round(b-a,3); N=int(round(D*FPS))
    t_tap=B.at("Just take a picture")+0.45-a; t_m1=B.at("our AI instantly")-a; t_res=B.at("tells you the calories")-0.25-a
    t_log=B.end_of("you're eating")-0.5-a
    log=json.load(open(f"{M2}/shots.json")); first={}; analyzing=[]
    for l in log:
        first.setdefault(l["tag"],l["path"])
        if l["tag"]=="analyzing": analyzing.append(l["path"])
    P=lambda t: f"{M2}/{first[t]}"
    photo_full=_load(P("photo_loaded_full")); result_full=_load(P("result_full")); logged_full=_load(P("logged_full"))
    y_photo,e1=_offset(photo_full,_load(P("photo_loaded"))); y_res,e2=_offset(result_full,_load(P("result_view"))); y_list,e3=_offset(result_full,_load(P("result_logbtn")))
    y_logb,e4=_offset(logged_full,_load(P("logged_b"))); y_top=min(y_photo,558)
    print(f"  offsets: photo {y_photo} ({e1:.1f}) result {y_res} ({e2:.1f}) list {y_list} ({e3:.1f}) logged {y_logb} ({e4:.1f}) top {y_top}")
    assert max(e1,e2,e3,e4)<3.0, "a viewport shot did not match its full-page shot"
    t_res2=t_res+0.9; t_res3=t_res2+1.6; t_loga=t_log+0.25; t_logb=t_loga+1.25; t_logc=t_logb+1.6
    frames=[]; prev_state=None
    for i in range(N):
        t=i/FPS
        if t<t_tap:     st="photo";  im=_win(photo_full, y_photo+200*ease(t/t_tap))
        elif t<t_m1:    st="btn";    im=_view(P("photo_analyzebtn"))
        elif t<t_res:   st="anal";   im=_view(f"{M2}/{analyzing[int((t-t_m1)/0.3)%len(analyzing)]}")
        elif t<t_res2:  st="res";    im=_win(result_full,y_res)
        elif t<t_res3:  st="res";    im=_win(result_full,y_res+(y_list-y_res)*ease((t-t_res2)/(t_res3-t_res2)))
        elif t<t_log:   st="res";    im=_win(result_full,y_list)
        elif t<t_loga:  st="loga";   im=_view(P("logged_a"))
        elif t<t_logb:  st="logb";   im=_view(P("logged_b"))
        elif t<t_logc:  st="logb";   im=_win(logged_full,y_logb+(y_top-y_logb)*ease((t-t_logb)/(t_logc-t_logb)))
        else:           st="logb";   im=_win(logged_full,y_top)
        frames.append((im, st!=prev_state)); prev_state=st
    _encode(_xfade(frames),D,f"{G}/pip_macro.mov",[a+x for x in (t_tap,t_m1,t_res,t_res2,t_res3,t_log,t_logb,t_logc)])

def hub():
    a,b=B.HUB; D=round(b-a,3); N=int(round(D*FPS))
    full=_load(f"{HUB}/hub_full.png")
    # the scroll ends with the LAST feature tile (Support) at the bottom of the phone -- not on the account-deletion
    # link below it. Tiles are pure-white cards on the off-white page: the last white row down the centre column is the
    # bottom of the Support card.
    col=full[:,full.shape[1]//2]; white=np.where((col>=252).all(axis=1))[0]; last_card=int(white.max())
    span=int(min(full.shape[0]-VH, last_card+36-VH))
    assert full.shape[1]==VW and span>100, f"hub capture is {full.shape}, last card row {last_card}: scroll span {span} too short"
    print(f"  hub page {full.shape[0]} px, last tile bottom {last_card}, scroll span {span} px over {D:.1f}s")
    h0,h1=0.8,0.8; frames=[]
    for i in range(N):
        t=i/FPS; p=ease((t-h0)/(D-h0-h1)); frames.append((_win(full,span*p),False))
    _encode([f for f,_ in frames],D,f"{G}/pip_hub.mov",[a+h0,b-h1])

# ---- REV 6: the Trainer PiP (NUM2) ------------------------------------------------------------------------------
TR=f"{HERE}/trainer"; SHEETS=["db-goblet-squat","pushup","plank"]; DEMOS="/Users/danielrose/Documents/Claude/Projects/Abs By AI/public/exercise-demos"
def _demo_frames(exid, rect, secs):
    """the REAL demo clip (public/exercise-demos/<id>.mp4) resampled to the timeline fps and scaled to the sheet's video rect"""
    x,y,w,h=rect; n=int(secs*FPS)+2
    raw=subprocess.run([FF,"-v","error","-i",f"{DEMOS}/{exid}.mp4","-t",f"{secs+0.2:.2f}","-vf",f"fps={FPSS},scale={w}:{h}:flags=lanczos","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
    fr=np.frombuffer(raw,np.uint8); k=len(fr)//(w*h*3); return fr[:k*w*h*3].reshape(k,h,w,3)
def num2():
    """day view (no stick figures) -> slow scroll over the first exercise cards -> three exercise sheets, each with its
    AI demo PLAYING inside the sheet's own video rect (the app shows a poster until tapped; the demo frames are the real
    exercise-demos/*.mp4 composited into that rect with the sheet's 12-px rounded corners)."""
    a,b=B.NUM2; D=round(b-a,3); N=int(round(D*FPS))
    full=_load(f"{TR}/day_full.png"); assert full.shape[1]==VW, full.shape
    span=int(min(full.shape[0]-VH, 950))                     # SLOW: Goblet Squat and Push-Up cards come fully into view over 2 s (Dan: "slowly")
    t_s0,t_s1=0.45,2.45; t_sh=[2.55,4.05,5.55]; assert t_sh[-1]+1.0<D
    sheets=[]
    for exid in SHEETS:
        info=json.load(open(f"{TR}/sheet_{exid}.json")); rect=info["rect_px"]
        img=Image.open(f"{TR}/sheet_{exid}.png").convert("RGB"); assert img.size==(VW,VH), img.size
        mask=Image.new("L",(rect[2],rect[3]),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,rect[2]-1,rect[3]-1],radius=36,fill=255)
        sheets.append((img,rect,mask,_demo_frames(exid,rect,D-t_sh[len(sheets)]+0.1)))
    frames=[]; prev=None
    for i in range(N):
        t=i/FPS
        if t<t_sh[0]:
            st="day"; y=span*ease((t-t_s0)/(t_s1-t_s0)); im=_win(full,y)
        else:
            idx=max(j for j,ts in enumerate(t_sh) if t>=ts); st=f"sheet{idx}"
            img,rect,mask,demo=sheets[idx]; k=min(len(demo)-1,int(round((t-t_sh[idx])*FPS)))
            comp=img.copy(); comp.paste(Image.fromarray(demo[k]),(rect[0],rect[1]),mask); im=comp.resize((PW,PH),Image.LANCZOS)
        frames.append((im, st!=prev)); prev=st
    from PIL import ImageDraw as _ID
    _encode(_xfade(frames),D,f"{G}/pip_num2.mov",[a+t_s0,a+t_s1]+[a+x for x in t_sh])
    # proof strip: 8 frames across the PiP at native 433x820
    picks=[int(N*p) for p in (0.08,0.2,0.34,0.4,0.55,0.62,0.8,0.95)]
    sheet=Image.new("RGB",(8*PW+9*6,PH+12),(20,20,20))
    for j,k in enumerate(picks): sheet.paste(frames[k][0] if isinstance(frames[k],tuple) else frames[k],(6+j*(PW+6),6))
    sheet.save(f"{HERE}/pv/rev6_pip_num2_strip.jpg",quality=90); print("  pv/rev6_pip_num2_strip.jpg")

if __name__=="__main__":
    for arg in sys.argv[1:]:
        print(arg)
        if arg=="tag": tag()
        elif arg.startswith("ai_"): ai(arg)
        elif arg=="macro": macro()
        elif arg=="hub": hub()
        elif arg=="num2": num2()
        else: raise SystemExit(f"unknown {arg}")
    print("build_inserts done")
