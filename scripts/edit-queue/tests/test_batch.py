"""Ledger, process recovery, and disconnected-owner behavior with isolated persistent state."""
import base64
import hashlib
import importlib.util
import json
import multiprocessing
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

PKG=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PKG))
import eq_common as eq
eq.unshadow();b=eq.sibling('batch');worker=eq.sibling('batch_runner')


def claim_process(home, results):
    b.HOME=Path(home)
    with patch.object(b,'here',return_value='m2'):
        results.put(b.handle(dict(op='claim',host='m2',digest='proof',occupied=[],slots=1)))


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.home=Path(self.tmp.name)
        self.p=patch.object(b,'HOME',self.home);self.p.start()
        self.h=patch.object(b,'here',return_value='m2');self.h.start()
        self.cfg=eq.load_config();self.cfg['paused_groups']=[]
        self.c=patch.object(eq,'load_config',return_value=self.cfg);self.c.start()
    def tearDown(self):self.c.stop();self.h.stop();self.p.stop();self.tmp.cleanup()
    def enqueue(self,name='night',ids=('SL-36',),placement='any',round_=1):
        data=b'CONTENT SFL: use approved source; stop for real choices.'
        jobs=[dict(id=j,round=round_,title='Real video '+j,size='S',order=i,kind='SFL',target='review',need_gb=5,
                   executor='claude',placement=placement,brief_sha256=hashlib.sha256(data).hexdigest()) for i,j in enumerate(ids)]
        return b.handle(dict(op='enqueue',batch=name,jobs=jobs,briefs={b.key(j):base64.b64encode(data).decode() for j in jobs},digest='proof'))
    def start(self,name='night'):
        b.handle(dict(op='preflight',proof=dict(passed=True,digest='proof')))
        return b.handle(dict(op='start',batch=name,digest='proof'))
    def claim(self,host='m2',slots=3,occupied=()):
        return b.handle(dict(op='claim',host=host,digest='proof',slots=slots,occupied=list(occupied)))
    def row(self):return b.handle(dict(op='snapshot'))['batches']['night']['jobs']['SL-36-R1']
    def outcome(self,c,status='delivered',**kw):
        return b.handle(dict(op='outcome',batch=c['batch'],key=c['key'],token=c['row']['claim']['token'],host=c['row']['claim']['owner'],outcome=dict(status=status,**kw)))
    def test_disabled_install_and_two_tick_receipt(self):
        self.enqueue();self.assertIsNone(self.claim())
        self.assertNotEqual(b.receipt('night')['receipt'],'queued')
        for host in ('m2','m6'):b.handle(dict(op='tick',host=host,observation={}))
        self.assertEqual(b.receipt('night')['receipt'],'queued')
        self.assertFalse(b.receipt('night')['enabled'])
    def test_exactly_one_owner_under_competing_processes(self):
        self.enqueue();self.start()
        ctx=multiprocessing.get_context('fork');q=ctx.Queue()
        workers=[ctx.Process(target=claim_process,args=(str(self.home),q)) for _ in range(4)]
        for p in workers:p.start()
        for p in workers:p.join(10);self.assertEqual(p.exitcode,0)
        self.assertEqual(sum(q.get(timeout=2) is not None for _ in workers),1)
        q.close();q.join_thread()
    def test_pinned_job_skipped_and_longest_first(self):
        self.enqueue(ids=('SL-36','RA-02'))
        p=self.home/'night/state.json';s=b.read(p);s['jobs']['SL-36-R1']['placement']='m2';s['jobs']['RA-02-R1']['size']='L';b.write(p,s)
        self.start();self.assertEqual(self.claim('m6')['row']['id'],'RA-02')
        self.assertIsNone(self.claim('m6'))
        self.assertEqual(self.claim('m2')['row']['id'],'SL-36')
    def test_failed_preflight_stops_new_claims_on_an_enabled_batch(self):
        self.enqueue();self.start()
        b.handle(dict(op='preflight',proof=dict(passed=False,digest='proof',problems=['other Mac mismatch'])))
        self.assertIsNone(self.claim())

    def test_stop_keeps_running_claim_and_prevents_starts(self):
        self.enqueue(ids=('SL-36','RA-02'));self.start();c=self.claim(slots=1)
        b.handle(dict(op='stop'));self.assertIsNone(self.claim())
        self.assertEqual(self.row()['status'],'claimed');self.outcome(c)
        self.assertEqual(self.row()['status'],'delivered')
    def test_starting_a_new_batch_does_not_restart_a_stopped_old_batch(self):
        self.enqueue();self.start();b.handle(dict(op='stop'))
        self.enqueue('later',ids=('RA-02',));self.start('later')
        self.assertEqual(self.claim()['batch'],'later')
        self.assertIsNone(self.claim())

    def test_round_dedup_and_live_takeover_refused(self):
        self.enqueue();self.start();c=self.claim()
        with self.assertRaises(ValueError):self.enqueue('other')
        with self.assertRaises(ValueError):b.handle(dict(op='takeover',job='SL-36',host='m6'))
        self.outcome(c)
        with self.assertRaises(ValueError):self.enqueue('next')
        self.enqueue('next',round_=2)
    def test_killed_runner_one_recovery_then_blocked(self):
        self.enqueue();self.start();c=self.claim()
        def expire():
            p=self.home/'night/state.json';s=b.read(p);s['jobs'][c['key']]['claim']['heartbeat']=0;b.write(p,s)
        expire();request=dict(op='recover',batch='night',key=c['key'],token=c['row']['claim']['token'],host='m2',pid_alive=True)
        self.assertEqual(b.handle(request)['status'],'claimed')
        request['pid_alive']=False;self.assertEqual(b.handle(request)['status'],'queued')
        c=self.claim();expire();request['token']=c['row']['claim']['token']
        self.assertEqual(b.handle(request)['status'],'blocked')
    def test_recovery_can_reuse_its_own_still_registered_full_slot(self):
        self.enqueue();self.start();c=self.claim(slots=1)
        p=self.home/'night/state.json';s=b.read(p);s['jobs'][c['key']]['claim']['heartbeat']=0;b.write(p,s)
        b.handle(dict(op='recover',batch='night',key=c['key'],token=c['row']['claim']['token'],host='m2',pid_alive=False))
        resumed=self.claim(slots=1,occupied=['SL-36'])
        self.assertIsNotNone(resumed);self.assertEqual(resumed['row']['resumes'],1)

    def test_usage_pause_keeps_folder_owner_and_three_retries(self):
        self.enqueue();self.start()
        for attempt in range(3):
            c=self.claim();token=c['row']['claim']['token']
            b.handle(dict(op='heartbeat',batch='night',key=c['key'],token=token,fields=dict(workdir='/saved/original')))
            r=self.outcome(c,'paused-for-allowance',reason='quota')
            if attempt<2:
                self.assertEqual(r['status'],'queued');self.assertEqual(r['workdir'],'/saved/original');self.assertEqual(r['placement'],'m2')
                self.assertIsNone(self.claim())
                p=self.home/'night/state.json';s=b.read(p);s['jobs'][c['key']]['not_before']=0;b.write(p,s)
                ctrl=b.control();ctrl['executor_backoff']={};b.write(self.home/'control.json',ctrl)
            else:self.assertEqual(r['status'],'blocked')
    def test_owner_disconnect_never_moves_claim(self):
        self.enqueue();self.start();c=self.claim('m6')
        with patch.object(b,'alive',return_value=False):b.reconcile(b.handle(dict(op='snapshot')))
        self.assertEqual(self.row()['claim']['owner'],'m6');self.assertIsNone(self.claim('m2',slots=1,occupied=['OTHER']))
    def test_stale_outcome_token_cannot_overwrite_new_owner(self):
        self.enqueue();self.start();c=self.claim();self.outcome(c)
        stale=dict(op='heartbeat',batch='night',key=c['key'],token='wrong',fields=dict(phase='wrong'))
        with self.assertRaises(ValueError):b.handle(stale)
        self.assertEqual(self.row()['status'],'delivered')
    def test_needs_dan_requires_question_and_link(self):
        self.enqueue();self.start();c=self.claim()
        with self.assertRaises(ValueError):self.outcome(c,'needs-dan',question='Pick one')
        self.assertEqual(self.row()['status'],'claimed')
        self.assertEqual(self.outcome(c,'needs-dan',question='Pick one',link='http://127.0.0.1:9876/')['status'],'needs-dan')
    def test_outcome_offline_outbox_replays_once(self):
        request=dict(batch='night',k='SL-36-R1',token='saved',outcome=dict(status='blocked',reason='test',next_action='inspect'))
        with patch.object(b,'rpc',side_effect=RuntimeError('m2 unavailable')):
            self.assertIsNone(b.update('outcome',**request))
        self.assertEqual(len(list((self.home/'outbox').glob('*.json'))),1)
        with patch.object(b,'rpc',return_value={}) as rpc:
            b.flush_outbox();b.flush_outbox();self.assertEqual(rpc.call_count,1)
    def test_brief_tamper_fails_before_worker_start(self):
        self.enqueue();self.start();(self.home/'night/briefs/SL-36-R1.md').write_text('tampered')
        with self.assertRaises(ValueError):self.claim()
    def test_checked_report_does_not_describe_a_delivered_job_as_queued(self):
        self.enqueue();self.start();c=self.claim();self.outcome(c,verdict='SHIP WITH DISCLOSED UNCERTAINTY')
        report=b.report(b.handle(dict(op='snapshot')))
        self.assertEqual(report['groups']['Checked'][0]['reason'],'SHIP WITH DISCLOSED UNCERTAINTY')
    def test_disabled_batch_does_not_accumulate_idle_slot_time(self):
        self.enqueue()
        b.handle(dict(op='tick',host='m2',observation={'_capacity':{'free':3}}))
        p=self.home/'night/state.json';s=b.read(p);s['ticks']['m2']=time.time()-120;b.write(p,s)
        b.handle(dict(op='tick',host='m2',observation={'_capacity':{'free':3}}))
        self.assertEqual(self.row().get('idle_slot_minutes',0),0)

    def test_temporary_start_wait_requeues_and_holds_the_host(self):
        self.enqueue(ids=('SL-36','RA-02'));self.start();c=self.claim()
        outcome=dict(op='outcome',batch='night',key=c['key'],token=c['row']['claim']['token'],host='m2',outcome={'status':'deferred-start','reason':'slot raced'},backoff_s=120)
        self.assertEqual(b.handle(outcome)['status'],'queued');self.assertIsNone(self.claim())
        self.assertEqual(self.claim('m6')['row']['id'],'RA-02')
    def test_allowance_backoff_is_shared_by_executor(self):
        self.enqueue(ids=('SL-36','RA-02'));self.start();c=self.claim()
        self.outcome(c,'paused-for-allowance',reason='quota',executor='claude')
        self.assertIsNone(self.claim('m6'))
    def test_malformed_outbox_does_not_wedge_later_items(self):
        (self.home/'outbox').mkdir();(self.home/'outbox/broken.json').write_text('{bad')
        b.flush_outbox()
        self.assertFalse((self.home/'outbox/broken.json').exists())
        self.assertTrue((self.home/'outbox-quarantine/broken.json').exists())
    def test_pending_mirror_does_not_consume_a_finished_workers_slot(self):
        self.enqueue(ids=('SL-36','RA-02'));self.start();c=self.claim(slots=1)
        b.handle(dict(op='heartbeat',batch='night',key=c['key'],token=c['row']['claim']['token'],fields={'phase':'outcome waiting for review mirror'}))
        self.assertEqual(self.claim(slots=1)['row']['id'],'RA-02')

    def test_outbox_permanent_rejection_becomes_visible_blocked(self):
        self.enqueue();self.start();c=self.claim();token=c['row']['claim']['token']
        request=dict(op='outcome',batch='night',key=c['key'],token=token,host='m2',outcome=dict(status='needs-dan',question='Pick',link='http://127.0.0.1:9850/',pending_review={'review_root':'bad','review_port':9850}))
        b.write(self.home/'outbox'/(token+'.json'),request)
        with patch.object(worker,'review_link',side_effect=ValueError('invalid review folder')):
            for _ in range(3):b.flush_outbox()
        self.assertEqual(self.row()['status'],'blocked');self.assertFalse(list((self.home/'outbox').glob('*.json')))
    def test_transport_failure_preserves_pending_review_for_long_outage(self):
        self.enqueue();self.start();c=self.claim();token=c['row']['claim']['token']
        request=dict(op='outcome',batch='night',key=c['key'],token=token,host='m2',outcome=dict(status='needs-dan',question='Pick',link='http://127.0.0.1:9850/',pending_review={'review_root':'saved','review_port':9850}))
        path=self.home/'outbox'/(token+'.json');b.write(path,request)
        with patch.object(worker,'review_link',side_effect=b.TransportError('M6 unreachable')):
            for _ in range(35):b.flush_outbox()
        self.assertIn('pending_review',b.read(path)['outcome']);self.assertEqual(self.row()['status'],'claimed')
    def test_takeover_preserves_the_previous_terminal_outcome(self):
        self.enqueue();self.start();c=self.claim();self.outcome(c,verdict='SHIP')
        b.handle(dict(op='takeover',job='SL-36',host='m2'))
        self.assertEqual(self.row()['prior_outcome']['status'],'delivered')

    def test_chat_batches_inherit_only_a_current_enabled_preflight(self):
        self.enqueue('seed',ids=('RA-02',));self.start('seed')
        self.enqueue('chat-SL-36-R1')
        self.assertTrue(b.read(self.home/'chat-SL-36-R1/state.json')['enabled'])
        b.handle({'op':'stop'});self.enqueue('chat-DS-106-R1',ids=('DS-106',))
        self.assertFalse(b.read(self.home/'chat-DS-106-R1/state.json')['enabled'])

    def test_capacity_waits_do_not_exhaust_start_failure_budget(self):
        self.enqueue();self.start()
        for _ in range(5):
            c=self.claim();token=c['row']['claim']['token']
            b.handle(dict(op='outcome',batch='night',key=c['key'],token=token,host='m2',outcome={'status':'deferred-start','reason':'dedicated reservation','retry_kind':'capacity'},backoff_s=0))
        self.assertEqual(self.row()['status'],'queued');self.assertEqual(self.row()['start_failures'],0)
    def test_unattempted_review_pause_does_not_extend_executor_backoff(self):
        self.enqueue(ids=('SL-36','RA-02'));self.start();first=self.claim();second=self.claim()
        self.outcome(first,'paused-for-allowance',reason='quota',executor='codex')
        until=b.control()['executor_backoff']['codex']['until']
        self.outcome(second,'paused-for-allowance',reason='waiting for quota',executor='codex',attempted=False)
        self.assertEqual(b.control()['executor_backoff']['codex']['until'],until)
    def test_live_render_only_or_waiting_jobs_cannot_enqueue(self):
        for state in ('waiting','promoted','active','parked'):
            self.assertTrue(b.job_live('SL-36',{'m2':{'editcap':{'edits':{'SL-36':state}}}}))
        self.assertTrue(b.job_live('SL-36',{'m2':{'editcap':{'in_use':['SL-36'],'edits':{}}}}))
        self.assertFalse(b.job_live('SL-36',{'m2':{'editcap':{'in_use':[],'edits':{}}}}))

    def test_real_demo_batch_keeps_its_id_and_drive_bound_placement(self):
        import editroute
        brief=self.home/'brief.md';brief.write_text('Build only the five real Batch 4 demos; stop for review.')
        spec=self.home/'spec.json'
        b.write(spec,dict(jobs=[dict(id='REALDEMOS-B04',round=1,title='Real Exercise Demos Batch 4 R1',
            size='M',kind='EXDEMO',executor='codex',need_gb=20,target='review',drive_bound=True,brief=str(brief))]))
        statuses={h:dict(reachable=True,editcap=dict(in_use=[],edits={})) for h in ('m2','m6')}
        with patch.object(editroute,'gather',return_value=statuses), patch.object(editroute,'holder',return_value=(None,None)), \
             patch.object(b,'rpc',side_effect=lambda op,**kw:b.handle(dict(op=op,**kw))), \
             patch.object(b,'fingerprints',return_value=dict(digest='proof')), patch.object(b,'kick'):
            b.enqueue('chat-REALDEMOS-B04-R1',spec)
        row=b.handle(dict(op='snapshot'))['batches']['chat-REALDEMOS-B04-R1']['jobs']['REALDEMOS-B04-R1']
        self.assertEqual(row['id'],'REALDEMOS-B04')
        self.assertEqual(row['placement'],'m2')
        self.assertEqual(row['brief_sha256'],hashlib.sha256(brief.read_bytes()).hexdigest())
        self.assertFalse(b.JOB.fullmatch('UNRELATEDLONG-B04'))

    def test_large_storage_wait_steps_aside_for_smaller_jobs_on_that_mac(self):
        self.enqueue(ids=('SL-36','RA-02'));self.start();c=self.claim('m6',slots=1)
        b.handle(dict(op='outcome',batch='night',key=c['key'],token=c['row']['claim']['token'],host='m6',outcome={'status':'deferred-start','reason':'need 80 GB; only 10 GB usable','retry_kind':'storage'},backoff_s=0))
        next_job=self.claim('m6',slots=1)
        self.assertEqual(next_job['row']['id'],'RA-02')
        self.assertEqual(self.claim('m2',slots=1)['row']['id'],'SL-36')

    def test_orphan_is_stopped_before_detached_render_drain_and_single_resume(self):
        import subprocess
        self.enqueue();self.start();c=self.claim();token=c['row']['claim']['token']
        b.handle(dict(op='heartbeat',batch='night',key=c['key'],token=token,fields={'session':{'pid':567,'birth':'recorded'}}))
        p=self.home/'night/state.json';s=b.read(p);s['jobs'][c['key']]['claim']['heartbeat']=0;b.write(p,s)
        snapshot=lambda:b.handle({'op':'snapshot'})
        with patch.object(b,'alive',side_effect=lambda pid,birth:pid==567),patch.object(b.os,'killpg') as kill,patch.object(b.subprocess,'run') as capacity:
            b.reconcile(snapshot());kill.assert_called_once_with(567,b.signal.SIGTERM);capacity.assert_not_called()
        busy=subprocess.CompletedProcess([],0,json.dumps({'renderq':{'SL-36':{'live':1}}}), '')
        with patch.object(b,'alive',return_value=False),patch.object(b.subprocess,'run',return_value=busy):b.reconcile(snapshot())
        self.assertEqual(self.row()['status'],'claimed')
        clear=subprocess.CompletedProcess([],0,json.dumps({'renderq':{}}), '')
        with patch.object(b,'alive',return_value=False),patch.object(b.subprocess,'run',return_value=clear):b.reconcile(snapshot())
        self.assertEqual(self.row()['status'],'queued');self.assertEqual(self.row()['resumes'],1)

    def test_stopped_ad_production_blocks_enqueue_and_existing_queued_claim(self):
        self.enqueue(ids=('RA-02',));self.start()
        self.cfg['paused_groups']=[{'group':'RA','executor':'any','reason':'Dan stopped new Abs By AI ads'}]
        self.assertIsNone(self.claim())
        with self.assertRaisesRegex(ValueError,'stopped new Abs By AI ads'):self.enqueue('other',ids=('RA-99',))

    def test_uncertainty_verdict_is_distinct_and_rejection_needs_evidence(self):
        p=self.home/'review.md';p.write_text('VERDICT: SHIP WITH DISCLOSED UNCERTAINTY\nUnsupported perceptual check disclosed.')
        self.assertEqual(worker.review_verdict(p),'SHIP WITH DISCLOSED UNCERTAINTY')
        p.write_text('VERDICT: DOES NOT SHIP\nSomething I would like Dan to approve')
        self.assertEqual(worker.review_verdict(p),'REJECTION WITHOUT CITATION')
        p.write_text('VERDICT: DOES NOT SHIP\n0:12, rule VIDEO-RULES.md: head clipped')
        self.assertEqual(worker.review_verdict(p),'DOES NOT SHIP')

if __name__=='__main__':unittest.main()
