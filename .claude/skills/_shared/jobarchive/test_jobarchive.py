import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from unittest.mock import patch

SPEC=importlib.util.spec_from_file_location('archive_under_test',Path(__file__).with_name('jobarchive.py'))
ja=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(ja)

class ArchiveSafety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='archive-fixture-');self.d=Path(self.tmp.name)
        self.work=self.d/'work';self.src=self.work/'OLD space';self.src.mkdir(parents=True)
        (self.src/'nested').mkdir();(self.src/'nested/file.bin').write_bytes(bytes(range(256))*10)
        (self.src/'file.txt').write_text('saved checkpoint');(self.src/'link').symlink_to('file.txt')
        self.sea=self.d/'Expansion';self.sea.mkdir();self.base=self.sea/ja.ARCHIVE_DIR;self.base.mkdir()
        self.repo=self.d/'repo';self.repo.mkdir();(self.repo/'AI_COORDINATION.md').write_text('')
        self.state=self.d/'state';self.state.mkdir()
        for r in ['.claude/skills','scripts','Media/clip-library']:(self.repo/r).mkdir(parents=True,exist_ok=True)
        for r in ['AGENTS.md','CLAUDE.md']:(self.repo/r).write_text('fixture rules')
        old=time.time()-45*86400
        for d,ds,fs in os.walk(self.src):
            for n in ds+fs+['']:os.utime(Path(d)/n,(old,old),follow_symlinks=False)
        self.env=patch.dict(os.environ,{'JOBARCHIVE_ROOTS':'internal='+str(self.work),'JOBARCHIVE_REPO':str(self.repo),
            'JOBARCHIVE_BUSY':'','JOBARCHIVE_EDITCAP_JSON':'{"edits":{},"renderq":{}}','JOBARCHIVE_HOST':'m6'})
        self.env.start();self.attrs=patch.multiple(ja,SEAGATE=self.sea,STATE=self.state,HOME=self.d/"home");self.attrs.start()
        self.mount=patch.object(ja,'mount_identity',return_value=['fixture-seagate',3]);self.mount.start();self.local=patch.object(ja,'seagate_local',return_value=True);self.local.start()
        self.row=ja.decide()[0];self.original=ja.hash_tree(str(self.src))
        self.second=self.d/'second';shutil.copytree(self.src,self.second,symlinks=True)
        (self.state/'verified-second-copies.json').write_text(json.dumps({str(self.src):str(self.second)}))
    def tearDown(self):
        self.local.stop();self.mount.stop();self.attrs.stop();self.env.stop();self.tmp.cleanup()
    def archive(self):return ja.archive_one(self.row,str(self.base),False)
    def test_move_restore_nested_space_path_links_and_hashes(self):
        dest=self.archive();self.assertFalse(self.src.exists())
        restored=self.d/'restored space'
        self.assertEqual(ja.cmd_restore(argparse.Namespace(job=self.src.name,to=str(restored))),0)
        self.assertEqual(ja.hash_tree(str(restored)),self.original)
        self.assertEqual(os.readlink(restored/'link'),'file.txt');self.assertTrue((restored/'link').exists())
    def test_second_copy_missing_retains_source(self):
        (self.state/'verified-second-copies.json').unlink();self.archive();self.assertTrue(self.src.exists())
    def test_index_failure_retains_source(self):
        with patch.object(ja,'append_index',side_effect=RuntimeError('index write failed')):
            with self.assertRaises(RuntimeError):self.archive()
        self.assertTrue(self.src.exists())
    def test_repeat_copy_does_not_duplicate_index(self):
        (self.state/'verified-second-copies.json').unlink()
        self.archive();before=(self.base/'index.jsonl').read_bytes();self.archive()
        self.assertEqual((self.base/'index.jsonl').read_bytes(),before)
    def test_retained_source_is_not_reported_as_moved(self):
        import contextlib,io
        output=io.StringIO()
        with patch.object(ja,'archive_one',return_value='fixture'),patch.object(ja,'warn_low_space'),contextlib.redirect_stdout(output):
            self.assertEqual(ja.cmd_run(argparse.Namespace(limit=1,until=None)),0)
        self.assertIn('0 moved, 1 verified copies with source retained',output.getvalue())

    def test_wrong_mount_retains_source(self):
        with patch.object(ja,'mount_identity',side_effect=RuntimeError('wrong mount')):
            with self.assertRaises(RuntimeError):self.archive()
        self.assertTrue(self.src.exists())
    def test_destination_corruption_retains_source(self):
        original=ja.hash_tree
        def corrupt(path,remote=False):
            x=original(path,remote)
            if str(path).startswith(str(self.base)):x['file.txt']=[1,'bad']
            return x
        with patch.object(ja,'hash_tree',side_effect=corrupt):
            with self.assertRaisesRegex(RuntimeError,'verify failed'):self.archive()
        self.assertTrue(self.src.exists())
    def test_old_review_never_expires(self):
        with patch.dict(os.environ,{'JOBARCHIVE_EDITCAP_JSON':json.dumps({'edits':{self.src.name:{'state':'with-dan'}},'renderq':{}})}):
            self.assertFalse(ja.decide()[0]['move'])
    def test_repo_keep_list_is_read_by_installed_copy(self):
        keep=self.repo/'.claude/skills/_shared/jobarchive/keep.txt';keep.parent.mkdir(parents=True);keep.write_text(self.src.name+'\n')
        self.assertFalse(ja.decide()[0]['move'])
    def test_changed_source_retains_original_manifest(self):
        (self.state/'verified-second-copies.json').unlink();dest=Path(self.archive())
        before=(dest/'.jobarchive-manifest.json').read_bytes();(self.src/'file.txt').write_text('new')
        with self.assertRaisesRegex(RuntimeError,'retry conflicts'):self.archive()
        self.assertEqual((dest/'.jobarchive-manifest.json').read_bytes(),before)
    def test_partial_removal_retry_keeps_full_manifest(self):
        with patch.object(ja.shutil,'rmtree',side_effect=OSError('interrupted')):
            with self.assertRaises(OSError):self.archive()
        dest=self.base/'m6-internal'/self.src.name;before=(dest/'.jobarchive-manifest.json').read_bytes()
        (self.src/'nested/file.bin').unlink()
        # Retry may only remove when full independent second copy remains verified.
        with patch.object(ja,'decide',return_value=[self.row]):self.archive()
        self.assertEqual((dest/'.jobarchive-manifest.json').read_bytes(),before)
        self.assertFalse(self.src.exists())
    def test_new_review_before_removal_retains_source(self):
        original=ja.append_index
        def appeared(*a,**k):
            original(*a,**k);(self.repo/'AI_COORDINATION.md').write_text('OLD space AWAITING review')
        with patch.object(ja,'append_index',side_effect=appeared):
            with self.assertRaisesRegex(RuntimeError,'protected'):self.archive()
        self.assertTrue(self.src.exists())
    def test_registered_old_review_protects_source_even_without_board_or_cap(self):
        home=self.d/'home';entries=home/'Library/Application Support/AbsByAI Review Hub/pages';entries.mkdir(parents=True)
        (entries/'9973.json').write_text(json.dumps({'root':str(self.src/'nested')}))
        cache=home/'Library/Application Support/AbsByAI Reviews/9973';cache.mkdir(parents=True)
        (cache/'manifest.json').write_text(json.dumps({'files':[{'path':'file.bin'}]}))
        self.assertFalse(ja.decide()[0]['move'])
    def test_incomplete_rule_evidence_blocks_removal(self):
        (self.repo/'AGENTS.md').unlink()
        with self.assertRaisesRegex(RuntimeError,'reference evidence incomplete'):ja.decide()

    def test_board_missing_blocks_archival(self):
        (self.repo/'AI_COORDINATION.md').unlink()
        with self.assertRaisesRegex(RuntimeError,'board unreadable'):ja.decide()
    def test_restore_hash_mismatch_fails(self):
        dest=Path(self.archive());(dest/'file.txt').write_text('corrupt')
        with self.assertRaisesRegex(RuntimeError,'hashes differ'):
            ja.cmd_restore(argparse.Namespace(job=self.src.name,to=str(self.d/'restore bad')))

if __name__=='__main__':unittest.main()
