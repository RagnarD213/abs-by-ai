"""macOS fixture tests. All queue-like writes are confined to TemporaryDirectory."""
import concurrent.futures
import copy
import fcntl
import hashlib
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch
import observe as o
import server as sv

def put(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v))
def tree(d):
    return [(str(p.relative_to(d)),p.stat().st_ino,p.stat().st_mtime_ns,hashlib.sha256(p.read_bytes()).digest() if p.is_file() else None) for p in sorted(d.rglob('*'))]
class Scratch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rt=tempfile.TemporaryDirectory();cls.lib=Path(cls.rt.name)
        subprocess.run(['clang','-O2','-dynamiclib','-framework','CoreFoundation','-framework','IOKit',str(o.HERE/'kernel.c'),'-o',str(cls.lib/'kernel.dylib')],check=True)
    @classmethod
    def tearDownClass(cls):cls.rt.cleanup()
    def setUp(self):
        t=tempfile.TemporaryDirectory();self.addCleanup(t.cleanup);self.base=Path(t.name)
        self.home=self.base/'home';self.tmp=self.base/'tmp';self.repo=self.base/'repo';self.shared=self.repo/'.claude/skills/_shared'
        self.rq=self.tmp/'absbyai-renderq';self.ec=self.tmp/'absbyai-editcap';self.route=self.home/'.absbyai-editroute';self.now=time.time()
        self.here=patch.object(o,'HERE',self.lib);self.here.start();self.addCleanup(self.here.stop)
        self.env=patch.dict(os.environ,{},clear=True);self.env.start();self.addCleanup(self.env.stop)
        for f in o.POLICY:
            dst=self.shared/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path(__file__).resolve().parents[2]/'.claude/skills/_shared'/f,dst)
        self.config=dict(primary='m6',reserve_min=30,hosts={h:dict(slots=n,cores_present=b,cores_away=b+4 if h=='m6' else b,away_after_min=30,names=[socket.gethostname().split('.')[0]],load_guard=False,first=['EXDEMO'] if h=='m2' else ['SFC']) for h,n,b in [('m6',2,6),('m2',3,8)]})
        put(self.shared/'editroute/hosts.json',self.config);put(self.repo/'Handoffs/video-editing/jobs.json',{'jobs':[{'id':'DS-98','title':'SealedToken'}]});put(self.ec/'registry.json',{'version':1,'edits':{}})
        (self.rq/'slots').mkdir(parents=True);(self.rq/'queue').mkdir()
        (self.rq/'slots/heavy.0.lock').touch();put(self.rq/'features.json',dict(priority=True,borrowing=True,fairness=True))
        put(self.route/'priority.json',dict(version=1,jobs={},reservation=None));put(self.route/'waiting.json',{});put(self.route/'storage.json',{});(self.route/'decisions.jsonl').touch()
        put(self.rq/'unmanaged.json',dict(t=self.now,v=2,builds=[]));put(self.rq/'mem.json',dict(last=dict(t=self.now,ok=True,ok_for=40)));put(self.rq/'admits.json',{'heavy':0})
    def snap(self,h='m6'):return o.observe(h,self.repo,self.tmp,self.home)
    def reg(self,**jobs):put(self.ec/'registry.json',dict(version=1,edits={k:dict(job=k,state=s) for k,s in jobs.items()}))
    def lease(self,job='DS-98-arm-SealedToken',ticket=False):
        p=self.rq/('queue/heavy.00001.json' if ticket else 'slots/heavy.0.lock')
        record=dict(group=job,pid=os.getpid(),start=time.time(),created=time.time(),cores=4,**{k:'SealedToken' for k in ('session','label','cmd','recipe','cwd','error')})
        put(p if ticket else p.with_suffix('.json'),record);f=p.open('rb');fcntl.flock(f,fcntl.LOCK_EX);self.addCleanup(f.close);return f
    def test_observer_cannot_write_or_lock(self):
        self.lease();self.lease(ticket=True)
        put(self.ec/'registry.json',dict(version=1,edits={'DS-98':dict(job='DS-98',state='promoted',title='SealedToken',wake='SealedToken',ai='SealedToken')}))
        before=tree(self.base);real_open=os.open;real_fcntl=fcntl.fcntl
        def safe(p,flags,*rest):
            self.assertFalse(flags&(os.O_CREAT|os.O_TRUNC|os.O_WRONLY|os.O_RDWR));self.assertFalse(str(p).startswith('/Volumes'));return real_open(p,flags,*rest)
        def query(fd,op,*a):self.assertEqual(op,fcntl.F_GETLK);return real_fcntl(fd,op,*a)
        with patch('os.open',safe),patch('fcntl.fcntl',query),patch('fcntl.flock',side_effect=AssertionError),patch('os.rename',side_effect=AssertionError),patch('os.replace',side_effect=AssertionError):
            data=self.snap()
        self.assertEqual(data['issues'],[]);self.assertEqual((data['used'],data['renders'],data['tickets']),(1,1,1));self.assertNotIn('SealedToken',json.dumps(data));self.assertEqual(before,tree(self.base))
    def test_review_handoff_supersedes_stall_until_next_round(self):
        catalog = self.repo/'Handoffs/video-editing/jobs.json'
        for host in ('m2','m6'):
            put(catalog, {'jobs':[{'id':'DS-98','state':'draft_review','review_ready_at':200,'note':'SealedToken'}]})
            put(self.ec/'registry.json', {'version':1,'edits':{'DS-98':{
                'job':'DS-98','state':'stalled','active_since':100,'last_seen':150,'since':250}}})
            result=self.snap(host)
            self.assertEqual(result['jobs'][0]['states'],['with-dan'])
            self.assertEqual(result['used'],0)
            self.assertNotIn('SealedToken',json.dumps(result))
            self.assertEqual(o.read(self.ec/'registry.json')['edits']['DS-98']['state'],'stalled')
            put(self.ec/'registry.json', {'version':1,'edits':{'DS-98':{
                'job':'DS-98','state':'active','active_since':210,'last_seen':211}}})
            self.assertEqual(self.snap(host)['jobs'][0]['states'],['active'])
            put(catalog, {'jobs':[{'id':'DS-98','state':'in_progress','review_ready_at':500}]})
            self.reg(**{'DS-98':'stalled'})
            self.assertEqual(self.snap(host)['jobs'][0]['states'],['stalled'])

    def test_dated_review_and_live_render(self):
        catalog = self.repo/'Handoffs/video-editing/jobs.json'
        put(catalog, {'jobs':[{'id':'DS-98','state':'delivered','updated':'2026-11-14'}]})
        put(self.ec/'registry.json', {'version':1,'edits':{'DS-98':{
            'job':'DS-98','state':'active','last_seen':100}}})
        self.lease()
        data=self.snap()
        self.assertEqual(data['jobs'][0]['states'],['with-dan'])
        self.assertEqual((data['used'],data['renders']),(1,1))
        put(catalog, {'jobs':[{'id':'DS-98','state':'delivered','updated':'unknown'}]})
        self.assertEqual(self.snap()['jobs'][0]['states'],['active'])

    def test_dead_and_reused_holders_and_tickets(self):
        f=self.lease();f.close()
        t=self.lease(ticket=True);t.close()
        self.assertEqual(self.snap()['renders'],0);self.assertEqual(self.snap()['tickets'],0);self.assertTrue((self.rq/'queue/heavy.00001.json').exists())
        self.lease();p=self.rq/'slots/heavy.0.json';r=o.read(p);r['start']=1;put(p,r)
        self.assertIsNone(self.snap()['used']);self.assertIn('Render ownership unconfirmed',self.snap()['issues'])
    def test_parked_ticket_and_render_only(self):
        self.lease('DS-22',True);put(self.ec/'registry.json',dict(version=1,edits={'DS-22':dict(job='DS-22',state='parked',reservation_parked=True)}))
        self.assertEqual(self.snap()['used'],0);self.lease('DS-77');self.assertEqual(self.snap()['used'],1)
    def test_registry_reboot_and_schema(self):
        (self.ec/'registry.json').unlink();s=self.snap();self.assertIsNone(s['used']);self.assertIsNotNone(s['pressure'])
        put(self.ec/'registry.json',dict(version=9,edits={}));self.assertIsNone(self.snap()['used'])
        (self.shared/'editroute/hosts.json').unlink();self.assertNotIn('cap',self.snap())
    def test_policy_change_and_presence(self):
        with patch.object(o,'kernel',return_value=type('Idle',(),{'idle_seconds':lambda _:1900})()):self.assertEqual(self.snap()['budget'],10)
        with patch.object(o,'kernel',return_value=type('Idle',(),{'idle_seconds':lambda _:-1})()):self.assertEqual(self.snap()['budget'],6)
        (self.shared/'editroute/hostcfg.py').write_text('unknown');self.assertIn('Installed scheduler version needs checking',self.snap()['issues'])
    def test_combined_line_and_later_wait_clear(self):
        p=self.route/'decisions.jsonl'
        p.write_text('\n'.join(json.dumps(dict(job='DS-98-Secret',t=self.now-i,host=h)) for i,h in [(20,'m2'),(10,'wait')]))
        self.assertEqual(self.snap()['route']['reserved']['m2'],[]);put(self.route/'waiting.json',{'DS-98-Secret':{}});self.assertEqual(self.snap()['route']['line'],['DS-98'])
        p.write_text((json.dumps(dict(job='DS-22',host='m6',t=self.now))+'\n')*7500)
        self.assertIsNone(self.snap()['route'])
    def test_unknown_mem_cleared_queue_untouched_cache(self):
        cached=self.route/'drives-cache.json';put(cached,{'Extreme':{'free_gb':999,'t':1,'names':{'SealedToken':1}}})
        import ctypes
        real=ctypes.CDLL
        with patch.object(o.C,'CDLL',side_effect=lambda p: real(p) if p else type('NoPressure',(),{'sysctlbyname':lambda *a:1})()):
            d=self.snap()
        self.assertIsNone(d['pressure']);self.assertNotIn('SealedToken',json.dumps(d))
        (self.rq/'slots/heavy.0.lock').unlink();self.assertIsNone(self.snap()['used'])
    def test_advice(self):
        a,b=self.snap(),self.snap('m2')
        u={h:{'age':0,'data':d} for h,d in [('m6',a),('m2',b)]}
        def advice():return sv.suggest(u,self.now)
        for d in (a,b):d['pressure']='normal';d['internalRoom']=35;d['outside']['at']=self.now
        a['used']=2;b['used']=2;self.assertIn('M2',advice()[1])
        b['jobs']=[dict(id='DS-99',occupies=True,states=['active'])];a['route']['reserved']['m2']=['DS-99'];self.assertEqual(advice()[0],'room')
        a['route']['reserved']['m2']=['DS-90'];self.assertEqual(advice()[0],'wait')
        a['route']['reserved']['m2']=[];b['pressure']='warning';self.assertEqual(advice()[0],'wait')
        b['pressure']='normal';a['route']['line']=['AA-01'];self.assertEqual(advice()[0],'wait');a['route']['line']=[]
        b['jobs'][0]['states']=['waiting'];self.assertEqual(advice()[0],'wait');b['jobs']=[]
        b['dedicated']='AA-01';self.assertEqual(advice()[0],'wait');b['dedicated']=None
        b['internalRoom']=3;self.assertEqual(advice()[0],'wait');b['used']=3;self.assertEqual(advice()[0],'wait')
        u['m6']['age']=121;self.assertEqual(advice()[0],'check');u['m6']['age']=0;b['issues']=['Memory pressure unknown'];self.assertEqual(advice()[0],'check')
    def test_attempt_storm_cached_failure_and_recovery(self):
        clock=[500.0];fail=[False];calls=[];hold=threading.Event()
        def collect(h):
            calls.append(h)
            if h=='m2':
                hold.wait(2)
                if fail[0]:raise OSError('SealedToken')
            return self.snap(h)
        s=sv.Store(self.base/'cache.json',collect,lambda:clock[0])
        def done():
            end=time.monotonic()+3
            while s.busy and time.monotonic()<end:time.sleep(.01)
            self.assertFalse(s.busy)
        with concurrent.futures.ThreadPoolExecutor(10) as ex:list(ex.map(lambda i:s.start(True),range(40)))
        for _ in range(100):
            if 'm6' not in s.busy:break
            time.sleep(.01)
        self.assertIn('data',s.view()['hosts']['m6']);self.assertTrue(s.view()['hosts']['m2']['busy'])
        hold.set();done();s.start(True);s.view();self.assertEqual(len(calls),2)
        old=s.view()['hosts']['m2']['lastSuccess'];clock[0]+=60;fail[0]=True;s.start();done()
        self.assertEqual(s.view()['advice'][0],'check');self.assertEqual(s.view()['hosts']['m2']['lastSuccess'],old)
        self.assertNotIn('SealedToken',(self.base/'cache.json').read_text());clock[0]+=60;fail[0]=False;s.start();done();self.assertIsNone(s.view()['hosts']['m2']['error'])
    def test_snapshot_survives_worker_relaunch(self):
        cache=self.base/'newcache.json'; s=sv.Store(cache,collect=self.snap);s.start()
        end=time.monotonic()+2
        while s.busy and time.monotonic()<end:time.sleep(.01)
        again=sv.Store(cache,collect=lambda h:self.fail('fresh cache should be reused'))
        again.start();self.assertEqual(again.busy,set());self.assertIn('data',again.view()['hosts']['m6'])
    def test_unassigned_groups_no_false_capacity(self):
        self.lease('pg:123');data=self.snap();self.assertEqual(data['renders'],1);self.assertEqual(data['used'],0)
        self.lease('work:UnknownSealedToken',ticket=True);data=self.snap();self.assertTrue(data['lowerBound']);self.assertNotIn('SealedToken',json.dumps(data));self.assertIn('One project identity unconfirmed',data['issues'])
    def test_child_timeout_and_reap(self):
        pidfile=self.base/'pid';cmd=[sys.executable,'-c','import os,time,sys;open(sys.argv[1],"w").write(str(os.getpid()));time.sleep(5)',str(pidfile)]
        with self.assertRaises(subprocess.TimeoutExpired):sv.remote(cmd,.3)
        with self.assertRaises(ProcessLookupError):os.kill(int(pidfile.read_text()),0)
if __name__=='__main__':unittest.main()
