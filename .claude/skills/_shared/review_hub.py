"""One local launchd registration for new review pages, with their original ports.

Page registrations are private JSON files, never additional LaunchAgents. The hub
only binds loopback and uses the existing review handler/cache/audio helper.
Existing per-page LaunchAgents remain in place until explicitly retired.
"""
import argparse
import contextlib
import fcntl
import functools
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import resource
import signal
import socket
import subprocess
import sys
import threading
import time
import urllib.request

LABEL = 'com.absbyai.review-hub'


def hub_root():
    return Path.home() / 'Library/Application Support/AbsByAI Review Hub'


def atomic_bytes(path, data):
    if path.exists() and path.read_bytes() == data:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f'.{path.name}.{os.getpid()}.{threading.get_ident()}.tmp')
    temporary.write_bytes(data)
    temporary.replace(path)
    return True


def atomic_json(path, value):
    return atomic_bytes(path, json.dumps(value, sort_keys=True, indent=2).encode())


@contextlib.contextmanager
def registration_lock(base):
    base.mkdir(parents=True, exist_ok=True, mode=0o700)
    with (base / 'registration.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def entry_path(port, base=None):
    return (base or hub_root()) / 'pages' / f'{port}.json'


def ensure_service(base):
    """Install once; an ordinary new page does not write/reload this plist."""
    runtime_script = base / 'review_hub.py'
    atomic_bytes(runtime_script, Path(__file__).read_bytes())
    plist = Path.home() / 'Library/LaunchAgents' / f'{LABEL}.plist'
    target = f'gui/{os.getuid()}/{LABEL}'
    domain = f'gui/{os.getuid()}'
    config = {'Label': LABEL,
              'ProgramArguments': [sys.executable, str(runtime_script), '--serve'],
              'RunAtLoad': True, 'KeepAlive': True, 'ProcessType': 'Background',
              'ThrottleInterval': 10,
              'StandardOutPath': str(base / 'hub.log'),
              'StandardErrorPath': str(base / 'hub.log')}
    fresh = not plist.exists()
    if fresh:
        atomic_bytes(plist, plistlib.dumps(config))
    else:
        previous = plistlib.loads(plist.read_bytes())
        # Keep the established interpreter and permissions across clients.
        args = previous.get('ProgramArguments', [])
        # Compare real locations: after a Mac migration the plist may name the same folder through an
        # old-username symlink (/Users/danielrose -> /Users/danrrose on the M6, 2026-11-14).
        same_script = len(args) == 3 and Path(args[1]).resolve() == runtime_script.resolve()
        if previous.get('Label') != LABEL or not same_script or args[2] != '--serve':
            raise RuntimeError(f'Unexpected existing shared-review configuration: {plist}')
    loaded = subprocess.run(['launchctl', 'print', target], capture_output=True).returncode == 0
    if not loaded:
        if fresh:
            subprocess.run(['launchctl', 'enable', target], check=True, capture_output=True)
        subprocess.run(['launchctl', 'bootstrap', domain, str(plist)], check=True, capture_output=True)
    return fresh


def managed(port, root, worker_source, snapshot, health, remove=False):
    """Refresh one cached review and register its port with the shared process."""
    root = Path(root).resolve()
    base = hub_root()
    entry = entry_path(port, base)
    runtime = Path.home() / 'Library/Application Support/AbsByAI Reviews' / str(port)
    cache = runtime / 'page'
    with registration_lock(base):
        if remove:
            if entry.exists():
                entry.unlink()
            # Preserve the cache. Removing a listener never deletes delivery files.
            print(f'Removed shared review listener on {port}. Cached page and original files retained.')
            return
        if entry.exists():
            old = json.loads(entry.read_text())
            if Path(old['root']).resolve() != root:
                raise RuntimeError(f'Port {port} is registered to another review. Use another port or --remove first.')
        else:
            with socket.socket() as probe:
                if probe.connect_ex(('127.0.0.1', port)) == 0:
                    raise RuntimeError(f'Port {port} is already in use; no existing listener was replaced.')
            manifest = runtime / 'manifest.json'
            if manifest.exists() and Path(json.loads(manifest.read_text())['source']).resolve() != root:
                raise RuntimeError(f'Port {port} has another cached review. Use another port to preserve its link.')
        runtime.mkdir(parents=True, exist_ok=True)
        worker = runtime / 'review_server.py'
        atomic_bytes(worker, Path(worker_source).read_bytes())
        atomic_bytes(runtime / 'review_player.js', Path(worker_source).with_name('review_player.js').read_bytes())
        records = snapshot(root, cache)
        atomic_json(runtime / 'manifest.json', {'source': str(root), 'files': records})
        # Service creation is independent of this page entry. It happens only once.
        fresh_service = ensure_service(base)
        atomic_json(entry, {'port': port, 'root': str(root), 'cache': str(cache), 'worker': str(worker)})
    # The first cold Python/launchd start can be slow on a busy Mac. Later pages
    # only need the registry poll and normally become ready within a second.
    deadline = time.monotonic() + (45 if fresh_service else 15)
    while time.monotonic() < deadline:
        state = health(port)
        if state and state.get('root') == str(root) and state.get('served_root') == str(cache) and state.get('shared_hub'):
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/', timeout=2) as response:
                if response.status != 200:
                    raise RuntimeError('Cached review page did not load')
            print(f'Managed review ready: http://127.0.0.1:{port}/')
            print(f'Shared local review service; survives crashes and login. {len(records)} linked files cached locally.')
            return
        time.sleep(0.1)
    try:
        status = json.loads((base / 'status.json').read_text())
        detail = status.get('errors', {}).get(str(port), 'listener did not become ready')
    except (OSError, ValueError):
        detail = 'shared review process did not become ready'
    raise RuntimeError(f'Review {port} failed: {detail}. Read {base / "hub.log"}')


class Hub:
    def __init__(self, base):
        self.base = Path(base)
        self.listeners = {}
        self.stop = threading.Event()
        self.errors = {}

    def start_page(self, entry):
        port = int(entry['port'])
        if not 1024 <= port <= 65535:
            raise ValueError('review port must be between 1024 and 65535')
        worker_path = Path(entry['worker'])
        spec = importlib.util.spec_from_file_location(f'review_page_{port}', worker_path)
        worker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(worker)
        source_root, cache = str(entry['root']), str(entry['cache'])
        class Handler(worker.Handler):
            def do_GET(self):
                if self.path == '/__review_health':
                    data = json.dumps({'root': source_root, 'served_root': cache,
                                       'available': Path(cache).is_dir(), 'pid': os.getpid(),
                                       'shared_hub': True}).encode()
                    response = self.memory_response(data, 'application/json')
                    with response:
                        self.copyfile(response, self.wfile)
                else:
                    super().do_GET()
        app = worker.Server(('127.0.0.1', port), functools.partial(Handler, directory=cache))
        thread = threading.Thread(target=app.serve_forever, kwargs={'poll_interval': 0.1}, daemon=True)
        thread.start()
        self.listeners[port] = (dict(entry), app, thread)

    def stop_page(self, port):
        _, app, thread = self.listeners.pop(port)
        app.shutdown()
        app.server_close()
        thread.join(timeout=5)

    def reconcile(self):
        wanted = {}
        self.errors = {}
        for path in sorted((self.base / 'pages').glob('*.json')):
            try:
                entry = json.loads(path.read_text())
                port = int(entry['port'])
                if path.stem != str(port):
                    raise ValueError('registry filename and port differ')
                wanted[port] = entry
            except (OSError, ValueError, KeyError) as error:
                self.errors[path.stem] = str(error)
        for port, (old, _, _) in list(self.listeners.items()):
            if wanted.get(port) != old:
                self.stop_page(port)
        for port, entry in wanted.items():
            if port not in self.listeners:
                try:
                    self.start_page(entry)
                except Exception as error:
                    self.errors[str(port)] = str(error)
        atomic_json(self.base / 'status.json', {'pid': os.getpid(),
                    'listening': sorted(self.listeners), 'errors': self.errors})

    def run(self):
        # One process owns the loopback sockets instead of adding fds to launchd.
        soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
        desired = min(4096, hard) if hard != resource.RLIM_INFINITY else 4096
        if soft < desired:
            resource.setrlimit(resource.RLIMIT_NOFILE, (desired, hard))
        try:
            while not self.stop.is_set():
                self.reconcile()
                self.stop.wait(0.25)
        finally:
            for port in list(self.listeners):
                self.stop_page(port)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', action='store_true', required=True)
    parser.add_argument('--base', type=Path)
    args = parser.parse_args()
    base = args.base or Path(__file__).resolve().parent
    base.mkdir(parents=True, exist_ok=True)
    # A lock also protects standalone tests/manual recovery from duplicate hubs.
    with (base / 'process.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('Another review hub already owns this registry')
        hub = Hub(base)
        for signum in (signal.SIGTERM, signal.SIGINT):
            signal.signal(signum, lambda *_: hub.stop.set())
        hub.run()


if __name__ == '__main__':
    main()
