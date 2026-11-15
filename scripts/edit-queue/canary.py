#!/usr/bin/env python3
"""Real one-turn readiness proof, consumed only by the installed launchd tick."""
import fcntl
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eq_common as eq
eq.unshadow()

HOME = Path.home() / '.absbyai-batch'

def save(path, doc):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w') as f:
        json.dump(doc, f, indent=2); f.flush(); os.fsync(f.fileno())
    tmp.replace(path)

def pending():
    request = HOME / 'canary-request.json'
    if not request.exists():
        return False
    HOME.mkdir(parents=True, exist_ok=True)
    with (HOME / 'canary.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return True
        req = json.loads(request.read_text())
        root = HOME / 'canary' / req['id']
        root.mkdir(parents=True, exist_ok=True)
        result = root / 'result.json'
        if result.exists() and json.loads(result.read_text()).get('finished'):
            return False
        cfg = eq.load_config()
        doc = dict(id=req['id'], started=time.time(), pid=os.getpid(), parent=os.getppid(), rows=[])
        save(result, doc)
        for executor in ('claude', 'codex'):
            for role in ('editor', 'reviewer'):
                token = 'CANARY_' + uuid.uuid4().hex
                prompt = ('This is an authorized one-turn launcher readiness test for the '+role+
                          ' role, not a video job. Use no tools and do no work. Reply with exactly: '+token)
                command = eq.build_command(executor, cfg, str(root), 'review-canary' if role=='reviewer' else 'edit-canary')
                reply = root / (executor+'-'+role+'-reply.txt')
                if executor == 'claude':
                    command[command.index('--output-format')+1] = 'json'
                    command += ['--max-turns', '1']
                else:
                    command[-1:-1] = ['--output-last-message', str(reply)]
                started = time.time()
                try:
                    run = subprocess.run(command, input=prompt, capture_output=True, text=True,
                                         cwd=eq.ROOT, timeout=180)
                    (root / (executor+'-'+role+'.log')).write_text(run.stdout+'\n'+run.stderr)
                    if executor == 'claude':
                        answer = json.loads(run.stdout).get('result', '')
                        reply.write_text(answer)
                    else:
                        answer = reply.read_text() if reply.exists() else ''
                    row = dict(executor=executor, role=role, code=run.returncode,
                               passed=run.returncode==0 and answer.strip()==token,
                               reply=str(reply), seconds=round(time.time()-started,2))
                except Exception as exc:
                    row = dict(executor=executor, role=role, passed=False, error=str(exc))
                doc['rows'].append(row); save(result, doc)
        doc.update(finished=time.time(), passed=all(row['passed'] for row in doc['rows']))
        save(result, doc)
        save(HOME / 'canary-latest.json', doc)
        print('Real session canary:', result, 'PASS' if doc['passed'] else 'FAIL', flush=True)
        return True

if __name__ == '__main__':
    HOME.mkdir(parents=True, exist_ok=True)
    if len(sys.argv)>1 and sys.argv[1]=='request':
        ident = time.strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6]
        save(HOME / 'canary-request.json', dict(id=ident, requested=time.time()))
        print(ident)
    else:
        pending()
