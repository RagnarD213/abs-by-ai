"""One owner-side calculation for incremental work-space commitments.
Reservations keep their remaining additional GB until consumed or explicitly abandoned.
"""
import contextlib
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time


def state_dir():
    return Path(os.environ.get('EDIT_STORAGE_DIR') or os.environ.get('EDITROUTE_DIR') or Path.home()/'.absbyai-editroute')


def reserve_gb(drive):
    return {'internal':80.0,'Extreme':30.0}.get(drive,100.0)


def available(free,committed,need,drive):
    if free is None:return False,'free space unknown'
    left=free-committed-need
    return left>=reserve_gb(drive), '{:.1f} GB free - {:.1f} committed - {:.1f} additional; {:.0f} GB reserve'.format(free,committed,need,reserve_gb(drive))


def usable(path):
    path=Path(path)
    if not str(path).startswith('/Volumes/'):return True
    root=Path('/Volumes')/path.parts[2]
    if not os.path.ismount(root):return False
    r=subprocess.run(['mount'],capture_output=True,text=True,timeout=3)
    line=next((l for l in r.stdout.splitlines() if ' on '+str(root)+' (' in l),'')
    return bool(line) and not any(k in line for k in ('smbfs','nfs','afpfs','webdav'))


def read():
    try:return json.loads((state_dir()/'storage.json').read_text())
    except FileNotFoundError:return {}


@contextlib.contextmanager
def locked():
    d=state_dir();d.mkdir(parents=True,exist_ok=True)
    with (d/'storage.lock').open('a') as f:
        fcntl.flock(f,fcntl.LOCK_EX);yield


def check(path,need,job,commit=False):
    if need<0:raise ValueError('need must be nonnegative')
    p=Path(path)
    while not p.exists() and p!=p.parent:p=p.parent
    if not usable(path):raise RuntimeError('work storage is missing or is a network share')
    drive=Path(path).parts[2] if str(path).startswith('/Volumes/') else 'internal'
    with locked():
        records=read()
        used=sum(v['remaining_gb'] for k,v in records.items() if k!=job and v['drive']==drive)
        ok,why=available(shutil.disk_usage(p).free/1e9,used,need,drive)
        if not ok:raise RuntimeError('storage: '+why)
        if commit:
            records[job]=dict(drive=drive,path=str(path),remaining_gb=need,t=time.time())
            save(records)
        return why


def save(records):
    p=state_dir()/'storage.json';tmp=p.with_name('storage.%s.tmp'%os.getpid());tmp.write_text(json.dumps(records));os.replace(tmp,p)


def consume(job,gb=None):
    with locked():
        r=read()
        if gb is None:r.pop(job,None)
        elif job in r:r[job]['remaining_gb']=max(0,r[job]['remaining_gb']-gb)
        save(r)
