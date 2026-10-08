import json
import sys
import tempfile
import unittest
from pathlib import Path
from datetime import datetime, timezone, timedelta
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from master_queue import Inventory, locked, import_studio, from_live, plan_topup, reconcile, stamp, longform_errors, CT
from review_queue import review, public_tile


def guard(*args, **kwargs):
    pass


class MasterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.inv = Inventory(self.temp.name)
        self.now = datetime(2026, 10, 8, 18, tzinfo=timezone.utc)
        self.plan = [{'post': 'p', 'account': '67203', 'platform': 'instagram', 'scheduledTime': '2026-10-09T22:00:00Z', 'media': ['https://example.com/a.jpg']}]
        self.manifest = {'approved_on': '2026-10-03', 'approval_quote': 'These are approved', 'status': 'Approved', 'posts': [{'id': 'p', 'title': 'Photo', 'caption': 'Caption'}]}

    def tearDown(self):
        self.inv.db.close()
        self.temp.cleanup()

    def seed(self):
        import_studio(self.inv, self.plan, self.manifest, self.now.isoformat())
        r = self.inv.records()[0]
        r['assetChecks'] = {u:{'checkedAt': self.now.isoformat(), 'status':200} for u in r['media']}
        self.inv.put(r, {'source': 'synthetic measured assets'})
        return r

    def test_rehosted_media_dedup_requires_approved_hashes(self):
        r = self.seed()
        self.manifest['posts'][0]['images'] = [{'sha256':'a'*64}]
        payload = json.loads(json.dumps(r['payload'])); payload['content']['mediaUrls'] = ['https://example.com/rehost.jpg']
        item = {'id':'live','scheduledAt':r['scheduledAt'],'draft':payload}
        self.inv.put(from_live(item,self.now.isoformat()),item)
        import_studio(self.inv,self.plan,self.manifest,self.now.isoformat(),[item],{'https://example.com/rehost.jpg':'wrong'})
        self.assertEqual(len(self.inv.records()),2)
        import_studio(self.inv,self.plan,self.manifest,self.now.isoformat(),[item],{'https://example.com/rehost.jpg':'a'*64})
        self.assertEqual(len(self.inv.records()),1)
        self.assertEqual(self.inv.records()[0]['approval']['status'],'approved')

    def test_topup_holds_inaccessible_media(self):
        r = self.seed(); r['assetChecks'][r['media'][0]]['status']=403
        self.inv.put(r, {'source':'synthetic inaccessible assets'})
        p = plan_topup(self.inv,[],self.now,guard)
        self.assertFalse(p['create'])
        self.assertIn('inaccessible', ' '.join(p['held'][0]['reasons']))

    def test_duplicate_import_preserves_approval_evidence(self):
        record = self.seed()
        self.seed()
        item = {'id': 'live1', 'scheduledAt': record['scheduledAt'], 'draft': record['payload']}
        self.inv.put(from_live(item, self.now.isoformat()), item)
        self.assertEqual(len(self.inv.records()), 1)
        self.assertEqual(self.inv.records()[0]['approval']['status'], 'approved')
        self.assertEqual(len(self.inv.records()[0]['provenance']), 2)
        self.assertEqual(len(plan_topup(self.inv, [item], self.now, guard)['create']), 0)

    def test_cap_counts_every_platform_and_no_inventory_cap(self):
        record = self.seed()
        for n in range(210):
            r = json.loads(json.dumps(record)); r['payload']['content']['text'] = str(n)
            self.inv.put(r, {'source': str(n)})
        live = [{'id': str(n), 'scheduledAt': '2026-11-15T15:00:00Z', 'draft': {'accountId': str(n), 'content': {'platform': 'tiktok'}, 'target': {}}} for n in range(199)]
        result = plan_topup(self.inv, live, self.now, guard)
        self.assertEqual(len(self.inv.records()), 211)
        self.assertEqual(len(result['create']), 1)
        self.assertTrue(result['held'])  # identical account/time never doubled
        live.append({**live[0], 'id': 'extra'})
        result = plan_topup(self.inv, live, self.now, guard)
        self.assertEqual(len(result['create']), 0)
        self.assertEqual(len(result['overflow']), 211)

    def test_no_draft_approval_no_date_reslot(self):
        self.manifest.pop('approval_quote')
        self.seed()
        result = plan_topup(self.inv, [], self.now, guard)
        self.assertEqual(len(result['create']), 0)
        self.assertIn('Explicit approval', result['held'][0]['reasons'][0])
        self.now += timedelta(days=3)
        self.assertIn('Authorized date', ' '.join(plan_topup(self.inv, [], self.now, guard)['held'][0]['reasons']))

    def test_repeat_reconciliation_and_uncertain_timeout(self):
        r = self.seed(); live = []
        def create(body):
            live.append({'id': 'new', 'scheduledAt': body['scheduledTime'], 'draft': body['post']})
            return {'ok': True}
        plan = plan_topup(self.inv, live, self.now, guard)
        reconcile(self.inv, lambda: live, create, self.now, guard, plan['planDigest'])
        again = plan_topup(self.inv, live, self.now, guard)
        self.assertEqual(again['create'], [])
        reconcile(self.inv, lambda: live, create, self.now, guard, again['planDigest'])
        self.assertEqual(len(live), 1)
        self.inv.submitted(r['id'], 'uncertain')
        result = plan_topup(self.inv, [], self.now, guard)
        self.assertEqual(result['create'], [])
        self.assertIn('unresolved', result['held'][0]['reasons'][0])

    def test_concurrent_cap_refresh_and_stale_plan(self):
        self.seed(); plan = plan_topup(self.inv, [], self.now, guard)
        count = 0
        def fetch():
            nonlocal count
            count += 1
            if count == 1: return []
            return [{'scheduledAt': '2026-11-01T15:00:00Z', 'draft': {'accountId': str(n), 'content': {}, 'target': {}}} for n in range(200)]
        calls = []
        reconcile(self.inv, fetch, calls.append, self.now, guard, plan['planDigest'])
        self.assertEqual(calls, [])
        with self.assertRaises(ValueError):
            reconcile(self.inv, lambda: [], calls.append, self.now, guard, 'stale')

    def test_lock_and_git_privacy(self):
        with locked(self.temp.name):
            with self.assertRaises(BlockingIOError):
                with locked(self.temp.name): pass
        (Path(self.temp.name) / '.git').mkdir()
        with self.assertRaises(ValueError):
            with locked(self.temp.name): pass

    def test_sunday_dst_and_other_platform_hold(self):
        r = self.seed(); r['kind'] = 'longform'; r['platform'] = 'youtube'
        r['scheduledAt'] = '2026-11-01T15:00:00Z'
        self.assertEqual(stamp(r['scheduledAt']).astimezone(CT).hour, 9)
        self.assertEqual(longform_errors([r]), {})
        r2 = {**r, 'id': 'second'}
        self.assertIn('More than one', longform_errors([r, r2])[r['id']][0])
        r['scheduledAt'] = '2026-10-07T14:00:00Z'
        self.assertIn('Sunday', longform_errors([r])[r['id']][0])
        r['platform'] = 'facebook'; r['youtubeReleaseAt'] = '2026-11-01T15:00:00Z'; r['scheduledAt'] = '2026-11-02T15:00:00Z'
        self.assertIn('not verified', longform_errors([r])[r['id']][0])
        r['youtubePublicVerifiedAt'] = '2026-11-01T15:05:00Z'
        self.assertEqual(longform_errors([r]), {})
        with self.assertRaises(ValueError): stamp('2026-11-01T09:00:00')

    def test_review_local_calendar_and_stale_assets(self):
        r = self.seed();r['scheduleId']='new'
        now = datetime(2026,10,31,18,tzinfo=timezone.utc)
        r['scheduledAt']='2026-11-01T15:00:00Z'
        q = review([r], [], now, {r['cover']: {'status':200,'checkedAt':'2026-10-01T00:00:00Z'}})
        self.assertEqual((stamp(q['windowTo'])-stamp(q['windowFrom'])).total_seconds(),169*3600)
        self.assertEqual(q['rows'][0]['preflight']['cover'],'unverified')
        q = review([r], [], now, {r['cover']: {'status':404,'checkedAt':now.isoformat()}})
        self.assertEqual(q['rows'][0]['preflight']['cover'],'broken')
        self.assertEqual(q['sourceCoverage']['youtubeStudio'],'error')

    def test_tile_false_positive_and_wrong_identity(self):
        r = self.seed();r['approvedCoverSHA256']='a'*64;r['publicPostUrl']='https://example.com/post'
        evidence={'placementId':r['id'],'publicPostUrl':r['publicPostUrl'],'approvedCoverSHA256':'a'*64,'surface':'public_profile_tile','observedAt':self.now.isoformat(),'tileSHA256':'b'*64}
        self.assertEqual(public_tile(r,evidence,self.now)['status'],'unverified')
        evidence.update(reviewer='Recorded reviewer',cropNormalized=True,assessment='mismatch')
        self.assertEqual(public_tile(r,evidence,self.now)['status'],'mismatch')
        evidence['placementId']='wrong'
        self.assertEqual(public_tile(r,evidence,self.now)['status'],'unverified')


if __name__ == '__main__': unittest.main()
