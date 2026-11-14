"""Read-only macOS observer. No scheduler imports, writes, external volumes or raw CLI output."""
import ctypes as C
import fcntl
import hashlib
import itertools
import json
import os
import re
import resource
import signal
import socket
import stat
import struct
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATES = {'active','promoted','waiting','with-dan','stalled','parked','finished'}
POLICY = json.loads((HERE/'policy.json').read_text())
_cache = {}


def raw(p, limit=1048576, tail=False):
    # Never follow record symlinks, wait on FIFOs or read an unbounded history.
    fd = os.open(p, os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        st=os.fstat(fd)
        if not stat.S_ISREG(st.st_mode): raise ValueError()
        cut = st.st_size>limit
        if cut:
            if not tail: raise ValueError()
            f.seek(-limit,2)
        data=f.read(limit+1)
        if len(data)>limit: raise ValueError()
        return (data.partition(b'\n')[2] if cut else data),cut


def read(p):
    return json.loads(raw(p)[0])


def memo(p, fn):
    st=p.stat()
    stamp=st.st_ino,st.st_mtime_ns,st.st_size
    if _cache.get(p,(None,))[0]!=stamp: _cache[p]=(stamp,fn(raw(p)[0]))
    return _cache[p][1]


def key(s):
    s=str(s).upper().removeprefix('WORK:')
    # Any suffix on the blind project is discarded before JSON serialization.
    if re.fullmatch(r'PG:\d+',s):return 'Unassigned render work'
    if re.search(r'DS[-_ ]?0?98(?!\d)',s): return 'DS-98'
    m=re.match(r'^([A-Z]{2,3})-?(\d{1,3}[A-Z]?)(?!\d)',s)
    if m: return m[1]+'-'+m[2]
    if re.fullmatch(r'(?:REALDEMOS|EXDEMO|SHOOT|SRM)(?:-[A-Z0-9]+){0,4}',s):return s
    return 'Unidentified project'


def get_titles(repo):
    return memo(repo/'Handoffs/video-editing/jobs.json',lambda b:{key(e['id']):e['title'] for e in json.loads(b)['jobs']})


def kernel():
    k=C.CDLL(str(HERE/'kernel.dylib'))
    k.idle_seconds.restype=C.c_double
    k.matches.argtypes=[C.c_int,C.c_double,C.c_int]
    return k


def locked(fd):
    # Darwin F_GETLK is a query only. -1 owner PID is expected for BSD flock.
    fmt='qqihh'
    ans=fcntl.fcntl(fd,fcntl.F_GETLK,struct.pack(fmt,0,0,0,fcntl.F_WRLCK,0))
    return struct.unpack(fmt,ans)[3]!=fcntl.F_UNLCK


def render_rows(rq,k):
    out=[]
    for sub in ('slots','queue'):
        directory=rq/sub
        names=list(itertools.islice(directory.iterdir(),257))
        if len(names)>256 or (sub=='slots' and not any(p.suffix=='.lock' for p in names)):raise ValueError()
        for p in names:
            if p.name.startswith('.') or p.suffix!=('.lock' if sub=='slots' else '.json'):continue
            fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode): raise ValueError()
                if not locked(fd):continue
                h=read(p.with_suffix('.json')); is_slot=sub=='slots'
                t=h['start' if is_slot else 'created']
                if h.get('ended') or not k.matches(int(h['pid']),float(t),fd) or not locked(fd):raise ValueError()
                if h.get('scheduler_version',5) not in (1,2,3,4,5):raise ValueError()
                cores=(int(h.get('cores') or {'heavy':4,'light':2,'quick':2}[h['pool']])) if is_slot else 0
                if is_slot and cores<=0:raise ValueError()
                out.append((key(h['group']),is_slot,cores,bool(h.get('priority'))))
            finally:os.close(fd)
    return out


def routes(d,window,now):
    line=read(d/'waiting.json')
    if not isinstance(line,dict):raise ValueError()
    buf,cut=raw(d/'decisions.jsonl',262144,True); latest={}; times=[]
    for s in buf.splitlines():
        e=json.loads(s); t=float(e['t']);times.append(t)
        if t>now+5 or (len(times)>1 and t<times[-2]-1):raise ValueError()
        if now-t<=window:latest[key(e['job'])]=None if e.get('dry') else e['host']
    if cut and (not times or times[0]>now-window):raise ValueError()
    if any(x not in ('m6','m2','wait',None) for x in latest.values()): raise ValueError()
    return {'line':sorted({key(j) for j in line}), 'reserved':{h:[j for j,v in latest.items() if v==h] for h in ('m6','m2')}}


def version(p): return memo(p,lambda b:hashlib.sha256(b).hexdigest())


def stamp(paths):
    def one(p):
        try:
            s=p.lstat();return s.st_ino,s.st_mtime_ns,s.st_size
        except FileNotFoundError:return None
    return tuple(one(p) for p in paths)


def observe(host,repo=None,tmp=Path('/tmp'),home=None,clock=time.time):
    now=clock(); home=home or Path.home()
    repo=repo or home/'Projects/Claude/Projects/Abs By AI'
    shared=repo/'.claude/skills/_shared'
    rq=Path(os.getenv('GATE_DIR',tmp/'absbyai-renderq')); ec=Path(os.getenv('EDITCAP_DIR',tmp/'absbyai-editcap'))
    route=Path(os.getenv('EDITROUTE_DIR',home/'.absbyai-editroute'))
    pr=Path(os.getenv('EDIT_PRIORITY_DIR',route)); storage=Path(os.getenv('EDIT_STORAGE_DIR',route))
    fallback=tmp/'absbyai-editroute'
    if not route.is_dir() and fallback.is_dir():route=fallback
    out={'host':host,'issues':[],'observed':now,'jobs':[], 'renders':None,'tickets':None,'used':None}
    def section(msg,fn):
        try:return fn()
        except (OSError,ValueError,TypeError,KeyError,AttributeError,IndexError,OverflowError):out['issues'].append(msg)
    cfg=section('Host settings unavailable',lambda:read(Path(os.getenv('EDITROUTE_HOSTS',shared/'editroute/hosts.json'))))
    hc={}
    if cfg:
        def config():
            h=cfg['hosts'][host]
            if cfg['primary']!='m6' or socket.gethostname().split('.')[0].lower() not in [n.lower() for n in h['names']]:raise ValueError()
            if min(int(h[v]) for v in ('slots','cores_present','cores_away','away_after_min'))<=0:raise ValueError()
            out['cap']=int(os.getenv('EDITCAP_MAX') or h['slots']);out['first']=h['first'];return h
        hc=section('Host identity or limits unknown',config) or {}
    def verify():
        if any(version(shared/p) not in (v if isinstance(v,list) else [v]) for p,v in POLICY.items()):raise ValueError()
    section('Installed scheduler version needs checking',verify)
    k=section('Kernel observations unavailable',kernel)
    if hc and k:
        idle=k.idle_seconds() if host=='m6' else -1
        away=idle>=60*hc['away_after_min']
        out.update(budget=hc['cores_away' if away else 'cores_present'],presence=('away' if away else 'recent input' if idle>=0 else 'input unknown') if host=='m6' else 'fixed')
    def pressure():
        val=C.c_int(); size=C.c_size_t(C.sizeof(val))
        if C.CDLL(None).sysctlbyname(b'kern.memorystatus_vm_pressure_level',C.byref(val),C.byref(size),None,0) or val.value not in (1,2,4): raise ValueError()
        return {1:'normal',2:'warning',4:'critical'}[val.value]
    out['pressure']=section('Memory pressure unknown',pressure)
    out['loadGuard']=bool(hc.get('load_guard') and os.getloadavg()[1]>(os.cpu_count() or 1))
    def features():
        f=read(rq/'features.json')
        if not all(type(f.get(x)) is bool for x in ('priority','fairness','borrowing')):raise ValueError()
        return f['priority']
    out['priorityEnabled']=section('Feature settings unknown',features)
    urgent=set()
    def reserve():
        x=read(pr/'priority.json')
        if x['version']!=1 or not isinstance(x['jobs'],dict):raise ValueError()
        urgent.update(key(j) for j,v in x['jobs'].items() if v['expires']>now)
        r=x['reservation'];return key(r['job']) if r and r['expires']>now and host=='m6' else None
    out['dedicated']=section('Dedicated reservation unknown',reserve)
    def space():
        sv=os.statvfs(home); rec=read(storage/'storage.json')
        return int(sv.f_bavail*sv.f_frsize/1e9-80-sum(float(v['remaining_gb']) for v in rec.values() if v['drive']=='internal'))
    out['internalRoom']=section('Internal storage headroom unknown',space)
    def unmanaged():
        x=read(rq/'unmanaged.json')
        if x['v']!=2 or not isinstance(x['builds'],list):raise ValueError()
        return {'count':len(x['builds']),'at':float(x['t'])}
    out['outside']=section('Outside work not measured',unmanaged)
    def mem():
        m=read(rq/'mem.json')['last']
        return {'at':float(m['t']),'ready':bool(m['ok'] and m['ok_for']>=30)}
    out['gate']=section('Render memory history unknown',mem)
    def adm():return max([float(t) for t in read(rq/'admits.json').values()]+[0])
    out['lastGrant']=section('Render settling time unknown',adm)
    watched=[ec/'registry.json',rq/'slots',rq/'queue',pr/'priority.json',rq/'features.json',storage/'storage.json']
    if host=='m6':watched.extend([route/'waiting.json',route/'decisions.jsonl'])
    titlemap=(section('Title catalog unavailable',lambda:get_titles(repo)) or {}) if host=='m6' else {}
    for attempt in range(2):
        before=stamp(watched);issues=len(out['issues'])
        def registry():
            r=read(ec/'registry.json')
            if r['version']!=1 or not isinstance(r['edits'],dict):raise ValueError()
            for j,e in r['edits'].items():
                if e['state'] not in STATES or key(j)!=key(e['job']):raise ValueError()
            return r['edits']
        reg=section('Edit register unavailable or unsupported',registry)
        rows=section('Render ownership unconfirmed',lambda:render_rows(rq,k))
        if host=='m6':
            def routeview():
                if route!=fallback and fallback.is_dir() and not os.getenv('EDITROUTE_DIR'):raise ValueError()
                return routes(route,float(cfg['reserve_min'])*60,now)
            out['route']=section('Shared waiting list or reservations unknown',routeview)
        if stamp(watched)==before:break
        if attempt==0:del out['issues'][issues:]
        else:out['issues'].append('Work changed during observation')
    jobs={}
    def job(j):
        return jobs.setdefault(j,dict(id=j,title='The Only 5 Machines You Need' if j=='DS-98' else titlemap.get(j,j),states=[],held=0,tickets=0,parked=False,urgent=False))
    for ident,e in (reg or {}).items():
        if e['state']=='finished':continue
        j=key(ident); a=job(j)
        if j not in ('DS-98','Unidentified project') and e.get('title'):a['title']=str(e['title'])[:110]
        a['states'].append(e['state']); a['parked']|=bool(e.get('reservation_parked')); a['urgent']|=bool(e.get('priority')) or j in urgent
    for j,held,cores,urgent in rows or []:
        a=job(j);a['held' if held else 'tickets']+=1;a['urgent']|=urgent
    unknown=jobs.get('Unidentified project')
    if unknown:
        if unknown['held'] or unknown['tickets'] or set(unknown['states'])&{'active','promoted'}:
            out['issues'].append('One project identity unconfirmed')
        else:out['note']='Unrecognized entry in the edit register; shown as recorded.'
    for a in jobs.values():
        s=set(a['states'])
        a['occupies']=a['id'] not in ('Unidentified project','Unassigned render work') and bool(s&{'active','promoted'} or a['held'] or (a['tickets'] and not (a['parked'] and s&{'parked','waiting'})))
    out['jobs']=list(jobs.values())
    if rows is not None:
        out.update(renders=sum(r[1] for r in rows),tickets=sum(not r[1] for r in rows),assigned=sum(r[2] for r in rows if r[1]))
    if reg is not None:
        out['registered']=sum(bool(set(a['states'])&{'active','promoted'}) for a in jobs.values() if a['id']!='Unidentified project')
    if reg is not None and rows is not None:
        out['used']=sum(a['occupies'] for a in jobs.values())
        out['lowerBound']='One project identity unconfirmed' in out['issues']
    return out


if __name__=='__main__':
    signal.alarm(5)
    try:
        data=observe(sys.argv[1]);u=resource.getrusage(resource.RUSAGE_SELF)
        data['cost']={'cpu':u.ru_utime+u.ru_stime,'rss':u.ru_maxrss}
        if (HERE/'measure').is_file():
            pid=os.getpid(); family=[]; k=kernel()
            for _ in range(5):
                if pid<=1:break
                a=(C.c_double*4)();old=pid;pid=k.cost(pid,a)
                if a[1]<=0: # privileged sshd: kernel footprint unavailable; ps provides RSS and CPU
                    try:
                        rss,spent=subprocess.check_output(['/bin/ps','-p',str(old),'-o','rss=,time='],timeout=1).decode().split()
                        mins,secs=spent.split(':');a[0]=60*int(mins)+float(secs);a[1]=1024*int(rss);a[2]=-1
                    except Exception:pass
                family.append(list(a))
            data['cost']['family']=family
        print(json.dumps(data,separators=(',',':')))
    except Exception:sys.exit(1)
