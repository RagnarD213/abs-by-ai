import contextlib,io,json,pathlib,runpy,subprocess,sys,tempfile,unittest
from unittest.mock import patch
SCRIPT=pathlib.Path(__file__).resolve().parents[1]/'wallpaper/install.py'
class Installer(unittest.TestCase):
 def run_action(self,home,action,loaded=False,active=False):
  calls=[]
  def run(command,**kw):
   calls.append(command)
   if command[0]=='launchctl' and command[1]=='print':return subprocess.CompletedProcess(command,0 if loaded else 113,'','' if loaded else 'Could not find service')
   return subprocess.CompletedProcess(command,0,'','')
  def output(command,**kw):
   if command[0]=='ps':return f'99  {__import__("os").getuid()} /usr/bin/node {home}/Library/Application Support/AbsByAIWallpaper/bin/reader.js' if active else ''
   if command[-1]=='--inspect':return json.dumps([{'id':'22','uuid':'physical','path':'new'}]).encode()
   raise AssertionError(command)
  stream=io.StringIO()
  with patch('pathlib.Path.home',return_value=home),patch.object(sys,'argv',[str(SCRIPT),action]),patch('subprocess.run',side_effect=run),patch('subprocess.check_output',side_effect=output),patch('time.sleep'),contextlib.redirect_stdout(stream):
   with self.assertRaises(SystemExit) as error:runpy.run_path(str(SCRIPT),run_name='__main__')
  return error.exception.code,calls,stream.getvalue()
 def test_verified_disable_preserves_unrelated_agents(self):
  with tempfile.TemporaryDirectory() as tmp:
   home=pathlib.Path(tmp);agents=home/'Library/LaunchAgents';agents.mkdir(parents=True)
   own=agents/'com.absbyai.wallpaper-reader.plist';own.write_text('reader');other=agents/'unrelated.plist';other.write_text('keep')
   code,calls,text=self.run_action(home,'stop')
   self.assertIsNone(code);self.assertIn('Offline rotation stopped',text)
   self.assertFalse(own.exists());self.assertEqual(own.with_suffix('.plist.disabled').read_text(),'reader');self.assertEqual(other.read_text(),'keep')
   self.assertTrue((home/'Library/Application Support/AbsByAIWallpaper/disabled').exists())
   self.assertEqual([c[1] for c in calls[:3]],['disable','bootout','print'])
 def test_unload_or_running_process_failure_is_not_success(self):
  for loaded,active,expected in [(True,False,'Could not verify'),(False,True,'remains running')]:
   with tempfile.TemporaryDirectory() as tmp:
    code,_,text=self.run_action(pathlib.Path(tmp),'stop',loaded,active)
    self.assertIn(expected,code);self.assertNotIn('Verified:',text)
 def test_restore_matches_physical_display_and_discloses_shuffle_limit(self):
  with tempfile.TemporaryDirectory() as tmp:
   home=pathlib.Path(tmp);root=home/'Library/Application Support/AbsByAIWallpaper';root.mkdir(parents=True)
   image=home/'old.png';image.write_bytes(b'synthetic')
   (root/'wallpapers-before.json').write_text(json.dumps([{'id':'1','uuid':'physical','path':str(image)}]))
   code,calls,text=self.run_action(home,'restore');self.assertIsNone(code)
   self.assertTrue(any(c[-1]=='--apply' for c in calls));self.assertIn('System Settings',text)
if __name__=='__main__':unittest.main()
