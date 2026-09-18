#!/usr/bin/env python3
"""Build and search permanent metadata sidecars for source footage rolls.

The source video is never modified. Each build writes a Markdown and JSON sidecar
beside the clip, heavy artifacts in <stem>.roll/, and a text-only mirror under
Media/footage-index so search still works when the source drive is unplugged.
"""

import argparse
import base64
import copy
import datetime as dt
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request


VIDEO_EXTENSIONS = {".mp4", ".mov", ".mxf", ".m4v", ".avi", ".mts", ".m2ts", ".insv"}
SAMPLE_BYTES = 64 * 1024 * 1024
SCHEMA_VERSION = 1
DEFAULT_MODEL = "gemini-3.1-flash-lite"
DESCRIPTION_INPUT_USD_PER_M = 0.25
DESCRIPTION_OUTPUT_USD_PER_M = 1.50


def repo_root():
    override = os.environ.get("ROLL_REPO_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    return Path(__file__).resolve().parents[4]


def mirror_root():
    override = os.environ.get("ROLL_MIRROR_ROOT")
    return Path(override).expanduser().resolve() if override else repo_root() / "Media" / "footage-index"


def edit_work_root():
    return Path(os.environ.get("ROLL_EDIT_WORK_ROOT", "/Volumes/Extreme/_edit_work")).expanduser()


def binary(name):
    override = os.environ.get("ROLL_" + name.upper())
    if override:
        return override
    bundled = repo_root() / "Media" / "video_edit" / "bin" / name
    if bundled.exists():
        return str(bundled)
    found = shutil.which(name)
    if found:
        return found
    raise RuntimeError("{} was not found".format(name))


def now_iso():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def slug(text):
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value or "shoot"


def shoot_name(clip):
    parent = clip.parent
    folder = parent.name.lower()
    if folder in {"main camera", "screen recordings", "screen-recordings"} or "gopro" in folder:
        return parent.parent.name + " - " + parent.name
    return parent.name


def clip_paths(clip):
    stem = clip.stem
    shoot = shoot_name(clip)
    drive_json = clip.with_name(stem + ".roll.json")
    drive_md = clip.with_name(stem + ".roll.md")
    drive_dir = clip.with_name(stem + ".roll")
    mdir = mirror_root() / slug(shoot)
    mirror_json = mdir / (stem + ".roll.json")
    mirror_md = mdir / (stem + ".roll.md")
    mirror_artifacts = mdir / (stem + ".roll")
    return {
        "drive_json": drive_json,
        "drive_md": drive_md,
        "drive_dir": drive_dir,
        "drive_words": drive_dir / "words.json",
        "drive_contact": drive_dir / "contact.jpg",
        "mirror_json": mirror_json,
        "mirror_md": mirror_md,
        "mirror_dir": mdir,
        "mirror_artifacts": mirror_artifacts,
        "mirror_words": mirror_artifacts / "words.json",
    }


def atomic_write(path, data, binary_mode=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "wb" if binary_mode else "w"
    kwargs = {} if binary_mode else {"encoding": "utf-8"}
    with tempfile.NamedTemporaryFile(mode=mode, dir=str(path.parent), delete=False, **kwargs) as handle:
        handle.write(data)
        temp_name = handle.name
    os.replace(temp_name, str(path))


def run(command, check=True, capture=True, nice=False, env=None):
    cmd = list(command)
    if nice and shutil.which("nice"):
        cmd = ["nice", "-n", "10"] + cmd
    result = subprocess.run(
        cmd,
        check=False,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        text=True,
        env=env,
    )
    if check and result.returncode:
        detail = (result.stderr or result.stdout or "command failed").strip()
        raise RuntimeError("{}: {}".format(Path(cmd[0]).name, detail[-2000:]))
    return result


def active_builds():
    result = run(["ps", "-Ao", "pid=,stat=,command="], check=False)
    current = os.getpid()
    matches = []
    pattern = re.compile(
        r"(?:^|\s)(?:\([^)]*ffmpeg[^)]*\)|\S*/?ffmpeg)(?:\s|$)"
        r"|(?:^|\s)(?:\S*/?python\S*)\s+\S*(?:whisper|render\.py|gate\.py|qc_style)",
        re.I,
    )
    for line in result.stdout.splitlines():
        parts = line.strip().split(None, 2)
        if len(parts) != 3:
            continue
        try:
            pid = int(parts[0])
        except ValueError:
            continue
        state, command = parts[1], parts[2]
        if "Z" not in state and pid != current and pattern.search(command) and "roll_sidecar.py" not in command:
            matches.append((pid, command))
    return matches


def wait_for_build_slot(label):
    announced = False
    while True:
        builds = active_builds()
        if len(builds) < 2:
            return
        if not announced:
            print("WAIT {}: two other builds are active; this indexer is not taking a third slot".format(label), flush=True)
            announced = True
        time.sleep(20)


def content_identity(path):
    size = path.stat().st_size
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        digest.update(handle.read(SAMPLE_BYTES))
        if size > SAMPLE_BYTES:
            handle.seek(max(0, size - SAMPLE_BYTES))
            digest.update(handle.read(SAMPLE_BYTES))
    sample = digest.hexdigest()
    return {
        "content_key": "{}:{}".format(size, sample),
        "size_bytes": size,
        "sample_sha256": sample,
    }


def fraction(value):
    if not value or value == "0/0":
        return None
    try:
        if "/" in value:
            a, b = value.split("/", 1)
            return round(float(a) / float(b), 6)
        return round(float(value), 6)
    except (ValueError, ZeroDivisionError):
        return None


def probe(path):
    result = run([
        binary("ffprobe"), "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", str(path),
    ])
    data = json.loads(result.stdout)
    streams = data.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), {})
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    rotation = 0
    for side in video.get("side_data_list", []):
        if "rotation" in side:
            rotation = int(round(float(side["rotation"])))
            break
    if not rotation:
        try:
            rotation = int(video.get("tags", {}).get("rotate", 0))
        except (TypeError, ValueError):
            rotation = 0
    width = int(video.get("width") or 0)
    height = int(video.get("height") or 0)
    decoded_width, decoded_height = (height, width) if abs(rotation) % 180 == 90 else (width, height)
    tags = {
        "color_space": video.get("color_space"),
        "color_transfer": video.get("color_transfer"),
        "color_primaries": video.get("color_primaries"),
        "color_range": video.get("color_range"),
    }
    tags_present = all(tags.values())
    duration = float(data.get("format", {}).get("duration") or video.get("duration") or 0.0)
    return {
        "duration": round(duration, 3),
        "picture": {
            "stored_resolution": "{}x{}".format(width, height),
            "decoded_resolution": "{}x{}".format(decoded_width, decoded_height),
            "fps": fraction(video.get("avg_frame_rate") or video.get("r_frame_rate")),
            "fps_fraction": video.get("avg_frame_rate") or video.get("r_frame_rate"),
            "rotation_degrees": rotation,
            "portrait": decoded_height > decoded_width,
            "codec": video.get("codec_name"),
            "pixel_format": video.get("pix_fmt"),
            "color_tags": tags,
            "color_tags_status": "present" if tags_present else "ABSENT",
            "untagged_decode_assumption": None if tags_present else "BT.709",
        },
        "audio_streams": [
            {
                "audio_index": idx,
                "stream_index": s.get("index"),
                "codec": s.get("codec_name"),
                "channels": s.get("channels"),
                "channel_layout": s.get("channel_layout"),
                "sample_rate": int(s["sample_rate"]) if s.get("sample_rate") else None,
            }
            for idx, s in enumerate(audio)
        ],
    }


def grade_family(clip):
    match = re.fullmatch(r"C(\d+)", clip.stem, re.I)
    number = int(match.group(1)) if match else None
    path_text = str(clip).lower()
    if "8:28 shoot" in path_text or "8-28 shoot" in path_text:
        if number is not None and 1650 <= number <= 1653:
            return {
                "roll_family": "8/28 landscape talking, four mono tracks",
                "grade_fit": "8/28 indoor S-Log3 family; closest approved reference is the website conversion LUT at 1.45x plus saturation 0.88",
                "source": "Docs/SHOOT_828_FOOTAGE_REPORT.md and .claude/skills/_shared/reference/picture.json",
            }
        if number is not None and 1654 <= number <= 1672:
            return {
                "roll_family": "8/28 native portrait outdoor talking, dual-mono lav",
                "grade_fit": "8/28 outdoor daylight S-Log3 family; use the approved per-roll daylight fit, never the indoor LUT blindly",
                "source": "Docs/SHOOT_828_FOOTAGE_REPORT.md and .claude/skills/_shared/reference/picture.json",
            }
        if number is not None and 1673 <= number <= 1685:
            return {
                "roll_family": "8/28 landscape exercise B-roll",
                "grade_fit": "8/28 outdoor S-Log3 exercise family; light changes by roll, so a per-clip trim is required",
                "source": "Docs/SHOOT_828_FOOTAGE_REPORT.md and .claude/skills/_shared/reference/picture.json",
            }
    return {"roll_family": "unknown", "grade_fit": "unknown", "source": ".claude/skills/_shared/reference/picture.json"}


def clip_number(clip):
    match = re.fullmatch(r"C(\d+)", clip.stem, re.I)
    return int(match.group(1)) if match else None


def words_from_payload(payload):
    words = []
    if isinstance(payload, dict) and isinstance(payload.get("segments"), list):
        for segment in payload["segments"]:
            for word in segment.get("words", []) or []:
                token = word.get("word", word.get("text", ""))
                if token and word.get("start") is not None and word.get("end") is not None:
                    words.append({
                        "word": str(token),
                        "start": round(float(word["start"]), 3),
                        "end": round(float(word["end"]), 3),
                        **({"probability": word["probability"]} if word.get("probability") is not None else {}),
                    })
    elif isinstance(payload, dict) and isinstance(payload.get("words"), list):
        for word in payload["words"]:
            if word.get("type") not in (None, "word"):
                continue
            token = word.get("word", word.get("text", ""))
            if token and word.get("start") is not None and word.get("end") is not None:
                words.append({"word": str(token), "start": round(float(word["start"]), 3), "end": round(float(word["end"]), 3)})
    return sorted(words, key=lambda item: (item["start"], item["end"]))


def transcript_inventory(root):
    inventory = {}
    if not root.exists():
        return inventory
    for current, dirs, files in os.walk(str(root)):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            lower = name.lower()
            if name.startswith("._") or not lower.endswith(".json"):
                continue
            if not any(mark in lower for mark in ("whisper", "transcript", "words")):
                continue
            key = re.split(r"[._ -]", lower, 1)[0]
            if key:
                inventory.setdefault(key, []).append(Path(current) / name)
    return inventory


def lav_inventory(root):
    inventory = {}
    if not root.exists():
        return inventory
    for current, dirs, files in os.walk(str(root)):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            lower = name.lower()
            if name.startswith("._") or not lower.endswith(".audio_source.json"):
                continue
            key = lower[: -len(".audio_source.json")]
            key = re.sub(r"\.(mp4|mov|mxf|m4v|avi|mts|m2ts)$", "", key)
            inventory.setdefault(key, []).append(Path(current) / name)
    return inventory


def duration_match(words, duration):
    if not words:
        return False
    end = words[-1]["end"]
    if end > duration + 2.0:
        return False
    return end >= min(duration * 0.55, max(1.0, duration - 20.0))


def harvest_transcript(clip, duration, inventory):
    candidates = inventory.get(clip.stem.lower(), [])
    ranked = []
    for candidate in candidates:
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
            words = words_from_payload(payload)
        except (OSError, ValueError, TypeError):
            continue
        if duration_match(words, duration):
            score = abs(duration - words[-1]["end"])
            ranked.append((score, len(words), candidate, words))
    if not ranked:
        return None, None
    ranked.sort(key=lambda row: (row[0], -row[1], len(str(row[2]))))
    _, _, candidate, words = ranked[0]
    return words, "harvested:" + str(candidate)


def lav_candidates(clip, inventory):
    direct = [clip.with_name(clip.name + ".audio_source.json"), clip.with_name(clip.stem + ".audio_source.json")]
    for item in direct:
        if item.exists():
            yield item
    for item in inventory.get(clip.stem.lower(), []):
        yield item


def valid_lav_payload(payload, duration):
    if not isinstance(payload, dict) or not payload.get("map") or not payload.get("filter"):
        return False
    recorded = payload.get("duration")
    return recorded is None or abs(float(recorded) - duration) <= max(1.0, duration * 0.01)


def get_lav(clip, duration, inventory):
    for candidate in lav_candidates(clip, inventory):
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if valid_lav_payload(payload, duration):
            payload = copy.deepcopy(payload)
            payload["source"] = "harvested:" + str(candidate)
            return payload
    wait_for_build_slot("lav pick for " + clip.name)
    picker = repo_root() / ".claude" / "skills" / "_shared" / "audio" / "pick_lav.py"
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as handle:
        output = Path(handle.name)
    try:
        result = run([sys.executable, str(picker), str(clip), "--out", str(output)], check=False, nice=True)
        if result.returncode == 0 and output.exists():
            payload = json.loads(output.read_text(encoding="utf-8"))
            payload["source"] = "measured:pick_lav.py"
            return payload
        return {"verdict": "unresolved", "source": "measured:pick_lav.py", "error": (result.stderr or result.stdout)[-1000:]}
    finally:
        output.unlink(missing_ok=True)


def transcribe(clip, lav, model="small"):
    if not lav.get("map") or not lav.get("filter"):
        return [], "not-run:lav-unresolved"
    wait_for_build_slot("Whisper for " + clip.name)
    runner = repo_root() / ".claude" / "skills" / "ad-edit" / "reference" / "whisper_chunked.py"
    with tempfile.TemporaryDirectory(prefix="roll-whisper-") as temp:
        temp_path = Path(temp)
        wav = temp_path / "lav.wav"
        output = temp_path / "whisper.json"
        run([
            binary("ffmpeg"), "-nostdin", "-v", "error", "-y", "-i", str(clip),
            "-map", str(lav["map"]), "-af", str(lav["filter"]),
            "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav),
        ], nice=True)
        child_env = os.environ.copy()
        child_env["PATH"] = str(Path(binary("ffmpeg")).parent) + os.pathsep + child_env.get("PATH", "")
        run([sys.executable, str(runner), str(wav), str(output), model], nice=True, env=child_env)
        words = words_from_payload(json.loads(output.read_text(encoding="utf-8")))
    return words, "whisper:" + model


def build_contact(clip, duration, output):
    interval = 2 if duration < 60 else 5
    count = max(1, int(math.ceil(duration / interval)))
    cols = 6
    rows = int(math.ceil(count / cols))
    font = "/System/Library/Fonts/Supplemental/Arial.ttf"
    font_part = "fontfile={}:".format(font) if Path(font).exists() else ""
    sampler = "select=eq(n\\,0)," if duration < interval else "fps=1/{},".format(interval)
    vf = (
        "{sampler}scale=320:180:force_original_aspect_ratio=decrease,"
        "pad=320:180:(ow-iw)/2:(oh-ih)/2:black,"
        "drawbox=x=0:y=0:w=112:h=26:color=black@0.72:t=fill,"
        "drawtext={font}text='%{{pts\\:hms}}':x=5:y=4:fontsize=16:fontcolor=white,"
        "tile={cols}x{rows}:padding=4:margin=4:color=black"
    ).format(sampler=sampler, font=font_part, cols=cols, rows=rows)
    wait_for_build_slot("contact sheet for " + clip.name)
    output.parent.mkdir(parents=True, exist_ok=True)
    run([
        binary("ffmpeg"), "-nostdin", "-v", "error", "-y", "-i", str(clip),
        "-vf", vf, "-frames:v", "1", "-q:v", "3", str(output),
    ], nice=True)
    return interval, count


def secret_value(name):
    if os.environ.get(name):
        return os.environ[name]
    path = Path.home() / ".absbyai-secrets.env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip("\"").strip("'")
    return None


def parse_json_text(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def describe_contact(contact, interval, model=None):
    key = secret_value("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not available")
    model = model or os.environ.get("ROLL_GEMINI_MODEL", DEFAULT_MODEL)
    prompt = (
        "This is a contact sheet from one continuous source clip. Every cell has a burned-in timestamp. "
        "Return JSON only with keys summary and shots. summary is one plain sentence. shots is a list of "
        "continuous visual ranges. Each shot needs start, end, setting, framing, angle, shirt, action, props, "
        "other_people, and description. framing must be near, medium, far, or unknown. angle must be front, "
        "45, profile, back, or unknown. Use timestamps visible in the sheet. Be literal and searchable. "
        "Name exercises and actions precisely. A stomach vacuum should say vacuum. Do not infer speech. "
        "The sampling interval is {} seconds.".format(interval)
    )
    payload = {
        "contents": [{"parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(contact.read_bytes()).decode("ascii")}},
        ]}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 2500, "responseMimeType": "application/json"},
    }
    url = "https://generativelanguage.googleapis.com/v1beta/models/{}:generateContent?key={}".format(model, key)
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            body = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError("Gemini HTTP {}: {}".format(exc.code, detail[-1000:]))
    text = "".join(
        part.get("text", "")
        for candidate in body.get("candidates", [])
        for part in candidate.get("content", {}).get("parts", [])
    )
    parsed = parse_json_text(text)
    usage = body.get("usageMetadata", {})
    input_tokens = int(usage.get("promptTokenCount") or 0)
    output_tokens = int(usage.get("candidatesTokenCount") or 0)
    cost = input_tokens * DESCRIPTION_INPUT_USD_PER_M / 1000000.0 + output_tokens * DESCRIPTION_OUTPUT_USD_PER_M / 1000000.0
    return parsed, {
        "provider": "Google Gemini",
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_actual_usd": round(cost, 6),
        "pricing_assumption": "${:.2f}/1M input and ${:.2f}/1M output".format(DESCRIPTION_INPUT_USD_PER_M, DESCRIPTION_OUTPUT_USD_PER_M),
    }


def transcript_text(words):
    return "".join(word["word"] for word in words).strip()


def normalized_tokens(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def contains_query(haystack, query):
    if not query or len(haystack) < len(query):
        return False
    if len(query) == 1:
        return query[0] in haystack
    return any(haystack[index:index + len(query)] == query for index in range(len(haystack) - len(query) + 1))


def take_list(words):
    if not words:
        return []
    groups = []
    current = [words[0]]
    for word in words[1:]:
        if word["start"] - current[-1]["end"] >= 1.0:
            groups.append(current)
            current = [word]
        else:
            current.append(word)
    groups.append(current)
    takes = []
    for index, group in enumerate(groups, 1):
        text = "".join(word["word"] for word in group).strip()
        tokens = normalized_tokens(text)
        retake_of = None
        for previous in takes:
            earlier = normalized_tokens(previous["text"])
            if len(tokens) >= 4 and len(earlier) >= 4:
                ratio = difflib.SequenceMatcher(None, tokens, earlier).ratio()
                if ratio >= 0.72:
                    retake_of = previous["take"]
                    break
        takes.append({
            "take": index,
            "start": group[0]["start"],
            "end": group[-1]["end"],
            "first_12_words": " ".join(tokens[:12]),
            "text": text,
            "retake_of": retake_of,
            "script_line": None,
        })
    return takes


def merge_locked(old, new):
    if isinstance(old, dict) and old.get("locked") is True:
        return copy.deepcopy(old)
    if isinstance(old, dict) and isinstance(new, dict):
        result = copy.deepcopy(new)
        for key, value in old.items():
            if key in new:
                result[key] = merge_locked(value, new[key])
        return result
    return new


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def all_mirror_sidecars():
    root = mirror_root()
    return sorted(root.glob("*/*.roll.json")) if root.exists() else []


def mirror_content_index():
    result = {}
    for path in all_mirror_sidecars():
        try:
            data = load_json(path)
        except (OSError, ValueError):
            continue
        key = data.get("identity", {}).get("content_key")
        if key and key not in result:
            result[key] = (path, data)
    return result


def find_by_content_key(content_key):
    for path in all_mirror_sidecars():
        try:
            data = load_json(path)
        except (OSError, ValueError):
            continue
        if data.get("identity", {}).get("content_key") == content_key:
            return path, data
    return None, None


def markdown(data):
    ident = data["identity"]
    picture = data["picture"]
    audio = data["audio"]
    grade = data["grade"]
    if isinstance(grade, dict) and grade.get("locked") is True and "value" in grade:
        grade = grade["value"]
    if not isinstance(grade, dict):
        grade = {"roll_family": str(grade), "grade_fit": "human-locked value"}
    lines = [
        "# Roll sidecar: " + ident["file_name"],
        "",
        "- Content key: `{}`".format(ident["content_key"]),
        "- Source: `{}`".format(ident["current_path"]),
        "- Shoot: {}".format(ident["shoot"]),
        "- Duration: {:.3f} s".format(ident["duration"]),
        "- Picture: {}, {} fps, rotation {} degrees, codec {}".format(picture["decoded_resolution"], picture.get("fps"), picture["rotation_degrees"], picture.get("codec")),
        "- Colour tags: {}. Untagged decode assumption: {}".format(picture["color_tags_status"], picture.get("untagged_decode_assumption") or "not needed"),
        "- Roll family: {}".format(grade["roll_family"]),
        "- Grade fit: {}".format(grade["grade_fit"]),
        "- Audio streams: {}. Lav verdict: {}. Lav source: {}".format(len(audio.get("streams", [])), audio.get("lav", {}).get("verdict", "unknown"), audio.get("lav", {}).get("source", "unknown")),
        "- Transcript source: {}".format(data.get("transcript_source")),
        "- Words: {}".format(data.get("transcript", {}).get("word_count", 0)),
        "",
        "## Transcript",
        "",
        data.get("transcript", {}).get("text") or "No speech found.",
        "",
        "## Takes",
        "",
    ]
    for take in data.get("takes", []):
        suffix = " (retake of {})".format(take["retake_of"]) if take.get("retake_of") else ""
        lines.append("- {:.2f}-{:.2f}: {}{}".format(take["start"], take["end"], take["first_12_words"], suffix))
    if not data.get("takes"):
        lines.append("- None")
    lines += ["", "## On screen", ""]
    description = data.get("description", {})
    if description.get("summary"):
        lines.append(description["summary"])
        lines.append("")
    shots = locked_value(data.get("shots", [])) or []
    for shot in shots:
        lines.append("- {start}-{end}: {description} [framing={framing}, angle={angle}]".format(
            start=shot.get("start", "?"), end=shot.get("end", "?"), description=shot.get("description", shot.get("action", "")),
            framing=shot.get("framing", "unknown"), angle=shot.get("angle", "unknown")))
    if not shots:
        lines.append("- Not described")
    lines += ["", "## Used in", ""]
    for row in data.get("used_in", []):
        lines.append("- {job}: {in:.3f}-{out:.3f} ({date})".format(**row))
    if not data.get("used_in"):
        lines.append("- Not recorded as used")
    lines.append("")
    return "\n".join(lines)


def save_sidecar(data, paths, words):
    rendered_json = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    rendered_md = markdown(data)
    rendered_words = json.dumps({"words": words}, indent=2, ensure_ascii=False) + "\n"
    atomic_write(paths["drive_json"], rendered_json)
    atomic_write(paths["drive_md"], rendered_md)
    atomic_write(paths["drive_words"], rendered_words)
    atomic_write(paths["mirror_json"], rendered_json)
    atomic_write(paths["mirror_md"], rendered_md)
    atomic_write(paths["mirror_words"], rendered_words)


def resolve_clips(target):
    path = Path(target).expanduser().resolve()
    if path.is_file():
        if path.suffix.lower() not in VIDEO_EXTENSIONS or path.name.startswith("._"):
            raise RuntimeError("not a supported source video: " + str(path))
        return [path]
    if not path.is_dir():
        raise RuntimeError("not found: " + str(path))
    return sorted(
        item for item in path.rglob("*")
        if item.is_file() and item.suffix.lower() in VIDEO_EXTENSIONS and not item.name.startswith("._")
    )


def build_one(clip, args, inventory, lavs, content_index):
    started = time.time()
    paths = clip_paths(clip)
    identity = content_identity(clip)
    existing_path, existing = content_index.get(identity["content_key"], (None, None))
    if existing and not args.force:
        print("SKIP {}: indexed as {}".format(clip, existing_path), flush=True)
        return {"status": "skipped", "duration": existing.get("identity", {}).get("duration", 0), "transcript_source": existing.get("transcript_source"), "description_cost_usd": 0}
    media = probe(clip)
    words, transcript_source = harvest_transcript(clip, media["duration"], inventory)
    lav = get_lav(clip, media["duration"], lavs) if media["audio_streams"] else {"verdict": "no-audio", "source": "ffprobe"}
    if words is None:
        if media["audio_streams"]:
            words, transcript_source = transcribe(clip, lav, args.whisper_model)
        else:
            words, transcript_source = [], "not-applicable:no-audio"
    interval, frame_count = build_contact(clip, media["duration"], paths["drive_contact"])
    description = {"summary": None}
    shots = []
    description_usage = None
    if not args.no_describe:
        described, description_usage = describe_contact(paths["drive_contact"], interval, args.gemini_model)
        described = postprocess_description(clip, described, words)
        description = {"summary": described.get("summary"), "source": "gemini-contact-sheet"}
        shots = described.get("shots", []) if isinstance(described.get("shots"), list) else []
    data = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": now_iso(),
        "identity": {
            **identity,
            "file_name": clip.name,
            "current_path": str(clip),
            "shoot": shoot_name(clip),
            "size_bytes": clip.stat().st_size,
            "duration": media["duration"],
        },
        "picture": media["picture"],
        "audio": {"streams": media["audio_streams"], "lav": lav},
        "grade": grade_family(clip),
        "transcript_source": transcript_source,
        "transcript": {"text": transcript_text(words), "word_count": len(words)},
        "takes": take_list(words),
        "description": description,
        "shots": shots,
        "description_usage": description_usage,
        "contact_sheet": {"interval_seconds": interval, "frame_count": frame_count, "drive_path": str(paths["drive_contact"])},
        "used_in": copy.deepcopy(existing.get("used_in", [])) if existing else [],
    }
    if existing:
        data = merge_locked(existing, data)
    save_sidecar(data, paths, words)
    content_index[identity["content_key"]] = (paths["mirror_json"], data)
    cost = (data.get("description_usage") or {}).get("estimated_actual_usd", 0) or 0
    status = "harvested" if str(transcript_source).startswith("harvested:") else "whispered" if str(transcript_source).startswith("whisper:") else "indexed"
    print("DONE {}: {:.1f}s, {}, ${:.6f}".format(clip.name, time.time() - started, status, cost), flush=True)
    return {"status": status, "duration": media["duration"], "transcript_source": transcript_source, "description_cost_usd": cost}


def command_build(args):
    clips = resolve_clips(args.target)
    if not clips:
        raise RuntimeError("no supported source clips found")
    inventory = transcript_inventory(edit_work_root())
    lavs = lav_inventory(edit_work_root())
    content_index = mirror_content_index()
    totals = {"clips": 0, "minutes": 0.0, "harvested": 0, "whispered": 0, "skipped": 0, "gemini_usd": 0.0, "errors": []}
    started = time.time()
    for clip in clips:
        try:
            row = build_one(clip, args, inventory, lavs, content_index)
            totals["clips"] += 1
            totals["minutes"] += float(row.get("duration") or 0) / 60.0
            if row["status"] in totals:
                totals[row["status"]] += 1
            totals["gemini_usd"] += float(row.get("description_cost_usd") or 0)
        except Exception as exc:
            totals["errors"].append({"clip": str(clip), "error": str(exc)})
            print("ERROR {}: {}".format(clip, exc), file=sys.stderr, flush=True)
    totals["minutes"] = round(totals["minutes"], 3)
    totals["gemini_usd"] = round(totals["gemini_usd"], 6)
    totals["wall_clock_seconds"] = round(time.time() - started, 3)
    print(json.dumps(totals, indent=2))
    return 1 if totals["errors"] else 0


def load_for_clip(clip):
    paths = clip_paths(clip)
    if paths["drive_json"].exists():
        return paths["drive_json"], load_json(paths["drive_json"])
    identity = content_identity(clip)
    return find_by_content_key(identity["content_key"])


def command_show(args):
    clip = Path(args.clip).expanduser().resolve()
    path, data = load_for_clip(clip)
    if not data:
        print("No sidecar. Run: {} build {}".format(Path(__file__).name, repr(str(clip))))
        return 1
    print(markdown(data))
    print("Sidecar: " + str(path))
    return 0


def locked_value(value):
    if isinstance(value, dict) and value.get("locked") is True and "value" in value:
        return value["value"]
    return value


def time_seconds(value):
    if value is None or value == "":
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    try:
        return float(text)
    except ValueError:
        pass
    parts = text.split(":")
    if len(parts) in (2, 3):
        try:
            numbers = [float(part) for part in parts]
            if len(numbers) == 2:
                return numbers[0] * 60 + numbers[1]
            return numbers[0] * 3600 + numbers[1] * 60 + numbers[2]
        except ValueError:
            return 0.0
    return 0.0


def postprocess_description(clip, described, words):
    """Normalize timestamps and block a known false action on 8/28 talking rolls."""
    result = copy.deepcopy(described) if isinstance(described, dict) else {}
    shots = result.get("shots", []) if isinstance(result.get("shots"), list) else []
    for shot in shots:
        shot["start"] = round(time_seconds(shot.get("start")), 3)
        shot["end"] = round(time_seconds(shot.get("end", shot.get("start"))), 3)
    number = clip_number(clip)
    path_text = str(clip).lower()
    talking_828 = (
        ("8:28 shoot" in path_text or "8-28 shoot" in path_text)
        and number is not None and 1650 <= number <= 1672 and len(words) >= 10
    )
    if talking_828:
        changed = False
        for shot in shots:
            visible = " ".join(str(shot.get(key, "")) for key in ("description", "action")).lower()
            if "vacuum" in visible:
                shot["action"] = "speaking to camera"
                shot["description"] = "Dan speaks to camera."
                changed = True
        if "vacuum" in str(result.get("summary", "")).lower() or changed:
            setting = shots[0].get("setting", "the recorded setting") if shots else "the recorded setting"
            result["summary"] = "Dan speaks to camera in {}.".format(setting)
    result["shots"] = shots
    return result


def overlaps_used(start, end, used):
    for row in used:
        if start < float(row.get("out", 0)) and end > float(row.get("in", 0)):
            return True
    return False


def find_rows(data, query):
    query_tokens = normalized_tokens(query)
    if not query_tokens:
        return []
    rows = []
    for take in locked_value(data.get("takes", [])) or []:
        text = take.get("text") or take.get("first_12_words", "")
        hay = normalized_tokens(text)
        if contains_query(hay, query_tokens):
            rows.append((float(take.get("start", 0)), float(take.get("end", 0)), text, None))
    for shot in locked_value(data.get("shots", [])) or []:
        text = " ".join(str(shot.get(key, "")) for key in ("description", "setting", "framing", "angle", "shirt", "action", "props", "other_people"))
        hay = normalized_tokens(text)
        if contains_query(hay, query_tokens):
            rows.append((time_seconds(shot.get("start", 0)), time_seconds(shot.get("end", shot.get("start", 0))), text.strip(), shot))
    if not rows:
        text = data.get("transcript", {}).get("text", "")
        hay = normalized_tokens(text)
        if contains_query(hay, query_tokens):
            rows.append((0.0, float(data.get("identity", {}).get("duration", 0)), text[:240], None))
    return rows


def command_find(args):
    hits = []
    for path in all_mirror_sidecars():
        try:
            data = load_json(path)
        except (OSError, ValueError):
            continue
        shoot = str(data.get("identity", {}).get("shoot", ""))
        if args.shoot and args.shoot.lower() not in shoot.lower():
            continue
        used = data.get("used_in", [])
        for start, end, text, shot in find_rows(data, args.words):
            if args.framing and (not shot or str(shot.get("angle", "")).lower() != args.framing.lower()):
                continue
            if args.unused and overlaps_used(start, end, used):
                continue
            source = data.get("identity", {}).get("current_path", "")
            source_offline = os.environ.get("ROLL_SOURCE_OFFLINE") == "1"
            mounted = source if not source_offline and source and Path(source).exists() else "drive unplugged"
            hits.append((shoot, data.get("identity", {}).get("file_name", path.name), start, end, re.sub(r"\s+", " ", text).strip(), mounted))
    for shoot, clip, start, end, text, mounted in hits:
        print("{} | {} | {:.2f}-{:.2f} | {} | {}".format(shoot, clip, start, end, text[:300], mounted))
    if not hits:
        print("No matches")
        return 1
    return 0


def command_mark_used(args):
    clip = Path(args.clip).expanduser().resolve()
    path, data = load_for_clip(clip)
    if not data:
        raise RuntimeError("no sidecar for " + str(clip))
    row = {"job": args.job, "in": round(args.in_point, 3), "out": round(args.out_point, 3), "date": args.date or dt.date.today().isoformat()}
    if row["out"] <= row["in"]:
        raise RuntimeError("--out must be greater than --in")
    used = data.setdefault("used_in", [])
    if row not in used:
        used.append(row)
    current_clip = Path(data["identity"]["current_path"])
    if not current_clip.exists():
        current_clip = clip
    paths = clip_paths(current_clip)
    if path and path.parent == paths["mirror_json"].parent:
        words_path = path.parent / path.name.replace(".roll.json", ".roll") / "words.json"
    else:
        words_path = paths["mirror_words"]
    words = load_json(words_path).get("words", []) if words_path.exists() else []
    save_sidecar(data, paths, words)
    print("Marked used: {} {:.3f}-{:.3f}".format(args.job, row["in"], row["out"]))
    return 0


def comparable(data):
    result = copy.deepcopy(data)
    return result


def command_verify(args):
    errors = []
    warnings = []
    seen = {}
    sidecars = all_mirror_sidecars()
    for mirror_json in sidecars:
        try:
            data = load_json(mirror_json)
        except Exception as exc:
            errors.append("invalid JSON {}: {}".format(mirror_json, exc))
            continue
        key = data.get("identity", {}).get("content_key")
        if not key:
            errors.append("missing content key: " + str(mirror_json))
        elif key in seen:
            errors.append("duplicate content key: {} and {}".format(seen[key], mirror_json))
        else:
            seen[key] = mirror_json
        mirror_md = mirror_json.with_suffix(".md")
        mirror_words = mirror_json.parent / mirror_json.name.replace(".roll.json", ".roll") / "words.json"
        if not mirror_md.exists():
            errors.append("missing mirror Markdown: " + str(mirror_md))
        if not mirror_words.exists():
            errors.append("missing mirror words: " + str(mirror_words))
        source_text = data.get("identity", {}).get("current_path", "")
        source = Path(source_text) if source_text else None
        if not source or not source.exists():
            warnings.append("source unavailable: {}".format(source_text or mirror_json))
            continue
        paths = clip_paths(source)
        if not paths["drive_json"].exists():
            errors.append("missing drive JSON: " + str(paths["drive_json"]))
        else:
            try:
                drive_data = load_json(paths["drive_json"])
                if comparable(drive_data) != comparable(data):
                    errors.append("mirror differs from drive: " + str(mirror_json))
            except Exception as exc:
                errors.append("invalid drive JSON {}: {}".format(paths["drive_json"], exc))
        for required in (paths["drive_md"], paths["drive_words"], paths["drive_contact"]):
            if not required.exists():
                errors.append("missing drive artifact: " + str(required))
    for warning in warnings:
        print("WARN " + warning)
    for error in errors:
        print("ERROR " + error)
    print("verify: {} sidecars, {} warning(s), {} error(s)".format(len(sidecars), len(warnings), len(errors)))
    return 1 if errors else 0


def parser():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build", help="build sidecars for one clip or a folder")
    build.add_argument("target")
    build.add_argument("--no-describe", action="store_true", help="skip the paid Gemini contact-sheet description")
    build.add_argument("--force", action="store_true", help="rebuild while preserving locked fields")
    build.add_argument("--whisper-model", default="small")
    build.add_argument("--gemini-model", default=None)
    build.set_defaults(func=command_build)
    find = sub.add_parser("find", help="search the local text mirror")
    find.add_argument("words")
    find.add_argument("--shoot")
    find.add_argument("--framing", choices=["front", "45", "profile"])
    find.add_argument("--unused", action="store_true")
    find.set_defaults(func=command_find)
    show = sub.add_parser("show", help="show the sidecar for a clip")
    show.add_argument("clip")
    show.set_defaults(func=command_show)
    used = sub.add_parser("mark-used", help="append a used range after an EDL is final")
    used.add_argument("clip")
    used.add_argument("--job", required=True)
    used.add_argument("--in", dest="in_point", required=True, type=float)
    used.add_argument("--out", dest="out_point", required=True, type=float)
    used.add_argument("--date")
    used.set_defaults(func=command_mark_used)
    verify = sub.add_parser("verify", help="check mirror and drive agreement")
    verify.set_defaults(func=command_verify)
    return ap


def main():
    args = parser().parse_args()
    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("Interrupted", file=sys.stderr)
        return 130
    except Exception as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
