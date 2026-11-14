"""Ownership and original-chat command execution, without real edit production."""
import contextlib
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import resume as rs


def config():
    return {"hosts": {h: {"repo": "/project with spaces", "ssh": h} for h in ("m6", "m2")}}


def statuses(owner="m2"):
    return {h: dict(reachable=True, job=dict(folders=[dict(path="/work/DS-39", entries=7, mtime=1)]
                                           if h == owner else [], editcap="with-dan" if h == owner else None))
            for h in ("m6", "m2")}


class Resume(unittest.TestCase):
    def test_ownership_probe_cannot_consume_command_stdin(self):
        response = subprocess.CompletedProcess([], 0, stdout=json.dumps(statuses()), stderr="")
        with patch.object(rs.subprocess, "run", return_value=response) as probe:
            self.assertEqual(rs.gather_without_stdin("DS-39", config()), statuses())
            self.assertEqual(probe.call_args.kwargs["stdin"], subprocess.DEVNULL)

    def test_existing_edit_ignores_new_short_preference(self):
        result = rs.locate("DS-39", statuses(), config(), "m6")
        self.assertEqual((result["host"], result["state"]), ("m2", "existing"))

    def test_unreachable_mac_never_creates_local_copy(self):
        states = statuses("m6")
        states["m2"] = dict(reachable=False)
        result = rs.locate("DS-39", states, config(), "m6")
        self.assertEqual(result["state"], "unresolved")
        self.assertIsNone(result["host"])

    def test_new_edit_still_uses_normal_routing(self):
        result = rs.locate("DS-39", statuses(None), config(), "m6")
        self.assertEqual(result["state"], "new")

    def test_remote_command_keeps_arguments_literal_and_streams_input(self):
        with tempfile.TemporaryDirectory(prefix="resume path ") as cwd:
            info = dict(job="DS-39", host="m2", here="m6")
            special = "literal $(touch DO_NOT_CREATE); 'quoted'\nmore"
            command = [sys.executable, "-c", "import json,os,sys; print(json.dumps([sys.argv[1],sys.stdin.read(),os.getcwd(),os.environ['GATE_GROUP']]))", special]
            argv = rs.command_for(info, command, config(), cwd)
            self.assertEqual(argv[0], "ssh")
            # Execute exactly the remote worker argv locally; no SSH or video output.
            worker = shlex.split(argv[-1])
            r = subprocess.run(worker, input="streamed stdin", text=True, capture_output=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            value, stdin, actual_cwd, group = json.loads(r.stdout)
            self.assertEqual((value, stdin, group), (special, "streamed stdin", "DS-39"))
            self.assertEqual(Path(actual_cwd).resolve(), Path(cwd).resolve())
            self.assertFalse((Path(cwd) / "DO_NOT_CREATE").exists())

    def test_local_command_returns_real_failure(self):
        with tempfile.TemporaryDirectory() as cwd:
            info = dict(job="DS-39", host="m6", here="m6")
            argv = rs.command_for(info, [sys.executable, "-c", "raise SystemExit(17)"], config(), cwd)
            self.assertEqual(subprocess.run(argv).returncode, 17)

    def test_no_execution_when_ownership_unresolved(self):
        with patch.object(rs, "locate", return_value=dict(state="unresolved", reason="offline")), \
                patch.object(rs.subprocess, "call") as call, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(rs.run("DS-39", ["hostname"]), 6)
            call.assert_not_called()

    def test_run_does_not_start_an_ai_or_retry_failure(self):
        info = dict(job="DS-39", host="m2", here="m6", state="existing")
        with patch.object(rs, "locate", return_value=info), patch.object(rs.er, "cfg", return_value=config()), \
                patch.object(rs.subprocess, "call", return_value=255) as call, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(rs.run("DS-39", ["hostname"]), 255)
            call.assert_called_once()
            self.assertEqual(call.call_args.args[0][0], "ssh")

    def test_editcap_blocks_wrong_mac_before_registry_mutation(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "editcap"))
        import editcap
        for command in ("acquire", "heartbeat", "wait"):
            with patch.object(rs, "check", return_value=5), patch.object(editcap, "acquire") as acquire, \
                    patch.object(editcap, "wait") as wait:
                self.assertEqual(editcap.main([command, "DS-39"]), 5)
                acquire.assert_not_called()
                wait.assert_not_called()


if __name__ == "__main__":
    unittest.main()
