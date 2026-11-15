"""Owner-side guarded mirror refresh. Staging never writes over a registered review."""
import fcntl
import json
from pathlib import Path
import socket
import subprocess
import sys
import urllib.request
import os


def preflight(port, dest, job, source):
    home=Path.home();dest=Path(dest).resolve()
    candidates=[home/'Library/Application Support/AbsByAI Review Hub/pages'/f'{port}.json',
                home/'Library/Application Support/AbsByAI Reviews'/str(port)/'manifest.json']
    for p in candidates:
        if p.exists():
            x=json.loads(p.read_text());root=x.get('root') or x.get('source')
            if root and Path(root).resolve()!=dest:raise RuntimeError('port belongs to another review')
    marker=dest/'.mirror-owner.json'
    if marker.exists():
        old=json.loads(marker.read_text())
        if (job and old.get('job') and old['job']!=job) or (not (job and old.get('job')) and old.get('source')!=source):
            raise RuntimeError('mirror belongs to another job')
    notes=home/'.absbyai-editroute/reviews.json'
    if notes.exists():
        old=json.loads(notes.read_text()).get(str(port),{})
        if old.get('job') and job and old['job']!=job:raise RuntimeError('port note belongs to another job')
        if old.get('source') and not (old.get('job') and job and old['job']==job) and old['source']!=source:raise RuntimeError('port source identity differs')
    with socket.socket() as s:
        s.settimeout(.5);busy=s.connect_ex(('127.0.0.1',port))==0
    if busy:
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/__review_health',timeout=2) as r:x=json.load(r)
            if Path(x['root']).resolve()!=dest:raise RuntimeError('occupied port has another owner')
        except Exception as e:raise RuntimeError('cannot safely refresh occupied port: '+str(e))


def main():
    port=int(sys.argv[1]);dest=Path(sys.argv[2]).expanduser();job=sys.argv[3];source=sys.argv[4]
    base=dest.parent;base.mkdir(parents=True,exist_ok=True)
    with (base/(str(port)+'.mirror.lock')).open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX);preflight(port,dest,job,source)
        if len(sys.argv)==5:return
        stage=Path(sys.argv[5]);server=sys.argv[6]
        dest.mkdir(parents=True,exist_ok=True)
        subprocess.run(['rsync','-a',str(stage)+'/',str(dest)+'/'],check=True)
        (dest/'.mirror-owner.json').write_text(json.dumps(dict(job=job,source=source)))
        subprocess.run(['python3',server,str(port),str(dest)],env=dict(os.environ,ABS_REVIEW_NO_MIRROR='1'),check=True)

if __name__=='__main__':main()
