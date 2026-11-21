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
 def test_silent_defaults_precede_page_scripts_and_are_idempotent(self):
  original=b'''<!doctype html><html><head><title>Review</title><script>window.pageCode=1</script></head><body><video controls autoplay src="film.mp4" data-label="a > b"></video><AUDIO controls src="voice.wav"></AUDIO><video muted controls></video><video-widget></video-widget><textarea>owner notes</textarea><script defer src="/__review_player.js"></script></body></html>'''
  page=server.prepare_review_html(original)
  self.assertEqual(page.count(b'/__review_player.js'),1)
  self.assertLess(page.index(b'/__review_player.js'),page.index(b'window.pageCode'))
  self.assertIn(b'<video muted controls autoplay',page)
  self.assertIn(b'<AUDIO muted controls',page)
  self.assertNotIn(b'muted muted',page)
  self.assertIn(b'<video muted data-note="keep muted please"',server.prepare_review_html(b'<video data-note="keep muted please" controls></video>'))
  self.assertIn(b'data-label="a > b"',page)
  self.assertIn(b'<video-widget>',page)
  self.assertIn(b'<textarea>owner notes</textarea>',page)
  self.assertEqual(server.prepare_review_html(page),page)
  fragment=server.prepare_review_html(b'<audio controls src="voice.wav"></audio>')
  self.assertTrue(fragment.startswith(b'<script src="/__review_player.js"></script>'))
  self.assertIn(b'<audio muted controls',fragment)
 def test_snapshot_preserves_context_media_without_raw_footage(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'root';root.mkdir();cache=Path(tmp)/'cache'
   (root/'index.html').write_text('<video src="film.mp4"></video><button onclick="play(&quot;context.mp4&quot;)">Play</button>')
   (root/'film.mp4').write_bytes(b'film');(root/'context.mp4').write_bytes(b'context');(root/'raw.mp4').write_bytes(b'raw')
   server.snapshot(root,cache)
   self.assertIn(b'<video muted', (cache/'index.html').read_bytes())
   self.assertEqual((cache/'index.html').read_bytes().count(b'/__review_player.js'),1)
   self.assertEqual({p.name for p in cache.iterdir()},{'index.html','film.mp4','context.mp4'})
   (root/'context.mp4').write_bytes(b'revised context')
   server.snapshot(root,cache)
   self.assertEqual((cache/'context.mp4').read_bytes(),b'revised context')
   (root/'film.mp4').unlink()
   self.assertEqual((cache/'film.mp4').read_bytes(),b'film')
   with self.assertRaises(FileNotFoundError):server.snapshot(root,cache)
 def test_seek_and_drive_reconnect(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'media';root.mkdir();data=bytes(range(256))*100
   (root/'clip.mp4').write_bytes(data);(root/'index.html').write_text('review')
   app=server.Server(('127.0.0.1',0),functools.partial(server.Handler,directory=str(root)))
   thread=threading.Thread(target=app.serve_forever,daemon=True);thread.start()
   base=f'http://127.0.0.1:{app.server_port}'
   try:
    with urllib.request.urlopen(base+'/') as r:
     page=r.read();self.assertEqual(page.count(b'/__review_player.js'),1)
    with urllib.request.urlopen(base+'/__review_player.js') as r:
     helper=r.read();self.assertIn(b'Reload video',helper);self.assertIn(b'Start silent checks',helper);self.assertIn(b'Finish checks for owner',helper);self.assertIn(b'AbsReviewAudio',helper);self.assertEqual(r.headers['Content-Type'],'text/javascript; charset=utf-8')
    with urllib.request.urlopen(urllib.request.Request(base+'/',method='HEAD')) as r:
     self.assertEqual(int(r.headers['Content-Length']),len(page));self.assertEqual(r.read(),b'')
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
 def test_idle_worker_exits(self):
  # 2026-10-21: a worker with no request for ABS_REVIEW_IDLE_H hours exits (launchd starts it again on the next visit)
  import socket,time
  with tempfile.TemporaryDirectory() as tmp:
   (Path(tmp)/'index.html').write_text('x')
   with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
   t=threading.Thread(target=server.serve,args=(port,Path(tmp)),kwargs={'idle_hours':0.0005},daemon=True);t.start()
   time.sleep(0.5)
   with urllib.request.urlopen(f'http://127.0.0.1:{port}/') as r:self.assertEqual(r.status,200)
   t.join(10);self.assertFalse(t.is_alive())
class Fullscreen(unittest.TestCase):
    """Owner Full screen opens the review's own file in VLC at the page's time; nothing outside the review."""
    def test_opens_inside_file_at_time(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'media').mkdir(); f = Path(d)/'media'/'film one.mp4'; f.write_bytes(b'x')
            calls = []
            r = server.open_fullscreen(d, {'src': 'http://127.0.0.1:9811/media/film%20one.mp4', 't': 12.345},
                                       launch=lambda cmd, **k: calls.append(cmd))
            self.assertTrue(r['ok'], r); self.assertEqual(len(calls), 1)
            if r['player'] == 'VLC':
                self.assertIn('--fullscreen', calls[0]); self.assertIn('--start-time=12.35', calls[0])
            self.assertEqual(calls[0][-1], str(f.resolve()))
    def test_refuses_outside_and_non_video(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'notes.txt').write_bytes(b'x')
            boom = lambda *a, **k: self.fail('must not launch')
            for src in ('/../../etc/passwd', '/notes.txt', '/missing.mp4', ''):
                self.assertFalse(server.open_fullscreen(d, {'src': src, 't': 0}, launch=boom)['ok'], src)
            self.assertFalse(server.open_fullscreen(d, {'src': '/a.mp4', 't': 'x'}, launch=boom)['ok'])


if __name__=='__main__':unittest.main()
