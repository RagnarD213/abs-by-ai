"""One batch worker. Owns its editcap slot and records an outcome on every ordinary exit."""
import base64
import hashlib
import json
import shutil
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import threading
import time

import eq_common as eq
eq.unshadow()
b=eq.sibling('batch')
r=eq.sibling('runner')


def review_verdict(path, expected_hashes=None, started_ns=None):
    try:text=Path(path).read_text()
    except FileNotFoundError:return None
    if started_ns is not None and Path(path).stat().st_mtime_ns<started_ns:return None
    identity_missing=bool(expected_hashes and any(digest not in text for digest in expected_hashes))
    first=text.splitlines()[0].strip().replace('**','') if text.strip() else ''
    for verdict in ('SHIP WITH DISCLOSED UNCERTAINTY','DOES NOT SHIP','SHIP'):
        if first=='VERDICT: '+verdict:
            if verdict=='DOES NOT SHIP' and (identity_missing or not (re.search(r'\b\d{1,2}:\d{2}\b',text) and re.search(r'rule|\.md|standard',text,re.I))):
                return 'REJECTION WITHOUT CITATION'
            if identity_missing:return None
            return verdict
    return None


# Evidence-format errors one automatic repair session may fix (2026-11-18). Anything else, including a
# delivery gate FAIL, is substantive and is never "repaired" by rewriting evidence.
FORMAT_ERRORS = ('DELIVERY approved_elements','DELIVERY reuse','DELIVERY paid_provider_costs','paid_provider_costs row',
                 'DELIVERY generation_spend_usd','revision_count must equal')


def split_delivery_errors(errors):
    fmt=[e for e in errors if e.startswith(FORMAT_ERRORS)]
    return fmt,[e for e in errors if e not in fmt]


def documented_gate_hold(info, substantive):
    """A gate FAIL whose every failing row the editor documented against an approved choice is Dan's call."""
    if not substantive or any('DELIVERY gate must be PASS' not in e for e in substantive):return None
    dispositions=info.get('gate_failure_dispositions')
    failures=info.get('gate_failures')
    if not dispositions or not failures:return None
    return dict(finding=failures if isinstance(failures,str) else json.dumps(failures)[:1500],
                dispositions=dispositions if isinstance(dispositions,str) else json.dumps(dispositions)[:1500])


class StartupWait(RuntimeError):
    def __init__(self,reason,kind='capacity'):
        super().__init__(reason);self.kind=kind


def review_location(info):
    root=Path(info.get('review_root',''));port=info.get('review_port')
    if not root.is_absolute() or not root.is_dir() or not isinstance(port,int) or not (1024<=port<=65535):
        raise ValueError('outcome needs an absolute review_root and review_port from editroute.py free-port')
    return root,port


def review_link(info):
    """The existing managed review server mirrors M2 pages to the M6 and verifies HTTP."""
    root,port=review_location(info)
    if info.get('review_report'):
        source=Path(info['review_report'])
        if source.is_file():
            shutil.copy2(source,root/'independent-review.md')
            page=root/'index.html'
            if page.is_file():
                html=page.read_text()
                if 'independent-review.md' not in html:
                    page.write_text(html+'\n<p><a href="independent-review.md">Independent review and findings</a></p>\n')
    run=subprocess.run([sys.executable,str(b.SHARED/'review_server.py'),str(port),str(root)],capture_output=True,text=True,timeout=120)
    if run.returncode:raise b.TransportError('managed review installation/mirror failed: '+(run.stdout+run.stderr)[-600:])
    link='http://127.0.0.1:'+str(port)+'/'
    if b.here()=='m2':
        cmd=['ssh','-oBatchMode=yes','-oConnectTimeout=3','m6','curl -fsS --max-time 5 -o /dev/null '+link]
    else:cmd=['curl','-fsS','--max-time','5','-o','/dev/null',link]
    opened=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
    if opened.returncode:raise b.TransportError('M6 review link did not open')
    return link


def candidate_stamps(files):
    """Reuse the shared gate's exact-file/version check without adding editorial thresholds."""
    sys.path.insert(0,str(Path(eq.ROOT)/'.claude/skills'))
    try:
        from _shared.deliver import gate
        for file in files:gate.require_stamp(file,quiet=True)
    except (SystemExit,Exception) as exc:
        raise ValueError('candidate lacks current exact-file gate evidence: '+str(exc))


def main(claim_path):
    owned=b.read(claim_path);row=owned['row'];name=owned['batch'];k=owned['key'];token=row['claim']['token']
    jobid=row['id'];cfg=eq.load_config();executor=row['executor']
    subprocess.Popen(['/usr/bin/caffeinate','-i','-w',str(os.getpid())],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    os.environ.update(EDIT_BATCH_TOKEN=token,GATE_GROUP=jobid,EDIT_BATCH_JOB=jobid)
    fields=dict(pid=os.getpid(),birth=b.identity(os.getpid()),phase='allocating work folder')
    if b.update('heartbeat',name,k,token,fields=fields) is None:
        # No session may start until this owner has confirmed its durable claim.
        b.write(Path(claim_path).parent/'not-started.json',dict(reason='coordinator unavailable before first session'))
        return 1
    stop=threading.Event();has_slot=False;cap_requested=False;session_started=False;pending_cleanup=False;wd=None;checkpoint={};edit_h=review_h=0.;started=time.time()
    outcome=dict(status='blocked',reason='runner exited before completing',next_action='Inspect the retained worker log')
    lock=threading.Lock();current=dict(fields)
    def progress(**values):
        with lock:current.update(values);data=dict(current)
        # Local identity survives M6 losing its coordinator connection.
        b.write(Path(claim_path).parent/'progress.json',data)
        return b.update('heartbeat',name,k,token,fields=data)
    def pulse():
        while not stop.wait(b.HEARTBEAT_S):
            try:
                if has_slot:
                    subprocess.run([sys.executable,str(b.SHARED/'editcap/editcap.py'),'heartbeat',jobid],capture_output=True,timeout=35)
                progress()
            except Exception as exc:
                print('heartbeat retry: '+(str(exc) or type(exc).__name__),flush=True)
    thread=threading.Thread(target=pulse,daemon=True);thread.start()
    def interrupted(signum,frame):raise r.SessionInterrupted('runner interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted)
    signal.signal(signal.SIGINT,interrupted)
    def session(ex, prompt, role, timeout):
        nonlocal session_started
        session_started=True
        def observe(pid,birth):progress(session=dict(pid=pid,birth=birth),phase=role)
        code,tail,hours=r.run_session(ex,cfg,str(wd),prompt,str(wd/'queue-run.log'),role,timeout,session_observer=observe)
        progress(session={},phase=role+' ended')
        return code,tail,hours
    try:
        # Claim and slot are separate: this runner acquires, refreshes and finally releases the slot.
        if not eq.resolve_binary(executor,cfg):raise StartupWait(executor+' program is unavailable','executor')
        cap_requested=True
        cap=subprocess.run([sys.executable,str(b.SHARED/'editcap/editcap.py'),'acquire',jobid,'--title',row['title'],'--type',row['kind']],capture_output=True,text=True,timeout=45)
        if cap.returncode!=0:raise StartupWait('edit slot not acquired: '+(cap.stdout+cap.stderr)[-600:])
        # editcap historically fails open. Confirm the registry actually records this job as active.
        registry=b.read(Path(os.environ.get('EDITCAP_DIR','/tmp/absbyai-editcap'))/'registry.json',{})
        if registry.get('edits',{}).get(jobid,{}).get('state')!='active':raise StartupWait('editcap did not record an active slot','infrastructure')
        has_slot=True
        work=subprocess.run([sys.executable,str(b.SHARED/'renderq/renderq.py'),'workdir',jobid,'--need',str(row['need_gb'])],capture_output=True,text=True,timeout=45)
        if work.returncode:raise StartupWait('work folder: '+(work.stdout+work.stderr)[-600:],'storage')
        wd=Path(work.stdout.strip().splitlines()[-1])
        if not wd.is_absolute() or not wd.is_dir():raise RuntimeError('renderq did not return a usable work folder')
        if row.get('workdir') and str(wd)!=row['workdir']:raise RuntimeError('resume must use the original work folder')
        progress(workdir=str(wd),phase='preparing editor')
        brief=base64.b64decode(owned['brief'],validate=True)
        if hashlib.sha256(brief).hexdigest()!=row['brief_sha256']:raise ValueError('brief hash mismatch')
        (wd/(k+'-BRIEF.md')).write_bytes(brief)
        checkpoint_path=wd/(k+'-batch-checkpoint.json');checkpoint=b.read(checkpoint_path,{})
        if checkpoint and checkpoint.get('brief_sha256')!=row['brief_sha256']:raise ValueError('resume brief changed')
        checkpoint.update(brief_sha256=row['brief_sha256'])
        if row['attempts']==1 and checkpoint.get('registration')!=name:
            checkpoint['review_attempts']=0
        checkpoint['registration']=name
        job=dict(id=jobid,title=row['title'],size=row['size'],state='ready',file=row.get('jobdoc',''),
                 claude=brief.decode(),codex=brief.decode())
        job['queue_revision']=dict(round=row['round'],words='Execute the copied batch brief exactly')
        packet=r.write_work_packet(job,str(wd),token)
        budget=eq.start_budget(job,cfg,str(wd),token,preserve_renders=bool(row['attempts']>1))
        # Carry elapsed work time forward. Allowance pauses do not get charged as active editing.
        hours_used=float(checkpoint.get('edit_hours',0))
        budget['hours_allowed']=max(0,budget['hours_allowed']-hours_used)
        import datetime
        clock=datetime.datetime.now().astimezone()
        budget['deadline']=(clock+datetime.timedelta(hours=budget['hours_allowed'])).isoformat()
        budget['soft_deadline']=(clock+datetime.timedelta(hours=budget['hours_allowed']*.7)).isoformat()
        b.write(wd/'BUDGET.json',budget)
        brief_text=brief.decode()
        instructions=f'''Read AGENTS.md, .claude/skills/_shared/VIDEO-RULES.md, WORK_PACKET.json and BUDGET.json first.
You are the single unattended editor for {row['title']} ({jobid}), round {row['round']}.
Your work folder is {wd}; the runner already holds and heartbeats your edit slot. Use renderq for heavy steps.
On M6, copy the needed source footage to the internal work folder with editroute.py fetch before heavy work; never encode against a network share.
Do not use ps to impose the old two-build cap, run editroute wait, acquire/release editcap yourself, or change queue state.
Do not upload, publish, schedule, send messages, change shared scheduling code, or spawn supervisors or a final reviewer. Required asset/frame checks still follow the existing skill.
Resume existing verified work and provider receipts in this folder. Never repeat a paid request without reconciling its result.
Target: {row['target']}. This is the complete approved scope, with no new review gates.
Keep all actual approval requirements. Headless sessions have no Flow browser. If new AI clips or choices are needed,
prepare the required first-review page and stop with needs-dan, not a claimed full film. Real footage/library first.
Use 1080p review exports. Automated checks stay silent; leave every owner player paused and sound-ready.
On a genuine choice write BATCH-OUTCOME.json with schema 1, token "{token}", status "needs-dan", question,
review_root (absolute managed review folder), review_port (reserved using editroute free-port), and evidence
listing the review file path and sha256. Include the first-review page. Never wait or poll for Dan.
If a mandatory quality check still fails and nothing approved is left to try, do not write blocked: write needs-dan
with the exact finding (finding), the choices Dan has (choices, a list) and the review page. Never change a threshold.
On a technical block write BATCH-OUTCOME.json with token "{token}", status "blocked", reason, owner (Dan, Claude or Codex)
and next_action written so a non-coder knows who does what next.
On a complete candidate write DELIVERY.json using the existing scripts/edit-queue/preamble.md final delivery schema,
plus review_root and review_port. Write BATCH-OUTCOME.json with token "{token}", status "candidate".
The final delivery must have every existing gate and self-check on the exact file. The runner starts the independent reviewer.
Exit 0 without a fresh outcome file is a failure. Do not invent a perceptual listen from silent checks.
Full renders obey the existing budget. Stop exploration at the soft deadline. Preserve every unchanged approval.
\nCOPIED BRIEF:\n{brief_text}'''
        marker_path=wd/'BATCH-OUTCOME.json'
        if not checkpoint.get('candidate'):
            if marker_path.exists():marker_path.replace(wd/('BATCH-OUTCOME.before-'+token+'.json'))
            progress(phase='editor')
            code,tail,edit_h=session(executor,instructions,'batch-editor',max(.001,budget['hours_allowed']))
            checkpoint['edit_hours']=hours_used+edit_h;b.write(checkpoint_path,checkpoint)
            marker=b.read(marker_path)
            if code!=0 and (not marker or marker.get('token')!=token):
                failure=r.classify_failure(code,tail,cfg)
                if failure=='usage_limited':
                    outcome=dict(status='paused-for-allowance',reason='editor usage limit',executor=executor);return 0
                if failure=='auth_failed':raise StartupWait('editor sign-in is unavailable','executor')
            if not marker or marker.get('token')!=token:raise RuntimeError('editor exited '+str(code)+' without a fresh outcome file')
            if code!=0:raise RuntimeError('editor exited '+str(code)+'; candidate not accepted')
            if marker.get('status')=='blocked':
                outcome=dict(status='blocked',reason=marker['reason'],next_action=marker['next_action'],
                             owner=marker.get('owner') or b.editor_name(row));return 0
            if marker.get('status')=='needs-dan':
                review_location(marker)
                evidence=marker.get('evidence',[])
                if not evidence:raise ValueError('needs-dan has no first-review evidence')
                for file in evidence:
                    if r.sha256(file['path'])!=file['sha256']:raise ValueError('review evidence hash mismatch')
                outcome=dict(status='needs-dan',question=marker['question'],link='http://127.0.0.1:'+str(marker.get('review_port',''))+'/',evidence=evidence)
                for extra in ('finding','choices'):
                    if marker.get(extra):outcome[extra]=marker[extra]
                try:outcome['link']=review_link(marker)
                except (OSError,RuntimeError,subprocess.SubprocessError):
                    outcome['pending_review']=dict(review_root=marker['review_root'],review_port=marker['review_port'])
                return 0
            if marker.get('status')!='candidate':raise ValueError('invalid editor outcome')
            info=b.read(wd/'DELIVERY.json',{})
            launch_state='frames_approved' if row.get('assets_approved') else 'ready'
            errors=r.validate_delivery(info,str(wd),packet,cfg,launch_state)
            fmt,substantive=split_delivery_errors(errors)
            if fmt and int(checkpoint.get('format_repairs',0))<1:
                # Exactly one repair by the same editor in the same folder; it may fix evidence format only.
                checkpoint['format_repairs']=1;b.write(checkpoint_path,checkpoint)
                repair=f'''Read AGENTS.md and {wd}/DELIVERY.json. You edited {row['title']} ({jobid}) round {row['round']} in {wd}.
The batch runner rejected only the FORMAT of your delivery evidence. Fix exactly these items in DELIVERY.json:
{chr(10).join('- '+e for e in fmt)}
Do not edit, render, re-time or regrade the film. Do not change any gate result, threshold, approval or file hash.
A gate FAIL stays a FAIL: leave gate and gate_failures as measured. For unknown costs add a row
{{"provider":"none","usd":0,"reason":"no paid provider used this round"}} or an unavailable row with a reason.
Then rewrite BATCH-OUTCOME.json with token "{token}" and status "candidate". Do not ask Dan anything.'''
                if marker_path.exists():marker_path.replace(wd/('BATCH-OUTCOME.before-repair-'+token+'.json'))
                progress(phase='evidence format repair')
                remaining=max(.25,min(1.0,float(budget['hours_allowed'])-edit_h))
                code,tail,repair_h=session(executor,repair,'batch-format-repair',remaining)
                edit_h+=repair_h;checkpoint['edit_hours']=hours_used+edit_h;b.write(checkpoint_path,checkpoint)
                if code!=0 and r.classify_failure(code,tail,cfg)=='usage_limited':
                    outcome=dict(status='paused-for-allowance',reason='editor usage limit during evidence repair',executor=executor);return 0
                marker=b.read(marker_path)
                if not marker or marker.get('token')!=token or marker.get('status')!='candidate':
                    raise ValueError('evidence format repair did not return a fresh candidate; remaining: '+'; '.join(fmt[:4]))
                info=b.read(wd/'DELIVERY.json',{})
                errors=r.validate_delivery(info,str(wd),packet,cfg,launch_state)
                fmt,substantive=split_delivery_errors(errors)
            hold=None if fmt else documented_gate_hold(info,substantive)
            if hold:
                review_location(info)
                outcome=dict(status='needs-dan',
                             question=('The finished film fails its delivery gate on rows the editor says conflict with your '
                                       'approved choices. Approve it as is, or ask for a fix of those rows?'),
                             finding=hold['finding'],dispositions=hold['dispositions'],
                             choices=['Approve as is (the failing rows follow your picks)','Ask for a fix of the failing rows'],
                             link='http://127.0.0.1:'+str(info.get('review_port',''))+'/')
                try:outcome['link']=review_link(info)
                except (OSError,RuntimeError,subprocess.SubprocessError):
                    outcome['pending_review']=dict(review_root=info['review_root'],review_port=info['review_port'])
                return 0
            if errors:raise ValueError('candidate evidence incomplete: '+'; '.join(errors[:6]))
            review_location(info)
            candidate_stamps(info['files'])
            checkpoint.update(candidate=True,files=[dict(path=f,sha256=r.sha256(f)) for f in info['files']],review_attempts=0)
            b.write(checkpoint_path,checkpoint)
        info=b.read(wd/'DELIVERY.json',{})
        candidate_stamps([file['path'] for file in checkpoint['files']])
        for file in checkpoint['files']:
            if r.sha256(file['path'])!=file['sha256']:raise ValueError('candidate changed after validation')
        review_location(info)
        link='http://127.0.0.1:'+str(info.get('review_port',''))+'/'
        reviewer=cfg['review']['reviewer_for'][executor]
        try:pause_control=b.rpc('snapshot')['control']
        except Exception:pause_control=b.read(b.HOME/'snapshot.json',{}).get('control',{})
        executor_pause=pause_control.get('executor_backoff',{}).get(reviewer,{})
        if executor_pause.get('until',0)>time.time():
            outcome=dict(status='paused-for-allowance',reason='reviewer allowance backoff',executor=reviewer,attempted=False);return 0
        verdict=None;reason='reviewer returned no valid verdict';report_path=None
        # A timeout or missing verdict gets one new session. A valid rejection never starts a fix loop.
        for attempt in range(int(checkpoint.get('review_attempts',0)),2):
            checkpoint['review_attempts']=attempt+1;b.write(checkpoint_path,checkpoint)
            report_path=wd/(k+'-'+token+'-BATCH-REVIEW-'+str(attempt+1)+'.md')
            if report_path.exists():report_path.replace(report_path.with_suffix('.before-session.md'))
            review_started_ns=time.time_ns()
            expected_hashes=[file['sha256'] for file in checkpoint['files']]
            prompt=f'''Read AGENTS.md and .claude/skills/_shared/VIDEO-RULES.md. Independently review only the exact
candidate files in {wd}/DELIVERY.json and the scope in {wd}/{k}-BRIEF.md and WORK_PACKET.json.
Do not read editor notes/logs or earlier review reports. Do not edit, render, publish, send, or ask Dan for a new gate.
Use existing checks and silent non-speaker inspection. Do not claim an audible listen from numbers.
Candidate SHA-256 values: {', '.join(expected_hashes)}. Echo every value in your report to identify the reviewed files.
Write {report_path}. First line exactly VERDICT: SHIP, VERDICT: DOES NOT SHIP, or
VERDICT: SHIP WITH DISCLOSED UNCERTAINTY. Cite the existing rule and a timestamp for every rejection.
Disclose unsupported checks and genuine uncertainty. Return one consolidated review; no fix loop or additional reviewers.'''
            progress(phase='reviewer')
            code,tail,hours=session(reviewer,prompt,'review-batch-'+str(attempt+1),float(budget['review_hours_allowed']))
            review_h+=hours
            verdict=review_verdict(report_path,expected_hashes,review_started_ns) if code==0 else None
            if verdict:break
            if code!=0 and r.classify_failure(code,tail,cfg)=='usage_limited':
                checkpoint['review_attempts']=attempt;b.write(checkpoint_path,checkpoint)
                outcome=dict(status='paused-for-allowance',reason='reviewer usage limit',executor=reviewer);return 0
            reason='reviewer timeout or no valid verdict after '+str(attempt+1)+' attempt(s)'
        for file in checkpoint['files']:
            if r.sha256(file['path'])!=file['sha256']:raise ValueError('candidate changed during review')
        candidate_stamps([file['path'] for file in checkpoint['files']])
        if verdict=='REJECTION WITHOUT CITATION':
            outcome=dict(status='delivered-unreviewed',reason='reviewer rejected without required rule, timestamp or candidate identity; findings attached',link=link,report=str(report_path),files=checkpoint['files'])
        elif verdict=='DOES NOT SHIP':
            outcome=dict(status='blocked',reason='independent reviewer: DOES NOT SHIP',next_action='Review the cut and consolidated findings; scope a separate revision',link=link,report=str(report_path))
        elif verdict in ('SHIP','SHIP WITH DISCLOSED UNCERTAINTY'):
            outcome=dict(status='delivered',verdict=verdict,link=link,report=str(report_path),files=checkpoint['files'])
        else:outcome=dict(status='delivered-unreviewed',reason=reason,link=link,files=checkpoint['files'])
        if report_path and report_path.exists():info['review_report']=str(report_path)
        try:outcome['link']=review_link(info)
        except (OSError,RuntimeError,subprocess.SubprocessError):
            outcome['pending_review']=dict(review_root=info['review_root'],review_port=info['review_port'],review_report=info.get('review_report'))
    except r.SessionCleanupFailed as exc:
        pending_cleanup=True
        progress(phase='session cleanup waiting; claim retained')
        outcome=dict(status='blocked',reason=str(exc),owner='Queue (automatic)',
                     next_action='Nothing for Dan yet: the queue waits for the old editor session to exit, then recovers it by itself.')
    except StartupWait as exc:
        outcome=dict(status='deferred-start',reason=str(exc) or type(exc).__name__,retry_kind=exc.kind)
    except Exception as exc:
        if not session_started and isinstance(exc,(OSError,RuntimeError,subprocess.SubprocessError)):
            outcome=dict(status='deferred-start',reason=str(exc) or type(exc).__name__,retry_kind='infrastructure')
        else:
            what=('fix what the check names; the film files are kept' if 'candidate evidence' in str(exc)
                  else 'finish the edit from where it stopped')
            outcome=dict(status='blocked',reason=str(exc) or type(exc).__name__,owner=b.editor_name(row),
                         next_action=b.takeover_action(row,what))
    finally:
        stop.set();thread.join(timeout=5)
        outcome=b.normalize_outcome(outcome)
        try:
            if wd:
                b.write(wd/(k+'-batch-outcome-'+token+'.json'),dict(outcome,token=token,at=time.time()))
            # Retain the exact outcome locally before attempting the M2 link; outbox syncs after reconnect.
            timing=dict(active_hours=edit_h,review_hours=review_h,worker_hours=(time.time()-started)/3600)
            if pending_cleanup:
                pass  # Keep the live claim and slot until the recorded session is confirmed gone.
            elif outcome.get('pending_review'):
                b.write(b.HOME/'outbox'/(token+'.json'),dict(op='outcome',batch=name,key=k,token=token,host=b.here(),outcome=outcome,timing=timing))
                progress(phase='outcome waiting for review mirror',session={})
            else:
                b.update('outcome',name,k,token,outcome=outcome,timing=timing,
                         backoff_s=120 if outcome['status']=='deferred-start' else eq.load_config()['stop']['usage_backoff_hours']*3600)
        finally:
            if cap_requested and not pending_cleanup:
                review=outcome['status'] in ('delivered','delivered-unreviewed','needs-dan') or bool(outcome.get('link'))
                subprocess.run([sys.executable,str(b.SHARED/'editcap/editcap.py'),'release',jobid]+(['--review'] if review else []),capture_output=True,timeout=45)
            b.kick(other=True)
    return 0 if outcome['status']!='blocked' else 1
