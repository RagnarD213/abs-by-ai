import contextlib,io,importlib.util,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('clip_library',Path(__file__).resolve().parents[1]/'clip_library.py');C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
class LibraryMetadataTests(unittest.TestCase):
 def records(self):
  base={'kind':'real','aspect':'16x9','people':'dan','category':'dan-filmed','duration':10,'used_in':[],'description':'Dan jumps rope','slug':'rope','tags':['rope'],'status':'usable-unused','library_path':'not-mounted.mp4','drive_id':None,'equipment':'jump rope'}
  return [{**base,'id':'B0001','intended_use':'correct demonstration','favorite':True},{**base,'id':'B0002','intended_use':'deliberate mistake','favorite':True},{**base,'id':'B0003','favorite':False}]
 def search(self,**options):
  args=SimpleNamespace(words='rope',kind=None,aspect=None,people=None,category=None,min_seconds=None,limit=15,rolls=False,**options)
  out=io.StringIO()
  with patch.object(C,'load',return_value={'clips':self.records()}),contextlib.redirect_stdout(out):C.cmd_find(args)
  return out.getvalue()
 def test_correct_form_excludes_mistakes_and_unknown(self):
  text=self.search(intended_use='correct demonstration',favorite=True)
  self.assertIn('B0001',text);self.assertNotIn('B0002',text);self.assertNotIn('B0003',text)
 def test_mistakes_can_be_retrieved_explicitly(self):
  text=self.search(intended_use='deliberate mistake');self.assertIn('B0002',text);self.assertNotIn('B0001',text)
 def test_old_search_still_includes_legacy_records(self):
  self.assertIn('B0003',self.search())
 def test_unusable_record_is_excluded_from_search(self):
  records=self.records();records[0]['status']='unusable'
  with patch.object(self,'records',return_value=records):self.assertNotIn('B0001',self.search())
 def test_source_out_of_bounds_rejected(self):
  with self.assertRaises(ValueError):C.metadata_fields({'source':{'in':2,'out':11,'duration':10}})
 def test_metadata_cannot_replace_id_or_library_path(self):
  self.assertEqual(C.metadata_fields({'id':'B9999','library_path':'bad','favorite':True}),{'favorite':True})
 def test_existing_sheet_shape_remains_aligned(self):
  r=self.records()[0];r.update(has_audio=True,needs_ai_label=False,file_name='clip.mp4',grade={'name':'C','filter':'technical recipe'});rows=C.sheet_rows({'clips':[r]});self.assertEqual(len(rows[0]),len(rows[1]));self.assertEqual(rows[1][-1],'C')
if __name__=='__main__':unittest.main()
