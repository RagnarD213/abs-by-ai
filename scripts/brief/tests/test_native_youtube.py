import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from native_youtube import native_records,add_native_rows


class NativeTests(unittest.TestCase):
    def snapshot(self):
        return {'status':'ok','checkedAt':'2026-10-08T20:00:00Z','channel':{'id':'channel'},'videos':[
            {'id':'D9v9POAKe_Q','status':{'privacyStatus':'private','publishAt':'2026-10-08T22:00:00Z'},
             'snippet':{'title':'Native short','description':'https://absbyai.com/?utm_medium=short','thumbnails':{'high':{'url':'https://i9.ytimg.com/vi/D9v9POAKe_Q/hqdefault.jpg?sqp=x&rs=y'}}}}]}

    def test_native_read_is_not_approval_and_short_does_not_trigger_sunday(self):
        records=native_records(self.snapshot());self.assertEqual(records[0]['approval']['status'],'scheduled_observed')
        q={'windowFrom':'2026-10-08T00:00:00-05:00','windowTo':'2026-10-15T00:00:00-05:00','checkedAt':'2026-10-08T20:00:00Z','rows':[]}
        add_native_rows(q,records,{records[0]['cover']:{'checkedAt':q['checkedAt'],'status':200}})
        self.assertEqual(q['rows'][0]['preflight']['cadence'],'verified');self.assertEqual(q['rows'][0]['preflight']['cover'],'verified')
        self.assertIsNone(q['rows'][0]['mediaUrl'])

    def test_error_never_becomes_verified_zero(self):
        self.assertEqual(native_records({'status':'error','reason':'HTTP401'}),[])

    def test_same_time_native_and_blotato_needs_identity_review(self):
        records=native_records(self.snapshot());q={'windowFrom':'2026-10-08T00:00:00-05:00','windowTo':'2026-10-15T00:00:00-05:00','checkedAt':'2026-10-08T20:00:00Z',
            'rows':[{'platform':'youtube','scheduledAt':records[0]['scheduledAt'],'preflight':{},'notes':[]}]}
        add_native_rows(q,records,{})
        self.assertTrue(all(r['preflight']['duplicates']=='duplicate' for r in q['rows']))


if __name__=='__main__':unittest.main()
