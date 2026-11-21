"""November 18 repairs, revised after the Codex Sol High review: start-blocker visibility per Mac, narrow
source check through the real start decision, strict launchd file-access checks, a real fixture worker
launched directly on the M2 with the M6 unreachable, plain blocked rows, holds, reclassification and
episode-based one-shot alerts. Temporary state only."""
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
sys.path.insert(0,str(PKG))
import eq_common as eq
eq.unshadow();b=eq.sibling('batch')


FULL=['create','write','rename','delete']


def passing_probe(home,host='m2',folders=None,request=None):
    b.write(Path(home)/'drive-probe-launchd.json',dict(at=time.time(),host=host,context='launchd',passed=True,request=request,
            interpreter='/usr/bin/python3',folders=folders or [dict(label='Videos to Review',passed=True,steps=FULL,resolved='/x',mounted=True)]))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.home=self.root/'batch';self.home.mkdir()
        self.patches=[]
        def use(x):self.patches.append(x);return x.start()
        self.use=use
        use(patch.object(b,'HOME',self.home));self.here=use(patch.object(b,'here',return_value='m2'))
        # Never reach a real Mac: whichever Mac a test pretends to be, the ledger is this temporary one.
        use(patch.object(b,'rpc',side_effect=lambda op,**v:b.handle(dict(op=op,**v))))
        def no_remote(*a,**k):raise AssertionError('test tried to reach a real Mac')
        use(patch.object(b,'remote',side_effect=no_remote))
        self.cfg=eq.load_config();self.cfg['paused_groups']=[]
        use(patch.object(eq,'load_config',return_value=self.cfg))
        self.notes=[];self.notify_patch=patch.object(b,'notify',side_effect=lambda t,m:(self.notes.append((t,m)),dict(method='test',rc=0))[1]);use(self.notify_patch)
        good=self.root/'vtr';good.mkdir()
        use(patch.dict(os.environ,EDIT_BATCH_PROBE_FOLDERS=json.dumps([dict(label='Videos to Review',path=str(good))])))
    def tearDown(self):
        for x in reversed(self.patches):x.stop()
        self.tmp.cleanup()
    def enqueue(self,name='chat-DS-51-R2',job='DS-51',round_=2,executor='claude',title='3 Ways To Lose Fat',placement='m2'):
        data=b'CONTENT SFC: approved picks.'
        j=dict(id=job,round=round_,title=title,size='S',order=0,kind='SFC',target='review',need_gb=5,executor=executor,
               placement=placement,brief_sha256=hashlib.sha256(data).hexdigest())
        b.handle(dict(op='enqueue',batch=name,jobs=[j],briefs={b.key(j):base64.b64encode(data).decode()},digest='proof'))
        return name,b.key(j)
    def snap(self):return b.handle(dict(op='snapshot'))
    def start(self,name):
        b.handle(dict(op='preflight',proof=dict(passed=True,digest='proof')));return b.handle(dict(op='start',batch=name,digest='proof'))
    def gates(self,**reasons):
        for host in ('m2','m6'):
            b.handle(dict(op='tick',host=host,observation={'_start_block':{'at':time.time(),'reason':reasons.get(host)}}))
    def claim(self,host='m2'):return b.handle(dict(op='claim',host=host,digest='proof',occupied=[],slots=3))


class StartBlockerVisibility(Base):
    def test_queued_with_starts_off_is_the_reports_first_line_with_count_and_reason(self):
        self.enqueue();self.enqueue('chat-WV-07-R1','WV-07',1,title='GAT Upsell 4')
        b.handle(dict(op='preflight',proof=dict(passed=False,at=time.time(),problems=['m6 source differs from pushed main: scripts/edit-queue/batch.py'])))
        b.handle(dict(op='stop'))
        doc=b.report(self.snap())
        first=(self.home/'morning-report.md').read_text().splitlines()[0]
        self.assertTrue(first.startswith('NOT STARTING: 2 queued edits will not start'),first)
        self.assertIn('new starts are switched off since',first)
        self.assertIn('failed: m6 source differs from pushed main: scripts/edit-queue/batch.py',first)
        self.assertIn('GAT Upsell 4 (WV-07 R1)',first)
        self.assertEqual(doc['not_starting']['count'],2);self.assertEqual(doc['alerts'][0],first)
    def test_enqueue_output_says_it_will_not_start_until_it_really_can(self):
        name,_=self.enqueue()
        self.assertTrue(b.startability(name)['start_status'].startswith('WILL NOT START'))
        self.start(name);self.gates()
        self.assertTrue(b.startability(name)['can_start'],b.startability(name))
    def test_enqueue_chat_prints_startability_as_its_last_line(self):
        captured=[]
        with patch.object(b,'enqueue',return_value=dict(registered=True,can_start=False,start_status='WILL NOT START: new starts are switched off.')),\
             patch.object(b,'write'),patch('builtins.print',side_effect=lambda *a,**k:captured.append(' '.join(map(str,a)))),\
             patch.object(sys,'argv',['batch.py','enqueue-chat','DS-51','--brief','/tmp/x.md','--round','2','--title','T','--size','S',
                                      '--kind','SFC','--executor','claude','--need-gb','5','--target','review']):
            self.assertEqual(b.main(),0)
        self.assertEqual(captured[-1],'WILL NOT START: new starts are switched off.')
    def test_nothing_queued_means_no_headline(self):
        self.assertIsNone(b.report(self.snap())['headline'])
    def test_unreachable_coordinator_is_named_in_the_report(self):
        self.enqueue();self.start('chat-DS-51-R2');self.gates()
        doc=b.report(self.snap(),'m2: ssh: connect to host m2 port 22: Operation timed out')
        self.assertIn('could not finish its check with the M2 ledger',doc['headline'])


class PerMacGates(Base):
    """Finding 2: each Mac's start gate reaches the other Mac's report and receipts."""
    def test_m6_view_knows_the_m2_cannot_start_an_m2_job(self):
        name,_=self.enqueue(placement='m2');self.start(name)
        self.gates(m2='the background agent cannot use: Videos to Review (PermissionError: Operation not permitted)')
        self.here.return_value='m6'
        status=b.startability(name)
        self.assertFalse(status['can_start']);self.assertIn('M2: the background agent cannot use: Videos to Review',status['start_status'])
        self.assertIn('NOT STARTING: 1 queued edit',b.report(self.snap())['headline'])
    def test_an_m6_block_does_not_stop_a_healthy_m2_job(self):
        name,_=self.enqueue(placement='m2');self.start(name);self.gates()
        self.here.return_value='m6'
        b.write(self.home/'start-block.json',dict(at=time.time(),start_block='the background agent cannot use: Extreme work folder'))
        self.assertTrue(b.startability(name)['can_start'])
        self.assertIsNone(b.report(dict(self.snap(),start_block='the background agent cannot use: Extreme work folder'))['headline'])
    def test_either_mac_job_needs_only_one_healthy_mac(self):
        name,_=self.enqueue(placement='any');self.start(name)
        self.gates(m6='the background agent cannot use: Videos to Review')
        self.assertTrue(b.startability(name)['can_start'])
        self.gates(m6='x',m2='y')
        self.assertFalse(b.startability(name)['can_start'])
    def test_mixed_batch_counts_only_the_stuck_round(self):
        a,_=self.enqueue('chat-A','DS-51',2,placement='m2');c,_=self.enqueue('chat-B','DS-50',2,placement='m6',title='Sleep')
        self.start(a);self.start(c);self.gates(m6='the background agent cannot use: Videos to Review')
        head=b.report(self.snap())['headline']
        self.assertIn('NOT STARTING: 1 queued edit',head);self.assertIn('Sleep (DS-50 R2)',head);self.assertNotIn('DS-51',head)
    def test_a_silent_mac_counts_as_not_starting(self):
        name,_=self.enqueue(placement='m2');self.start(name)
        b.handle(dict(op='tick',host='m2',observation={'_start_block':{'at':time.time()-1200,'reason':None}}))
        self.here.return_value='m6'
        self.assertIn('has not reported for 20 minutes',b.startability(name)['start_status'])


class SourceCheckThroughTheStartDecision(Base):
    """Finding 11: dirty unrelated files reach the claim; a real scheduler change stops it, by name."""
    def setUp(self):
        super().setUp();root=self.repo=self.root/'repo'
        files={'scripts/edit-queue/batch.py':'print(1)\n','scripts/edit-queue/preamble.md':'schema\n','scripts/edit-queue/README.md':'notes\n',
               'scripts/edit-queue/tests/test_batch.py':'pass\n','scripts/edit-dashboard/desk_records.py':'x=1\n',
               '.claude/skills/_shared/editcap/editcap.py':'y=1\n','.claude/skills/_shared/editcap/selftest.py':'z=1\n',
               '.claude/skills/_shared/renderq/bench10.py':'b=1\n','scripts/edit-queue/scoreboard.json':'{}\n'}
        for name,text in files.items():
            (root/name).parent.mkdir(parents=True,exist_ok=True);(root/name).write_text(text)
        git=lambda *a:subprocess.run(['git',*a],cwd=root,check=True,capture_output=True)
        git('init','-q');git('add','-A');git('-c','user.email=t@t','-c','user.name=t','commit','-qm','x');git('update-ref','refs/remotes/origin/main','HEAD')
        self.use(patch.object(b.eq,'ROOT',str(root)))
        self.launched=[]
        real_run=subprocess.run
        def fake_run(command,**kwargs):
            if 'editcap.py' in ' '.join(map(str,command)):return subprocess.CompletedProcess(command,0,json.dumps(dict(cap=3,in_use=[],renderq={})),'')
            if command and command[0]=='git':return real_run(command,**kwargs)
            return subprocess.CompletedProcess(command,0,'','')
        class Proc:pid=4242
        self.use(patch.object(b.subprocess,'run',side_effect=fake_run))
        real_popen=subprocess.Popen
        def popen(c,**k):
            if c and c[0]=='git':return real_popen(c,**k)
            self.launched.append(c);return Proc()
        self.use(patch.object(b.subprocess,'Popen',side_effect=popen))
        self.use(patch.object(b,'observe_local',return_value={}));self.use(patch.object(b,'identity',return_value='birth'))
        passing_probe(self.home)
        digest=b.fingerprints()['digest']
        name,self.k=self.enqueue();b.handle(dict(op='preflight',proof=dict(passed=True,digest=digest)));b.handle(dict(op='start',batch=name,digest=digest))
    def test_dashboard_docs_and_tests_edits_still_start(self):
        for name in ('scripts/edit-dashboard/desk_records.py','scripts/edit-queue/README.md','scripts/edit-queue/tests/test_batch.py',
                     '.claude/skills/_shared/editcap/selftest.py','.claude/skills/_shared/renderq/bench10.py','scripts/edit-queue/scoreboard.json'):
            (self.repo/name).write_text('another session is editing this\n')
        b.tick()
        self.assertEqual(len(self.launched),1)
        self.assertEqual(self.snap()['batches']['chat-DS-51-R2']['jobs'][self.k]['status'],'claimed')
    def test_real_scheduler_change_blocks_and_is_named(self):
        (self.repo/'.claude/skills/_shared/editcap/editcap.py').write_text('y=2\n')
        (self.repo/'scripts/edit-queue/preamble.md').write_text('changed prompt\n')
        b.tick()
        self.assertEqual(self.launched,[])
        first=(self.home/'morning-report.md').read_text().splitlines()[0]
        self.assertIn('M2: installed source differs from pushed main: .claude/skills/_shared/editcap/editcap.py, scripts/edit-queue/preamble.md',first)


class BackgroundFileAccess(Base):
    """Findings 1, 3, 4 and the verification round's probe defects."""
    def folders(self,*items):return [('f'+str(i),Path(x),True,False) for i,x in enumerate(items)]
    def good(self,request=None):
        passing_probe(self.home,request=request)
    def test_probe_uses_a_per_mac_folder_and_clears_only_its_own_files(self):
        a=self.root/'Videos to Review';a.mkdir();box=a/(b.PROBE_DIR+'-m2');box.mkdir();(box/'probe.txt').write_text('old')
        link=self.root/'linked';link.symlink_to(a)
        [r]=b.drive_probe(self.folders(link))
        self.assertTrue(r['passed']);self.assertEqual(r['steps'],FULL)
        self.assertEqual(r['cleared_leftovers'],[str(a.resolve()/(b.PROBE_DIR+'-m2')/'probe.txt')]);self.assertEqual(list(a.iterdir()),[])
    def test_unrelated_files_in_the_probe_folder_are_never_removed(self):
        a=self.root/'Videos to Review';a.mkdir();box=a/(b.PROBE_DIR+'-m2');box.mkdir();(box/'review.mp4').write_text('keep')
        [r]=b.drive_probe(self.folders(a))
        self.assertFalse(r['passed']);self.assertEqual((box/'review.mp4').read_text(),'keep')
    def test_probe_folder_that_is_a_link_is_refused(self):
        a=self.root/'Videos to Review';a.mkdir();elsewhere=self.root/'reviews';elsewhere.mkdir();(elsewhere/'probe.txt').write_text('keep')
        (a/(b.PROBE_DIR+'-m2')).symlink_to(elsewhere)
        [r]=b.drive_probe(self.folders(a))
        self.assertFalse(r['passed']);self.assertIn('is a link',r['error']);self.assertEqual((elsewhere/'probe.txt').read_text(),'keep')
    def test_two_macs_never_share_a_probe_folder(self):
        a=self.root/'shared';a.mkdir()
        self.assertTrue(b.drive_probe(self.folders(a),host='m6')[0]['passed']);self.assertTrue(b.drive_probe(self.folders(a),host='m2')[0]['passed'])
    def test_denied_folder_fails_by_label(self):
        locked=self.root/'locked';locked.mkdir();locked.chmod(0o500)
        try:[r]=b.drive_probe(self.folders(locked))
        finally:locked.chmod(0o700)
        self.assertFalse(r['passed']);self.assertEqual(r['error'],'PermissionError: Permission denied')
    def test_missing_root_is_created_where_the_allocator_would(self):
        root=self.root/'internal/_edit_work'
        [r]=b.drive_probe([('internal work folder',root,True,True)])
        self.assertTrue(r['passed']);self.assertTrue(root.is_dir())
    def test_unmounted_volume_is_skipped_and_never_counts_as_tested(self):
        stale=self.root/'Volumes/Extreme/_edit_work';stale.mkdir(parents=True)
        with patch.object(b,'volume_root',return_value=str(self.root/'Volumes/Extreme')):
            [r]=b.drive_probe([('Videos to Review',stale,True,True)])
        self.assertFalse(r['passed']);self.assertTrue(r['skipped']);self.assertIn('drive not mounted',r['error'])
        # Even a record claiming passed without the four steps on a mounted volume does not satisfy status.
        passing_probe(self.home,folders=[dict(label='Videos to Review',passed=True,mounted=False,steps=[],resolved=str(stale))])
        self.assertIn('not fully tested',b.launchd_probe_status()['problem'])
    def test_status_never_touches_the_drives(self):
        self.good()
        with patch.object(b.os.path,'ismount',side_effect=AssertionError('touched a mount')),\
             patch.object(b.os.path,'realpath',side_effect=AssertionError('touched a path')):
            self.assertTrue(b.launchd_probe_status()['ok'])
    def test_launchd_context_records_and_interactive_does_not_count(self):
        with patch.dict(os.environ,XPC_SERVICE_NAME='application.com.apple.Terminal'):self.assertIsNone(b.maybe_probe())
        self.assertFalse(b.launchd_probe_status()['ok'])
        with patch.dict(os.environ,XPC_SERVICE_NAME=b.AGENT_LABEL):doc=b.maybe_probe()
        self.assertEqual(doc['context'],'launchd');self.assertTrue(doc['passed'],doc);self.assertTrue(b.launchd_probe_status()['ok'])
    def test_answered_request_is_not_rerun_by_the_timed_check(self):
        b.write(self.home/'drive-probe-request.json',dict(id='A',at=time.time()))
        with patch.dict(os.environ,XPC_SERVICE_NAME=b.AGENT_LABEL):
            self.assertEqual(b.maybe_probe()['request'],'A')
            d=b.read(self.home/'drive-probe-launchd.json');d['at']-=b.PROBE_EVERY_S+5;b.write(self.home/'drive-probe-launchd.json',d)
            self.assertEqual(b.maybe_probe()['request'],'A')            # timed check keeps the answered id
            self.assertIsNone(b.maybe_probe())                          # and does not treat A as pending again
    def test_cached_pass_with_no_answer_to_a_fresh_request_fails(self):
        self.good(request='old')
        self.assertIn('did not answer a fresh',b.launchd_probe_status(request_id='new')['problem'])
        self.assertTrue(b.launchd_probe_status(request_id='old')['ok'])
    def test_empty_or_incomplete_records_fail(self):
        b.write(self.home/'drive-probe-launchd.json',dict(at=time.time(),passed=False,folders=[]))
        self.assertFalse(b.launchd_probe_status()['ok'])
        passing_probe(self.home,folders=[dict(label='Extreme work folder',passed=True,steps=FULL,resolved='/x')])
        self.assertIn('Videos to Review (not checked by the background agent)',b.launchd_probe_status()['problem'])
    def test_extreme_is_required_by_default(self):
        with patch.dict(os.environ,{},clear=False):
            os.environ.pop('EDIT_BATCH_PROBE_FOLDERS',None)
            passing_probe(self.home,folders=[dict(label=l,passed=True,steps=FULL,resolved='/x') for l in ('Videos to Review','internal work folder')])
            self.assertIn('Extreme work folder (not checked',b.launchd_probe_status()['problem'])
    def test_preflight_fails_when_a_mac_does_not_answer(self):
        self.good(request='old')
        remote=dict(host='m6',dirty=[],launcher_ok=True,canary=dict(passed=True,rows=[1,2,3,4]),hashes={},digest='d',commit='c',drive_probe=dict(ok=True))
        local=dict(remote,host='m2',drive_probe=b.launchd_probe_status(request_id='fresh'))
        with patch.object(b,'fingerprints',return_value=local),patch.object(b,'remote',return_value=remote):
            proof=b.preflight()
        self.assertFalse(proof['passed']);self.assertIn('m2 the background agent did not answer a fresh file-access check',proof['problems'])
    def test_hung_probe_times_out_and_fails(self):
        real=subprocess.Popen
        with patch.object(b,'PROBE_TIMEOUT_S',1),patch.object(b.subprocess,'Popen',side_effect=lambda c,**k:real(['/bin/sleep','30'],**k)):
            doc=b.record_probe('launchd')
        self.assertFalse(doc['passed']);self.assertIn('timed out after 1 s',doc['folders'][0]['error'])
        self.assertIn('all folders',b.launchd_probe_status()['problem'])
    def test_real_probe_child_runs_under_a_deadline(self):
        doc=b.record_probe('launchd')
        self.assertTrue(doc['passed'],doc);self.assertEqual(doc['folders'][0]['steps'],FULL)
    def test_stale_probe_is_refused(self):
        self.good();d=b.read(self.home/'drive-probe-launchd.json');d['at']-=7*3600;b.write(self.home/'drive-probe-launchd.json',d)
        self.assertIn('older than six hours',b.launchd_probe_status()['problem'])


FIXTURE_WORKER='''import json,os,subprocess,sys,time
sys.path.insert(0,sys.argv[1]);import eq_common as eq;eq.unshadow();b=eq.sibling('batch')
b.kick=lambda other=False:None          # never touch a real LaunchAgent from a test
owned=b.read(sys.argv[2]);row=owned['row'];token=row['claim']['token']
assert b.update('heartbeat',owned['batch'],owned['key'],token,fields=dict(pid=os.getpid(),birth=b.identity(os.getpid()),phase='fixture editing'))
first=subprocess.run(['ssh','m6','true']).returncode       # M6 connected at the start
open(sys.argv[3],'w').close()                                # ... then the M6 drops mid-job
time.sleep(.5)
second=subprocess.run(['ssh','m6','true']).returncode
assert (first,second)==(0,255),(first,second)
b.update('outcome',owned['batch'],owned['key'],token,outcome=dict(status='delivered',verdict='SHIP',link='http://127.0.0.1:9850/'),timing={})
'''


class RealFixtureWorkerOnM2(Base):
    """Finding 11: a real child process, launched directly by a real M2 tick, starts and finishes with the M6 unreachable."""
    def test_m2_fixture_job_starts_and_finishes_with_the_m6_unreachable(self):
        bin_=self.root/'bin';bin_.mkdir();log=self.root/'ssh-calls.log'
        drop=self.root/'m6-dropped'
        (bin_/'ssh').write_text('#!/bin/sh\necho "$@" >> '+str(log)+'\n[ -e '+str(drop)+' ] || exit 0\necho "ssh: connect to host m6: Operation timed out" >&2\nexit 255\n');(bin_/'ssh').chmod(0o755)
        script=self.root/'fixture_worker.py';script.write_text(FIXTURE_WORKER)
        env={'PATH':str(bin_)+':'+os.environ['PATH'],'EDIT_BATCH_HOME':str(self.home),'EDITROUTE_HOST':'m2'}
        self.use(patch.dict(os.environ,env))
        self.use(patch.object(b,'worker_command',side_effect=lambda claim:([sys.executable,'-B',str(script),str(PKG),str(claim),str(drop)],False)))
        real_run=subprocess.run
        def fake_run(command,**kwargs):
            if 'editcap.py' in ' '.join(map(str,command)):return subprocess.CompletedProcess(command,0,json.dumps(dict(cap=3,in_use=[],renderq={})),'')
            return real_run(command,**kwargs)
        self.use(patch.object(b.subprocess,'run',side_effect=fake_run))
        self.use(patch.object(b,'fingerprints',return_value=dict(host='m2',dirty=[],digest='proof',hashes={},launcher_ok=True,canary={},commit='c')))
        self.use(patch.object(b,'observe_local',return_value={}))
        passing_probe(self.home)
        name,k=self.enqueue(placement='m2');self.start(name)
        b.tick()
        deadline=time.time()+20
        while time.time()<deadline and self.snap()['batches'][name]['jobs'][k]['status']!='delivered':time.sleep(.2)
        row=self.snap()['batches'][name]['jobs'][k]
        self.assertEqual(row['status'],'delivered',row)
        calls=log.read_text() if log.exists() else ''
        self.assertNotIn('runner.py',calls)                # no launch through any other Mac
        self.assertEqual(calls.count('m6 true'),2)         # connected, then dropped mid-job; the worker carried on


class BlockedRowsAndDecisions(Base):
    def test_blocked_rows_name_an_owner_and_plain_next_action(self):
        name,k=self.enqueue(executor='codex',title='Real Exercise Demos Batch 5',job='REALDEMOS-B05',round_=1);self.start(name)
        c=self.claim()
        for _ in range(2):
            b.handle(dict(op='recover',batch=name,key=k,token=c['row']['claim']['token'],host='m2',pid_alive=False,spawn_failed=True))
            if self.snap()['batches'][name]['jobs'][k]['status']=='queued':c=self.claim()
        row=self.snap()['batches'][name]['jobs'][k]
        self.assertEqual(row['status'],'blocked');self.assertEqual(row['outcome']['owner'],'Codex')
        self.assertIn('Open a new Codex chat for Real Exercise Demos Batch 5 (REALDEMOS-B05 R1)',row['outcome']['next_action'])
        b.report(self.snap())
        line=[x for x in (self.home/'morning-report.md').read_text().splitlines() if 'REALDEMOS' in x][0]
        self.assertIn('NEXT (Codex): Open a new Codex chat',line)
    def test_third_start_failure_gives_a_takeover_that_really_resumes(self):
        name,k=self.enqueue();self.start(name)
        for _ in range(3):
            c=self.claim()
            b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',backoff_s=0,
                          outcome=dict(status='deferred-start',reason='executor missing',retry_kind='executor')))
            c2=b.control();c2.pop('host_backoff',None);b.write(self.home/'control.json',c2)
        row=self.snap()['batches'][name]['jobs'][k]
        self.assertEqual(row['status'],'blocked');self.assertIn('batch.py takeover DS-51',row['outcome']['next_action'])
        self.assertEqual(b.handle(dict(op='takeover',job='DS-51',host='m6'))['status'],'blocked')
    def test_needs_dan_report_shows_the_exact_finding_and_choices(self):
        name,k=self.enqueue('chat-DS-106-R2','DS-106',2,title='Protein Snack Can');self.start(name);c=self.claim()
        b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',
                      outcome=dict(status='blocked',reason='early decay 83 ms vs 80',next_action='Decide the audio standard')))
        row=b.handle(dict(op='reclassify',batch=name,key=k,why='handoff item 5',
                          outcome=dict(status='needs-dan',question='Hold for another audio pass?',link='http://127.0.0.1:9814/',
                                       finding='early decay 83 ms vs 80',choices=['Hold for another audio pass'])))
        self.assertEqual(row['status'],'needs-dan');self.assertEqual(row['prior_outcome']['reason'],'early decay 83 ms vs 80')
        b.report(self.snap())
        text=(self.home/'morning-report.md').read_text()
        self.assertIn('Finding: early decay 83 ms vs 80',text);self.assertIn('Choices: Hold for another audio pass',text)
        with self.assertRaises(ValueError):
            b.handle(dict(op='reclassify',batch=name,key=k,outcome=dict(status='needs-dan',question='q',link='l')))
    def test_held_round_never_starts_and_is_not_counted_as_waiting(self):
        name,k=self.enqueue();self.start(name);self.gates()
        b.handle(dict(op='hold',batch=name,key=k,reason='Dan paused DS-51 R2 on Nov 17'))
        self.assertIsNone(self.claim())
        self.assertIsNone(b.report(self.snap())['headline']);self.assertIn('Dan paused DS-51 R2',(self.home/'morning-report.md').read_text())
        b.handle(dict(op='unhold',batch=name,key=k))
        self.assertEqual(self.claim()['row']['id'],'DS-51')


class EpisodeAlerts(Base):
    """Findings 9 and 10."""
    def setUp(self):
        super().setUp();self.here.return_value='m6'
        b.write(self.home/'alerts.json',dict(created=time.time(),events={},episodes={}))
    def test_once_per_episode_recorded_and_wording_drift_does_not_ring(self):
        self.enqueue();b.handle(dict(op='stop'))
        b.report(self.snap());b.report(self.snap())
        b.handle(dict(op='preflight',proof=dict(passed=False,at=time.time(),problems=['probe file 1234'])));b.report(self.snap())
        self.assertEqual(len(self.notes),1);self.assertIn('DS-51 R2 WILL NOT START (3 Ways To Lose Fat)',self.notes[0][1])
        [event]=[e for e in b.read(self.home/'alerts.json')['events'].values()]
        self.assertTrue(event['sent']);self.assertIn('not verifiable',event['screen_delivery'])
    def test_clear_and_recur_rings_again(self):
        name,_=self.enqueue();b.handle(dict(op='stop'));b.report(self.snap())
        self.start(name);self.gates();b.report(self.snap())
        b.handle(dict(op='stop'));b.report(self.snap())
        self.assertEqual(len(self.notes),2)
    def test_partial_resolution_does_not_ring(self):
        a,ka=self.enqueue('chat-A','DS-51');self.enqueue('chat-B','DS-50',title='Sleep');b.handle(dict(op='stop'));b.report(self.snap())
        b.handle(dict(op='hold',batch=a,key=ka,reason='Dan paused it'));b.report(self.snap())
        self.assertEqual(len(self.notes),1)
    def test_new_decision_rings_and_old_rows_before_rollout_do_not(self):
        name,k=self.enqueue();self.start(name);self.gates();c=self.claim()
        b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',
                      outcome=dict(status='needs-dan',question='Approve?',link='http://127.0.0.1:9809/')))
        with patch.object(b,'ROLLOUT_AT',time.time()+60):b.report(self.snap())
        self.assertEqual(self.notes,[])
        b.write(self.home/'alerts.json',dict(created=time.time(),events={},episodes={}))
        b.report(self.snap());b.report(self.snap())
        self.assertEqual(len(self.notes),1);self.assertIn('DS-51 R2 NEEDS YOU',self.notes[0][1])
    def test_long_messages_record_only_what_was_shown(self):
        for i in range(6):self.enqueue('chat-X'+str(i),'DS-'+str(60+i),title='A rather long recognizable video title number '+str(i))
        b.handle(dict(op='stop'));result=b.report(self.snap())['alert']
        self.assertGreater(result['waiting'],0)
        state=b.read(self.home/'alerts.json');sent=[e for e in state['events'].values() if e.get('sent')]
        self.assertEqual(len(sent),result['sent'])
        for e in sent:self.assertIn(e['text'],self.notes[0][1])
        b.report(self.snap());self.assertEqual(len(self.notes),2)
    def test_failed_notification_retries_at_most_three_times(self):
        self.notify_patch.stop();self.patches.remove(self.notify_patch);calls=[]
        with patch.object(b,'notify',side_effect=lambda t,m:(calls.append(1),dict(method='test',rc=1,stderr='no'))[1]):
            self.enqueue();b.handle(dict(op='stop'))
            for _ in range(5):b.report(self.snap())
        self.assertEqual(len(calls),3)
    def test_m2_never_sends(self):
        self.here.return_value='m2';self.enqueue();b.handle(dict(op='stop'));b.report(self.snap())
        self.assertEqual(self.notes,[])
    def test_migration_does_not_reannounce_current_rows(self):
        b.write(self.home/'alerts.json',dict(created=time.time(),events={}))
        self.enqueue();b.handle(dict(op='stop'));b.report(self.snap())
        self.assertEqual(self.notes,[])


class VerificationRoundFixes(Base):
    def test_coordinator_unreachable_is_global_but_a_local_fault_is_only_this_mac(self):
        a,_=self.enqueue('chat-A','DS-51',2,placement='m2');c,_=self.enqueue('chat-B','DS-50',2,placement='m6',title='Sleep')
        self.start(a);self.start(c);self.gates();b.save_snapshot(self.snap())
        self.here.return_value='m6'
        with patch.object(b,'maybe_probe'),patch.object(b,'flush_outbox'),patch.object(b,'fingerprints',return_value=dict(dirty=[],digest='proof')),\
             patch.object(b,'observe_local',side_effect=subprocess.TimeoutExpired('editcap',30)):
            doc=b.tick()
        self.assertIn('Sleep (DS-50 R2)',doc['headline']);self.assertNotIn('DS-51',doc['headline'])
        self.assertIn("M6: this Mac's last check failed",doc['headline'])
        with patch.object(b,'maybe_probe'),patch.object(b,'flush_outbox'),patch.object(b,'fingerprints',return_value=dict(dirty=[],digest='proof')),\
             patch.object(b,'observe_local',return_value={}),patch.object(b,'rpc',side_effect=b.CoordinatorUnreachable('ssh timed out')):
            doc=b.tick()
        self.assertIn('M2 ledger unreachable',doc['headline']);self.assertIn('DS-51',doc['headline'])
    def test_takeover_action_names_the_exact_round(self):
        name,k=self.enqueue();self.start(name)
        for _ in range(3):
            c=self.claim()
            b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',backoff_s=0,
                          outcome=dict(status='deferred-start',reason='executor missing',retry_kind='executor')))
            c2=b.control();c2.pop('host_backoff',None);b.write(self.home/'control.json',c2)
        self.enqueue('chat-DS-51-R3','DS-51',3)
        row=self.snap()['batches'][name]['jobs'][k]
        self.assertIn('batch.py takeover DS-51 --round 2',row['outcome']['next_action'])
        self.assertEqual(b.handle(dict(op='takeover',job='DS-51',round=2,host='m6'))['round'],2)
    def test_finished_batch_is_not_reported_as_queued(self):
        name,k=self.enqueue();self.start(name);self.gates();c=self.claim()
        b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',outcome=dict(status='delivered',link='l')))
        status=b.startability(name)
        self.assertFalse(status['can_start']);self.assertEqual(status['start_status'],'NOT WAITING: DS-51 R2 DELIVERED.')
        self.assertNotEqual(b.receipt(name)['receipt'],'queued')
    def test_paused_group_is_counted_as_not_starting(self):
        name,_=self.enqueue();self.start(name);self.gates()
        self.cfg['paused_groups']=[dict(group=eq.group_of('DS-51'),executor='claude',reason='circuit breaker test')]
        self.assertIn('paused group (circuit breaker test)',b.startability(name)['start_status'])
    def test_allowance_wait_says_it_will_start_later(self):
        name,k=self.enqueue();self.start(name);self.gates()
        c=b.control();c['executor_backoff']={'claude':dict(until=time.time()+3600,reason='limit')};b.write(self.home/'control.json',c)
        self.assertTrue(b.startability(name)['start_status'].startswith('CAN START LATER: DS-51 R2 after'))
    def test_fresh_alert_ledger_rings_the_first_live_incident(self):
        self.here.return_value='m6';self.enqueue();b.handle(dict(op='stop'));b.report(self.snap())
        self.assertEqual(len(self.notes),1);self.assertTrue(self.notes[0][1].startswith('DS-51 R2 WILL NOT START'))


class DeskFallback(Base):
    def test_m6_desk_card_shows_the_alert_lines_and_a_report_link(self):
        sys.path.insert(0,str(PKG.parent/'edit-dashboard'))
        import observe
        home=self.root/'home';(home/'.absbyai-batch').mkdir(parents=True)
        self.enqueue();b.handle(dict(op='stop'))
        (home/'.absbyai-batch'/'morning-report.json').write_text(json.dumps(b.report(self.snap())))
        out=observe.observe('m6',repo=self.root/'repo',tmp=self.root,home=home)
        self.assertTrue(out['alerts'][0].startswith('NOT STARTING: 1 queued edit'))
        self.assertNotIn('NOT STARTING',' '.join(out['issues']))
        desk=PKG.parent/'edit-dashboard'
        self.assertIn("a.href='/batch-report'",(desk/'app.js').read_text())
        self.assertIn("self.path=='/batch-report'",(desk/'server.py').read_text())


if __name__=='__main__':unittest.main()
