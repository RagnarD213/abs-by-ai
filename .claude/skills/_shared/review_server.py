"""Durable local video reviews, with byte-range seeking.

review_server.py PORT [DIR]           macOS: install/start a login service
review_server.py PORT DIR --serve     foreground worker (tests/launchd)
review_server.py PORT --remove        stop/remove this managed review service

The same URL survives chat completion, process crashes and the next Mac login.
External media must remain mounted. No media is uploaded.
"""
import argparse
import functools
import http.server
import json
import os
from pathlib import Path
import plistlib
import re
import socketserver
import subprocess
import sys
import time
import urllib.request


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/__review_health':
            body = json.dumps({'root': str(Path(self.directory).resolve()),
                               'available': Path(self.directory).is_dir(),
                               'pid': os.getpid()}).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()

    def send_head(self):
        self._left = None
        if not Path(self.directory).is_dir():
            self.send_error(503, 'Review drive unavailable. Reconnect it and reload this page.')
            return None
        path = self.translate_path(self.path)
        m = re.fullmatch(r'bytes=(\d*)-(\d*)', self.headers.get('Range', ''))
        if not m or not os.path.isfile(path):
            return super().send_head()
        size = os.path.getsize(path)
        a, b = m.groups()
        if not a and not b:
            return super().send_head()
        start = int(a) if a else max(0, size - int(b))
        end = min(int(b), size - 1) if a and b else size - 1
        if size == 0 or start >= size or start > end or (not a and int(b) == 0):
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return None
        f = open(path, 'rb')
        f.seek(start)
        self._left = end - start + 1
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(self._left))
        self.send_header('Last-Modified', self.date_time_string(os.path.getmtime(path)))
        self.end_headers()
        return f

    def end_headers(self):
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def copyfile(self, source, outputfile):
        left = getattr(self, '_left', None)
        self._left = None
        try:
            if left is None:
                return super().copyfile(source, outputfile)
            while left > 0:
                buf = source.read(min(256 * 1024, left))
                if not buf:
                    break
                outputfile.write(buf)
                left -= len(buf)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *args):
        pass


class Server(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def health(port):
    try:
        with urllib.request.urlopen(f'http://127.0.0.1:{port}/__review_health', timeout=2) as r:
            return json.load(r)
    except (OSError, ValueError):
        return None


def managed(port, root, remove=False):
    label = f'com.absbyai.review.{port}'
    domain = f'gui/{os.getuid()}'
    target = f'{domain}/{label}'
    plist = Path.home() / 'Library/LaunchAgents' / f'{label}.plist'
    runtime = Path.home() / 'Library/Application Support/AbsByAI Reviews' / str(port)
    if remove:
        subprocess.run(['launchctl', 'bootout', target], capture_output=True)
        if plist.exists():
            plist.unlink()
        print(f'Removed review service on {port}. Review media retained.')
        return
    if plist.exists():
        old = plistlib.loads(plist.read_bytes())
        if Path(old['ProgramArguments'][3]).resolve() != root:
            raise RuntimeError(f'Port {port} is registered to another review. Use another port or --remove first.')
    # Refuse to displace another service, including a legacy review, without identifying it first.
    import socket
    with socket.socket() as s:
        occupied = s.connect_ex(('127.0.0.1', port)) == 0
    state = health(port) if occupied else None
    if occupied and (not plist.exists() or not state or Path(state['root']) != root):
        raise RuntimeError(f'Port {port} is already in use. Identify its owner before migrating it.')
    runtime.mkdir(parents=True, exist_ok=True)
    worker = runtime / 'review_server.py'
    content = Path(__file__).read_bytes()
    if not worker.exists() or worker.read_bytes() != content:
        temporary = runtime / 'review_server.py.tmp'
        temporary.write_bytes(content)
        temporary.replace(worker)
    log = runtime / 'server.log'
    args = [sys.executable, str(worker), str(port), str(root), '--serve']
    config = {'Label': label, 'ProgramArguments': args, 'RunAtLoad': True,
              'KeepAlive': True, 'ThrottleInterval': 3,
              'StandardOutPath': str(log), 'StandardErrorPath': str(log)}
    plist.parent.mkdir(parents=True, exist_ok=True)
    plist.write_bytes(plistlib.dumps(config))
    subprocess.run(['launchctl', 'bootout', target], capture_output=True)
    subprocess.run(['launchctl', 'enable', target], check=True, capture_output=True)
    subprocess.run(['launchctl', 'bootstrap', domain, str(plist)], check=True, capture_output=True)
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        state = health(port)
        if state and Path(state['root']) == root:
            print(f'Managed review ready: http://127.0.0.1:{port}/')
            print(f'Automatic restart and login startup enabled. Media available: {state["available"]}')
            return
        time.sleep(.25)
    raise RuntimeError(f'Review did not start. Read {log}')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('port', type=int)
    p.add_argument('directory', nargs='?', default='.')
    p.add_argument('--serve', action='store_true', help='Foreground worker; does not install a service')
    p.add_argument('--remove', action='store_true')
    a = p.parse_args()
    root = Path(a.directory).resolve()
    if not 1024 <= a.port <= 65535:
        p.error('Use a local port between 1024 and 65535')
    # Existing older launch agents already supervise the foreground command. Avoid nested installation.
    legacy_agent = os.getppid() == 1 and not a.remove
    if sys.platform == 'darwin' and not a.serve and not legacy_agent:
        managed(a.port, root, a.remove)
    elif a.remove:
        p.error('--remove requires macOS launchd')
    else:
        handler = functools.partial(Handler, directory=str(root))
        Server(('127.0.0.1', a.port), handler).serve_forever()


if __name__ == '__main__':
    main()
