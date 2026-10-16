#!/usr/bin/env python3
"""Coordination-board limits. No dependencies; --hook reads Claude's JSON on stdin."""
import datetime
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
TITLE = re.compile(r"^(?:(?:[-+*]|\d+[.)])\s+)?(?:⚠\ufe0f?\s*)*\*\*(.+?)\*\*")
BOUNDARY = re.compile(r"^(?:#{1,6}\s|\s*[-+*]\s|---\s*$)")
DATE = re.compile(r"(?<![\w/\-])(?:\d{4}-)?\d{2}-\d{2}(?![\w/\-])")


def entries(text):
    current = None
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith(('```', '~~~')):
            fenced = not fenced
        title = None if fenced else TITLE.match(line)
        if title or (not fenced and BOUNDARY.match(line)):
            if current:
                yield current
                current = None
        if title:
            current = [number, title.group(1), line]
        elif current:
            current[2] += '\n' + line
    if current:
        yield current


def has_date(text):
    # Ignore filenames, URLs and code: a dated handoff link is not an entry date.
    text = re.sub(r'`[^`]*`|https?://\S+', '', text)
    for match in DATE.finditer(text):
        value = match.group()
        try:
            datetime.date.fromisoformat(value if len(value) == 10 else '2000-' + value)
            return True
        except ValueError:
            pass
    return False


def check(path):
    try:
        text = path.read_text()
    except OSError as error:
        return [str(error)], 0
    count = len(text.split())
    errors = []
    if count > 2500:
        errors.append(f'BOARD: {count} words; limit 2,500 (remove {count - 2500}).')
    for line, title, body in entries(text):
        words = len(body.split())
        if words > 80:
            errors.append(f'line {line} [{title}]: {words} words; entry limit 80.')
        if not has_date(body):
            errors.append(f'line {line} [{title}]: no date; add YYYY-MM-DD (legacy MM-DD accepted).')
    return errors, count


def main():
    hook = sys.argv[1:] == ['--hook']
    path = ROOT / 'AI_COORDINATION.md'
    if hook:
        # Fail only the session that edited the board, so other sessions are not
        # blocked by an over-budget board they never touched.
        payload = json.load(sys.stdin)
        tool = payload.get('tool_name', '')
        tool_input = payload.get('tool_input', {}) or {}
        if tool in ('Edit', 'Write', 'MultiEdit'):
            edited = Path(tool_input.get('file_path', ''))
            if not edited.is_absolute():
                edited = Path(payload.get('cwd', str(ROOT))) / edited
            if edited.resolve() != path:
                return 0
        elif tool == 'Bash':
            if 'AI_COORDINATION.md' not in str(tool_input.get('command', '')):
                return 0
        else:
            return 0
    elif len(sys.argv) == 2:
        path = Path(sys.argv[1])
    elif len(sys.argv) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    errors, words = check(path)
    if errors:
        print('Board check FAILED:\n' + '\n'.join(errors), file=sys.stderr)
        if hook:
            print('You edited the board. Trim YOUR OWN entry only (never another session\'s), '
                  'then rerun scripts/board-check.sh.', file=sys.stderr)
        else:
            print('Compress or archive finished work, fix dates, then rerun scripts/board-check.sh.', file=sys.stderr)
        return 2 if hook else 1  # PostToolUse exit 2 feeds stderr back to Claude.
    if not hook:
        print(f'Board check PASS: {words}/2,500 words; dated entries all <=80 words.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
