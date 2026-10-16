"""Release holds must prevent both direct submission and automatic date/media work."""
import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ad_guard
import danrosefit_migration
import video_topup


class ReleaseHoldTests(unittest.TestCase):
    def test_direct_guard_rejects_hold_before_registry_reads(self):
        with patch.object(ad_guard, 'ad_titles', side_effect=AssertionError('registry read')):
            with self.assertRaises(ad_guard.AdGuardError):
                ad_guard.assert_organic({'content_type': 'organic', 'release_hold': 'reopened'})

    def run_topup(self, entry_hold, config_hold):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / 'config.json'
            config = {'slug': 'test', 'main': '2026-11-03T15:00:00.000Z'}
            if config_hold:
                config['release_hold'] = 'corrections and exact-file approval pending'
            p.write_text(json.dumps(config))
            entry = {'config': str(p), 'kind': 'short', 'job': 'DS-05'}
            if entry_hold:
                entry['release_hold'] = 'reopened'
            original = copy.deepcopy(entry)
            output = io.StringIO()
            with patch.object(video_topup, 'load', return_value=[entry]), \
                 patch.object(danrosefit_migration, 'api_key', return_value='test-only'), \
                 patch.object(danrosefit_migration, 'fetch_schedules', return_value=[]), \
                 patch.object(video_topup, 'head_bytes', side_effect=AssertionError('media read')), \
                 patch.object(video_topup.subprocess, 'run', side_effect=AssertionError('submission')), \
                 patch.object(sys, 'argv', ['video_topup.py', '--apply']), \
                 contextlib.redirect_stdout(output):
                # Avoid writing the real waitlist when testing --apply.
                with patch.object(video_topup, 'WAITLIST', str(Path(td) / 'waitlist.json')):
                    self.assertEqual(video_topup.main(), 0)
            self.assertEqual(entry, original)
            self.assertEqual(json.loads(p.read_text()), config)
            self.assertIn('held', output.getvalue())
            self.assertNotIn('queue   DS-05', output.getvalue())

    def test_held_entry_does_not_reserve_capacity_ahead_of_other_posts(self):
        ready = {'job': 'other-ready'}
        held = {'job': 'DS-05', 'release_hold': 'reopened'}
        queued = {'job': 'other-queued', 'queued': {'date': '2026-10-16'}}
        self.assertEqual(video_topup.pending([ready, held, queued]), [ready])

    def test_entry_hold_blocks_auto_submission(self):
        self.run_topup(True, False)

    def test_config_hold_blocks_auto_submission(self):
        self.run_topup(False, True)


if __name__ == '__main__':
    unittest.main()
