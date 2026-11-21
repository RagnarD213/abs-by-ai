"""Check registration churn without changing real macOS jobs or permissions."""
import importlib.util
from pathlib import Path
import plistlib
import subprocess
import tempfile
import unittest
from unittest.mock import patch, MagicMock

HERE = Path(__file__).resolve().parent
if not (HERE / 'review_server.py').exists():
    HERE = HERE.parent
spec = importlib.util.spec_from_file_location('review_server', HERE / 'review_server.py')
server = importlib.util.module_from_spec(spec)
spec.loader.exec_module(server)


class Registration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.plist = Path(self.tmp.name) / 'review.plist'
        self.config = {'Label': 'com.absbyai.review.9999', 'ProgramArguments': ['/usr/bin/python3', 'worker.py']}
        self.plist.write_bytes(plistlib.dumps(self.config))

    def run_registration(self, *, loaded=True, changed=False, config=None):
        def execute(args, **kwargs):
            return subprocess.CompletedProcess(args, 0 if loaded or args[1] != 'print' else 113)
        with patch.object(server.subprocess, 'run', side_effect=execute) as run:
            result = server.register_review_service(self.plist, config or self.config, 'gui/501', changed)
        return result, [call.args[0][1] for call in run.call_args_list]

    def test_refresh_keeps_registration_bytes_mtime_and_running_job(self):
        before = self.plist.stat().st_mtime_ns
        result, calls = self.run_registration()
        self.assertFalse(result)
        self.assertEqual(calls, ['print'])
        self.assertEqual(self.plist.stat().st_mtime_ns, before)

    def test_worker_update_reloads_without_rewriting_plist_or_enabling(self):
        before = self.plist.stat().st_mtime_ns
        result, calls = self.run_registration(changed=True)
        self.assertTrue(result)
        self.assertEqual(calls, ['print', 'bootout', 'bootstrap'])
        self.assertEqual(self.plist.stat().st_mtime_ns, before)

    def test_unloaded_existing_service_recovers_without_changing_permission(self):
        result, calls = self.run_registration(loaded=False)
        self.assertTrue(result)
        self.assertEqual(calls, ['print', 'bootstrap'])

    def test_new_service_is_registered_once(self):
        self.plist.unlink()
        result, calls = self.run_registration(loaded=False)
        self.assertTrue(result)
        self.assertEqual(calls, ['print', 'enable', 'bootstrap'])
        self.assertEqual(plistlib.loads(self.plist.read_bytes()), self.config)

    def test_changed_configuration_is_applied(self):
        config = dict(self.config, ThrottleInterval=3)
        result, calls = self.run_registration(config=config)
        self.assertTrue(result)
        self.assertEqual(calls, ['print', 'bootout', 'bootstrap'])
        self.assertEqual(plistlib.loads(self.plist.read_bytes()), config)

    def test_managed_page_refresh_updates_cache_without_reloading_service(self):
        home = Path(self.tmp.name).resolve()
        source = home / 'source'
        source.mkdir()
        (source / 'index.html').write_text('<html><body>first</body></html>')
        cache = home / 'Library/Application Support/AbsByAI Reviews/9999/page'
        legacy = home / 'Library/LaunchAgents/com.absbyai.review.9999.plist'
        legacy.parent.mkdir(parents=True)
        legacy.write_bytes(plistlib.dumps(server.on_demand_plist('com.absbyai.review.9999', server.sys.executable, cache.parent / 'review_server.py', 9999, cache, source, cache.parent / 'server.log')))
        state = {'root': str(source), 'served_root': str(cache)}
        def execute(args, **kwargs):
            exists = (home / 'Library/LaunchAgents/com.absbyai.review.9999.plist').exists()
            return subprocess.CompletedProcess(args, 0 if exists or args[1] != 'print' else 113)
        sock = MagicMock()
        sock.__enter__.return_value.connect_ex.return_value = 1
        response = MagicMock()
        response.__enter__.return_value.status = 200
        with patch.object(server.Path, 'home', return_value=home), patch('socket.socket', return_value=sock), patch.object(server, 'health', return_value=state), patch.object(server.urllib.request, 'urlopen', return_value=response), patch.object(server.subprocess, 'run', side_effect=execute) as run:
            server.managed(9999, source)
            plist = home / 'Library/LaunchAgents/com.absbyai.review.9999.plist'
            before = plist.stat().st_mtime_ns
            run.reset_mock()
            (source / 'index.html').write_text('<html><body>updated</body></html>')
            server.managed(9999, source)
            self.assertIn(b'updated', (cache / 'index.html').read_bytes())
            self.assertEqual(plist.stat().st_mtime_ns, before)
            self.assertEqual([call.args[0][1] for call in run.call_args_list], ['print'])


if __name__ == '__main__':
    unittest.main()
