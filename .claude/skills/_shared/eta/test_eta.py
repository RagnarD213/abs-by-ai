#!/usr/bin/env python3
"""Tests for eta.py: python3 .claude/skills/_shared/eta/test_eta.py"""
import json, os, sys, tempfile, unittest
from pathlib import Path

os.environ["ETA_DIR"] = tempfile.mkdtemp(prefix="eta-test-")
os.environ["ETA_NO_DRIVE"] = "1"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import eta  # noqa: E402

T0 = 1_800_000_000.0


def hist(step, minutes, kind="WV", n=3):
    return [json.dumps(dict(step=eta.norm(step), kind=kind, minutes=minutes)) for _ in range(n)]


class Plan(unittest.TestCase):
    def setUp(self):
        for f in Path(os.environ["ETA_DIR"]).glob("*"):
            f.unlink()

    def test_plan_step_records_history(self):
        eta.cmd_plan("WV-09", ["Take map:20", "Key 14 pieces:180", "Build:60"], now=T0)
        eta.cmd_step("WV-09", 2, now=T0 + 25 * 60)
        rec = eta.load("WV-09")
        self.assertEqual(rec["current"], 2)
        h = [json.loads(l) for l in eta.HISTORY.read_text().splitlines()]
        self.assertEqual(h[-1]["step"], "take map")
        self.assertAlmostEqual(h[-1]["minutes"], 25.0)

    def test_done_clears(self):
        eta.cmd_plan("WV-08", ["A:10"], now=T0)
        eta.cmd_done("WV-08", now=T0 + 60)
        self.assertIsNone(eta.load("WV-08"))

    def test_names_learn_across_counts(self):
        self.assertEqual(eta.norm("Key 14 pieces"), eta.norm("key 9 pieces!"))


class Estimate(unittest.TestCase):
    def rec(self, **kw):
        r = dict(job="WV-05", current=2, retries=0, left=None,
                 steps=[dict(name="Take map", expect=20, started=T0 - 3600, ended=T0 - 3000),
                        dict(name="Key", expect=60, started=T0 - 600), dict(name="Build", expect=30)])
        r.update(kw)
        return r

    def test_on_plan(self):
        e = eta.estimate_job(self.rec(), T0, hist_lines=[])
        self.assertEqual(e["mid_min"], 80)          # 50 left in Key + 30 Build
        self.assertLess(e["low_min"], 80)
        self.assertGreater(e["high_min"], 80)
        self.assertEqual((e["step"], e["of"]), (2, 3))

    def test_running_long_never_goes_negative(self):
        r = self.rec()
        r["steps"][1]["started"] = T0 - 200 * 60     # 200 min into a 60 min step
        e = eta.estimate_job(r, T0, hist_lines=[])
        self.assertEqual(e["basis"], "running long")
        self.assertGreaterEqual(e["mid_min"], 30 + 60)

    def test_measured_left_is_tight(self):
        r = self.rec(current=3, left=dict(minutes=12, at=T0 - 120))
        r["steps"][2]["started"] = T0 - 300
        e = eta.estimate_job(r, T0, hist_lines=[])
        self.assertEqual(e["basis"], "measured")
        self.assertEqual(e["mid_min"], 10)
        self.assertLessEqual(e["high_min"] - e["low_min"], 5)

    def test_history_moves_the_guess(self):
        e = eta.estimate_job(self.rec(), T0, hist_lines=hist("Build", 90))
        self.assertEqual(e["mid_min"], 50 + 60)     # Build = mean of plan 30 and history 90

    def test_retries_widen(self):
        a = eta.estimate_job(self.rec(), T0, hist_lines=[])
        b = eta.estimate_job(self.rec(retries=2), T0, hist_lines=[])
        self.assertGreater(b["high_min"], a["high_min"])

    def test_unknown_step_is_rough(self):
        r = self.rec()
        r["steps"][2]["expect"] = None
        self.assertEqual(eta.estimate_job(r, T0, hist_lines=[])["basis"], "rough")

    def test_render_wait_adds(self):
        a = eta.estimate_job(self.rec(), T0, hist_lines=[])
        b = eta.estimate_job(self.rec(), T0, hist_lines=[], render=dict(waiting=1, wait_min=40))
        self.assertEqual(b["mid_min"] - a["mid_min"], 40)


class Rows(unittest.TestCase):
    def mac(self, **kw):
        v = dict(edits={}, progress={}, render={}, waiting_order=[])
        v.update(kw)
        return v

    def test_waiting_on_dan(self):
        d = eta.combine({"m6": self.mac(edits={"WV-05": dict(state="with-dan", title="Upsell 2")})}, now=T0)
        self.assertEqual(d["jobs"]["WV-05"]["kind"], "dan")

    def test_slot_wait(self):
        d = eta.combine({"m2": self.mac(edits={"RO-39": dict(state="waiting")}, waiting_order=["RO-39"])}, now=T0)
        self.assertIn("#1", d["jobs"]["RO-39"]["text"])

    def test_stuck(self):
        d = eta.combine({"m6": self.mac(edits={"WV-05": dict(state="active", last_seen=T0 - 3 * 3600)})}, now=T0)
        self.assertEqual(d["jobs"]["WV-05"]["kind"], "stuck")

    def test_not_stuck_while_rendering(self):
        d = eta.combine({"m6": self.mac(edits={"WV-05": dict(state="active", last_seen=T0 - 3 * 3600)},
                                        render={"WV-05": dict(running=1)})}, now=T0)
        self.assertEqual(d["jobs"]["WV-05"]["kind"], "noplan")

    def test_eta_row_and_order(self):
        prog = dict(low_min=30, high_min=60, mid_min=40, basis="estimate", step=2, of=3, step_name="Key",
                    retries=0, retry_note="", updated=T0)
        d = eta.combine({"m6": self.mac(edits={"WV-05": dict(state="active", last_seen=T0), "X-1": dict(state="with-dan")},
                                        progress={"WV-05": prog})}, now=T0)
        row = d["jobs"]["WV-05"]
        self.assertEqual(row["kind"], "eta")
        self.assertIn(" to ", row["text"])
        self.assertIn("Step 2 of 3: Key", row["detail"])
        self.assertEqual(d["order"][0], "WV-05")

    def test_span_reads_naturally(self):
        import datetime as dt
        lo = dt.datetime(2026, 11, 18, 15, 28).timestamp(); hi = dt.datetime(2026, 11, 18, 16, 14).timestamp()
        self.assertEqual(eta.span(lo, hi), "3:30 to 4:15 PM")

    def test_unreachable_mac_is_harmless(self):
        d = eta.combine({"m6": self.mac(), "m2": {}}, now=T0)
        self.assertEqual(d["order"], [])
        self.assertFalse(d["macs"]["m2"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
