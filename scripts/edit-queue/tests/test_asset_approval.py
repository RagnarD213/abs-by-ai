#!/usr/bin/env python3
"""Schema-1 approval contract tests. Every file and registry is an isolated temporary fixture."""
import copy, json, os, sys, tempfile, unittest

PKG = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PKG)
import asset_approval as asset  # noqa: E402


class AssetApproval(unittest.TestCase):
    def setUp(self):
        self.wd = tempfile.mkdtemp(prefix="eq-assets-")
        self.packet_path = os.path.join(self.wd, asset.PACKET_NAME)
        self.draft = self.file("DRAFT-test.mp4", b"draft")
        self.start = self.file("start.png", b"start")
        self.end = self.file("end.png", b"end")
        self.preview = self.file("preview.mp4", b"moving preview")
        self.source = self.file("source.mp4", b"source")

    def file(self, name, body):
        path = os.path.join(self.wd, name)
        with open(path, "wb") as fh: fh.write(body)
        return path

    def rec(self, path, **extra):
        return dict(path=path, sha256=asset.sha256(path), **extra)

    def item(self, iid="AI-1"):
        return {"id": iid, "type": "ai_motion", "in": 1.0, "out": 2.5, "duration": 1.5,
                "spoken_beat": "make this exercise clear", "intended_action": "slow controlled crunch",
                "affected_scenes": ["scene-2"], "boundary_joins": ["join-1"], "estimated_usd": 0.12,
                "placeholder": {"label": f"PLACEHOLDER — {iid}", "sha256": "0" * 64},
                "start_frame": self.rec(self.start), "end_frame": self.rec(self.end),
                "approval": {"status": "pending", "selected_hashes": [], "words": None,
                             "timestamp": None, "selection_fingerprint": None}, "final_clip": None}

    def packet(self, items=None):
        return {"schema_version": 1, "video_id": "FIXTURE-01", "revision": 0,
                "status": "approval_required", "draft": self.rec(self.draft),
                "prior_paid_spend_usd": 0, "prior_paid_spend_reason": "synthetic fixture",
                "items": items if items is not None else [self.item()]}

    def test_atomic_write_approval_and_complete_are_hash_bound(self):
        asset.write_packet(self.packet_path, self.packet(), self.wd)
        approved = asset.decide(self.packet_path, [{"id": "AI-1", "status": "approved", "words": " Use this one. "}], self.wd)
        self.assertEqual(approved["status"], "approved")
        self.assertEqual(approved["items"][0]["approval"]["words"], " Use this one. ")
        clip = self.file("clip.mp4", b"generated from approved frames")
        final = self.file("FINAL.mp4", b"final without placeholder")
        watch = self.file("watch.json", b"{}")
        with self.assertRaisesRegex(asset.PacketError, "requires the final chronological watch log"):
            asset.mark_complete(self.packet_path, {"AI-1": clip}, final, self.wd)
        complete = asset.mark_complete(self.packet_path, {"AI-1": clip}, final, self.wd, watch_log=watch)
        self.assertEqual(complete["status"], "complete")
        with open(clip, "ab") as fh: fh.write(b"stale")
        with self.assertRaisesRegex(asset.PacketError, "changed"):
            asset.read_packet(self.packet_path, self.wd, require_complete=True, delivered_video=final, watch_log=watch)

    def test_partial_duplicate_and_wordless_rejection_are_refused(self):
        packet = self.packet([self.item("AI-1"), self.item("AI-2")])
        asset.write_packet(self.packet_path, packet, self.wd)
        with self.assertRaisesRegex(asset.PacketError, "every current item"):
            asset.decide(self.packet_path, [{"id": "AI-1", "status": "approved", "words": "yes"}], self.wd)
        with self.assertRaisesRegex(asset.PacketError, "duplicate"):
            asset.decide(self.packet_path, [{"id": "AI-1", "status": "approved", "words": "yes"}] * 2, self.wd)
        with self.assertRaisesRegex(asset.PacketError, "exact approval/rejection words"):
            asset.decide(self.packet_path, [{"id": "AI-1", "status": "rejected", "words": ""},
                                            {"id": "AI-2", "status": "approved", "words": "Approved"}], self.wd)

    def test_material_change_resets_only_changed_approval(self):
        packet = self.packet([self.item("AI-1"), self.item("AI-2")])
        asset.write_packet(self.packet_path, packet, self.wd)
        asset.decide(self.packet_path, [{"id": x, "status": "approved", "words": f"approve {x}"}
                                        for x in ("AI-1", "AI-2")], self.wd)
        changed = copy.deepcopy(packet)
        changed["items"][0]["intended_action"] = "different motion"
        result = asset.write_packet(self.packet_path, changed, self.wd)
        self.assertEqual(result["items"][0]["approval"]["status"], "pending")
        self.assertEqual(result["items"][1]["approval"]["status"], "approved")

    def test_traversal_duplicate_ids_and_stale_input_hash_fail(self):
        bad = self.packet([self.item("AI-1"), self.item("AI-1")])
        with self.assertRaisesRegex(asset.PacketError, "unique IDs"):
            asset.write_packet(self.packet_path, bad, self.wd)
        bad = self.packet(); bad["draft"] = {"path": "/etc/hosts", "sha256": asset.sha256("/etc/hosts")}
        with self.assertRaisesRegex(asset.PacketError, "escapes"):
            asset.write_packet(self.packet_path, bad, self.wd)
        asset.write_packet(self.packet_path, self.packet(), self.wd)
        with open(self.start, "ab") as fh: fh.write(b"changed")
        with self.assertRaisesRegex(asset.PacketError, "changed"):
            asset.read_packet(self.packet_path, self.wd)

    def test_stock_requires_moving_preview_trim_crop_and_rights(self):
        item = self.item("STOCK-1")
        item.update(type="stock", estimated_usd=0, preview=self.rec(self.preview, preview_seconds=1.5),
                    source=self.rec(self.source, trim_in=3.0, trim_out=4.5, crop="center crop", rights="licensed fixture"))
        item.pop("start_frame"); item.pop("end_frame")
        asset.write_packet(self.packet_path, self.packet([item]), self.wd)
        changed = json.load(open(self.packet_path)); changed["items"][0]["source"].pop("rights")
        with self.assertRaisesRegex(asset.PacketError, "rights"):
            asset.validate_packet(changed, self.wd)
        changed = json.load(open(self.packet_path)); changed["items"][0]["preview"]["preview_seconds"] = 8
        with self.assertRaisesRegex(asset.PacketError, "exact"):
            asset.validate_packet(changed, self.wd)

    def test_duration_or_trim_change_resets_approval_and_budget_is_hard(self):
        over_authority = self.packet(); over_authority["generation_budget_usd"] = 5.01
        with self.assertRaisesRegex(asset.PacketError, "cannot exceed"):
            asset.write_packet(self.packet_path, over_authority, self.wd)
        packet = self.packet(); packet["generation_budget_usd"] = 5.0
        packet["items"][0]["estimated_usd"] = 4.25; packet["prior_paid_spend_usd"] = 1.0
        asset.write_packet(self.packet_path, packet, self.wd)
        with self.assertRaisesRegex(asset.PacketError, "exceed"):
            asset.decide(self.packet_path,[{"id":"AI-1","status":"approved","words":"yes"}],self.wd)
        rejected = asset.decide(self.packet_path,[{"id":"AI-1","status":"rejected","words":"Too expensive."}],self.wd)
        self.assertEqual(rejected["items"][0]["approval"]["status"],"rejected")
        packet["prior_paid_spend_usd"] = 0
        asset.write_packet(self.packet_path, packet, self.wd)
        asset.decide(self.packet_path,[{"id":"AI-1","status":"approved","words":"yes"}],self.wd)
        packet["items"][0]["out"] = 3.0; packet["items"][0]["duration"] = 2.0
        changed = asset.write_packet(self.packet_path,packet,self.wd)
        self.assertEqual(changed["items"][0]["approval"]["status"],"pending")


if __name__ == "__main__": unittest.main(verbosity=1)
