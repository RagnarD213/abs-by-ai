"""Dated release phases (Dan, 2026-10-28): weekdays, Short slots, kitchen and gym holds, and the top-up slotting."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import danrosefit_migration
import release_phases as rp
import video_topup


class FixedTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 10, 28, 19, tzinfo=timezone.utc).astimezone(tz)


class PhaseRuleTests(unittest.TestCase):
    def test_longform_weekdays_by_phase(self):
        self.assertTrue(rp.longform_allowed(date(2026, 11, 4)))    # Wed, phase 1
        self.assertFalse(rp.longform_allowed(date(2026, 11, 6)))   # Fri, phase 1
        self.assertTrue(rp.longform_allowed(date(2026, 11, 27)))   # Fri, phase 2
        self.assertFalse(rp.longform_allowed(date(2026, 12, 25)))  # Christmas Day
        self.assertTrue(rp.longform_allowed(date(2027, 1, 1)))     # Fri, phase 3
        self.assertTrue(rp.longform_allowed(date(2027, 1, 31)))    # Sun
        self.assertFalse(rp.longform_allowed(date(2027, 2, 3)))    # Wed, phase 4 is Sunday only
        self.assertTrue(rp.longform_allowed(date(2027, 2, 7)))

    def test_short_slots_by_phase(self):
        self.assertEqual(rp.short_times(date(2026, 11, 5)), ("09:00",))           # Thu phase 1
        self.assertEqual(rp.short_times(date(2026, 11, 8), True), ())                   # Sun long-form day, film booked
        self.assertEqual(rp.short_times(date(2026, 11, 8), False), ("09:00",))    # film-less long-form day: one Short
        self.assertEqual(rp.short_times(date(2026, 11, 26)), ("09:00", "18:00"))  # Thanksgiving, phase 2
        self.assertEqual(rp.short_times(date(2026, 12, 25)), ("09:00", "18:00"))  # Christmas
        self.assertEqual(rp.short_times(date(2026, 12, 27), True), ())            # Sun long-form
        self.assertEqual(rp.short_times(date(2026, 12, 26)), ("09:00", "18:00"))  # Sat, phase 3
        self.assertEqual(rp.short_times(date(2027, 1, 5)), ("09:00", "18:00"))    # Tue, phase 3
        self.assertEqual(rp.short_times(date(2027, 2, 2)), ("09:00",))            # Tue, phase 4
        self.assertEqual(rp.short_times(date(2027, 2, 6)), ("09:00",))            # Sat, phase 4

    def test_kitchen_and_gym_holds(self):
        kitchen, gym = {"kitchen": True}, {"gym": True}
        self.assertTrue(rp.blocked_by_content(date(2026, 11, 12), kitchen, "ro07"))
        self.assertFalse(rp.blocked_by_content(date(2026, 11, 12), kitchen, "sl03-short2"))  # salad family
        self.assertFalse(rp.blocked_by_content(date(2026, 11, 12), kitchen, "ro05-daily-salad"))
        self.assertFalse(rp.blocked_by_content(date(2026, 12, 1), kitchen, "ro07"))           # phase 2
        self.assertTrue(rp.blocked_by_content(date(2027, 1, 12), kitchen, "ro07"))            # phase 3
        self.assertFalse(rp.blocked_by_content(date(2027, 2, 9), kitchen, "ro07"))            # phase 4
        self.assertTrue(rp.blocked_by_content(date(2026, 11, 12), gym, "ds84"))
        self.assertFalse(rp.blocked_by_content(date(2026, 11, 12), {"gym": True, "phase1_test": True}, "ds84"))
        self.assertFalse(rp.blocked_by_content(date(2026, 12, 29), gym, "ds84"))

    def test_next_short_slot_skips_longform_days_and_taken(self):
        taken = {(date(2026, 11, 3), "09:00")}
        self.assertEqual(rp.next_short_slot(date(2026, 11, 2), taken, {}, "x"), (date(2026, 11, 5), "09:00"))
        # Wed Nov 4 and Sun Nov 8 are long-form days: never auto-used
        self.assertEqual(rp.next_short_slot(date(2026, 11, 7), set(), {}, "x"), (date(2026, 11, 9), "09:00"))
        # kitchen entry in phase 1 jumps to phase 2
        self.assertEqual(rp.next_short_slot(date(2026, 11, 10), set(), {"kitchen": True}, "ro07"), (date(2026, 11, 26), "09:00"))
        # phase 2 gives the evening slot once the morning one is taken
        self.assertEqual(rp.next_short_slot(date(2026, 11, 25), {(date(2026, 11, 26), "09:00")}, {}, "x"),
                         (date(2026, 11, 26), "18:00"))


class TopupSlottingTests(unittest.TestCase):
    def run_topup(self, entry, items, config):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "s.json"
            p.write_text(json.dumps(config))
            entry = {**entry, "config": str(p)}
            out = io.StringIO()
            with patch.object(video_topup, "load", return_value=[entry]), \
                 patch.object(video_topup, "datetime", FixedTime), \
                 patch.object(video_topup, "head_bytes", return_value=1000), \
                 patch.object(danrosefit_migration, "api_key", return_value="t"), \
                 patch.object(danrosefit_migration, "fetch_schedules", return_value=items), \
                 patch.object(video_topup.subprocess, "run", side_effect=AssertionError("dry run")), \
                 patch.object(sys, "argv", ["video_topup.py"]), contextlib.redirect_stdout(out):
                code = video_topup.main()
            return code, out.getvalue()

    def short(self, main, **entry):
        cfg = {"slug": "dstest", "main": main, "video_url": "https://example.test/v.mp4"}
        return self.run_topup({"job": "DS-99", "label": "Test", "kind": "short", **entry}, [], cfg)

    def test_valid_evening_slot_is_kept_in_phase_2(self):
        code, out = self.short("2026-12-01T00:00:00.000Z")  # Mon Nov 30 6 PM Central
        self.assertEqual(code, 0)
        self.assertIn("short on Mon 2026-11-30 06:00 PM Central", out)
        self.assertNotIn("re-slotted", out)

    def test_evening_slot_in_phase_1_is_re_slotted_to_nine_am(self):
        code, out = self.short("2026-11-06T00:00:00.000Z")  # Thu Nov 5 6 PM: phase 1 has no evening slot
        self.assertIn("re-slotted", out)
        self.assertIn("09:00 AM Central", out)

    def test_dedicated_short_is_no_longer_thursday_only(self):
        code, out = self.short("2026-11-03T15:00:00.000Z")  # Tue Nov 3 9 AM
        self.assertIn("short on Tue 2026-11-03 09:00 AM Central", out)
        self.assertNotIn("re-slotted", out)

    def test_kitchen_short_is_moved_out_of_phase_1(self):
        code, out = self.short("2026-11-06T15:00:00.000Z", kitchen=True)
        self.assertIn("re-slotted", out)
        self.assertIn("2026-11-26 09:00 AM Central", out)

    def test_kitchen_short_keeps_its_phase_2_slot(self):
        code, out = self.short("2026-12-03T15:00:00.000Z", kitchen=True)
        self.assertNotIn("re-slotted", out)

    def test_gym_short_waits_for_january(self):
        code, out = self.short("2026-11-06T15:00:00.000Z", gym=True)
        self.assertIn("2026-12-26 09:00 AM Central", out)

    def test_gym_phase1_test_short_keeps_its_slot(self):
        code, out = self.short("2026-11-23T15:00:00.000Z", gym=True, phase1_test=True)
        self.assertNotIn("re-slotted", out)

    def test_longform_friday_is_valid_in_phase_2_only(self):
        cfg = {"slug": "lf", "main": "2026-11-27T15:00:00.000Z", "video_url": "https://example.test/v.mp4"}
        code, out = self.run_topup({"job": "RO-99", "label": "Film", "kind": "longform"}, [], cfg)
        self.assertNotIn("re-slotted", out)
        cfg["main"] = "2026-11-20T15:00:00.000Z"  # Fri in phase 1: not a long-form day
        code, out = self.run_topup({"job": "RO-99", "label": "Film", "kind": "longform"}, [], cfg)
        self.assertIn("re-slotted", out)

    def test_kitchen_longform_is_kept_out_of_phase_1(self):
        cfg = {"slug": "lf", "main": "2026-11-15T15:00:00.000Z", "video_url": "https://example.test/v.mp4"}
        code, out = self.run_topup({"job": "RO-99", "label": "Film", "kind": "longform", "kitchen": True}, [], cfg)
        self.assertIn("2026-11-27 09:00 AM Central", out)


if __name__ == "__main__":
    unittest.main()
