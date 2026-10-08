"""Playback regression checks: seeking, missing drives and reconnect recovery."""
import functools
import importlib.util
from pathlib import Path
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
import sys
spec=importlib.util.spec_from_file_location('review_server',sys.argv.pop(1))
server=importlib.util.module_from_spec(spec);spec.loader.exec_module(server)
class Playback(unittest.TestCase):
 def test_seek_and_drive_reconnect(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'media';root.mkdir();data=bytes(range(256))*100
   (root/'clip.mp4').write_bytes(data);(root/'index.html').write_text('review')
   app=server.Server(('127.0.0.1',0),functools.partial(server.Handler,directory=str(root)))
   thread=threading.Thread(target=app.serve_forever,daemon=True);thread.start()
   base=f'http://127.0.0.1:{app.server_port}'
   try:
    for header,start,end in [('bytes=10000-10099',10000,10100),('bytes=10-19',10,20),('bytes=-8',len(data)-8,len(data)),('bytes=25000-',25000,len(data))]:
     with urllib.request.urlopen(urllib.request.Request(base+'/clip.mp4',headers={'Range':header})) as r:
      self.assertEqual(r.status,206);self.assertEqual(r.read(),data[start:end]);self.assertEqual(r.headers['Content-Range'],f'bytes {start}-{end-1}/{len(data)}')
    with urllib.request.urlopen(base+'/clip.mp4') as r:self.assertEqual(r.read(),data)
    for header in ['bytes=999999-','bytes=50-10','bytes=-0']:
     with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(urllib.request.Request(base+'/clip.mp4',headers={'Range':header}))
     self.assertEqual(e.exception.code,416)
    moved=root.with_name('disconnected');root.rename(moved)
    with self.assertRaises(urllib.error.HTTPError) as e:urllib.request.urlopen(base+'/')
    self.assertEqual(e.exception.code,503)
    self.assertFalse(server.health(app.server_port)['available'])
    moved.rename(root)
    with urllib.request.urlopen(base+'/') as r:self.assertEqual(r.status,200)
   finally:app.shutdown();app.server_close();thread.join()
if __name__=='__main__':unittest.main()
