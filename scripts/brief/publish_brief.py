#!/usr/bin/env python3
"""Validate a private writer document; publish only with explicit --publish."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", help="Structured private edition JSON outside Git")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--key-file", default=str(Path.home() / ".absbyai-brief" / "publish-key.pem"))
    args = parser.parse_args()
    try:
        file = Path(args.document).expanduser().resolve()
        if any((parent / ".git").exists() for parent in (file.parent, *file.parents)):
            raise ValueError("Document must remain outside Git")
        data = file.read_bytes()
        if len(data) > 512000:
            raise ValueError("Document too large")
        validator = Path(__file__).parent / "web/document.js"
        # The validator is a trusted absolute local path, passed as an argv value.
        script = "const fs=require('fs');const {validate}=require(process.argv[1]);process.stdout.write(JSON.stringify(validate(JSON.parse(fs.readFileSync(0,'utf8')))));"
        result = subprocess.run(["node", "-e", script, str(validator)], input=data, capture_output=True, timeout=15)
        if result.returncode:
            raise ValueError("Writer document validation failed")
        document = json.loads(result.stdout)
        if args.publish:
            signer = Path(__file__).parent / "mac_signer.js"
            signed = subprocess.run(["node", str(signer), "--sign", str(Path(args.key_file).expanduser())],
                                    input=result.stdout, capture_output=True, timeout=15)
            if signed.returncode:
                raise ValueError("Local signing unavailable")
            headers = json.loads(signed.stdout)
            headers["Content-Type"] = "application/json"
            request = Request("https://absbyai.com/api/brief/publish", data=result.stdout,
                              headers=headers, method="POST")
            with urlopen(request, timeout=25) as response:
                receipt = json.load(response)
            if receipt.get("ok") is not True or receipt.get("forDate") != document["forDate"] or receipt.get("routineEnabled") != document["routineEnabled"]:
                raise ValueError("Publication receipt not verified")
        print(json.dumps({"status": "published" if args.publish else "validated_only", "forDate": document["forDate"],
                          "editionType": document["editionType"], "routineEnabled": document["routineEnabled"], "scheduleChanged": False}))
        return 0
    except Exception:
        # Provider bodies, credentials and private document text never reach stdout.
        print("Brief validation/publication failed; no successful publication claimed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
