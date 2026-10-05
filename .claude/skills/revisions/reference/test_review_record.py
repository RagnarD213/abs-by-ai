import json,tempfile,unittest
from pathlib import Path
from review_record import sha,validate,freeze
class Record(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.b=Path(self.tmp.name)
  (self.b/'proof').write_text('Observed evidence');(self.b/'video').write_bytes(b'video fixture')
  self.d={'source':{'path':str(self.b/'video'),'sha256':sha(self.b/'video'),'duration':10},'coverage':{k:[{'start':0,'end':10,'reviewer':'reviewer','method':'stated method','observations':'whole span','evidence':'proof'}] for k in ('picture','motion','audio')},'unresolved':[],'benchmark_unseen':True}
  for k in ('joins','ai_shots','text_panels'):self.d[k]={'inventory_complete':True,'items':[],'none_reason':'fixture has none'}
  for k in ('audio_measurements','framing_evidence','library_pass','calibration_selfcheck'):self.d[k]='proof'
 def tearDown(self):self.tmp.cleanup()
 def test_complete_is_bookkeeping_only(self):self.assertEqual(validate(self.d,self.b)[0],[])
 def test_tail_missing(self):
  self.d['coverage']['audio'][0]['end']=9;self.assertTrue(validate(self.d,self.b)[0])
 def test_internal_gap(self):
  x=self.d['coverage']['motion'][0];self.d['coverage']['motion']=[dict(x,end=3),dict(x,start=4)];self.assertTrue(validate(self.d,self.b)[0])
 def test_changed_source(self):
  (self.b/'video').write_bytes(b'changed');self.assertTrue(validate(self.d,self.b)[0])
 def test_missing_ai_ending(self):
  self.d['ai_shots']['items']=[{'start':1,'end':3,'observation':'face','disposition':'retained','consecutive_fullres':'proof','regions':'proof','motion':'proof'}];self.assertTrue(validate(self.d,self.b)[0])
 def test_unresolved(self):
  self.d['unresolved']=['unknown'];self.assertTrue(validate(self.d,self.b)[0])
 def test_proof_missing(self):
  (self.b/'proof').unlink();self.assertTrue(validate(self.d,self.b)[0])
 def test_no_blind_freeze_exposed(self):
  self.d['benchmark_unseen']=False;p=self.b/'record.json';p.write_text(json.dumps(self.d))
  with self.assertRaises(ValueError):freeze(p,self.b/'proof',self.b/'proof',True)
 def test_freeze_no_overwrite(self):
  p=self.b/'record.json';p.write_text(json.dumps(self.d));f=freeze(p,self.b/'proof',self.b/'proof',True)
  self.assertIsNone(json.loads(f.read_text())['editorial_pass'])
  with self.assertRaises(FileExistsError):freeze(p,self.b/'proof',self.b/'proof',True)
if __name__=='__main__':unittest.main()
