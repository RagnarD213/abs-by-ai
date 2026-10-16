from pathlib import Path
R=Path('/Volumes/Extreme/_edit_work/ra13');src=(R/'round2/recipe/review_page_r2.py').read_text().replace('/Volumes/Extreme/_edit_work/ra13/round2','/Volumes/Expansion/Abs By AI Edit Work/ra13/round3').replace("'round2'","'round3'").replace('AD R2','AD R3').replace('ROUND 2','ROUND 3')
a=src.index('items=[');b=src.index('\ncs=',a)
src=src[:a]+'''items=[('centering','0.00, 2.27, 25.16, 38.97, 42.61, 46.58','Vertical centering','Measured the exact first frame of every presenter shot, then used the shared land-then-hold track. Approved crop sizes and hair clearance preserved.'),('P1','14.35 - 25.16','Generation and results in one phone','B0550: the white man generating, then his own settled after-only results screen. Same phone frame, size and position throughout. The internal screen cut is at 20.59.'),('A1','28.36 - 33.77','Matching analysis photo','The exact white-man after picture replaces Dan in the existing scan, three bars and plan treatment. No invented numbers.')]'''+src[b:]
src=src.replace('Brighter Natural B, approved lighter bass and vertical crop. Horizontal close shots retain their size with about 30% less empty headroom.','R3: corrected vertical landings, the white-man generation/results sequence inside one phone, and his matching analysis picture. Approved audio, color, captions and horizontal framing preserved.')
a=src.index('<h2>Changes to check</h2>');b=src.index('<h2>Retained graphics in timeline order</h2>',a)
src=src[:a]+'''<h2>Changes to check</h2><section><p><b>Vertical centering:</b> opening and each presenter return or scale cut at 0.00, 2.27, 25.16, 38.97, 42.61 and 46.58. Watch 0 - 6, 24.5 - 29 and 38.5 - 48.</p><p><b>Phone sequence:</b> 14.35 - 25.16, internal result cut 20.59. Watch 13 - 27.</p><p><b>Analysis photo:</b> 28.36 - 33.77. Watch 27 - 35.</p></section>'''+src[b:]
src=src.replace('Retained graphics in timeline order','Changed scenes in timeline order')
src=src.replace("localStorage.getItem('RA13R2notes')||''","localStorage.getItem('RA13R3notes')||localStorage.getItem('RA13R2notes')||''").replace("localStorage.setItem('RA13R2notes'","localStorage.setItem('RA13R3notes'")
# Keep the October 16 recovery and inactive-tab code intact.
assert 'function recoverVideo()' in src and 'restoreAfterInactivity' in src
exec(compile(src,str(R/'round3/recipe/review_page.py'),'exec'))
from pathlib import Path
import html,json
P=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3/review');status=json.load(open(P.parent/'delivery-status.json'));doc=(P/'index.html').read_text();flags=status.get('open_gate_rows',{})
rows=''.join('<li><b>'+html.escape(fmt)+'</b>: '+html.escape(x['key'])+'<br>'+html.escape(x['detail'])+'</li>' for fmt,items in flags.items() for x in items)
if rows:doc=doc.replace('<h2>Changes to check</h2>','<details><summary>Recorded numerical gate flags</summary><ul>'+rows+'</ul></details><h2>Changes to check</h2>')
doc=doc.replace('Full-quality physical copies are also in Videos to Review for VLC.','Full-quality physical copies are also in Videos to Review for VLC. <a href="Most Guys Abs AD R3 - Audio AB.m4a">Audio comparison</a> | <a href="R3 review notes.txt">Review notes and checks</a>')
assert '\u2014' not in doc and '\u2013' not in doc
(P/'index.html').write_text(doc)
doc=(P/'index.html').read_text()
doc=doc.replace('<button onclick="recoverVideo()">Reload video</button>','<button id="soundToggle" onclick="film.muted=!film.muted">Mute</button><button onclick="film.pause()">Pause video</button><button onclick="recoverVideo()">Reload video</button>')
doc=doc.replace('<h2>Changes to check</h2><section>','<h2>Changes to check</h2><section><button onclick="load(\'Most Guys Abs AD R3 - 9x16 - REVIEW540p.mp4\',\'Phone screen cut\',19.5)">Check phone cut</button><button onclick="load(\'Most Guys Abs AD R3 - 9x16 - REVIEW540p.mp4\',\'Analysis photo\',27)">Check analysis</button><button onclick="load(\'Most Guys Abs AD R3 - 9x16 - REVIEW540p.mp4\',\'Later vertical centering\',38.5)">Check later centering</button>')
doc=doc.replace("const playbackStatus=", "const soundToggle=document.querySelector('#soundToggle');\nfunction syncSoundLabel(){soundToggle.textContent=film.muted?'Unmute':'Mute';}\nfilm.addEventListener('volumechange',syncSoundLabel);syncSoundLabel();\nconst playbackStatus=")
assert '\u2014' not in doc and '\u2013' not in doc
(P/'index.html').write_text(doc)
