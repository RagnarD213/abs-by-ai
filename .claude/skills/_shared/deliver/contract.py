#!/usr/bin/env python3
"""Versioned evidence contract for checks that follow composited or transformed media.

Version 2 adds facts the old flat plan could not represent: rendered PNG caption states, graphic
regions, talking-head windows, and moving label tracks. New geometry is accepted only when it is
bound to the exact delivered file. That prevents an old plan from certifying a new render.
"""
import hashlib
import os

CONTRACT_VERSION = 2
PATH_KEYS = {"image", "wrong_image", "mov", "reference", "mask", "clearance_report"}
NEW_KEYS = ("caption_states", "graphic_regions", "talking_head_windows", "label_tracks")


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def resolve_paths(value, base):
    """Resolve nested contract asset paths in-place."""
    if isinstance(value, list):
        for item in value:
            resolve_paths(item, base)
    elif isinstance(value, dict):
        for key, item in list(value.items()):
            if key in PATH_KEYS and isinstance(item, str) and item and not os.path.isabs(item):
                value[key] = os.path.normpath(os.path.join(base, item))
            else:
                resolve_paths(item, base)


def validate(plan, video_sha256):
    """Return None for legacy/no-new-geometry plans, else an actionable contract error."""
    if not any(k in plan for k in NEW_KEYS):
        return None
    c = plan.get("evidence_contract") or {}
    if c.get("version") != CONTRACT_VERSION:
        return (f"new geometry requires evidence_contract.version {CONTRACT_VERSION}; "
                f"got {c.get('version')!r}")
    if c.get("video_sha256") != video_sha256:
        return ("geometry is stale: evidence_contract.video_sha256 does not match the delivered "
                "file")
    missing, changed = [], []
    for group in NEW_KEYS:
        for item in plan.get(group) or []:
            for key in PATH_KEYS:
                path = item.get(key)
                if not path:
                    continue
                if not os.path.exists(path):
                    missing.append(path)
                expected = item.get(f"{key}_sha256")
                if expected and os.path.exists(path) and file_sha256(path) != expected:
                    changed.append(path)
    if missing:
        return f"contract asset(s) missing: {missing[:3]}"
    if changed:
        return f"contract asset hash changed: {changed[:3]}"
    return None


def contract_error(plan, key):
    """Explain why a new-schema row cannot trust its geometry."""
    err = plan.get("_contract_error")
    return None if not err else f"{key} cannot use the declared geometry: {err}"


def rect_at(items, t, frame_w, frame_h):
    """Return (x,y,w,h,item) for the last declared window active at t."""
    matches = [x for x in (items or []) if x.get("beat", [1, 0])[0] <= t < x["beat"][1]]
    if not matches:
        return 0, 0, frame_w, frame_h, {"motion": "tracking", "name": "full-frame"}
    item = matches[-1]
    rect = item.get("rect")
    if not rect or len(rect) != 4:
        return None
    x, y, w, h = (int(round(float(v))) for v in rect)
    if x < 0 or y < 0 or w < 2 or h < 2 or x + w > frame_w or y + h > frame_h:
        return None
    return x, y, w, h, item


def transform_rect(item, source_size=None):
    """Turn rect or pos+source-size into a concrete output rectangle."""
    if item.get("rect") and len(item["rect"]) == 4:
        return tuple(int(round(float(v))) for v in item["rect"])
    if item.get("pos") and source_size:
        x, y = item["pos"]
        scale = float(item.get("scale", 1.0))
        return (int(round(x)), int(round(y)), int(round(source_size[0] * scale)),
                int(round(source_size[1] * scale)))
    return None


def timed_word_pairs(caption_states, speech_words):
    """Sequence-align rendered highlight states to delivered-audio words.

    The offset is the compositor state's visible start minus the spoken word's start. A state's
    optional `speech` field is useful provenance, but must never be the measured caption time: it
    normally came from the same alignment file and comparing it back to itself would be circular.
    """
    import difflib
    import re
    norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s).lower())  # noqa: E731
    caps = [(norm(s.get("word")), s) for s in caption_states if norm(s.get("word"))]
    said = [(norm(s.get("w") or s.get("word")), s) for s in speech_words
            if norm(s.get("w") or s.get("word"))]
    sm = difflib.SequenceMatcher(None, [x[0] for x in caps], [x[0] for x in said], autojunk=False)
    out = []
    for a0, b0, n in sm.get_matching_blocks():
        for j in range(n):
            c, s = caps[a0 + j][1], said[b0 + j][1]
            ct = float(c["beat"][0])
            st = float(s.get("t", s.get("start")))
            out.append((ct - st, c, s))
    return out, len(caps), len(said)


def pixel_correlations(video, jobs, cache=None):
    """Verify many transformed RGBA states in one sequential decode.

    `jobs` is [(id, item, time, path_key)]. One 4-minute decode is dramatically faster and less
    disruptive than opening ffmpeg hundreds of times. Results may be shared by multiple rows.
    """
    import cv2
    import numpy as np
    from PIL import Image
    cache = cache if cache is not None else {}
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    prepared, by_frame = {}, {}
    for ident, item, t, path_key in jobs:
        ck = (path_key, item.get(path_key), tuple(item.get("rect") or ()),
              tuple(item.get("pos") or ()), float(item.get("scale", 1.0)),
              int(item.get("search_px", 0)), round(float(t), 4))
        if ck in cache:
            continue
        path = item.get(path_key)
        if not path or not os.path.exists(path):
            cache[ck] = None
            continue
        with Image.open(path) as src_im:
            source_size = src_im.size
            # Wrong-label templates must be compared in the EXPECTED label's output rectangle,
            # not at their own native size (the real and AI chips have different text lengths).
            rect_size = source_size
            if path_key != "image" and item.get("image") and os.path.exists(item["image"]):
                with Image.open(item["image"]) as expected_im:
                    rect_size = expected_im.size
            rect = transform_rect(item, rect_size)
            if rect is None:
                cache[ck] = None
                continue
            x, y, w, h = rect
            im = src_im.convert("RGBA").resize((w, h), Image.Resampling.LANCZOS)
        src = np.asarray(im, dtype=np.float32)
        mask = src[..., 3] >= 160
        if mask.sum() < 24:
            cache[ck] = None
            continue
        prepared[ck] = (ident, x, y, w, h, src[..., :3], mask, int(item.get("search_px", 0)))
        by_frame.setdefault(max(0, int(round(float(t) * fps))), []).append(ck)
    if not by_frame:
        cap.release()
        return cache
    want = set(by_frame)
    last, n = max(want), 0
    while n <= last:
        ok, frame = cap.read()
        if not ok:
            break
        if n in want:
            H, W = frame.shape[:2]
            rgb = frame[..., ::-1]
            for ck in by_frame[n]:
                _ident, x, y, w, h, src, mask, search = prepared[ck]
                if x - search < 0 or y - search < 0 or x + w + search > W or y + h + search > H:
                    cache[ck] = None
                    continue
                a = src[mask].ravel()
                best = -1.0
                for dy in range(-search, search + 1):
                    for dx in range(-search, search + 1):
                        got = rgb[y + dy:y + dy + h, x + dx:x + dx + w].astype(np.float32)
                        b = got[mask].ravel()
                        score = (0.0 if a.std() < 1 or b.std() < 1 else
                                 float(np.corrcoef(a, b)[0, 1]))
                        best = max(best, score)
                cache[ck] = best
        n += 1
    cap.release()
    for ck in prepared:
        cache.setdefault(ck, None)
    return cache


def correlation_key(item, t, path_key="image"):
    return (path_key, item.get(path_key), tuple(item.get("rect") or ()),
            tuple(item.get("pos") or ()), float(item.get("scale", 1.0)),
            int(item.get("search_px", 0)), round(float(t), 4))
