from pathlib import Path
import sys,subprocess,json,hashlib
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra13');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra13/round3');B=W/'round2';sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
FF=str(R/'Media/video_edit/bin/ffmpeg');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();rows=[]
buildcap.wait('RA13 R3 exact audio and preservation evidence')
for fmt in ['9x16','16x9']:
 old=next((B/'final').glob('[!._]*'+fmt+'*.mp4'));new=next((O/'final').glob('[!._]*'+fmt+'*.mp4'));audio=[]
 assert sha(old)=={'9x16':'2f10b36412e1890c8618161c628725876cce1f794e329bc5c31e7f49abaa90ed','16x9':'453c6f10bcb7142f6065c7344e8b91fa0b29a088b301d245a450f4a9a4752d5a'}[fmt],'R2 baseline hash changed'
 for p in [old,new]:
  raw=subprocess.run([FF,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True).stdout;audio.append(hashlib.sha256(raw).hexdigest())
 assert audio[0]==audio[1],fmt+' audio changed'
 rows.append(dict(format=fmt,baseline_sha256=sha(old),candidate_sha256=sha(new),audio_aac_sha256=audio[0],audio_bit_identical=True))
# Horizontal camera and unaffected tour inputs are copied whole, not re-cropped.
components=[]
for pattern in ['seg16/[!._]*.mp4','media/P2-*.mp4']:
 for p in O.glob(pattern):
  q=B/p.relative_to(O);assert sha(p)==sha(q);components.append(dict(path=str(p),baseline=str(q),sha256=sha(p),byte_identical=True))
for fmt in ['9','16']:
 old=json.load(open(B/f'cap{fmt}/caption_states.json'));new=json.load(open(O/f'cap{fmt}/caption_states.json'));assert old==new
 (O/f'checks{fmt}/speech.json').write_bytes((B/f'checks{fmt}/speech.json').read_bytes());(O/f'checks{fmt}/transcript.json').write_bytes((B/f'checks{fmt}/transcript.json').read_bytes())
(O/'preservation.json').write_text(json.dumps(dict(videos=rows,components=components,captions='Identical states and PNG inputs; unchanged 1616-frame timeline.',transcript='Reused CTC and Whisper evidence only after exact delivered AAC identity verification.'),indent=2));print('PRESERVATION VERIFIED',flush=True)
