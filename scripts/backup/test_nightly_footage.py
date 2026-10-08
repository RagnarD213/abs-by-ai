import os
import tempfile
import time
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from scripts.backup import nightly_footage as backup


class CopyOnlyDriveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.shoot = Path(self.temp.name) / "abs by ai test shoot"
        self.shoot.mkdir()
        self.raw = self.shoot / "camera.mp4"
        self.raw.write_bytes(b"raw footage fixture")
        old = time.time() - 3600
        os.utime(self.raw, (old, old))
        (self.shoot / backup.READY_MARKER).touch()
        self.config = {"drive": self.shoot.name, "raw": ["."]}
        self.deadline = datetime.now(backup.TZ) + timedelta(hours=1)

    def test_copy_verifies_and_never_removes_source(self):
        state = {"shoots": {}}
        with patch.object(backup, "eligible_shoots", return_value=[(self.shoot, self.config)]), \
             patch.object(backup, "rclone_transfer") as transfer, \
             patch.object(backup, "run_command") as command, \
             patch.object(backup, "save_state"):
            self.assertEqual(backup.copy_only_to_drive(state, self.deadline, False), 0)
            self.assertTrue(self.raw.exists())
            self.assertIn("drive_verified", state["shoots"][self.shoot.name])
            self.assertEqual(transfer.call_count, 1)
            self.assertEqual(command.call_count, 1)
            self.assertEqual(backup.copy_only_to_drive(state, self.deadline, False), 0)
            self.assertEqual(transfer.call_count, 1)

    def test_failed_verification_keeps_source_and_no_success_state(self):
        state = {"shoots": {}}
        with patch.object(backup, "eligible_shoots", return_value=[(self.shoot, self.config)]), \
             patch.object(backup, "rclone_transfer", side_effect=RuntimeError("checksum mismatch")), \
             patch.object(backup, "save_state"):
            self.assertEqual(backup.copy_only_to_drive(state, self.deadline, False), 1)
        self.assertTrue(self.raw.exists())
        self.assertNotIn("drive_verified", state["shoots"][self.shoot.name])


if __name__ == "__main__":
    unittest.main()
