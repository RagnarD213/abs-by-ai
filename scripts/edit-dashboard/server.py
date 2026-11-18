"""Loopback launchd socket, one in-flight collection per host, no autonomous polling."""
import ctypes
import http.server
import json
import os
import resource
import signal
import socket
import subprocess
import threading
import time
from pathlib import Path
import observe
import desk_records

HERE=Path(__file__).resolve().parent
HOSTS=('m6','m2'); AUTO=58; MANUAL=12; STALE=120; IDLE=75
REMOTE='exec "$HOME/.local/share/abs-edit-dashboard/collect"'
SSH=['/usr/bin/ssh','-T','-oBatchMode=yes','-oConnectTimeout=3','-oConnectionAttempts=1','-oControlMaster=no','-oControlPath=none','-oStrictHostKeyChecking=yes','-oClearAllForwardings=yes','-oForwardAgent=no']
def remote(cmd=None,timeout=7):
    # Remote script has its own alarm; local deadline kills and reaps the SSH group.
    p=subprocess.Popen(cmd or SSH+['m2',REMOTE],stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,start_new_session=True)
    peak=[0,0];start=time.monotonic()
    if (HERE/'measure').is_file():
        k=observe.kernel()
        for _ in range(12):
            a=(ctypes.c_double*4)();k.cost(p.pid,a);peak=[max(peak[0],a[1]),max(peak[1],a[2])]
            if p.poll() is not None:break
            time.sleep(.006)
    try:b=p.communicate(timeout=max(.001,timeout-(time.monotonic()-start)))[0]
    except subprocess.TimeoutExpired:
        try:os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError:pass
        p.communicate();raise
    if p.returncode or len(b)>262144:raise ValueError()
    data=json.loads(b)
    if data['host']!='m2' or abs(time.time()-data['observed'])>30:raise ValueError()
    try:titles=observe.get_titles(Path.home()/'Projects/Claude/Projects/Abs By AI')
    except (OSError,ValueError,KeyError):titles={}
    for j in data['jobs']:
        if j['id']==j['title'] and j['id'] in titles:j['title']=titles[j['id']]
    if any(peak):data['cost']['sshClientPeak']=peak
    return data

def suggest(hosts,now):
    # An unrelated unassigned render can never free a recorded, occupied slot.
    # This negative decision needs no guess about the identity of that render.
    if all(not hosts[h].get('error') and hosts[h].get('age',9999)<=STALE and
           (hosts[h].get('data') or {}).get('registered',-1)>=(hosts[h].get('data') or {}).get('cap',999) and
           set((hosts[h].get('data') or {}).get('issues',[]))<={'One project identity unconfirmed'}
           for h in HOSTS):
        return ['wait','Queue additional edits','Both Macs have all their edit slots in use. Existing work gets the next opening.']
    for h in HOSTS:
        v=hosts[h]; d=v.get('data') or {}
        if v.get('error') or v.get('age',9999)>STALE or not d or d.get('issues'):
            why=(d.get('issues') or ['No complete current reading'])[0]
            return ['check','Check status before starting',h.upper()+': '+(v.get('error') or ('Last reading is stale' if v.get('age',0)>STALE else why))+'.']
    a,b=[hosts[h]['data'] for h in HOSTS];route=a['route']
    if hosts['m6'].get('sharedLine',route['line']):return ['wait','Queue additional edits','The shared waiting list already has work for the next opening.']
    reasons=[]
    for d in (b,a):
        h=d['host']; jobs=d['jobs']; existing={j['id'] for j in jobs if j['occupies']}
        extra=set(route['reserved'][h])-existing
        if d['used']+len(extra)>=d['cap']:reasons.append('its edit slots are occupied or reserved');continue
        if any(j.get('batchStage') or set(j['states'])&{'waiting','parked'} for j in jobs) or d['tickets'] or d['dedicated']:
            reasons.append('waiting or reserved work has the next turn');continue
        if d['pressure']!='normal' or d['loadGuard']:reasons.append('the Mac is under load');continue
        if d['internalRoom']<20:reasons.append('internal space for a new edit is unconfirmed');continue
        if not d['outside'] or not 0<=now-d['outside']['at']<=3:reasons.append('outside work has no recent reading');continue
        if d['outside']['count'] or (d['renders'] and (not d['gate'] or not 0<=now-d['gate']['at']<=15 or not d['gate']['ready'] or now-d['lastGrant']<15 or d['assigned']+2>d['budget'])):
            reasons.append('render work needs room to finish');continue
        return ['room','Room for one new edit on '+h.upper(),('A new exercise batch' if 'EXDEMO' in d.get('first',[]) else 'A new Short' if 'SFC' in d.get('first',[]) else 'A new edit')+' needing up to 20 GB is a candidate. Use normal routing to confirm ownership and space.']
    if all(d['used']>=d['cap'] for d in (a,b)):return ['wait','Queue additional edits','Both Macs have all their edit slots in use. Existing work gets the next opening.']
    return ['wait','Queue additional edits','M2: '+reasons[0]+'. M6: '+reasons[1]+'.']

ETA_FILE=Path.home()/'Projects/Claude/Projects/Abs By AI/tmp/edit-queue-export/edit-queue-eta.json'
def eta_file():
    # Finish-time ranges (Dan, 2026-11-18): written by .claude/skills/_shared/eta/eta.py refresh every 10 minutes.
    try:
        d=json.loads(ETA_FILE.read_text())
        return {'jobs':d.get('jobs',{}),'checked':d.get('checked',''),'generated':d.get('generated',0)}
    except (OSError,ValueError,AttributeError):return {'jobs':{},'checked':'','generated':0}

class Store:
    def __init__(self,cache,collect=None,clock=lambda:time.clock_gettime(time.CLOCK_MONOTONIC)):
        self.lock=threading.Lock();self.cache=cache;self.clock=clock;self.collect=collect or (lambda h: observe.observe(h) if h=='m6' else remote())
        self.items={h:{} for h in HOSTS};self.busy=set()
        try:
            s=json.loads(cache.read_text())
            if abs(s['boot']-(time.time()-clock()))<3:self.items.update({h:s['items'][h] for h in HOSTS})
        except (ValueError,KeyError,OSError,TypeError):pass
    def start(self,manual=False):
        with self.lock:
            for h in HOSTS:
                x=self.items[h];n=self.clock()
                if h in self.busy or max(n-x.get('attemptMono',-1e10),time.time()-x.get('attempt',0))<(MANUAL if manual else AUTO):continue
                self.busy.add(h);x.update(attemptMono=n,attempt=time.time(),attempts=x.get('attempts',0)+1)
                threading.Thread(target=self._work,args=(h,),daemon=True).start()
    def _work(self,h):
        try:
            data=self.collect(h);err=None
        except Exception:data=None;err='Mac did not return a usable reading'
        with self.lock:
            x=self.items[h]
            if data is not None:
                x.update(data=data,readMono=self.clock(),readAt=time.time())
                if not (set(data['issues'])-{'One project identity unconfirmed'}):x.update(lastSuccess=x['readAt'],lastGood=data)
            x['error']=err;self.busy.discard(h)
            if (HERE/'measure').is_file():
                cpu=resource.getrusage(resource.RUSAGE_SELF);kid=resource.getrusage(resource.RUSAGE_CHILDREN)
                x['meter']=[os.getpid(),cpu.ru_utime+cpu.ru_stime,kid.ru_utime+kid.ru_stime,cpu.ru_maxrss,kid.ru_maxrss]
            t=self.cache.with_suffix('.new')
            t.write_text(json.dumps(dict(boot=time.time()-self.clock(),items=self.items)))
            t.replace(self.cache)
    def view(self):
        with self.lock:
            hosts={h:dict(x,age=max(0,time.time()-x.get('readAt',time.time()),self.clock()-x['readMono']) if 'readMono' in x else None,busy=h in self.busy) for h,x in self.items.items()}
            for x in hosts.values():
                if x['age'] is None:x.pop('age')
                for k in ('lastGood','meter','readMono','attemptMono'):x.pop(k,None)
                if x.get('data'):x['data']={k:v for k,v in x['data'].items() if k!='cost'}
            hosts, requests, pending, shared, titles = desk_records.reconcile(hosts)
            hosts['m6']['sharedLine']=shared
            return dict(hosts=hosts,advice=suggest(hosts,time.time()),now=time.time(),
                        reviews=requests,unconfirmed=pending,shared=shared,titles=titles,eta=eta_file())

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*a):pass
    def setup(self): super().setup();self.connection.settimeout(1)
    def sendbody(self,body,typ,code=200):
        self.send_response(code);self.send_header('Content-Type',typ);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Referrer-Policy','no-referrer');self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'");self.end_headers()
        try:self.wfile.write(body)
        except OSError:pass
    def ok(self):return self.headers.get('Host')==f'127.0.0.1:{self.server.server_port}'
    def do_GET(self):
        if not self.ok():return self.sendbody(b'','text/plain',403)
        if self.path=='/state':return self.state()
        if self.path=='/batch-report':
            # The overnight batch's persistent morning report (2026-11-18): what the M6 notification points to.
            try:body=(Path.home()/'.absbyai-batch'/'morning-report.md').read_bytes()
            except OSError:body=b'No overnight batch report on this Mac yet.'
            return self.sendbody(body,'text/plain; charset=utf-8')
        if self.path in ('/','/app.js','/style.css'):
            f,t={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','application/javascript'),'/style.css':('style.css','text/css')}[self.path]
            return self.sendbody((HERE/f).read_bytes(),t)
        return self.sendbody(b'','text/plain',404)
    def do_POST(self):
        if not self.ok() or self.path not in ('/refresh','/manual') or self.headers.get('X-Edit-View')!='visible':return self.sendbody(b'','text/plain',403)
        self.server.store.start(self.path=='/manual');self.state()
    def state(self):self.sendbody(json.dumps(self.server.store.view()).encode(),'application/json')
def serve():
    lib=ctypes.CDLL(None);fds=ctypes.POINTER(ctypes.c_int)();count=ctypes.c_size_t()
    if lib.launch_activate_socket(b'Listeners',ctypes.byref(fds),ctypes.byref(count)) or count.value!=1:raise RuntimeError('No dashboard socket')
    sock=socket.socket(fileno=fds[0]);lib.free(fds);sock.setblocking(True)
    httpd=http.server.HTTPServer(sock.getsockname(),Handler,bind_and_activate=False);httpd.socket.close();httpd.socket=sock
    httpd.server_port=sock.getsockname()[1];httpd.store=Store(HERE/'cache.json');httpd.timeout=IDLE
    while True:
        start=time.monotonic();httpd.handle_request()
        if time.monotonic()-start>=IDLE and not httpd.store.busy:break
    httpd.server_close()
if __name__=='__main__':serve()
