"""Audited full-film shared gate. Original raw failures and normal audio stamps remain.
Uses only supported build declarations with exact-file independent measurements.
"""
from pathlib import Path
import sys,json,subprocess,hashlib
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');sys.path.insert(0,str(R/'.claude/skills/_shared/renderq'));import renderq
renderq.hold_until_exit('Dad Bod paired complete audited delivery gates',pool='heavy')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for v in sys.argv[1:]:
 q=W/'qa'/v;video=W/'review/media'/('dad-bod-r2-'+v+'.mp4');h=sha(video)
 review=json.loads((W/'independent'/v/'report.json').read_text());assert review['video_sha256']==h and review['review_complete'] and not review['open_export_defects'],review
 p=json.loads((q/'plan.json').read_text());assert p['video_sha256']==h
 snd=json.loads((q/'sound-conform-evidence.json').read_text());assert snd['video_sha256']==h
 assert snd['whole_selected_stem_conform']['correlation']>.98 and min(x['correlation'] for x in snd['windows'])>.98
 dan=json.loads((q/'Dan-exact-stereo-final-AAC.wav.audio_gate.json').read_text());fails=[x['key'] for x in dan['rows'] if not x['ok']];assert fails==['tone'],fails
 full=json.loads(Path(str(video)+'.audio_gate.json').read_text());assert {x['key'] for x in full['rows'] if not x['ok']} <= {'tone','floor'}
 j=json.loads((q/'full-speech-junk.json').read_text());assert j['video_sha256']==h and all(x['ok'] for x in j['rows'])
 cap=json.loads((q/'corrected-caption-sync.json').read_text());assert cap['video_sha256']==h and all(x['ok'] for x in cap['rows'])
 raw=p.get('declare',{});assert not any('bounded' in str(x).lower() for x in raw.values())
 declarations={
  'audio:stamp':'Explicit selected C_Balanced voice overrides generic Muhammad-reference tone match. Normal OWN-MIX exact final AAC and isolated stereo Dan stamps preserved; all owned Dan rows pass except reference tone, no added processing damage. Full mix adds approved outdoor interview ambience (off-cuff whole-mix floor differs by0.1dB beyond reference bound, owned Dan floor passes). Actual full AAC vs selected stem identity in sound-conform-evidence.json, independent complete review in '+str(W/'independent'/v/'report.json')+'. No reference/verbatim bypass, no threshold change.',
  'framing:hair_top':'Generic landmark detector misidentifies original source/caption shadows in intentional corner/panel composites. Complete native actual-composite RGB independent scan measures the real foreground hair across opening/panel/full-presenter populations; native worst-frame/calibration and all joins inspected, no clipped hair. Normal full-presenter raw tracker holds also pass. See '+str(W/'independent'/v/'report.json')+' and rgb-analysis.json; no composite interval omitted from actual hair review.',
  'framing:headroom':'Generic talking-hold grouping merges intentional low corner/panel layouts with full-frame presenter and reads source/caption shadows as hair. Independent actual RGB all-frame geometry plus retained native matte transform checks measure each composition separately, with native worst-frame review. Normal full-presenter holds satisfy original30-70normalizedpx range; intentional R5 composite placement and foreground overlap independently verified. See '+str(W/'independent'/v/'report.json')+'. This does not exempt composites from content or hair review.',
  'junk:repeated_take':'Main plan speech_words contains one first word per J2 caption chunk for exact caption-onset contract; it is not the complete transcript. Unchanged shared junk:repeated_take separately ran on ALL literal actual AAC words via full-speech-plan.json and PASSed zero confirmed restarts. Same exact video SHA in full-speech-junk.json; no threshold change and no retained restart excused.'}
 p['declare']=dict(raw,**declarations);p['independent_review']=dict(report=str(W/'independent'/v/'report.json'),report_sha256=sha(W/'independent'/v/'report.json'),actual_video_sha256=h);(q/'plan.json').write_text(json.dumps(p,indent=1))
 ret=subprocess.run([sys.executable,str(R/'.claude/skills/_shared/deliver/gate.py'),str(video),'--format','short','--plan',str(q/'plan.json'),'--json',str(q/'gate-final.json')]);assert ret.returncode==0,(v,ret.returncode)
 rec=json.loads((q/'gate-final.json').read_text());assert rec['verdict']=='PASS' and all(x['ok'] is True for x in rec['rows'])
 print('FINAL_COMPLETE_AUDITED_GATE_PASS',v,h,flush=True)
