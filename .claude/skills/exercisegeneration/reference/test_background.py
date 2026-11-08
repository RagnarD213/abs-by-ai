"""Behavior checks for the empty-background gate, using lossless silent fixtures."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import cv2
import numpy as np


class BackgroundGateTests(unittest.TestCase):
    def run_case(self, moving_stack=False, hide_everything=False, exposure_jump=False):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            masks = root / 'masks'
            masks.mkdir()
            base = np.full((96, 160, 3), 150, np.uint8)
            cv2.rectangle(base, (70, 28), (92, 70), (55, 55, 55), -1)
            cv2.imwrite(str(root / 'plate.png'), base)
            writer = cv2.VideoWriter(str(root / 'take.avi'), cv2.VideoWriter_fourcc(*'FFV1'), 24, (160, 96))
            self.assertTrue(writer.isOpened(), 'Lossless test encoder is unavailable')
            for i, x in enumerate([55, 25, 105, 10]):
                image = base.copy()
                # The first foreground position hides some of the stack. It must
                # not become a false reference for newly uncovered background.
                if moving_stack and i >= 2:
                    image[20:80, 65:100] = 150
                    cv2.rectangle(image, (70, 42), (92, 82), (55, 55, 55), -1)
                if exposure_jump and i >= 2:
                    image = image + 5
                cv2.rectangle(image, (x, 15), (x+25, 75), (0, 0, 230), -1)
                writer.write(image)
                mask = np.full((96, 160), 255 if hide_everything else 0, np.uint8)
                cv2.rectangle(mask, (x, 15), (x+25, 75), 255, -1)
                cv2.imwrite(str(masks / f'{i:04d}.png'), mask)
            writer.release()
            report = root / 'report.json'
            result = subprocess.run([
                sys.executable, str(Path(__file__).with_name('background.py')), str(root / 'take.avi'),
                '--plate', str(root / 'plate.png'), '--masks', str(masks), '--report', str(report)
            ], capture_output=True, text=True)
            self.assertTrue(report.exists(), result.stderr)
            return result.returncode, json.loads(report.read_text())

    def test_moving_foreground_and_newly_uncovered_still_stack_pass(self):
        code, report = self.run_case()
        self.assertEqual(code, 0)
        self.assertEqual(report['verdict'], 'PASS')
        self.assertEqual(report['frames_checked'], 4)

    def test_unoccupied_stack_moving_after_it_is_uncovered_fails(self):
        code, report = self.run_case(moving_stack=True)
        self.assertEqual(code, 1)
        self.assertEqual(report['verdict'], 'FAIL')
        self.assertGreater(len(report['failed_frames']), 0)

    def test_mask_cannot_hide_the_entire_background(self):
        code, report = self.run_case(hide_everything=True)
        self.assertEqual(code, 1)
        self.assertEqual(report['verdict'], 'FAIL')

    def test_background_brightness_pop_fails_without_object_movement(self):
        code, report = self.run_case(exposure_jump=True)
        self.assertEqual(code, 1)
        self.assertGreater(abs(report['worst_exposure']['background_exposure_shift']), 2.0)


if __name__ == '__main__':
    unittest.main()
