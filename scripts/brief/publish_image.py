#!/usr/bin/env python3
"""Publish one approved private local image with a Mac-held signing key."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    parser.add_argument("--key-file", default=str(Path.home() / ".absbyai-brief" / "publish-key.pem"))
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    try:
        file = Path(args.image).expanduser().resolve()
        if any((parent / ".git").exists() for parent in (file.parent, *file.parents)):
            raise ValueError("Image must remain outside Git")
        if not 4 < file.stat().st_size <= 8 * 1024 * 1024:
            raise ValueError("Image size invalid")
        data = file.read_bytes()
        mime = "image/png" if data.startswith(b"\x89PNG\r\n\x1a\n") else "image/jpeg" if data.startswith(b"\xff\xd8") and data.endswith(b"\xff\xd9") else None
        if not mime:
            raise ValueError("Unsupported image")
        digest = hashlib.sha256(data).hexdigest()
        if args.publish:
            signer = Path(__file__).parent / "mac_signer.js"
            signed = subprocess.run(["node", str(signer), "--sign-image", str(Path(args.key_file).expanduser())], input=data, capture_output=True, timeout=15)
            if signed.returncode:
                raise ValueError("Local signing unavailable")
            headers = json.loads(signed.stdout)
            headers["Content-Type"] = mime
            request = Request("https://absbyai.com/api/brief/image/publish", data=data, headers=headers, method="POST")
            with urlopen(request, timeout=30) as response:
                receipt = json.load(response)
            if receipt.get("ok") is not True or receipt.get("sha256") != digest or receipt.get("mime") != mime:
                raise ValueError("Publication receipt not verified")
        print(json.dumps({"status": "published" if args.publish else "validated_only", "sha256": digest, "mime": mime, "routineEnabled": False}))
        return 0
    except Exception:
        print("Private image validation/publication failed; no successful publication claimed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
