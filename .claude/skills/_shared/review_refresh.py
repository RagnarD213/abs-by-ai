#!/usr/bin/env python3
"""Push the current review_server.py and review_player.js into EVERY existing review page on this Mac, then restart
the shared review hub so the pages pick them up (same links; a page reload is enough).

    python3 .claude/skills/_shared/review_refresh.py            # refresh all, restart the hub, verify
    python3 .claude/skills/_shared/review_refresh.py --dry-run  # list what would change

Why (2026-11-16): each page runs from its own runtime copy under ~/Library/Application Support/AbsByAI Reviews/<port>/,
so a fix to the shared files (here: real Full screen through VLC) reached only pages built after the fix. Run this after
any change to review_server.py or review_player.js, on each Mac (the M2's pages open on the M6 through its own copies).
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import urllib.request

HERE = Path(__file__).resolve().parent
RUNTIMES = Path.home() / 'Library/Application Support/AbsByAI Reviews'
HUB = Path.home() / 'Library/Application Support/AbsByAI Review Hub'
HUB_LABEL = 'com.absbyai.review-hub'


def copy_if_changed(src, dst, dry):
    data = src.read_bytes()
    if dst.exists() and dst.read_bytes() == data:
        return False
    if not dry:
        tmp = dst.with_name(dst.name + '.tmp')
        tmp.write_bytes(data)
        os.replace(tmp, dst)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    server, player = HERE / 'review_server.py', HERE / 'review_player.js'
    changed = pages = 0
    for runtime in sorted(p for p in RUNTIMES.glob('*') if (p / 'review_server.py').exists()):
        pages += 1
        c = copy_if_changed(server, runtime / 'review_server.py', a.dry_run)
        c |= copy_if_changed(player, runtime / 'review_player.js', a.dry_run)
        if (runtime / 'page' / '__review_player.js').exists():
            c |= copy_if_changed(player, runtime / 'page' / '__review_player.js', a.dry_run)
        changed += c
    print(f'{pages} review pages; {changed} updated{" (dry run)" if a.dry_run else ""}')
    if a.dry_run or not changed:
        return
    # The hub imports each page's worker when it starts listening: restart it to load the new server code.
    def hub_pid():
        try:
            return json.loads((HUB / 'status.json').read_text()).get('pid')
        except (OSError, ValueError):
            return None
    old_pid = hub_pid()
    subprocess.run(['/bin/launchctl', 'kickstart', '-k', f'gui/{os.getuid()}/{HUB_LABEL}'], check=False)
    ports = []
    deadline = time.time() + 60
    while time.time() < deadline:
        try:
            ports = json.loads((HUB / 'status.json').read_text()).get('listening', [])
        except (OSError, ValueError):
            ports = []
        if ports and hub_pid() not in (None, old_pid):
            time.sleep(2)       # the new hub has written status; give its listeners a moment
            break
        time.sleep(0.5)
    ok = bad = 0
    for port in ports:
        try:
            req = urllib.request.Request(f'http://127.0.0.1:{port}/__fullscreen', data=b'{}', method='POST',
                                         headers={'Content-Type': 'application/json'})
            try:
                urllib.request.urlopen(req, timeout=3)
            except urllib.error.HTTPError as e:     # 400 {"ok": false} = the endpoint exists; 404/501 = old code
                if e.code != 400:
                    raise
            ok += 1
        except Exception:
            bad += 1
    print(f'hub restarted; {ok} listening pages answer the new full-screen endpoint, {bad} do not')


if __name__ == '__main__':
    main()
