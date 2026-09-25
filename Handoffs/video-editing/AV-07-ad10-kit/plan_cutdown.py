#!/usr/bin/env python3
"""Build an evidence-contract-v2 plan for AV-07's frame-exact 9:16 cutdown."""
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import os
import sys

FPS = 30000 / 1001


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--video", required=True)
    ap.add_argument("--audit", required=True)
    ap.add_argument("--transcribe", action="store_true")
    a = ap.parse_args()

    build = os.path.abspath(a.build)
    video = os.path.abspath(a.video)
    audit = os.path.abspath(a.audit)
    cut = os.path.join(build, "cut")
    os.makedirs(os.path.join(audit, "logs"), exist_ok=True)
    os.makedirs(os.path.join(audit, "plan_assets"), exist_ok=True)

    master = json.load(open(os.path.join(build, "plan.json")))
    cut_plan = json.load(open(os.path.join(build, "cut_plan.json")))
    ranges = cut_plan["ranges"]

    def mapped_spans(beat):
        a0, a1 = (float(x) for x in beat)
        out = []
        for r in ranges:
            lo, hi = max(a0, r["src0"]), min(a1, r["src1"])
            if hi - lo >= 0.5 / FPS:
                out.append([round(r["dst0"] + lo - r["src0"], 6),
                            round(r["dst0"] + hi - r["src0"], 6)])
        return out

    def mapped_time(t):
        t = float(t)
        for r in ranges:
            if r["src0"] - 1e-6 <= t <= r["src1"] + 1e-6:
                return round(r["dst0"] + t - r["src0"], 6)
        return None

    def map_items(items):
        out = []
        for item in items or []:
            for beat in mapped_spans(item["beat"]):
                q = dict(item)
                q["beat"] = beat
                out.append(q)
        return out

    joins = {round(r["dst0"], 3) for r in ranges[1:]}
    for t in master.get("joins", []):
        mt = mapped_time(t)
        if mt is not None and 0 < mt < cut_plan["seconds"]:
            joins.add(round(mt, 3))

    def map_plain(spans):
        return [[round(x, 3), round(y, 3)] for beat in spans or [] for x, y in mapped_spans(beat)]

    mapped_covered = map_plain(master.get("covered"))
    punch, punch_covered = [], []
    for item, covered in zip(master.get("punch", []), master.get("punch_covered", [])):
        for beat in mapped_spans(item[:2]):
            cuts = sorted({beat[0], beat[1]} |
                          {x for a_, b_ in mapped_covered for x in (a_, b_)
                           if beat[0] < x < beat[1]})
            for left, right in zip(cuts, cuts[1:]):
                if right - left < 0.5 / FPS:
                    continue
                mid = (left + right) / 2
                hidden = any(a_ <= mid <= b_ for a_, b_ in mapped_covered)
                punch.append([round(left, 3), round(right, 3), item[2]])
                punch_covered.append(bool(covered or hidden))

    real_photos = map_items(master.get("real_photos"))
    ai_inserts = map_items(master.get("ai_inserts"))
    graphics = map_items(master.get("graphics"))
    graphic_regions = map_items(master.get("graphic_regions"))
    windows = map_items(master.get("talking_head_windows"))
    tracks = map_items(master.get("label_tracks"))

    sys.path.insert(0, build)
    spec = importlib.util.spec_from_file_location("cut_captions", os.path.join(build, "captions.py"))
    captions = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(captions)
    words_tuples = captions.load_words(os.path.join(cut, "words_ctc.json"))
    mute = [tuple(x) for x in json.load(open(os.path.join(cut, "mute.json")))]
    real_seams = [r["dst0"] for r, prev in zip(ranges[1:], ranges[:-1])
                  if abs(r["src0"] - prev["src1"]) > 1e-3]
    captions.BT.SEAMS = real_seams
    groups = captions.groups(words_tuples, mute)

    def ts(t):
        h = int(t // 3600)
        m = int(t % 3600 // 60)
        s = t % 60
        return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")

    stops = sorted(set([x for x, _ in mute] + real_seams))
    srt = []
    for i, g in enumerate(groups, 1):
        nxt = groups[i][0][1] if i < len(groups) else None
        ws, we = g[-1][1], g[-1][2]
        hold = max(we, ws + 0.12)
        end = min(nxt, max(hold, min(nxt, we + 0.8))) if nxt is not None else we + 0.3
        end = max(end, ws + 1.0 / FPS)
        stop = next((x for x in stops if x > ws + 1e-3), None)
        if stop is not None:
            end = max(min(end, stop), ws + 1.0 / FPS)
        srt.append(f"{i}\n{ts(g[0][1])} --> {ts(end)}\n{' '.join(x[0] for x in g)}\n")
    srt_path = os.path.join(audit, "plan_assets", "captions.srt")
    open(srt_path, "w").write("\n".join(srt))

    words = [dict(w=w, t=round(t, 3), e=round(e, 3)) for w, t, e in words_tuples]
    manifest = json.load(open(os.path.join(cut, "cap", "manifest.json")))
    plan = dict(
        target_seconds=round(cut_plan["seconds"], 6),
        target_frames=int(cut_plan["frames"]),
        joins=sorted(joins),
        covered=mapped_covered,
        cards=map_plain(master.get("cards")),
        punch=punch,
        punch_covered=punch_covered,
        real_photos=real_photos,
        ai_inserts=ai_inserts,
        graphics=graphics,
        label_chips=master.get("label_chips", {}),
        label_pos=master.get("label_pos", {}),
        srt=srt_path,
        words=words,
        source_audio=os.path.join(cut, "his_mix.wav"),
        watch_log=os.path.join(audit, "logs", "watch_pass.json"),
        banned_source=master.get("banned_source"),
        banned_times=master.get("banned_times", []),
        caption_states=manifest["caption_states"],
        caption_highlight_rgb=[140, 153, 91],
        speech_words=words,
        speech_words_evidence=dict(method="verbatim_source_ctc"),
        graphic_regions=graphic_regions,
        talking_head_windows=windows,
        label_tracks=tracks,
        evidence_contract=dict(version=2, video_sha256=sha(video),
                               generated_at=datetime.datetime.now(datetime.timezone.utc).isoformat()),
        cut=dict(ranges=ranges, source_video=os.path.join(build, "ad10_9x16_review.mp4")),
    )
    if a.transcribe:
        import whisper
        result = whisper.load_model("small").transcribe(video, word_timestamps=False, language="en")
        plan["transcript_words"] = [dict(w=w) for seg in result["segments"] for w in seg["text"].split()]
    old_path = os.path.join(audit, "plan.json")
    if os.path.exists(old_path):
        old = json.load(open(old_path))
        for key in ("negative_events_scan", "label_clearance", "declare"):
            if key in old:
                plan[key] = old[key]
    json.dump(plan, open(old_path, "w"), indent=1)
    print(f"cut plan: {len(joins)} joins, {len(groups)} caption cues, {len(tracks)} labels, "
          f"{len(windows)} windows, sha {sha(video)[:12]}")


if __name__ == "__main__":
    main()
