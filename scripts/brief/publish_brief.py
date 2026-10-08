#!/usr/bin/env python3
"""Validate a private writer document; publish only with explicit --publish."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone
from urllib.request import Request, urlopen


def private_file(file):
    file = Path(file).expanduser().resolve()
    if any((parent / '.git').exists() for parent in (file, file.parent, *file.parents)):
        raise ValueError('Private inputs must remain outside Git')
    return file


def social_inputs(directory, now=None):
    now = now or datetime.now(timezone.utc)
    directory = private_file(directory)
    if directory.stat().st_mode & 0o077:
        raise ValueError('Private social directory permissions')
    queue = json.loads((directory / 'social-queue.json').read_text())
    checked = datetime.fromisoformat(queue['checkedAt'].replace('Z', '+00:00'))
    age = (now - checked).total_seconds()
    if not 0 <= age <= 12 * 3600:
        raise ValueError('Social review is stale')
    records = json.loads((directory / 'social-master-export.json').read_text())
    if not isinstance(records, list):
        raise ValueError('Invalid social inventory')
    return queue, records


def batches(document, records):
    """A bounded transport never truncates the unlimited inventory."""
    if not records:
        yield json.dumps(document).encode(), 0
        return
    offset = 0
    while offset < len(records):
        size = min(100, len(records) - offset)
        while True:
            data = json.dumps({**document, 'socialMasterImports': records[offset:offset+size]}).encode()
            if len(data) <= 512000:
                break
            if size == 1:
                raise ValueError('One inventory record exceeds publication size')
            size = max(1, size // 2)
        yield data, size
        offset += size


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", help="Structured private edition JSON outside Git")
    parser.add_argument("--publish", action="store_true")
    parser.add_argument("--key-file", default=str(Path.home() / ".absbyai-brief" / "publish-key.pem"))
    parser.add_argument('--social-state-dir', help='Private fresh queue and complete master export; imports every record in bounded batches')
    parser.add_argument('--refresh-social-project', help='Run the read-only social review after edition creation, using this existing project root')
    args = parser.parse_args()
    try:
        file = private_file(args.document)
        data = file.read_bytes()
        if len(data) > 512000:
            raise ValueError("Document too large")
        validator = Path(__file__).parent / "web/document.js"
        records = []
        if args.refresh_social_project:
            if not args.social_state_dir:
                raise ValueError('Social refresh needs a private state directory')
            refreshed = subprocess.run([sys.executable, str(Path(__file__).parent / 'social_daily.py'),
                                        '--project-root', args.refresh_social_project, '--state-dir', args.social_state_dir, '--live'],
                                       capture_output=True, timeout=180)
            if refreshed.returncode:
                raise ValueError('Social read-only refresh failed')
        if args.social_state_dir:
            queue, records = social_inputs(args.social_state_dir)
            draft = json.loads(data)
            draft['socialReleaseQueue'] = queue
            data = json.dumps(draft).encode()
            # Validate all import batches before sending the first publication.
            social_validator = Path(__file__).parent / 'web/social.js'
            script = "const fs=require('fs');const {validateMaster}=require(process.argv[1]);const rows=JSON.parse(fs.readFileSync(0,'utf8'));for(let i=0;i<rows.length;i+=100)validateMaster(rows.slice(i,i+100));"
            checked = subprocess.run(['node','-e',script,str(social_validator)],input=json.dumps(records).encode(),capture_output=True,timeout=15)
            if checked.returncode:
                raise ValueError('Master import validation failed')
        # The validator is a trusted absolute local path, passed as an argv value.
        script = "const fs=require('fs');const {validate}=require(process.argv[1]);process.stdout.write(JSON.stringify(validate(JSON.parse(fs.readFileSync(0,'utf8')))));"
        result = subprocess.run(["node", "-e", script, str(validator)], input=data, capture_output=True, timeout=15)
        if result.returncode:
            raise ValueError("Writer document validation failed")
        document = json.loads(result.stdout)
        if args.publish:
            signer = Path(__file__).parent / "mac_signer.js"
            for body, size in batches(document, records):
                signed = subprocess.run(["node", str(signer), "--sign", str(Path(args.key_file).expanduser())],
                                        input=body, capture_output=True, timeout=15)
                if signed.returncode:
                    raise ValueError("Local signing unavailable")
                headers = json.loads(signed.stdout)
                headers["Content-Type"] = "application/json"
                request = Request("https://absbyai.com/api/brief/publish", data=body,
                                  headers=headers, method="POST")
                with urlopen(request, timeout=25) as response:
                    receipt = json.load(response)
                if (receipt.get("ok") is not True or receipt.get("forDate") != document["forDate"]
                        or receipt.get("routineEnabled") != document["routineEnabled"] or receipt.get('scheduleChanged') is not False
                        or (size and receipt.get('masterImported') != size)):
                    raise ValueError("Publication receipt not verified")
        print(json.dumps({"status": "published" if args.publish else "validated_only", "forDate": document["forDate"],
                          "editionType": document["editionType"], "routineEnabled": document["routineEnabled"], "scheduleChanged": False,
                          'masterRecords': len(records)}))
        return 0
    except Exception:
        # Provider bodies, credentials and private document text never reach stdout.
        print("Brief validation/publication failed; no successful publication claimed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
