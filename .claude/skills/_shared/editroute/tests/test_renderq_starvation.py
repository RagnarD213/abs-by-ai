"""Render queue lane starvation (M2, 2026-11-18): 2-core frame checks waited 3 to 9 hours while heavy keys that
joined later got every freed 4-core opening. A light/quick step that has waited past the max wait (STARVE_S) now
takes the next freed cores before any heavy step that joined after it."""
import os
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SHARED = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(SHARED / 'editroute'), str(SHARED / 'renderq'), str(SHARED / 'editcap')]
import renderq as rq  # noqa: E402

MIN = 60.0


def heavy_holder(group='WV-03'):
    return dict(pool='heavy', held=True, info={'cores': 4, 'group': group, 'drives': ['Extreme']})


class Starvation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='renderq-starve-')
        d = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {
            'EDITROUTE_HOST': 'm2', 'EDIT_PRIORITY_DIR': str(d / 'priority'), 'EDITCAP_DIR': str(d / 'cap'),
            'GATE_DIR': str(d / 'rq'), 'GATE_FAIRNESS': '0', 'GATE_BORROWING': '0', 'GATE_BUDGET': '8',
            'GATE_UNMANAGED': '0', 'GATE_MEM': '20,0', 'GATE_HEADROOM_S': '0', 'GATE_SETTLE': '0',
            'GATE_NO_HOSTCFG': '1', 'GATE_POOLS': 'heavy=2:4,light=1:3,quick=2:2'})
        self.env.start()
        os.environ.pop('GATE_STARVE_S', None)
        self.rqd = patch.object(rq, 'DIR', d / 'rq')
        self.rqd.start()
        rq._ensure()
        now = time.time()
        # The observed shape: one key running (4 of 8 cores), a frame check waiting 3 h, a later key ready.
        self.light = dict(pool='light', group='work:WV-04', seq=1, created=now - 190 * MIN, label='frame check START.png',
                          max_wait=True)
        self.heavy = dict(pool='heavy', group='WV-03', seq=2, created=now - 21 * MIN, drives=['Extreme'],
                          label='WV-03 key Q105')
        self.states = [heavy_holder()]

    def tearDown(self):
        self.rqd.stop()
        self.env.stop()
        self.tmp.cleanup()

    def line(self, *tickets):
        return patch.object(rq, '_tickets', lambda pool=None: [t for t in tickets if pool in (None, t['pool'])])

    def test_reproduces_and_fixes_the_m2_starvation(self):
        """Old rule: the legacy heavy reservation blocked the light step whenever a heavy waited, and the heavy
        step had nothing to stop it. Now the 3-hour light step goes and the later heavy step waits."""
        with self.line(self.light, self.heavy):
            self.assertFalse(rq.budget_check('light', self.states))      # 4 used + 2 fits in 8
            self.assertFalse(rq.budget_check('heavy', self.states))      # 4 used + 4 fits in 8
            self.assertEqual(rq._lane_reason(self.light, self.states, ()), '')
            why = rq._lane_reason(self.heavy, self.states, ())
            self.assertIn('goes first', why)
            self.assertIn('frame check', why)
            self.assertTrue(rq._eligible(self.light, self.states, ()))
            self.assertFalse(rq._eligible(self.heavy, self.states, ()))

    def test_a_light_step_under_the_max_wait_keeps_the_old_heavy_reservation(self):
        fresh = dict(self.light, created=time.time() - 5 * MIN)
        with self.line(fresh, self.heavy):
            self.assertIn('legacy heavy reservation', rq._lane_reason(fresh, self.states, ()))
            self.assertEqual(rq._lane_reason(self.heavy, self.states, ()), '')

    def test_an_older_heavy_step_is_not_held_back(self):
        older = dict(self.heavy, created=self.light['created'] - MIN)
        with self.line(self.light, older):
            self.assertEqual(rq._starve_reason(older, self.states, ()), '')

    def test_priority_heavy_still_goes_first(self):
        with self.line(self.light, dict(self.heavy, priority=True)):
            self.assertEqual(rq._starve_reason(dict(self.heavy, priority=True), self.states, ()), '')

    def test_room_for_both_does_not_delay_heavy(self):
        with patch.dict(os.environ, {'GATE_BUDGET': '10'}), self.line(self.light, self.heavy):
            self.assertEqual(rq._starve_reason(self.heavy, self.states, ()), '')

    def test_full_small_lane_or_held_back_video_reserves_nothing(self):
        full = self.states + [dict(pool='light', held=True, info={'cores': 2}) for _ in range(3)]
        with self.line(self.light, self.heavy):
            self.assertEqual(rq._starve_reason(self.heavy, full, ()), '')
            with patch.object(rq.job_priority, 'blocked', lambda g, host=None: g == 'work:WV-04'):
                self.assertEqual(rq._starve_reason(self.heavy, self.states, ()), '')
            with patch.object(rq, '_parked', lambda g: g == 'work:WV-04'):
                self.assertEqual(rq._starve_reason(self.heavy, self.states, ()), '')

    def test_quick_lane_too(self):
        quick = dict(self.light, pool='quick', label='clip check clip.mp4')
        with self.line(quick, self.heavy):
            self.assertEqual(rq._lane_reason(quick, self.states, ()), '')
            self.assertIn('quick step', rq._starve_reason(self.heavy, self.states, ()))

    def test_starving_step_heads_its_own_lane(self):
        newer_priority = dict(self.light, seq=9, created=time.time(), priority=True, label='new')
        newer_quick = dict(newer_priority, pool='quick')
        old_quick = dict(self.light, pool='quick', seq=3)
        self.assertEqual(rq._rank([newer_priority, self.light], self.states, 'light')[0]['seq'], 1)
        self.assertEqual(rq._rank([newer_quick, old_quick], self.states, 'quick')[0]['seq'], 3)

    def test_with_fairness_and_borrowing_on(self):
        """v5 features active: the loan rules used to refuse the light step ('protecting a fitting heavy opening')."""
        with patch.dict(os.environ, {'GATE_FAIRNESS': '1', 'GATE_BORROWING': '1'}), self.line(self.light, self.heavy):
            fresh = dict(self.light, created=time.time() - MIN)
            self.assertIn('fitting heavy', rq._lane_reason(fresh, self.states, ()))
            self.assertEqual(rq._lane_reason(self.light, self.states, ()), '')
            eligible = [t for t in (self.light, self.heavy) if rq._eligible(t, self.states, ())]
            self.assertEqual([t['seq'] for t in rq._fair_order(eligible, self.states)], [1])

    def test_memory_gate_is_the_same_for_every_lane(self):
        """The 18:00 status said 'room for 0 s (memory pressure warning)': that closes heavy as well as light, so
        it delays everyone equally and is not what starved the light lane."""
        bad = {'ok': False, 'reason': 'memory: macOS reports memory pressure (warning)'}
        with patch.object(rq, 'mem_state', return_value=bad), self.line(self.light, self.heavy):
            for pool in ('heavy', 'light', 'quick'):
                self.assertIn('memory pressure', rq.budget_check(pool, self.states))

    def test_waiters_on_older_code_are_not_waited_for(self):
        """Rollout: a light waiter that loaded the old code still refuses cores while a heavy step waits, so a new
        heavy step must not leave cores idle for it. A new-code starving step ranks ahead of it in the lane."""
        old = dict(self.light, seq=0, created=self.light['created'] - 600 * MIN)
        old.pop('max_wait')
        with self.line(old, self.heavy):
            self.assertFalse(rq._starving(old))
            self.assertEqual(rq._starve_reason(self.heavy, self.states, ()), '')
        with self.line(old, self.light, self.heavy):
            self.assertEqual(rq._rank([old, self.light], self.states, 'light')[0]['seq'], 1)
            self.assertIn('goes first', rq._starve_reason(self.heavy, self.states, ()))

    def test_new_tickets_carry_the_marker(self):
        t = rq.Ticket('light', 'fixture', 'DS-701', False)
        try:
            self.assertTrue(rq._read(t.path).get('max_wait'))
        finally:
            t.close()

    def test_max_wait_is_tunable(self):
        with patch.dict(os.environ, {'GATE_STARVE_S': str(4 * 3600)}), self.line(self.light, self.heavy):
            self.assertFalse(rq._starving(self.light))
            self.assertEqual(rq._starve_reason(self.heavy, self.states, ()), '')


if __name__ == '__main__':
    unittest.main()
