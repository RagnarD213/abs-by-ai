"""One queued full-film build and current unchanged shared measurements. Failures stay raw."""
from pathlib import Path
import json,subprocess,sys,os,time
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');v=sys.argv[1];q=W/'qa'/v;q.mkdir(parents=True,exist_ok=True);FF=str(R/'Media/video_edit/bin/ffmpeg');out=W/'review/media'/('dad-bod-r2-'+v+'.mp4');out.parent.mkdir(parents=True,exist_ok=True)
def run(label,cmd,allow_fail=False):
 print('STAGE_START',v,label,flush=True);ret=subprocess.run(list(map(str,cmd)));print('STAGE_END',v,label,ret.returncode,flush=True)
 state=q/'pipeline-state.json';state.write_text(json.dumps(dict(stage=label,returncode=ret.returncode,at=time.time(),candidate=str(out)),indent=2))
 if ret.returncode and not allow_fail:raise SystemExit(ret.returncode)
P=sys.executable
run('complete_render',[P,W/'recipe/render_r2.py',v,'--out',out])
run('full_plan_and_decode',[P,W/'recipe/qa_full_r2.py','prep',v])
run('normal_exact_aac_gate',[P,R/'.claude/skills/_shared/audio/audio_gate.py',out,'--untreated',W/v/'mix-untreated.wav','--ab',q/'audio-ab.wav'],True)
run('exact_Dan_AAC_extraction',[FF,'-v','error','-nostdin','-y','-ss',str(469/(30000/1001)),'-i',out,'-vn','-ac','1','-ar','48000','-c:a','pcm_s24le',q/'Dan-from-final-AAC.wav'])
run('normal_exact_Dan_AAC_gate',[P,R/'.claude/skills/_shared/audio/audio_gate.py',q/'Dan-from-final-AAC.wav','--untreated',W/v/'audio/lav.wav'],True)
run('full_watch',[P,W/'recipe/qa_full_r2.py','watch',v])
run('actual_caption_states',[P,W/'recipe/caption_states_r2.py',v])
run('full_actual_delivered_asr',[P,W/'recipe/qa_full_r2.py','asr',v])
run('independent_acoustic_model',[P,W/'recipe/ctc_delivered_r2.py',v])
run('ordered_chunk_projection',[P,W/'recipe/project_chunk_onsets_r2.py',v])
run('raw_full_shared_gate',[P,W/'recipe/qa_full_r2.py','gate',v])
print('FULL_CANDIDATE_MEASURED_NOT_YET_INDEPENDENTLY_CLEARED',v,flush=True)
