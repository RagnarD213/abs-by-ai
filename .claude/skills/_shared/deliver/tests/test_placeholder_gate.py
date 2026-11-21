#!/usr/bin/env python3
"""Focused synthetic proof for compliance:placeholder; creates no real media or queue state."""
import hashlib, importlib.util, json, os, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
DELIVER = os.path.dirname(HERE)
SKILLS = os.path.dirname(os.path.dirname(DELIVER))
ROOT = os.path.dirname(os.path.dirname(SKILLS))
sys.path.insert(0, SKILLS)
sys.path.insert(0, os.path.join(ROOT, "scripts", "edit-queue"))
from _shared.deliver.checks import compliance  # noqa: E402
import asset_approval as asset  # noqa: E402


class PlaceholderGate(unittest.TestCase):
    def setUp(self):
        self.wd = tempfile.mkdtemp(prefix="placeholder-gate-")
        self.video = self.put("FINAL.mp4", b"final pixels")
        self.draft = self.put("DRAFT.mp4", b"PLACEHOLDER - AI-1")
        self.start = self.put("start.png", b"start")
        self.end = self.put("end.png", b"end")
        self.clip = self.put("clip.mp4", b"approved motion")
        self.watch = os.path.join(self.wd, "watch.json")
        self.packet = os.path.join(self.wd, "placeholders.json")
        item = {"id":"AI-1","type":"ai_motion","in":1.0,"out":2.0,"duration":1.0,
                "spoken_beat":"fixture","intended_action":"fixture motion","affected_scenes":["scene-1"],
                "boundary_joins":[],"estimated_usd":0.1,"placeholder":{"label":"PLACEHOLDER — AI-1","sha256":"0"*64},
                "start_frame":self.rec(self.start),"end_frame":self.rec(self.end),
                "approval":{"status":"pending","selected_hashes":[],"words":None,"timestamp":None,"selection_fingerprint":None},
                "final_clip":None}
        asset.write_packet(self.packet,{"schema_version":1,"video_id":"FIXTURE","revision":0,
                           "status":"approval_required","draft":self.rec(self.draft),"prior_paid_spend_usd":0,
                           "items":[item]},self.wd)

    def put(self, name, body):
        p=os.path.join(self.wd,name); open(p,"wb").write(body); return p

    def rec(self, path): return {"path":path,"sha256":asset.sha256(path)}

    def write_watch(self, defect=False):
        json.dump({"watch_version":"1.1.0","sha256":asset.sha256(self.video),"inspected":True,
                   "checklist":["placeholder"],"judged":([{"image":"sheet.jpg","verdict":"defect",
                   "item":"placeholder","disposition":"accepted_by_dan"}] if defect else
                   [{"image":"sheet.jpg","verdict":"clean"}])},open(self.watch,"w"))

    def row(self):
        plan={"_sha256":asset.sha256(self.video),"watch_log":self.watch,"placeholders":self.packet}
        return compliance.placeholder("compliance:placeholder",{}, {"required":True},plan,self.video,self.wd)

    def complete(self, defect=False):
        asset.decide(self.packet,[{"id":"AI-1","status":"approved","words":"Use it."}],self.wd)
        self.write_watch(defect)
        asset.mark_complete(self.packet,{"AI-1":self.clip},self.video,self.wd,watch_log=self.watch)

    def test_pending_draft_fails(self):
        self.write_watch()
        row=self.row(); self.assertFalse(row.ok); self.assertIn("not complete",row.detail)

    def test_complete_replacement_passes(self):
        self.complete(); row=self.row(); self.assertTrue(row.ok,row.detail)

    def test_visible_placeholder_is_nonwaivable(self):
        self.complete(defect=True); row=self.row(); self.assertFalse(row.ok)
        self.assertIn("cannot be waived",row.detail)

    def test_stale_approved_frame_hash_fails(self):
        self.complete()
        with open(self.start,"ab") as fh: fh.write(b"changed")
        row=self.row(); self.assertFalse(row.ok); self.assertIn("changed",row.detail)

    def test_no_packet_is_measured_pass(self):
        os.unlink(self.packet)
        row=compliance.placeholder("compliance:placeholder",{}, {"required":True},
                                   {"_sha256":asset.sha256(self.video)},self.video,self.wd)
        self.assertTrue(row.ok)


if __name__ == "__main__": unittest.main(verbosity=1)
