"""Synthetic helper tests; these do not assess editing or model quality."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import trial


def have_media_tools():
    try:
        trial.media_tool("ffmpeg"); trial.media_tool("ffprobe")
        return True
    except FileNotFoundError:
        return False


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.brief = self.base / "brief.md"
        self.brief.write_text("Synthetic source brief")
        self.root = self.base / "private"
        self.state = trial.initialize(self.root, "synthetic-test", {"brief": self.brief})

    def log(self, events, name="events.jsonl"):
        p = self.base / name
        p.write_text("".join(json.dumps(e) + "\n" for e in events))
        return p

    def native(self, totals, model=trial.SOL, sid="s1"):
        return [{"type": "session_meta", "payload": {"id": sid}},
                {"type": "turn_context", "payload": {"model": model, "effort": "high"}},
                *[{"type": "event_msg", "payload": {"type": "token_count", "info": {
                    "total_token_usage": {"input_tokens": n, "cached_input_tokens": n // 2,
                    "cache_write_input_tokens": 0, "output_tokens": 10,
                    "reasoning_output_tokens": 4, "total_tokens": n + 10}}}}
                  for n in totals]]

    def test_exclusive_init_and_random_permutation(self):
        self.assertCountEqual(self.state["execution_order"], trial.ARMS)
        with self.assertRaises(FileExistsError):
            trial.initialize(self.root, "other", {"brief": self.brief})
        self.assertEqual(trial.read(self.root / "trial.json")["job"], "synthetic-test")

    def test_frozen_copy_is_source_of_truth(self):
        self.brief.write_text("Changed source after freeze")
        self.assertEqual(trial.verify(self.root, self.state), [])
        (self.root / self.state["frozen"]["brief"]["copy"]).write_text("Tampered")
        self.assertTrue(trial.verify(self.root, self.state))

    def test_refuses_public_repository_state(self):
        (self.base / ".git").mkdir()
        with self.assertRaises(ValueError):
            trial.private_root(self.base / "public-trial")

    def test_cumulative_snapshots_not_added_and_subsets_not_doubled(self):
        p = self.log(self.native([100, 100, 200]))
        data = trial.parse_log(p)
        self.assertEqual(data["tokens"]["input_tokens"], 200)
        self.assertEqual(data["tokens"]["total_tokens"], 210)
        self.assertEqual(data["tokens"]["cached_input_tokens"], 100)
        self.assertEqual(data["tokens"]["reasoning_output_tokens"], 4)
        self.assertFalse(data["issues"])

    def test_cli_turns_add_and_unknown_stays_unknown(self):
        p = self.log([{"type": "thread.started", "thread_id": "s1"},
                      *[{"type": "turn.completed", "usage": {"input_tokens": 100,
                         "cached_input_tokens": 50, "output_tokens": 10}} for _ in range(2)]])
        data = trial.parse_log(p)
        self.assertEqual(data["tokens"]["total_tokens"], 220)
        self.assertIsNone(data["tokens"]["reasoning_output_tokens"])
        trial.register_log(self.state, "all_sol", "editor", p)
        self.assertFalse(trial.usage_report(self.state)["groups"]["all_sol"]["model_effort_verified"])

    def test_counter_regression_and_mixed_streams_do_not_claim_totals(self):
        for events in (self.native([200, 100]), self.native([100]) + [
                {"type": "turn.completed", "usage": {"input_tokens": 100, "output_tokens": 10}}]):
            data = trial.parse_log(self.log(events))
            self.assertIsNone(data["tokens"])
            self.assertTrue(data["issues"])

    def test_missing_usage_is_not_zero(self):
        p = self.log(self.native([]))
        trial.register_log(self.state, "all_sol", "editor", p)
        groups = trial.usage_report(self.state)["groups"]
        self.assertIsNone(groups["all_sol"]["known_tokens"]["total_tokens"])
        self.assertIsNone(groups["all_astra"]["known_tokens"]["total_tokens"])

    def test_missing_and_malformed_log_keeps_coverage_gap(self):
        p = self.log(self.native([100]))
        with p.open("a") as f: f.write('{"partial":')
        self.assertTrue(trial.parse_log(p)["issues"])
        p.unlink()
        self.assertTrue(trial.parse_log(p)["issues"])

    def test_same_session_cannot_be_counted_twice(self):
        p = self.log(self.native([100]))
        trial.register_log(self.state, "all_sol", "editor", p)
        trial.register_log(self.state, "all_sol", "editor", p)
        self.assertEqual(len(self.state["logs"]), 1)
        other = self.log(self.native([100]), "another-export.jsonl")
        with self.assertRaises(ValueError):
            trial.register_log(self.state, "hybrid", "editor", other)

    def test_hybrid_worker_on_astra_is_flagged(self):
        p = self.log(self.native([100], model=trial.ASTRA))
        trial.register_log(self.state, "hybrid", "editor", p)
        group = trial.usage_report(self.state)["groups"]["hybrid"]
        self.assertFalse(group["model_effort_verified"])
        self.assertEqual(group["known_tokens"]["total_tokens"], 110)
        self.assertTrue(any("differs" in x for x in group["sessions"][0]["issues"]))

    def test_both_parent_and_worker_counted(self):
        for role, model, sid in (("coordinator", trial.ASTRA, "a"), ("editor", trial.SOL, "s")):
            p = self.log(self.native([100], model=model, sid=sid), sid + ".jsonl")
            trial.register_log(self.state, "hybrid", role, p)
        group = trial.usage_report(self.state)["groups"]["hybrid"]
        self.assertEqual(group["known_tokens"]["total_tokens"], 220)
        self.assertTrue(group["model_effort_verified"])

    def passed_checks(self, media):
        evidence = self.base / "evidence.json"
        evidence.write_text('{"synthetic_fixture": true}')
        checks = trial.checks_template()
        checks.update(status="pass", stage_scope="synthetic fixture only", review_file_sha256=trial.digest(media))
        for item in checks["checks"].values(): item.update(status="pass", evidence=[str(evidence)])
        p = self.base / "checks.json"
        trial.write(p, checks)
        return p

    def test_pass_requires_files_and_consistent_check_status(self):
        media = self.base / "not-a-real-video.mp4"
        media.write_bytes(b"synthetic fixture")
        checks = trial.checks_template()
        checks.update(status="pass", stage_scope="fixture", review_file_sha256=trial.digest(media))
        p = self.base / "checks.json"
        trial.write(p, checks)
        with self.assertRaises(ValueError):
            trial.record_artifact(self.root, self.state, "all_sol", "test", media, p)
        checks["checks"]["picture"].update(status="pass")
        trial.write(p, checks)
        with self.assertRaises(ValueError):
            trial.record_artifact(self.root, self.state, "all_sol", "test", media, p)

    def test_source_can_be_blinded_before_one_final_independent_review(self):
        media = self.base / "source.mp4"; media.write_bytes(b"fixture")
        p = self.passed_checks(media)
        checks = trial.read(p)
        checks["status"] = "ready_for_blinding"
        checks["checks"]["independent_review"] = {"status": "pending_neutral_file", "evidence": []}
        trial.write(p, checks)
        trial.record_artifact(self.root, self.state, "all_sol", "test", media, p)
        item = self.state["artifacts"]["test"]["all_sol"]
        self.assertEqual(item["checks"]["status"], "ready_for_blinding")
        self.assertEqual(item["checks"]["checks"]["independent_review"]["evidence"], [])

    @unittest.skipUnless(have_media_tools(), "Needs local media tools")
    def test_real_neutral_packaging_ballot_hashes_and_early_reveal_gate(self):
        media = self.base / "astra-identifying-name.mp4"
        subprocess.run([trial.media_tool("ffmpeg"), "-nostdin", "-v", "error", "-f", "lavfi", "-i",
                        "color=c=black:s=1080x1920:r=30:d=0.1", "-f", "lavfi", "-i",
                        "anullsrc=r=48000:cl=stereo", "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac",
                        "-metadata", "title=GPT-6 Astra", "-pix_fmt", "yuv420p", "-t", "0.1", str(media)],
                       check=True, capture_output=True)
        for stage in ("first-review", "candidate"):
            checks = self.passed_checks(media)
            source_checks = trial.read(checks)
            source_checks["status"] = "ready_for_blinding"
            source_checks["checks"]["independent_review"] = {"status": "pending_neutral_file", "evidence": []}
            trial.write(checks, source_checks)
            for arm in trial.ARMS:
                trial.record_artifact(self.root, self.state, arm, stage, media, checks)
            public = trial.blind_package(self.root, self.state, stage)
            serialized = json.dumps(public).lower()
            for name in (*trial.ARMS, "astra", "gpt-6"):
                self.assertNotIn(name, serialized)
            self.assertFalse((self.root / "review" / stage / "trial.json").exists())
            self.assertFalse(public["ready_for_owner"])
            for label in ("X1", "X2", "X3"):
                neutral = self.root / "review" / stage / (label + ".mp4")
                streams = trial.probe(neutral)["streams"]
                self.assertEqual(len([s for s in streams if s["codec_type"] == "audio"]), 1)
                subprocess.run([trial.media_tool("ffmpeg"), "-nostdin", "-v", "error", "-i",
                                str(neutral), "-t", "0.1", "-f", "null", "-"],
                               check=True, capture_output=True)
                check = self.passed_checks(neutral)
                result = trial.neutral_check(self.root, self.state, stage, label, check)
            self.assertTrue(result["ready_for_owner"])
            with self.assertRaises(ValueError): trial.blind_package(self.root, self.state, stage)
        ballot = trial.read(self.root / "review/candidate/ballot-template.json")
        ballot["ranking"] = ["X2", "X1", "X3"]
        bp = self.base / "ballot.json"; trial.write(bp, ballot)
        with self.assertRaises(ValueError): trial.reveal(self.root, self.state, "first-review", bp)
        ballot["review_sha256"]["X1"] = "wrong"
        trial.write(bp, ballot)
        with self.assertRaises(ValueError): trial.reveal(self.root, self.state, "candidate", bp)
        ballot = trial.read(self.root / "review/candidate/ballot-template.json")
        ballot["ranking"] = ["X2", "X1", "X3"]; trial.write(bp, ballot)
        report = trial.reveal(self.root, self.state, "candidate", bp)
        self.assertEqual(set(report["identities"]), {"X1", "X2", "X3"})
        self.assertTrue(self.state["blind_stages"]["candidate"]["revealed"])
        early = trial.read(self.root / "review/first-review/ballot-template.json")
        trial.write(bp, early)
        report = trial.reveal(self.root, self.state, "first-review", bp,
                              early_reason="Synthetic test of an explicit early-reveal request")
        self.assertEqual(report["judgment_status"], "revealed_before_judging")

    def test_tied_ranking_is_accepted_without_inventing_a_preference(self):
        # Ballot validation reaches the readiness guard, rather than rejecting ties.
        mapping = {x: {"review_sha256": "fixture"} for x in ("X1", "X2", "X3")}
        self.state["blind_stages"]["candidate"] = {"mapping": mapping}
        folder = self.root / "review/candidate"; folder.mkdir(parents=True)
        trial.write(folder / "manifest.json", {"ready_for_owner": False})
        p = self.base / "ballot.json"
        trial.write(p, {"judge": "Dan", "stage": "candidate", "ranking": [["X1", "X2"], ["X3"]]})
        with self.assertRaisesRegex(ValueError, "Exact neutral-file checks"):
            trial.reveal(self.root, self.state, "candidate", p)

    def test_later_turn_with_missing_model_evidence_is_not_verified(self):
        events = self.native([100]) + [{"type": "turn_context", "payload": {}}]
        p = self.log(events)
        trial.register_log(self.state, "all_sol", "editor", p)
        group = trial.usage_report(self.state)["groups"]["all_sol"]
        self.assertFalse(group["model_effort_verified"])
        self.assertNotIn(trial.SOL, group["known_tokens_by_observed_model"])
        self.assertEqual(group["known_tokens_by_observed_model"]["unknown_or_mixed"]["total_tokens"], 110)


if __name__ == "__main__":
    unittest.main()
