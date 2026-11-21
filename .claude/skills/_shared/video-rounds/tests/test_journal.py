import hashlib
import importlib.util
import json
import multiprocessing
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('journal', Path(__file__).parents[1] / 'journal.py')
journal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journal)


def contender(path, queue):
    try:
        journal.cas(path, None, {'revision': 0, 'key': 'job:R3', 'plan': {'round': 3}})
        queue.put('won')
    except ValueError:
        queue.put('lost')


class JournalTests(unittest.TestCase):
    def test_concurrent_reservation_has_one_winner(self):
        with tempfile.TemporaryDirectory() as tmp:
            ctx = multiprocessing.get_context('fork')
            queue = ctx.Queue()
            path = str(Path(tmp) / 'round-controller.json')
            workers = [ctx.Process(target=contender, args=(path, queue)) for _ in range(4)]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(5)
                self.assertEqual(worker.exitcode, 0)
            self.assertEqual(sorted(queue.get(timeout=1) for _ in workers), ['lost', 'lost', 'lost', 'won'])
            self.assertEqual(json.loads(Path(path).read_text())['revision'], 0)

    def test_approved_bytes_are_verified_never_rewritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'decisions.json'
            path.write_bytes(b'{"locked":"Dan exact words"}\n')
            files = [{'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]
            original = path.read_bytes()
            journal.verify(files, str(path))
            self.assertEqual(path.read_bytes(), original)
            path.write_bytes(original + b' ')
            with self.assertRaisesRegex(ValueError, 'hash changed'):
                journal.verify(files, str(path))

    def test_cannot_overwrite_arbitrary_state_or_reserved_packet(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                journal.cas(Path(tmp) / 'jobs.json', None, {})
            path = Path(tmp) / 'round-controller.json'
            journal.cas(path, None, {'revision': 0, 'key': 'job:R3', 'plan': {}})
            with self.assertRaises(ValueError):
                journal.cas(path, 0, {'revision': 1, 'key': 'job:R4', 'plan': {}})


if __name__ == '__main__':
    unittest.main()
