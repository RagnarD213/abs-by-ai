"""RO-21 voice bake-off (copied from RO-24 audio_options24.py; RO-24 locked B-balanced-bass on 2026-10-21) (PRE-RENDER-APPROVAL "run the look and sound bake-off yourself"): the same continuous 26.5 s of the
C1724 lav (the hook take, starts on speech, no pause over 0.6 s), six ways, every one finished by the shared chain's own
finisher to -14.1 LUFS / -1.5 dBTP so they are level matched. Same lav, room and session as Bill Maher (DS-40), whose
Balanced voice Dan approved on 2026-10-20 for that film; it is the starting candidate here, not a lock.

  audio_options24.py [t0] [dur]
"""
import sys, os, subprocess, json, random
W = '/Volumes/Expansion/_edit_work/RO-21'; O = f'{W}/audio/opts'; os.makedirs(O, exist_ok=True)
FF = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
VC = '/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/audio/voice_chain.py'
T0 = float(sys.argv[1]) if len(sys.argv) > 1 else 21.10; D = float(sys.argv[2]) if len(sys.argv) > 2 else 26.5
BAL = 'highpass=f=70,equalizer=f=110:t=q:w=0.8:g=-1.5,equalizer=f=550:t=q:w=0.8:g=1.3,equalizer=f=1100:t=q:w=0.8:g=1.6,equalizer=f=3200:t=q:w=0.8:g=-0.7'
OPEN = 'highpass=f=70,equalizer=f=120:t=q:w=0.8:g=1.5,equalizer=f=450:t=q:w=1:g=-1,equalizer=f=3200:t=q:w=1:g=-1'
NOEXP = 'DS-40 R1 blind listening on this same lav and room reported clipped word tails with the expander; Dan kept the open, no-expander voice there.'
ROOM = 'DS-40 R2 blind listener heard "noticeable room echo" on Balanced (same green-screen room and lav, listening.json); raw room here measures 53-72 ms.'
OPTS = {
    'A-balanced':      dict(eq=BAL, what="Bill Maher's approved voice (same mic, same room): a little less boom, a little more presence. Nothing between words is touched."),
    'B-balanced-bass': dict(eq=BAL + ',equalizer=f=120:t=q:w=0.8:g=3', what="Balanced plus the house bass lift (+3 dB at 120 Hz) that is the standard for our mixes."),
    'D-less-room':     dict(eq=BAL, room=True, what="Balanced plus the light pass that takes some room echo off."),
    'E-untreated':     dict(eq='highpass=f=70', what="The lav as recorded, only the rumble below the voice removed."),
    'F-chain-default': dict(default=True, what="The shared chain's automatic default: tone matched to the reference mix, plus a gate that turns the room down between words."),
}
src = f'{O}/_window.wav'
subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', f'{T0}', '-t', f'{D}', '-i', f'{W}/audio/lav_full.wav', '-c:a', 'pcm_s24le', src], check=True)
done = {}
for k, o in OPTS.items():
    cmd = ['python3', VC, '--in', src, '--pull', 'anull', '--out', f'{O}/{k}.wav', '--work', f'{O}/_{k}', '--target', '-14.1', '--tp', '-1.5', '--oversample', '4']
    if not o.get('default'):
        cmd += ['--eq', o['eq'], '--no-expander-because', NOEXP]
    if o.get('room'):
        cmd += ['--dereverb-because', ROOM]
    r = subprocess.run(cmd, capture_output=True, text=True)
    open(f'{O}/{k}.log', 'w').write(r.stdout + r.stderr)
    assert os.path.exists(f'{O}/{k}.wav'), (k, r.stdout[-500:], r.stderr[-500:])
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', f'{O}/{k}.wav', '-c:a', 'libmp3lame', '-b:a', '192k', f'{O}/{k}.mp3'], check=True)
    subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-i', f'{O}/{k}.wav', '-c:a', 'aac', '-b:a', '256k', f'{O}/{k}.m4a'], check=True)
    done[k] = o['what']; print('built', k, flush=True)
json.dump({'t0': T0, 'dur': D, 'options': done}, open(f'{O}/options.json', 'w'), indent=1)
print('AUDIO OPTIONS DONE')
