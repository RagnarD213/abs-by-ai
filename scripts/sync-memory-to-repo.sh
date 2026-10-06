#!/bin/bash
# Copies Claude's local memory folder into Docs/memory/ so cloud sessions can read it.
#
# Usage: scripts/sync-memory-to-repo.sh [--check] [--add <name> ...]
#
#   (no flags)  copy every allowed entry, rebuild Docs/memory/MEMORY.md, run the secret scan.
#   --check     report what would change and run the scan; write nothing.
#   --add name  also publish a `type: user` entry (those are held back by default).
#
# An entry that exists only in Docs/memory/ (a cloud session wrote it) is kept and reported.
# An entry newly listed in .repo-private is removed from Docs/memory/ on the next run.
#
# The repo is PUBLIC. Three guards, all must pass:
#   1. <memory>/.repo-private   names that are never copied (one per line, no .md).
#   2. <memory>/.repo-redacted  names whose repo copy is hand-written; never overwritten here.
#   3. The scan below (keys, phone numbers, unknown emails, addresses, blocked terms).
#      Any hit stops the run with exit 3 and nothing is left half-copied.
# Both lists live in the local memory folder on purpose: they are not in the repo.
# No list on this machine = the script refuses to run.
#
# This script does not commit. After it passes:
#   scripts/git/safe-push.sh -m "Sync memory to repo" -- Docs/memory
#
# Exit codes: 0 ok, 1 refused to start, 3 scan found something.

set -u
top=$(git rev-parse --show-toplevel 2>/dev/null) || { echo "sync-memory: not inside the repo" >&2; exit 1; }
slug=$(printf '%s' "$top" | sed 's|[^A-Za-z0-9]|-|g')
src="${ABS_MEMORY_DIR:-$HOME/.claude/projects/$slug/memory}"
dst="$top/Docs/memory"

if [ ! -d "$src" ]; then
  echo "sync-memory: no local memory folder at $src."
  echo "In a cloud session this is expected: write new entries straight into Docs/memory/ and push."
  exit 0
fi
[ -f "$src/.repo-private" ] || { echo "sync-memory: refused, $src/.repo-private is missing. Without it nothing is known to be private." >&2; exit 1; }

exec python3 - "$src" "$dst" "$@" <<'PY'
import os, re, sys, shutil, filecmp

src, dst, args = sys.argv[1], sys.argv[2], sys.argv[3:]
check = '--check' in args
added = set()
i = 0
while i < len(args):
    if args[i] == '--add' and i + 1 < len(args):
        added.add(args[i + 1].replace('.md', '')); i += 2
    else:
        i += 1

def names(path):
    if not os.path.exists(path): return set()
    return {l.strip().replace('.md', '') for l in open(path) if l.strip() and not l.startswith('#')}

private = names(os.path.join(src, '.repo-private'))
redacted = names(os.path.join(src, '.repo-redacted'))
blocked_path = os.path.join(src, '.repo-blocked-terms')
blocked = [re.compile(l.strip(), re.I) for l in open(blocked_path) if l.strip() and not l.startswith('#')] \
    if os.path.exists(blocked_path) else []

OK_EMAIL = re.compile(r'^(dan@absbyai\.com|noreply@absbyai\.com|support@absbyai\.com|danroseconsulting(\+[a-z0-9-]+)?@gmail\.com|'
                      r'[^@]+@(example\.com|local\.test|mailinator\.com)|noreply@anthropic\.com|git@github\.com)$', re.I)
OK_NUMBER = {'342-717-0837', '324-458-6445'}   # Google Ads account ids, already in the public board
SCANS = [
    ('key or token', re.compile(r'(sk_live_[A-Za-z0-9]{8,}|sk_test_[A-Za-z0-9]{8,}|pk_live_[A-Za-z0-9]{8,}|rk_live_[A-Za-z0-9]{8,}|'
                                r'whsec_[A-Za-z0-9]{8,}|\bre_[A-Za-z0-9]{16,}|AIza[0-9A-Za-z_-]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_\w{10,}|'
                                r'xox[bap]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|eyJ[A-Za-z0-9_-]{20,}\.|r8_[A-Za-z0-9]{20,}|ph[cx]_[A-Za-z0-9]{20,}|'
                                r'sk-ant-[A-Za-z0-9-]{10,}|\bsk-[A-Za-z0-9]{24,}|ya29\.[A-Za-z0-9_-]{10,}|1//[0-9A-Za-z_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY)')),
    ('password or PIN value', re.compile(r'(?i)\b(password|passcode|passphrase|recovery pin|pin)\b\**\s*((:|=)\s*\**`?[A-Za-z0-9!@#$%^&*_-]{4,}|is\s+\**`?(?=[A-Za-z!@#$%^&*_-]*\d)[A-Za-z0-9!@#$%^&*_-]{4,})')),
    ('SSN-shaped number', re.compile(r'\b\d{3}-\d{2}-\d{4}\b')),
    ('street address', re.compile(r'\b\d{2,5}\s+[A-Z][A-Za-z]+\s+(Rd|Road|St|Street|Ave|Avenue|Dr|Drive|Ln|Lane|Blvd|Way|Ct|Court|Cir|Trail|Pkwy)\b\.?')),
]
PHONE = re.compile(r'(?<![\d-])\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?![\d-])')
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')

def scan(name, text):
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for label, rx in SCANS:
            if rx.search(line): hits.append((name, n, label))
        for m in PHONE.finditer(line):
            if m.group(0).strip('()') not in OK_NUMBER: hits.append((name, n, 'phone number'))
        for m in EMAIL.finditer(line):
            if not OK_EMAIL.match(m.group(0)): hits.append((name, n, 'email address'))
        for rx in blocked:
            if rx.search(line): hits.append((name, n, 'blocked term /%s/' % rx.pattern))
    return hits

def mem_type(text):
    m = re.search(r'^\s*type:\s*(\w+)', text, re.M)
    return m.group(1) if m else ''

local = sorted(f[:-3] for f in os.listdir(src) if f.endswith('.md') and f != 'MEMORY.md')
in_repo = {f[:-3] for f in os.listdir(dst)} if os.path.isdir(dst) else set()
in_repo = {n for n in in_repo if n != 'MEMORY'}

to_copy, held, stale_redacted, hits = [], [], [], []
for n in local:
    if n in private: continue
    p = os.path.join(src, n + '.md')
    text = open(p, errors='replace').read()
    if n in redacted:
        q = os.path.join(dst, n + '.md')
        if not os.path.exists(q): held.append((n, 'redacted entry has no hand-written repo copy yet'))
        elif os.path.getmtime(p) > os.path.getmtime(q): stale_redacted.append(n)
        continue
    if mem_type(text) == 'user' and n not in in_repo and n not in added:
        held.append((n, "type: user, held back. Publish with --add %s, or list it in .repo-private" % n)); continue
    h = scan(n + '.md', text)
    if h: hits += h; continue
    to_copy.append(n)

# the hand-written copies get scanned too
for n in sorted(redacted):
    q = os.path.join(dst, n + '.md')
    if os.path.exists(q): hits += scan('Docs/memory/' + n + '.md', open(q, errors='replace').read())

if hits:
    print('sync-memory: STOPPED. The scan found %d item(s). Nothing was copied.' % len(hits))
    for name, n, label in hits: print('  %s:%d  %s' % (name, n, label))
    print('Fix the local entry, or add its name to %s/.repo-private (or .repo-redacted and hand-write the repo copy).' % src)
    sys.exit(3)

publish = set(to_copy) | {n for n in redacted if os.path.exists(os.path.join(dst, n + '.md'))}
changed = [n for n in to_copy if not (os.path.exists(os.path.join(dst, n + '.md')) and
                                       filecmp.cmp(os.path.join(src, n + '.md'), os.path.join(dst, n + '.md'), shallow=False))]
gone = sorted(n for n in in_repo if n in private)                       # newly marked private: pull it
repo_only = sorted(n for n in in_repo if n not in publish and n not in private)   # written in a cloud session
publish |= set(repo_only)

# index: keep the local index lines whose entry is published
index = []
for line in open(os.path.join(src, 'MEMORY.md'), errors='replace'):
    m = re.match(r'\s*- \[[^\]]*\]\(([^)]+)\.md\)', line)
    if m is None or m.group(1) in publish: index.append(line)
if os.path.exists(os.path.join(dst, 'MEMORY.md')):                    # keep index lines of cloud-written entries
    for line in open(os.path.join(dst, 'MEMORY.md'), errors='replace'):
        m = re.match(r'\s*- \[[^\]]*\]\(([^)]+)\.md\)', line)
        if m and m.group(1) in repo_only and line not in index: index.append(line)
index_text = ''.join(index)
hits = scan('MEMORY.md (index)', index_text)
if hits:
    print('sync-memory: STOPPED. The index would carry %d flagged line(s). Nothing was copied.' % len(hits))
    for name, n, label in hits: print('  %s:%d  %s' % (name, n, label))
    sys.exit(3)

print('sync-memory: %d local entries, %d private, %d redacted, %d to publish (%d new or changed), %d to remove from the repo copy.'
      % (len(local), len([n for n in local if n in private]), len(redacted), len(publish), len(changed), len(gone)))
for n, why in held: print('  HELD  %s: %s' % (n, why))
for n in repo_only: print('  REPO-ONLY %s: exists in Docs/memory but not in local memory (written in a cloud session?). Kept. Copy it into local memory if it should apply here too.' % n)
for n in stale_redacted: print('  STALE %s: the local entry changed after its hand-written repo copy. Update Docs/memory/%s.md by hand.' % (n, n))
if check:
    for n in changed: print('  would copy   %s' % n)
    for n in gone: print('  would remove %s' % n)
    sys.exit(0)

os.makedirs(dst, exist_ok=True)
for n in changed: shutil.copyfile(os.path.join(src, n + '.md'), os.path.join(dst, n + '.md'))
for n in gone: os.remove(os.path.join(dst, n + '.md'))
open(os.path.join(dst, 'MEMORY.md'), 'w').write(index_text)
print('sync-memory: done. Scan clean. Now: scripts/git/safe-push.sh -m "Sync memory to repo" -- Docs/memory')
PY
