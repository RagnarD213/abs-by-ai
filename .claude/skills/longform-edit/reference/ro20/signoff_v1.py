"""Video 1's own sign-off (pieces v1so1 to v1so4, appended after the 53 minute timeline): the review clip and its join frames.
usage: signoff_v1.py range   -> prints the section's frames and seconds on the cut timeline
       signoff_v1.py clip    -> round3/context/v1-signoff.mp4 (+ a 540p review copy). The whole-film voice (voice/film_voice.wav)
                                stops at 3184.3 s, so this clip's voice is assembled from the lav at the cut's own frames and run
                                through the shared chain with the locked voice 4 settings (build.render_voice, build.VOICE4).
       signoff_v1.py joins   -> round3/signoff_v1/qc/join_*.jpg: the last 4 frames before and the first 4 after every picture
                                change in the clip (decoded in order from the rendered file, never by seeking), plus the first
                                and last frames of the section.
The clip is built from plan_resolved.json and hf/manifest.json as they stand (items Gi01 to Gi05 and P03)."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro20/recipe")
W = "/Volumes/Extreme/_edit_work/ro20"; FPS = 30000/1001
OUT = f"{W}/round3/context/v1-signoff.mp4"; QC = f"{W}/round3/signoff_v1/qc"
S = [s for s in json.load(open(f"{W}/shots.json")) if s["piece"].startswith("v1so")]
F0, F1 = S[0]["out_f0"], S[-1]["out_f1"]
def secs(f): return f/FPS
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "range":
        print(f"frames {F0} to {F1} ({F1-F0} frames), {secs(F0):.3f} to {secs(F1):.3f} s, {secs(F1-F0):.3f} s")
    elif what == "clip":
        import build as Bd
        a, b = secs(F0), secs(F1); assert Bd.fr(a) == F0 and Bd.fr(b) == F1
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        Bd.render_range(a, b, OUT)                         # picture + voice 4 through the shared chain, frame-locked to the picture
        subprocess.run([Bd.FF, "-v", "error", "-y", "-i", OUT, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-c:a", "aac", "-b:a", "160k",
                        "-movflags", "+faststart", OUT.replace(".mp4", " - REVIEW 540p.mp4")], check=True)
        for ext in (".base.mp4", ".base.mp4.txt", ".v.mp4"):
            try: os.remove(OUT + ext)
            except OSError: pass
        print("clip", OUT, F1-F0, "frames", flush=True)
    elif what == "joins":
        import build as Bd
        from PIL import Image, ImageDraw
        os.makedirs(QC, exist_ok=True)
        sg = [s for s in Bd.all_segments() if s["shot"].startswith("v1so")]
        items = [it for it in Bd.R if it["t1"] > secs(F0)]
        cuts = {}                                           # clip frame index -> label
        for p, s in zip(sg, sg[1:]):
            kind = "reframe (same take)" if Bd.same_take(p, s) else "JOIN (source cut)"
            cuts[s["o0"]-F0] = f"{kind} {p['key']} {p['framing']} > {s['key']} {s['framing']}"
        for it in items:
            if it["kind"] == "clip":
                cuts[Bd.fr(it["t0"])-F0] = cuts.get(Bd.fr(it["t0"])-F0, "") + f" | {it['id']} IN"
                cuts[Bd.fr(it["t1"])-F0] = cuts.get(Bd.fr(it["t1"])-F0, "") + f" | {it['id']} OUT"
        n = F1-F0; want = {}
        for c, lab in cuts.items():
            for k in range(c-4, c+4):
                if 0 <= k < n: want[k] = (c, lab)
        for k in list(range(0, 4)) + list(range(n-4, n)): want.setdefault(k, (0 if k < 4 else n, "section start" if k < 4 else "section end"))
        dec = subprocess.Popen([Bd.FF, "-v", "error", "-i", OUT, "-vf", "scale=640:360:in_color_matrix=bt709,format=rgb24", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
        got = {}
        for k in range(n):
            buf = dec.stdout.read(640*360*3)
            if len(buf) < 640*360*3: raise SystemExit(f"short read at frame {k} of {n}")
            if k in want: got[k] = Image.frombytes("RGB", (640, 360), buf)
        assert dec.stdout.read(1) == b"", "the clip has more frames than the section"
        dec.wait()
        groups = {}
        for k, (c, lab) in want.items(): groups.setdefault((c, lab), []).append(k)
        for (c, lab), ks in sorted(groups.items()):
            ks = sorted(ks); sh = Image.new("RGB", (640*4, 360*((len(ks)+3)//4)))
            for i, k in enumerate(ks):
                im = got[k].copy(); d = ImageDraw.Draw(im); d.rectangle((0, 0, 330, 16), fill=(0, 0, 0))
                d.text((3, 2), f"clip f{k}  film f{F0+k}  {secs(F0+k):.3f} s  {'BEFORE' if k < c else 'AFTER'}", fill=(255, 255, 0))
                sh.paste(im, ((i % 4)*640, (i//4)*360))
            name = f"{QC}/join_{c:04d}.jpg"; sh.save(name, quality=88); print(name, "|", lab.strip(" |"), flush=True)
