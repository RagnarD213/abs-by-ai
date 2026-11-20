#!/usr/bin/env python3
"""Require exact-file sync, blind audiovisual review and transcript-verified client rows."""
import argparse
import concurrent.futures
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

from delivery_gemini import budget as gemini_budget, cost as gemini_cost, native_review
from delivery_sync import (
    SYNC_TOLERANCE, caption_alignment, check_source_ranges, joint_vigor_plan,
    probe, tokens, transcript_words,
)

VERSION = 1
TOOLS = Path(__file__).resolve().parent
SKILLS = TOOLS.parents[1]
GEMINI = SKILLS / "_shared/gemini-cli/gemini.sh"
CHECKS = ("captions", "source_sync", "gemini", "blind_review", "rows")
INPUT_ERRORS = (OSError, ValueError, KeyError, TypeError, AttributeError, IndexError, ZeroDivisionError,
                subprocess.SubprocessError, SystemExit)


def sha256(path):
    with path.open("rb") as stream:
        digest = hashlib.sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def strict_json(data):
    def invalid_constant(constant):
        raise ValueError(f"invalid JSON constant {constant}")

    return json.loads(data, parse_constant=invalid_constant)


def load_json(path):
    return strict_json(path.read_text(encoding="utf-8"))


def write_json(path, value):
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, encoding="utf-8", delete=False) as temp:
        staged = Path(temp.name)
        try:
            json.dump(value, temp, indent=2, ensure_ascii=False, allow_nan=False)
            temp.write("\n")
            temp.close()
            staged.replace(path)
        finally:
            staged.unlink(missing_ok=True)


def receipt_path(video):
    return video.with_name(video.name + ".delivery-gate.json")


def evidence_dir(job, digest):
    return job / "delivery" / digest


def fingerprint(path):
    path = Path(path).resolve(strict=True)
    return {"path": str(path), "sha256": sha256(path)}


def require_receipt(video, rows, job=None, captions=None):
    """Fail before a consumer publishes anything. Return the checked rows and hashes."""
    video, rows = Path(video), Path(rows)
    try:
        receipt = load_json(receipt_path(video))
        if (receipt["version"] != VERSION or receipt["result"] != "PASS"
                or any(receipt["checks"][key]["result"] != "PASS" for key in CHECKS)
                or not {"manifest", "source_map", "captions", "rows", "blind_review", "transcript", "gemini"}
                <= receipt["inputs"].keys()):
            raise ValueError("receipt does not pass every required check")
        if not isinstance(receipt["checks"]["rows"]["verified"], dict):
            raise ValueError("receipt has invalid verified rows")
        if receipt["sha256"] != sha256(video):
            raise ValueError("video bytes differ from the passing receipt")
        if job is not None and Path(job).resolve() != Path(receipt["job"]):
            raise ValueError("receipt came from a different client job")
        rows_bytes = rows.read_bytes()
        if receipt["inputs"]["rows"]["sha256"] != hashlib.sha256(rows_bytes).hexdigest():
            raise ValueError("review page rows changed after the gate")
        for key, artifact in receipt["inputs"].items():
            if key != "rows" and sha256(Path(artifact["path"])) != artifact["sha256"]:
                raise ValueError(f"gate input {key} changed after the check")
        if captions is not None and sha256(Path(captions)) != receipt["inputs"]["captions"]["sha256"]:
            raise ValueError("captions being published differ from the checked SRT")
        return receipt, strict_json(rows_bytes)
    except INPUT_ERRORS as error:
        raise ValueError(f"Delivery blocked for {video.name}: {error}. Run delivery_gate.py on this video and rows.") from None


def checked_call(action):
    try:
        return action()
    except INPUT_ERRORS as error:
        details = getattr(error, "stderr", "") or str(error)
        return {"result": "FAIL", "error": str(details).strip()[-1800:]}


def matching_quote(words, quote):
    phrase = tokens(quote)
    if len(phrase) < 2:
        return []
    spoken = [word[0] for word in words]
    return [words[index][1] for index in range(len(spoken) - len(phrase) + 1)
            if spoken[index:index + len(phrase)] == phrase]


def blind_review(path, media_sha, editor, duration):
    report = load_json(path)
    if report["sha256"] != media_sha:
        raise ValueError("blind review is for a different video")
    if not all(isinstance(report.get(key), str) and report[key].strip()
               for key in ("reviewer", "reviewer_session", "reviewed_at", "method")):
        raise ValueError("blind review lacks reviewer identity, session, time or method")
    when = datetime.datetime.fromisoformat(report["reviewed_at"].replace("Z", "+00:00"))
    if when.tzinfo is None:
        raise ValueError("blind review needs a timezone in reviewed_at")
    if report["reviewer"].strip().casefold() == editor.strip().casefold():
        raise ValueError("editor cannot sign the blind review")
    if any(report.get(key) is not True for key in ("blind", "moving_video", "audio", "whole_film")):
        raise ValueError("independent reviewer must attest to reviewing the whole moving film with sound, blind")
    if not abs(duration - float(report["reviewed_duration_s"])) <= SYNC_TOLERANCE:
        raise ValueError("blind review did not cover the full file duration")
    if report["verdict"] != "PASS" or report["findings"] != []:
        raise ValueError("blind review must PASS with zero unresolved findings")
    verifications = report["row_verifications"]
    if not isinstance(verifications, dict) or any(
        entry["result"] not in ("PASS", "NOT YET") for entry in verifications.values()
    ):
        raise ValueError("blind report contains a failed, unsure or invalid row verdict")
    return {"result": "PASS", "reviewer": report["reviewer"], "reviewer_session": report["reviewer_session"],
            "method": report["method"], "findings": [], "verifications": verifications}


def row_status(row):
    value = str(row.get("verdict", row.get("status", ""))).strip().casefold()
    if value in ("pass", "done"):
        return "done"
    if value in ("not yet", "open", "kept", "n/a", "fail", "later"):
        return "not yet"
    raise ValueError(f"{row.get('id', '?')}: unknown row status {value!r}")


def verify_rows(data, review, words, duration):
    rows = data["asked"]
    if not isinstance(rows, list):
        raise ValueError("rows JSON needs an asked list")
    seen = set()
    problems = []
    verified = {}
    for row in rows:
        identifier = row["id"]
        if not isinstance(identifier, str) or not identifier.strip() or identifier in seen:
            raise ValueError(f"missing or repeated row id: {identifier!r}")
        seen.add(identifier)
        if row_status(row) != "done":
            continue
        transcript_quotes = {}
        try:
            client_words = row["words"]
            literal_quotes = re.findall(r'"([^"]+)"|“([^”]+)”', client_words)
            transcript_quotes = {
                first or second: matching_quote(words, first or second) for first, second in literal_quotes
            }
            transcript_quotes = {quote: hits for quote, hits in transcript_quotes.items() if hits}
            verification = review.get("verifications", {}).get(identifier, {})
            if verification.get("result") != "PASS":
                raise ValueError("no independent verification for this exact file")
            fix = row["fix"]
            if (verification["client_words"] != client_words or verification["fix"] != fix
                    or not all(isinstance(value, str) and value.strip()
                               for value in (client_words, fix, verification["observed"]))):
                raise ValueError("reviewer did not verify the exact note and fix shown on the page")
            quote = row.get("spoken_quote") or verification["spoken_quote"]
            if tokens(verification["spoken_quote"]) != tokens(quote):
                raise ValueError("reviewer verified a different spoken quote")
            if transcript_quotes and all(tokens(candidate) != tokens(quote) for candidate in transcript_quotes):
                raise ValueError("reviewer did not use the client's quoted dialogue found in the final transcript")
            published_time, reviewed_time = float(row["t"]), float(verification["t"])
            if not all(0 <= value < duration for value in (published_time, reviewed_time)):
                raise ValueError("missing or invalid exact-file timestamp")
            hits = [hit for hit in matching_quote(words, quote)
                    if max(abs(hit - published_time), abs(hit - reviewed_time),
                           abs(published_time - reviewed_time)) <= SYNC_TOLERANCE + 1e-9]
            if len(hits) != 1:
                raise ValueError("quoted line did not uniquely match the final transcript at this timestamp")
            verified[identifier] = {"t": hits[0], "client_words": client_words, "spoken_quote": quote}
        except INPUT_ERRORS as error:
            problems.append({"id": identifier, "error": str(error), "claimed_time": row.get("t"),
                             "client_quote_matches_in_final_transcript": transcript_quotes})
    return {"result": "FAIL" if problems else "PASS", "rows": len(rows),
            "verified": verified, "problems": problems}


def subscription_review(file, output, prompt):
    command = [str(GEMINI), "-m", "gemini-4-carbon-medium", "-o", str(output), "-f", str(file), prompt]
    with subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
                          start_new_session=True) as process:
        try:
            _, stderr = process.communicate(timeout=180)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            raise ValueError("Gemini subscription review timed out") from None
        if process.returncode:
            raise ValueError(f"Gemini CLI exit {process.returncode}: {stderr.strip()[-500:]}")
    return output.read_text()


def review_part(file, start, end, fps, artifacts, use_api=False):
    part_duration = end - start
    output = artifacts / f"{file.stem}.txt"
    prompt = (
        "Review the attached MP4 directly as moving video with its audio. Review from the opening to the last "
        "frame. Report EVERY visible-speaking moment where lips do not match speech, and every shot that "
        "contradicts the words. Normal narrated B-roll, labeled dramatizations, silent expressions, and "
        "cutaways while a narrator continues are valid. Only judge a person's lips when that person visibly "
        "appears to be the audible speaker. For each issue include short spoken words and concrete visible "
        "evidence, rather than a general impression or a visual style. Use seconds relative to the attachment. "
        "If you cannot hear the actual audio or inspect the moving picture, or only sampled stills are available, "
        "mark UNAVAILABLE. No tools, external files, or inference from on-screen captions. "
        f"The expected span is approximately {part_duration:.2f} seconds; report the actual inspected span. "
        'Return only JSON with these keys: {"verdict":"PASS|FAIL|UNAVAILABLE","moving_video":true,'
        '"audio":true,"inspected_seconds":0,"last_picture":"specific visual near the end",'
        '"spoken_samples":[{"t":0,"quote":"exact consecutive words heard"}],'
        '"findings":[{"start_s":0,"end_s":0,"kind":"lip_sync|picture_speech","detail":"what happened"}]}. '
        "Include speech examples around the first and last thirds if speech is present and an empty findings "
        "list if no issue. State uncertainty as an issue. Do not infer what is beyond your input."
    )
    if use_api:
        raw = native_review(file, prompt, output, part_duration)
    else:
        raw = subscription_review(file, output, prompt)
    raw = raw.strip()
    raw = re.sub(r"^\x60\x60\x60(?:json)?\s*|\s*\x60\x60\x60$", "", raw, flags=re.I)
    report = strict_json(raw)
    if isinstance(report, list) and len(report) == 1:
        report = report[0]
    if report["moving_video"] is not True or report["audio"] is not True or report["verdict"] == "UNAVAILABLE":
        raise ValueError("Gemini could not inspect moving picture with native audio")
    if not abs(float(report["inspected_seconds"]) - part_duration) <= max(1.0, 2 / fps):
        raise ValueError("Gemini did not inspect this complete part")
    if not report["last_picture"].strip():
        raise ValueError("Gemini did not report the ending picture")
    if not isinstance(report["findings"], list) or not isinstance(report["spoken_samples"], list):
        raise ValueError("Gemini did not return structured findings and speech samples")
    findings = []
    for finding in report["findings"]:
        first = float(finding["start_s"])
        last = float(finding["end_s"])
        if not 0 <= first <= last <= part_duration + 1 or not finding["detail"].strip():
            raise ValueError("Gemini returned a finding without a usable timestamp or detail")
        findings.append({**finding, "start_s": round(start + first, 3), "end_s": round(start + last, 3)})
    if report["verdict"] not in ("PASS", "FAIL"):
        raise ValueError(f"unrecognized Gemini verdict {report['verdict']!r}")
    return {"result": "PASS" if report["verdict"] == "PASS" and not findings else "FAIL",
            "findings": findings, "start_s": start, "end_s": end,
            "spoken_samples": report["spoken_samples"]}


def gemini_review(video, duration, fps, ffmpeg, artifacts):
    artifacts.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="client-av-") as scratch:
        scratch = Path(scratch)
        # Stream copy keeps moving frames and audio from the exact checked movie.
        # Segment at keyframes to fit Antigravity's 100 MB attachment limit.
        subprocess.run(
            [ffmpeg, "-nostdin", "-v", "error", "-i", str(video), "-map", "0:v:0", "-map", "0:a:0",
             "-c", "copy", "-f", "segment", "-segment_time", "45", "-reset_timestamps", "1",
             "-segment_list", str(scratch / "parts.csv"), str(scratch / "part%03d.mp4")],
            check=True, capture_output=True, text=True,
        )
        parts = [(scratch / name, float(start), float(end))
                 for name, start, end in (line.split(",") for line in (scratch / "parts.csv").read_text().splitlines())]
        if not parts or abs(parts[-1][2] - duration) > 2 / fps:
            raise ValueError("Gemini attachment split does not cover the end of the file")
        previous_end = 0
        for file, start, end in parts:
            if abs(start - previous_end) > 2 / fps or start >= end:
                raise ValueError(f"gap or invalid interval in Gemini attachments near {start:.2f}s")
            if file.stat().st_size >= 95_000_000:
                raise ValueError("Gemini attachment exceeds the safe limit; use a smaller keyframe interval")
            previous_end = end
        first = checked_call(lambda: review_part(*parts[0], fps, artifacts))
        use_api = "error" in first
        reserved = gemini_budget(parts) if use_api else 0
        remaining = parts if use_api else parts[1:]
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as workers:
            results = list(workers.map(
                lambda part: checked_call(lambda: review_part(*part, fps, artifacts, use_api)), remaining,
            ))
        if not use_api:
            results.insert(0, first)
        for result, (file, start, end) in zip(results, parts):
            result.update(start_s=start, end_s=end, attachment_sha256=sha256(file))
    costs = [gemini_cost(load_json(file)["usageMetadata"]) for file in artifacts.glob("*.api.json")]
    return {"result": "PASS" if all(part["result"] == "PASS" for part in results) else "FAIL",
            "parts": results, "estimated_usd": round(sum(c[0] for c in costs), 6),
            "usage_upper_usd": round(sum(c[1] for c in costs), 6),
            "reserved_max_usd": round(reserved, 6),
            "billing": "Gemini API" if use_api else "Google AI subscription",
            "subscription_attempt": first}


def check_gemini_speech(report, words):
    for part in report.get("parts", []):
        if part["result"] != "PASS":
            continue
        start, end = part["start_s"], part["end_s"]
        if any(start + 2 < onset < end - 2 for _, onset, _ in words) and not any(
            any(abs(hit - (start + float(sample["t"]))) <= 5
                for hit in matching_quote(words, sample["quote"]))
            for sample in part["spoken_samples"]
        ):
            part.update(result="FAIL", error="Gemini's speech sample did not match the final-file transcription")
            report["result"] = "FAIL"
    return report


def run_gate(video, job, rows):
    digest = sha256(video)
    evidence = evidence_dir(job, digest)
    evidence.mkdir(parents=True, exist_ok=True)
    with (evidence / "gate.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("a delivery gate is already checking these exact video bytes") from None
        return run_checks(video, job, rows, digest, evidence)


def run_checks(video, job, rows, digest, evidence):
    inputs = {"rows": fingerprint(rows)}
    checks = {check: {"result": "FAIL", "error": "required evidence unavailable"} for check in CHECKS}
    receipt = {"version": VERSION, "job": str(job), "sha256": digest, "result": "FAIL",
               "checks": checks, "inputs": inputs}
    # Invalidate any old PASS while a rerun is in progress.
    write_json(receipt_path(video), {**receipt, "time": datetime.datetime.now(datetime.timezone.utc).isoformat()})
    try:
        manifest_path = evidence / "inputs.json"
        inputs["manifest"] = fingerprint(manifest_path)
        config = load_json(manifest_path)
        if config["sha256"] != digest:
            raise ValueError("render inputs are for different video bytes")
        if not isinstance(config["editor"], str) or not config["editor"].strip():
            raise ValueError("render inputs do not identify the editor")
        for key in ("captions", "source_map"):
            inputs[key] = fingerprint(evidence / config[key])
            if inputs[key]["sha256"] != config[key + "_sha256"]:
                raise ValueError(f"{key} differs from the render inputs manifest")

        sys.path.insert(0, str(SKILLS))
        from _shared.cut import speech
        duration, fps = probe(video, speech.FP)
        receipt["duration_s"] = duration

        def source_sync():
            data = load_json(Path(inputs["source_map"]["path"]))
            if data["kind"] == "source_ranges":
                return check_source_ranges(data, duration, fps)
            if data["kind"] == "joint_vigor":
                for kind in ("plan", "edl"):
                    inputs[kind] = fingerprint(Path(data[kind]))
                    if inputs[kind]["sha256"] != data[kind + "_sha256"]:
                        raise ValueError(f"archived {kind} differs from the render source map")
                return joint_vigor_plan(data, duration, fps)
            raise ValueError(f"unknown source map kind {data['kind']!r}")

        review_path = evidence / "blind-review.json"

        def get_review():
            inputs["blind_review"] = fingerprint(review_path)
            return blind_review(review_path, digest, config["editor"], duration)

        checks["source_sync"] = checked_call(source_sync)
        checks["blind_review"] = checked_call(get_review)
        print(f"{video.name}: source sync {checks['source_sync']['result']}, "
              f"blind review {checks['blind_review']['result']}. Checking the final audio and video.", flush=True)
        words = []
        run_artifacts = Path(tempfile.mkdtemp(prefix="run-", dir=evidence))

        def captions():
            raw_words, origin = speech.transcribe(str(video), model="small.en")
            words.extend(transcript_words(raw_words))
            transcript_path = run_artifacts / "final-transcript.json"
            write_json(transcript_path, {"sha256": digest, "origin": origin, "words": words})
            inputs["transcript"] = fingerprint(transcript_path)
            return caption_alignment(Path(inputs["captions"]["path"]), words, duration, fps)

        with tempfile.TemporaryDirectory(prefix="gemini-evidence-", dir=run_artifacts) as temp:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as workers:
                gemini = workers.submit(
                    checked_call, lambda: gemini_review(video, duration, fps, speech.FF, Path(temp))
                )
                checks["captions"] = checked_call(captions)
                checks["rows"] = checked_call(
                    lambda: verify_rows(load_json(rows), checks["blind_review"], words, duration)
                )
                checks["gemini"] = checked_call(lambda: check_gemini_speech(gemini.result(), words))
            # Preserve the model's replies even when no PASS can be issued.
            audit = run_artifacts / "gemini-av-review.json"
            write_json(audit, {"sha256": digest, "checks": checks["gemini"],
                               "responses": {file.name: file.read_text(errors="replace") for file in Path(temp).iterdir()}})
            inputs["gemini"] = fingerprint(audit)
        for key, artifact in inputs.items():
            if sha256(Path(artifact["path"])) != artifact["sha256"]:
                raise ValueError(f"{key} changed while running the gate")
        if sha256(video) != digest:
            raise ValueError("video changed while running the gate")
        receipt["result"] = "PASS" if all(check["result"] == "PASS" for check in checks.values()) else "FAIL"
    except (ImportError, *INPUT_ERRORS) as error:
        receipt["error"] = str(error)
    receipt["time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write_json(receipt_path(video), receipt)
    print(f"CLIENT DELIVERY GATE {receipt['result']} | {video.name} | sha256 {digest}")
    for name, check in checks.items():
        detail = check.get("error")
        if not detail and check["result"] == "FAIL":
            counts = ("timing_violations", "word_mismatches", "mismatches", "problems")
            detail = ", ".join(f"{len(check[key])} {key.replace('_', ' ')}" for key in counts if check.get(key))
            if name == "gemini":
                detail = f"{sum(part['result'] != 'PASS' for part in check['parts'])} flagged or incomplete parts"
        print(f"  {name}: {check['result']}" + (f" ({detail})" if detail else ""))
    if receipt.get("error"):
        print(f"  {receipt['error']}")
    print(f"  Receipt: {receipt_path(video)}")
    return int(receipt["result"] != "PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--job", required=True, type=Path)
    parser.add_argument("--rows", required=True, type=Path)
    args = parser.parse_args()
    try:
        return run_gate(args.file.resolve(strict=True), args.job.resolve(strict=True), args.rows.resolve())
    except INPUT_ERRORS as error:
        parser.exit(1, f"CLIENT DELIVERY GATE FAILED: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
