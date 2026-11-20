"""Guard client review page builders and stage only the bytes checked by the gate."""
import argparse
import html
from pathlib import Path
import shutil
import tempfile

from delivery_gate import require_receipt, sha256


def checked_review(video, captions, rows_path, job):
    try:
        receipt, rows = require_receipt(video, rows_path, job=job, captions=captions)
    except ValueError as error:
        raise SystemExit(str(error)) from None
    confirmed = receipt["checks"]["rows"]["verified"]
    for row in rows["asked"]:
        verification = confirmed.get(row["id"])
        row["verdict"] = "Done" if verification else "not yet"
        row["t"] = verification["t"] if verification else None
        if not verification:
            row["fix"] = ""
    for row in rows.get("open", []):
        row.pop("t", None)
    rows["checks"] = [
        "Caption timing, picture-to-dialogue source times and Gemini video with audio passed.",
        "Independent whole-film review with sound passed.",
        f"{len(confirmed)} rows verified against the final film's transcript.",
        f"Video SHA-256 {receipt['sha256']}",
    ]
    return receipt, rows


def review_args(video, captions, job):
    parser = argparse.ArgumentParser(description="Build a client review page from a passing delivery receipt.")
    parser.add_argument("rows", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--video", type=Path, default=video)
    parser.add_argument("--captions", type=Path, default=captions)
    parser.add_argument("--job", type=Path, default=job)
    args = parser.parse_args()
    receipt, rows = checked_review(args.video, args.captions, args.rows, args.job)
    names = stage_media(args.video, args.captions, args.out, receipt)
    return args.out, rows, names


def stage_media(video, captions, out, receipt):
    media = Path(out) / "media"
    media.mkdir(parents=True, exist_ok=True)
    names = []
    for source, digest in ((video, receipt["sha256"]), (captions, receipt["inputs"]["captions"]["sha256"])):
        source = Path(source)
        name = f"{source.stem}-{digest[:16]}{source.suffix}"
        dest = media / name
        if not (dest.is_file() and sha256(dest) == digest):
            with tempfile.NamedTemporaryFile(dir=media, delete=False) as temp:
                staged = Path(temp.name)
                try:
                    with source.open("rb") as original:
                        shutil.copyfileobj(original, temp)
                    temp.close()
                    if sha256(staged) != digest:
                        raise SystemExit(f"Delivery blocked: {source.name} changed during copy.")
                    staged.chmod(0o644)
                    staged.replace(dest)
                finally:
                    staged.unlink(missing_ok=True)
        names.append(name)
    return names


def row_table(rows):
    """R4's simple review page uses the same status and timestamp rules as R5."""
    entries = []
    for row in rows["asked"]:
        time = row["t"]
        watch = "" if time is None else (
            f'<button onclick="go({time:.3f})">{int(time // 60)}:{time % 60:05.2f}</button>'
        )
        cells = [html.escape(row["verdict"]), html.escape(row["words"]), html.escape(row["fix"]), watch]
        entries.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in cells) + "</tr>")
    return "<table>" + "".join(entries) + "</table>"


def write_page(out, page):
    assert "—" not in page and "–" not in page, "dash in page"
    out = Path(out)
    with tempfile.NamedTemporaryFile(mode="w", dir=out, encoding="utf-8", delete=False) as temp:
        staged = Path(temp.name)
        try:
            temp.write(page)
            temp.close()
            staged.chmod(0o644)
            staged.replace(out / "index.html")
        finally:
            staged.unlink(missing_ok=True)
