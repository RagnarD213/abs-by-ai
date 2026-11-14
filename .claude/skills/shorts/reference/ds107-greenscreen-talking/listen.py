"""DS-107 R1 sound bake-off (PRE-RENDER-APPROVAL step 3): the four level-matched voices on the same 30 s speech-first passage (film
28.4-58.4, 'You have more stress...' to '...rest of the day'), five blind trials with fresh letters and order, Gemini as the listener
against Dan's reference voice. From DS-55 listen.py."""
from pathlib import Path
import subprocess, json, random, re, os, shutil
W = Path(__file__).resolve().parents[1]; R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); F = R/'Media/video_edit/bin/ffmpeg'
ref = W/'evidence/reference.mp3'
subprocess.run([str(F), '-nostdin', '-v', 'error', '-y', '-i', str(R/'.claude/skills/_shared/audio/reference/muhammad_16x9_voice.flac'), '-t', '12', '-c:a', 'libmp3lame', '-b:a', '160k', str(ref)], check=True)
V = ['house_bass15', 'fitted', 'balanced', 'untreated']; results = []
for i in range(5):
    d = W/f'evidence/listen-{i}'; d.mkdir(exist_ok=True); keys = V[:]; random.Random(107 + i).shuffle(keys); mapping = dict(zip('KLMN', keys)); files = []
    for blind, key in mapping.items():
        dst = d/f'clip-{blind}.mp3'; shutil.copy(W/f'review/media/voice-{key}.mp3', dst); files.append(str(dst))
    q = ('You are a dialogue mixer. Listen to all four SAME 30-second speech-first studio lav recordings (green screen studio), level matched. '
         'The reference is the client\'s preferred voice from a different video. Judge naturalness and professional clarity. Listen for harsh '
         'distortion on loud words, clipped word tails, boomy or excess bass, thin sound, hiss, room echo, speech swallowed into processing. Do not '
         'penalize a natural breath or intentional emphasis. Return JSON only: {"scores":{"clip-K":{"score":1,"fault":"..."}},"best":"clip-K",'
         '"source_defects":[{"time":0,"words":"...","issue":"..."}]}. Score 1-10. All four blind letters must be scored. A source issue common to all is not a processing difference.')
    (d/'prompt.txt').write_text(q); (d/'mapping.json').write_text(json.dumps(mapping))
    run = subprocess.run(['python3', str(W/'recipe/gemini_listen.py'), str(d/'prompt.txt'), str(ref)] + files, capture_output=True, text=True, env=dict(os.environ, GM='gemini-3.1-pro-preview'))
    (d/'response.txt').write_text(run.stdout + run.stderr)
    try:
        raw = run.stdout.split('USAGE')[0]; j = json.loads(re.search(r'\{.*\}', raw, re.S).group())
        scores = {mapping[re.search(r'clip-([KLMN])', k).group(1)]: v for k, v in j['scores'].items()}
        results.append(dict(trial=i, scores=scores, best=mapping[re.search(r'clip-([KLMN])', j['best']).group(1)], source_defects=j.get('source_defects'), usage=run.stdout.split('USAGE')[-1].strip()))
        print(i, {k: v['score'] for k, v in scores.items()}, flush=True)
    except Exception as e:
        results.append(dict(trial=i, error=str(e), out=run.stdout[-400:] + run.stderr[-400:])); print('LISTEN FAILURE', i, str(e), run.stdout[-300:], run.stderr[-300:], flush=True)
    (W/'evidence/listen-results.json').write_text(json.dumps(results, indent=2))
avg = {v: round(sum(r['scores'][v]['score'] for r in results if 'scores' in r)/max(1, sum('scores' in r for r in results)), 2) for v in V}
print('AVERAGE', avg); (W/'evidence/listen-average.json').write_text(json.dumps(avg)); print('LISTEN_DONE', flush=True)
