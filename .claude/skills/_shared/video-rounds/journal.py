"""Only manages a new per-video controller journal. Never touches Codex databases/media."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile


def verify(files, decisions):
    if not Path(decisions).is_file():
        raise ValueError('Decisions file is missing')
    for item in files:
        path = Path(item['path'])
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != item['sha256']:
            raise ValueError('Approved file hash changed: ' + str(path))


def cas(path, expected, state):
    path = Path(path)
    if path.name != 'round-controller.json':
        raise ValueError('Use a dedicated round-controller.json, never an existing job/media file')
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.with_suffix('.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        current = json.loads(path.read_text()) if path.exists() else None
        if (current['revision'] if current else None) != expected:
            raise ValueError('Concurrent update or duplicate launch; reload journal before doing anything')
        if current and (current['key'] != state['key'] or current['plan'] != state['plan']):
            raise ValueError('Cannot replace a reserved round packet')
        if state['revision'] != (0 if expected is None else expected + 1):
            raise ValueError('Invalid journal revision')
        fd, temporary = tempfile.mkstemp(prefix='.round-controller-', dir=path.parent)
        try:
            with os.fdopen(fd, 'w') as output:
                json.dump(state, output, indent=2)
                output.write('\n')
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    return state


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['read', 'cas', 'verify'])
    parser.add_argument('--path')
    parser.add_argument('--json', default='{}')
    args = parser.parse_args()
    data = json.loads(args.json)
    if args.action == 'verify':
        verify(data['files'], data['decisions'])
        print(json.dumps({'verified': True}))
    elif args.action == 'read':
        path = Path(args.path)
        print(path.read_text() if path.exists() else 'null')
    else:
        print(json.dumps(cas(args.path, data['expected'], data['state'])))


if __name__ == '__main__':
    main()
