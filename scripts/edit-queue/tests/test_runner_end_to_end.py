#!/usr/bin/env python3
"""End-to-end run of runner.py with a FAKE editor/reviewer program: no AI session, no allowance, no real job.
Proves the slot mechanics: one edit -> one independent review -> delivered or parked, claim released,
scoreboard row complete. Also the parked (BLOCKED.md) and the signed-out paths.

  python3 scripts/edit-queue/tests/test_runner_end_to_end.py
"""
import json, os, stat, subprocess, sys, tempfile, unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAKE = r'''#!/usr/bin/env python3
import sys, os, re, json
prompt = sys.stdin.read()
mode = os.environ.get("FAKE_MODE", "ok")
wd = re.search(r"work directory is `([^`]+)`|`([^`]+)/DELIVERY.json`", prompt)
wd = wd.group(1) or wd.group(2)
if mode == "signedout":
    print("Not logged in · Please run /login"); sys.exit(1)
if "INDEPENDENT REVIEW" in prompt:
    n = int(re.search(r"review (\d+)", prompt).group(1))
    verdict = "VERDICT: DOES NOT SHIP" if mode == "review_fail" else "VERDICT: SHIP"
    open(os.path.join(wd, f"QUEUE-REVIEW-{n}.md"), "w").write(verdict + "\nGood pace.\nCaption late at 0:12.\n")
elif mode == "blocked":
    open(os.path.join(wd, "BLOCKED.md"), "w").write("The approved vertical master is missing.\nNeed the file.\n")
else:
    open(os.path.join(wd, "cut.mp4"), "w").write("x")
    json.dump({"status": "not_applicable", "reason": "fake test has no source selection"}, open(os.path.join(wd, "PRE_RENDER_CHECK.json"), "w"))
    json.dump({"files": [wd + "/cut.mp4"], "review_copy": wd + "/cut.mp4", "gate": "PASS", "generation_spend_usd": 0,
               "revision_count": 0, "approved_elements": ["fake audio"],
               "reuse": {k: {"status": "not_applicable", "reason": "fake test"} for k in ("scenes", "audio", "transcript", "assets")},
               "paid_provider_costs": [{"provider": "none", "usd": 0}], "summary": "s"}, open(os.path.join(wd, "DELIVERY.json"), "w"))
'''


class EndToEnd(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="eq-e2e-")
        fake = os.path.join(self.tmp, "fake-exec"); open(fake, "w").write(FAKE); os.chmod(fake, os.stat(fake).st_mode | stat.S_IEXEC)
        cfg = json.load(open(os.path.join(PKG, "config.json")))
        cfg["work_root"] = os.path.join(self.tmp, "work"); os.makedirs(cfg["work_root"])
        for ex in cfg["executors"].values():
            ex.pop("binary_glob", None); ex["binary"] = fake; ex["auth_check"] = None
        json.dump(cfg, open(os.path.join(self.tmp, "config.json"), "w"))
        json.dump({"jobs": [{"id": "AV-01", "state": "ready", "size": "S", "order": 1, "title": "t", "file": "", "claude": "edit it", "codex": "edit it", "rev": 1}]},
                  open(os.path.join(self.tmp, "jobs.json"), "w"))
        self.env = dict(os.environ, EDIT_QUEUE_DIR=self.tmp, EDIT_QUEUE_NO_DRIVE="1", EDIT_QUEUE_CONFIG=os.path.join(self.tmp, "config.json"),
                        EDIT_QUEUE_SCOREBOARD=os.path.join(self.tmp, "scoreboard.json"))

    def go(self, mode):
        env = dict(self.env, FAKE_MODE=mode)
        code = ("import sys,os; sys.path.insert(0, %r); import eq_common as eq; eq.unshadow(); d=eq.sibling('dispatcher'); q=eq.sibling('queue');"
                "cfg=eq.load_config(); print(d.launch('AV-01','claude',cfg)); "
                "import time\n"
                "for _ in range(200):\n"
                "    time.sleep(0.1)\n"
                "    if 'claim' not in q.find(q.load(),'AV-01'): break\n") % PKG
        subprocess.run([sys.executable, "-c", code], env=env, check=True, capture_output=True, timeout=60)
        job = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
        row = json.load(open(os.path.join(self.tmp, "scoreboard.json")))["runs"][-1]
        return job, row

    def test_one_review_then_ship(self):
        job, row = self.go("ok")
        self.assertEqual(job["state"], "delivered"); self.assertNotIn("claim", job); self.assertTrue(job["queue_owned"])
        self.assertEqual(row["reviewer_verdicts"], ["SHIP"]); self.assertEqual(row["revision_rounds"], 0)
        self.assertEqual(row["outcome"], "delivered"); self.assertEqual(row["first_pass_gate"], "PASS"); self.assertIsNotNone(row["ended"])
        self.assertEqual(len(row["model_usage"]), 2)
        self.assertIsNone(row["model_usage"][0]["input_tokens"])
        log = open(os.path.join(self.tmp, "work", "AV-01", "queue-run.log")).read()
        for part in ("edit session", "review-1 session"):
            self.assertIn(part, log)
        self.assertNotIn("revision-1 session", log)
        self.assertNotIn("review-2 session", log)

    def test_rejected_review_parks_without_automatic_fix_loop(self):
        job, row = self.go("review_fail")
        self.assertEqual(job["state"], "needs")
        self.assertEqual(row["reviewer_verdicts"], ["DOES NOT SHIP"])
        self.assertEqual(row["outcome"], "parked")
        log = open(os.path.join(self.tmp, "work", "AV-01", "queue-run.log")).read()
        self.assertNotIn("revision-1 session", log)
        self.assertNotIn("review-2 session", log)

    def test_blocked_parks_as_needs(self):
        job, row = self.go("blocked")
        self.assertEqual(job["state"], "needs"); self.assertIn("approved vertical master is missing", job["note"])
        self.assertEqual(row["outcome"], "parked"); self.assertNotIn("claim", job)

    def test_signed_out_goes_back_in_line_and_backs_off(self):
        job, row = self.go("signedout")
        self.assertEqual(row["outcome"], "auth_failed"); self.assertEqual(job["state"], "ready"); self.assertNotIn("claim", job)
        self.assertIsNone(row["paid_provider_costs"][0]["usd"])
        self.assertIn("unavailable", row["paid_provider_costs"][0]["reason"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
