#!/usr/bin/env python3
"""Explicit named rounds, pulled by each Mac from one locked M2 ledger. Disabled on install."""
import argparse
import base64
import contextlib
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import signal
import subprocess
import sys
import time
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eq_common as eq
eq.unshadow()
sys.path.insert(0, str(Path(eq.ROOT)/'.claude/skills/_shared/editroute'))
import hostcfg

HOME = Path(os.environ.get('EDIT_BATCH_HOME') or Path.home()/'.absbyai-batch')
SHARED = Path(eq.ROOT)/'.claude/skills/_shared'
# Only what the scheduler and its workers execute or read at run time (2026-11-18): the edit desk, tests,
# docs, fixtures and snapshots no longer stop starts, so another session's unsaved edits there are harmless.
SOURCE_ROOTS = ['.claude/skills/_shared/'+n for n in ('editroute','editcap','renderq')] + ['scripts/edit-queue']
RUNTIME_DOCS = {'scripts/edit-queue/preamble.md','scripts/edit-queue/reviewer-brief.md'}  # read into every session prompt
RUNTIME_SUFFIXES = ('.py','.json','.sh','.plist','.js','.c')
NON_RUNTIME_DIRS = {'tests','test','fixtures','testdata','__pycache__','approved-clips'}
TERMINAL = {'delivered','delivered-unreviewed','needs-dan','blocked','taken-over'}
AGENT_LABEL = 'com.absbyai.edit-queue'
PROBE_EVERY_S = 1800        # background file-access check: every 30 min, or at once on request
PROBE_MAX_AGE_S = 6*3600    # preflight refuses an older check
EDITOR_NAMES = {'claude':'Claude','codex':'Codex'}
NAME = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_-]{0,95}$')
JOB = re.compile(r'^(?:[A-Z]{2,8}|REALDEMOS)-[A-Z0-9-]+$')
class TransportError(RuntimeError):pass
class CoordinatorUnreachable(TransportError):
    """The M2 ledger could not be reached, as distinct from a fault on this Mac."""
class RejectedError(RuntimeError):pass

HEARTBEAT_S = 60
STALE_S = 600


def read(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except FileNotFoundError:
        return default


def write(path, doc):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    with tmp.open('w') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, path)
    fd = os.open(str(path.parent), os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)


def checked_name(name):
    if not NAME.fullmatch(name): raise ValueError('invalid batch name')
    return name


def here():
    h = hostcfg.this_host()
    if h not in ('m2','m6'): raise RuntimeError('unknown Mac')
    return h


def remote(host, args, payload=None, timeout=25):
    hc = hostcfg.host(host)
    command = 'cd '+shlex.quote(hc['repo'])+' && python3 -B scripts/edit-queue/batch.py '+shlex.join(args)
    run = subprocess.run(['ssh','-oBatchMode=yes','-oConnectTimeout=3',hc.get('ssh',host),command],
                         input=json.dumps(payload) if payload is not None else None,
                         capture_output=True, text=True, timeout=timeout)
    if run.returncode: raise (TransportError if run.returncode==255 else RejectedError)(host+': '+(run.stderr or run.stdout)[-1000:])
    try:return json.loads(run.stdout)
    except ValueError as exc:raise RejectedError('invalid coordinator response: '+str(exc))


def rpc(op, **values):
    request = dict(op=op, **values)
    if here()=='m2':return handle(request)
    try:return remote('m2',['_rpc'],request)
    except (TransportError,subprocess.TimeoutExpired,OSError) as exc:
        raise CoordinatorUnreachable(str(exc) or type(exc).__name__) from exc


@contextlib.contextmanager
def locked():
    HOME.mkdir(parents=True, exist_ok=True)
    with (HOME/'ledger.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def batches():
    return sorted(p.parent for p in HOME.glob('*/manifest.json'))


def control():
    return read(HOME/'control.json', {'enabled':False})


def key(job): return job['id']+'-R'+str(job['round'])


def load_batch(name):
    p = HOME/checked_name(name)
    return p, read(p/'manifest.json'), read(p/'state.json')


def snapshot():
    result = dict(control=control(), batches={})
    for p in batches():
        manifest=read(p/'manifest.json'); state=read(p/'state.json')
        if not manifest or not state: raise RuntimeError('incomplete ledger: '+p.name)
        result['batches'][p.name] = dict(manifest=manifest, **state)
    return result


def editor_name(row):
    return EDITOR_NAMES.get((row or {}).get('executor'),'Claude')


def takeover_action(row, what='finish it'):
    """A next action a non-coder can follow: who opens which chat, and what the chat does. Names the exact round."""
    job=(row or {}).get('id','this video');title=(row or {}).get('title') or job;rnd=(row or {}).get('round')
    cmd='batch.py takeover '+job+(' --round '+str(rnd) if rnd else '')
    return ('Open a new '+editor_name(row)+' chat for '+title+' ('+job+(' R'+str(rnd) if rnd else '')+'), have it take over the saved work '
            '('+cmd+') and '+what+'. Nothing is lost; the work folder is kept.')


def finish(row, outcome):
    status=outcome.get('status')
    if status not in TERMINAL: raise ValueError('invalid terminal outcome')
    if status in ('blocked','delivered-unreviewed') and not outcome.get('reason'):
        raise ValueError('outcome needs reason')
    if status=='blocked' and not outcome.get('next_action'): raise ValueError('blocked needs next action')
    if status=='needs-dan' and not (outcome.get('question') and outcome.get('link')):
        raise ValueError('needs Dan requires a question and review link')
    if status=='blocked' and not outcome.get('owner'):
        # Every blocked row names who acts next (2026-11-18); the editor that owns the video by default.
        outcome=dict(outcome,owner=editor_name(row))
    row.update(status=status, outcome=outcome, ended=time.time())
    row.pop('claim',None)


def handle(req):
    """The only ledger writer. Every mutation, including stop/claim, uses this single flock."""
    with locked():
        op=req['op']; now=time.time()
        if op=='snapshot': return snapshot()
        if op=='stop':
            for p in batches():
                state=read(p/'state.json');state['enabled']=False;write(p/'state.json',state)
            c=control(); c.update(enabled=False,stopped=now);write(HOME/'control.json',c);return c
        if op=='preflight':
            c=control();c['preflight']=req['proof'];write(HOME/'control.json',c);return c
        if op=='enqueue':
            name=checked_name(req['batch']);p=HOME/name
            if (p/'manifest.json').exists():
                old=read(p/'manifest.json')
                if old['jobs']!=req['jobs']:raise ValueError('batch name already used with different jobs')
                return dict(registered=True,batch=name,duplicate=True)
            all_rows=[r for d in snapshot()['batches'].values() for r in d['jobs'].values()]
            for job in req['jobs']:
                reason=eq.paused_reason(job['id'],job['executor'],eq.load_config())
                if reason:raise ValueError(reason)
                for prior in all_rows:
                    if prior['id']==job['id'] and (prior['status'] not in TERMINAL or prior['round']==job['round']):
                        raise ValueError(job['id']+' has a nonterminal round; finish or take it over first')
                for sibling in req['jobs']:
                    if sibling is not job and sibling['id']==job['id']:
                        raise ValueError('only one round of a job per batch')
            p.mkdir(parents=True,exist_ok=True); rows={}
            for job in req['jobs']:
                data=base64.b64decode(req['briefs'][key(job)],validate=True)
                dest=p/'briefs'/(key(job)+'.md');dest.parent.mkdir(exist_ok=True)
                with dest.open('wb') as f:f.write(data);f.flush();os.fsync(f.fileno())
                if hashlib.sha256(dest.read_bytes()).hexdigest()!=job['brief_sha256']:
                    raise ValueError('brief readback failed')
                rows[key(job)]=dict(job,status='queued',queued_at=now,attempts=0,resumes=0,allowance_tries=0,not_before=0)
            c=control();chat_enabled=name.startswith('chat-') and c.get('enabled') and c.get('preflight',{}).get('passed') and req.get('digest')==c.get('preflight',{}).get('digest')
            write(p/'state.json',dict(enabled=bool(chat_enabled),jobs=rows,ticks={}))
            write(p/'manifest.json',dict(schema=1,batch=name,created=now,jobs=req['jobs']))
            return dict(registered=True,batch=name)
        if op=='tick':
            for p in batches():
                state=read(p/'state.json')
                last=state['ticks'].get(req['host'],now)
                elapsed=min(180,max(0,now-last))/60
                capacity=req.get('observation',{}).get('_capacity',{})
                for row in state['jobs'].values():
                    if control().get('enabled') and state['enabled'] and row['status']=='queued' and row['placement'] in ('any',req['host']) and row['not_before']<=now and capacity.get('free',0)>0:
                        row['idle_slot_minutes']=row.get('idle_slot_minutes',0)+elapsed
                state['ticks'][req['host']]=now
                state.setdefault('observations',{})[req['host']]=req.get('observation',{})
                write(p/'state.json',state)
            return snapshot()
        if op=='start':
            p,manifest,state=load_batch(req['batch'])
            if not state:raise ValueError('unknown batch')
            proof=control().get('preflight',{})
            if not proof.get('passed') or proof.get('digest')!=req['digest']:
                raise ValueError('run preflight successfully before enabling')
            state['enabled']=True;write(p/'state.json',state)
            c=control();c.update(enabled=True,started=now);write(HOME/'control.json',c);return state
        if op=='claim':
            c=control()
            if not c.get('enabled') or not c.get('preflight',{}).get('passed') or req['digest']!=c.get('preflight',{}).get('digest'):return None
            live=[]
            for d in snapshot()['batches'].values():
                live.extend(r for r in d['jobs'].values() if r['status']=='claimed' and r['claim']['owner']==req['host'])
            unregistered=sum(r['id'] not in req['occupied'] and r['claim'].get('phase')!='outcome waiting for review mirror' for r in live)
            if c.get('host_backoff',{}).get(req['host'],{}).get('until',0)>now:return None
            full=len(req['occupied'])+unregistered>=req['slots']
            choices=[]
            for p in batches():
                state=read(p/'state.json')
                if not state['enabled']:continue
                for k,r in state['jobs'].items():
                    if r['status']=='queued' and r['not_before']<=now and r['placement'] in ('any',req['host']) and not r.get('held'):
                        if eq.paused_reason(r['id'],r['executor'],eq.load_config()):continue
                        if r['id'] in req.get('unavailable',[]):continue
                        if r.get('host_defer',{}).get(req['host'],0)>now:continue
                        next_executor=r.get('next_executor',r['executor'])
                        if c.get('executor_backoff',{}).get(next_executor,{}).get('until',0)>now:continue
                        choices.append(({'L':0,'M':1,'S':2}[r['size']],r['order'],r['queued_at'],p,k,r))
            if full:choices=[entry for entry in choices if entry[-1]['id'] in req['occupied']]
            if not choices:return None
            _,_,_,p,k,row=min(choices,key=lambda x:x[:3])
            state=read(p/'state.json');row=state['jobs'][k]
            brief=(p/'briefs'/(k+'.md')).read_bytes()
            if hashlib.sha256(brief).hexdigest()!=row['brief_sha256']:raise ValueError('stored brief changed')
            row.update(status='claimed',attempts=row['attempts']+1)
            row['claim']=dict(token=uuid.uuid4().hex,owner=req['host'],at=now,heartbeat=now,pid=None,birth=None,phase='starting')
            row['first_started']=row.get('first_started',now)
            write(p/'state.json',state)
            brief=(p/'briefs'/(k+'.md')).read_bytes()
            if hashlib.sha256(brief).hexdigest()!=row['brief_sha256']:raise ValueError('stored brief changed')
            return dict(batch=p.name,key=k,row=row,brief=base64.b64encode(brief).decode())
        if op in ('hold','unhold'):
            # Dan's explicit pause of one queued round: it keeps its registration and never starts until released.
            p,manifest,state=load_batch(req['batch']);row=state['jobs'][req['key']]
            if row['status']!='queued':raise ValueError('only a queued round can be held or released')
            if op=='hold':
                if not req.get('reason'):raise ValueError('a hold needs the reason')
                row['held']=dict(at=now,by=req.get('by','Dan'),reason=req['reason'])
            else:row.pop('held',None)
            write(p/'state.json',state);return row
        if op=='reclassify':
            # One-time correction of a blocked row whose real state is a decision for Dan (2026-11-18 rules).
            p,manifest,state=load_batch(req['batch']);row=state['jobs'][req['key']]
            if row['status']!='blocked':raise ValueError('only a blocked row can be reclassified')
            new=dict(req['outcome'],reclassified=dict(at=now,why=req.get('why','')))
            if new.get('status') not in ('needs-dan','blocked'):raise ValueError('reclassify to needs-dan or blocked only')
            prior=dict(row['outcome']);ended=row.get('ended')
            finish(row,new);row['prior_outcome']=prior;row['blocked_at']=ended
            write(p/'state.json',state);return row
        if op=='takeover':
            found=[]
            for p in batches():
                state=read(p/'state.json')
                for k,r in state['jobs'].items():
                    if r['id']==req['job'] and r['status']!='taken-over' and (req.get('round') is None or r['round']==int(req['round'])):
                        found.append((p,k,r))
            if not found:raise ValueError('no batch job found')
            p,k,row=max(found,key=lambda x:x[2]['queued_at'])
            if row['status']=='claimed':raise ValueError('live or unconfirmed claim; takeover refused until owner confirms exit')
            state=read(p/'state.json');row=state['jobs'][k]
            result=dict(row)
            if row.get('outcome'):row['prior_outcome']=dict(row['outcome'])
            finish(row,dict(status='taken-over',reason='explicit chat takeover',by=req['host']))
            write(p/'state.json',state);return result
        p,manifest,state=load_batch(req['batch'])
        row=state['jobs'][req['key']]
        claim=row.get('claim',{})
        if row['status']!='claimed' or claim.get('token')!=req['token']:
            # Idempotent replay from an offline owner's durable outbox.
            if op=='outcome' and row.get('outcome_token')==req['token']:return row
            raise ValueError('stale claim token')
        if req.get('host') and claim['owner']!=req['host']:raise ValueError('owner mismatch')
        if op=='heartbeat':
            claim.update(req.get('fields',{}));claim['heartbeat']=now
        elif op=='outcome':
            row['outcome_token']=req['token']; row.setdefault('timing',{})
            for field,value in req.get('timing',{}).items():row['timing'][field]=row['timing'].get(field,0)+value
            outcome=req['outcome']
            if outcome['status']=='deferred-start':
                resource_wait=outcome.get('retry_kind') in ('capacity','storage')
                row['start_waits']=row.get('start_waits',0)+int(resource_wait)
                row['start_failures']=row.get('start_failures',0)+int(not resource_wait)
                delay=req.get('backoff_s',120)
                c=control()
                if outcome.get('retry_kind')=='storage':row.setdefault('host_defer',{})[claim['owner']]=now+max(600,delay)
                else:
                    c.setdefault('host_backoff',{})[claim['owner']]=dict(until=now+delay,reason=outcome['reason']);write(HOME/'control.json',c)
                if resource_wait or row['start_failures']<3:
                    row.update(status='queued',not_before=now+delay,last_start_error=outcome['reason'])
                    if claim.get('workdir'):row.update(placement=claim['owner'],workdir=claim['workdir'])
                    row.pop('claim',None)
                else:finish(row,dict(status='blocked',reason='start failed three times: '+outcome['reason'],owner=editor_name(row),
                                     next_action=takeover_action(row,'fix the start problem named here, then start the edit in that chat')))
            elif outcome['status']=='paused-for-allowance':
                attempted=outcome.get('attempted',True)
                row['allowance_tries']+=int(attempted)
                next_executor=outcome.get('executor',row['executor']);row['next_executor']=next_executor
                c=control();prior=c.get('executor_backoff',{}).get(next_executor,{})
                until=(now+req.get('backoff_s',7200)*(2**max(0,row['allowance_tries']-1))) if attempted else max(now,prior.get('until',now))
                delay=until-now
                if attempted:
                    c.setdefault('executor_backoff',{})[next_executor]=dict(until=until,reason=outcome['reason']);write(HOME/'control.json',c)
                if row['allowance_tries']<3:
                    row.update(status='queued',not_before=now+delay,last_pause=now,
                               placement=claim['owner'],workdir=claim.get('workdir'),resume_phase=claim.get('phase'))
                    row.setdefault('allowance_pauses',[]).append(dict(at=now,until=row['not_before']))
                    row.pop('claim',None)
                else:finish(row,dict(status='blocked',reason='allowance exhausted after three attempts',owner='Dan',
                                     next_action='The '+editor_name(dict(executor=next_executor))+' allowance ran out three times. When it is back, tell any chat to resume this edit; the saved work continues.'))
            else:finish(row,outcome)
        elif op=='recover':
            if req['pid_alive'] or req.get('session_alive'):return row
            if now-claim['heartbeat']<STALE_S and not req.get('spawn_failed'):return row
            if row['resumes']<1:
                row.update(status='queued',resumes=row['resumes']+1,placement=claim['owner'],
                           workdir=claim.get('workdir'),not_before=now,resume_phase=claim.get('phase'))
                row.pop('claim',None)
            else:finish(row,dict(status='blocked',reason='runner exited without an outcome after one recovery',owner=editor_name(row),
                                 next_action=takeover_action(row,'finish the edit from where it stopped')))
        else:raise ValueError('unknown operation '+op)
        write(p/'state.json',state);return row


def scheduler_file(name):
    """True for a tracked file the scheduler or a worker runs or reads; tests, docs and snapshots are not."""
    if name in RUNTIME_DOCS:return True
    parts=name.split('/');base=parts[-1]
    if NON_RUNTIME_DIRS.intersection(parts[:-1]):return False
    if not base.endswith(RUNTIME_SUFFIXES):return False
    stem=base.rsplit('.',1)[0]
    if base in ('scoreboard.json','review-snapshot.html') or 'snapshot' in stem:return False
    if stem.startswith(('test_','selftest')) or stem.endswith('_test') or 'bench' in stem:return False
    return True


def fingerprints(fresh_probe=False):
    """Bind installed source bytes to pushed Git objects, not the shared checkout's dirty HEAD."""
    files=subprocess.check_output(['git','ls-tree','-rz','origin/main','--',*SOURCE_ROOTS],cwd=eq.ROOT)
    hashes={};dirty=[]
    for record in files.split(b'\0'):
        if not record:continue
        meta,name=record.split(b'\t',1);mode,typ,blob=meta.decode().split();name=name.decode()
        p=Path(eq.ROOT)/name
        if not scheduler_file(name):continue
        if not p.exists():dirty.append(name+': missing');continue
        data=os.readlink(p).encode() if mode=='120000' and p.is_symlink() else p.read_bytes()
        gitsha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if gitsha!=blob:dirty.append(name)
        hashes[name]=hashlib.sha256(data).hexdigest()
    canary=read(HOME/'canary-latest.json',{})
    digest=hashlib.sha256(json.dumps(hashes,sort_keys=True).encode()).hexdigest()
    launcher_ok=(canary.get('launcher_sha256')==hashlib.sha256(Path(eq.__file__).read_bytes()).hexdigest() and canary.get('executors_sha256')==hashlib.sha256(json.dumps(eq.load_config()['executors'],sort_keys=True).encode()).hexdigest())
    request_id=request_launchd_probe() if fresh_probe else None
    return dict(host=here(),launcher_ok=launcher_ok,hashes=hashes,digest=digest,dirty=dirty,canary=canary,
                drive_probe=launchd_probe_status(request_id=request_id),
                commit=subprocess.check_output(['git','rev-parse','origin/main'],cwd=eq.ROOT,text=True).strip())


# ---- Background file access (2026-11-18). The launchd Python, not a chat's shell, must be able to use the
# drives: on Nov 17-18 it could not write the M2 work drive or the M6's Videos to Review folder.
PROBE_DIR = '.absbyai-batch-probe'   # + '-<host>': one private folder per Mac per checked folder, never a link
PROBE_FILES = ('probe.txt','probe-renamed.txt')   # the only names cleanup ever removes
# Required on every Mac: the delivery folder, the internal work folder and the Extreme work folder (the handoff's
# explicit proof). Expansion is checked and reported when mounted but never blocks: finals reach it through
# Videos to Review, which is checked on its own.
REQUIRED_PROBE_LABELS = ('Videos to Review','internal work folder','Extreme work folder')
PROBE_TIMEOUT_S = 60


def volume_root(path):
    """'/Volumes/X' for a path on an external or network volume, else None (the internal disk)."""
    parts=Path(path).parts
    return str(Path(*parts[:3])) if len(parts)>=3 and parts[1]=='Volumes' else None


def probe_folders():
    """(label, folder, required, create_root). Mirrors renderq: internal work first, then mounted drives."""
    override=os.environ.get('EDIT_BATCH_PROBE_FOLDERS')
    if override:
        return [(f['label'],Path(f['path']),bool(f.get('required',True)),bool(f.get('create',False))) for f in json.loads(override)]
    internal=Path(os.environ.get('GATE_INTERNAL_WORK') or Path.home()/'Projects/_edit_work')
    return [('Videos to Review',Path(eq.ROOT)/'Videos to Review',True,False),('internal work folder',internal,True,True),
            ('Extreme work folder',Path('/Volumes/Extreme/_edit_work'),True,True),
            ('Expansion work folder',Path('/Volumes/Expansion/_edit_work'),False,True)]


def drive_probe(folders=None, host=None):
    """Create, write, rename and delete inside each folder exactly as a worker would. Runs only inside the
    deadline-bounded child (run_probe_with_deadline); nothing outside it touches the drives."""
    results=[];box_name=PROBE_DIR+'-'+(host or here())
    for label,folder,required,create_root in (probe_folders() if folders is None else folders):
        r=dict(label=label,path=str(folder),required=required,steps=[])
        try:
            real=Path(os.path.realpath(folder));r['resolved']=str(real)
            vol=volume_root(real)
            if vol and not os.path.ismount(vol):
                # A leftover folder at an unmounted /Volumes path is the internal disk, never the drive.
                r.update(passed=False,skipped=True,mounted=False,error='drive not mounted ('+vol+')');results.append(r);continue
            r['mounted']=True
            if vol:
                st=os.stat(vol);r['volume']=dict(dev=st.st_dev,ino=st.st_ino)
            if not real.is_dir() and create_root:real.mkdir(parents=True,exist_ok=True)
            if not real.is_dir():
                r.update(passed=False,error='folder missing');results.append(r);continue
            box=real/box_name
            if box.is_symlink():raise RuntimeError('probe folder '+box_name+' is a link; refusing to use it')
            leftovers=[str(box/n) for n in PROBE_FILES if (box/n).exists()] if box.is_dir() else []
            for x in leftovers:Path(x).unlink()
            if leftovers:r['cleared_leftovers']=leftovers
            box.mkdir(exist_ok=True);r['steps'].append('create')
            f=box/PROBE_FILES[0]
            with f.open('w') as h:h.write('absbyai batch probe\n');h.flush();os.fsync(h.fileno())
            r['steps'].append('write')
            moved=box/PROBE_FILES[1];os.replace(f,moved);r['steps'].append('rename')
            ok=moved.read_text()=='absbyai batch probe\n'
            moved.unlink();box.rmdir();r['steps'].append('delete')
            r['passed']=ok
            if not ok:r['error']='read back differs'
        except Exception as exc:
            # Stable text: the folder is named by its label, never a probe file name.
            r.update(passed=False,error=type(exc).__name__+': '+(getattr(exc,'strerror',None) or str(exc)))
            box=Path(r.get('resolved',folder))/box_name
            try:r['leftovers']=[str(box/n) for n in PROBE_FILES if (box/n).exists()]
            except OSError:r['leftovers']=['unreadable: '+str(box)]
        results.append(r)
    return results


def launchd_context():
    return os.environ.get('XPC_SERVICE_NAME')==AGENT_LABEL


def process_executable(pid=None):
    try:
        out=subprocess.run(['/bin/ps','-p',str(pid or os.getpid()),'-o','comm='],capture_output=True,text=True,timeout=5)
        return out.stdout.strip() or None
    except (OSError,subprocess.SubprocessError):return None


def run_probe_with_deadline():
    """The probe runs in a child of this same interpreter (same launchd responsibility), with a deadline,
    so a hung share can never stall the tick."""
    proc=subprocess.Popen([sys.executable,'-B',str(Path(__file__).resolve()),'_probe-worker',here()],stdin=subprocess.DEVNULL,
                          stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
    try:
        out,err=proc.communicate(timeout=PROBE_TIMEOUT_S)
        return json.loads(out),None
    except subprocess.TimeoutExpired:
        proc.kill()
        try:proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:pass
        return None,'file-access check timed out after '+str(PROBE_TIMEOUT_S)+' s (a drive or share is hung)'
    except ValueError:
        return None,'file-access check crashed: '+(err or '')[-300:]


def record_probe(context=None, request=None, deadline=True):
    context=context or ('launchd' if launchd_context() else 'interactive')
    if deadline:folders,error=run_probe_with_deadline()
    else:folders,error=drive_probe(),None
    if error:folders=[dict(label='all folders',passed=False,required=True,error=error)]
    previous=read(HOME/('drive-probe-'+context+'.json'),{})
    required=[f for f in folders if f.get('label') in REQUIRED_PROBE_LABELS or f.get('required')]
    doc=dict(at=time.time(),host=here(),context=context,interpreter=sys.executable,
             real_interpreter=os.path.realpath(sys.executable),process=process_executable(),pid=os.getpid(),
             # The last answered request survives timed checks, so an answered request is never re-run.
             request=(request or {}).get('id') or previous.get('request'),answered_now=bool(request),
             passed=bool(required) and all(f['passed'] for f in required),folders=folders)
    write(HOME/('drive-probe-'+context+'.json'),doc)
    return doc


def maybe_probe():
    """Run from the launchd tick: a fresh check on request, every 30 minutes, or 5 minutes after a failure."""
    if not launchd_context():return None
    last=read(HOME/'drive-probe-launchd.json',{});request=read(HOME/'drive-probe-request.json',{})
    age=time.time()-last.get('at',0)
    pending=request.get('id') and request.get('id')!=last.get('request')
    if pending or age>PROBE_EVERY_S or (not last.get('passed') and age>300):
        return record_probe('launchd',request if pending else None)
    return None


def launchd_probe_status(now=None, request_id=None):
    """OK only for a fresh launchd record (answering the request, when given) in which every required folder was
    really created, written, renamed and deleted on a mounted volume. Reads the saved record only: no drive or
    share is touched here, so a hung mount cannot stall a tick."""
    now=now or time.time();doc=read(HOME/'drive-probe-launchd.json',{})
    if not doc:return dict(ok=False,problem='no background file-access check has run yet on this Mac')
    seen={f.get('label'):f for f in doc.get('folders',[])};problems=[]
    if 'all folders' in seen:problems.append('all folders ('+seen['all folders'].get('error','failed')+')')
    labels=list(REQUIRED_PROBE_LABELS) if not os.environ.get('EDIT_BATCH_PROBE_FOLDERS') else [
        f['label'] for f in json.loads(os.environ['EDIT_BATCH_PROBE_FOLDERS']) if f.get('required',True)]
    for label in labels:
        f=seen.get(label)
        if 'all folders' in seen:break
        if not f:problems.append(label+' (not checked by the background agent)')
        elif not f.get('passed'):problems.append(label+' ('+f.get('error','failed')+')')
        elif f.get('steps')!=['create','write','rename','delete'] or not f.get('resolved') or f.get('mounted') is False:
            problems.append(label+' (not fully tested)')
    if problems:problem='the background agent cannot use: '+'; '.join(problems)
    elif request_id and doc.get('request')!=request_id:problem='the background agent did not answer a fresh file-access check'
    elif now-doc.get('at',0)>PROBE_MAX_AGE_S:problem='the background file-access check is older than six hours'
    else:problem=None
    return dict(ok=not problem,problem=problem,at=doc.get('at'),interpreter=doc.get('interpreter'),
                real_interpreter=doc.get('real_interpreter'),process=doc.get('process'))


def request_launchd_probe(wait_s=75):
    """Ask this Mac's own launchd agent for a fresh check, then wait for its answer. Returns the request id."""
    request=dict(id=uuid.uuid4().hex,at=time.time());write(HOME/'drive-probe-request.json',request)
    kick()
    deadline=request['at']+wait_s
    while time.time()<deadline:
        if read(HOME/'drive-probe-launchd.json',{}).get('request')==request['id']:break
        time.sleep(2)
    return request['id']


def preflight():
    local=fingerprints(fresh_probe=True);other='m2' if here()=='m6' else 'm6'
    remote_fp=remote(other,['fingerprints','--fresh-probe'],timeout=150)
    problems=[]
    for fp in (local,remote_fp):
        if fp['dirty']:problems.append(fp['host']+' source differs from pushed main: '+', '.join(fp['dirty']))
        probe=fp.get('drive_probe') or {}
        if not probe.get('ok'):problems.append(fp['host']+' '+(probe.get('problem') or 'background file-access check missing'))
        if not fp['launcher_ok'] or not fp['canary'].get('passed') or len(fp['canary'].get('rows',[]))!=4:problems.append(fp['host']+' real-session canary incomplete')
    if local['hashes']!=remote_fp['hashes']:problems.append('scheduler hashes differ between Macs')
    proof=dict(passed=not problems,at=time.time(),digest=local['digest'],problems=problems,
               hosts={f['host']:dict(commit=f['commit'],canary=f['canary'].get('id'),drive_probe=f.get('drive_probe')) for f in (local,remote_fp)})
    rpc('preflight',proof=proof);return proof


def identity(pid):
    if not pid:return None
    try:
        os.kill(int(pid),0)
        p=subprocess.run(['/bin/ps','-p',str(int(pid)),'-o','lstart='],capture_output=True,text=True,timeout=3)
        return p.stdout.strip() if p.returncode==0 else None
    except (OSError,ValueError,subprocess.SubprocessError):return None


def alive(pid,birth):return bool(birth and identity(pid)==birth)


def kick(other=False):
    label='gui/'+str(os.getuid())+'/com.absbyai.edit-queue'
    try:subprocess.run(['launchctl','kickstart',label],capture_output=True,timeout=5)
    except Exception:pass
    if other:
        target='m2' if here()=='m6' else 'm6'
        try:
            subprocess.run(['ssh','-oBatchMode=yes','-oConnectTimeout=3',target,
                            'launchctl kickstart gui/$(id -u)/com.absbyai.edit-queue'],capture_output=True,timeout=8)
        except subprocess.SubprocessError:pass


def save_snapshot(snap):
    write(HOME/'snapshot.json',snap)
    registrations={}
    ordered=sorted(((n,k,r) for n,d in snap['batches'].items() for k,r in d['jobs'].items()),key=lambda x:x[2]['queued_at'])
    for n,k,r in ordered:
        if r['status']=='taken-over':registrations.pop(r['id'],None)
        else:registrations[r['id']]=dict(batch=n,key=k,status=r['status'],token=(r.get('claim') or {}).get('token'))
    write(HOME/'registrations.json',registrations)


def guard(job):
    row=read(HOME/'registrations.json',{}).get(job)
    if row and row['status']=='claimed' and row.get('token')==os.environ.get('EDIT_BATCH_TOKEN'):return None
    return row


def normalize_outcome(outcome):
    outcome=dict(outcome)
    if outcome.get('status') in ('deferred-start','paused-for-allowance') and outcome.get('reason'):return outcome
    try:finish({},outcome)
    except Exception as exc:
        return dict(status='blocked',reason='invalid worker outcome: '+(str(exc) or type(exc).__name__),next_action='Inspect the saved outcome and retained work')
    return outcome


def flush_outbox():
    for p in sorted((HOME/'outbox').glob('*.json')):
        request={};error=None
        try:
            request=read(p)
            request['outcome']=normalize_outcome(request['outcome'])
            pending=request['outcome'].get('pending_review')
            if pending:
                request['outcome']['link']=eq.sibling('batch_runner').review_link(pending)
                request['outcome'].pop('pending_review',None)
            rpc(**{k:v for k,v in request.items() if not k.startswith('_')});p.unlink()
        except (TransportError,subprocess.TimeoutExpired,ConnectionError) as exc:
            error=str(exc) or type(exc).__name__
        except Exception as exc:
            error=str(exc) or type(exc).__name__
            if not request.get('token'):
                write(HOME/'outbox-quarantine'/p.name,dict(error=error,raw=p.read_text(errors='replace')))
                p.unlink();continue
            request['_failures']=request.get('_failures',0)+1
            if request['_failures']>=3:
                quarantine=HOME/'outbox-quarantine'/p.name
                write(quarantine,dict(request,error=error))
                request['outcome']=dict(status='blocked',reason='outcome synchronization rejected: '+error,next_action='Inspect quarantined outcome; retained media and work are unchanged')
                try:rpc(**{k:v for k,v in request.items() if not k.startswith('_')});p.unlink();continue
                except Exception:pass
        if error:
            request['_error']=error;write(p,request)


def update(op, batch, k, token, **kwargs):
    if op=='outcome':kwargs['outcome']=normalize_outcome(kwargs['outcome'])
    request=dict(op=op,batch=batch,key=k,token=token,host=here(),**kwargs)
    try:return rpc(**request)
    except Exception:
        # Heartbeats do not queue: after reconnect the live process sends a fresh one.
        if op=='outcome':write(HOME/'outbox'/(token+'.json'),request)
        return None


def observe_local():
    reg=read(Path('/tmp/absbyai-editcap')/'registry.json',{})
    result={j:dict(state=e.get('state'),since=e.get('since')) for j,e in reg.get('edits',{}).items()}
    cap=subprocess.run([sys.executable,str(SHARED/'editcap/editcap.py'),'status','--json'],capture_output=True,text=True,timeout=30)
    if cap.returncode==0:
        ec=json.loads(cap.stdout);result['_capacity']=dict(free=max(0,ec['cap']-len(ec['in_use'])))
    return result


def reconcile(snap):
    for n,d in snap['batches'].items():
        for k,row in d['jobs'].items():
            if row['status']!='claimed':continue
            c=row['claim']
            if c['owner']!=here():continue
            if (HOME/'outbox'/(c['token']+'.json')).exists():continue
            local=read(HOME/'runs'/c['token']/'progress.json',{})
            if local.get('pid') and (not c.get('pid') or local['pid']==c['pid']):
                c=dict(c, **local)
            if alive(c.get('pid'),c.get('birth')):
                progress_path=HOME/'runs'/c['token']/'progress.json'
                fresh=progress_path.exists() and time.time()-progress_path.stat().st_mtime<STALE_S
                if fresh:continue
                if time.time()-c['heartbeat']<STALE_S:continue
                stopfile=HOME/'runs'/c['token']/'runner-stop.json';prior=read(stopfile,{})
                os.kill(c['pid'],signal.SIGKILL if prior.get('at') and time.time()-prior['at']>30 else signal.SIGTERM)
                if not prior:write(stopfile,dict(at=time.time()))
                continue
            if time.time()-c['heartbeat']<STALE_S:continue
            session=c.get('session',{})
            live=alive(session.get('pid'),session.get('birth'))
            if live:
                # Only the recorded orphan's exact process group, never another editor's processes.
                stopfile=HOME/'runs'/c['token']/'orphan-stop.json'
                previous=read(stopfile,{})
                force=previous.get('at') and time.time()-previous['at']>30
                try:os.killpg(session['pid'],signal.SIGKILL if force else signal.SIGTERM)
                except ProcessLookupError:pass
                if not previous:write(stopfile,dict(at=time.time(),pid=session['pid'],birth=session['birth']))
                # A following tick confirms that group exited before any recovery claim.
                continue
            # A detached heavy step in renderq must finish before another editor resumes its folder.
            capacity=subprocess.run([sys.executable,str(SHARED/'editcap/editcap.py'),'status','--json'],capture_output=True,text=True,timeout=30)
            if capacity.returncode:continue
            if json.loads(capacity.stdout).get('renderq',{}).get(row['id'],{}).get('live',0):continue
            result=rpc('recover',batch=n,key=k,token=c['token'],host=here(),pid_alive=False,session_alive=False)
            if result['status'] in TERMINAL:
                subprocess.run([sys.executable,str(SHARED/'editcap/editcap.py'),'release',row['id']],capture_output=True,timeout=30)


def when(t):
    return time.strftime('%b %-d %-I:%M %p',time.localtime(t)) if t else 'an unknown time'


GATE_STALE_S = 600
ROLLOUT_AT = 1795042800   # Nov 18 2026 5:00 p.m. Central: rows that ended before this were reported before alerts existed


def row_label(r):
    return (r.get('title') or r['id'])+' ('+r['id']+' R'+str(r['round'])+')'


def host_gates(snap, local=None, now=None):
    """Each Mac's own start gate as it last reported it to the coordinator. A Mac silent for ten minutes
    is not claiming anything, so it counts as gated too. `local` = (host, reason) overrides with this
    Mac's fresher reading."""
    now=now or time.time();latest={}
    for d in snap.get('batches',{}).values():
        for host,obs in (d.get('observations') or {}).items():
            gate=(obs or {}).get('_start_block')
            if isinstance(gate,dict) and gate.get('at',0)>latest.get(host,{}).get('at',0):latest[host]=gate
    gates={}
    for host in ('m2','m6'):
        g=latest.get(host)
        if not g:gates[host]='the '+host.upper()+' has not reported its start check yet'
        elif now-g['at']>GATE_STALE_S:gates[host]='the '+host.upper()+' has not reported for '+str(int((now-g['at'])//60))+' minutes'
        else:gates[host]=g.get('reason')
    if local:gates[local[0]]=local[1]
    return gates


def start_blockers(snap, start_block=None, batch=None, error=None, local=None):
    """Why queued rounds will not start, in plain words, per round and per Mac. Empty reasons means they can start."""
    c=snap.get('control',{}) or {};pre=c.get('preflight') or {}
    rows=[(n,k,r) for n,d in snap.get('batches',{}).items() for k,r in d.get('jobs',{}).items()
          if r.get('status')=='queued' and not r.get('held') and (batch is None or n==batch)]
    held=[(n,k,r) for n,d in snap.get('batches',{}).items() for k,r in d.get('jobs',{}).items()
          if r.get('status')=='queued' and r.get('held') and (batch is None or n==batch)]
    reasons=[];kinds=[];global_block=False
    if error:
        global_block=True;kinds.append('coordinator-unreachable')
        reasons.append('this Mac could not finish its check with the M2 ledger ('+str(error)[:160]+'), so what is shown may be out of date')
    if not c.get('enabled'):
        global_block=True;kinds.append('starts-off')
        reasons.append('new starts are switched off'+(' since '+when(c['stopped']) if c.get('stopped') else '')+
                       ' (a chat runs batch.py start NAME to switch them on)')
    if not pre:
        global_block=True;kinds.append('no-preflight');reasons.append('no safety check (preflight) has passed yet')
    elif not pre.get('passed'):
        global_block=True;kinds.append('preflight-failed')
        reasons.append('the last safety check ('+when(pre.get('at'))+') failed: '+'; '.join(pre.get('problems') or ['no reason saved']))
    if local is None and start_block:local=(here(),start_block)
    gates=host_gates(snap,local)
    stuck=[];host_reasons={};off=set()
    for n,k,r in rows:
        eligible=['m2','m6'] if r.get('placement')=='any' else [r.get('placement')]
        blocked_hosts=[h for h in eligible if gates.get(h)]
        if global_block:stuck.append((n,k,r));continue
        if not snap['batches'][n].get('enabled'):stuck.append((n,k,r));off.add(n);continue
        paused=eq.paused_reason(r['id'],r.get('next_executor',r['executor']),eq.load_config())
        if paused:stuck.append((n,k,r));host_reasons['group pause']=r['id']+' is in a paused group ('+paused+')';continue
        if blocked_hosts and len(blocked_hosts)==len(eligible):
            stuck.append((n,k,r))
            for h in blocked_hosts:host_reasons[h]=gates[h]
    if not global_block:
        for h,why in sorted(host_reasons.items()):
            kinds.append('gate-'+h);reasons.append(why if h=='group pause' else h.upper()+': '+why)
        if off:kinds.append('batch-off');reasons.append('these batches were never switched on: '+', '.join(sorted(off)))
    return dict(count=len(stuck),reasons=reasons if stuck else [],kinds=kinds if stuck else [],
                keys=sorted(n+':'+k for n,k,_ in stuck),rows={n+':'+k:row_label(r) for n,k,r in stuck},
                short={n+':'+k:short_label(r,'WILL NOT START') for n,k,r in stuck},
                jobs=[row_label(r) for _,_,r in stuck],
                held=[row_label(r)+': '+r['held'].get('reason','') for _,_,r in held])


def headline(blockers):
    if not blockers['count']:return None
    n=blockers['count']
    return ('NOT STARTING: '+str(n)+' queued edit'+('s' if n!=1 else '')+' will not start until this is fixed. '+
            'Why: '+'; '.join(blockers['reasons'])+'. Waiting: '+', '.join(blockers['jobs'])+'.')


def report(snap, error=None):
    """Saved on M6 every tick, including when the M2 link is down."""
    groups={x:[] for x in ('Checked','Unreviewed','Needs Dan','Blocked','Unknown (Mac unreachable)','Queued / Running')}
    now=time.time()
    for name,d in snap.get('batches',{}).items():
        for k,r in d['jobs'].items():
            if r['status']=='taken-over':continue
            owner=(r.get('claim') or {}).get('owner',r.get('placement'))
            c=r.get('claim') or {};last_tick=d.get('ticks',{}).get(owner,0)
            unknown=(bool(error) and r['status'] not in TERMINAL) or (r['status']=='claimed' and now-last_tick>STALE_S)
            group='Unknown (Mac unreachable)' if unknown else {'delivered':'Checked','delivered-unreviewed':'Unreviewed','needs-dan':'Needs Dan','blocked':'Blocked'}.get(r['status'],'Queued / Running')
            o=r.get('outcome',{});link=o.get('link','');verified=False
            if link and here()=='m6':
                try:
                    import urllib.request
                    with urllib.request.urlopen(link,timeout=3) as response:verified=response.status==200
                except Exception:pass
            item=dict(batch=name,job=r['id'],round=r['round'],title=r['title'],host=owner,status=r['status'],
                      reason='owner unreachable' if unknown else o.get('reason') or o.get('question') or o.get('verdict') or c.get('phase') or r.get('last_start_error') or ('paused-for-allowance until '+str(r['not_before']) if r['not_before']>now else r['status']),
                      link=link,link_verified=verified,timing=r.get('timing',{}),allowance_pauses=r.get('allowance_pauses',[]),idle_slot_minutes_sampled=r.get('idle_slot_minutes',0),queue_wait_s=max(0,r.get('first_started',now)-r['queued_at']))
            if r['status']=='needs-dan':
                item['waiting_s']=now-r.get('ended',now)
                if o.get('finding'):item['reason']=str(item['reason'])+' Finding: '+str(o['finding'])
                if o.get('choices'):item['reason']=str(item['reason'])+' Choices: '+'; '.join(map(str,o['choices']))
            if r['status']=='blocked' and not unknown:
                item['owner']=o.get('owner') or editor_name(r)
                item['reason']=str(item['reason'])+' NEXT ('+item['owner']+'): '+str(o.get('next_action','not recorded'))
            if r['status']=='queued' and r.get('held'):item['reason']='Held: '+r['held'].get('reason','')
            groups[group].append(item)
    lost=[]
    if here()=='m6':
        catalog={r['id']:r for r in read(Path(eq.ROOT)/'Handoffs/video-editing/jobs.json',{'jobs':[]})['jobs']}
        route=read(Path.home()/'.absbyai-editroute/waiting.json',{})
        obs=d.get('observations',{}) if snap.get('batches') else {}
        # Combined-line promotions are journalled even after waiting.json is popped.
        path=Path.home()/'.absbyai-editroute/decisions.jsonl'
        try:
            entries=[json.loads(line) for line in path.read_text().splitlines()[-2000:]]
            latest={e['job']:e for e in entries if not e.get('dry')}
            for j,e in latest.items():
                if catalog.get(j,{}).get('state') in ('delivered','draft_review','finalized','uploaded'):continue
                if e.get('host') in ('m2','m6') and e.get('from_line') and 600<now-e['t']<86400:
                    observed=[v.get(j) for dd in snap.get('batches',{}).values() for v in dd.get('observations',{}).values()]
                    if not any(observed):lost.append(j+' LOST: promoted without editcap entry after 10 minutes')
        except (OSError,ValueError,KeyError):pass
    outbox_errors=[read(p).get('_error') for p in (HOME/'outbox').glob('*.json') if read(p).get('_error')]
    blockers=start_blockers(snap,error=error,local=(here(),snap.get('start_block')))
    head=headline(blockers)
    alerts=[x for x in [head,
                        (str(len(groups['Needs Dan']))+' video(s) need your answer') if groups['Needs Dan'] else None,
                        (str(len(groups['Blocked']))+' video(s) blocked; each names who acts next') if groups['Blocked'] else None,
                        ('Status unknown: '+error) if error else None] if x]
    doc=dict(outbox_errors=outbox_errors,at=now,start_block=snap.get('start_block'),enabled=snap.get('control',{}).get('enabled',False),
             error=error,groups=groups,lost=lost,headline=head,not_starting=blockers,alerts=alerts,report=str(HOME/'morning-report.md'))
    write(HOME/'morning-report.json',doc)
    lines=([head,''] if head else [])+['# Overnight edit report','',time.strftime('%Y-%m-%d %H:%M:%S %Z'),'', 'New starts: '+('enabled' if doc['enabled'] else 'disabled')]
    if blockers['held']:lines+=['','Held by Dan (not counted as waiting): '+'; '.join(blockers['held'])]
    if error:lines+=['',error]
    if outbox_errors:lines+=['','Outcome sync waiting: '+ '; '.join(outbox_errors)]
    if doc['start_block']:lines+=['','New starts blocked: '+doc['start_block']]
    for group,rows in groups.items():
        lines+=['','## '+group,'','| Video | Mac | State / next action | Review |','|---|---|---|---|']
        for r in rows:
            label='Open review' if r['link_verified'] else 'Link unverified'
            link='['+label+']('+r['link']+')' if r['link'] else ''
            lines.append('| '+r['title'].replace('|','/')+' ('+r['job']+' R'+str(r['round'])+') | '+str(r['host'])+' | '+str(r['reason']).replace('|','/')+' | '+link+' |')
    lines+=['',*lost]
    (HOME/'morning-report.md').write_text('\n'.join(lines)+'\n')
    try:doc['alert']=send_alerts(snap,doc)
    except Exception as exc:doc['alert']=dict(error=str(exc) or type(exc).__name__)
    return doc


def applescript(text):
    return '"'+str(text).replace('\\','\\\\').replace('"','\\"')+'"'


def notify(title, message):
    """A local notification on this Mac. Delivery to the screen cannot be confirmed from launchd; the edit
    desk shows the same alert lines as the fallback."""
    script='display notification '+applescript(message[:240])+' with title '+applescript(title[:80])+' sound name "Glass"'
    run=subprocess.run(['/usr/bin/osascript','-e',script],capture_output=True,text=True,timeout=20)
    return dict(method='osascript display notification',rc=run.returncode,stderr=(run.stderr or '')[-300:])


def short_label(r, what):
    """Job, round and status first; only the title is clipped."""
    return r['id']+' R'+str(r['round'])+' '+what+' ('+(r.get('title') or '')[:40]+')'


def alert_events(snap, doc):
    """(key, short text, ended) for every blocked or needs-Dan row."""
    events=[]
    for n,d in snap.get('batches',{}).items():
        for k,r in d.get('jobs',{}).items():
            if r.get('status') in ('blocked','needs-dan'):
                o=r.get('outcome') or {}
                what='NEEDS YOU' if r['status']=='needs-dan' else 'BLOCKED, '+(o.get('owner') or editor_name(r))+' next'
                events.append((r['status']+':'+n+':'+k+':'+str(int(r.get('ended') or 0)),short_label(r,what),r.get('ended') or 0))
    return events


def send_alerts(snap, doc, now=None):
    """One notification per new event, recorded in alerts.json and never repeated. M6 only.

    Blocked and needs-Dan rows are events by their ending. A round that cannot start opens an episode that
    stays open while it stays stuck and closes when it clears, so a later recurrence rings again and a
    partly resolved set does not."""
    if here()!='m6':return None
    now=now or time.time();path=HOME/'alerts.json';existing=read(path)
    state=existing or dict(created=now,events={},episodes={})
    state.setdefault('events',{})
    migrating=existing is not None and 'episodes' not in existing   # only an older ledger's open incidents are known
    episodes=state.setdefault('episodes',{})
    candidates=[]
    for e,text,ended in alert_events(snap,doc):
        if e in state['events']:
            prior=state['events'][e]
            if prior.get('sent') or prior.get('seeded') or prior.get('tries',0)>=3:continue
        elif ended<ROLLOUT_AT:
            state['events'][e]=dict(text=text,at=now,seeded=True);continue
        candidates.append((e,text))
    stuck=(doc.get('not_starting') or {}).get('short') or {}
    for rk in list(episodes):
        if rk not in stuck:episodes.pop(rk)
    for rk,label in sorted(stuck.items()):
        if rk not in episodes:
            episodes[rk]=dict(id='not-starting:'+rk+':'+uuid.uuid4().hex[:10],since=now)
            if migrating:state['events'][episodes[rk]['id']]=dict(text=label,at=now,seeded=True);continue
        e=episodes[rk]['id'];prior=state['events'].get(e,{})
        if not (prior.get('sent') or prior.get('seeded') or prior.get('tries',0)>=3):candidates.append((e,label))
    included=[];body=''
    for e,text in candidates:
        nxt=(body+'; ' if body else '')+text
        if len(nxt)>200 and included:break      # the rest wait for the next tick; only what is shown is recorded
        included.append((e,text));body=nxt
    if not included:
        write(path,state);return dict(sent=0)
    title='Edit queue: '+str(len(candidates))+' item(s), report on the edit desk'
    body=body[:230]
    try:result=notify(title,body)
    except Exception as exc:result=dict(method='osascript display notification',rc=-1,stderr=str(exc))
    for e,text in included:
        prior=state['events'].get(e,{})
        state['events'][e]=dict(text=text,at=now,sent=result['rc']==0,tries=prior.get('tries',0)+1,delivery=result,
                                screen_delivery='not verifiable from the background; the edit desk shows the alert and the report')
    write(path,state)
    return dict(sent=len(included),waiting=len(candidates)-len(included),result=result)


def worker_command(claim_path):
    """Both Macs launch the runner directly from their own launchd agent (2026-11-18).

    The old M2 -> M6 -> M2 SSH hop made every M2 edit depend on the M6 staying awake. Drive access now comes
    from the agent's own Full Disk Access grant, and preflight plus every tick refuse to start anything until
    that Mac's background file-access check passes. The returned PID is the runner itself."""
    return [sys.executable,str(Path(eq.HERE)/'runner.py'),'--batch',str(claim_path)], False


def worker_spawn_fields(proc, via_ssh):
    # The SSH transport is not the runner. Its first heartbeat supplies the actual local PID.
    prefix='transport_' if via_ssh else ''
    return {prefix+'pid':proc.pid,prefix+'birth':identity(proc.pid)}


def tick():
    HOME.mkdir(parents=True,exist_ok=True)
    with (HOME/'tick.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return dict(busy=True)
        try:
            try:maybe_probe()
            except Exception as exc:print('file-access check failed to run:',exc,flush=True)
            flush_outbox()
            fp=fingerprints()
            def gate(control):
                probe=launchd_probe_status()
                if fp['dirty']:return 'installed source differs from pushed main: '+', '.join(fp['dirty'])
                if control.get('enabled') and fp['digest']!=control.get('preflight',{}).get('digest'):return 'scheduler changed since preflight'
                return None if probe['ok'] else probe['problem']
            # This Mac's own start gate travels with its observation, so the other Mac's report and receipts know it.
            observation=observe_local()
            observation['_start_block']=dict(at=time.time(),reason=gate(read(HOME/'snapshot.json',{}).get('control',{})))
            snap=rpc('tick',host=here(),observation=observation);save_snapshot(snap)
            reconcile(snap)
            start_block=gate(snap['control'])
            if not start_block:
                while True:
                    cap=subprocess.run([sys.executable,str(SHARED/'editcap/editcap.py'),'status','--json'],capture_output=True,text=True,timeout=30)
                    if cap.returncode:raise RuntimeError('editcap status unavailable: '+cap.stderr[-300:])
                    ec=json.loads(cap.stdout)
                    owned=rpc('claim',host=here(),digest=fp['digest'],occupied=ec['in_use'],slots=ec['cap'])
                    if not owned:break
                    snap=rpc('snapshot');save_snapshot(snap)
                    row=owned['row'];token=row['claim']['token']
                    claim_home=HOME/'runs'/token;claim_home.mkdir(parents=True,exist_ok=True)
                    write(claim_home/'claim.json',owned)
                    log=(claim_home/'runner.log').open('a')
                    try:
                        command,via_ssh=worker_command(claim_home/'claim.json')
                        proc=subprocess.Popen(command,cwd=eq.ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
                        update('heartbeat',owned['batch'],owned['key'],token,fields=worker_spawn_fields(proc,via_ssh))
                    except OSError:
                        rpc('recover',batch=owned['batch'],key=owned['key'],token=token,host=here(),pid_alive=False,spawn_failed=True)
                    finally:log.close()
            snap=rpc('snapshot');save_snapshot(snap)
            if start_block:snap['start_block']=start_block
            write(HOME/'start-block.json',dict(at=time.time(),host=here(),start_block=start_block))
            doc=report(snap)
            print('Batch tick:',here(),'new starts',snap['control'].get('enabled',False),flush=True)
            return doc
        except CoordinatorUnreachable as exc:
            doc=report(read(HOME/'snapshot.json',{}),'M2 ledger unreachable: '+str(exc))
            print('Batch tick unavailable:',exc,flush=True);return doc
        except Exception as exc:
            # A fault on this Mac stops only this Mac's claims; the other Mac's rounds are judged on their own.
            snap=read(HOME/'snapshot.json',{});why='this Mac\'s last check failed: '+(str(exc) or type(exc).__name__)[:200]
            snap['start_block']=why
            write(HOME/'start-block.json',dict(at=time.time(),host=here(),start_block=why))
            doc=report(snap)
            print('Batch tick incomplete:',exc,flush=True);return doc


def job_live(job_id,statuses):
    return any(job_id in st.get('editcap',{}).get('in_use',[]) or
               st.get('editcap',{}).get('edits',{}).get(job_id) in ('waiting','promoted','active','parked')
               for st in statuses.values())


def enqueue(name,path):
    source=Path(path).resolve();request=json.loads(source.read_text())
    jobs=[];briefs={}
    # Source location and owner are inspected once at enqueue, before accepting the work.
    sys.path.insert(0,str(SHARED/'editroute'));import editroute
    for i,j in enumerate(request['jobs']):
        job=dict(j);job['id']=job['id'].upper()
        if not JOB.fullmatch(job['id']):raise ValueError('invalid job ID')
        shortened=re.match(r'^([A-Z]{2,3})-(\d{1,3}[A-Z]?)(?![0-9])',job['id'])
        if shortened and shortened.group(0)!=job['id']:raise ValueError('job ID would be shortened by editcap')
        if job.get('size') not in ('L','M','S') or int(job.get('round',0))<1:raise ValueError('size and positive round required')
        if job.get('executor') not in ('claude','codex'):raise ValueError('preserve an explicit editor for each job')
        if not job.get('title') or not job.get('kind') or not job.get('target'):raise ValueError('title, kind and target required')
        if float(job.get('need_gb',0))<=0:raise ValueError('honest additional storage need_gb required')
        job['order']=job.get('order',i);job['round']=int(job['round'])
        job['chroma']=bool(job.get('chroma'));job['drive_bound']=bool(job.get('drive_bound'))
        statuses=editroute.gather(job['id']);owner,_=editroute.holder(job['id'],statuses)
        if any(not st.get('reachable') for st in statuses.values()):raise ValueError('both Macs must be reachable to establish placement at enqueue')
        if job_live(job['id'],statuses):
            raise ValueError(job['id']+' has active production; batch enqueue cannot transfer a live chat')
        if owner:placement=owner
        elif job['kind']=='LFC' or job['chroma'] or job['drive_bound']:placement='m2'
        else:placement='any'
        job['placement']=placement
        brief=Path(job.pop('brief'));brief=brief if brief.is_absolute() else source.parent/brief
        data=brief.read_bytes();job['brief_sha256']=hashlib.sha256(data).hexdigest()
        briefs[key(job)]=base64.b64encode(data).decode();jobs.append(job)
    result=rpc('enqueue',batch=name,jobs=jobs,briefs=briefs,digest=fingerprints()['digest'])
    kick(other=True)
    result['receipt']='registered; waiting for both Macs to log this batch'
    result.update(startability(name))
    return result


def startability(name, snap=None):
    """Whether anything will actually launch this batch now. A chat is never told 'queued' when nothing will."""
    snap=snap or rpc('snapshot')
    local=read(HOME/'start-block.json',{})
    mine=(here(),local.get('start_block')) if time.time()-local.get('at',0)<GATE_STALE_S else None
    blockers=start_blockers(snap,batch=name,local=mine)
    if not snap.get('batches',{}).get(name):
        return dict(can_start=False,start_status='WILL NOT START: batch '+name+' is not registered.')
    rows=list(snap['batches'][name]['jobs'].values())
    if rows and all(r['status']!='queued' for r in rows):
        state='; '.join(r['id']+' R'+str(r['round'])+' '+('RUNNING on the '+str((r.get('claim') or {}).get('owner','?')).upper()
                        if r['status']=='claimed' else r['status'].upper()) for r in rows)
        return dict(can_start=False,start_status='NOT WAITING: '+state+'.')
    if blockers['count']:
        return dict(can_start=False,blockers=blockers['reasons'],
                    start_status='WILL NOT START: '+'; '.join(blockers['reasons'])+'. It stays registered; nothing will launch it until that is fixed.')
    held=[r for r in snap['batches'][name]['jobs'].values() if r.get('held')]
    if held:return dict(can_start=False,start_status='WILL NOT START: held by Dan ('+held[0]['held'].get('reason','')+').')
    c=snap.get('control',{});now=time.time();later=[]
    for r in rows:
        ex=r.get('next_executor',r['executor']);until=max(r.get('not_before',0),c.get('executor_backoff',{}).get(ex,{}).get('until',0))
        if r['status']=='queued' and until>now:later.append(r['id']+' R'+str(r['round'])+' after '+when(until))
    if later:return dict(can_start=True,start_status='CAN START LATER: '+', '.join(later)+' (allowance or retry wait), then when a slot is free.')
    return dict(can_start=True,start_status='CAN START: starts are on and the safety check passed; it begins when a slot on its Mac is free.')


def receipt(name):
    snap=rpc('snapshot');d=snap['batches'][name]
    observed=all(d.get('ticks',{}).get(h,0)>=d['manifest']['created'] for h in ('m2','m6'))
    can=startability(name,snap)
    text=('queued' if can['can_start'] else 'logged by both Macs but '+can['start_status']) if observed else 'registered; waiting for both ticks'
    return dict(batch=name,receipt=text,enabled=d['enabled'],ticks=d['ticks'],jobs=list(d['jobs']),**can)


def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('_rpc');p=sub.add_parser('_probe-worker');p.add_argument('host');sub.add_parser('preflight');sub.add_parser('tick');sub.add_parser('stop');sub.add_parser('status')
    p=sub.add_parser('fingerprints');p.add_argument('--fresh-probe',action='store_true')
    p=sub.add_parser('drive-probe',help='check background file access; --launchd asks this Mac\'s agent and waits')
    p.add_argument('--launchd',action='store_true')
    p=sub.add_parser('hold');p.add_argument('batch');p.add_argument('key');p.add_argument('--reason',required=True)
    p=sub.add_parser('unhold');p.add_argument('batch');p.add_argument('key')
    p=sub.add_parser('enqueue');p.add_argument('batch');p.add_argument('manifest')
    p=sub.add_parser('enqueue-chat');p.add_argument('job');p.add_argument('--brief',required=True)
    p.add_argument('--round',type=int,required=True);p.add_argument('--title',required=True)
    p.add_argument('--size',choices=['S','M','L'],required=True);p.add_argument('--kind',required=True)
    p.add_argument('--executor',choices=['claude','codex'],required=True);p.add_argument('--need-gb',type=float,required=True)
    p.add_argument('--target',required=True);p.add_argument('--chroma',action='store_true')
    p=sub.add_parser('receipt');p.add_argument('batch')
    p=sub.add_parser('start');p.add_argument('batch')
    p=sub.add_parser('takeover');p.add_argument('job');p.add_argument('--round',type=int)
    p=sub.add_parser('guard');p.add_argument('job')
    args=ap.parse_args()
    if args.cmd=='_rpc':result=handle(json.load(sys.stdin))
    elif args.cmd=='fingerprints':result=fingerprints(fresh_probe=args.fresh_probe)
    elif args.cmd=='_probe-worker':
        print(json.dumps(drive_probe(host=args.host)));return 0
    elif args.cmd=='drive-probe':
        if args.launchd:
            request_id=request_launchd_probe(wait_s=90)
            status=launchd_probe_status(request_id=request_id)
            answered=read(HOME/'drive-probe-launchd.json',{}).get('request')==request_id
            result=dict(answered=answered,record=read(HOME/'drive-probe-launchd.json',{}),status=status)
            print(json.dumps(result,indent=2))
            print(('PASS' if result['status']['ok'] else 'FAIL')+' '+here()+' background agent: '+(result['status']['problem'] or 'every folder: create, write, rename, delete')
                  +('' if answered else ' (agent did not answer within 90 s; shown result is the last saved one)'))
            return 0 if result['status']['ok'] and answered else 2
        result=record_probe('interactive')
    elif args.cmd in ('hold','unhold'):result=rpc(args.cmd,batch=args.batch,key=args.key,reason=getattr(args,'reason',None),by='Dan')
    elif args.cmd=='preflight':result=preflight()
    elif args.cmd=='tick':result=tick()
    elif args.cmd=='enqueue':result=enqueue(args.batch,args.manifest)
    elif args.cmd=='enqueue-chat':
        spec=HOME/'chat-submissions'/(args.job+'-R'+str(args.round)+'.json')
        write(spec,dict(jobs=[dict(id=args.job,round=args.round,title=args.title,size=args.size,kind=args.kind,
                                  executor=args.executor,need_gb=args.need_gb,target=args.target,chroma=args.chroma,
                                  brief=str(Path(args.brief).resolve()))]))
        result=enqueue('chat-'+args.job+'-R'+str(args.round),spec)
        print(json.dumps(result,indent=2));print(result['start_status']);return 0
    elif args.cmd=='receipt':
        result=receipt(args.batch);print(json.dumps(result,indent=2));print(result['start_status']);return 0
    elif args.cmd=='start':
        proof=preflight()
        if not proof['passed']:raise RuntimeError('; '.join(proof['problems']))
        result=rpc('start',batch=args.batch,digest=proof['digest']);kick(other=True)
    elif args.cmd=='stop':result=rpc('stop')
    elif args.cmd=='takeover':
        result=rpc('takeover',job=args.job,round=args.round,host=here());save_snapshot(rpc('snapshot'));kick(other=True)
    elif args.cmd=='guard':
        result=guard(args.job)
        if result:print(json.dumps(result));return 3
    else:result=rpc('snapshot')
    print(json.dumps(result,indent=2));return 0

if __name__=='__main__':
    try:sys.exit(main())
    except Exception as exc:print(str(exc),file=sys.stderr);sys.exit(1)
