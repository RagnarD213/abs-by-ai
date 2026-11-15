"""Worker outcomes and actual process-interruption cleanup. No model calls or real media."""
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

PKG=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PKG));import eq_common as eq
eq.unshadow();b=eq.sibling('batch');w=eq.sibling('batch_runner');r=eq.sibling('runner')

class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.home=self.root/'home';self.home.mkdir()
        self.wd=self.root/'work';self.wd.mkdir();self.review=self.wd/'review';self.review.mkdir()
        self.video=self.wd/'final.mp4';self.video.write_bytes(b'candidate bytes')
        self.cap=self.root/'cap';self.cap.mkdir();self.released=0;self.sessions=[];self.mode='clean';self.capacity_code=0
        self.patches=[]
        def use(p):self.patches.append(p);return p.start()
        use(patch.object(b,'HOME',self.home));use(patch.object(b,'here',return_value='m2'))
        use(patch.dict(os.environ,EDITCAP_DIR=str(self.cap)))
        self.cfg=eq.load_config();use(patch.object(eq,'load_config',return_value=self.cfg));use(patch.object(eq,'resolve_binary',return_value='/bin/echo'))
        brief=b'CONTENT. Reuse exact approved input.'
        job=dict(id='SL-36',round=1,title='Man Boobs Shorts',size='S',order=0,kind='SFL',executor='claude',need_gb=1,target='approved candidate',placement='m2',brief_sha256=hashlib.sha256(brief).hexdigest())
        b.handle(dict(op='enqueue',batch='worker-test',jobs=[job],briefs={'SL-36-R1':base64.b64encode(brief).decode()}))
        b.handle(dict(op='preflight',proof={'passed':True,'digest':'test'}));b.handle(dict(op='start',batch='worker-test',digest='test'))
        self.claim=b.handle(dict(op='claim',host='m2',digest='test',occupied=[],slots=1));self.token=self.claim['row']['claim']['token']
        self.claim_path=self.home/'runs'/self.token/'claim.json';b.write(self.claim_path,self.claim)
        use(patch.object(w.subprocess,'Popen'))
        use(patch.object(w.subprocess,'run',side_effect=self.fake_command))
        use(patch.object(w.signal,'signal'))
        use(patch.object(b,'kick'))
        use(patch.object(w,'review_link',return_value='http://127.0.0.1:9850/'))
        use(patch.object(w,'candidate_stamps'))
        use(patch.object(r,'write_work_packet',return_value={'revision_number':1}))
        use(patch.object(r,'validate_delivery',return_value=[]))
        use(patch.object(r,'run_session',side_effect=self.fake_session))
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.temp.cleanup()
    def fake_command(self,command,**kwargs):
        if 'editcap.py' in str(command):
            if 'acquire' in command:
                if self.capacity_code:return subprocess.CompletedProcess(command,self.capacity_code,'waiting','')
                b.write(self.cap/'registry.json',{'version':1,'edits':{'SL-36':{'state':'active'}}})
            if 'release' in command:self.released+=1
            return subprocess.CompletedProcess(command,0,'','')
        if 'workdir' in command:
            if self.mode=='storage':return subprocess.CompletedProcess(command,1,'','storage temporarily full')
            return subprocess.CompletedProcess(command,0,str(self.wd)+'\n','')
        return subprocess.CompletedProcess(command,0,'','')
    def fake_session(self,executor,cfg,wd,prompt,log,role,timeout,**kwargs):
        self.sessions.append((executor,role))
        if role=='batch-editor':
            if self.mode=='interrupted':raise r.SessionInterrupted('signal test')
            if self.mode=='cleanup':raise r.SessionCleanupFailed('session still alive')
            if self.mode=='missing':return 0,'normal exit',.01
            if self.mode=='allowance':return 1,'usage limit',.01
            info=dict(files=[str(self.video)],review_copy=str(self.video),review_root=str(self.review),review_port=9850)
            if self.mode=='bad-link':info.pop('review_root')
            b.write(self.wd/'DELIVERY.json',info)
            b.write(self.wd/'BATCH-OUTCOME.json',{'token':self.token,'status':'candidate'})
            return 0,'Example note: rate limit was handled; session limit is discussed in the script',.01
        if self.mode in ('no-verdict','timeout'):
            return (r.BUDGET_EXCEEDED_CODE if self.mode=='timeout' else 0),'no report',.01
        report=Path(prompt.split('Write ',1)[1].split('. First line',1)[0])
        digest=r.sha256(self.video)
        verdict='DOES NOT SHIP' if self.mode in ('reject','uncited','unbound-reject') else 'SHIP'
        text='VERDICT: '+verdict+'\nCandidate SHA-256: '+digest+'\n'
        if self.mode=='unbound-reject':text='VERDICT: DOES NOT SHIP\n0:12, rule VIDEO-RULES.md: clipped head.'
        if self.mode=='reject':text+='0:12, rule VIDEO-RULES.md: head is clipped.\n'
        report.write_text(text)
        if self.mode=='changed':self.video.write_bytes(b'changed after review')
        return 0,'rate limit mentioned in final notes',.01
    def execute(self):
        code=w.main(str(self.claim_path));row=b.handle({'op':'snapshot'})['batches']['worker-test']['jobs']['SL-36-R1']
        return code,row
    def test_successful_candidate_is_not_mistaken_for_allowance_failure(self):
        code,row=self.execute();self.assertEqual(row['status'],'delivered');self.assertEqual(len(self.sessions),2);self.assertEqual(self.released,1)
    def test_old_review_cannot_ship_a_new_candidate_without_a_verdict(self):
        (self.wd/'BATCH-REVIEW-1.md').write_text('VERDICT: SHIP\nold candidate')
        self.mode='no-verdict';_,row=self.execute();self.assertEqual(row['status'],'delivered-unreviewed');self.assertEqual(len(self.sessions),3)
    def test_reviewer_timeout_gets_only_one_retry(self):
        self.mode='timeout';_,row=self.execute();self.assertEqual(row['status'],'delivered-unreviewed');self.assertEqual(len(self.sessions),3)
    def test_uncited_rejection_does_not_get_a_second_opinion(self):
        self.mode='uncited';_,row=self.execute();self.assertEqual(row['status'],'delivered-unreviewed');self.assertEqual(len(self.sessions),2);self.assertIn('rejected without',row['outcome']['reason'])
    def test_rejection_missing_candidate_identity_is_not_a_second_opinion(self):
        self.mode='unbound-reject';_,row=self.execute();self.assertEqual(row['status'],'delivered-unreviewed');self.assertEqual(len(self.sessions),2)
    def test_valid_rejection_parks_without_a_fix_loop(self):
        self.mode='reject';_,row=self.execute();self.assertEqual(row['status'],'blocked');self.assertEqual(len(self.sessions),2)
    def test_temporary_slot_wait_is_queued_and_releases_registration(self):
        self.capacity_code=3;_,row=self.execute();self.assertEqual(row['status'],'queued');self.assertEqual(self.sessions,[]);self.assertEqual(self.released,1)
    def test_temporary_storage_shortage_is_queued(self):
        self.mode='storage';_,row=self.execute();self.assertEqual(row['status'],'queued');self.assertEqual(self.sessions,[]);self.assertEqual(self.released,1)
    def test_missing_outcome_is_a_failure_even_on_exit_zero(self):
        self.mode='missing';_,row=self.execute();self.assertEqual(row['status'],'blocked');self.assertIn('fresh outcome',row['outcome']['reason'])
    def test_interruption_never_becomes_an_allowance_pause(self):
        self.mode='interrupted';_,row=self.execute();self.assertEqual(row['status'],'blocked');self.assertIn('signal test',row['outcome']['reason']);self.assertEqual(self.released,1)
    def test_unconfirmed_session_cleanup_retains_claim_and_slot(self):
        self.mode='cleanup';_,row=self.execute();self.assertEqual(row['status'],'claimed');self.assertEqual(self.released,0)
    def test_allowance_pause_is_shared_and_keeps_original_folder(self):
        self.mode='allowance';_,row=self.execute();self.assertEqual(row['status'],'queued');self.assertEqual(row['workdir'],str(self.wd));self.assertIn('claude',b.control()['executor_backoff'])
    def test_invalid_review_location_does_not_spend_a_reviewer(self):
        self.mode='bad-link';_,row=self.execute();self.assertEqual(row['status'],'blocked');self.assertEqual(len(self.sessions),1)
    def test_heartbeat_errors_do_not_kill_the_pulse_thread(self):
        original_command=self.fake_command;original_session=self.fake_session;beats=[]
        def command(args,**kwargs):
            if 'heartbeat' in args:
                beats.append(1)
                if len(beats)<3:raise subprocess.TimeoutExpired(args,35)
            return original_command(args,**kwargs)
        def session(*args,**kwargs):
            if args[5]=='batch-editor':time.sleep(.08)
            return original_session(*args,**kwargs)
        with patch.object(b,'HEARTBEAT_S',.005),patch.object(w.subprocess,'run',side_effect=command),patch.object(r,'run_session',side_effect=session):
            _,row=self.execute()
        self.assertEqual(row['status'],'delivered');self.assertGreaterEqual(len(beats),3)
    def test_candidate_changed_during_review_cannot_be_delivered(self):
        self.mode='changed';_,row=self.execute();self.assertEqual(row['status'],'blocked');self.assertIn('changed during review',row['outcome']['reason'])

class RealSessionCleanup(unittest.TestCase):
    def test_sigterm_stops_the_real_fake_executor_process_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            script=Path(tmp)/'interrupt.py'
            script.write_text('''import sys,os,json,signal,threading,time,subprocess
from pathlib import Path
sys.path.insert(0,sys.argv[1]);import eq_common as eq;eq.unshadow();r=eq.sibling('runner')
root=Path(sys.argv[2]);seen=[]
eq.build_command=lambda *a,**k:['/bin/sh','-c','echo rate limit; sleep 30']
def stop(s,f):raise r.SessionInterrupted('signal')
signal.signal(signal.SIGTERM,stop)
threading.Timer(.5,lambda:os.kill(os.getpid(),signal.SIGTERM)).start()
try:r.run_session('claude',{},str(root),'test',str(root/'log'),'test',1,session_observer=lambda pid,birth:seen.append(pid))
except r.SessionInterrupted:pass
else:raise AssertionError('interruption was swallowed')
assert seen
states=subprocess.check_output(['/bin/ps','-axo','pgid=,stat='],text=True)
assert not any(int(p[0])==seen[0] and not p[1].startswith('Z') for line in states.splitlines() if len(p:=line.split())>=2),seen
print('session group stopped and interruption propagated')
''')
            run=subprocess.run([sys.executable,str(script),str(PKG),tmp],capture_output=True,text=True,timeout=20)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)

if __name__=='__main__':unittest.main()
