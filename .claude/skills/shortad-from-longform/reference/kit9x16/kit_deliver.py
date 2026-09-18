#!/usr/bin/env python3
"""THE KIT'S BUILD ORDER, as one script with numbered stages, each resumable. Nothing here decides
design (build_kit.py did) and nothing here grades (the shared gate does).

  python3 kit_deliver.py setup   --build DIR --from-build SRC        copy the pipeline + link the asset dirs
  python3 kit_deliver.py audio   --build DIR --mode master --approved <approved vertical.mp4>
                                 (his mix, untouched: stream-copied into his_audio.m4a, decoded to his_mix.wav)
  python3 kit_deliver.py words   --build DIR                          ref.whisper.json -> words_ctc.json (a2/align_ctc.py)
  python3 kit_deliver.py picture --build DIR                          render.py (all beats) -> picture.mp4
  python3 kit_deliver.py captions --build DIR                         captions.py -> captions.mov + cap/manifest.json
  python3 kit_deliver.py mux     --build DIR --out NAME.mp4           picture + captions + his audio (copy) -> master
  python3 kit_deliver.py gate    --build DIR --video NAME.mp4 [--reference-cut his.mp4] [--banned-source .. --banned-times ..]
                                 audio_gate (--reference-mix --verbatim) -> plan -> watch pass -> deliver gate
  python3 kit_deliver.py review  --build DIR --video NAME.mp4         540p review copy

Stages that the shared modules own are only CALLED here: _shared/audio/audio_gate.py, _shared/deliver/watch.py,
_shared/deliver/gate.py. The watch pass's JUDGE is a fresh subagent (watch/JUDGE_PROMPT.md), never this script.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.abspath(os.path.join(HERE, ".."))                 # shortad-from-longform/reference
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
FF = os.path.join(REPO, "Media/video_edit/bin/ffmpeg")
FP = FF.replace("ffmpeg", "ffprobe")
SHARED = os.path.join(REPO, ".claude/skills/_shared")
PY = sys.executable
FPS = 30000 / 1001


def run(cmd, cwd=None):
    print("$", " ".join(os.path.basename(c) if i == 0 else c for i, c in enumerate(cmd))[:300], flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def setup(a):
    os.makedirs(a.build, exist_ok=True)
    for f in ("render.py", "vlib.py", "captions.py", "mux.py"):
        shutil.copy(os.path.join(REF, f), os.path.join(a.build, f))
    shutil.copy(os.path.join(REF, "a2", "align_ctc.py"), os.path.join(a.build, "align_ctc.py"))
    for f in ("grade.py", "assets.py"):
        src = os.path.join(a.from_build, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(a.build, f))
    for d in ("stock", "stock2", "stock3", "stock4", "assets_v", "aigen", "assets", "music"):
        src = os.path.join(a.from_build, d)
        dst = os.path.join(a.build, d)
        if os.path.isdir(src) and not os.path.exists(dst):
            os.symlink(src, dst)
    for d in ("out", "gfx", "logs", "cap"):
        os.makedirs(os.path.join(a.build, d), exist_ok=True)
    print(f"{a.build}: pipeline copied from the skill, grade/assets from {a.from_build}, asset dirs linked")


def audio(a):
    os.chdir(a.build)
    if a.mode == "master":
        if not a.approved:
            raise SystemExit("--mode master needs --approved <the approved vertical whose audio is reused>")
        # ⚠ AN EDITOR'S FINISHED MIX SHIPS UNTOUCHED (AGENTS.md 2026-09-10). The approved vertical carries his
        # mix at the approved constant-gain treatment; it is stream-copied here, bit for bit, and gated in
        # --reference-mix --verbatim mode against its own decode.
        run([FF, "-nostdin", "-v", "error", "-y", "-i", a.approved, "-map", "0:a:0", "-c:a", "copy", "his_audio.m4a"])
        run([FF, "-nostdin", "-v", "error", "-y", "-i", a.approved, "-map", "0:a:0", "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", "his_mix.wav"])
        md5 = subprocess.run([FF, "-v", "error", "-i", a.approved, "-map", "0:a:0", "-c:a", "copy", "-f", "md5", "-"],
                             capture_output=True, text=True).stdout.strip()
        json.dump(dict(source=os.path.abspath(a.approved), audio_stream_md5=md5, mode="verbatim-copy"), open("audio_source_kit.json", "w"), indent=1)
        print("his audio:", md5)
    else:
        raise SystemExit("from-raw audio is built by kit_audio.py (voice_chain + bed + ticks); not this stage")


def words(a):
    os.chdir(a.build)
    if not os.path.exists("ref.whisper.json"):
        raise SystemExit("ref.whisper.json (the mix's Whisper transcript with word timings) must be in the build dir")
    if not os.path.exists("his_mix.wav"):
        raise SystemExit("his_mix.wav missing -- run the audio stage first")
    if os.path.exists("words_ctc.json"):
        os.remove("words_ctc.json")      # the aligner's OUTPUT; left over, captions.load_words() reads it as the input
                                         # and the FIX map never re-applies (from-raw pass 6: 777 stale vs 769 fixed words)
    run([PY, "align_ctc.py"], cwd=a.build)


def picture(a):
    os.chdir(a.build)
    if not os.path.exists("facetrack.json"):
        raise SystemExit("facetrack.json missing -- run kit_track.py first")
    run([PY, "render.py", "--selftest"], cwd=a.build)
    run([PY, "render.py"], cwd=a.build)


def captions(a):
    os.chdir(a.build)
    run([PY, "captions.py"], cwd=a.build)


def mux(a):
    os.chdir(a.build)
    sys.path.insert(0, os.getcwd())
    import beats as B
    plan = round(B.DUR * FPS)
    aud = "his_audio.m4a" if os.path.exists("his_audio.m4a") else "audio_final.wav"
    acodec = ["-c:a", "copy"] if aud.endswith(".m4a") else ["-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2"]
    run([FF, "-nostdin", "-v", "error", "-y", "-i", "picture.mp4", "-i", "captions.mov", "-i", aud,
         "-filter_complex", "[0:v][1:v]overlay=0:0:eof_action=pass:format=auto[v]", "-map", "[v]", "-map", "2:a",
         "-r", "30000/1001", "-frames:v", str(plan), "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
         "-video_track_timescale", "30000"] + acodec + ["-movflags", "+faststart", a.out])
    n = subprocess.run([FP, "-v", "error", "-select_streams", "v", "-count_frames", "-show_entries", "stream=nb_read_frames",
                        "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout.strip().split(",")[0]
    if int(n) != plan:
        raise SystemExit(f"FRAME COUNT {n} != PLAN {plan}")
    if aud.endswith(".m4a"):
        md5 = subprocess.run([FF, "-v", "error", "-i", a.out, "-map", "0:a:0", "-c:a", "copy", "-f", "md5", "-"],
                             capture_output=True, text=True).stdout.strip()
        want = json.load(open("audio_source_kit.json"))["audio_stream_md5"]
        if md5 != want:
            raise SystemExit(f"audio stream changed in the mux: {md5} != {want}")
        print("audio stream bit-identical to the approved vertical's:", md5)
    print(f"{a.out}: {n} frames")


def gate(a):
    os.chdir(a.build)
    v = a.video
    # 1. the audio gate: his mix, verbatim
    cmd = [PY, os.path.join(SHARED, "audio/audio_gate.py"), v, "--reference-mix", "his_mix.wav", "--verbatim"]
    run(cmd)
    # 2. the plan, bound to this file
    cmd = [PY, os.path.join(HERE, "kit_plan.py"), "--build", a.build, "--video", v, "--transcribe"]
    if a.reference_cut:
        cmd += ["--reference-cut", a.reference_cut]
    if a.banned_source:
        cmd += ["--banned-source", a.banned_source, "--banned-times"] + [str(t) for t in (a.banned_times or [])]
    env = dict(os.environ, PATH=os.path.dirname(FF) + ":" + os.environ.get("PATH", ""))
    print("$ kit_plan.py ... --transcribe", flush=True)
    subprocess.run(cmd, check=True, env=env)
    # 3. the watch pass (scan + strips + sheets); the judge is a fresh subagent, then --judge, then the gate
    run([PY, os.path.join(SHARED, "deliver/watch.py"), v, "--plan", "plan.json"])
    print("\nNEXT: a fresh subagent judges watch/ (see watch/JUDGE_PROMPT.md), then\n"
          f"  python3 {SHARED}/deliver/watch.py --judge logs/watch_pass.json --findings logs/findings.json --by <who>\n"
          f"  python3 {SHARED}/deliver/gate.py {v} --format ad9x16 --plan plan.json")


def review(a):
    os.chdir(a.build)
    out = a.video.replace(".mp4", "_REVIEW_540p.mp4")
    run([FF, "-nostdin", "-v", "error", "-y", "-i", a.video, "-vf", "scale=540:960", "-c:v", "libx264", "-preset", "medium",
         "-crf", "23", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out])
    print(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup"); s.add_argument("--build", required=True); s.add_argument("--from-build", required=True)
    s = sub.add_parser("audio"); s.add_argument("--build", required=True); s.add_argument("--mode", required=True); s.add_argument("--approved")
    s = sub.add_parser("words"); s.add_argument("--build", required=True)
    s = sub.add_parser("picture"); s.add_argument("--build", required=True)
    s = sub.add_parser("captions"); s.add_argument("--build", required=True)
    s = sub.add_parser("mux"); s.add_argument("--build", required=True); s.add_argument("--out", required=True)
    s = sub.add_parser("gate"); s.add_argument("--build", required=True); s.add_argument("--video", required=True)
    s.add_argument("--reference-cut"); s.add_argument("--banned-source"); s.add_argument("--banned-times", nargs="*", type=float)
    s = sub.add_parser("review"); s.add_argument("--build", required=True); s.add_argument("--video", required=True)
    a = ap.parse_args()
    return dict(setup=setup, audio=audio, words=words, picture=picture, captions=captions, mux=mux, gate=gate, review=review)[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
