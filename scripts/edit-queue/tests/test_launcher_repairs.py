import copy
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

PKG=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PKG));import eq_common as eq
eq.unshadow()

class LauncherRepairs(unittest.TestCase):
    def test_invalid_binary_falls_back_only_to_valid_absolute_executable(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'executor';p.write_text('#!/bin/sh\nexit 0');p.chmod(0o700)
            cfg={'executors':{'claude':{'binary':'/does/not/exist','binary_candidates':[str(p)]}}}
            self.assertEqual(eq.resolve_binary('claude',cfg),str(p))
            p.chmod(0o600);self.assertIsNone(eq.resolve_binary('claude',cfg))
    def test_unknown_model_blocks_executor_before_login(self):
        cfg=eq.load_config();cfg['executors']['codex']['model']='obsolete-model-not-installed'
        with patch.object(eq,'resolve_binary',return_value='/usr/bin/true'):
            self.assertFalse(eq.auth_ok('codex',cfg)[0])
    def test_absent_login_probe_is_unverified_not_ready(self):
        cfg=eq.load_config();cfg['executors']['claude']['auth_check']=None
        with patch.object(eq,'resolve_binary',return_value='/usr/bin/true'):
            self.assertFalse(eq.auth_ok('claude',cfg)[0])
    def test_durable_claim_precedes_spawn_and_spawn_failure_releases_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            q=eq.sibling('queue');d=eq.sibling('dispatcher');cfg=eq.load_config();cfg['work_root']=tmp+'/work'
            jobs=Path(tmp)/'jobs.json';jobs.write_text(json.dumps({'jobs':[dict(id='AV-999',state='ready',size='S',order=1,title='disposable',rev=1)]}))
            with patch.multiple(q,JOBS=str(jobs),LOCK=tmp+'/jobs.lock'),patch.object(eq,'SCOREBOARD',tmp+'/scoreboard.json'):
                def failed(*a,**k):
                    self.assertIn('claim',json.loads(jobs.read_text())['jobs'][0])
                    raise OSError('injected pre-spawn failure')
                with patch.object(d.subprocess,'Popen',side_effect=failed):
                    ok,why=d.launch('AV-999','claude',cfg)
                self.assertFalse(ok);self.assertIn('spawn failed',why)
                self.assertNotIn('claim',json.loads(jobs.read_text())['jobs'][0])
                self.assertEqual(json.loads(jobs.read_text())['jobs'][0]['state'],'ready')

    def test_pause_and_review_backlog_four_and_five_block(self):
        import datetime
        d=eq.sibling('dispatcher');cfg=eq.load_config()
        base=dict(now=datetime.datetime.now(),pause_file=True,free_gb=1000,idle_seconds=9999,foreign_builds=0,
             auth={x:(True,'') for x in cfg['executors']},pid_alive=lambda p:False,master='',board='',work_dirs={},missing_sources={})
        for n in (4,5):
            data={'jobs':[dict(id='DS-'+str(i),state='delivered',size='S',order=i,title='fixture') for i in range(n)]}
            result=d.decide(data,cfg,base,{'runs':[]})
            self.assertFalse(result['launches']);self.assertTrue(any('PAUSE' in s for s in result['stops']))
            self.assertTrue(any('review queue' in s for s in result['stops']))

if __name__=='__main__':unittest.main()
