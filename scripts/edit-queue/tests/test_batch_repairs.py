"""November 18 repairs: start-blocker visibility, narrow source check, background file access, direct M2
launch with the M6 gone, plain blocked rows, holds, reclassification and one-shot alerts. Temporary state only."""
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


def passing_probe(home,host='m2'):
    b.write(Path(home)/'drive-probe-launchd.json',dict(at=time.time(),host=host,context='launchd',passed=True,
            interpreter='/usr/bin/python3',folders=[dict(label='Videos to Review',passed=True)]))


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.home=Path(self.tmp.name)/'batch';self.home.mkdir()
        self.patches=[]
        def use(x):self.patches.append(x);return x.start()
        use(patch.object(b,'HOME',self.home));self.here=use(patch.object(b,'here',return_value='m2'))
        self.cfg=eq.load_config();self.cfg['paused_groups']=[]
        use(patch.object(eq,'load_config',return_value=self.cfg))
        self.notes=[];use(patch.object(b,'notify',side_effect=lambda t,m:(self.notes.append((t,m)),dict(method='test',rc=0))[1]))
    def tearDown(self):
        for x in reversed(self.patches):x.stop()
        self.tmp.cleanup()
    def enqueue(self,name='chat-DS-51-R2',job='DS-51',round_=2,executor='claude',title='3 Ways To Lose Fat'):
        data=b'CONTENT SFC: approved picks.'
        j=dict(id=job,round=round_,title=title,size='S',order=0,kind='SFC',target='review',need_gb=5,executor=executor,
               placement='m2',brief_sha256=hashlib.sha256(data).hexdigest())
        b.handle(dict(op='enqueue',batch=name,jobs=[j],briefs={b.key(j):base64.b64encode(data).decode()},digest='proof'))
        return name,b.key(j)
    def snap(self):return b.handle(dict(op='snapshot'))
    def start(self,name):
        b.handle(dict(op='preflight',proof=dict(passed=True,digest='proof')));return b.handle(dict(op='start',batch=name,digest='proof'))
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
    def test_enqueue_output_says_it_will_not_start(self):
        name,_=self.enqueue()
        status=b.startability(name)
        self.assertFalse(status['can_start']);self.assertTrue(status['start_status'].startswith('WILL NOT START'))
        self.start(name)
        self.assertTrue(b.startability(name)['can_start'])
        b.write(self.home/'start-block.json',dict(at=time.time(),start_block='M2: the background agent cannot use: Extreme work folder (PermissionError)'))
        self.assertIn('Extreme work folder',b.startability(name)['start_status'])
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


class SourceCheckScope(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();root=self.root=Path(self.tmp.name)
        files={'scripts/edit-queue/batch.py':'print(1)\n','scripts/edit-queue/preamble.md':'schema\n','scripts/edit-queue/README.md':'notes\n',
               'scripts/edit-queue/tests/test_batch.py':'pass\n','scripts/edit-dashboard/desk_records.py':'x=1\n',
               '.claude/skills/_shared/editcap/editcap.py':'y=1\n','.claude/skills/_shared/editcap/selftest.py':'z=1\n',
               '.claude/skills/_shared/renderq/bench10.py':'b=1\n','scripts/edit-queue/scoreboard.json':'{}\n'}
        for name,text in files.items():
            (root/name).parent.mkdir(parents=True,exist_ok=True);(root/name).write_text(text)
        git=lambda *a:subprocess.run(['git',*a],cwd=root,check=True,capture_output=True)
        git('init','-q');git('add','-A');git('-c','user.email=t@t','-c','user.name=t','commit','-qm','x');git('update-ref','refs/remotes/origin/main','HEAD')
        self.patches=[patch.object(b.eq,'ROOT',str(root)),patch.object(b,'HOME',root/'home'),patch.object(b,'here',return_value='m6')]
        for x in self.patches:x.start()
    def tearDown(self):
        for x in reversed(self.patches):x.stop()
        self.tmp.cleanup()
    def test_dashboard_docs_and_tests_edits_do_not_block(self):
        for name in ('scripts/edit-dashboard/desk_records.py','scripts/edit-queue/README.md','scripts/edit-queue/tests/test_batch.py',
                     '.claude/skills/_shared/editcap/selftest.py','.claude/skills/_shared/renderq/bench10.py','scripts/edit-queue/scoreboard.json'):
            (self.root/name).write_text('another session is editing this\n')
        fp=b.fingerprints()
        self.assertEqual(fp['dirty'],[])
        self.assertNotIn('scripts/edit-dashboard/desk_records.py',fp['hashes'])
        self.assertIn('scripts/edit-queue/preamble.md',fp['hashes'])
    def test_real_scheduler_change_blocks_and_is_named(self):
        (self.root/'.claude/skills/_shared/editcap/editcap.py').write_text('y=2\n')
        (self.root/'scripts/edit-queue/preamble.md').write_text('changed prompt\n')
        self.assertEqual(sorted(b.fingerprints()['dirty']),['.claude/skills/_shared/editcap/editcap.py','scripts/edit-queue/preamble.md'])


class BackgroundFileAccess(Base):
    def folders(self,*paths):
        return [('f'+str(i),Path(x),True) for i,x in enumerate(paths)]
    def test_probe_creates_writes_renames_and_deletes_without_leftovers(self):
        a=Path(self.tmp.name)/'Videos to Review';a.mkdir()
        link=Path(self.tmp.name)/'linked';link.symlink_to(a)
        [r]=b.drive_probe(self.folders(link))
        self.assertTrue(r['passed']);self.assertEqual(r['steps'],['create','write','rename','delete'])
        self.assertEqual(r['resolved'],str(a.resolve()));self.assertEqual(list(a.iterdir()),[])
    def test_unwritable_or_missing_folder_fails_with_its_name(self):
        locked=Path(self.tmp.name)/'locked';locked.mkdir();locked.chmod(0o500)
        try:
            results=b.drive_probe(self.folders(locked,Path(self.tmp.name)/'missing'))
        finally:locked.chmod(0o700)
        self.assertFalse(results[0]['passed']);self.assertIn('PermissionError',results[0]['error'])
        self.assertFalse(results[1]['passed']);self.assertIn('not mounted',results[1]['error'])
    def test_launchd_context_records_and_interactive_does_not_count(self):
        good=Path(self.tmp.name)/'good';good.mkdir()
        env=dict(EDIT_BATCH_PROBE_FOLDERS=json.dumps([dict(label='Videos to Review',path=str(good))]))
        with patch.dict(os.environ,env):
            with patch.dict(os.environ,XPC_SERVICE_NAME='application.com.apple.Terminal'):
                self.assertIsNone(b.maybe_probe())
            self.assertFalse(b.launchd_probe_status()['ok'])
            with patch.dict(os.environ,XPC_SERVICE_NAME=b.AGENT_LABEL):
                doc=b.maybe_probe()
        self.assertEqual(doc['context'],'launchd');self.assertTrue(doc['passed']);self.assertTrue(doc['interpreter'])
        self.assertTrue(b.launchd_probe_status()['ok'])
    def test_missing_grant_blocks_preflight_with_named_reason(self):
        b.write(self.home/'drive-probe-launchd.json',dict(at=time.time(),passed=False,folders=[
            dict(label='Videos to Review',passed=False,error="PermissionError: [Errno 1] Operation not permitted")]))
        local=dict(host='m2',dirty=[],launcher_ok=True,canary=dict(passed=True,rows=[1,2,3,4]),hashes={'a':'1'},digest='d',commit='c',
                   drive_probe=b.launchd_probe_status())
        remote=dict(local,host='m6',drive_probe=dict(ok=True))
        with patch.object(b,'fingerprints',return_value=local),patch.object(b,'remote',return_value=remote):
            proof=b.preflight()
        self.assertFalse(proof['passed'])
        self.assertIn('m2 the background agent cannot use: Videos to Review (PermissionError: [Errno 1] Operation not permitted)',proof['problems'])
    def test_stale_probe_is_refused(self):
        passing_probe(self.home);doc=b.read(self.home/'drive-probe-launchd.json');doc['at']-=7*3600;b.write(self.home/'drive-probe-launchd.json',doc)
        self.assertIn('older than six hours',b.launchd_probe_status()['problem'])


class TickLaunch(Base):
    """A real tick on the M2 with the M6 unreachable: it claims, launches the runner directly, never touches the M6."""
    def fake_run(self,command,**kwargs):
        text=' '.join(map(str,command))
        if 'ssh' in command or 'm6' in command:
            self.m6_calls.append(command);return subprocess.CompletedProcess(command,255,'','ssh: connect to host m6: timed out')
        if 'editcap.py' in text and 'status' in text:
            return subprocess.CompletedProcess(command,0,json.dumps(dict(cap=3,in_use=[],renderq={})),'')
        return subprocess.CompletedProcess(command,0,'','')
    def setUp(self):
        super().setUp();self.m6_calls=[];self.launched=[]
        fp=dict(host='m2',dirty=[],digest='proof',hashes={},launcher_ok=True,canary={},commit='c')
        self.patches+= [patch.object(b,'fingerprints',return_value=fp),patch.object(b,'observe_local',return_value={}),
                        patch.object(b.subprocess,'run',side_effect=self.fake_run),patch.object(b,'identity',return_value='birth')]
        class Proc:
            pid=999
        def popen(command,**kwargs):self.launched.append(command);return Proc()
        self.patches.append(patch.object(b.subprocess,'Popen',side_effect=popen))
        for x in self.patches[-5:]:x.start()
    def test_m2_launch_needs_no_m6_and_records_runner_pid(self):
        passing_probe(self.home)
        name,k=self.enqueue();self.start(name)
        b.tick()
        self.assertEqual(len(self.launched),1);self.assertEqual(self.launched[0][0],sys.executable)
        self.assertTrue(self.launched[0][1].endswith('runner.py'))
        self.assertEqual([c for c in self.m6_calls if c[:1]!=['ssh'] or 'kickstart' not in ' '.join(c)],[])
        row=self.snap()['batches'][name]['jobs'][k]
        self.assertEqual(row['status'],'claimed');self.assertEqual(row['claim']['pid'],999);self.assertEqual(row['claim']['birth'],'birth')
    def test_missing_grant_on_this_mac_blocks_its_starts(self):
        name,k=self.enqueue();self.start(name)
        b.tick()
        self.assertEqual(self.launched,[])
        self.assertEqual(self.snap()['batches'][name]['jobs'][k]['status'],'queued')
        first=(self.home/'morning-report.md').read_text().splitlines()[0]
        self.assertIn('M2: no background file-access check has run yet',first)


class BlockedRowsAndDecisions(Base):
    def test_blocked_rows_name_an_owner_and_plain_next_action(self):
        name,k=self.enqueue(executor='codex',title='Real Exercise Demos Batch 5',job='REALDEMOS-B05',round_=1);self.start(name)
        c=self.claim()
        for _ in range(2):
            b.handle(dict(op='recover',batch=name,key=k,token=c['row']['claim']['token'],host='m2',pid_alive=False,spawn_failed=True))
            row=self.snap()['batches'][name]['jobs'][k]
            if row['status']=='queued':c=self.claim()
        row=self.snap()['batches'][name]['jobs'][k]
        self.assertEqual(row['status'],'blocked');self.assertEqual(row['outcome']['owner'],'Codex')
        self.assertIn('Open a new Codex chat for Real Exercise Demos Batch 5 (REALDEMOS-B05)',row['outcome']['next_action'])
        line=[x for x in (self.home/'morning-report.md').read_text().splitlines() if 'REALDEMOS' in x] if b.report(self.snap()) else []
        self.assertIn('NEXT (Codex): Open a new Codex chat',line[0])
    def test_reclassify_blocked_quality_dead_end_to_needs_dan(self):
        name,k=self.enqueue('chat-DS-106-R2','DS-106',2,title='Protein Snack Can');self.start(name);c=self.claim()
        b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',
                      outcome=dict(status='blocked',reason='early decay 83 ms vs 80',next_action='Decide the audio standard')))
        row=b.handle(dict(op='reclassify',batch=name,key=k,why='handoff 2026-11-18 item 5',
                          outcome=dict(status='needs-dan',question='Hold for another audio pass?',link='http://127.0.0.1:9814/',
                                       finding='early decay 83 ms vs 80',choices=['Hold for another audio pass'])))
        self.assertEqual(row['status'],'needs-dan');self.assertEqual(row['prior_outcome']['reason'],'early decay 83 ms vs 80')
        with self.assertRaises(ValueError):
            b.handle(dict(op='reclassify',batch=name,key=k,outcome=dict(status='needs-dan',question='q',link='l')))
    def test_held_round_never_starts_and_is_not_counted_as_waiting(self):
        name,k=self.enqueue();self.start(name)
        b.handle(dict(op='hold',batch=name,key=k,reason='Dan paused DS-51 R2 on Nov 17'))
        self.assertIsNone(self.claim())
        doc=b.report(self.snap())
        self.assertIsNone(doc['headline']);self.assertIn('Dan paused DS-51 R2',(self.home/'morning-report.md').read_text())
        b.handle(dict(op='unhold',batch=name,key=k))
        self.assertEqual(self.claim()['row']['id'],'DS-51')


class OneShotAlerts(Base):
    def test_alert_sent_once_per_event_recorded_and_not_repeated(self):
        self.here.return_value='m6'
        name,k=self.enqueue()
        b.handle(dict(op='stop'))
        b.report(self.snap());b.report(self.snap());b.report(self.snap())
        self.assertEqual(len(self.notes),1);self.assertIn('NOT STARTING: 1 queued edit',self.notes[0][1])
        state=b.read(self.home/'alerts.json')
        [event]=[e for e in state['events'].values() if not e.get('seeded')]
        self.assertTrue(event['sent']);self.assertIn('not verifiable',event['screen_delivery'])
        # A new decision for Dan rings once more; the old condition does not ring again.
        self.start(name);c=self.claim()
        b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',
                      outcome=dict(status='needs-dan',question='Approve?',link='http://127.0.0.1:9809/')))
        b.report(self.snap());b.report(self.snap())
        self.assertEqual(len(self.notes),2);self.assertIn('needs your answer',self.notes[1][1])
    def test_first_run_does_not_ring_for_old_rows(self):
        self.here.return_value='m6'
        name,k=self.enqueue();self.start(name);c=self.claim()
        b.handle(dict(op='outcome',batch=name,key=k,token=c['row']['claim']['token'],host='m2',
                      outcome=dict(status='blocked',reason='old',next_action='old action')))
        b.report(self.snap())
        self.assertEqual(self.notes,[])
    def test_m2_never_sends(self):
        name,k=self.enqueue();b.handle(dict(op='stop'));b.report(self.snap())
        self.assertEqual(self.notes,[])
    def test_failed_notification_retries_at_most_three_times(self):
        self.here.return_value='m6';self.patches[-1].stop()
        calls=[]
        with patch.object(b,'notify',side_effect=lambda t,m:(calls.append(1),dict(method='test',rc=1,stderr='no'))[1]):
            self.enqueue();b.handle(dict(op='stop'))
            for _ in range(5):b.report(self.snap())
        self.assertEqual(len(calls),3)
        self.patches[-1].start()



class DeskFallback(Base):
    def test_m6_desk_card_shows_the_alert_lines(self):
        sys.path.insert(0,str(PKG.parent/'edit-dashboard'))
        import observe
        home=Path(self.tmp.name)/'home';(home/'.absbyai-batch').mkdir(parents=True)
        self.enqueue();b.handle(dict(op='stop'))
        doc=b.report(self.snap())
        (home/'.absbyai-batch'/'morning-report.json').write_text(json.dumps(doc))
        out=observe.observe('m6',repo=Path(self.tmp.name)/'repo',tmp=Path(self.tmp.name),home=home)
        self.assertTrue(out['alerts'][0].startswith('NOT STARTING: 1 queued edit'))
        self.assertNotIn('NOT STARTING',' '.join(out['issues']))
        self.assertIn("Overnight queue: '+alert",(PKG.parent/'edit-dashboard'/'app.js').read_text())

if __name__=='__main__':unittest.main()
