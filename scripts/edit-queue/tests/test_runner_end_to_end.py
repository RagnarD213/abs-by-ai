#!/usr/bin/env python3
"""End-to-end run of runner.py with a FAKE editor/reviewer program: no AI session, no allowance, no real job.
Proves the slot mechanics: one edit -> one independent review -> delivered or parked, claim released,
scoreboard row complete. Also the parked (BLOCKED.md) and the signed-out paths.

  python3 scripts/edit-queue/tests/test_runner_end_to_end.py
"""
import json, os, stat, subprocess, sys, tempfile, unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAKE = r'''#!/usr/bin/env python3
import sys, os, re, json, time, datetime, hashlib
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
elif mode.startswith("phase2") and "THIS LAUNCH IS STAGE ONE" in prompt:
    sys.path.insert(0, os.environ["EDIT_QUEUE_PKG"]); import asset_approval as asset
    def put(name, body):
        p=os.path.join(wd,name); open(p,"wb").write(body); return {"path":p,"sha256":asset.sha256(p)}
    draft,start,end=put("DRAFT-fixture.mp4",b"draft placeholder"),put("start.png",b"start"),put("end.png",b"end")
    item={"id":"AI-1","type":"ai_motion","in":1.0,"out":2.0,"duration":1.0,
          "spoken_beat":"fixture beat","intended_action":"fixture motion","affected_scenes":["scene-2"],
          "boundary_joins":["join-1"],"estimated_usd":0.05,
          "placeholder":{"label":"PLACEHOLDER — AI-1","sha256":"0"*64},"start_frame":start,"end_frame":end,
          "approval":{"status":"pending","selected_hashes":[],"words":None,"timestamp":None,"selection_fingerprint":None},"final_clip":None}
    packet={"schema_version":1,"video_id":"AV-01","revision":0,"status":"approval_required","draft":draft,
            "prior_paid_spend_usd":0,"items":[item]}
    pp=os.path.join(wd,"placeholders.json"); packet=asset.write_packet(pp,packet,wd)
    marker={"schema":1,"gate":"DRAFT","revision_count":0,"packet":pp,
            "packet_material_fingerprint":asset.packet_material_fingerprint(packet),"draft_sha256":draft["sha256"],
            "stage_one_ended":datetime.datetime.now().astimezone().isoformat(timespec="seconds"),"full_render_count":1,
            "generation_spend_usd":0.02,"paid_provider_costs":[{"provider":"fake-motion","purpose":"failed synthetic attempt","usd":0.02,"status":"failed"},{"provider":"none-stage-one","usd":0}]}
    if mode == "phase2_wait":
        until=time.time()+8
        while time.time()<until and not os.path.exists(os.path.join(wd,"release-stage-one")): time.sleep(.05)
    else:
        time.sleep(1.05)
    marker["stage_one_ended"]=datetime.datetime.now().astimezone().isoformat(timespec="seconds")
    json.dump(marker,open(os.path.join(wd,"DRAFT-DELIVERY.json"),"w"))
elif mode.startswith("phase2") and "THIS LAUNCH IS FINISHING" in prompt:
    sys.path.insert(0, os.environ["EDIT_QUEUE_PKG"]); import asset_approval as asset
    pp=os.path.join(wd,"placeholders.json"); packet=asset.read_packet(pp,wd,require_approved=True)
    clip=os.path.join(wd,"AI-1-final.mp4"); open(clip,"wb").write(b"approved motion")
    final=os.path.join(wd,"FINAL-fixture.mp4"); open(final,"wb").write(b"final no placeholder")
    sha=lambda p: hashlib.sha256(open(p,"rb").read()).hexdigest()
    watch=os.path.join(wd,"watch.json")
    json.dump({"watch_version":"1.1.0","sha256":sha(final),"inspected":True,"reviewed":1,"boundaries":1,
               "sheets":["sheet.jpg"],"strips":[],"judged":[{"image":"sheet.jpg","verdict":"clean"}],
               "judged_by":"fake","checklist":["placeholder"]},open(watch,"w"))
    asset.mark_complete(pp,{"AI-1":clip},final,wd,watch_log=watch)
    json.dump({"gate_version":"2.2.0","format":"ad16x9","verdict":"PASS","sha256":sha(final),
               "rows":{"compliance:placeholder":{"ok":True}}},open(final+".deliver_gate.json","w"))
    json.dump({"status":"not_applicable","reason":"synthetic fixture"},open(os.path.join(wd,"PRE_RENDER_CHECK.json"),"w"))
    json.dump({"files":[final],"review_copy":final,"gate":"PASS","generation_spend_usd":0,
               "revision_count":0,"approved_elements":["stage-one draft"],"placeholders":pp,"watch_log":watch,
               "asset_rebuild":{"rebuilt_scenes":["scene-2"],"rebuilt_joins":["join-1"],"reused_scenes":["scene-1"],
                                  "reused_assets":[],"full_render_count":2},
               "reuse":{"scenes":{"status":"mixed","evidence":"scene-1 reused; scene-2 rebuilt"},
                        "audio":{"status":"reused","evidence":"same fixture hash"},
                        "transcript":{"status":"reused","evidence":"same fixture hash"},
                        "assets":{"status":"rebuilt","evidence":pp}},
               "paid_provider_costs":[{"provider":"none-finishing","usd":0}],"summary":"phase2"},
              open(os.path.join(wd,"DELIVERY.json"),"w"))
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
                        EDIT_QUEUE_SCOREBOARD=os.path.join(self.tmp, "scoreboard.json"), EDIT_QUEUE_PKG=PKG,
                        EDIT_QUEUE_PAUSE_FILE=os.path.join(self.tmp, "PAUSE"),
                        EDIT_QUEUE_SNAPSHOT=os.path.join(self.tmp,"review-snapshot.html"))

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
        for part in ("stage-one session", "review-1 session"):
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

    def test_phase2_approval_while_running_then_one_finishing_and_one_review(self):
        env = dict(self.env, FAKE_MODE="phase2_wait")
        launch = ("import sys;sys.path.insert(0,%r);import eq_common as eq;eq.unshadow();"
                  "d=eq.sibling('dispatcher');print(d.launch('AV-01','claude',eq.load_config()))") % PKG
        subprocess.run([sys.executable, "-c", launch], env=env, check=True, capture_output=True)
        wd = os.path.join(self.tmp, "work", "AV-01")
        for _ in range(100):
            if os.path.exists(os.path.join(wd, "placeholders.json")): break
            __import__("time").sleep(.05)
        decide = ("import sys;sys.path.insert(0,%r);import eq_common as eq;eq.unshadow();"
                  "r=eq.sibling('review_page');print(r.record_asset_decisions('AV-01',[{'id':'AI-1','status':'approved','words':'Use these exact frames.'}]))") % PKG
        subprocess.run([sys.executable, "-c", decide], env=env, check=True, capture_output=True)
        live = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
        self.assertEqual(live["state"], "in_progress"); self.assertIn("claim", live)
        __import__("time").sleep(1.1)
        open(os.path.join(wd, "release-stage-one"), "w").close()
        for _ in range(200):
            __import__("time").sleep(.05)
            first = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
            if "claim" not in first: break
        self.assertEqual(first["state"], "frames_approved")
        env["FAKE_MODE"] = "phase2"
        subprocess.run([sys.executable, "-c", launch], env=env, check=True, capture_output=True)
        for _ in range(200):
            __import__("time").sleep(.05)
            final_job = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
            if "claim" not in final_job: break
        self.assertEqual(final_job["state"], "delivered")
        rows = json.load(open(os.path.join(self.tmp, "scoreboard.json")))["runs"]
        self.assertEqual(len(rows), 1, "stage one and finishing are one logical scoreboard row")
        self.assertEqual(rows[0]["reviewer_verdicts"], ["SHIP"])
        self.assertEqual([x["role"] for x in rows[0]["model_usage"]],
                         ["stage-one editor", "finishing editor", "independent reviewer"])
        self.assertEqual(rows[0]["asset_flow"]["approval_submissions"], 1)
        self.assertEqual(rows[0]["asset_flow"]["rebuilt_scenes"], ["scene-2"])
        self.assertEqual(rows[0]["paid_provider_costs"],
                         [{"provider":"fake-motion","purpose":"failed synthetic attempt","usd":0.02,"status":"failed"},
                          {"provider":"none-stage-one","usd":0},{"provider":"none-finishing","usd":0}])
        self.assertEqual(rows[0]["generation_spend_usd"],0.02)
        self.assertLess(rows[0]["asset_flow"]["packet_visible_at"], rows[0]["asset_flow"]["stage_one_ended"])

    def test_phase2_after_exit_approval_moves_state_and_rejection_parks_without_review(self):
        job, row = self.go("phase2")
        self.assertEqual(job["state"], "draft_review")
        self.assertEqual(row["reviewer_verdicts"], [])
        self.assertEqual([x["role"] for x in row["model_usage"]], ["stage-one editor"])
        decide = ("import sys;sys.path.insert(0,%r);import eq_common as eq;eq.unshadow();"
                  "r=eq.sibling('review_page');print(r.record_asset_decisions('AV-01',[{'id':'AI-1','status':'rejected','words':'The motion is too artificial.'}]))") % PKG
        subprocess.run([sys.executable, "-c", decide], env=dict(self.env, FAKE_MODE="phase2"), check=True, capture_output=True)
        parked = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
        self.assertEqual(parked["state"], "draft_review")
        decide = decide.replace("'rejected','words':'The motion is too artificial.'", "'approved','words':'Use the exact frame pair.'")
        subprocess.run([sys.executable, "-c", decide], env=dict(self.env, FAKE_MODE="phase2"), check=True, capture_output=True)
        approved = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
        self.assertEqual(approved["state"], "frames_approved")
        tick = ("import sys,datetime,time;sys.path.insert(0,%r);import eq_common as eq;eq.unshadow();"
                "d=eq.sibling('dispatcher');q=eq.sibling('queue');cfg=eq.load_config();"
                "facts={'now':datetime.datetime.now(),'pause_file':False,'free_gb':1000,'idle_seconds':99999,"
                "'foreign_builds':0,'auth':{x:(True,'') for x in cfg['executors']},'pid_alive':q.pid_alive,"
                "'master':'','board':'','work_dirs':{'AV-01':['isolated-existing-workdir']},'missing_sources':{'AV-01':[]}};"
                "d.gather=lambda _cfg,_data:facts;print(d.tick(False));"
                "\nfor _ in range(200):\n time.sleep(.05)\n"
                " if 'claim' not in q.find(q.load(),'AV-01'): break\n"
                "print(d.tick(True))") % PKG
        ran = subprocess.run([sys.executable, "-c", tick], env=dict(self.env, FAKE_MODE="phase2"),
                             check=True, capture_output=True, text=True, timeout=60)
        self.assertIn("LAUNCH: AV-01 ->", ran.stdout)
        self.assertIn("launching nothing", ran.stdout, "the next ordinary tick must not launch finishing twice")
        finished = json.load(open(os.path.join(self.tmp, "jobs.json")))["jobs"][0]
        rows = json.load(open(os.path.join(self.tmp, "scoreboard.json")))["runs"]
        self.assertEqual(finished["state"], "delivered")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["reviewer_verdicts"], ["SHIP"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
