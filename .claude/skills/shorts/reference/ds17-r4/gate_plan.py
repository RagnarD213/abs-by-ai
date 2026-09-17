from pathlib import Path
import json,hashlib
W=Path(__file__).resolve().parents[1];e=json.loads((W/'edit.json').read_text());v=W/'ds-17_how-to-jump-rope.mp4';sha=hashlib.sha256(v.read_bytes()).hexdigest();fps=30000/1001;opening_end=e['shots'][0]['frames']/fps if e['shots'][0].get('kind')=='opening' else 0;opening_cut=75/fps if opening_end else None
intended="""Jump rope is the best cardio that you can do at home, but most people are doing it wrong. Here's how to go from tripping over the rope to skipping rope like a boxer in just a few minutes. First, don't hop over the rope with two feet. Skip over the rope one foot at a time. It's less impact on your joints and it's easier to push your cardio without tripping on the rope. Skipping over the rope one foot at a time is hard to do at full speed when you first start. So your first time, move the rope slowly and skip over it one foot at a time. Accelerate it gradually, bit by bit, until you're skipping over the rope one foot at a time at full speed. Once you're good at jump roping, do it for two minutes every morning when you wake up to get your blood pumping. Or do two minutes before your workout for a quick cardio warmup. Comment below to let me know how learning jump rope this way worked for you."""
joins=[p['out'] for p in e['pieces'][1:]]+([opening_cut] if opening_cut is not None else [])
covered=[[s['out'],s['out']+s['frames']/fps] for s in e['shots'] if s['kind'] in ('opening','demo')]
plan={'target_seconds':e['duration'],'target_frames':e['frames'],'evidence_contract':{'version':2,'video_sha256':sha},'joins':sorted(joins),'covered':covered,'punch':[[s['out'],s['out']+s['frames']/fps,s.get('level','OPENING' if s.get('kind')=='opening' else 'DEMO')] for s in e['shots']], 'talking_head_windows':[{'beat':[s['out'],s['out']+s['frames']/fps],'rect':[0,310,1080,1610],'motion':'tracking' if s.get('tracking') else 'fixed-wide'} for s in e['shots'] if s['kind']=='talk'], 'captions_ass':str(W/'captions.ass'),'words':[{'w':s} for s in intended.split()],'source_audio':str(W/'untreated.wav'),'source_picture':str(W/'picture.mp4'),'graphics':[{'name':n,'beat':[opening_end,e['duration']],'mov':str(W/('assets/'+n+'.mov'))} for n in ['title-header','wordmark']], 'cards':[], 'real_photos':[], 'ai_inserts':[], 'watch_log':str(W/'logs/watch_pass.json')}
if (W/'finished-asr.json').exists():
 d=json.loads((W/'finished-asr.json').read_text());plan['transcript_words']=[{'w':a['word']} for s in d['segments'] for a in s['words']]
plan['punch_covered']=[s['kind'] in ('opening','demo') for s in e['shots']]
if opening_cut is not None:
 plan['join_notes']=[{'t':opening_cut,'kind':'picture_only','reason':'Intentional side-to-front opening angle change at output frame 75; the continuous dialogue track is not cut here.'}]
plan['banned_source']='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/ad2-nutritionist/clips/app-flow-generate-future-self.mp4'
plan['banned_times']=[26.,30.]
if (W/'caption-evidence/states.json').exists():
 plan['caption_states']=json.loads((W/'caption-evidence/states.json').read_text())
 plan['caption_evidence_note']='Plain white ASS chunks, not individual word highlighting. State onset anchored to first word; image exports retain entire actual cue. Independent finished-audio ASR; no self-comparison.'
 demo_spans=[[s['out'],s['out']+s['frames']/fps] for s in e['shots'] if s['kind']=='demo']
 plan['graphic_regions']=[{'name':'Title header','beat':[opening_end,e['duration']],'rect':[0,0,1080,310]},{'name':'AbsByAI wordmark','beat':[opening_end,e['duration']],'rect':[685,1805,300,70]}]+[{'name':'Full demonstration stage including border','beat':q,'rect':[0,310,1080,1080]} for q in demo_spans]
 plan['speech_words']=[{'w':a['word'],'t':a['start'],'e':a['end']} for ss in d['segments'] for a in ss['words']]
 plan['speech_words_evidence']={'method':'delivered_asr','video_sha256':sha,'source':str(W/'finished-asr.json'),'model':'Whisper base.en, independently run on finished MP4; captions authored from medium.en on voice WAV'}
vdir=W/'review/ctc-validation-r4'
if (vdir/'summary.json').exists():
 val=json.loads((vdir/'summary.json').read_text())
 if val['sha256']==sha:
  plan['speech_words']=json.loads((vdir/'speech-anchors-50.json').read_text())
  plan['speech_words_evidence']={'method':'delivered_asr','video_sha256':sha,'pipeline':'Decoded final audio; recognized transcript + WAV2VEC2_ASR_BASE_960H alignment in11 independent edit-piece windows','scope':'All50caption-chunk first-word onsets, exact full-transcript order; no karaoke claim','full_word_alignment':str(vdir/'speech-words-181.json'),'full_word_alignment_sha256':__import__('hashlib').sha256((vdir/'speech-words-181.json').read_bytes()).hexdigest(),'validation':val}
  plan['transcript_words']=json.loads((vdir/'speech-words-181.json').read_text())
if (W/'logs/negative-events.json').exists():
 neg=json.loads((W/'logs/negative-events.json').read_text())
 if neg['sha256']==sha:plan['negative_events_scan']=neg
(W/'gate-plan.json').write_text(json.dumps(plan,indent=2));print('PLAN',sha)
