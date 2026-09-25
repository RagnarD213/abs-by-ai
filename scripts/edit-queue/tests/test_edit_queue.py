#!/usr/bin/env python3
"""Unit tests for the overnight edit queue: slot counting, double-claim, stale claim, every stop
condition, routing, eligibility and the verdict parser. Nothing here touches the real job list,
the Drive file, the drive, or launches anything.

  python3 scripts/edit-queue/tests/test_edit_queue.py
"""
import copy, datetime, json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
TMP = tempfile.mkdtemp(prefix="eq-test-")
os.environ["EDIT_QUEUE_DIR"] = TMP
os.environ["EDIT_QUEUE_NO_DRIVE"] = "1"
os.environ["EDIT_QUEUE_SCOREBOARD"] = os.path.join(TMP, "scoreboard.json")
sys.path.insert(0, PKG)
import eq_common as eq                                          # noqa: E402
eq.unshadow()
q, d, runner, review_page = (eq.sibling("queue"), eq.sibling("dispatcher"), eq.sibling("runner"),
                             eq.sibling("review_page"))

NOW = datetime.datetime(2026, 9, 18, 2, 0, 0)          # 2 AM: Dan is asleep
CFG = eq.load_config()


def job(jid, state="ready", size="S", order=1, **kw):
    return dict({"id": jid, "state": state, "size": size, "order": order, "title": jid, "file": "",
                 "claude": "do it", "codex": "do it", "note": "", "rev": 1}, **kw)


def facts(**kw):
    f = {"now": NOW, "pause_file": False, "free_gb": 1200.0, "idle_seconds": 6 * 3600, "foreign_builds": 0,
         "auth": {"claude": (True, ""), "codex": (True, "")}, "pid_alive": lambda pid: False,
         "master": "", "board": "", "work_dirs": {}, "missing_sources": {}}
    f.update(kw)
    return f


def claim(by="claude", pid=111, beat_minutes_ago=1):
    t = (NOW - datetime.timedelta(minutes=beat_minutes_ago)).isoformat(timespec="seconds")
    return {"by": by, "pid": pid, "started": t, "heartbeat": t}


def run(data, f=None, sb=None, cfg=None):
    return d.decide(data, cfg or copy.deepcopy(CFG), f or facts(), sb or {"runs": []})


class Routing(unittest.TestCase):
    def test_phase2_states_and_drive_schema_are_explicit(self):
        self.assertIn("draft_review", q.STATES); self.assertIn("frames_approved", q.STATES)
        old = q.EXPORT; q.EXPORT = TMP
        try:
            self.assertTrue(q.push_drive({"jobs": [job("AV-01", "draft_review")]}))
            status = json.load(open(os.path.join(TMP, "edit-queue-status.json")))
        finally:
            q.EXPORT = old
        self.assertEqual(status["schema"], 2)
        self.assertEqual(status["assetApprovalSchema"], 1)
        self.assertEqual(status["stateLabels"]["frames_approved"], "ASSETS APPROVED: finishing queued")

    def test_dans_assignment_2026_09_17(self):
        # Raw cuts route to Codex; secondary cuts route to Claude since the September 24 reset.
        for g in ("RA", "RO", "DS"):
            self.assertEqual(eq.executor_for(g + "-01", CFG), "codex", g)
        for g in ("AV", "AS", "SL"):
            self.assertEqual(eq.executor_for(g + "-01", CFG), "claude", g)

    def test_rx_is_never_queued(self):
        self.assertIsNone(eq.executor_for("RX-01", CFG))
        self.assertIsNone(eq.executor_for("ZZ-01", CFG))

    def test_prefers_one_of_each_executor(self):
        # With the restored split, the second slot uses Codex for a raw cut.
        cfg = copy.deepcopy(CFG); cfg["unattended"]["groups"] += ["DS"]
        data = {"jobs": [job("AV-01", order=1), job("AV-02", order=2), job("DS-01", order=3)]}
        self.assertEqual(run(data, cfg=cfg)["launches"], [("AV-01", "claude"), ("DS-01", "codex")])

    def test_lowest_order_first_and_revision_first(self):
        data = {"jobs": [job("AV-02", order=2), job("AV-01", order=1)]}
        self.assertEqual(run(data)["launches"][0][0], "AV-01")
        data["jobs"][0]["queue_revision"] = {"round": 1, "words": "fix the captions"}
        self.assertEqual(run(data)["launches"][0][0], "AV-02")

    def test_approved_assets_finish_before_new_ready_work(self):
        data = {"jobs": [job("AV-01", "ready", order=1), job("AV-02", "frames_approved", order=99)]}
        self.assertEqual(run(data)["launches"][0][0], "AV-02")


class Slots(unittest.TestCase):
    def test_slots_counted_by_claims_not_processes(self):
        # a claimed session that is only thinking (no ffmpeg anywhere) still holds its slot
        data = {"jobs": [job("AV-01", "in_progress", claim=claim()), job("AV-02", "in_progress", claim=claim(pid=112)), job("AV-03", order=3)]}
        r = run(data)
        self.assertEqual(r["slots"]["free"], 0)
        self.assertEqual(r["launches"], [])

    def test_foreign_builds_count_toward_the_two(self):
        data = {"jobs": [job("AV-01"), job("AV-02", order=2)]}
        self.assertEqual(len(run(data, facts(foreign_builds=1))["launches"]), 1)
        self.assertEqual(run(data, facts(foreign_builds=2))["launches"], [])
        self.assertEqual(run(data, facts(foreign_builds=5))["launches"], [])

    def test_never_more_than_two(self):
        data = {"jobs": [job(f"AV-0{i}", order=i) for i in range(1, 6)]}
        self.assertEqual(len(run(data)["launches"]), 2)

    def test_foreign_build_grouping_and_own_tree(self):
        ps = {10: (1, "caffeinate -i python runner.py"), 11: (10, "python runner.py"), 12: (11, "codex exec"),
              13: (12, "/x/ffmpeg -i a"),                       # ours: ancestor 10 holds a claim
              20: (1, "zsh"), 21: (20, "/x/ffmpeg -f rawvideo"), 22: (20, "/x/ffmpeg -i pipe"),   # one foreign pipe
              30: (1, "python whisper_run.py"), 40: (1, "grep ffmpeg"), 41: (1, "Electron Renderer ffmpeg")}
        self.assertEqual(d.foreign_builds(ps, {10}), 2)
        self.assertEqual(d.foreign_builds(ps, set()), 3)

    def test_dan_at_machine_drops_to_one_automated_slot(self):
        data = {"jobs": [job("AV-01"), job("AV-02", order=2)]}
        self.assertEqual(len(run(data, facts(idle_seconds=60))["launches"]), 1)
        busy = {"jobs": [job("AV-01", "in_progress", claim=claim()), job("AV-02", order=2)]}
        self.assertEqual(run(busy, facts(idle_seconds=60))["launches"], [])
        self.assertEqual(len(run(busy, facts(idle_seconds=3600))["launches"]), 1)


class Claims(unittest.TestCase):
    def setUp(self):
        json.dump({"jobs": [job("AV-01"), job("AV-02", "needs")]}, open(q.JOBS, "w"))

    def test_double_claim_refused(self):
        data = q.load()
        self.assertTrue(q.claim_job(data, "AV-01", "claude", 1)[0])
        ok, why = q.claim_job(data, "AV-01", "codex", 2)
        self.assertFalse(ok); self.assertIn("already has a claim", why)

    def test_double_claim_refused_across_processes(self):
        cli = [sys.executable, os.path.join(PKG, "queue.py"), "claim", "AV-01", "--pid", "1", "--by"]
        procs = [subprocess.Popen(cli + [w], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=os.environ) for w in ("a", "b", "c", "d")]
        codes = sorted(p.wait() for p in procs)
        self.assertEqual(codes, [0, 3, 3, 3])

    def test_cannot_claim_a_job_that_is_not_launchable(self):
        self.assertFalse(q.claim_job(q.load(), "AV-02", "claude", 1)[0])

    def test_heartbeat_and_release_cli(self):
        cli = [sys.executable, os.path.join(PKG, "queue.py")]
        subprocess.run(cli + ["claim", "AV-01", "--by", "x", "--pid", "1"], check=True, capture_output=True)
        j = q.find(q.load(), "AV-01"); j["claim"]["heartbeat"] = "2026-01-01T00:00:00"; q.save({"jobs": [j, job("AV-02", "needs")]})
        subprocess.run(cli + ["heartbeat", "AV-01"], check=True, capture_output=True)
        self.assertNotEqual(q.find(q.load(), "AV-01")["claim"]["heartbeat"], "2026-01-01T00:00:00")
        subprocess.run(cli + ["release", "AV-01"], check=True, capture_output=True)
        self.assertNotIn("claim", q.find(q.load(), "AV-01"))

    def test_stale_claim_becomes_stalled_never_relaunched(self):
        data = {"jobs": [job("AV-01", "in_progress", claim=claim(beat_minutes_ago=46)), job("AV-02", order=2)]}
        r = run(data)
        self.assertEqual([s[0] for s in r["stalls"]], ["AV-01"])
        self.assertNotIn("AV-01", [l[0] for l in r["launches"]])

    def test_old_heartbeat_but_pid_alive_is_still_live(self):
        data = {"jobs": [job("AV-01", "in_progress", claim=claim(beat_minutes_ago=300))]}
        r = run(data, facts(pid_alive=lambda pid: True))
        self.assertEqual(r["stalls"], []); self.assertEqual(r["slots"]["live_claims"], ["AV-01"])

    def test_pid_gone_but_heartbeat_fresh_is_still_live(self):
        data = {"jobs": [job("AV-01", "in_progress", claim=claim(beat_minutes_ago=44))]}
        self.assertEqual(run(data)["stalls"], [])

    def test_stalled_job_is_not_eligible_and_frees_its_slot(self):
        data = {"jobs": [job("AV-01", "stalled", claim=claim(beat_minutes_ago=500)), job("AV-02", order=2), job("AV-03", order=3)]}
        r = run(data)
        self.assertEqual(r["stalls"], []); self.assertEqual([l[0] for l in r["launches"]], ["AV-02", "AV-03"])

    def test_stall_cli_sets_state(self):
        subprocess.run([sys.executable, os.path.join(PKG, "queue.py"), "stall", "AV-01", "--note", "x"], check=True, capture_output=True, env=os.environ)
        self.assertEqual(q.find(q.load(), "AV-01")["state"], "stalled")


class StopConditions(unittest.TestCase):
    DATA = {"jobs": [job("AV-01"), job("AV-02", order=2)]}

    def assertStops(self, r, word):
        self.assertEqual(r["launches"], [])
        self.assertTrue(any(word in s for s in r["stops"]), r["stops"])

    def test_baseline_launches(self):
        self.assertEqual(len(run(self.DATA)["launches"]), 2)

    def test_pause_file(self):
        self.assertStops(run(self.DATA, facts(pause_file=True)), "PAUSE")

    def test_volume_unmounted(self):
        self.assertStops(run(self.DATA, facts(free_gb=None)), "not mounted")

    def test_volume_low(self):
        self.assertStops(run(self.DATA, facts(free_gb=149.0)), "GB free")
        self.assertEqual(len(run(self.DATA, facts(free_gb=151.0))["launches"]), 2)

    def test_review_queue_full(self):
        full = {"jobs": self.DATA["jobs"] + [job(f"DS-0{i}", "delivered") for i in range(4)]}
        self.assertStops(run(full), "review queue")
        three = {"jobs": self.DATA["jobs"] + [job(f"DS-0{i}", "delivered") for i in range(3)]}
        self.assertEqual(len(run(three)["launches"]), 2)

    def test_nightly_cap(self):
        sb = {"runs": [{"executor": "claude", "started": "2026-09-17T22:00:00", "ended": "2026-09-17T23:00:00", "outcome": "delivered"}] * 3}
        self.assertStops(run(self.DATA, sb=sb), "nightly")
        sb = {"runs": sb["runs"][:2]}
        self.assertEqual(len(run(self.DATA, sb=sb)["launches"]), 1)      # one launch left tonight
        old = {"runs": [{"executor": "claude", "started": "2026-09-16T22:00:00", "ended": "2026-09-16T23:00:00", "outcome": "delivered"}] * 3}
        self.assertEqual(len(run(self.DATA, sb=old)["launches"]), 2)     # last night's launches don't count

    def test_usage_limit_backs_off_two_hours_then_tries(self):
        sb = {"runs": [{"executor": "claude", "started": "2026-09-18T00:30:00", "ended": "2026-09-18T01:00:00", "outcome": "usage_limited"}]}
        r = run(self.DATA, sb=sb)
        self.assertEqual(r["launches"], []); self.assertIn("claude", r["executor_stops"])
        r = run(self.DATA, facts(now=NOW + datetime.timedelta(hours=1, minutes=1)), sb=sb)
        self.assertEqual(len(r["launches"]), 2)                          # 03:01, backoff over: launches again

    def test_usage_limit_on_one_executor_does_not_stop_the_other(self):
        # A Claude outage stops AV but leaves the Codex raw-cut route available.
        cfg = copy.deepcopy(CFG); cfg["unattended"]["groups"] += ["DS"]
        sb = {"runs": [{"executor": "claude", "started": "2026-09-18T01:30:00", "ended": "2026-09-18T01:40:00", "outcome": "usage_limited"}]}
        data = {"jobs": [job("AV-01"), job("DS-01", order=2)]}
        self.assertEqual(run(data, sb=sb, cfg=cfg)["launches"], [("DS-01", "codex")])

    def test_signed_out_executor_launches_nothing(self):
        r = run(self.DATA, facts(auth={"claude": (False, "claude: not signed in"), "codex": (True, "")}))
        self.assertEqual(r["launches"], []); self.assertIn("claude", r["executor_stops"])

    def test_group_paused_by_circuit_breaker(self):
        cfg = copy.deepcopy(CFG); cfg["paused_groups"] = [{"group": "AV", "executor": "claude", "reason": "captions drift"}]
        r = run(self.DATA, cfg=cfg)
        self.assertEqual(r["launches"], []); self.assertIn("captions drift", r["skipped"]["AV-01"])


class Eligibility(unittest.TestCase):
    def why(self, j, f=None, cfg=None):
        r = run({"jobs": [j]}, f, cfg=cfg)
        return r["skipped"].get(j["id"]) if not r["launches"] else None

    def test_states(self):
        for s in ("draft_review", "needs", "blocked", "in_progress", "delivered", "finalized", "uploaded", "stalled"):
            self.assertEqual(run({"jobs": [job("AV-01", s)]})["launches"], [], s)

    def test_pilot_is_small_no_ai_slot_groups_only(self):
        self.assertIn("size", self.why(job("AV-02", size="M")))
        self.assertIn("pilot", self.why(job("RA-02")))
        self.assertIn("pilot", self.why(job("DS-01")))

    def test_your_calls_row_blocks(self):
        master = "# x\n## Your calls (these unblock jobs)\n\n| job | the decision |\n|---|---|\n| AS-01, AV-01 | still wanted? |\n\n---\n\n## LIST 1\n| [AV-02](f) |\n"
        self.assertEqual(d.your_calls_jobs(master), {"AS-01", "AV-01"})
        self.assertIn("Your calls", self.why(job("AV-01"), facts(master=master)))

    def test_board_active_blocks(self):
        board = "# DAN'S DECISIONS\n- AV-09 thing\n# ACTIVE\n\n**AV-01 first cut — ACTIVE, Claude.**\n\n# BLOCKED\nAV-03\n"
        self.assertEqual(d.board_active_jobs(board), {"AV-01"})
        self.assertIn("ACTIVE", self.why(job("AV-01"), facts(board=board)))

    def test_existing_work_directory_blocks_unless_dan_asked_for_a_revision(self):
        f = facts(work_dirs={"AV-01": ["av01"]})
        self.assertIn("work directory", self.why(job("AV-01"), f))
        self.assertIsNone(self.why(job("AV-01", queue_revision={"round": 1, "words": "x"}), f))
        self.assertIsNone(self.why(job("AV-01", "frames_approved"), f))

    def test_missing_source_blocks(self):
        self.assertIn("source not on disk", self.why(job("AV-01"), facts(missing_sources={"AV-01": ["/Volumes/Extreme/x.mp4"]})))

    def test_unattended_false_blocks(self):
        self.assertIn("unattended:false", self.why(job("AV-01", unattended=False)))

    def test_missing_sources_parser(self):
        doc = os.path.join(TMP, "AV-77.md")
        real = os.path.join(TMP, "real.mp4"); open(real, "w").close()
        open(doc, "w").write(f"src `{real}` and `/Volumes/Nope/gone.mp4`, out `title | claude | 9x16.mp4`, tpl `Short-form video content/<slug>.mp4`, "
                             f"own `{CFG['work_root']}/AV-77/`")
        self.assertEqual(d.missing_sources(job("AV-77", file="AV-77.md"), CFG), ["/Volumes/Nope/gone.mp4"])
        self.assertTrue(d.missing_sources(job("AV-78", file="nope.md"), CFG))

    def test_a_jobs_own_output_is_not_a_missing_source(self):
        # found on the first real launch (DS-01, 2026-09-17): the deliverable path was read as a source
        doc = os.path.join(TMP, "DS-77.md")
        open(doc, "w").write("## Source\n`/Volumes/Nope/raw.mp4`\n## Build\nold `Short-form video content/ds-77_draft.mp4`\n"
                             "## Deliver\n`/Volumes/Nope/final.mp4`\n## Starter prompts\n`/Volumes/Nope/x.mp4`\n")
        self.assertEqual(d.missing_sources(job("DS-77", file="DS-77.md"), CFG), ["/Volumes/Nope/raw.mp4"])


class Runner(unittest.TestCase):
    def test_verdict_parser(self):
        wd = tempfile.mkdtemp(dir=TMP)
        for n, text, want in ((1, "VERDICT: SHIP\nfine", "SHIP"), (2, "**VERDICT: DOES NOT SHIP**\nbad", "DOES NOT SHIP"),
                              (3, "Looks good to me, ship it", "NO VERDICT")):
            with open(os.path.join(wd, f"QUEUE-REVIEW-{n}.md"), "w") as fh:
                fh.write(text)
            self.assertEqual(runner.read_verdict(wd, n)[0], want)
        self.assertEqual(runner.read_verdict(wd, 9)[0], "NO VERDICT")     # a review that did not run is a failure

    def test_failure_classifier(self):
        self.assertEqual(runner.classify_failure(1, "Not logged in · Please run /login", CFG), "auth_failed")
        self.assertEqual(runner.classify_failure(1, "You've hit your usage limit. Try again at 3am", CFG), "usage_limited")
        # the real wording from the first Claude launch (AV-01, 2026-09-17 20:23), which the first pattern list missed
        self.assertEqual(runner.classify_failure(
            1, "You've hit your monthly spend limit · raise it at claude.ai/settings/usage?from=cc_cli_limit_message · "
               "your session limit resets 9pm (America/Chicago)", CFG), "usage_limited")
        self.assertEqual(runner.classify_failure(1, "Traceback ...", CFG), "session_failed")
        self.assertEqual(runner.classify_failure(-9, "", CFG), "timeout")
        self.assertEqual(runner.classify_failure(runner.BUDGET_EXCEEDED_CODE, "usage limit", CFG), "budget_exceeded")

    def test_size_budget_job_override_and_no_budget(self):
        base = eq.job_budget(job("AV-01", size="S"), CFG)
        self.assertEqual((base["edit_hours"], base["full_renders"], base["review_hours"]), (2.5, 2, 0.75))
        override = eq.job_budget(job("AV-01", size="S", budget={"edit_hours": 4, "full_renders": 5}), CFG)
        self.assertEqual((override["edit_hours"], override["full_renders"], override["review_hours"]), (4, 5, 0.75))
        lifted = eq.job_budget(job("AV-01", size="S"), CFG, no_budget=True)
        self.assertFalse(lifted["enabled"])
        self.assertIsNone(lifted["full_renders"])
        self.assertEqual(lifted["edit_hours"], CFG["claims"]["max_job_hours"])

    def test_pre_render_check_counts_full_renders_and_refuses_the_next(self):
        wd = tempfile.mkdtemp(dir=TMP)
        json.dump({"status": "not_applicable", "reason": "Fixture has no risky source choice."},
                  open(os.path.join(wd, "PRE_RENDER_CHECK.json"), "w"))
        budget = eq.start_budget(job("AV-01", size="S"), CFG, wd, "fixture-run")
        self.assertEqual(budget["renders_used"], 0)
        self.assertEqual(runner.validate_pre_render(wd), [])
        self.assertEqual(eq.load_budget(wd)["renders_used"], 0, "making and checking previews does not spend a full render")
        cli = [sys.executable, os.path.join(PKG, "pre_render_check.py"), wd]
        first = subprocess.run(cli, capture_output=True, text=True)
        second = subprocess.run(cli, capture_output=True, text=True)
        refused = subprocess.run(cli, capture_output=True, text=True)
        self.assertEqual((first.returncode, second.returncode, refused.returncode), (0, 0, 1))
        self.assertIn("full-render budget exhausted", refused.stdout)
        self.assertEqual(eq.load_budget(wd)["renders_used"], 2)

    def test_review_page_budget_stop_label(self):
        self.assertIn("stopped at budget", review_page.budget_stop_label(
            {"outcome": "budget_exceeded", "budget": {"exceeded": True}}))
        self.assertEqual(review_page.budget_stop_label({"outcome": "parked", "budget": {"exceeded": False}}), "")

    def test_commands_are_unattended_and_locked_down(self):
        cx = eq.build_command("codex", CFG, "/w/AV-01")
        self.assertIn('approval_policy="never"', cx); self.assertEqual(cx[-1], "-"); self.assertIn("/w/AV-01", cx)
        # Dan, 2026-09-17: edits run Sol / high; the queue's own review sessions use review_effort
        self.assertIn("gpt-5.6-sol", cx); self.assertIn('model_reasoning_effort="high"', cx)
        if eq.resolve_binary("claude", CFG):
            cl = eq.build_command("claude", CFG, "/w/AV-01", "review-1")
            self.assertIn("-p", cl); self.assertIn("bypassPermissions", cl); self.assertIn("--strict-mcp-config", cl)
            self.assertIn("ra-reviewer", cl)
            self.assertNotIn("ra-reviewer", eq.build_command("claude", CFG, "/w/AV-01", "edit"))

    def test_newest_claude_version_wins(self):
        self.assertLess(eq._version_key("/claude-code/2.1.260/x"), eq._version_key("/claude-code/2.1.270/x"))
        self.assertLess(eq._version_key("/claude-code/2.1.99/x"), eq._version_key("/claude-code/2.1.270/x"))

    def test_revision_work_packet_is_short_and_preserves_approved_elements(self):
        wd = tempfile.mkdtemp(dir=TMP)
        j = job("AV-01", queue_revision={"round": 3, "words": "Replace only the workout shot",
                                         "approved_elements": ["audio", "app demo"]})
        p = runner.write_work_packet(j, wd, "run-1", {"files": ["/old.mp4"], "_archived_path": "/old-delivery.json"})
        self.assertEqual(p["revision_number"], 3)
        self.assertEqual(p["requested_changes"], ["Replace only the workout shot"])
        self.assertEqual(p["approved_elements"], ["audio", "app demo"])
        self.assertEqual(p["reuse_candidates"]["files"], ["/old.mp4"])

    def test_usage_row_marks_unavailable_tokens(self):
        row = eq.model_usage_record("codex", CFG, "editor")
        self.assertEqual(row["measurement"], "unavailable")
        self.assertIsNone(row["input_tokens"])
        self.assertIn("not exposed", row["reason"])
        measured = eq.model_usage_record("codex", CFG, "editor", "done\ntokens used\n156,790\n")
        self.assertEqual(measured["total_tokens"], 156790)
        self.assertEqual(measured["measurement"], "available_total_only")

    def test_review_page_names_unavailable_measurements(self):
        line = review_page.efficiency_line({"model_usage": [], "paid_provider_costs": None})
        self.assertIn("model usage unavailable", line)
        self.assertIn("paid-provider costs unavailable", line)

    def test_delivery_contract_requires_reuse_cost_and_preview_evidence(self):
        wd = tempfile.mkdtemp(dir=TMP)
        json.dump({"status": "not_applicable", "reason": "Only caption text changed; source selection is unchanged."},
                  open(os.path.join(wd, "PRE_RENDER_CHECK.json"), "w"))
        delivered = os.path.join(wd, "cut.mp4")
        open(delivered, "w").close()
        packet = {"revision_number": 2}
        info = {"files": [delivered], "review_copy": delivered, "gate": "PASS",
                "revision_count": 2, "approved_elements": ["audio"],
                "reuse": {k: {"status": "reused", "evidence": "REUSE_REPORT.json"}
                          for k in ("scenes", "audio", "transcript", "assets")},
                "generation_spend_usd": 0,
                "paid_provider_costs": [{"provider": "none", "usd": 0}]}
        self.assertEqual(runner.validate_delivery(info, wd, packet), [])
        info["reuse"].pop("audio")
        self.assertTrue(any("reuse.audio" in e for e in runner.validate_delivery(info, wd, packet)))

    def test_stock_stage_cannot_claim_preview_check_not_applicable(self):
        wd = tempfile.mkdtemp(dir=TMP)
        draft = os.path.join(wd,"DRAFT.mp4"); open(draft,"wb").write(b"draft")
        src = os.path.join(wd,"src.mp4"); open(src,"wb").write(b"source")
        prev = os.path.join(wd,"preview.mp4"); open(prev,"wb").write(b"preview")
        rec = lambda p: {"path":p,"sha256":runner.asset.sha256(p)}
        item={"id":"B-1","type":"stock","in":1.0,"out":2.0,"duration":1.0,"spoken_beat":"beat",
              "intended_action":"action","affected_scenes":["s1"],"boundary_joins":[],"estimated_usd":0,
              "placeholder":{"label":"PLACEHOLDER — B-1","sha256":"0"*64},
              "preview":dict(rec(prev),preview_seconds=1.0),
              "source":dict(rec(src),trim_in=0.0,trim_out=1.0,crop="center",rights="licensed"),
              "approval":{"status":"pending","selected_hashes":[],"words":None,"timestamp":None,"selection_fingerprint":None},
              "final_clip":None}
        packet={"schema_version":1,"video_id":"AV-01","revision":0,"status":"approval_required","draft":rec(draft),
                "prior_paid_spend_usd":0,"items":[item],"created_at":"2026-09-18T10:00:00-05:00"}
        marker={"schema":1,"gate":"DRAFT","revision_count":0,"packet":os.path.join(wd,"placeholders.json"),
                "packet_material_fingerprint":runner.asset.packet_material_fingerprint(packet),"draft_sha256":rec(draft)["sha256"],
                "stage_one_ended":"2026-09-18T10:01:00-05:00","full_render_count":1,
                "paid_provider_costs":[{"provider":"none","usd":0}]}
        json.dump(marker,open(os.path.join(wd,"DRAFT-DELIVERY.json"),"w"))
        json.dump({"status":"not_applicable","reason":"incorrect fixture claim"},open(os.path.join(wd,"PRE_RENDER_CHECK.json"),"w"))
        errors=runner.validate_draft_delivery(wd,{"revision_number":0},packet)
        self.assertTrue(any("status verified" in x for x in errors),errors)


if __name__ == "__main__":
    unittest.main(verbosity=1)
