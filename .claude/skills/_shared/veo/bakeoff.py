"""Blind model bake-off page: a candidate video model against our baseline (Veo 3.1 Fast in Flow) on the STANDARD pairs.

  bakeoff.py build CANDIDATE_DIR --name "Kling 3.5 Pro" [--port 9072]

CANDIDATE_DIR holds the candidate's takes named P1.mp4 ... P6.mp4 (same start/end frames and prompts as
/Volumes/Extreme/_edit_work/model-bakeoff-standard/pairs.json; a missing file = the model refused or failed, shown as such).
Both sides are muted, re-encoded to the same size and frame rate, sides shuffled; the key goes to CANDIDATE_DIR/blind-key.json,
outside the served folder. After Dan picks, record each pair with `veo.py pick --kind bakeoff`.
"""
import argparse, html, json, os, random, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
STD = "/Volumes/Extreme/_edit_work/model-bakeoff-standard/pairs.json"
FF = os.path.join(HERE, "..", "..", "..", "..", "Media", "video_edit", "bin", "ffmpeg")   # render-queue shim


def enc(src, dst, aspect):
    box = "1920:1080" if aspect == "16:9" else "1080:1920"
    vf = f"scale={box}:force_original_aspect_ratio=decrease,pad={box}:(ow-iw)/2:(oh-ih)/2,fps=24"
    subprocess.run(["nice", "-n", "20", FF, "-y", "-loglevel", "error", "-i", src, "-t", "10", "-vf", vf, "-an",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", dst], check=True)


def still(src, dst):
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-vf", "scale=640:-2", dst], check=True)


def build(a):
    pairs = json.load(open(STD))["pairs"]; R = os.path.join(a.candidate_dir, "review"); os.makedirs(R, exist_ok=True)
    rng = random.Random(a.name); key = {}; cards = []
    for p in pairs:
        cand = os.path.join(a.candidate_dir, f"{p['id']}.mp4"); base = p["baseline"]["take"]
        still(p["start"], f"{R}/{p['id']}-start.jpg"); still(p["end"], f"{R}/{p['id']}-end.jpg")
        head = (f"<section><h2>{p['id']} · {html.escape(p['video'])}</h2><div class=frames><figure><img src='{p['id']}-start.jpg'>"
                f"<figcaption>Start frame</figcaption></figure><figure><img src='{p['id']}-end.jpg'><figcaption>End frame</figcaption></figure></div>"
                f"<details><summary>What the clip should show</summary><p class=prompt>{html.escape(p['prompt'])}</p></details>")
        if not os.path.exists(cand):
            key[p["id"]] = "candidate missing"
            cards.append(head + "<p><b>The new model refused or failed this shot</b>, so there is nothing to compare.</p></section>"); continue
        sides = ["candidate", "baseline"]; rng.shuffle(sides); key[p["id"]] = {"X": sides[0], "Y": sides[1]}
        for lab, s in zip("XY", sides): enc(cand if s == "candidate" else base, f"{R}/{p['id']}-{lab}.mp4", p["aspect"])
        cls = "v16" if p["aspect"] == "16:9" else "v9"
        cards.append(head + f"<div class='pair {cls}'>" + "".join(
            f"<figure><video src='{p['id']}-{l}.mp4' controls preload=metadata playsinline muted loop></video><figcaption>Clip {l}</figcaption></figure>"
            for l in "XY") + "</div></section>")
    json.dump({"candidate": a.name, "key": key}, open(os.path.join(a.candidate_dir, "blind-key.json"), "w"), indent=1)
    page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Video Model Blind Test</title><style>
:root{{--bg:#f6f7f9;--fg:#15181d;--muted:#5b6370;--card:#fff;--line:#dfe3e8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#111418;--fg:#e8ebef;--muted:#9aa3ae;--card:#1a1e24;--line:#2a3038}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 -apple-system,system-ui,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:24px 16px 64px}} .lede{{color:var(--muted)}}
section{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:0 0 20px}}
h2{{margin:0 0 12px;font-size:18px}} figure{{margin:0}} figcaption{{color:var(--muted);font-size:14px;margin-top:4px;text-align:center}}
.frames{{display:flex;gap:12px;margin-bottom:8px}} .frames img{{height:120px;border-radius:6px;display:block;max-width:45%;object-fit:cover}}
.pair{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}} .pair.v9{{max-width:640px}}
video{{width:100%;border-radius:8px;background:#000;display:block}} .prompt{{color:var(--muted);font-size:14px}}
@media (max-width:640px){{.pair.v16{{grid-template-columns:1fr}}}}
</style></head><body><main><h1>Video model blind test</h1>
<p class=lede>Frame pairs you already approved. In each pair one clip is a new video model and one is Veo 3.1 Fast, what we use now.
Sides are shuffled and both are muted. For each pair tell me X, Y or "same"; I reveal which was which after.</p>
{''.join(cards)}</main></body></html>"""
    open(os.path.join(R, "index.html"), "w").write(page)
    subprocess.run([sys.executable, os.path.join(HERE, "..", "review_server.py"), str(a.port), R], check=True)
    print(f"blind page: http://127.0.0.1:{a.port}/  (key: {a.candidate_dir}/blind-key.json)")


if __name__ == "__main__":
    P = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    S = P.add_subparsers(dest="cmd", required=True)
    s = S.add_parser("build"); s.add_argument("candidate_dir"); s.add_argument("--name", required=True); s.add_argument("--port", type=int, default=9072)
    a = P.parse_args(); globals()[a.cmd](a)
