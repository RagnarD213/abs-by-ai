from full import R,ROOT,FF,sha,dump
import sys,json,subprocess
import finish,renderq
with renderq.slot('Vacuum phone review copy checks '+','.join(sys.argv[1:] or ['A','B','C']),pool='light',group='SL-11'):
 rows=[]
 for S in (sys.argv[1:] or ['A','B','C']):
  v=R/'review/films'/f'Vacuum-{S}-R1-540p.mp4';d=R/'build'/S;T=json.loads((d/'timeline.json').read_text());fp=str(ROOT/'Media/video_edit/bin/ffprobe');meta=json.loads(subprocess.check_output([fp,'-v','error','-show_streams','-show_format','-of','json',str(v)]));video=next(x for x in meta['streams'] if x['codec_type']=='video');audio=next(x for x in meta['streams'] if x['codec_type']=='audio');assert (video['width'],video['height'])==(540,960);assert abs(float(video['duration'])-T['seconds'])<.04;assert audio['channels']==2 and int(audio['sample_rate'])==48000
  rc=finish.command(['python3',ROOT/'.claude/skills/_shared/audio/audio_gate.py',v,'--reference-mix',d/'his_mix.wav','--verbatim'],d/'phone-audio-check.log');assert rc==0,(S,'phoneaudio');rows.append(dict(short=S,file=str(v),sha256=sha(v),seconds=float(video['duration']),resolution=[540,960],audio_gate=str(v)+'.audio_gate.json'))
 old=R/'phone-review-checks.json';merged={x['short']:x for x in (json.loads(old.read_text()) if old.exists() else [])};merged.update({x['short']:x for x in rows});dump(old,[merged[x] for x in sorted(merged)]);print('PHONE COPIES CHECKED',sys.argv[1:] or ['A','B','C'],flush=True)
