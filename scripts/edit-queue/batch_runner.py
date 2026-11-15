"""One batch worker. Owns its editcap slot and records an outcome on every ordinary exit."""
import base64
import hashlib
import json
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


def review_verdict(path):
    try:text=Path(path).read_text()
    except FileNotFoundError:return None
    first=text.splitlines()[0].strip().replace('**','') if text.strip() else ''
    for verdict in ('SHIP WITH DISCLOSED UNCERTAINTY','DOES NOT SHIP','SHIP'):
        if first=='VERDICT: '+verdict:
            if verdict=='DOES NOT SHIP' and not (re.search(r'\b\d{1,2}:\d{2}\b',text) and re.search(r'rule|\.md|standard',text,re.I)):
                return None
            return verdict
    return None


def review_link(info):
    """The existing managed review server mirrors M2 pages to the M6 and verifies HTTP."""
    root=Path(info.get('review_root',''));port=info.get('review_port')
    if not root.is_absolute() or not root.is_dir() or not isinstance(port,int) or not (1024<=port<=65535):
        raise ValueError('outcome needs an absolute review_root and review_port from editroute.py free-port')
    run=subprocess.run([sys.executable,str(b.SHARED/'review_server.py'),str(port),str(root)],capture_output=True,text=True,timeout=120)
    if run.returncode:raise RuntimeError('managed review installation/mirror failed: '+(run.stdout+run.stderr)[-600:])
    link='http://127.0.0.1:'+str(port)+'/'
    if b.here()=='m2':
        cmd=['ssh','-oBatchMode=yes','-oConnectTimeout=3','m6','curl -fsS --max-time 5 -o /dev/null '+link]
    else:cmd=['curl','-fsS','--max-time','5','-o','/dev/null',link]
    opened=subprocess.run(cmd,capture_output=True,text=True,timeout=10)
    if opened.returncode:raise RuntimeError('M6 review link did not open')
    return link


def main(claim_path):
    owned=b.read(claim_path);row=owned['row'];name=owned['batch'];k=owned['key'];token=row['claim']['token']
    jobid=row['id'];cfg=eq.load_config();executor=row['executor']
    os.environ.update(EDIT_BATCH_TOKEN=token,GATE_GROUP=jobid,EDIT_BATCH_JOB=jobid)
    fields=dict(pid=os.getpid(),birth=b.identity(os.getpid()),phase='allocating work folder')
    if b.update('heartbeat',name,k,token,fields=fields) is None:
        # No session may start until this owner has confirmed its durable claim.
        b.write(Path(claim_path).parent/'not-started.json',dict(reason='coordinator unavailable before first session'))
        return 1
    stop=threading.Event();has_slot=False;cap_requested=False;wd=None;checkpoint={};edit_h=review_h=0.;started=time.time()
    outcome=dict(status='blocked',reason='runner exited before completing',next_action='Inspect the retained worker log')
    lock=threading.Lock();current=dict(fields)
    def progress(**values):
        with lock:current.update(values);data=dict(current)
        # Local identity survives M6 losing its coordinator connection.
        b.write(Path(claim_path).parent/'progress.json',data)
        return b.update('heartbeat',name,k,token,fields=data)
    def pulse():
        while not stop.wait(b.HEARTBEAT_S):
            if has_slot:
                subprocess.run([sys.executable,str(b.SHARED/'editcap/editcap.py'),'heartbeat',jobid],capture_output=True,timeout=35)
            progress()
    thread=threading.Thread(target=pulse,daemon=True);thread.start()
    def interrupted(signum,frame):raise RuntimeError('runner interrupted by signal '+str(signum))
    signal.signal(signal.SIGTERM,interrupted)
    signal.signal(signal.SIGINT,interrupted)
    def session(ex, prompt, role, timeout):
        def observe(pid,birth):progress(session=dict(pid=pid,birth=birth),phase=role)
        code,tail,hours=r.run_session(ex,cfg,str(wd),prompt,str(wd/'queue-run.log'),role,timeout,session_observer=observe)
        progress(session={},phase=role+' ended')
        return code,tail,hours
    try:
        # Claim and slot are separate: this runner acquires, refreshes and finally releases the slot.
        cap_requested=True
        cap=subprocess.run([sys.executable,str(b.SHARED/'editcap/editcap.py'),'acquire',jobid,'--title',row['title'],'--type',row['kind']],capture_output=True,text=True,timeout=45)
        if cap.returncode!=0:raise RuntimeError('edit slot not acquired: '+(cap.stdout+cap.stderr)[-600:])
        # editcap historically fails open. Confirm the registry actually records this job as active.
        registry=b.read(Path(os.environ.get('EDITCAP_DIR','/tmp/absbyai-editcap'))/'registry.json',{})
        if registry.get('edits',{}).get(jobid,{}).get('state')!='active':raise RuntimeError('editcap did not record an active slot')
        has_slot=True
        work=subprocess.run([sys.executable,str(b.SHARED/'renderq/renderq.py'),'workdir',jobid,'--need',str(row['need_gb'])],capture_output=True,text=True,timeout=45)
        if work.returncode:raise RuntimeError('work folder: '+(work.stdout+work.stderr)[-600:])
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
        job=dict(id=jobid,title=row['title'],size=row['size'],state='ready',file=row.get('jobdoc',''),
                 claude=brief.decode(),codex=brief.decode())
        job['queue_revision']=dict(round=row['round'],words='Execute the copied batch brief exactly')
        packet=r.write_work_packet(job,str(wd),token)
        budget=eq.start_budget(job,cfg,str(wd),token,preserve_renders=bool(row['attempts']>1))
        # Carry elapsed work time forward. Allowance pauses do not get charged as active editing.
        hours_used=float(checkpoint.get('edit_hours',0))
        budget['hours_allowed']=max(0,budget['hours_allowed']-hours_used)
        brief_text=brief.decode()
        instructions=f'''Read AGENTS.md, .claude/skills/_shared/VIDEO-RULES.md, WORK_PACKET.json and BUDGET.json first.
You are the single unattended editor for {row['title']} ({jobid}), round {row['round']}.
Your work folder is {wd}; the runner already holds and heartbeats your edit slot. Use renderq for heavy steps.
Do not use ps to impose the old two-build cap, run editroute wait, acquire/release editcap yourself, or change queue state.
Do not upload, publish, schedule, send messages, change shared scheduling code, or spawn supervisors/reviewers.
Resume existing verified work and provider receipts in this folder. Never repeat a paid request without reconciling its result.
Target: {row['target']}. This is the complete approved scope, with no new review gates.
Keep all actual approval requirements. Headless sessions have no Flow browser. If new AI clips or choices are needed,
prepare the required first-review page and stop with needs-dan, not a claimed full film. Real footage/library first.
Use 1080p review exports. Automated checks stay silent; leave every owner player paused and sound-ready.
On a genuine choice write BATCH-OUTCOME.json with schema 1, token "{token}", status "needs-dan", question,
review_root (absolute managed review folder), review_port (reserved using editroute free-port), and evidence
listing the review file path and sha256. Include the first-review page. Never wait or poll for Dan.
On a technical block write BATCH-OUTCOME.json with token "{token}", status "blocked", reason and next_action.
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
            if r.classify_failure(code,tail,cfg)=='usage_limited':
                outcome=dict(status='paused-for-allowance',reason='editor usage limit');return 0
            marker=b.read(marker_path)
            if not marker or marker.get('token')!=token:raise RuntimeError('editor exited '+str(code)+' without a fresh outcome file')
            if code!=0:raise RuntimeError('editor exited '+str(code)+'; candidate not accepted')
            if marker.get('status')=='blocked':
                outcome=dict(status='blocked',reason=marker['reason'],next_action=marker['next_action']);return 0
            if marker.get('status')=='needs-dan':
                evidence=marker.get('evidence',[])
                if not evidence:raise ValueError('needs-dan has no first-review evidence')
                for file in evidence:
                    if r.sha256(file['path'])!=file['sha256']:raise ValueError('review evidence hash mismatch')
                outcome=dict(status='needs-dan',question=marker['question'],link='http://127.0.0.1:'+str(marker.get('review_port',''))+'/',evidence=evidence)
                try:outcome['link']=review_link(marker)
                except (OSError,RuntimeError,subprocess.SubprocessError):
                    outcome['pending_review']=dict(review_root=marker['review_root'],review_port=marker['review_port'])
                return 0
            if marker.get('status')!='candidate':raise ValueError('invalid editor outcome')
            info=b.read(wd/'DELIVERY.json',{})
            errors=r.validate_delivery(info,str(wd),packet,cfg,'frames_approved' if row.get('assets_approved') else 'ready')
            if errors:raise ValueError('candidate evidence incomplete: '+'; '.join(errors[:6]))
            checkpoint.update(candidate=True,files=[dict(path=f,sha256=r.sha256(f)) for f in info['files']],review_attempts=0)
            b.write(checkpoint_path,checkpoint)
        info=b.read(wd/'DELIVERY.json',{})
        for file in checkpoint['files']:
            if r.sha256(file['path'])!=file['sha256']:raise ValueError('candidate changed after validation')
        link='http://127.0.0.1:'+str(info.get('review_port',''))+'/'
        reviewer=cfg['review']['reviewer_for'][executor]
        verdict=None;reason='reviewer returned no valid verdict';report_path=None
        # A timeout or missing verdict gets one new session. A valid rejection never starts a fix loop.
        for attempt in range(int(checkpoint.get('review_attempts',0)),2):
            checkpoint['review_attempts']=attempt+1;b.write(checkpoint_path,checkpoint)
            report_path=wd/('BATCH-REVIEW-'+str(attempt+1)+'.md')
            prompt=f'''Read AGENTS.md and .claude/skills/_shared/VIDEO-RULES.md. Independently review only the exact
candidate files in {wd}/DELIVERY.json and the scope in {wd}/{k}-BRIEF.md and WORK_PACKET.json.
Do not read editor notes/logs or earlier review reports. Do not edit, render, publish, send, or ask Dan for a new gate.
Use existing checks and silent non-speaker inspection. Do not claim an audible listen from numbers.
Write {report_path}. First line exactly VERDICT: SHIP, VERDICT: DOES NOT SHIP, or
VERDICT: SHIP WITH DISCLOSED UNCERTAINTY. Cite the existing rule and a timestamp for every rejection.
Disclose unsupported checks and genuine uncertainty. Return one consolidated review; no fix loop or additional reviewers.'''
            progress(phase='reviewer')
            code,tail,hours=session(reviewer,prompt,'review-batch-'+str(attempt+1),float(budget['review_hours_allowed']))
            review_h+=hours
            verdict=review_verdict(report_path) if code==0 else None
            if verdict:break
            if r.classify_failure(code,tail,cfg)=='usage_limited':
                checkpoint['review_attempts']=attempt;b.write(checkpoint_path,checkpoint)
                outcome=dict(status='paused-for-allowance',reason='reviewer usage limit');return 0
            reason='reviewer timeout or no valid verdict after '+str(attempt+1)+' attempt(s)'
        if verdict=='DOES NOT SHIP':
            outcome=dict(status='blocked',reason='independent reviewer: DOES NOT SHIP',next_action='Review the cut and consolidated findings; scope a separate revision',link=link,report=str(report_path))
        elif verdict in ('SHIP','SHIP WITH DISCLOSED UNCERTAINTY'):
            outcome=dict(status='delivered',verdict=verdict,link=link,report=str(report_path),files=checkpoint['files'])
        else:outcome=dict(status='delivered-unreviewed',reason=reason,link=link,files=checkpoint['files'])
        try:outcome['link']=review_link(info)
        except (OSError,RuntimeError,subprocess.SubprocessError):
            outcome['pending_review']=dict(review_root=info['review_root'],review_port=info['review_port'])
    except Exception as exc:
        outcome=dict(status='blocked',reason=str(exc),next_action='Inspect retained files and worker log; use batch.py takeover to resume in chat')
    finally:
        stop.set();thread.join(timeout=5)
        try:
            if wd:
                b.write(wd/(k+'-batch-outcome-'+token+'.json'),dict(outcome,token=token,at=time.time()))
            # Retain the exact outcome locally before attempting the M2 link; outbox syncs after reconnect.
            timing=dict(active_hours=edit_h,review_hours=review_h,worker_hours=(time.time()-started)/3600)
            if outcome.get('pending_review'):
                b.write(b.HOME/'outbox'/(token+'.json'),dict(op='outcome',batch=name,key=k,token=token,host=b.here(),outcome=outcome,timing=timing))
                progress(phase='outcome waiting for review mirror',session={})
            else:
                b.update('outcome',name,k,token,outcome=outcome,timing=timing,
                         backoff_s=eq.load_config()['stop']['usage_backoff_hours']*3600)
        finally:
            if cap_requested:
                review=outcome['status'] in ('delivered','delivered-unreviewed','needs-dan') or bool(outcome.get('link'))
                subprocess.run([sys.executable,str(b.SHARED/'editcap/editcap.py'),'release',jobid]+(['--review'] if review else []),capture_output=True,timeout=45)
            b.kick(other=True)
    return 0 if outcome['status']!='blocked' else 1
