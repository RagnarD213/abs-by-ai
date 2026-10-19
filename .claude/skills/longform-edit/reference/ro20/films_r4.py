"""RO-20 round 4 (2026-10-18): the three "Invest In Your Health" films, each a list of parts of the ONE approved timeline plus the
approved studio pickups (round3/pickups, option A, locked by round3b/round3b-hashes.sha256).

  films_r4.py check            the parts, frame counts and the boundary checks (nothing rendered)
  films_r4.py picture V        render every part's picture (graphics and clips as approved), concat -> round4/V/pic.mp4 (+ base.mp4)
  films_r4.py audio V          voice track = the treated film voice sliced at the part frames + the pickup voices AS THEY ARE (never through
                               voice_chain a second time) + treated room tone for the two roll handles; untreated twin for the audio gate;
                               the quiet RO-07 bed; voice_chain --finish-only (gain + limiter only) -> round4/V/MASTER.mp4
Parts:  film f0 f1 [bare]   frames of the cut timeline (shots.json out frames), bare = presenter only (no plan items, no lower thirds)
        pickup Pn           the approved pickup segment, picture re-encoded on the same settings, its treated voice
        handle s0 s1 shot   raw roll source frames s0..s1 shown at that shot's approved crop and grade (v3 lead-in and tail)"""
import os, sys, json, subprocess, wave, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import build as Bd
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes")
sys.path.insert(0, "/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio")
import composite as HC
W = Bd.W; FPS = Bd.FPS; SR = 48000; FF = Bd.FF; FP = FF.replace("ffmpeg", "ffprobe")
PK = f"{W}/round3/pickups"; OUT = f"{W}/round4"
REPO = "/Users/danielrose/Documents/Claude/Projects/Abs By AI"
VC = f"{REPO}/.claude/skills/_shared/audio/voice_chain.py"
C1722 = f"{W}/round3b/src/c1722_lav_0-192_48k_mono.wav"           # the raw shoot lav the pickups were cut from (untreated twin)
TAKE0 = {"P1": 35.90, "P2": 53.00, "P3": 116.30, "P4": 166.05}     # pickup_audio20b.TAKES: each P#.voice.wav starts at its take's start
fr = Bd.fr
VIDEOS = {
    "v1": dict(job="RO-20", title="Why You Should Invest More In Your Health", parts=[
        ("film", 0, 14681),            # round 4 review fix: to 489.856, after "...too." (the look-down at his hands 489.86 to 490.22 is cut; the pause runs 0.41 s)
        ("film", 14692, 16184),        # from mind2.0r0 ("Now, ..."); then to the end of Gb23, after "...therapy and medication." (envelope -50 dB at 540.007; "And" starts 540.06)
        ("film", 16228, fr(900.35)),   # "The fourth reason why" (cost1.0r0 starts at 541.474); "And I'll go more into that in a minute." is out
        ("pickup", "P1"),
        ("film", 95434, 97247)]),      # video 1's own sign-off (round 3), ends on "filled with motivation." then the restart
    "v2": dict(job="RO-20B", title="What To Cut To Afford Getting In Shape", parts=[
        ("film", fr(3014.45), fr(3026.62), "bare"),   # opens on camera: "You need to be spending more money on your health ... no matter how little money you have."
        ("pickup", "P2"),
        ("film", fr(904.70), 42581),   # "But I know at this point in the video" to "once you're there in a couple months." (more3.0 ends at 42581)
        ("pickup", "P3")]),            # carries its 5.4 s end-screen tail
    "v3": dict(job="RO-20C", title="What To Buy For Your Health At Every Income Level", parts=[
        ("pickup", "P4"),
        ("handle", 55249, 55258, "home1.0r0"),   # 0.30 s of the roll before "All right." (he is still, hands together, mouth closed; lav -60 dB)
        ("film", 42581, 95434),        # "All right. So let me walk you through it." to "I'll see you in the next video."
        ("handle", 123680, 123698, "cta.0r7")]), # 0.60 s of his held smile after the last word (roll; lav room tone; the thumbs-up starts at 123706)
}
def probe_frames(p):
    r = subprocess.run([FP, "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", p], capture_output=True, text=True)
    return int(r.stdout.strip())
def pickup_frames(pid): return probe_frames(f"{PK}/{pid}.mp4")
def nframes(p):
    if p[0] == "film": return p[2] - p[1]
    if p[0] == "pickup": return pickup_frames(p[1])
    return p[2] - p[1]
def layout(v):
    """[(part, out_f0, out_f1)] on the video's own timeline."""
    out, t = [], 0
    for p in VIDEOS[v]["parts"]:
        n = nframes(p); out.append((p, t, t + n)); t += n
    return out
MAN = json.load(open(Bd.MANIFEST))
# the approved self-generation demo (P01, P03) was built by ro06/recipe/phone_demo.py into ro06/round5/phone/, which no longer exists. Rebuilt with
# that same script and its own softblue.py (round4/phone_recipe/, only OUT changed) into round4/phone/; a 40-frame P03 render from it matches the
# approved round 3 sign-off clip at 0.12 to 0.16 mean grey levels with zero bias (encoder noise): round4/phone/PROOF.txt
_OLD_P01 = "/Volumes/Extreme/_edit_work/ro06/round5/phone/P01-softblue.mp4"; NEW_P01 = f"{W}/round4/phone/P01-softblue.mp4"
if not os.path.exists(_OLD_P01):
    for _it in Bd.R:
        if _it["kind"] == "clip": _it["src"] = [s_.replace(_OLD_P01, NEW_P01) for s_ in _it["src"]]
# round 4 review fixes (watch judge, 2026-10-18), applied in memory so the approved plan files stay as they were:
# 1. 345.11: the camera's own recording skips a beat (mouth open to closed, head 40 px, between consecutive roll frames 14298|14299) inside the
#    tight run prod4.0r0|prod4.0r1. The shot list cut there for exactly that reason (prod4.0r1 reframe, W); the round 1 solve held both tight.
#    prod4.0r1 goes to the wide size, so the skip is a zoom cut, and prod4.0r2 (continuous source) cuts back to tight.
# 2. Cb02 (poolside AI clip): its chip sat on the passing man's face; top left is clear (the couple sit lower left).
# 3. Gb20 runs across the 489.856 trim: before it, a copy whose hold is 11 frames shorter and whose own fade-out is intact (round4/hf_fix); after it, none.
Bd.all_segments()
for _s in Bd._SEGS:
    if _s["key"] == "prod4.0r1": _s.update(framing="W", crop=(1920, 1080, 0, 0), zoom=1.0)
for _it in Bd.R:
    if _it["id"] == "Cb02": _it["chip_at"] = ((54, 54), "lt")
# 4. Standing / posing cutaways of Dan are never used (VIDEO-RULES 2026-10-14; B0438 and B0459 are named there, B0458 is library-rejected
#    since 2026-10-16 as a standing-around shot, B0429 is a still vacuum hold with a light stand in frame): Cb04, Cc21, Cd22, Cd27 come out and he
#    stays on camera (the presenter under Cb04, Cc21 and Cd27 is one continuous take at one crop). Under Cd22 two takes meet at the same size
#    (vac2|vac3 at 1306.67): vac3.0r0 goes to the wide size, as the rest of vac3.0r0's take already is.
# 5. Cc22 (handstand push-ups) sat under the Gc18 key point, which covered his head at the bottom of every rep: it comes out (one take underneath,
#    a zoom cut on continuous speech).
# 6. Stock that reads near black beside the kitchen (all B-roll is colour corrected, VIDEO-RULES 2026-10-11): the beer can (Cd07, low-key on black)
#    gets a mid-tone lift that keeps its black field (picked from three on a still, round4 notes).
import gfx as G
_DARK = "curves=all='0/0 0.06/0.09 0.20/0.32 0.50/0.66 1/1'"     # video 3 judge: stock at 35 to 55 % of the presenter's brightness (still sheet, round4 notes)
STOCK_GRADE = {"pexels-5538285": "curves=all='0/0 0.04/0.07 0.15/0.30 0.45/0.68 1/1'",
               "pexels-3296053": _DARK, "pexels-6944078": _DARK, "pexels-39347711": _DARK, "pexels-35585667": _DARK, "pexels-3209241": _DARK,
               "pexels-12188782": _DARK, "B0308_": _DARK, "B0020_": _DARK, "B0470_": _DARK,
               # video 1 judge (rebuild): the couch shot (Cb25) dark and strongly blue, the brain-scan tablet (Cc09) dim
               "pexels-6605951": _DARK + ",colorbalance=rs=0.04:bs=-0.06:rm=0.03:bm=-0.05", "B0336_": _DARK,
               # video 2 judge (rebuild): the smoking pan (Cd11) dark and colourless, the couple on the sofa (Cd28) dim and blue
               "pexels-8626681": _DARK + ",eq=saturation=1.25", "pexels-6336604": _DARK + ",colorbalance=rs=0.04:bs=-0.06:rm=0.03:bm=-0.05",
               # video 2 final judge: the old car (Cc26) dim and teal, the two men on the sofa (Cd05) murky grey, the gamers (Cd16) dark and red-magenta
               "pexels-8103389": _DARK + ",colorbalance=rs=0.04:bs=-0.05:rm=0.03:bm=-0.04", "pexels-9627292": _DARK + ",eq=saturation=1.3",
               "pexels-8888437": _DARK + ",colorbalance=rm=-0.04:gm=0.03:bm=0.01"}
_grade_for0 = G.grade_for
def _grade_for(src):
    return _grade_for0(src) or next((g for k, g in STOCK_GRADE.items() if k in os.path.basename(src or "")), None)
G.grade_for = _grade_for
# 7. Video 3 judge: Cf16 (medicine-ball V-ups) sat under Gf17, which covered his abs: out (one take underneath, a zoom cut on continuous speech).
#    Ce24's second shot (AI leg curl, A0106) has a roller pad floating with no lever arm: Ce24 keeps only its first shot (AI leg press, on
#    "things like a leg press"), and he is on camera for "a leg curl machine" (the same wide take runs underneath).
#    2628.23: another skip in the camera's own recording inside the tight run rich3.0r3|rich3.0r4 (continuous roll frames): rich3.0r3 goes wide
#    (its start is under Cf24), so the skip is a zoom cut; rich3.0r4 cannot (rich4.0r0 after it is a different take, already wide).
REMOVED = {"Cb04", "Cc21", "Cd22", "Cd27", "Cc22", "Cf16", "Cd07", "Ce19"}   # Ce19: black-and-white bedroom stock between colour shots (video 3 final judge); one take underneath   # Cd07: the beer can still read near black after a lift (video 2 judge, rebuild); one take underneath
for _it in Bd.R:
    if _it["id"] == "Ce24":
        _n = fr(_it["t1"]) - fr(_it["t0"]); _it["src"] = _it["src"][:1]; _it["t1"] = (fr(_it["t0"]) + _n//2)/FPS
for _s in Bd._SEGS:
    if _s["key"] == "rich3.0r3": _s.update(framing="W", crop=(1920, 1080, 0, 0), zoom=1.0)
# 8. Lower thirds whose main line is spoken 3 to 8 s after they appear sat with only the small top line (video 3 judge, junk_card): a copy keeps the
#    entrance (frames 0 to 18) and resumes at K, so the main line still reveals on the same word; the graphic starts K - 19 frames later.
LT_RETIME = {"Gf24": 232, "Gf25": 100, "Ge32": 84, "Gf08": 72}
def _retime(m, K):
    out = {}
    for key in ("mov", "mask"):
        dst = f"{W}/round4/hf_fix/{m['id']}{'_mask' if key == 'mask' else ''}_from{K}.mov"
        if not os.path.exists(dst):
            subprocess.run([FF, "-v", "error", "-y", "-i", m[key], "-vf", f"select='lt(n\\,19)+gte(n\\,{K})',setpts=N/FRAME_RATE/TB",
                            "-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le", "-vendor", "apl0", dst], check=True)
        out[key] = dst
    return dict(m, a=(fr(m["a"]) + K - 19)/FPS, **out)
MAN = [_retime(m, LT_RETIME[m["id"]]) if m["id"] in LT_RETIME else m for m in MAN]
for _it in Bd.R:
    if _it["id"] in LT_RETIME: _it["t0"] = next(m["a"] for m in MAN if m["id"] == _it["id"])
Bd.R[:] = [i for i in Bd.R if i["id"] not in REMOVED]
for _s in Bd._SEGS:
    if _s["key"] == "vac3.0r0": _s.update(framing="W", crop=(1920, 1080, 0, 0), zoom=1.0)
# 9. Video 2 final judge: at 1363.90 (v2 8:05.52) the wide take ther2.0r0 opens with his head turned away for 4 frames while "Now" starts. Picture only:
#    the outgoing tight take (still, silent, facing the lens on roll frames 52111 to 52114) holds 4 frames longer; the voice is untouched.
for _i, _s in enumerate(Bd._SEGS):
    if _s["key"] == "ther2.0r0" and _s["o0"] == 40876:
        Bd._SEGS[_i - 1]["o1"] += 4; _s.update(o0=_s["o0"] + 4, src0=_s["src0"] + 4)
_GB20 = dict(next(m for m in MAN if m["id"] == "Gb20"), b=14681/FPS, mov=f"{W}/round4/hf_fix/Gb20_trim.mov", mask=f"{W}/round4/hf_fix/Gb20_mask_trim.mov")
PART_MAN = {("v1", 0): {"Gb20": _GB20}, ("v1", 1): {"Gb20": None}}
def part_manifest(v, k):
    o = PART_MAN.get((v, k), {}); out = []
    for m in MAN:
        if m["id"] in o:
            if o[m["id"]] is not None: out.append(o[m["id"]])
        else: out.append(m)
    return out
def check(v):
    errs = []
    for p, a, b in layout(v):
        if p[0] != "film" or (len(p) > 3 and p[3] == "bare"): continue
        f0, f1 = p[1], p[2]
        ovr = set().union(*[set(o) for (vv, _k), o in PART_MAN.items() if vv == v]) if any(vv == v for vv, _k in PART_MAN) else set()
        for it in Bd.R:
            if it["id"] in ovr: continue          # handled by its per-part manifest override
            i0, i1 = fr(it["t0"]), fr(it["t1"])
            for e in (f0, f1):
                if i0 < e < i1: errs.append(f"{v}: {it['id']} ({it['kind']}) crosses part edge {e} ({i0}..{i1})")
        k = [q[0] for q in layout(v)].index(p)
        for m in part_manifest(v, k):
            i0, i1 = fr(m["a"]), fr(m["b"])
            for e in (f0, f1):
                if i0 < e < i1: errs.append(f"{v}: lower third {m['id']} crosses part edge {e}")
    return errs
def seg_of(key): return next(s for s in Bd.all_segments() if s["key"] == key)
def enc_args(out):
    return ["-c:v", "libx264", "-crf", "15", "-preset", "medium", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", out]
VF_SAME = "scale=in_color_matrix=bt709:in_range=tv,format=rgb24,scale=out_color_matrix=bt709:out_range=tv,format=yuv420p"   # render_picture's own decode/encode
def picture(v):
    d = f"{OUT}/{v}/parts"; os.makedirs(d, exist_ok=True); lst, blst, info = [], [], []
    R0, M0 = Bd.R, Bd.MANIFEST; Bd.all_segments()
    for k, (p, a, b) in enumerate(layout(v)):
        out = f"{d}/{k:02d}_{p[0]}.mp4"; n = b - a
        if p[0] == "film":
            bare = len(p) > 3 and p[3] == "bare"
            Bd.R = [] if bare else R0
            comp = HC.Compositor([] if bare else part_manifest(v, k))
            segs = Bd.segments(p[1], p[2])
            if not os.path.exists(out + ".v.mp4") or probe_frames(out + ".v.mp4") != n:
                Bd.render_picture(p[1]/FPS, p[2]/FPS, out, p[1], p[2], segs, comp)
            Bd.R = R0
            info.append(dict(part=list(p), out=[a, b], segments=[dict(s, o0=s["o0"] - p[1] + a, o1=s["o1"] - p[1] + a) for s in segs]))
            lst.append(out + ".v.mp4"); blst.append(out + ".base.mp4")
        elif p[0] == "pickup":
            if not os.path.exists(out) or probe_frames(out) != n:
                # no colour conversion: the approved pickup pixels, re-encoded only (an RGB round trip measured 2 grey levels darker, 2026-10-18)
                subprocess.run([FF, "-v", "error", "-y", "-i", f"{PK}/{p[1]}.mp4", "-map", "0:v", "-vf", "format=yuv420p"] + enc_args(out), check=True)
            info.append(dict(part=list(p), out=[a, b])); lst.append(out); blst.append(out)
        else:
            sg = dict(seg_of(p[3]), src0=p[1], o0=0, o1=n)        # the shot's own crop and grade, on the roll frames before / after it
            if not os.path.exists(out + ".v.mp4") or probe_frames(out + ".v.mp4") != n:
                Bd.R = []; Bd.render_picture(0, n/FPS, out, 0, n, [sg], HC.Compositor([])); Bd.R = R0     # the film's own picture path, nothing composited
            info.append(dict(part=list(p), out=[a, b], segments=[dict(sg, o0=a, o1=b)])); lst.append(out + ".v.mp4"); blst.append(out + ".base.mp4")
        got = probe_frames(lst[-1]); assert got == n, (out, got, n)
        print(f"  part {k} {p[:3]} -> {n} frames", flush=True)
    for name, L in (("pic", lst), ("base", blst)):
        txt = f"{OUT}/{v}/{name}.txt"; open(txt, "w").write("".join(f"file '{x}'\n" for x in L))
        subprocess.run([FF, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", txt, "-c", "copy", "-movflags", "+faststart", f"{OUT}/{v}/{name}.mp4"], check=True)
    tot = layout(v)[-1][2]; got = probe_frames(f"{OUT}/{v}/pic.mp4"); assert got == tot, (got, tot)
    json.dump(dict(video=v, frames=tot, parts=info), open(f"{OUT}/{v}/layout.json", "w"), indent=1)
    print(v, "picture", tot, "frames", round(tot/FPS, 3), "s", flush=True)
# ------------------------------------------------------------------------------------------------ audio
def rd(path, s0, n, ch_out=1):
    w = wave.open(path); ch = w.getnchannels(); w.setpos(max(0, s0))
    x = np.frombuffer(w.readframes(n), np.int16).astype(np.float32).reshape(-1, ch)/32768
    x = x[:, 0]
    if len(x) < n: x = np.concatenate([x, np.zeros(n - len(x), np.float32)])
    return x
def smp(f): return int(round(f/FPS*SR))
FADE = int(0.012*SR)
def fades(x):
    x = x.copy(); x[:FADE] *= np.linspace(0, 1, FADE); x[-FADE:] *= np.linspace(1, 0, FADE); return x
def room_like(raw, film_ref):
    """treated room tone for a roll handle: voice 4's EQ on the raw lav, then the level of the film voice's own room tone next to the join"""
    tmp = f"{OUT}/_h.wav"; o = wave.open(tmp, "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(raw, -1, 1)*32767).astype("<i2").tobytes()); o.close()
    eq = Bd.VOICE4[1]
    y = subprocess.run([FF, "-v", "error", "-i", tmp, "-af", eq, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    y = np.frombuffer(y, np.float32)[:len(raw)]
    if len(y) < len(raw): y = np.concatenate([y, np.zeros(len(raw) - len(y), np.float32)])
    g = np.sqrt(np.mean(film_ref**2) + 1e-12)/np.sqrt(np.mean(y**2) + 1e-12)
    return y*g, 20*np.log10(g)
def audio_tracks(v):
    FV, FU = f"{W}/voice/film_voice.wav", f"{W}/voice/film_voice.untreated.wav"
    L = f"{W}/lav.wav"; lay = layout(v); N = smp(lay[-1][2]); vo = np.zeros(N, np.float32); un = np.zeros(N, np.float32); notes = []
    for k, (p, a, b) in enumerate(lay):
        s0, s1 = smp(a), smp(b); n = s1 - s0
        if p[0] == "film":
            x = rd(FV, smp(p[1]), n); u = rd(FU, smp(p[1]), n)
        elif p[0] == "pickup":
            x = rd(f"{PK}/{p[1]}.voice.wav", 0, n); u = rd(C1722, int(round(TAKE0[p[1]]*SR)), n)
            if p[1] == "P3":                       # its tail is silent for the end screen (pickup_audio20b); the twin is too
                y = np.abs(rd(f"{PK}/{p[1]}.voice.wav", 0, n)); last = np.nonzero(y > 1e-4)[0][-1]; u[last + 1:] = 0
        else:
            raw = rd(L, smp(p[1]), n)
            nxt = lay[k + 1] if k + 1 < len(lay) else None; prv = lay[k - 1]
            # the film voice's room tone right next to the join (0.10 s inside the neighbouring film part, away from words)
            ref = rd(FV, smp(nxt[0][1]) - int(0.09*SR), int(0.07*SR)) if p[1] == 55249 else rd(FV, smp(prv[0][2]) - int(0.08*SR), int(0.07*SR))
            x, gdb = room_like(raw, ref); u = raw
            notes.append(f"handle {p[1]}..{p[2]}: voice 4 EQ, {gdb:+.1f} dB to the film voice's room tone beside the join")
            if p[1] == 123680:                     # the film ends: fade the room out over the tail
                x = x*np.linspace(1, 0, n)**1.5
        vo[s0:s1] = fades(x); un[s0:s1] = fades(u)
    return vo, un, notes
def wr(path, x, ch=2):
    o = wave.open(path, "w"); o.setnchannels(ch); o.setsampwidth(2); o.setframerate(SR)
    y = (np.clip(x, -1, 1)*32767).astype("<i2"); o.writeframes(np.repeat(y[:, None], ch, 1).tobytes() if ch == 2 else y.tobytes()); o.close()
def audio(v, bed_db="-30"):
    import common as C
    d = f"{OUT}/{v}"; pic = f"{d}/pic.mp4"; M = f"{d}/MASTER.mp4"
    vo, un, notes = audio_tracks(v)
    wr(f"{d}/voice.wav", vo); wr(f"{d}/untreated.wav", un, 1)
    tot = len(vo)/SR
    subprocess.run(["python3", f"{W}/recipe/bed.py", f"{tot:.3f}", f"{d}/bed.wav"], check=True)
    subprocess.run(["python3", VC, "--in", f"{d}/voice.wav", "--finish-only", "--bed", f"{d}/bed.wav", "--bed-db", str(bed_db), "--video", pic, "--frame-lock", pic,
                    "--out", M, "--work", f"{d}/vc_work"], check=True)
    ss, dur = C.analysis_window(M)
    b = C.stash_untreated(M, C.pcm(f"{d}/untreated.wav", ss=ss, dur=dur),
                          note=f"RO-20 R4 {v}: the untreated twin of the voice track (raw kitchen lav at the cut frames, raw C1722 lav under the pickups, raw roll under the handles), same sample positions")
    json.dump(dict(notes=notes, bed_db=bed_db, untreated=b), open(f"{d}/audio_build.json", "w"), indent=1)
    print(v, "audio done", notes, b, flush=True)
if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "check":
        for v in VIDEOS:
            lay = layout(v); print(v, VIDEOS[v]["job"], f"{lay[-1][2]} frames = {lay[-1][2]/FPS/60:.2f} min")
            for p, a, b in lay: print(f"   {a:6d}-{b:6d} ({(b-a)/FPS:7.2f} s) {p}")
            for e in check(v): print("   !!", e)
    elif cmd == "picture": picture(sys.argv[2])
    elif cmd == "audio": audio(sys.argv[2], *(sys.argv[3:4]))
