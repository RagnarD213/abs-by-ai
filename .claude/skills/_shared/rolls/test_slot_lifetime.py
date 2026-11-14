import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

SHARED=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SHARED/'renderq'));import renderq
spec=importlib.util.spec_from_file_location('roll_sidecar_test',Path(__file__).with_name('roll_sidecar.py'))
roll=importlib.util.module_from_spec(spec);sys.modules[spec.name]=roll;spec.loader.exec_module(roll)

class SlotLifetime(unittest.TestCase):
    def test_long_decode_child_remains_covered_until_exit(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.dict(os.environ,{'GATE_DIR':d,'EDIT_PRIORITY_DIR':d+'/policy','GATE_BUDGET':'8','GATE_UNMANAGED':'0','GATE_MEM':'20,0','GATE_HEADROOM_S':'0','GATE_SETTLE':'0','GATE_GROUP':'SHOOT-20990101'}):
                observations=[]
                def child(cmd,**kw):
                    # roll loads renderq by path, so inspect that instance's actual isolated registry.
                    rq=roll._buildcap()._renderq();states=rq.slot_states()
                    observations.append(sum(s['held'] for s in states));self.assertTrue(rq.held_by_me())
                    before=time.monotonic();subprocess.run([sys.executable,'-c','import time;time.sleep(.25)'],check=True)
                    self.assertTrue(rq.held_by_me());self.assertGreater(time.monotonic()-before,.24)
                with patch.object(roll,'run',side_effect=child),patch.object(roll,'binary',return_value='/fixture/ffmpeg'):
                    roll.build_contact(Path('/fixture/long roll.mp4'),180,Path(d)/'sheet.jpg')
                self.assertEqual(observations,[1]);self.assertFalse(os.environ.get('GATE_HELD'))
                self.assertTrue('"dur": 0.0' not in (Path(d)/'history.jsonl').read_text())
if __name__=='__main__':unittest.main()
