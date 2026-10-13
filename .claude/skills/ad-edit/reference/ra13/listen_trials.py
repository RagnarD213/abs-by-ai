import sys,os,json,random,shutil,subprocess,re,collections
from pathlib import Path
W=Path(__file__).resolve().parents[1];O=W/'audio-options'
script=W/'recipe/gemini_listen.py';s=script.read_text().replace('else "audio/wav"','else ("audio/flac" if p.endswith(".flac") else "audio/wav")');script.write_text(s)
keys=['untreated','default','warm-bass','lighter-bass'];res=collections.defaultdict(list);wins=collections.Counter()
q='You are a dialogue mixer. reference.flac is an approved voice tone from a different video, comparison only. Each of the four WAV files contains the SAME 30 seconds, level matched, with unknown treatment. Listen to each completely. Rank the finished voice by naturalness, body, clarity and absence of boom, hiss, harshness and chopped endings. Do not prefer processing for its own sake. JSON only: {"scores":{"clip_A.wav":{"score":8,"room":false,"chopped":false,"fault":"..."}},"ship":"clip_A.wav"}. Give all four scores. If differences are not reliable, say so in a confidence field.'
for i in range(5):
 d=O/f'trial{i+1}';d.mkdir(exist_ok=True);rng=random.Random(1310+i);kk=keys.copy();rng.shuffle(kk);mapping=dict(zip('ABCD',kk))
 for a,b in mapping.items():shutil.copyfile(O/(b+'.wav'),d/f'clip_{a}.wav')
 ref=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/reference/muhammad_16x9_voice.flac');shutil.copyfile(ref,d/'reference.flac');(d/'prompt.txt').write_text(q)
 order=list(mapping);rng.shuffle(order)
 r=subprocess.run([sys.executable,str(script),str(d/'prompt.txt'),str(d/'reference.flac')]+[str(d/f'clip_{x}.wav') for x in order],capture_output=True,text=True,env=dict(os.environ,GM='gemini-3.1-pro-preview'))
 (d/'answer.txt').write_text(r.stdout+r.stderr);(d/'map.json').write_text(json.dumps(mapping))
 try:
  ans=json.loads(re.search(r'\{.*\}',r.stdout.split('USAGE')[0],re.S).group())
  for name,v in ans['scores'].items():res[mapping[re.search('clip_([A-D])',name).group(1)]].append(v)
  wins[mapping[re.search('clip_([A-D])',ans['ship']).group(1)]]+=1
  print('trial',i+1,{k:[v['score'] for v in x] for k,x in res.items()},flush=True)
 except Exception as e:print('review parse failed',i+1,str(e),flush=True)
 (O/'trial_summary.json').write_text(json.dumps({'scores':dict(res),'wins':dict(wins)},indent=2))
print('LISTEN COMPLETE',flush=True)
