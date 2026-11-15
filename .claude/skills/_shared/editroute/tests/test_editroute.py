"""Unit tests for two-Mac edit routing: `python3 editroute.py selftest` (or python3 -m unittest in this folder).

Every rule in VIDEO-RULES.md "Two Macs" / handoff 03 has a test, plus an unreachable M2, the per-Mac numbers
(slots, cores present/away/night, work-folder order) and the combined waiting line. Nothing here touches the live
edit cap, render queue or decision log: every state folder is a temporary one.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ER = HERE.parent
SHARED = ER.parent
sys.path.insert(0, str(ER))
import editroute as er                                              # noqa: E402
import hostcfg                                                      # noqa: E402

CFG = json.loads((ER / "hosts.json").read_text())


def st(host, in_use=(), waiting=(), edits=None, load5=1.0, ncpu=12, pressure=1, reachable=True, job=None):
    if not reachable:
        return dict(host=host, reachable=False, error="ssh: connect timed out")
    e = dict(edits or {})
    for j in in_use:
        e.setdefault(j, "active")
    for j in waiting:
        e.setdefault(j, "waiting")
    out = dict(host=host, reachable=True, ncpu=ncpu, load=[load5, load5, load5], pressure=pressure,
               drives=[dict(drive='internal',free_gb=500)], storage_commitments={},editcap=dict(cap=CFG["hosts"][host]["slots"], in_use=list(in_use), waiting=list(waiting), edits=e))
    if job is not None:
        out["job"] = job
    return out


def both(m6=None, m2=None):
    return {"m6": m6 or st("m6"), "m2": m2 or st("m2")}


def pick(statuses, job="DS-200", kind="OTHER", rnd=1, chroma=False, named=None, move=False, reserved=None):
    return er.decide(job, kind, rnd, chroma, named, move, statuses, CFG, reserved)


class Config(unittest.TestCase):
    def test_numbers_dan_gets(self):
        self.assertEqual(CFG["hosts"]["m6"]["slots"], 2)
        self.assertEqual(CFG["hosts"]["m2"]["slots"], 3)
        self.assertEqual(CFG["hosts"]["m6"]["slots"] + CFG["hosts"]["m2"]["slots"], 5, "total stays 5")
        self.assertEqual(CFG["hosts"]["m2"]["cores_present"], 8)
        self.assertEqual(CFG["hosts"]["m2"]["cores_away"], 8)
        self.assertEqual(CFG["hosts"]["m6"]["cores_away"], 12 - 2, "M6 away/night: all but 2 of its 12 cores")

    def test_host_lookup_and_slots(self):
        for h, n in (("m6", 2), ("m2", 3)):
            os.environ["EDITROUTE_HOST"] = h
            try:
                self.assertEqual(hostcfg.this_host(), h)
                self.assertEqual(hostcfg.slots(), n)
            finally:
                del os.environ["EDITROUTE_HOST"]

    def test_unknown_mac_keeps_old_defaults(self):
        os.environ["EDITROUTE_HOST"] = "laptop"
        try:
            self.assertIsNone(hostcfg.this_host())
            self.assertIsNone(hostcfg.slots())
            self.assertIsNone(hostcfg.core_budget())
        finally:
            del os.environ["EDITROUTE_HOST"]

    def test_m6_cores_present_away_night(self):
        self.assertEqual(hostcfg.core_budget("m6", hour=14, idle=60), 6, "Dan at the Mac: about half")
        self.assertEqual(hostcfg.core_budget("m6", hour=14, idle=31 * 60), 10, "away 30+ min: all but 2")
        self.assertEqual(hostcfg.core_budget("m6", hour=14, idle=29 * 60), 6)
        self.assertEqual(hostcfg.core_budget("m6", hour=22, idle=0), 6, "10 PM recent input remains present")
        self.assertEqual(hostcfg.core_budget("m6", hour=6, idle=0), 6, "night recent input remains present")
        self.assertEqual(hostcfg.core_budget("m6", hour=7, idle=0), 6, "7 AM onwards")
        self.assertEqual(hostcfg.core_budget("m2", hour=14, idle=0), 8, "M2: 8 always")
        self.assertEqual(hostcfg.core_budget("m2", hour=23, idle=0), 8)

    def test_broken_config_fails_open(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "hosts.json"
            p.write_text("{not json")
            os.environ["EDITROUTE_HOSTS"] = str(p)
            os.environ["EDITROUTE_HOST"] = "m6"
            try:
                self.assertEqual(hostcfg.load(), {})
                self.assertIsNone(hostcfg.slots())
                self.assertIsNone(hostcfg.core_budget())
                r = subprocess.run([sys.executable, "-c", "import sys; sys.path.insert(0, %r); import editcap; "
                                    "print(editcap.CAP)" % str(SHARED / "editcap")], capture_output=True, text=True,
                                   env=dict(os.environ, EDITCAP_MAX=""))
                self.assertEqual(r.stdout.strip(), "5", r.stderr)
            finally:
                del os.environ["EDITROUTE_HOSTS"], os.environ["EDITROUTE_HOST"]

    def test_editcap_and_renderq_read_the_host(self):
        code = ("import sys; sys.path[:0] = [%r, %r]; import editcap, renderq; print(editcap.CAP, renderq.core_budget())"
                % (str(SHARED / "editcap"), str(SHARED / "renderq")))
        for h, hour, idle, want in (("m6", "14", "0", "2 6"), ("m6", "23", "0", "2 6"), ("m2", "14", "0", "3 8")):
            env = dict(os.environ, EDITROUTE_HOST=h, EDITROUTE_HOUR=hour, EDITROUTE_IDLE_S=idle, EDITCAP_MAX="",
                       GATE_BUDGET="")
            env.pop("EDITCAP_MAX")
            env.pop("GATE_BUDGET")
            r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env)
            self.assertEqual(r.stdout.strip(), want, (h, r.stderr))

    def test_m2_new_work_folder_goes_on_the_extreme_first(self):
        from unittest.mock import patch
        sys.path.insert(0,str(SHARED/'renderq'));import renderq
        with tempfile.TemporaryDirectory() as d:
            ext,internal=Path(d)/'Extreme',Path(d)/'internal'
            ext.mkdir();internal.mkdir()
            with patch.object(renderq,'find_workdir',return_value=None),patch.object(renderq,'mounted_work_drives',return_value=[('Extreme',ext)]),patch.object(renderq,'INTERNAL_WORK',internal),patch.object(renderq.work_storage,'check',return_value='fixture room'):
                with patch.dict(os.environ,{'EDITROUTE_HOST':'m2'}):
                    self.assertEqual(renderq.workdir('DS-200'),ext/'_edit_work'/'DS-200')
                with patch.dict(os.environ,{'EDITROUTE_HOST':'m6'}):
                    self.assertEqual(renderq.workdir('DS-201'),internal/'DS-201')


class Rules(unittest.TestCase):
    def test_rule1_existing_work_folder_stays(self):
        s = both(m2=st("m2", job=dict(folders=[dict(drive="Extreme", path="/Volumes/Extreme/_edit_work/RO-40",
                                                     entries=12, mtime=1)], editcap=None)),
                 m6=st("m6", job=dict(folders=[], editcap=None)))
        h, why = pick(s, "RO-40", "SFC")                      # an SFC would prefer the M6, but its folder is on the M2
        self.assertEqual(h, "m2")
        self.assertIn("rule 1", why[0])

    def test_rule1_beats_a_named_mac_unless_moved(self):
        s = both(m6=st("m6", job=dict(folders=[dict(drive="internal", path="/x/SL-30", entries=4, mtime=1)])),
                 m2=st("m2", job=dict(folders=[])))
        self.assertEqual(pick(s, "SL-30", "SFL", named="m2")[0], "m6")
        self.assertEqual(pick(s, "SL-30", "SFL", named="m2", move=True)[0], "m2")

    def test_rule1_folders_on_both_live_slot_wins(self):
        s = both(m6=st("m6", job=dict(folders=[dict(drive="internal", path="/a", entries=40, mtime=9)])),
                 m2=st("m2", job=dict(folders=[dict(drive="Extreme", path="/b", entries=3, mtime=1)],
                                      editcap="active")))
        self.assertEqual(pick(s, "SL-21", "SFL")[0], "m2")

    def test_rule1_folders_on_both_biggest_wins(self):
        s = both(m6=st("m6", job=dict(folders=[dict(drive="internal", path="/a", entries=1, mtime=9)])),
                 m2=st("m2", job=dict(folders=[dict(drive="Extreme", path="/b", entries=60, mtime=1)])))
        self.assertEqual(pick(s, "SL-21", "SFL")[0], "m2", "a mirrored review folder on the M6 does not win")

    def test_rule2_named_mac(self):
        self.assertEqual(pick(both(), kind="SFC", named="m2")[0], "m2")
        self.assertEqual(pick(both(), kind="LFC", named="m6")[0], "m6")
        self.assertRaises(ValueError, pick, both(), "DS-1", "SFC", 1, False, "m9")

    def test_rule3_short_interactive_work_to_the_m6(self):
        for kind, rnd in (("SFC", 1), ("SFL", 1), ("ADCUT", 1), ("LFC", 2), ("AD", 3), ("VSL", 2)):
            h, why = pick(both(), kind=kind, rnd=rnd)
            self.assertEqual(h, "m6", (kind, rnd))
            self.assertIn("rule 3", why[0])

    def test_rule4_long_unattended_work_to_the_m2(self):
        for kind, rnd, chroma in (("LFC", 1, False), ("EXDEMO", 1, False), ("SFC", 1, True), ("LFC", 3, True)):
            h, why = pick(both(), kind=kind, rnd=rnd, chroma=chroma)
            self.assertEqual(h, "m2", (kind, rnd, chroma))
            self.assertIn("rule 4", why[0])

    def test_rule5_preferred_full_goes_to_the_other(self):
        s = both(m6=st("m6", in_use=["A", "B"]))
        h, why = pick(s, kind="SFC")
        self.assertEqual((h, "rule 5" in why[0]), ("m2", True))
        s = both(m2=st("m2", in_use=["A", "B", "C"]))
        self.assertEqual(pick(s, kind="LFC")[0], "m6")

    def test_rule5_m6_under_dans_load_counts_as_full(self):
        busy = both(m6=st("m6", load5=13.5, ncpu=12))
        h, why = pick(busy, kind="SFC")
        self.assertEqual(h, "m2")
        self.assertIn("under system load", why[0])
        pressure = both(m6=st("m6", pressure=2))
        self.assertEqual(pick(pressure, kind="SFC")[0], "m2")
        self.assertEqual(pick(both(m2=st("m2", load5=40, ncpu=10)), kind="LFC")[0], "m2", "no load guard on the M2")

    def test_rule6_order_from_idle_is_m6_m2_m2_m6_m2_then_wait(self):
        m6, m2, got = [], [], []
        for i in range(6):
            h, _ = pick(both(st("m6", in_use=m6), st("m2", in_use=m2)), job="J-{}".format(i), kind="OTHER")
            got.append(h)
            {"m6": m6, "m2": m2}.get(h, []).append("J-{}".format(i))
        self.assertEqual(got, ["m6", "m2", "m2", "m6", "m2", "wait"])

    def test_rule6_fourth_edit_skips_a_loaded_m6(self):
        h, _ = pick(both(st("m6", in_use=["A"], load5=20), st("m2", in_use=["B", "C"])), kind="OTHER")
        self.assertEqual(h, "m2")

    def test_rule7_both_full_waits(self):
        h, why = pick(both(st("m6", in_use=["A", "B"]), st("m2", in_use=["C", "D", "E"])), kind="SFC")
        self.assertEqual(h, "wait")
        self.assertIn("rule 7", why[-1])

    def test_waiters_on_a_mac_count_as_used(self):
        s = both(st("m6", in_use=["A"], waiting=["B"]))
        self.assertEqual(pick(s, kind="SFC")[0], "m2")

    def test_routed_but_not_started_reserves_a_slot(self):
        self.assertEqual(pick(both(), kind="SFC", reserved={"m6": ["DS-1", "DS-2"]})[0], "m2")
        s = both(st("m6", in_use=["DS-1"]))                    # DS-1 started: counted once, not twice
        self.assertEqual(pick(s, kind="SFC", reserved={"m6": ["DS-1"]})[0], "m6")

    def test_unreachable_m2_counts_as_full_and_is_reported(self):
        s = both(m2=st("m2", reachable=False))
        h, why = pick(s, kind="LFC")
        self.assertEqual(h, "m6")
        self.assertIn("unreachable", " ".join(why))
        h, why = pick(both(st("m6", in_use=["A", "B"]), st("m2", reachable=False)), kind="LFC")
        self.assertEqual(h, "wait")

    def test_route_class(self):
        self.assertEqual(er.route_class("LFC", 1), "LFC")
        self.assertEqual(er.route_class("LFC", 2), "REV")
        self.assertEqual(er.route_class("SFC", 2, chroma=True), "CHROMA")

    def test_kind_from_job_code(self):
        for job, kind in (("DS-107", "SFC"), ("SL-38", "SFL"), ("RO-40", "LFC"), ("RA-28", "AD"), ("AV-02", "ADCUT"),
                          ("WV-04", "VSL"), ("EXDEMO-3MORE", "EXDEMO"), ("REALDEMOS-B02", "EXDEMO")):
            self.assertEqual(er.infer_kind(job), kind, job)


class RealRemote(unittest.TestCase):
    """The ssh path with a Mac that does not exist: reported unreachable within the connect timeout."""

    def test_unreachable_host_is_fast_and_reported(self):
        c = json.loads(json.dumps(CFG))
        c["hosts"]["m2"]["ssh"] = "editroute-test-no-such-host.invalid"
        t0 = time.time()
        s = er.remote_status("m2", None, c)
        self.assertFalse(s["reachable"])
        self.assertTrue(s["error"])
        self.assertLess(time.time() - t0, 9)


class CombinedLine(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="editroute-test-")
        os.environ["EDITROUTE_DIR"] = self.d
        self.saved = er.gather
        self.saved_claim = er.claim_storage
        er.claim_storage = lambda *a,**k:None

    def tearDown(self):
        er.gather = self.saved
        er.claim_storage = self.saved_claim
        os.environ.pop("EDITROUTE_DIR", None)

    def _full(self, job=None, c=None):
        return both(st("m6", in_use=["A", "B"]), st("m2", in_use=["C", "D", "E"]))

    def test_pick_when_full_joins_the_line_then_oldest_first(self):
        er.gather = self._full
        self.assertEqual(er.cmd_pick("DS-301", "SFC"), er.EXIT_WAIT)
        time.sleep(0.01)
        self.assertEqual(er.cmd_pick("DS-302", "SFC"), er.EXIT_WAIT)
        line = json.loads((Path(self.d) / "waiting.json").read_text())
        self.assertEqual(sorted(line), ["DS-301", "DS-302"])
        # one slot frees on the M2: the older waiter gets it, the newer keeps waiting
        er.gather = lambda job=None, c=None: both(st("m6", in_use=["A", "B"]), st("m2", in_use=["C", "D"]))
        line["DS-301"]["seen"] = line["DS-302"]["seen"] = time.time()
        (Path(self.d) / "waiting.json").write_text(json.dumps(line))
        self.assertEqual(er.cmd_wait("DS-302", max_hours=0.0, poll=0.01), er.EXIT_TIMEOUT)
        self.assertEqual(er.cmd_wait("DS-301", max_hours=0.0, poll=0.01), er.EXIT_GO)
        line = json.loads((Path(self.d) / "waiting.json").read_text())
        self.assertEqual(sorted(line), ["DS-302"])
        last = [json.loads(x) for x in (Path(self.d) / "decisions.jsonl").read_text().splitlines()][-1]
        self.assertEqual((last["job"], last["host"]), ("DS-301", "m2"))

    def test_stale_older_waiter_does_not_block(self):
        er.gather = self._full
        er.cmd_pick("DS-311", "SFC")
        er.cmd_pick("DS-312", "SFC")
        p = Path(self.d) / "waiting.json"
        line = json.loads(p.read_text())
        line["DS-311"]["seen"] = time.time() - 3600              # its wait loop died an hour ago
        p.write_text(json.dumps(line))
        er.gather = lambda job=None, c=None: both(st("m6", in_use=["A"]), st("m2", in_use=["C", "D", "E"]))
        self.assertEqual(er.cmd_wait("DS-312", max_hours=0.0, poll=0.01), er.EXIT_GO)

    def test_repeat_pick_sticks_to_the_first_decision(self):
        er.gather = lambda job=None, c=None: both()
        er.cmd_pick("DS-321", "SFC")
        er.gather = lambda job=None, c=None: both(st("m6", in_use=["A", "B"]))
        er.cmd_pick("DS-321", "SFC")
        hosts = [json.loads(x)["host"] for x in (Path(self.d) / "decisions.jsonl").read_text().splitlines()]
        self.assertEqual(hosts, ["m6", "m6"])

    def test_dry_run_records_nothing_that_counts(self):
        er.gather = lambda job=None, c=None: both()
        er.cmd_pick("DS-331", "SFC", dry=True)
        self.assertFalse((Path(self.d) / "decisions.jsonl").exists())


class StatusTable(unittest.TestCase):
    def test_table_shows_both_macs_and_an_unreachable_one(self):
        txt = er.status_text(both(st("m6", in_use=["WV-03"]), st("m2", reachable=False)), CFG, {}, [], {})
        self.assertIn("M6 (Dan's Mac)", txt)
        self.assertIn("M2 Pro (edit machine)", txt)
        self.assertIn("WV-03", txt)
        self.assertIn("NO:", txt)
        self.assertIn("Next a dedicated Short would go to: m6", txt)


class OvernightQueue(unittest.TestCase):
    """Unattended launches by scripts/edit-queue/dispatcher.py (`pick --queue`) are their own class: M2 first."""

    def q(self, statuses, job="AV-200", kind="ADCUT", **kw):
        return er.decide(job, kind, 1, False, None, False, statuses, CFG, kw.get("reserved"), True)

    def test_queue_launch_goes_to_the_m2_even_for_a_kind_the_m6_takes_first(self):
        self.assertEqual(pick(both(), job="AV-200", kind="ADCUT")[0], "m6")
        host, why = self.q(both())
        self.assertEqual(host, "m2")
        self.assertIn("unattended overnight-queue edit", why[0])

    def test_queue_launch_spills_to_the_m6_only_when_the_m2_is_full(self):
        host, why = self.q(both(m2=st("m2", in_use=["A-1", "A-2", "A-3"])))
        self.assertEqual(host, "m6")
        self.assertIn("rule 5", why[0])

    def test_queue_launch_never_moves_a_job_with_work_on_the_m6(self):
        m6 = st("m6", job=dict(folders=[dict(drive="internal", path="/x/AV-200", entries=4, mtime=1)], editcap=None))
        self.assertEqual(self.q(both(m6=m6))[0], "m6")

    def test_queue_launch_waits_when_both_are_full(self):
        full = both(st("m6", in_use=["A", "B"]), st("m2", in_use=["C", "D", "E"]))
        self.assertEqual(self.q(full)[0], "wait")

    def test_queue_pick_never_joins_the_waiting_line(self):
        d = tempfile.mkdtemp(prefix="editroute-queue-")
        os.environ["EDITROUTE_DIR"] = d
        old = er.gather
        er.gather = lambda job=None, c=None: both(st("m6", in_use=["A", "B"]), st("m2", in_use=["C", "D", "E"]))
        try:
            self.assertEqual(er.cmd_pick("AV-201", "ADCUT", queue=True, as_json=True), er.EXIT_WAIT)
            self.assertEqual(json.loads((Path(d) / "waiting.json").read_text()), {})
        finally:
            er.gather = old
            os.environ.pop("EDITROUTE_DIR", None)


class SleepingDrive(unittest.TestCase):
    """2026-11-14: the M2's status call waited for the sleeping Seagate, ran past the M6's 8 s limit and the M2 was
    counted as full. A drive now gets a short deadline; past it the answer comes from the last saved folder list."""

    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="editroute-drive-")
        self.drive = Path(tempfile.mkdtemp(prefix="editroute-fake-drive-"))
        (self.drive / "_edit_work" / "DS-300").mkdir(parents=True)
        (self.drive / "_edit_work" / "DS-300" / "cut.mp4").write_text("x")
        os.environ["EDITROUTE_DIR"] = self.d
        self._cands, self._one = er._external_candidates, er._probe_one
        er._external_candidates = lambda: [("Expansion", self.drive)]

    def tearDown(self):
        er._external_candidates, er._probe_one = self._cands, self._one
        os.environ.pop("EDITROUTE_DIR", None)

    def _awake(self, name, root, job, network=False):
        names = {}
        found = er._job_dirs(name, root, ("_edit_work",), job, names) if job else []
        return dict(free_gb=1234, names=names if job else None, job_folders=found)

    def _asleep(self, name, root, job, network=False):
        time.sleep(5)
        return self._awake(name, root, job)

    def test_awake_drive_is_read_and_remembered(self):
        er._probe_one = self._awake
        drives, folders, slow = er.probe_drives("DS-300", deadline=1.0)
        self.assertEqual(slow, [])
        self.assertEqual([f["entries"] for f in folders if f["drive"] == "Expansion"], [1])
        cache = json.loads((Path(self.d) / "drives-cache.json").read_text())
        self.assertIn("DS-300", cache["Expansion"]["names"]["_edit_work"])

    def test_sleeping_drive_answers_from_the_saved_list_without_waiting(self):
        er._probe_one = self._awake
        er.probe_drives("DS-300", deadline=1.0)
        er._probe_one = self._asleep
        t0 = time.time()
        drives, folders, slow = er.probe_drives("DS-300", deadline=0.3)
        self.assertLess(time.time() - t0, 1.5)
        self.assertEqual(slow, ["Expansion"])
        ex = [x for x in drives if x["drive"] == "Expansion"][0]
        self.assertTrue(ex["asleep"])
        self.assertEqual(ex["free_gb"], 1234)
        hit = [f for f in folders if f["drive"] == "Expansion"]
        self.assertEqual(len(hit), 1)
        self.assertTrue(hit[0]["cached"])
        # rule 1 still holds the job on its Mac, and says the drive was asleep
        m2 = st("m2", job=dict(folders=hit, editcap=None))
        host, why = pick(both(m2=m2), job="DS-300", kind="SFC")
        self.assertEqual(host, "m2")
        self.assertIn("drive asleep", why[0])

    def test_sleeping_drive_with_no_saved_list_still_answers(self):
        er._probe_one = self._asleep
        t0 = time.time()
        drives, folders, slow = er.probe_drives("DS-300", deadline=0.3)
        self.assertLess(time.time() - t0, 1.5)
        self.assertEqual(slow, ["Expansion"])
        self.assertEqual([f for f in folders if f["drive"] == "Expansion"], [])

    def test_a_status_call_without_a_job_keeps_the_saved_names(self):
        er._probe_one = self._awake
        er.probe_drives("DS-300", deadline=1.0)
        er.probe_drives(None, deadline=1.0)
        cache = json.loads((Path(self.d) / "drives-cache.json").read_text())
        self.assertIn("DS-300", cache["Expansion"]["names"]["_edit_work"])

    def test_a_network_share_is_the_other_macs_drive(self):
        """The M2's drives are shared to the M6 over the cable: the M6 must not report the M2's job folders."""
        seen = {}

        def one(name, root, job, network=False):
            seen["network"] = network
            return self._one(name, root, job, network)
        er._probe_one = one
        types, er._mount_types = er._mount_types, lambda: {str(self.drive): "smbfs"}
        os.environ["GATE_DRIVE_MAP"] = ""
        real_ismount, os.path.ismount = os.path.ismount, lambda p: True
        try:
            drives, folders, slow = er.probe_drives("DS-300", deadline=1.0)
        finally:
            er._mount_types, os.path.ismount = types, real_ismount
            os.environ.pop("GATE_DRIVE_MAP", None)
        self.assertTrue(seen["network"])
        self.assertEqual(folders, [])
        self.assertTrue([d for d in drives if d["drive"] == "Expansion"][0]["network"])

    def test_a_slow_status_answer_records_where_the_time_went(self):
        er._probe_one = self._awake
        old = er.SLOW_STATUS_S
        er.SLOW_STATUS_S = -1.0
        os.environ["EDITROUTE_HOST"] = "m2"
        try:
            s = er.local_status("DS-300")
        finally:
            er.SLOW_STATUS_S = old
            os.environ.pop("EDITROUTE_HOST", None)
        self.assertEqual(sorted(s["took"]), ["drives", "editcap", "git", "idle", "renderq"])
        row = json.loads((Path(self.d) / "slow-status.jsonl").read_text().splitlines()[-1])
        self.assertEqual(row["job"], "DS-300")
        self.assertIn("drives", row["took"])

    def test_table_marks_a_sleeping_drive(self):
        m2 = st("m2")
        m2["drives"] = [dict(drive="internal", free_gb=59), dict(drive="Expansion", free_gb=16000, asleep=True)]
        self.assertIn("Expansion 16.0 TB (asleep)", er.status_text(both(m2=m2), CFG, {}, [], {}))


class RemoteRetry(unittest.TestCase):
    """A dropped connection is asked once more; a Mac that is slow to answer is not."""

    def setUp(self):
        self._run = er.subprocess.run
        self.calls = 0

    def tearDown(self):
        er.subprocess.run = self._run

    def test_fast_failure_is_retried_once(self):
        def fake(*a, **k):
            self.calls += 1
            if self.calls == 1:
                return subprocess.CompletedProcess(a, 255, "", "kex_exchange_identification: Connection closed")
            return subprocess.CompletedProcess(a, 0, json.dumps(dict(host="m2")), "")
        er.subprocess.run = fake
        s = er.remote_status("m2", None, CFG)
        self.assertTrue(s["reachable"])
        self.assertEqual((self.calls, s["attempts"]), (2, 2))

    def test_timeout_is_not_retried_and_reads_plainly(self):
        def fake(*a, **k):
            self.calls += 1
            raise subprocess.TimeoutExpired(a, k.get("timeout"))
        er.subprocess.run = fake
        s = er.remote_status("m2", None, CFG)
        self.assertFalse(s["reachable"])
        self.assertEqual(self.calls, 1)
        self.assertEqual(s["error"], "no answer within 8 s")

    def test_two_failures_are_reported(self):
        def fake(*a, **k):
            self.calls += 1
            return subprocess.CompletedProcess(a, 255, "", "ssh: connect to host m2: Connection refused")
        er.subprocess.run = fake
        s = er.remote_status("m2", None, CFG)
        self.assertFalse(s["reachable"])
        self.assertEqual(self.calls, 2)
        self.assertIn("Connection refused", s["error"])




class PushThroughSharedDrive(unittest.TestCase):
    """A delivery folder that is a link to a drive both Macs see is proved, never copied onto itself."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name).resolve()
        self.repo, self.drive, self.other = root / "repo", root / "drive", root / "other-mac-repo"
        for d in (self.repo, self.drive / "Videos to Review", self.other):
            d.mkdir(parents=True)
        (self.repo / "Videos to Review").symlink_to(self.drive / "Videos to Review")
        (self.other / "Videos to Review").symlink_to(self.drive / "Videos to Review")
        self.final = self.drive / "Videos to Review" / "final.mp4"
        self.final.write_bytes(b"film" * 1000)
        cfg = json.loads(json.dumps(CFG))
        cfg["hosts"]["m6"]["repo"] = str(self.other)
        self.saved = (er.REPO, er.cfg, er.me, er._ssh, er._rsync)
        self.copied = []
        er.REPO, er.cfg, er.me = self.repo, (lambda: cfg), (lambda: "m2")
        er._rsync = lambda *a, **k: self.copied.append(a)
        er._ssh = lambda h, command, timeout=60: subprocess.run(command, shell=True, capture_output=True, text=True)

    def tearDown(self):
        er.REPO, er.cfg, er.me, er._ssh, er._rsync = self.saved
        self.tmp.cleanup()

    def run_push(self, path):
        import contextlib
        import io
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = er.cmd_push([str(path)])
        return rc, out.getvalue()

    def test_linked_file_is_proved_not_copied(self):
        rc, out = self.run_push(self.repo / "Videos to Review" / "final.mp4")
        self.assertEqual(rc, er.EXIT_GO)
        self.assertIn("already on the m6 through the shared drive (same checksum", out)
        self.assertEqual(self.copied, [])

    def test_linked_folder_is_proved_by_names_and_sizes(self):
        rc, out = self.run_push(self.repo / "Videos to Review")
        self.assertEqual(rc, er.EXIT_GO)
        self.assertIn("1 files, same names and sizes", out)
        self.assertEqual(self.copied, [])

    def test_drive_not_mounted_on_the_other_mac_fails_loudly(self):
        (self.other / "Videos to Review").unlink()
        rc, out = self.run_push(self.repo / "Videos to Review" / "final.mp4")
        self.assertEqual(rc, er.EXIT_ERR)
        self.assertIn("NOT confirmed on the m6", out)
        self.assertEqual(self.copied, [])

    def test_a_different_file_there_fails(self):
        (self.other / "Videos to Review").unlink()
        (self.other / "Videos to Review").mkdir()
        (self.other / "Videos to Review" / "final.mp4").write_bytes(b"old!" * 1000)
        rc, out = self.run_push(self.repo / "Videos to Review" / "final.mp4")
        self.assertEqual(rc, er.EXIT_ERR)
        self.assertIn("checksums differ", out)

    def test_ordinary_project_file_is_still_copied(self):
        (self.repo / "Docs").mkdir()
        (self.repo / "Docs" / "note.md").write_text("x")
        rc, out = self.run_push(self.repo / "Docs" / "note.md")
        self.assertEqual(rc, er.EXIT_GO)
        self.assertEqual(len(self.copied), 1)
        self.assertIn("Docs/note.md -> m6:", out)


if __name__ == "__main__":
    unittest.main()
