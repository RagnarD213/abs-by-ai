"""Silent measurements for the client delivery gate."""
import bisect
import difflib
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path

SYNC_TOLERANCE = 0.2
JOINT_VIGOR_FPS = Fraction(30000, 1001)
NUMBER_WORDS = "zero one two three four five six seven eight nine ten".split()


def tokens(text):
    text = text.casefold().replace("’", "'").replace("'", "")
    text = re.sub(r"(?<=\d)\s*\+", " plus ", text)
    text = re.sub(r"(?<=\d)\s*%", " percent ", text)
    return re.findall(r"[^\W_]+", text)


def caption_token(token):
    if token.isascii() and token.isdigit() and len(token) <= 2 and int(token) < len(NUMBER_WORDS):
        return NUMBER_WORDS[int(token)]
    return token


def probe(media, ffprobe):
    result = subprocess.run(
        [ffprobe, "-v", "error", "-show_streams", "-of", "json", str(media)],
        check=True, capture_output=True, text=True,
    )
    streams = json.loads(result.stdout)["streams"]
    video = [stream for stream in streams if stream["codec_type"] == "video"
             and not stream.get("disposition", {}).get("attached_pic")]
    audio = [stream for stream in streams if stream["codec_type"] == "audio"]
    if len(video) != 1 or len(audio) != 1:
        raise ValueError("need exactly one moving picture track and one audio track")
    duration = float(video[0]["duration"])
    fps = float(Fraction(video[0]["avg_frame_rate"]))
    if not math.isfinite(duration) or not math.isfinite(fps) or min(duration, fps) <= 0:
        raise ValueError("invalid video duration or frame rate")
    if any(abs(float(stream["start_time"])) > 1 / fps for stream in [*audio, *video]):
        raise ValueError("picture or audio does not start within one frame of file time zero")
    if abs(float(audio[0]["duration"]) - duration) > max(1 / fps, 0.05):
        raise ValueError("picture and audio end at different times")
    return duration, fps


def srt_cues(path, duration, fps):
    pattern = re.compile(r"(\d{2,}:\d{2}:\d{2}[,.]\d{3})\s+-->\s+(\d{2,}:\d{2}:\d{2}[,.]\d{3})")

    def seconds(value):
        hours, minutes, seconds = value.replace(",", ".").split(":")
        return 3600 * int(hours) + 60 * int(minutes) + float(seconds)

    cues = []
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        if len(lines) < 3 or not lines[0].isdigit() or not (match := pattern.fullmatch(lines[1].strip())):
            raise ValueError(f"invalid SRT cue in {path}: {block[:85]}")
        start, end = map(seconds, match.groups())
        words = tokens(re.sub(r"<[^>]+>", "", " ".join(lines[2:])))
        if not 0 <= start < end <= duration + 1 / fps or not words:
            raise ValueError(f"SRT cue {lines[0]} has invalid timing or empty text")
        if cues and start < cues[-1][0]:
            raise ValueError("SRT cues are out of order")
        cues.append((start, end, words))
    return cues


def transcript_words(words):
    expanded = [(token, word["t"], word["e"]) for word in words for token in tokens(word["w"])]
    if not expanded or any(not 0 <= start <= end < math.inf for _, start, end in expanded):
        raise ValueError("Whisper did not produce a usable word transcript")
    return expanded


def caption_alignment(srt, words, duration, fps):
    cues = srt_cues(srt, duration, fps)
    expected = [(caption_token(token), cue) for cue, (_, _, words) in enumerate(cues) for token in words]
    words = [(caption_token(token), start, stop) for token, start, stop in words]
    # Align text first. A timing-based match could pair a delayed caption with the wrong repeat.
    alignment = difflib.SequenceMatcher(
        None, [word[0] for word in expected], [word[0] for word in words], autojunk=False,
    )
    matched = [[] for _ in cues]
    missing = []
    for tag, a, b, c, d in alignment.get_opcodes():
        if tag == "equal":
            for (_, cue), word in zip(expected[a:b], words[c:d]):
                matched[cue].append(word)
        elif (tag == "replace" and expected[a][1] == expected[b - 1][1]
              and "".join(w for w, _ in expected[a:b]) == "".join(w for w, _, _ in words[c:d])):
            # "boardgames" and "board games" have identical spoken content.
            matched[expected[a][1]].extend(words[c:d])
        elif tag in ("delete", "replace"):
            missing.append({"caption_at": cues[expected[a][1]][0], "caption": " ".join(w for w, _ in expected[a:b]),
                            "whisper": " ".join(w for w, _, _ in words[c:d])})
    timing = []
    for index, ((start, end, _), hits) in enumerate(zip(cues, matched), 1):
        for position, (word, onset, offset) in enumerate(hits):
            # Phrase SRTs supply a display interval, not an onset for every word.
            # Compare spoken and displayed intervals; also check the cue entrance
            # against its first spoken word. ASR gives a bounded word, not a point.
            outside = max(start - offset, onset - end, 0)
            if position == 0:
                outside = max(outside, onset - start)
            if outside > SYNC_TOLERANCE + 1e-9:
                timing.append({"cue": index, "caption_at": start, "spoken_at": onset,
                               "spoken_until": offset, "word": word, "outside_s": round(outside, 3)})
    # Protect against an SRT that only captions a small part of the film.
    # Insertion-only differences may be Whisper hallucinations or omitted speech.
    # Surface them as failures so legitimately unclear audio receives a new alignment.
    insertions = [{"spoken_at": words[c][1], "whisper": " ".join(w for w, _, _ in words[c:d])}
                  for tag, _, _, c, d in alignment.get_opcodes() if tag == "insert"]
    return {"result": "PASS" if not (missing or timing or insertions) else "FAIL",
            "cue_count": len(cues), "max_allowed_s": SYNC_TOLERANCE,
            "transcribed_words": len(words), "caption_words": len(expected),
            "word_mismatches": missing + insertions, "timing_violations": timing}


def check_source_ranges(data, duration, fps):
    """Check the edit decision list for the rendered revision in final-file seconds."""
    if abs(float(data["duration_s"]) - duration) > 1 / fps:
        raise ValueError("source map duration does not match the final file")
    segments = data["segments"]
    if not segments:
        raise ValueError("source map is empty")
    end = 0
    mismatches = []
    checked = 0
    for segment in segments:
        start = float(segment["start_s"])
        stop = float(segment["end_s"])
        if not 0 <= start < stop <= duration + 1 / fps or abs(start - end) > 1 / fps:
            raise ValueError(f"source map has a gap, overlap or invalid interval at {start:g}s")
        end = stop
        if segment["kind"] in ("cover", "silent"):
            if not str(segment.get("reason", "")).strip():
                raise ValueError(f"no reason given for {segment['kind']} at {start:g}s")
            continue
        if segment["kind"] != "speaker":
            raise ValueError(f"unknown source map kind {segment['kind']!r}")
        picture, audio = segment["picture"], segment["audio"]
        source_fps = float(Fraction(str(segment["source_fps"])))
        if not 0 < source_fps < math.inf:
            raise ValueError(f"invalid source fps at {start:g}s")
        times = [float(clip[key]) for clip in (picture, audio) for key in ("in_s", "out_s")]
        if not (all(math.isfinite(t) and t >= 0 for t in times)
                and times[0] < times[1] and times[2] < times[3]
                and all(str(clip["source"]).strip() for clip in (picture, audio))):
            raise ValueError(f"invalid source ranges at {start:g}s")
        deltas = [abs(times[i] - times[i + 2]) * source_fps for i in (0, 1)]
        checked += 1
        # Source-time maps are linear within a segment. The maximum drift is at one of its ends.
        if picture["source"] != audio["source"] or max(deltas) > 1 + 1e-9:
            mismatches.append({"film_start_s": start, "film_end_s": stop, "picture": picture,
                               "audio": audio, "max_source_frame_delta": max(deltas)})
    if abs(end - duration) > 1 / fps:
        raise ValueError("source map does not cover the end of the file")
    return {"result": "FAIL" if mismatches else "PASS", "speaker_segments": checked,
            "mismatches": mismatches}


def joint_vigor_plan(data, duration, fps):
    """Adapt JV's saved render plan and dialogue EDL using its camera lookup.

    The lookup and frame rounding come from R5 build/lipsync_gate.py. Use
    archived render inputs only. Moving picture/audio for the composited
    opening and other prebuilt inserts are also checked by Gemini.
    """
    plan = json.loads(Path(data["plan"]).read_text())
    edl = json.loads(Path(data["edl"]).read_text())
    plan_fps = float(JOINT_VIGOR_FPS)
    start, end, pace = map(float, (data["start_s"], data["end_s"], data["pace"]))
    if not 0 <= start < end <= plan["end"] or not 0 < pace < math.inf:
        raise ValueError("invalid Joint Vigor render range or pace")
    if abs(float(data["duration_s"]) - duration) > 1 / fps:
        raise ValueError("Joint Vigor render metadata does not match the video duration")
    excludes = [(round(a * plan_fps), round(b * plan_fps)) for a, b in data["exclude"]]
    if any(not 0 <= a < b <= round(end * plan_fps) for a, b in excludes):
        raise ValueError("invalid Joint Vigor cut range")
    shots = sorted(plan["base"], key=lambda shot: shot[0])
    if not shots:
        raise ValueError("Joint Vigor plan has no picture events")
    dialogue = sorted(edl, key=lambda row: row["film0"])
    cameras = [row for row in dialogue if row["src"] == "cam"]
    camera_starts = [row["film0"] for row in cameras]
    if not cameras:
        raise ValueError("Joint Vigor EDL has no camera recording")

    checked_frames = checked_shots = 0
    mismatches = []
    for shot, next_shot in zip(shots, shots[1:] + [[plan["end"]]]):
        left, right = max(shot[0], start), min(next_shot[0], end)
        if shot[1] != "cam" or left >= right:
            continue
        checked_shots += 1
        for audio in dialogue:
            audio_end = audio["film0"] + audio["e"] - audio["s"]
            first = math.ceil(max(left, audio["film0"]) * plan_fps)
            stop = math.ceil(min(right, audio_end) * plan_fps)
            bad = []
            for frame in range(first, stop):
                if any(a <= frame < b for a, b in excludes):
                    continue
                checked_frames += 1
                time = frame / plan_fps
                # The assembler falls back to the most recent camera take even during voiceover.
                camera_index = bisect.bisect_right(camera_starts, time + 1e-6) - 1
                picture = cameras[max(0, camera_index)]
                picture_frame, audio_frame = [
                    round((row["s"] + time - row["film0"]) * plan_fps) for row in (picture, audio)
                ]
                if audio["src"] != "cam" or abs(picture_frame - audio_frame) > 1:
                    bad.append((frame, picture["id"], picture_frame, audio_frame))
            if bad:
                frame, picture_id, picture_frame, audio_frame = bad[0]
                mismatches.append({"first_plan_frame": frame, "last_plan_frame": bad[-1][0],
                                   "count": len(bad), "picture": f"cam/{picture_id} frame {picture_frame}",
                                   "audio": f"{audio['src']}/{audio['id']} frame {audio_frame}"})
    if not checked_frames:
        raise ValueError("Joint Vigor plan contains no camera frames over dialogue at these bounds")
    return {"result": "FAIL" if mismatches else "PASS", "speaker_segments": checked_shots,
            "dialogue_frames": checked_frames, "mismatched_frames": sum(m["count"] for m in mismatches),
            "mismatches": mismatches}
