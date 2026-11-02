"""Retire idle review-page login services so launchd never runs out of file handles.

review_retire.py [--days N] [--max N] [--dry-run]   retire idle com.absbyai.review.PORT launch agents
review_retire.py --restore PORT                     bring one back on the same link
review_retire.py --list                             active and retired counts

Why (2026-11-02): every managed review (review_server.py) installs a launch agent whose listening socket launchd
itself holds, and nothing ever removed them. At 136 agents launchd hit "Too many open files" (errno 24), could no
longer start any process, and the Mac froze twice, once during boot, until it was forced off.

Retiring boots the agent out and moves its plist into the review's own folder as launchagent.plist.retired. The cached
page and the source files are untouched. A review is idle when its plist, manifest and server.log are all older than
--days (3); after that the oldest idle ones go until at most --max (40) stay active. Ports linked from
AI_COORDINATION.md are always kept. Runs every 30 minutes from ~/bin/claude-cleanup.sh.
"""
import argparse
import os
from pathlib import Path
import re
import subprocess
import time

AGENTS = Path.home() / 'Library/LaunchAgents'
RUNTIME = Path.home() / 'Library/Application Support/AbsByAI Reviews'
BOARD = Path(__file__).resolve().parents[3] / 'AI_COORDINATION.md'
DOMAIN = f'gui/{os.getuid()}'
IDLE_DAYS = 3.0
MAX_ACTIVE = 40


def _last_used(port, plist):
    times = [plist.stat().st_mtime]
    for name in ('manifest.json', 'server.log'):
        f = RUNTIME / str(port) / name
        if f.exists():
            times.append(f.stat().st_mtime)
    return max(times)


def _board_ports():
    try:
        return {int(p) for p in re.findall(r'127\.0\.0\.1:(\d{4,5})', BOARD.read_text())}
    except OSError:
        return set()


def active():
    out = []
    for plist in AGENTS.glob('com.absbyai.review.*.plist'):
        port = plist.stem.rsplit('.', 1)[-1]
        if port.isdigit():
            out.append((int(port), plist, _last_used(port, plist)))
    return out


def retire(port, plist, dry_run=False):
    if dry_run:
        return True
    dest = RUNTIME / str(port)
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(['launchctl', 'bootout', f'{DOMAIN}/{plist.stem}'], capture_output=True)
    plist.replace(dest / 'launchagent.plist.retired')
    return True


def restore(port):
    saved = RUNTIME / str(port) / 'launchagent.plist.retired'
    if not saved.exists():
        raise SystemExit(f'No retired review on port {port}.')
    plist = AGENTS / f'com.absbyai.review.{port}.plist'
    saved.replace(plist)
    os.utime(plist)                                        # counts as fresh use, so the next sweep keeps it
    subprocess.run(['launchctl', 'enable', f'{DOMAIN}/{plist.stem}'], capture_output=True)
    subprocess.run(['launchctl', 'bootstrap', DOMAIN, str(plist)], check=True, capture_output=True)
    print(f'Restored: http://127.0.0.1:{port}/')


def sweep(days=IDLE_DAYS, cap=MAX_ACTIVE, dry_run=False):
    keep = _board_ports()
    now = time.time()
    rows = sorted(active(), key=lambda r: r[2])            # oldest use first
    gone = [r for r in rows if r[0] not in keep and now - r[2] > days * 86400]
    left = [r for r in rows if r not in gone]
    extra = len(left) - cap
    if extra > 0:
        gone += [r for r in left if r[0] not in keep][:extra]
    for port, plist, used in gone:
        retire(port, plist, dry_run)
    verb = 'would retire' if dry_run else 'retired'
    print(f'{verb} {len(gone)} of {len(rows)} review services; {len(rows) - len(gone)} stay active'
          + (f' (ports {", ".join(str(r[0]) for r in gone)})' if gone and dry_run else ''))
    return len(gone)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--days', type=float, default=IDLE_DAYS)
    p.add_argument('--max', type=int, default=MAX_ACTIVE)
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--restore', type=int, metavar='PORT')
    p.add_argument('--list', action='store_true')
    a = p.parse_args()
    if a.restore:
        return restore(a.restore)
    if a.list:
        retired = len(list(RUNTIME.glob('*/launchagent.plist.retired'))) if RUNTIME.is_dir() else 0
        print(f'{len(active())} active, {retired} retired')
        return
    sweep(a.days, a.max, a.dry_run)


if __name__ == '__main__':
    main()
