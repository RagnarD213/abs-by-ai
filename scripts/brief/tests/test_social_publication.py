import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from publish_brief import batches, social_inputs


class PublicationTests(unittest.TestCase):
    def test_transport_batches_do_not_truncate_inventory(self):
        records = [{'id':str(n),'caption':'x'*8000} for n in range(253)]
        result=list(batches({'focus':{'task':'Keep original text'}},records))
        self.assertEqual(sum(size for _,size in result),253)
        self.assertTrue(all(len(body)<=512000 for body,_ in result))
        imported=[r for body,_ in result for r in json.loads(body)['socialMasterImports']]
        self.assertEqual(imported,records)
        self.assertTrue(all(json.loads(body)['focus']['task']=='Keep original text' for body,_ in result))

    def test_stale_source_and_private_directory(self):
        now=datetime(2026,10,8,18,tzinfo=timezone.utc)
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'social-master-export.json').write_text('[]')
            (root/'social-queue.json').write_text(json.dumps({'checkedAt':now.isoformat()}))
            self.assertEqual(social_inputs(root,now)[1],[])
            with self.assertRaises(ValueError):social_inputs(root,now+timedelta(hours=13))
            (root/'.git').mkdir()
            with self.assertRaises(ValueError):social_inputs(root,now)


if __name__=='__main__':unittest.main()
