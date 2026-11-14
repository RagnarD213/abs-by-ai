import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SHARED=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(SHARED/'editroute'),str(SHARED/'renderq'),str(SHARED/'editcap')]
import editroute as er
import hostcfg
import priority
import storage
import editcap as ec
import renderq as rq

class Optimization(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='optimization-fixture-');self.d=Path(self.tmp.name)
        self.env=patch.dict(os.environ,{'EDITROUTE_HOST':'m6','EDIT_PRIORITY_DIR':str(self.d/'priority'),
          'EDIT_STORAGE_DIR':str(self.d/'storage'),'EDITROUTE_DIR':str(self.d/'route'),
          'EDITCAP_DIR':str(self.d/'cap'),'GATE_DIR':str(self.d/'rq'),'GATE_FAIRNESS':'1','EDITCAP_FAIRNESS':'1',
          'GATE_BORROWING':'1','GATE_BUDGET':'6','GATE_UNMANAGED':'0','GATE_MEM':'20,0',
          'GATE_HEADROOM_S':'0','GATE_SETTLE':'0'})
        self.env.start();self.attrs=patch.multiple(ec,DIR=self.d/'cap',CAP=2);self.attrs.start()
        self.rqd=patch.object(rq,'DIR',self.d/'rq');self.rqd.start();rq._ensure()
        self.cal=ec.Calendar(longform='',shorts='',jobs={})
    def tearDown(self):self.rqd.stop();self.attrs.stop();self.env.stop();self.tmp.cleanup()
    def ctx(self,running=None):return time.time(),running or {},self.cal
    def test_third_job_reservation_parks_and_restores_owner_order(self):
        ec.acquire('DS-701',ctx=self.ctx());ec.acquire('DS-702',ctx=self.ctx())
        with ec._locked():
            reg=ec._load();reg['edits']['DS-701']['checkpoint']='saved-17';ec._save(reg)
        priority.update('reserve','DS-703')
        self.assertEqual(ec.acquire('DS-703',ctx=self.ctx())[0],0)
        reg=ec._load();self.assertEqual(reg['edits']['DS-701']['state'],'parked')
        self.assertEqual(reg['edits']['DS-701']['checkpoint'],'saved-17')
        self.assertTrue(priority.blocked('DS-701'));self.assertFalse(priority.blocked('DS-703'))
        self.assertFalse(priority.blocked('DS-701',host='m2'))
        ec.release('DS-703',review=True,ctx=self.ctx())
        reg=ec._load();self.assertEqual(reg['edits']['DS-701']['state'],'promoted')
        self.assertEqual(reg['edits']['DS-702']['state'],'promoted')
        self.assertFalse(priority.current());self.assertTrue(ec.pending_wakes(reg))
    def test_running_step_not_parked_until_checkpoint(self):
        ec.acquire('DS-701',ctx=self.ctx());ec.acquire('DS-702',ctx=self.ctx())
        priority.update('reserve','DS-703')
        busy={'DS-701':{'live':1,'running':1},'DS-702':{'live':1,'running':1}}
        self.assertEqual(ec.acquire('DS-703',ctx=self.ctx(busy))[0],3)
        self.assertEqual(ec._load()['edits']['DS-701']['state'],'active')
        busy['DS-702']={'live':1,'running':0}
        self.assertEqual(ec.acquire('DS-703',ctx=self.ctx(busy))[0],0)
    def test_milestone_cancel_expiry_and_owner_crash(self):
        for mode in ('milestone','release','expired','crashed'):
            priority.update('reserve','DS-703',owner_pid=os.getpid())
            if mode in ('milestone','release'):priority.update(mode,'DS-703')
            else:
                x=priority.read()
                if mode=='expired':x['reservation']['expires']=time.time()-1
                else:x['reservation']['owner_start']='reused PID / dead owner'
                priority.save(x)
            self.assertIsNone(priority.current())
    def test_ordinary_priority_with_two_openings_bound(self):
        ec.acquire('DS-701',ctx=self.ctx());ec.acquire('DS-702',ctx=self.ctx())
        ec.acquire('DS-710',ctx=self.ctx())
        for i in range(3):
            urgent='DS-'+str(720+i);ec.acquire(urgent,ctx=self.ctx(),priority=True)
            ec.release('DS-701' if i==0 else 'DS-'+str(719+i),ctx=self.ctx())
            reg=ec._load()
            if i<2:self.assertEqual(reg['edits'][urgent]['state'],'promoted')
        self.assertEqual(ec._load()['edits']['DS-710']['state'],'promoted')
    def test_budgets_memory_and_both_small_lanes(self):
        states=[dict(pool='heavy',held=True,info={'cores':4,'group':'DS-701','drives':['internal']})]
        heavy=dict(pool='heavy',group='DS-702',seq=1,drives=['internal'])
        small=dict(pool='light',group='DS-703',seq=2,expected_s=30,recipe='known-check')
        with patch.object(rq,'_tickets',return_value=[heavy]):
            self.assertFalse(rq.budget_check('light',states))
            self.assertFalse(rq._borrow_reason(small,states,()))
            rq._write(rq.DIR/'borrowing.json',{'1':{'t':time.time()}})
            self.assertIn('loan used',rq._borrow_reason(dict(small,pool='quick'),states,()))
        for budget in (6,8,10):
            with patch.dict(os.environ,{'GATE_BUDGET':str(budget)}):
                why=rq.budget_check('heavy',states)
                self.assertEqual(bool(why),budget<8)
        with patch.object(rq,'mem_state',return_value={'ok':False,'reason':'memory pressure warning'}):self.assertTrue(rq.budget_check('light',states))
        with patch.dict(os.environ,{'GATE_BUDGET':'6'}):
            self.assertTrue(rq.budget_check('light',states,[{'cpu':200}]))
    def test_different_ready_heavy_goes_before_second_same_job(self):
        states=[dict(pool='heavy',held=True,info={'group':'work:wv-03'})]
        tickets=[dict(group='WV-03',seq=1),dict(group='DS-701',seq=2)]
        self.assertEqual(rq._fair_order(tickets,states,'heavy')[0]['group'],'DS-701')
    def test_budget_reduction_protects_running_holders_and_fitting_heavy(self):
        states=[dict(pool='heavy',held=True,info={'cores':4,'group':j,'drives':['internal']}) for j in ('DS-701','DS-702')]
        before=json.loads(json.dumps(states))
        with patch.dict(os.environ,{'GATE_BUDGET':'10'}):self.assertFalse(rq.budget_check('quick',states))
        with patch.dict(os.environ,{'GATE_BUDGET':'6'}):self.assertTrue(rq.budget_check('quick',states))
        self.assertEqual(states,before)
        heavy=dict(pool='heavy',group='DS-703',seq=1,drives=['internal'])
        small=dict(pool='quick',group='DS-704',seq=2,expected_s=30,recipe='short')
        with patch.dict(os.environ,{'GATE_BUDGET':'8'}),patch.object(rq,'_tickets',return_value=[heavy]):
            self.assertFalse(rq.budget_check('heavy',states[:1]))
            self.assertIn('fitting heavy',rq._borrow_reason(small,states[:1],()))
        with patch.object(rq,'_tickets',return_value=[heavy]),patch.object(rq,'drive_full',return_value=['Extreme']):
            self.assertFalse(rq._borrow_reason(dict(small,expected_s=0),states[:1],()))
    def test_borrow_overrun_records_without_killing_and_disqualifies_recipe(self):
        now=time.time();info=dict(start=now-121,pool='quick',i=0,group='DS-704',borrowed=True,recipe='too-long',cores=2)
        rq._finish(info,rq.DIR/'slots/quick.0.json',now)
        self.assertGreater(rq._read(rq.DIR/'borrow-overruns.json')['too-long'],0)
        states=[dict(pool='heavy',held=True,info={'cores':4,'group':'DS-701','drives':['internal']})]
        heavy=dict(pool='heavy',group='DS-702',seq=1,drives=['internal'])
        with patch.object(rq,'_tickets',return_value=[heavy]):
            self.assertIn('previously overran',rq._borrow_reason(dict(pool='light',group='DS-704',seq=2,expected_s=30,recipe='too-long'),states,()))

    def test_storage_outstanding_bytes_and_full_existing_job(self):
        with patch.object(storage.shutil,'disk_usage',return_value=type('Disk',(),{'free':110*1e9})()):
            storage.check(self.d/'job1',20,'JOB1',commit=True)
            with self.assertRaisesRegex(RuntimeError,'storage:'):storage.check(self.d/'job2',20,'JOB2',commit=True)
            storage.consume('JOB1',20);storage.check(self.d/'job2',20,'JOB2',commit=True)
        with patch.object(rq,'find_workdir',return_value=self.d/'existing'),patch.object(storage,'check',side_effect=RuntimeError('no growth space')):
            with self.assertRaisesRegex(RuntimeError,'wait in place'):rq.workdir('EXISTING')
    def test_unknown_occupancy_and_active_night(self):
        s={h:dict(reachable=True,editcap={'error':'unreadable'}) for h in ('m6','m2')}
        self.assertEqual(er.capacity(s,er.cfg())['m6']['free'],0)
        self.assertEqual(hostcfg.core_budget('m6',hour=23,idle=1),6)
        with patch.object(hostcfg,'idle_seconds',return_value=None):self.assertEqual(hostcfg.core_budget('m6',hour=23),6)
    def test_activation_waits_for_old_ticket_and_scoped_rollback_releases_reservation(self):
        saved={k:os.environ.pop(k,None) for k in ('GATE_FAIRNESS','GATE_BORROWING')}
        try:
            ticket=rq.Ticket('heavy','old fixture','DS-701',False)
            ticket.info['scheduler_version']=4;ticket.path.write_text(json.dumps(ticket.info))
            self.assertEqual(priority.main(['activate']),3)
            ticket.close()
            self.assertEqual(priority.main(['activate']),0)
            self.assertTrue(rq.feature('priority'));self.assertTrue(rq.feature('fairness'))
            priority.update('reserve','DS-703')
            priority.update('set','DS-704')
            self.assertTrue(priority.urgent('DS-704'))
            self.assertEqual(priority.main(['deactivate']),0)
            self.assertFalse(priority.urgent('DS-704'))
            self.assertEqual(priority.read()['jobs'],{})
            self.assertFalse(rq.feature('priority'));self.assertIsNone(priority.current())
        finally:
            for k,v in saved.items():
                if v is not None:os.environ[k]=v

    def test_activation_refuses_an_old_whole_edit_waiter(self):
        with patch.object(priority,'legacy_cap_waiters',return_value=[{'job':'DS-701','pid':123}]):
            self.assertEqual(priority.main(['activate']),3)
            self.assertFalse((rq.DIR/'features.json').exists())

    def test_holder_version_survives_publication_and_finish(self):
        h=rq.acquire('fixture',group='DS-701',quiet=True);h.publish();self.assertEqual(h.info['scheduler_version'],5)
        h.release();history=json.loads((rq.DIR/'history.jsonl').read_text().splitlines()[-1]);self.assertEqual(history['scheduler_version'],5)

if __name__=='__main__':unittest.main()
