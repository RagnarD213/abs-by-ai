"""Run: python3 -m unittest discover -s scripts/tests -p test_board_check.py"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class BoardCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='board-check-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'scripts').mkdir()
        for name in ('board-check.sh', 'board-check.py'):
            shutil.copy2(ROOT / 'scripts' / name, self.root / 'scripts' / name)
        self.board = self.root / 'AI_COORDINATION.md'
        self.command = json.loads((ROOT / '.claude/settings.json').read_text())['hooks']['PostToolUse'][-1]['hooks'][0]['command']

    def run_check(self, text):
        self.board.write_text(text)
        return subprocess.run([str(self.root / 'scripts/board-check.sh')], capture_output=True, text=True, cwd='/tmp')

    def hook(self, tool, path):
        payload = {'tool_name': tool, 'cwd': str(self.root), 'tool_input': {'file_path': str(path)}}
        return subprocess.run(self.command, shell=True, input=json.dumps(payload), capture_output=True, text=True,
                              env={**os.environ, 'CLAUDE_PROJECT_DIR': str(self.root)}, cwd='/tmp')

    def test_word_boundaries(self):
        entry = '**Task** 2026-09-15 ' + 'word ' * 78
        self.assertEqual(self.run_check(entry).returncode, 0)  # exactly 80
        self.assertIn('81 words', self.run_check(entry + 'extra').stderr)
        text = '# Header\n' + 'word ' * 2498
        self.assertEqual(self.run_check(text).returncode, 0)  # exactly 2,500
        self.assertIn('BOARD: 2501', self.run_check(text + 'extra').stderr)

    def test_entries_and_dates(self):
        text = '# Active\n**Missing** needs a date.\n\n- **Oversized** 2026-09-15 ' + 'word ' * 81
        result = self.run_check(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn('[Missing]: no date', result.stderr)
        self.assertIn('[Oversized]', result.stderr)
        self.assertIn('entry limit 80', result.stderr)
        self.assertEqual(self.run_check('**Task** bad 2026-02-30; `handoff-2026-09-15.md`').returncode, 1)
        self.assertEqual(self.run_check('**Task** updated 09-15.\n\n# Next\n' + 'word ' * 90).returncode, 0)
        self.assertEqual(self.run_check('**Task** 2026-09-15\n  **Inline emphasis** is a continuation.').returncode, 0)

    def test_over_budget_edit_through_configured_hook(self):
        original = (ROOT / 'AI_COORDINATION.md').read_text()
        self.board.write_text(original)
        self.assertEqual(self.hook('Edit', self.board).returncode, 0)
        # Test edit of an isolated board copy; never overwrite another session's live board.
        self.board.write_text(original + '\n# Temporary budget test\n' + 'overflow ' * 2501)
        for tool in ('Edit', 'Write', 'MultiEdit', 'Bash'):
            result = self.hook(tool, self.board)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn('BOARD:', result.stderr)
            self.assertIn('limit 2,500', result.stderr)
        self.assertEqual(self.hook('Edit', self.root / 'other.md').returncode, 0)
        self.board.write_text(original)
        self.assertEqual(self.hook('Edit', 'AI_COORDINATION.md').returncode, 0)
        self.board.write_text('**Undated entry** needs a date')
        result = self.hook('Edit', self.board)
        self.assertEqual(result.returncode, 2)
        self.assertIn('[Undated entry]: no date', result.stderr)


if __name__ == '__main__':
    unittest.main()
