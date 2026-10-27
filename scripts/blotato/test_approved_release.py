"""Capacity fallback must preserve a later film's explicitly approved release date."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import danrosefit_migration
import video_topup


class FixedTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 10, 25, 19, tzinfo=timezone.utc).astimezone(tz)


def scheduled(day):
    return {'accountId': '46963', 'scheduledAt': day + 'T15:00:00.000Z',
            'draft': {'content': {'text': 'utm_campaign=longform&utm_content=existing-' + day}}}


class ApprovedReleaseTests(unittest.TestCase):
    def plan(self, include_earlier=False, clash=False, changed=False):
        with tempfile.TemporaryDirectory() as td:
            entries = []
            if include_earlier:
                p = Path(td) / 'earlier.json'
                p.write_text(json.dumps({'slug': 'earlier', 'main': '2026-12-30T15:00:00.000Z', 'video_url': 'https://example.test/video.mp4'}))
                entries.append({'job': 'earlier', 'label': 'Earlier film', 'kind': 'longform', 'config': str(p)})
            p = Path(td) / 'approved.json'
            data = {'slug': 'approved', 'main': ('2027-01-10' if changed else '2027-01-06') + 'T15:00:00.000Z', 'video_url': 'https://example.test/video.mp4'}
            p.write_text(json.dumps(data))
            entries.append({'job': 'approved', 'label': 'Approved film', 'kind': 'longform', 'config': str(p), 'approved_release': '2027-01-06T15:00:00.000Z'})
            items = [scheduled('2026-12-30'), scheduled('2027-01-03')]
            if clash:
                items.append(scheduled('2027-01-06'))
            output = io.StringIO()
            with patch.object(video_topup, 'load', return_value=entries), \
                 patch.object(video_topup, 'datetime', FixedTime), \
                 patch.object(video_topup, 'head_bytes', return_value=1000), \
                 patch.object(danrosefit_migration, 'api_key', return_value='test'), \
                 patch.object(danrosefit_migration, 'fetch_schedules', return_value=items), \
                 patch.object(video_topup.subprocess, 'run', side_effect=AssertionError('No writes in dry run')), \
                 patch.object(sys, 'argv', ['video_topup.py']), contextlib.redirect_stdout(output):
                code = video_topup.main()
            self.assertEqual(json.loads(p.read_text()), data)
            return code, output.getvalue()

    def test_earlier_fallback_skips_later_approved_day(self):
        code, output = self.plan(include_earlier=True)
        self.assertEqual(code, 0)
        self.assertIn('earlier Earlier film: longform on Sun 2027-01-10', output)
        self.assertIn('approved Approved film: longform on Wed 2027-01-06', output)

    def test_approved_day_clash_stops_instead_of_silent_move(self):
        code, output = self.plan(clash=True)
        self.assertEqual(code, 1)
        self.assertIn('explicitly approved release date is unavailable', output)
        self.assertNotIn('would queue  approved', output)

    def test_changed_config_does_not_override_explicit_approval(self):
        code, output = self.plan(changed=True)
        self.assertEqual(code, 1)
        self.assertIn('explicitly approved release date is unavailable or changed', output)


if __name__ == '__main__':
    unittest.main()
