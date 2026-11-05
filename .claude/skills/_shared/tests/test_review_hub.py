import importlib.util
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
if not (HERE / 'review_hub.py').exists():
    HERE = HERE.parent
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
hub = load('hub_test', HERE / 'review_hub.py')
worker = load('worker_test', HERE / 'review_server.py')

def free_port():
    with socket.socket() as probe:
        probe.bind(('127.0.0.1', 0))
        return probe.getsockname()[1]

def get(port, path='/', headers=None):
    with urllib.request.urlopen(urllib.request.Request(f'http://127.0.0.1:{port}{path}', headers=headers or {}), timeout=3) as response:
        return response.status, dict(response.headers), response.read()


class SharedReview(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name).resolve()
        self.base = self.home / 'hub'
        self.base.mkdir()
        self.process = None
        self.start()
        self.addCleanup(self.stop)

    def start(self):
        self.process = subprocess.Popen([sys.executable, str(HERE / 'review_hub.py'), '--serve', '--base', str(self.base)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
        if self.process:
            self.process.communicate(timeout=10)

    def register(self, port, root):
        with patch.object(hub.Path, 'home', return_value=self.home), patch.object(hub, 'hub_root', return_value=self.base), patch.object(hub, 'ensure_service') as install:
            hub.managed(port, root, HERE / 'review_server.py', worker.snapshot, worker.health)
        self.assertEqual(install.call_count, 1)

    def page(self, name):
        root = self.home / name
        root.mkdir()
        (root / 'index.html').write_text(f'<html><head><title>{name}</title></head><body>{name}<video muted controls autoplay src="clip.mp4"></video><audio muted controls src="clip.mp4"></audio></body></html>')
        (root / 'clip.mp4').write_bytes(bytes(range(256)) * 20)
        return root

    def test_multiple_pages_keep_isolated_roots_same_process_and_range_audio_helper(self):
        first, second = free_port(), free_port()
        a, b = self.page('alpha'), self.page('beta')
        self.register(first, a)
        self.register(second, b)
        for port, root in [(first, a), (second, b)]:
            state = worker.health(port)
            self.assertEqual(state['root'], str(root))
            self.assertEqual(state['pid'], self.process.pid)
            self.assertTrue(state['shared_hub'])
            status, _, body = get(port)
            self.assertEqual(status, 200)
            self.assertIn(b'<video muted controls', body)
            self.assertIn(b'<audio muted controls', body)
            self.assertEqual(body.count(b'/__review_player.js'), 1)
            self.assertIn(root.name.encode(), body)
            status, headers, data = get(port, '/clip.mp4', {'Range': 'bytes=100-149'})
            self.assertEqual(status, 206)
            self.assertEqual(headers['Content-Range'], 'bytes 100-149/5120')
            self.assertEqual(data, (root / 'clip.mp4').read_bytes()[100:150])
            _, _, helper = get(port, '/__review_player.js')
            self.assertEqual(helper, (HERE / 'review_player.js').read_bytes())
        self.assertFalse((self.home / 'Library/LaunchAgents').exists())

    def test_refresh_keeps_url_process_and_entry_while_updating_cache(self):
        port, root = free_port(), self.page('refresh')
        self.register(port, root)
        entry = hub.entry_path(port, self.base)
        stamp = entry.stat().st_mtime_ns
        (root / 'index.html').write_text('<html><body>revised<audio controls src="clip.mp4"></audio></body></html>')
        self.register(port, root)
        self.assertEqual(entry.stat().st_mtime_ns, stamp)
        self.assertEqual(worker.health(port)['pid'], self.process.pid)
        self.assertIn(b'revised', get(port)[2])

    def test_restart_reopens_registered_urls_and_cached_page_without_source_drive(self):
        port, root = free_port(), self.page('restart')
        self.register(port, root)
        self.stop()
        root.rename(root.with_name('disconnected'))
        self.start()
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            state = worker.health(port)
            if state and state.get('pid') == self.process.pid:
                break
            time.sleep(0.1)
        self.assertEqual(worker.health(port)['pid'], self.process.pid)
        self.assertIn(b'restart', get(port)[2])
        self.assertEqual(get(port, '/clip.mp4', {'Range': 'bytes=0-9'})[0], 206)

    def test_unknown_listener_and_registered_different_root_are_not_replaced(self):
        root = self.page('collision')
        with socket.socket() as existing:
            existing.bind(('127.0.0.1', 0))
            existing.listen()
            port = existing.getsockname()[1]
            with self.assertRaisesRegex(RuntimeError, 'already in use'):
                self.register(port, root)
            self.assertFalse(hub.entry_path(port, self.base).exists())
        port = free_port()
        self.register(port, root)
        with self.assertRaisesRegex(RuntimeError, 'another review'):
            self.register(port, self.page('other-root'))
        self.assertIn(b'collision', get(port)[2])

    def test_corrupt_entry_and_removing_one_page_leave_other_page_available(self):
        a, b = free_port(), free_port()
        root_a, root_b = self.page('keep'), self.page('remove')
        self.register(a, root_a)
        self.register(b, root_b)
        (self.base / 'pages/bad.json').write_text('broken')
        with patch.object(hub.Path, 'home', return_value=self.home), patch.object(hub, 'hub_root', return_value=self.base):
            hub.managed(b, root_b, HERE / 'review_server.py', worker.snapshot, worker.health, remove=True)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline and worker.health(b):
            time.sleep(0.1)
        self.assertIsNone(worker.health(b))
        self.assertEqual(get(a)[0], 200)
        cache = self.home / 'Library/Application Support/AbsByAI Reviews' / str(b) / 'page/index.html'
        self.assertTrue(cache.exists())


class ServiceRegistration(unittest.TestCase):
    def test_new_pages_do_not_rewrite_or_reload_shared_launch_agent(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp).resolve()
            base = home / 'hub'
            base.mkdir()
            loaded = False
            calls = []
            def execute(args, **kwargs):
                nonlocal loaded
                calls.append(args[1])
                if args[1] == 'bootstrap':
                    loaded = True
                return subprocess.CompletedProcess(args, 0 if loaded or args[1] != 'print' else 113)
            with patch.object(hub.Path, 'home', return_value=home), patch.object(hub.subprocess, 'run', side_effect=execute):
                self.assertTrue(hub.ensure_service(base))
                plist = home / 'Library/LaunchAgents/com.absbyai.review-hub.plist'
                stamp, contents = plist.stat().st_mtime_ns, plist.read_bytes()
                calls.clear()
                self.assertFalse(hub.ensure_service(base))
                self.assertEqual(calls, ['print'])
                self.assertEqual(plist.stat().st_mtime_ns, stamp)
                self.assertEqual(plist.read_bytes(), contents)


if __name__ == '__main__':
    unittest.main()
