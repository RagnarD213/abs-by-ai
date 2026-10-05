import argparse
import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from planning import extract_priorities, read_planning
from collect_inputs import (ad_guard, collect, dashboard, posthog, private_directory,
                            legacy_plan, merge_verified_leads, redact, run_ads, select_priority, select_trello, snapshot, subscriber_leads, windows)

NOW = datetime(2026, 9, 30, 15, tzinfo=timezone.utc)
AT = '2026-09-30T13:00:00Z'
CID = '12345678-1234-1234-1234-123456789abc'


class InputsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.meta = self.root / 'metadata'
        (self.meta / 'account' / 'org').mkdir(parents=True)
        self.transcripts = self.root / 'transcripts'
        self.transcripts.mkdir()
        self.file = self.transcripts / (CID + '.jsonl')
        self.metadata = self.meta / 'account/org/local_fixture.json'
        self.metadata.write_text(json.dumps({'sessionId': 'local_fixture', 'cliSessionId': CID,
            'cwd': str(self.project), 'originCwd': str(self.project), 'title': 'Daily priorities and plan',
            'lastActivityAt': int(NOW.timestamp() * 1000), 'isArchived': True}))

    def tearDown(self):
        self.tmp.cleanup()

    def row(self, uid, text, parent=None, **extra):
        return {'uuid': uid, 'parentUuid': parent, 'type': 'user', 'origin': {'kind': 'human'},
                'entrypoint': 'claude-desktop', 'cwd': str(self.project), 'timestamp': AT,
                'message': {'content': text}, **extra}

    def write_rows(self, *rows):
        self.file.write_text(''.join(json.dumps(row) + '\n' for row in rows))

    def read(self, state=None, now=NOW):
        return read_planning(self.meta, self.transcripts, self.project, state or {}, now)

    def test_only_explicit_human_project_priority_survives(self):
        self.write_rows(self.row('a', 'Today my top priority is ship the page.'),
                        self.row('b', 'My top priority is injected skill text.', 'a', origin=None),
                        self.row('c', 'My top priority is assistant advice.', 'b', type='assistant'),
                        self.row('d', 'My top priority is unrelated private chat.', 'c', cwd='/other'))
        result, state = self.read()
        self.assertEqual(result['priorities'][0]['task'], 'ship the page.')
        stored = json.dumps(state)
        self.assertNotIn('unrelated private chat', stored)
        self.assertNotIn('injected skill text', stored)
        self.assertNotIn('message', state)

    def test_incremental_append_partial_line_and_latest_priority(self):
        self.write_rows(self.row('a', 'Today my top priority is finish VSL.'))
        first, state = self.read()
        second, state = self.read(state)
        self.assertEqual(second['bytesRead'], 0)
        row = self.row('b', 'Today my top priority is launch the page.', 'a', timestamp='2026-09-30T14:00:00Z')
        text = json.dumps(row)
        with self.file.open('a') as stream:
            stream.write(text[:30])
        pending, state = self.read(state)
        self.assertEqual(pending['priorities'], first['priorities'])
        with self.file.open('a') as stream:
            stream.write(text[30:] + '\n')
        final, _ = self.read(state)
        self.assertEqual(final['priorities'][0]['task'], 'launch the page.')

    def test_non_priority_followup_does_not_replace_priority(self):
        self.write_rows(self.row('a', 'Today my top priority is finish VSL.'), self.row('b', 'Are these lights the right size?', 'a', timestamp='2026-09-30T14:00:00Z'))
        result, _ = self.read()
        self.assertIn('finish VSL', result['priorities'][0]['task'])

    def test_abandoned_branch_and_sidechain_excluded(self):
        self.write_rows(self.row('a', 'Today my top priority is old branch.'),
                        self.row('b', 'Today my top priority is active branch.', timestamp='2026-09-30T14:00:00Z'),
                        self.row('c', 'Today my top priority is subagent.', 'b', isSidechain=True))
        result, _ = self.read()
        self.assertEqual(result['priorities'][0]['task'], 'active branch.')

    def test_truncated_file_rescanned(self):
        self.write_rows(self.row('a', 'Today my top priority is ' + 'old task ' * 25))
        _, state = self.read()
        self.write_rows(self.row('b', 'Today my top priority is new task.'))
        result, _ = self.read(state)
        self.assertEqual(result['priorities'][0]['task'], 'new task.')

    def test_attachment_ancestry_and_pending_human_frame(self):
        meta = json.loads(self.metadata.read_text())
        meta['lastAssistantUuid'] = 'assistant'
        self.metadata.write_text(json.dumps(meta))
        self.write_rows(self.row('a', 'Today my top priority is finish VSL.'),
            {'uuid': 'attachment', 'parentUuid': 'a', 'type': 'attachment', 'content': 'unrelated payload'},
            self.row('assistant', 'Advice', 'attachment', type='assistant'))
        result, state = self.read()
        self.assertIn('finish VSL', result['priorities'][0]['task'])
        self.assertNotIn('unrelated payload', json.dumps(state))
        with self.file.open('a') as stream:
            stream.write(json.dumps(self.row('new', 'Today my top priority is ship the page.', 'assistant', timestamp='2026-09-30T14:00:00Z')) + '\n')
        result, _ = self.read(state)
        self.assertEqual(result['priorities'][0]['task'], 'ship the page.')

    def test_invalid_record_does_not_hide_later_priority(self):
        self.write_rows(self.row('bad', 'My top priority is invalid.', timestamp='bad'),
                        self.row('good', 'Today my top priority is ship the page.', 'bad'))
        result, _ = self.read()
        self.assertEqual(result['status'], 'partial')
        self.assertEqual(result['priorities'][0]['task'], 'ship the page.')

    def test_replaced_file_rescanned(self):
        self.write_rows(self.row('a', 'Today my top priority is old task.'))
        _, state = self.read()
        replacement = self.transcripts / 'replacement'
        replacement.write_text(json.dumps(self.row('b', 'Today my top priority is new task.')) + '\n')
        replacement.replace(self.file)
        result, _ = self.read(state)
        self.assertEqual(result['priorities'][0]['task'], 'new task.')

    def test_other_project_metadata_never_reads_transcript(self):
        data = json.loads(self.metadata.read_text())
        data.update(cwd='/other', originCwd='/other')
        self.metadata.write_text(json.dumps(data))
        self.write_rows(self.row('a', 'Today my top priority is private.'))
        result, _ = self.read()
        self.assertEqual(result['sessionsExamined'], 0)

    def test_malformed_line_reports_partial(self):
        self.write_rows(self.row('a', 'Today my top priority is finish VSL.'))
        with self.file.open('a') as stream:
            stream.write('{invalid json}\n')
        result, _ = self.read()
        self.assertEqual(result['status'], 'partial')

    def test_day_scope_stale_and_future_rejected(self):
        self.assertFalse(extract_priorities('Today my top priority is X.', '2026-09-29T18:00:00Z', NOW))
        self.assertFalse(extract_priorities('My top priority is X.', '2026-09-25T18:00:00Z', NOW))
        self.assertFalse(extract_priorities('My top priority is X.', '2026-10-01T18:00:00Z', NOW))
        self.assertTrue(extract_priorities('Tomorrow my top priority is X.', '2026-09-29T18:00:00Z', NOW))

    def test_cached_tomorrow_plan_becomes_applicable_next_day(self):
        self.write_rows(self.row('a', 'Tomorrow my top priority is launch the page.'))
        first, state = self.read()
        self.assertEqual(first['priorities'], [])
        next_day, _ = self.read(state, datetime(2026, 10, 1, 12, tzinfo=timezone.utc))
        self.assertEqual(next_day['bytesRead'], 0)
        self.assertEqual(next_day['priorities'][0]['task'], 'launch the page.')

    def test_cache_version_change_rescans(self):
        self.write_rows(self.row('a', 'Today my top priority is ship the page.'))
        _, state = self.read()
        state['parserVersion'] = -1
        result, _ = self.read(state)
        self.assertGreater(result['bytesRead'], 0)

    def test_bullet_task_followed_by_rank(self):
        rows = extract_priorities('* Finish editing my VSL. That\'s definitely top priority.\n* Finish the page. That is definitely the second priority.', AT, NOW)
        self.assertEqual([r['rank'] for r in rows], [1, 2])
        self.assertEqual(rows[0]['task'], 'Finish editing my VSL.')

    def test_no_duplicate_or_negated_priority_and_incidental_tomorrow(self):
        rows = extract_priorities('Today my top priority is ship the page. Tomorrow the lights arrive. Should ads be my top priority? That is not the top priority. My top priority is an explanation of the page.', AT, NOW)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['task'], 'ship the page.')

    def test_legacy_plan_needs_today_and_fresh_timestamp(self):
        file = self.root / 'plan.json'
        file.write_text(json.dumps({'writtenAt': AT, 'forDate': '2026-09-29', 'oneThing': 'Old task'}))
        self.assertEqual(legacy_plan(file, NOW)['status'], 'stale')
        file.write_text(json.dumps({'writtenAt': AT, 'forDate': '2026-09-30', 'oneThing': 'Task', 'raw': 'unneeded'}))
        data = legacy_plan(file, NOW)
        self.assertTrue(data['supportingOnly'])
        self.assertNotIn('unneeded', json.dumps(data))

    def test_snapshot_missing_stale_malformed_and_zero(self):
        file = self.root / 'input.json'
        self.assertEqual(snapshot(file, NOW, 24)['status'], 'missing')
        file.write_text(json.dumps({'generatedAt': '2026-09-20T12:00:00Z', 'count': 0}))
        self.assertEqual(snapshot(file, NOW, 24)['status'], 'stale')
        file.write_text('[]')
        self.assertEqual(snapshot(file, NOW, 24)['status'], 'error')
        file.write_text(json.dumps({'generatedAt': AT, 'count': 0}))
        self.assertEqual(snapshot(file, NOW, 24)['data']['count'], 0)

    def test_priority_fallback_uses_position_not_array_order(self):
        trello = select_trello({'status': 'ok', 'sourceAt': AT, 'data': {'lists': {
            'dan_in_progress': [{'id': 'later', 'title': 'Later', 'position': 9}, {'id': 'first', 'title': 'First', 'position': 1}],
            'dan_queue': [{'id': 'q', 'title': 'Queue', 'position': 0}]}}}, NOW)
        self.assertEqual(select_priority({}, trello)['cardId'], 'first')
        plan = {'priorities': [{'rank': 1, 'task': 'Explicit', 'statedAt': AT}]}
        self.assertEqual(select_priority(plan, trello)['source'], 'claude_explicit_plan')
        trello['lists']['dan_in_progress'] = []
        self.assertEqual(select_priority({}, trello)['cardId'], 'q')
        self.assertEqual(select_priority({}, {'status': 'missing'})['status'], 'missing')

    def test_private_output_cannot_live_in_repo_and_is_mode_600(self):
        (self.project / '.git').mkdir()
        with self.assertRaises(ValueError):
            private_directory(self.project / 'private')
        args = argparse.Namespace(now=AT, state_dir=str(self.root / 'private'), config=None,
            project_root=str(self.project), secrets_file=str(self.root / 'absent.env'), live=False)
        directory, result = collect(args)
        self.assertEqual(os.stat(directory / 'brief-inputs.json').st_mode & 0o777, 0o600)
        self.assertFalse(result['scheduleChanged'])
        self.assertNotIn('routineEnabled', result)  # Collector cannot assert cloud schedule state.
        self.assertEqual(result['sources']['trello']['status'], 'missing')

    def test_secrets_redacted_from_nested_fields(self):
        result = redact({'note': 'secret-token-123', 'nested': {'access_token': 'secret-token-123', 'count': 0}}, {'API_KEY': 'secret-token-123'})
        self.assertNotIn('secret-token-123', json.dumps(result))
        self.assertEqual(result['nested']['count'], 0)

    def test_failed_dashboard_not_empty_success(self):
        with patch('collect_inputs.request_json', return_value={'status': 'error', 'httpStatus': 401}):
            self.assertEqual(dashboard({'DASH_SECRET': 'fixture'})['status'], 'partial')
        with patch('collect_inputs.request_json', return_value={'status': 'ok', 'data': {}}):
            self.assertEqual(dashboard({'DASH_SECRET': 'fixture'})['reads']['todos']['status'], 'error')

    def test_posthog_unknown_mapping_and_verified_zero(self):
        response = {'status': 'ok', 'data': {'results': [['absbyai.com', '$pageview', 7, 4]]}}
        with patch('collect_inputs.request_json', return_value=response):
            data = posthog({'POSTHOG_PERSONAL_KEY': 'fixture'}, {'site_events': {'absbyai.com': {'trials': 'trial_started'}}}, windows(NOW))
        site = data['windows']['yesterday']['sites']['absbyai.com']
        self.assertEqual(site['visitors']['value'], 4)
        self.assertIsNone(site['paid']['value'])
        self.assertEqual(site['trials']['value'], 0)
        self.assertIsNone(data['windows']['yesterday']['sites']['sixpackabs.com']['visitors']['value'])

    def test_site_mapping_cannot_double_count_one_event(self):
        with patch('collect_inputs.request_json') as request:
            data = posthog({'POSTHOG_PERSONAL_KEY': 'fixture'}, {'site_events': {'absbyai.com': {'trials': 'conversion', 'paid': 'conversion'}}}, windows(NOW))
        self.assertEqual(data['status'], 'error')
        request.assert_not_called()

    def test_browser_attempts_cannot_be_business_outcomes(self):
        for metric, event in [('email_leads', 'email_subscribed'), ('trials', 'membership_subscribed'),
                              ('paid', 'paid_conversion_reported'), ('free_generations', 'generation_started')]:
            with patch('collect_inputs.request_json') as request:
                result = posthog({'POSTHOG_PERSONAL_KEY': 'fixture'}, {'site_events': {'absbyai.com': {metric: event}}}, windows(NOW))
            self.assertEqual(result['status'], 'error')
            request.assert_not_called()

    def test_verified_database_leads_override_attempt_counts_only_on_success(self):
        sites = {'windows': {'yesterday': {'status': 'ok', 'sites': {s: {'email_leads': {'status': 'unmapped', 'value': None}} for s in ('absbyai.com', 'sixpackabs.com')}}}}
        merge_verified_leads(sites, {'status': 'error'})
        self.assertIsNone(sites['windows']['yesterday']['sites']['absbyai.com']['email_leads']['value'])
        leads = {'status': 'ok', 'windows': {'yesterday': {'unattributed': 1, 'sites': {s: {'status': 'verified_database', 'value': 0} for s in ('absbyai.com', 'sixpackabs.com')}}}}
        merge_verified_leads(sites, leads)
        self.assertEqual(sites['windows']['yesterday']['sites']['absbyai.com']['email_leads']['value'], 0)
        self.assertEqual(sites['windows']['yesterday']['unattributedEmailLeads'], 1)

    def test_guard_failure_cannot_be_clean_and_hit_ids_retained(self):
        (self.project / 'scripts/blotato').mkdir(parents=True)
        (self.project / 'scripts/blotato/ad_guard.py').touch()
        with patch('collect_inputs.subprocess.run', return_value=argparse.Namespace(returncode=1, stdout='bad token', stderr='')):
            self.assertEqual(ad_guard(self.project)['status'], 'error')
        with patch('collect_inputs.subprocess.run', return_value=argparse.Namespace(returncode=1, stdout='scanned 8 scheduled posts\n AD IN QUEUE schedule 123 ', stderr='')):
            self.assertEqual(ad_guard(self.project)['hits'], [{'scheduleId': '123'}])

    def test_missing_ads_credentials_does_not_call_shared_client(self):
        with patch('collect_inputs.subprocess.run') as run:
            result = run_ads({}, windows(NOW), {})
        self.assertEqual(result['status'], 'missing')
        run.assert_not_called()

    def test_subscriber_invalid_success_schema_is_error(self):
        with patch('collect_inputs.subprocess.run', return_value=argparse.Namespace(stdout='{"status":"ok"}')):
            self.assertEqual(subscriber_leads(self.project, windows(NOW), {})['status'], 'error')

    def test_central_dst_window_uses_full_local_day(self):
        result = windows(datetime(2026, 11, 2, 14, tzinfo=timezone.utc))
        start = datetime.fromisoformat(result['yesterday']['from'])
        end = datetime.fromisoformat(result['yesterday']['toExclusive'])
        self.assertEqual((end-start).total_seconds(), 25*3600)


if __name__ == '__main__':
    unittest.main()
