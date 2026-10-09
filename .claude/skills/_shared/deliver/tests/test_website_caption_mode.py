import copy
import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/'formats.py'
spec=importlib.util.spec_from_file_location('caption_formats',P)
F=importlib.util.module_from_spec(spec);spec.loader.exec_module(F)
class WebsiteCaptionMode(unittest.TestCase):
 def test_srt_requires_sidecar_and_prohibits_running_captions(self):
  c=F.config_for('website','srt')
  self.assertTrue(c['rows']['srt:present']['required'])
  self.assertFalse(c['rows']['captions:burned']['present'])
  self.assertEqual(c['rows']['srt:shape'],F.FORMATS['longform']['rows']['srt:shape'])
  self.assertEqual(set(F.ALL_ROWS),set(c['rows'])|set(c['not_applicable']))
  self.assertFalse(set(c['rows'])&set(c['not_applicable']))
 def test_every_other_website_requirement_is_unchanged(self):
  original=copy.deepcopy(F.FORMATS['website']);c=F.config_for('website','srt')
  changed={'captions:burned','captions:sync','captions:graphic_clearance','captions:card_collision','srt:present','srt:shape'}
  for group in ('rows','not_applicable'):
   self.assertEqual({k:v for k,v in original[group].items() if k not in changed},{k:v for k,v in c[group].items() if k not in changed})
  c['rows']['container:fps']['fps']='bad'
  self.assertEqual(F.config_for('website'),original)
 def test_mistyped_or_unrelated_mode_is_rejected(self):
  for fmt,mode in [('website','none'),('website','SRT'),('ad16x9','srt')]:
   with self.assertRaises(ValueError):F.config_for(fmt,mode)
if __name__=='__main__':unittest.main()
