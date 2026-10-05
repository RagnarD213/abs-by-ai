import importlib.util,subprocess,tempfile,unittest
from pathlib import Path
p=Path(__file__).with_name('framing.py')
spec=importlib.util.spec_from_file_location('framing',p); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
# Use the same bundled decoder as framing.py.
class Geometry(unittest.TestCase):
 def test_decoded_shapes(self):
  with tempfile.TemporaryDirectory() as tmp:
   for source,expected,sar in [('1080x1920',(540,960),'1'),('1920x1080',(960,540),'1'),('800x800',(960,960),'1'),('720x480',(960,540),'32/27')]:
    f=Path(tmp)/(source+sar.replace('/','_')+'.mp4')
    subprocess.run([m.FF,'-v','error','-f','lavfi','-i','testsrc2=size='+source+':rate=2','-vf','setsar='+sar,'-t','1','-c:v','libx264',str(f)],check=True)
    size=m.analysis_size(f);self.assertEqual(size,expected)
    imgs=list(m.frames(str(f),2,*size));self.assertEqual(len(imgs),2);self.assertEqual(imgs[0].shape,(expected[1],expected[0],3))
   rotated=Path(tmp)/'rotated.mp4'
   subprocess.run([m.FF,'-v','error','-i',str(Path(tmp)/'1920x10801.mp4'),'-c','copy','-metadata:s:v:0','rotate=90',str(rotated)],check=True)
   self.assertEqual(m.analysis_size(rotated),(540,960))
 def test_bad_input_fails(self):
  with self.assertRaises(subprocess.CalledProcessError):m.analysis_size('/no-such-video.mp4')
if __name__=='__main__':unittest.main()
