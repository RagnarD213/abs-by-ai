#!/usr/bin/env python3
"""Give every queued TikTok post a DESIGNED cover instead of a random screenshot.

WHY THIS EXISTS
---------------
TikTok's Content Posting API -- which is all Blotato can drive -- has no field for a cover
IMAGE. The only cover control it offers is `video_cover_timestamp_ms`, a timestamp INTO the
video (Blotato exposes it as the target field `videoCoverTimestamp`). Instagram's API does
take a real image (`coverImageUrl`), which is why the same short shows a designed cover on
Reels and a mid-sentence screenshot on TikTok.

Measured on @absbyai 2026-09-17: with no timestamp sent, TikTok uses FRAME 0. Three published
videos were downloaded and their frame 0 matched the profile-grid tile pixel for pixel. The
handful of tiles that DO look designed ("The Truth About Supplements", "Home Ab Workout") are
older videos that happen to open on a title card.

So the only way to put a designed cover on TikTok is to make frame 0 BE the designed cover.
This script prepends the post's existing Instagram cover PNG as a single frame (1/24 s) and
pins `videoCoverTimestamp: 0`. One frame is below the threshold of perception in playback, so
the viewer's experience is unchanged -- only the grid tile changes.

The prepend is LOSSLESS. The video is stream-copied (concat demuxer, `-c copy`) and the audio
is mapped straight off the original with `-itsoffset`, so the audio stream is bit-identical,
never re-encoded and never re-muxed at a join. That matters: under AGENTS.md an editor's mix is
delivered untouched. Verified on abwheel/v3 shorts -- video frames 1560 -> 1561, audio packets
3048 -> 3048, full decode with zero errors.

COVER SOURCE
------------
A TikTok post's cover comes from its Instagram twin, which carries the designed PNG in
`target.coverImageUrl`. The twin is found by campaign key (utm_content) or by media url --
see plan() for why both are needed. All 21 queued TikTok posts resolved on 2026-09-17. A post
with no twin needs a cover built (see /coverimage) and passed in --covers.

BLOTATO CANNOT EDIT A SCHEDULED POST, so --apply is create-then-delete, exactly as
swap_media.py does it: recreate the post with the identical account, caption, scheduledAt and
target plus the new mediaUrl and videoCoverTimestamp, verify the new schedule exists, then
delete the old id. The old post's full body is written to cover_backup/ before the delete.

Idempotent: a post whose target already carries `videoCoverTimestamp` is done and is skipped.

    python3 scripts/blotato/tiktok_cover.py                      # plan: what resolves, what doesn't
    python3 scripts/blotato/tiktok_cover.py --build              # build the mp4s into work/
    python3 scripts/blotato/tiktok_cover.py --apply --urls U.json  # rebuild the schedules

UPLOADING
---------
Blotato has no REST route for a presigned upload (probed 2026-09-17: /media/presigned-upload-url,
/media/upload-url, /media/presign, /media/signed-url, /uploads/presigned-url all 404;
`POST /v2/media {"url": ...}` only re-hosts an already-public URL). Minting a presigned PUT is
only exposed through the Blotato MCP tool `blotato_create_presigned_upload_url`. So --build
emits work/UPLOAD.md listing each file to upload, and --apply reads U.json:

    {"<schedule id>": "<publicUrl returned with the presigned upload>", ...}
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from danrosefit_migration import api_key, call, fetch_schedules  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.path.join(HERE, "cover_work")
BACKUP = os.path.join(HERE, "cover_backup")
FFMPEG = os.path.join(ROOT, "Media", "video_edit", "bin", "ffmpeg")
FFPROBE = os.path.join(ROOT, "Media", "video_edit", "bin", "ffprobe")

TIKTOK = "58181"


def run(cmd: list, **kw):
    p = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if p.returncode:
        raise SystemExit(f"FAILED: {' '.join(cmd[:4])}...\n{p.stderr[-2000:]}")
    return p.stdout.strip()


def probe(path: str) -> dict:
    """The parameters the cover frame has to match for a lossless concat."""
    out = run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries",
               "stream=width,height,r_frame_rate,profile,level,pix_fmt", "-of", "json", path])
    v = json.loads(out)["streams"][0]
    num, den = v["r_frame_rate"].split("/")
    return {"w": v["width"], "h": v["height"], "fps": float(num) / float(den),
            "profile": v.get("profile", "High").lower(), "level": v.get("level", 40),
            "pix_fmt": v.get("pix_fmt", "yuv420p")}


def fetch(url: str, dest: str):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return dest
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        f.write(r.read())
    return dest


def cover_filter(w: int, h: int) -> str:
    """Fit the (9:16) cover into a w x h frame WITHOUT distorting it.

    The first version scaled the cover straight to w x h. On a 16:9 long-form that squashed a
    1080x1920 cover into 1920x1080 -- 3x too wide -- and TikTok's grid showed the stretched
    headline (Dan, 2026-09-22: the 1-minute workout and ab-wheel long-forms).

    TikTok's profile grid is a 3:4 centre crop of the video. A 9:16 post therefore shows the
    middle 3:4 of its cover. For a landscape video we lay the cover out so the grid's centre
    3:4 window shows EXACTLY that same region: scale the cover to the window's width (h*3/4),
    keep its middle h pixels, and fill the sides with a dark blur of the cover. The grid tile
    then matches every 9:16 post's tile; the full frame only shows for 1/24 s.
    """
    if w > h:
        tw = int(round(h * 3 / 4 / 2)) * 2
        return (f"[0:v]split[a][b];"
                f"[a]scale={w}:{h}:force_original_aspect_ratio=increase:flags=lanczos,crop={w}:{h},"
                f"boxblur=30:3,eq=brightness=-0.35[bg];"
                f"[b]scale={tw}:-2:flags=lanczos,crop={tw}:'min(ih,{h})'[fg];"
                f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,format=yuv420p")
    # Portrait / square: preserve aspect, centre, pad dark. A 1080x1920 cover on a 1080x1920
    # video is a plain 1:1 copy.
    return (f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease:flags=lanczos,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,format=yuv420p")


def render_cover_frame(cover: str, w: int, h: int, dest: str) -> str:
    """The exact still build() puts in frame 0 -- also what to upload in the TikTok app."""
    run([FFMPEG, "-v", "error", "-y", "-i", cover, "-filter_complex", cover_filter(w, h),
         "-frames:v", "1", dest])
    return dest


def build(video: str, cover: str, dest: str, hold_frames: int = 1) -> dict:
    """Prepend `cover` as `hold_frames` frames of `video`. Video copied, audio untouched."""
    p = probe(video)
    tmp = dest + ".parts"
    os.makedirs(tmp, exist_ok=True)
    cov_v, src_v = os.path.join(tmp, "cover_v.mp4"), os.path.join(tmp, "src_v.mp4")
    # The cover clip must decode to exactly the source's raw parameters or `-c copy` refuses to
    # concat. Timescale is pinned too: a mismatched one makes the join stutter.
    run([FFMPEG, "-loglevel", "error", "-y", "-loop", "1", "-framerate", f"{p['fps']}",
         "-i", cover, "-frames:v", str(hold_frames),
         "-filter_complex", cover_filter(p["w"], p["h"]),
         "-c:v", "libx264", "-profile:v", p["profile"], "-level", str(p["level"] / 10),
         "-pix_fmt", p["pix_fmt"], "-preset", "veryslow", "-crf", "14",
         "-video_track_timescale", "12288", "-an", cov_v])
    run([FFMPEG, "-loglevel", "error", "-y", "-i", video, "-map", "0:v", "-c", "copy",
         "-video_track_timescale", "12288", src_v])
    lst = os.path.join(tmp, "concat.txt")
    with open(lst, "w") as f:
        f.write(f"file '{cov_v}'\nfile '{src_v}'\n")
    # -itsoffset delays the ORIGINAL audio stream by the cover's duration and maps it whole, so
    # the audio is one continuous copied stream -- no second AAC segment, no join, no click.
    offset = hold_frames / p["fps"]
    run([FFMPEG, "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst,
         "-itsoffset", f"{offset:.6f}", "-i", video, "-map", "0:v", "-map", "1:a",
         "-c", "copy", "-movflags", "+faststart", dest])
    return verify(video, dest, hold_frames, cover)


def cover_psnr(out: str, cover: str, tmp: str) -> float:
    """Frame 0 of the BUILT file against the cover it was supposed to get.

    Not paranoia: this loop resolves a cover per post from a twin lookup, and a mispaired
    cover -- someone else's headline over Dan's video -- would look deliberate and ship.
    A correct pairing measures ~43 dB; a wrong one is in the teens.
    """
    from PIL import Image  # noqa: PLC0415 -- optional, only needed for this check
    # Compare against the frame cover_filter() SHOULD have produced, at the video's own aspect,
    # so a distorted layout fails here instead of shipping (the 2026-09-22 squash passed a
    # check that stretched both sides to the same 180x320).
    os.makedirs(tmp, exist_ok=True)
    p = probe(out)
    a_png, b_png = os.path.join(tmp, "qc_f0.png"), os.path.join(tmp, "qc_cov.png")
    exp = render_cover_frame(cover, p["w"], p["h"], os.path.join(tmp, "qc_expected.png"))
    size = "320:180" if p["w"] > p["h"] else "180:320"
    run([FFMPEG, "-v", "error", "-y", "-i", out, "-frames:v", "1", "-vf", f"scale={size}", a_png])
    run([FFMPEG, "-v", "error", "-y", "-i", exp, "-vf", f"scale={size}", b_png])
    da = list(Image.open(a_png).convert("L").getdata())
    db = list(Image.open(b_png).convert("L").getdata())
    mse = sum((x - y) ** 2 for x, y in zip(da, db)) / len(da)
    return 99.0 if mse == 0 else 10 * math.log10(255 * 255 / mse)


def verify(src: str, out: str, hold_frames: int, cover: str | None = None) -> dict:
    """A check that did not run is a failure (AGENTS.md). Every row here is measured."""
    def frames(path):
        return int(run([FFPROBE, "-v", "error", "-select_streams", "v", "-count_frames",
                        "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path]))

    def apkts(path):
        return int(run([FFPROBE, "-v", "error", "-select_streams", "a", "-count_packets",
                        "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path]))

    decode = subprocess.run([FFMPEG, "-v", "error", "-i", out, "-f", "null", "-"],
                            capture_output=True, text=True)
    res = {
        "frames_src": frames(src), "frames_out": frames(out),
        "audio_pkts_src": apkts(src), "audio_pkts_out": apkts(out),
        "decode_errors": decode.stderr.strip()[:400],
    }
    # A check that did not run is a FAILURE, never a silent skip (AGENTS.md).
    res["cover_psnr"] = cover_psnr(out, cover, out + ".parts") if cover else None
    res["ok"] = (res["frames_out"] == res["frames_src"] + hold_frames
                 and res["audio_pkts_out"] == res["audio_pkts_src"]
                 and not res["decode_errors"]
                 and res["cover_psnr"] is not None and res["cover_psnr"] >= 30)
    return res


def utm_key(item: dict) -> str | None:
    """utm_content is unique per short and survives the platform rewrite of the caption."""
    blob = item["draft"]["content"]["text"] + " " + (item["draft"]["target"].get("firstComment") or "")
    m = re.search(r"utm_content=([A-Za-z0-9_\-]+)", blob)
    return m.group(1) if m else None


def plan(items: list, covers: dict) -> list:
    """Match every queued TikTok post to the designed cover its Instagram twin carries.

    Two keys, because neither alone is enough: Blotato re-hosts the same file under a NEW uuid
    per post, so Instagram and TikTok usually carry different media urls (13/21 matched by url),
    while one backfill reel carries no utm_content (20/21 matched by campaign key). Together
    they resolve all 21.
    """
    by_media, by_utm = {}, {}
    for i in items:
        if i["draft"]["content"]["platform"] != "instagram":
            continue
        cov = i["draft"]["target"].get("coverImageUrl")
        if not cov:
            continue
        url = (i["draft"]["content"].get("mediaUrls") or [None])[0]
        if url:
            by_media.setdefault(url, cov)
        k = utm_key(i)
        if k:
            by_utm.setdefault(k, cov)

    rows = []
    for i in items:
        d = i["draft"]
        if d["content"]["platform"] != "tiktok":
            continue
        sid = str(i["id"])
        url = (d["content"].get("mediaUrls") or [None])[0]
        src = ("override" if covers.get(sid) else
               "instagram:utm" if by_utm.get(utm_key(i)) else
               "instagram:media" if by_media.get(url) else None)
        rows.append({
            "id": sid, "when": i["scheduledAt"], "media": url,
            "cover": covers.get(sid) or by_utm.get(utm_key(i)) or by_media.get(url),
            "cover_from": src,
            "done": d["target"].get("videoCoverTimestamp") is not None,
            "hook": d["content"]["text"].split("\n")[0][:58],
            "item": i,
        })
    return sorted(rows, key=lambda r: r["when"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true", help="download + build the cover-prefixed mp4s")
    ap.add_argument("--apply", action="store_true", help="rebuild the schedules (needs --urls)")
    ap.add_argument("--urls", help="JSON {schedule id: publicUrl} of the uploaded builds")
    ap.add_argument("--covers", help="JSON {schedule id: /path/to/cover.png} for posts with no IG twin")
    ap.add_argument("--only", help="comma-separated schedule ids")
    ap.add_argument("--sources", help="JSON {schedule id: /path/to/source.mp4}; use when the queued "
                    "media already carries a (bad) cover frame, so it is not stacked twice")
    ap.add_argument("--redo", action="store_true",
                    help="with --only: rebuild posts already marked covered (e.g. a squashed cover)")
    ap.add_argument("--hold-frames", type=int, default=1,
                    help="frames the cover is held for (1 = imperceptible, the default)")
    a = ap.parse_args()

    covers = json.load(open(a.covers)) if a.covers else {}
    sources = json.load(open(a.sources)) if a.sources else {}
    key = api_key()
    rows = plan(fetch_schedules(key), covers)
    if a.only:
        keep = set(a.only.split(","))
        rows = [r for r in rows if r["id"] in keep]
        if a.redo:
            for r in rows:
                r["done"] = False

    todo = [r for r in rows if not r["done"] and r["cover"]]
    blocked = [r for r in rows if not r["done"] and not r["cover"]]
    print(f"queued TikTok posts: {len(rows)}   already covered: {sum(r['done'] for r in rows)}   "
          f"ready: {len(todo)}   need a cover built: {len(blocked)}")
    for r in rows:
        mark = "done" if r["done"] else ("->" if r["cover"] else "NO COVER")
        print(f"  {r['id']:>8} {r['when'][:10]} {mark:>8}  {r['hook']}")
    if blocked:
        print("\nNo designed cover exists for these -- build one with /coverimage and pass --covers:")
        for r in blocked:
            print(f"  {r['id']}  {r['hook']}")

    if not (a.build or a.apply):
        return

    if a.build:
        os.makedirs(WORK, exist_ok=True)
        manifest = []
        for r in todo:
            vid = sources.get(r["id"]) or fetch(r["media"], os.path.join(WORK, f"{r['id']}_src.mp4"))
            covpath = r["cover"]
            if covpath.startswith("http"):
                ext = ".png" if ".png" in covpath.lower() else ".jpg"
                covpath = fetch(covpath, os.path.join(WORK, f"{r['id']}_cover{ext}"))
            out = os.path.join(WORK, f"{r['id']}_covered.mp4")
            print(f"\nbuilding {r['id']} ...", flush=True)
            res = build(vid, covpath, out, a.hold_frames)
            print(f"  frames {res['frames_src']} -> {res['frames_out']}   "
                  f"audio packets {res['audio_pkts_src']} -> {res['audio_pkts_out']}   "
                  f"cover match {res['cover_psnr']:.1f} dB   "
                  f"{'PASS' if res['ok'] else 'FAIL ' + res['decode_errors']}")
            if not res["ok"]:
                raise SystemExit(f"{r['id']}: build failed verification, nothing uploaded")
            manifest.append({"id": r["id"], "file": out, "when": r["when"], "hook": r["hook"]})
        with open(os.path.join(WORK, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=1)
        with open(os.path.join(WORK, "UPLOAD.md"), "w") as f:
            f.write("# Upload these, then run --apply --urls U.json\n\n"
                    "For each file: mint a presigned upload with the Blotato MCP tool\n"
                    "`blotato_create_presigned_upload_url`, PUT the bytes, and record its publicUrl.\n\n"
                    "    curl -X PUT \"<presignedUrl>\" --data-binary \"@<file>\"\n\n")
            for m in manifest:
                f.write(f"- `{m['id']}` {m['when'][:10]} — `{m['file']}`  ({m['hook']})\n")
        print(f"\nbuilt {len(manifest)} files -> {WORK}\nnext: {WORK}/UPLOAD.md")

    if a.apply:
        if not a.urls:
            raise SystemExit("--apply needs --urls U.json {schedule id: publicUrl}")
        urls = json.load(open(a.urls))
        os.makedirs(BACKUP, exist_ok=True)
        for r in todo:
            new_url = urls.get(r["id"])
            if not new_url:
                print(f"{r['id']}: no uploaded url, skipped")
                continue
            it, d = r["item"], r["item"]["draft"]
            body = {"post": {"accountId": d["accountId"],
                             "target": {**d["target"], "videoCoverTimestamp": 0},
                             "content": {**d["content"], "mediaUrls": [new_url]}},
                    "scheduledTime": it["scheduledAt"]}
            json.dump(it, open(os.path.join(BACKUP, f"{r['id']}.json"), "w"), indent=1)
            print(f"{r['id']} {r['when'][:10]}: {r['hook']}")
            call("DELETE", f"/schedules/{r['id']}", key)
            print("   deleted old (backup on disk)")
            call("POST", "/posts", key, body)
            # Blotato's schedule list lags its own create. A single read 3 s later reported
            # "not found" for 6 of 21 posts on 2026-09-17 that had in fact all been created --
            # an alarming false failure that invites a human to double-create. Poll instead.
            new = []
            for attempt in range(8):
                time.sleep(3)
                new = [s for s in fetch_schedules(key)
                       if s["draft"]["accountId"] == TIKTOK
                       and s["scheduledAt"] == it["scheduledAt"]
                       and s["draft"]["content"].get("mediaUrls") == [new_url]
                       and s["draft"]["target"].get("videoCoverTimestamp") == 0]
                if new:
                    break
            if not new:
                print(f"   !! still not visible after 24 s -- CHECK THE QUEUE BEFORE RETRYING "
                      f"(it may exist); backup {BACKUP}/{r['id']}.json")
                continue
            print(f"   verified new schedule {new[0]['id']}, cover pinned at frame 0")


if __name__ == "__main__":
    main()
