"""RO-19 round 4 media (Dan's two round 3 notes, 2026-10-13: his photo at 0:48, the false start at 9:07 out). Round 3's script pointed at round4/. usage: round4_19.py bed | first | film | excerpts
bed:      the quiet music bed for the whole film (bed.py: Pixabay acoustic_bg, the bed of the approved RO-05 / RO-06 / RO-07 / RO-12 films), round3/bed/bed.wav (round 4 does not rebuild it)
first:    the first minute as a preflight (new P02, voice B2, the bed), round4/first-minute/
film:     the full film, round4/film/. Pre-flights every clip against its slot first (RO-06: one short clip killed a full render at minute 11).
excerpts: review copies cut from the MASTER (never a separate render): the first minute, each changed item with 3 s either side.
Builds in round4/ only; rounds 1 to 3 are never touched. The music bed is round 3's own file, unchanged."""
import sys, os, json, subprocess
sys.path.insert(0, "/Volumes/Extreme/_edit_work/ro19/recipe")
W = "/Volumes/Extreme/_edit_work/ro19"; OUT = f"{W}/round4"
BED = f"{W}/round3/bed/bed.wav"; BED_DB = "-30"     # ROUND 4: the SAME bed file as the film Dan approved, byte for byte (sha256 3720759c...fb2b; `bed` is not run in round 4). It is 1121.4 s long, so it fades out 5 s before the end of this film (7 s before the end of round 3's). Round 3's note: the chain's ceiling; RO-07 measured -30 against the gate's floor row (+1.1 / +1.2 / +4.2, limit -3.0)
if sys.argv[1] != "bed": os.environ["RO07_BED"] = BED; os.environ["RO07_BED_DB"] = BED_DB
import build as Bd, gfx as G
FF = Bd.FF; total = Bd.S[-1]["out_f1"]/Bd.FPS
FM = f"{OUT}/first-minute/RO-19 round 4 - first minute.mp4"; FILM = f"{OUT}/film/RO-19 round 4 - full film.mp4"
def first_end():
    lim = max([60.0] + [it["t1"] + 0.3 for it in Bd.R if it["t0"] < 60.0])
    return min(s["out_f0"] for s in Bd.S if s["out_f0"]/Bd.FPS >= lim)/Bd.FPS
def review_copy(src, dst, a=None, b=None, poster_t=1.5):
    cut = [] if a is None else ["-ss", f"{a:.3f}", "-t", f"{b-a:.3f}"]
    subprocess.run([FF, "-v", "error", "-y"] + cut + ["-i", src, "-vf", "scale=960:540", "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", dst], check=True)
    subprocess.run([FF, "-v", "error", "-y", "-ss", str(poster_t), "-i", dst, "-frames:v", "1", "-q:v", "3", dst[:-4] + ".jpg"], check=True)
def preflight():
    assert Bd.fr(total) == Bd.S[-1]["out_f1"]; assert not Bd.jumps(), Bd.jumps()
    assert not [i["id"] for i in Bd.R if i.get("pending") or i.get("frames")], "a placeholder is still in the plan"
    ffp = FF.replace("ffmpeg", "ffprobe")
    for it in Bd.R:
        if it["kind"] != "clip": continue
        n = Bd.fr(it["t1"]) - Bd.fr(it["t0"]); s = it["src"]; per = n // len(s)
        for k, sp in enumerate(s):
            m = per if k < len(s)-1 else n - per*(len(s)-1); p = G.src_path(sp); assert os.path.exists(p), p
            dur = float(subprocess.run([ffp, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
            assert dur - G.src_start(sp) >= m/Bd.FPS - 0.02, f"{it['id']}: {sp} too short for its slot"
    print("preflight ok:", sum(i["kind"] == "clip" for i in Bd.R), "clips,", len(Bd.all_segments()), "segments", flush=True)
if __name__ == "__main__":
    what = sys.argv[1]
    assert what != "bed", "round 4 uses round 3's bed file as it is"
    if what == "bed":
        import bed; os.makedirs(os.path.dirname(BED), exist_ok=True); bed.build_bed(total, BED); print("bed", round(total, 3), "s")
    if what == "first":
        preflight(); os.makedirs(os.path.dirname(FM), exist_ok=True); e = first_end(); Bd.render_range(0.0, e, FM); print("first minute to", round(e, 2), flush=True)
    if what == "film":
        preflight(); os.makedirs(os.path.dirname(FILM), exist_ok=True); print("rendering", Bd.S[-1]["out_f1"], "frames", round(total, 3), "s", flush=True)
        Bd.render_range(0, total, FILM); print("RENDER COMPLETE", flush=True)
    if what == "excerpts":
        os.makedirs(f"{OUT}/review", exist_ok=True); e = first_end()
        review_copy(FILM, f"{OUT}/review/full-film - REVIEW 540p.mp4", poster_t=1.5)
        subprocess.run([FF, "-v", "error", "-y", "-i", FILM, "-t", f"{e:.3f}", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", f"{OUT}/review/first-minute.mp4"], check=True)
        review_copy(FILM, f"{OUT}/review/first-minute - REVIEW 540p.mp4", 0, e)
        for i in sys.argv[2:]:
            it = next(r for r in Bd.R if r["id"] == i); a, b = max(0.0, it["t0"]-3.0), min(total, it["t1"]+3.0)
            review_copy(FILM, f"{OUT}/review/{i}-context - REVIEW 540p.mp4", a, b, poster_t=min(it["t0"]-a+1.5, b-a-0.5)); print("excerpt", i, round(a, 1), round(b, 1), flush=True)
