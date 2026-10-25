#!/usr/bin/env python3
"""Prepare a bounded private display copy; never edit operational social state."""
import argparse
import copy
import hashlib
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from collect_inputs import private_directory, write_private


def bounded(value, limit):
    return value.encode('utf-16-le')[:limit * 2].decode('utf-16-le', errors='ignore')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    source = Path(args.source).resolve()
    output = private_directory(Path(args.output))
    if source == output:
        raise ValueError('Display copy must be separate from operational state')
    files = [source / name for name in ['social-queue.json', 'social-master-export.json']]
    before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    queue = copy.deepcopy(json.loads(files[0].read_text()))
    edits = []
    obsolete = {'More than one YouTube long-form in this Sunday week', 'Long-form YouTube must release Sunday at 9 AM Central'}
    for row in queue['rows']:
        original = row.get('caption', '')
        row['caption'] = bounded(original, 1000)
        if original != row['caption']:
            edits.append({'id': row['id'], 'reason': 'Display caption bounded to 1000 UTF-16 units'})
        at = datetime.fromisoformat(row['scheduledAt'].replace('Z', '+00:00')).astimezone(ZoneInfo('America/Chicago'))
        if row['platform'] == 'youtube' and obsolete.intersection(row.get('notes', [])) and at.weekday() in (2, 6) and (at.hour, at.minute, at.second) == (9, 0, 0):
            row['notes'] = [n for n in row['notes'] if n not in obsolete]
            row['notes'].append('Current rule permits Sunday/Wednesday at 9 AM Central; approved release date still needs verification.')
            row['preflight']['cadence'] = 'unverified'
            edits.append({'id': row['id'], 'reason': 'Obsolete Sunday-only rule removed; approval remains unverified'})
    write_private(output / 'social-queue.json', queue)
    write_private(output / 'social-master-export.json', json.loads(files[1].read_text()))
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == before[p.name] for p in files)
    write_private(output / 'preparation-proof.json', {'checkedAt': datetime.now().astimezone().isoformat(), 'sourceHashes': before, 'operationalSourcesUnchanged': True, 'edits': edits})
    print(json.dumps({'queueRows': len(queue['rows']), 'displayEdits': len(edits), 'operationalSourcesUnchanged': True}))


if __name__ == '__main__':
    main()
