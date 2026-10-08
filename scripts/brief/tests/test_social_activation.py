import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from master_queue import Inventory, import_studio, plan_topup, reconcile
from social_topup import AuthorizedInventory
from public_tiles import extract_tiles, acquire, published_posts, PROFILES


class ActivationTests(unittest.TestCase):
    def test_authorization_cannot_expand_or_change_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            inv = Inventory(directory)
            manifest = {'approved_on':'2026-10-03','approval_quote':'Approved these','status':'Approved',
                        'posts':[{'id':'p','title':'Photo','caption':'Caption','images':[{'sha256':'a'*64}]}]}
            plan = [{'post':'p','account':'1','platform':'instagram','scheduledTime':'2026-10-09T22:00:00Z','media':['https://example.com/photo.jpg']}]
            import_studio(inv,plan,manifest,'2026-10-08T18:00:00Z')
            original = inv.records()[0]
            policy = {'version':1,'enabled':True,'windowDays':30,'cap':200,'authorizedBy':'parent','placementIds':[original['id']]}
            scoped = AuthorizedInventory(inv,policy)
            changed = json.loads(json.dumps(original)); changed['scheduledAt']='2026-10-10T22:00:00Z'
            inv.put(changed,{'source':'unapproved date change'})
            self.assertEqual([r['id'] for r in scoped.records()],[original['id']])
            with self.assertRaises(ValueError): AuthorizedInventory(inv,{**policy,'cap':201})
            with self.assertRaises(ValueError): AuthorizedInventory(inv,{**policy,'enabled':False},require_enabled=True)
            inv.db.close()

    def test_concurrent_account_time_collision_holds_without_create(self):
        with tempfile.TemporaryDirectory() as directory:
            inv = Inventory(directory)
            r={'payload':{'accountId':'1','content':{'platform':'instagram','text':'photo','mediaUrls':['https://x/a.jpg']},'target':{}},
               'platform':'instagram','account':'1','title':'photo','caption':'photo','media':['https://x/a.jpg'],'kind':'photo',
               'scheduledAt':'2026-10-09T22:00:00Z','approval':{'status':'approved'},'provenance':[]}
            inv.put(r,{})
            now=datetime(2026,10,8,18,tzinfo=timezone.utc)
            checks={'https://x/a.jpg':{'checkedAt':now.isoformat(),'status':200}}
            guard=lambda *a,**kw:None
            collision={'id':'external','scheduledAt':r['scheduledAt'],'draft':{**r['payload'],'content':{**r['payload']['content'],'text':'different'}}}
            calls=[]
            def fetch():
                calls.append(1)
                return [] if len(calls)==1 else [collision]
            digest=plan_topup(inv,[],now,guard,checks)['planDigest']
            reconcile(inv,fetch,lambda b:self.fail('Must not create collision'),now,guard,digest,checks)
            inv.db.close()

    def test_profile_renderer_not_watch_og_and_tiktok_author(self):
        renderer={'reelItemRenderer':{'videoId':'abcdefghijk','thumbnail':{'thumbnails':[{'url':'https://i.ytimg.com/vi/abcdefghijk/hqdefault.jpg'}]}}}
        self.assertEqual(len(extract_tiles('youtube','var ytInitialData = '+json.dumps(renderer)+';')),1)
        self.assertFalse(extract_tiles('youtube','<meta property="og:image" content="watch.jpg">'))
        state={'ItemModule':{'1':{'author':'someone','video':{'cover':'wrong'}},'2':{'author':'absbyai','video':{'cover':'right'}}}}
        self.assertEqual([t['postId'] for t in extract_tiles('tiktok','<script id="SIGI_STATE">'+json.dumps(state)+'</script>')],['2'])

    def test_published_read_paginates_and_rejects_repeated_cursor(self):
        class Api:
            def call(self,*a,**kw): return {'items':[],'cursor':'repeat'}
        with self.assertRaises(ValueError): published_posts(Api(),'secret',datetime.now(timezone.utc))

    def test_no_approved_reference_is_reported_and_never_matched(self):
        now=datetime.now(timezone.utc)
        post={'id':'1','platform':'youtube','text':'Caption','account':{'id':'1'},'postTime':now.isoformat(),
              'state':{'postUrl':'https://www.youtube.com/watch?v=abcdefghijk'}}
        with tempfile.TemporaryDirectory() as directory, patch('public_tiles.read_public',return_value=b'login shell'):
            rows,profiles=acquire([], [post],now,Path(directory),lambda *a:None)
        self.assertEqual(rows[0]['status'],'unverified')
        self.assertIn('no unique approved',rows[0]['reason'])
        self.assertTrue(all(p['tileCount']==0 for p in profiles))


if __name__ == '__main__': unittest.main()
