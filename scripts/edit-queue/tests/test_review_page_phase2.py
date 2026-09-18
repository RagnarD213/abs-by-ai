#!/usr/bin/env python3
"""Local page proof using only a temporary queue/config/work root and synthetic bytes."""
import json, os, sys, tempfile, unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = tempfile.mkdtemp(prefix="eq-page-")
os.environ.update(EDIT_QUEUE_DIR=TMP, EDIT_QUEUE_NO_DRIVE="1",
                  EDIT_QUEUE_CONFIG=os.path.join(TMP,"config.json"),
                  EDIT_QUEUE_SCOREBOARD=os.path.join(TMP,"scoreboard.json"),
                  EDIT_QUEUE_PAUSE_FILE=os.path.join(TMP,"PAUSE"),
                  EDIT_QUEUE_SNAPSHOT=os.path.join(TMP,"snapshot.html"))
sys.path.insert(0,PKG)
import eq_common as eq  # noqa: E402
eq.unshadow(); q=eq.sibling("queue"); asset=eq.sibling("asset_approval"); page=eq.sibling("review_page")


class ReviewPagePhase2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.path.join(PKG,"config.json")) as fh: cfg=json.load(fh)
        cfg["work_root"]=os.path.join(TMP,"work"); cfg["stop"]["volume"]=TMP
        for ex in cfg["executors"].values(): ex["binary"]="/usr/bin/true"; ex["auth_check"]=None
        with open(os.environ["EDIT_QUEUE_CONFIG"],"w") as fh: json.dump(cfg,fh)
        job={"id":"AV-99","state":"in_progress","size":"S","order":1,"title":"Synthetic page",
             "file":"","claude":"x","codex":"x","rev":1,
             "claim":{"by":"fake","pid":999999,"started":"2026-09-18T10:00:00","heartbeat":"2026-09-18T10:00:00"}}
        with open(q.JOBS,"w") as fh: json.dump({"jobs":[job]},fh)
        with open(os.environ["EDIT_QUEUE_SCOREBOARD"],"w") as fh: json.dump({"schema":1,"runs":[]},fh)
        cls.wd=os.path.join(cfg["work_root"],"AV-99"); os.makedirs(cls.wd)
        def put(name,body):
            p=os.path.join(cls.wd,name); open(p,"wb").write(body); return {"path":p,"sha256":asset.sha256(p)}
        draft,start,end=put("DRAFT.mp4",b"draft"),put("start.png",b"start"),put("end.png",b"end")
        item={"id":"AI-1","type":"ai_motion","reuse_status":"new","in":2.0,"out":3.5,"duration":1.5,
              "spoken_beat":"show the movement","intended_action":"controlled crunch","affected_scenes":["scene-2"],
              "boundary_joins":["join-1"],"estimated_usd":0.25,"placeholder":{"label":"PLACEHOLDER — AI-1","sha256":"0"*64},
              "start_frame":start,"end_frame":end,"approval":{"status":"pending","selected_hashes":[],"words":None,
              "timestamp":None,"selection_fingerprint":None},"final_clip":None}
        asset.write_packet(os.path.join(cls.wd,"placeholders.json"),
                           {"schema_version":1,"video_id":"AV-99","revision":0,"status":"approval_required",
                            "draft":draft,"prior_paid_spend_usd":1.0,"generation_budget_usd":5.0,"items":[item]},cls.wd)

    def test_live_and_static_asset_cards_and_hash_allowlist(self):
        live=page.render(); static=page.render(static=True)
        for text in ("Asset choices","show the movement","controlled crunch","projected per-video total $1.25",
                     "budget $5.00","Submit every choice once"):
            self.assertIn(text,live)
        self.assertNotIn("Submit every choice once",static)
        allow=page.allowed_media(eq.load_config(),q.load())
        self.assertEqual(len(allow),3)
        start=os.path.join(self.wd,"start.png")
        with open(start,"ab") as fh: fh.write(b"stale")
        self.assertNotIn(os.path.realpath(start),page.allowed_media(eq.load_config(),q.load()))

    def test_static_snapshot_uses_isolated_path(self):
        self.assertEqual(page.build(),os.environ["EDIT_QUEUE_SNAPSHOT"])
        self.assertTrue(os.path.isfile(os.environ["EDIT_QUEUE_SNAPSHOT"]))


if __name__=="__main__": unittest.main(verbosity=1)
