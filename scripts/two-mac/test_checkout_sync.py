#!/usr/bin/env python3
"""Sandbox tests for checkout-sync.py and reconcile-checkout.py. Touches only a temp folder.

    python3 scripts/two-mac/test_checkout_sync.py
"""
import os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SYNC = os.path.join(HERE, "checkout-sync.py")


def sh(cwd, *a, ok=True):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    if ok and r.returncode != 0:
        raise AssertionError("{} failed: {}{}".format(a, r.stdout, r.stderr))
    return r


class Sandbox(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="checkout-sync-test-")
        self.origin, self.live, self.other = (os.path.join(self.d, n) for n in ("origin.git", "live", "other"))
        sh(self.d, "git", "init", "-q", "--bare", "-b", "main", self.origin)
        sh(self.d, "git", "clone", "-q", self.origin, self.live)
        for repo in (self.live,):
            sh(repo, "git", "config", "user.email", "test@example.com"); sh(repo, "git", "config", "user.name", "Test")
        self.write(self.live, "a.txt", "one\ntwo\nthree\n"); self.write(self.live, "b.txt", "".join("line %d\n" % i for i in range(1, 21)))
        self.write(self.live, "old.txt", "to be deleted upstream\n"); self.write(self.live, "old-edited.txt", "to be deleted upstream\n")
        self.write(self.live, "staged-gone.txt", "a session stages its removal\n")
        sh(self.live, "git", "add", "."); sh(self.live, "git", "commit", "-q", "-m", "base"); sh(self.live, "git", "push", "-q", "origin", "main")
        sh(self.d, "git", "clone", "-q", self.origin, self.other)
        sh(self.other, "git", "config", "user.email", "o@example.com"); sh(self.other, "git", "config", "user.name", "Other")
        self.state = os.path.join(self.d, "state")

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def write(self, repo, name, text):
        with open(os.path.join(repo, name), "w") as f:
            f.write(text)

    def read(self, repo, name):
        with open(os.path.join(repo, name)) as f:
            return f.read()

    def upstream(self, msg="upstream"):
        sh(self.other, "git", "add", "-A"); sh(self.other, "git", "commit", "-q", "-m", msg); sh(self.other, "git", "push", "-q", "origin", "main")

    def sync(self, *extra):
        env = dict(os.environ, CHECKOUT_SYNC_REPO=self.live, CHECKOUT_SYNC_STATE=self.state, CHECKOUT_SYNC_HOST="testmac")
        return subprocess.run([sys.executable, SYNC] + list(extra), capture_output=True, text=True, env=env)

    def vs_origin(self):
        return sh(self.live, "git", "rev-list", "--left-right", "--count", "HEAD...origin/main").stdout.split()

    def test_pushes_past_uncommitted_edits_then_levels(self):
        self.write(self.other, "b.txt", self.read(self.other, "b.txt").replace("line 2\n", "line 2 from GitHub\n")); self.upstream()
        self.write(self.live, "a.txt", "one\ntwo\nthree\nfour from this Mac\n"); sh(self.live, "git", "commit", "-q", "-am", "local commit")
        self.write(self.live, "b.txt", self.read(self.live, "b.txt").replace("line 19\n", "line 19 unsaved edit\n"))   # blocks a plain merge
        self.write(self.live, "notes-untracked.txt", "mine\n")
        r = self.sync()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.vs_origin(), ["0", "0"])
        self.assertIn("four from this Mac", sh(self.other, "git", "fetch", "-q") and sh(self.other, "git", "show", "origin/main:a.txt").stdout)
        b = self.read(self.live, "b.txt")
        self.assertIn("line 2 from GitHub", b); self.assertIn("line 19 unsaved edit", b)
        self.assertEqual(sh(self.live, "git", "status", "--porcelain").stdout.split("\n")[:2], [" M b.txt", "?? notes-untracked.txt"])
        self.assertTrue(self.read(self.state, "status.txt").startswith("OK "))

    def test_committed_conflict_stops_and_changes_nothing(self):
        self.write(self.other, "a.txt", "ONE (GitHub)\ntwo\nthree\n"); self.upstream()
        self.write(self.live, "a.txt", "ONE (this Mac)\ntwo\nthree\n"); sh(self.live, "git", "commit", "-q", "-am", "local")
        head = sh(self.live, "git", "rev-parse", "HEAD").stdout
        before = sh(self.other, "git", "rev-parse", "HEAD").stdout
        r = self.sync()
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("a.txt", r.stdout)
        self.assertEqual(sh(self.live, "git", "rev-parse", "HEAD").stdout, head)
        self.assertEqual(sh(self.origin, "git", "rev-parse", "main").stdout, before)
        self.assertTrue(self.read(self.state, "status.txt").startswith("STOPPED "))

    def test_upstream_delete_and_staged_removal(self):
        sh(self.other, "git", "rm", "-q", "old.txt", "old-edited.txt"); self.upstream()
        self.write(self.live, "old-edited.txt", "to be deleted upstream\nbut a session here added this\n")
        sh(self.live, "git", "rm", "-q", "staged-gone.txt")                                   # another session's staged work
        r = self.sync()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.vs_origin(), ["0", "0"])
        self.assertFalse(os.path.exists(os.path.join(self.live, "old.txt")))
        self.assertIn("a session here added this", self.read(self.live, "old-edited.txt"))
        st = sh(self.live, "git", "status", "--porcelain").stdout
        self.assertIn("D  staged-gone.txt", st); self.assertIn("?? old-edited.txt", st)
        backups = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(self.live, "tmp")) for f in fs]
        self.assertTrue(any(p.endswith("/old.txt") for p in backups))

    def test_unsaved_edit_on_the_same_lines_stops_levelling_but_commits_still_reach_github(self):
        self.write(self.other, "a.txt", "one\nTWO (GitHub)\nthree\n"); self.upstream()
        self.write(self.live, "b.txt", self.read(self.live, "b.txt") + "local commit line\n"); sh(self.live, "git", "commit", "-q", "-am", "local")
        self.write(self.live, "a.txt", "one\nTWO (unsaved, this Mac)\nthree\n")
        r = self.sync()
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        sh(self.other, "git", "fetch", "-q")
        self.assertIn("local commit line", sh(self.other, "git", "show", "origin/main:b.txt").stdout)   # pushed anyway
        self.assertEqual(self.read(self.live, "a.txt"), "one\nTWO (unsaved, this Mac)\nthree\n")         # untouched
        self.assertEqual(self.vs_origin()[0], "0")

    def test_union_files_keep_both_sides_entries(self):
        self.write(self.other, ".gitattributes", "board.md merge=union\n"); self.write(self.other, "board.md", "# ACTIVE\n\nold entry\n"); self.upstream("board")
        sh(self.live, "git", "pull", "-q", "--ff-only")
        self.write(self.other, "board.md", "# ACTIVE\n\nentry from the other Mac\n\nold entry\n"); self.upstream()
        self.write(self.live, "board.md", "# ACTIVE\n\ncommitted entry from this Mac\n\nold entry\n"); sh(self.live, "git", "commit", "-q", "-am", "local board entry")
        r = self.sync()                                                                      # committed on both sides: push path
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        board = self.read(self.live, "board.md")
        self.assertIn("entry from the other Mac", board); self.assertIn("committed entry from this Mac", board)
        sh(self.other, "git", "pull", "-q", "--ff-only")
        self.write(self.other, "board.md", self.read(self.other, "board.md").replace("# ACTIVE\n", "# ACTIVE\n\nsecond entry from the other Mac\n")); self.upstream()
        self.write(self.live, "board.md", board.replace("# ACTIVE\n", "# ACTIVE\n\nUNSAVED entry from this Mac\n"))
        r = self.sync()                                                                      # unsaved here, committed there: levelling path
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        board = self.read(self.live, "board.md")
        self.assertIn("second entry from the other Mac", board); self.assertIn("UNSAVED entry from this Mac", board)
        self.assertEqual(self.vs_origin(), ["0", "0"])
        self.assertIn(" M board.md", sh(self.live, "git", "status", "--porcelain").stdout)

    def jobs(self, **changes):
        import json
        base = {"schema": 1, "jobs": [{"id": "A-1", "state": "ready", "note": "", "rev": 1, "syncedRev": 1},
                                      {"id": "A-2", "state": "ready", "note": "", "rev": 1, "syncedRev": 1}]}
        for i, fields in changes.items():
            next(j for j in base["jobs"] if j["id"] == i.replace("_", "-")).update(fields)
        return json.dumps(base, indent=1, ensure_ascii=False) + "\n"

    def test_jobs_json_merges_job_by_job_and_newer_rev_wins(self):
        import json
        name = "Handoffs/video-editing/jobs.json"
        os.makedirs(os.path.join(self.other, "Handoffs/video-editing")); self.write(self.other, name, self.jobs()); self.upstream("jobs")
        sh(self.live, "git", "pull", "-q", "--ff-only")
        self.write(self.other, name, self.jobs(A_1={"state": "in_progress", "rev": 2}, A_2={"note": "from GitHub", "rev": 2})); self.upstream()
        self.write(self.live, name, self.jobs(A_1={"state": "finalized", "rev": 4, "syncedRev": 4})); sh(self.live, "git", "commit", "-q", "-am", "local job change")
        self.write(self.live, name, self.jobs(A_1={"state": "finalized", "rev": 5, "syncedRev": 4, "note": "unsaved note"}))
        r = self.sync()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.vs_origin(), ["0", "0"])
        sh(self.other, "git", "pull", "-q", "--ff-only")
        pushed = {j["id"]: j for j in json.loads(self.read(self.other, name))["jobs"]}
        self.assertEqual((pushed["A-1"]["state"], pushed["A-1"]["rev"], pushed["A-1"]["syncedRev"]), ("finalized", 4, 1))
        self.assertEqual(pushed["A-2"]["note"], "from GitHub")
        here = {j["id"]: j for j in json.loads(self.read(self.live, name))["jobs"]}
        self.assertEqual((here["A-1"]["note"], here["A-1"]["rev"], here["A-2"]["note"]), ("unsaved note", 5, "from GitHub"))

    def test_jobs_json_equal_rev_conflict_stops(self):
        name = "Handoffs/video-editing/jobs.json"
        os.makedirs(os.path.join(self.other, "Handoffs/video-editing")); self.write(self.other, name, self.jobs()); self.upstream("jobs")
        sh(self.live, "git", "pull", "-q", "--ff-only")
        self.write(self.other, name, self.jobs(A_1={"state": "in_progress", "rev": 2})); self.upstream()
        self.write(self.live, name, self.jobs(A_1={"state": "finalized", "rev": 2})); sh(self.live, "git", "commit", "-q", "-am", "local job change")
        r = self.sync()
        self.assertEqual(r.returncode, 3, r.stdout + r.stderr)
        self.assertIn("jobs.json", r.stdout)

    def test_stale_hand_copy_takes_githubs_current_version(self):
        self.write(self.other, "tool.py", "v1\n"); self.upstream("v1")
        self.write(self.live, "tool.py", "v1\n")                                            # hand copy, untracked here
        self.write(self.other, "tool.py", "v1\nv2\n"); self.upstream("v2")
        r = self.sync()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(self.read(self.live, "tool.py"), "v1\nv2\n")
        self.assertEqual(sh(self.live, "git", "status", "--porcelain", "tool.py").stdout, "")

    def test_dry_run_changes_nothing(self):
        self.write(self.other, "a.txt", "one\ntwo\nthree\nupstream\n"); self.upstream()
        self.write(self.live, "b.txt", self.read(self.live, "b.txt") + "x\n"); sh(self.live, "git", "commit", "-q", "-am", "local")
        head = sh(self.live, "git", "rev-parse", "HEAD").stdout
        r = self.sync("--dry")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(sh(self.live, "git", "rev-parse", "HEAD").stdout, head)
        self.assertNotEqual(sh(self.origin, "git", "rev-parse", "main").stdout, head)
        self.assertFalse(os.path.exists(os.path.join(self.state, "status.txt")))


if __name__ == "__main__":
    unittest.main(verbosity=1)
