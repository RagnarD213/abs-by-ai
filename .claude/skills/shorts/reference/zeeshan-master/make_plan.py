#!/usr/bin/env python3
"""Gate plan for each delivered SL-04 short: python3 make_plan.py A|F <delivered.mp4>
Everything is read out of the build (manifest, pieces, ASS, overlays, layout) and the delivered
file (sha256, delivered-audio ASR), never typed by hand."""
import json, sys, os, subprocess, hashlib, re
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
seg, video = sys.argv[1], os.path.abspath(sys.argv[2])
FF = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js')))"], cwd=HERE))['FF']
FPS = 30000 / 1001
FONTS = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./config.js').FONTS))"], cwd=HERE))
L = json.load(open(f'{HERE}/layout.json'))
man = [m for m in json.load(open(f'{HERE}/shots/manifest.json')) if m['seg'] == seg]
S = json.loads(subprocess.check_output(['node', '-e', "console.log(JSON.stringify(require('./segments.js').SEGMENTS))"], cwd=HERE))
pieces = next(s for s in S if s['id'] == seg)['pieces']
sha = hashlib.sha256(open(video, 'rb').read()).hexdigest()
frames = sum(m['frames'] for m in man); dur = frames / FPS
G = f'{HERE}/gate/{seg}'; os.makedirs(f'{G}/cap', exist_ok=True)

# ---- captions: one RGBA state per cue, rendered by the same libass + fonts as the burn ------
ass = f'{HERE}/build/{seg}/{seg}.ass'
lines = open(ass).read().split('\n')
head = [l for l in lines if not l.startswith('Dialogue:')]
def secs(s):
    h, m, x = s.split(':'); return int(h) * 3600 + int(m) * 60 + float(x)
states = []
lines_d = [l for l in lines if l.startswith('Dialogue:')]
for i, l in enumerate(lines_d):
    f = l.split(',', 9)
    a, b, txt = secs(f[1]), secs(f[2]), f[9]
    one = '\n'.join(head).replace('[Events]\n', '[Events]\n') + '\n' + ','.join([f[0], '0:00:00.00', '0:00:05.00'] + f[3:]) + '\n'
    p = f'{G}/cap/cue{i:03d}.ass'; open(p, 'w').write(one)
    png = f'{G}/cap/cue{i:03d}.png'
    subprocess.run([FF, '-v', 'error', '-y', '-f', 'lavfi', '-i', 'color=c=black@0.0:s=1080x1920:d=1,format=rgba',
                    '-vf', f"subtitles={p}:fontsdir='{FONTS}':alpha=1",
                    '-frames:v', '1', png], check=True)
    word = re.sub(r'\{[^}]*\}', '', txt).split()[0]
    states.append({'name': f'cap{i:03d}', 'beat': [round(a, 4), round(b, 4)], 'image': png,
                   'image_sha256': hashlib.sha256(open(png, 'rb').read()).hexdigest(),
                   'rect': [0, 0, 1080, 1920], 'word': word})

# ---- delivered-audio words ------------------------------------------------------------------
asr = json.load(open(f'{HERE}/gate/{seg}_asr_clean.json'))['chunks']
speech = json.load(open(f'{HERE}/gate/{seg}_speech_ctc.json'))   # gate/ctc_delivered.py
assert len(speech) >= 0.97 * len([c for c in asr if c['text'].strip()]), 'CTC lost words'
intended = json.loads(subprocess.check_output(['node', '-e',
    "const {segWords}=require('./captions.js');const {SEGMENTS}=require('./segments.js');"
    f"console.log(JSON.stringify(segWords(SEGMENTS.find(s=>s.id==='{seg}'))))"], cwd=HERE))
words = [{'w': w['text'].strip(), 't': round(w['timestamp'][0], 3), 'e': round(w['timestamp'][1], 3)} for w in intended]

# ---- picture geometry ------------------------------------------------------------------------
joins, off = [], 0.0
for p in pieces[:-1]:
    off += p['end'] - p['start']; joins.append(round(off, 4))
beat = lambda m: [round(m['outStart'], 4), round(m['outStart'] + m['frames'] / FPS, 4)]
talk = [m for m in man if m['t'] == 'talk']
cards = [m for m in man if m['t'] == 'card']
LEVEL = {'zoom': 'NEAR', 'mid': 'MID', 'full': 'FAR'}
thw = [{'name': m['name'], 'beat': beat(m), 'rect': [0, L['dropTop'], 1080, 1920 - L['dropTop']], 'motion': 'fixed-wide'} for m in talk]
# every shot in timeline order; a card is its own level and marks the pair covered (jump_cut
# only compares ADJACENT visible segments). A talk shot on Zeeshan's MEDIUM camera is its own level.
MEDIUM = {'A-p0-s01', 'A-p1-s01', 'F-p1-s01'}
def level(m):
    if m['t'] == 'card': return 'CARD'
    src_medium = m.get('cam') == 'medium' or (482.024 <= m['absStart'] < 487.2)
    return ('MEDIUM-' if src_medium else '') + LEVEL[m['win']]
punch = [beat(m) + [level(m)] for m in man]
punch_cov = [m['t'] == 'card' for m in man]
regions = [{'name': 'title_band', 'beat': [0.0, round(dur, 4)], 'rect': [0, 0, 1080, L['dropTop']]},
           {'name': 'wordmark', 'beat': [0.0, round(dur, 4)], 'rect': [L['wordmark']['x'], L['wordmark']['y'], 420, 60]}]
graphics = []
for m in cards:
    cc = m.get('cardCrop', [0, 1, 0, 1]); w = 1920 * (cc[1] - cc[0]); h = 1080 * (cc[3] - cc[2])
    ch = round(h * 1080 / w)
    regions.append({'name': f"card_{m['name']}", 'beat': beat(m), 'rect': [0, m.get('cardY', L['card']['y']), 1080, ch]})
    chip = f"{HERE}/assets/chip-{m['name']}.png"
    if os.path.exists(chip):
        cw, chh = Image.open(chip).size
        regions.append({'name': f"chip_{m['name']}", 'beat': beat(m), 'image': chip, 'pos': [(1080 - cw) // 2, L['card']['chipY']]})
OV = json.load(open(f'{HERE}/overlays.json')).get(seg, [])
for o in OV:
    chip = f"{HERE}/assets/chip-{o['id']}.png"; cw, chh = Image.open(chip).size
    regions.append({'name': o['id'], 'beat': [o['t0'], o['t1']], 'image': chip, 'pos': [(1080 - cw) // 2, o['y']]})
covered = []
for j in joins:
    # the shot the join falls in: a card, a picture continuing across it (the L-cut), or a
    # framing change on the join itself -- all hide it
    for m in man:
        a, b = beat(m)
        if a - 0.05 <= j <= b + 0.05:
            covered.append([a, b]); break

# ---- chunk-onset scope (the DS-17 method): align the FULL caption word stream to the FULL
# delivered-audio word stream in order, then give the gate, for each caption chunk, the delivered
# word its FIRST word matched. Matching chunk-first words alone against every spoken word lets a
# common word ("is", "the", "your") land on the wrong occurrence seconds away.
import difflib
nz = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
cap_tokens = []                     # (norm word, chunk index, is_first)
for ci, st in enumerate(states):
    txt = re.sub(r'\{[^}]*\}', '', lines_d[ci].split(',', 9)[9]).replace('\\N', ' ')
    for k, wd in enumerate(txt.split()):
        if nz(wd): cap_tokens.append((nz(wd), ci, k == 0))
sp_tokens = [(nz(s['w']), i) for i, s in enumerate(speech) if nz(s['w'])]
sm = difflib.SequenceMatcher(None, [x[0] for x in cap_tokens], [x[0] for x in sp_tokens], autojunk=False)
first_match = {}
for a0, b0, n in sm.get_matching_blocks():
    for j in range(n):
        tok = cap_tokens[a0 + j]
        if tok[2]: first_match[tok[1]] = speech[sp_tokens[b0 + j][1]]
chunk_speech = [first_match[ci] for ci in range(len(states)) if ci in first_match]
json.dump(speech, open(f'{G}/speech_words_all.json', 'w'))
print(f'chunk onsets matched in full-stream order: {len(chunk_speech)}/{len(states)}')

plan = {
    'target_seconds': round(dur, 6), 'target_frames': frames,
    'joins': joins, 'covered': covered, 'punch': punch, 'punch_covered': punch_cov,
    'graphics': graphics, 'graphic_regions': regions, 'ai_inserts': [], 'real_photos': [], 'cards': [],
    '_cards_why': 'no full-screen card: every card is an inset stage (y >= 310) with the caption band below it; declared as graphic_regions so the clearance is measured',
    'talking_head_windows': thw,
    'captions_ass': ass,
    'evidence_contract': {'version': 2, 'video_sha256': sha},
    'caption_states': states,
    'speech_words': chunk_speech, 'speech_words_evidence': {'method': 'delivered_asr', 'video_sha256': sha, 'scope': 'one delivered word per caption chunk: the word the chunk\'s FIRST word matches when the full caption text is aligned to the full delivered transcript in order (DS-17 method); every delivered word is in full_word_alignment', 'full_word_alignment': f'{G}/speech_words_all.json', 'pipeline': 'delivered file audio -> Whisper (Replicate incredibly-fast-whisper) transcript -> WAV2VEC2_ASR_BASE_960H CTC forced alignment in windows split at the ASR long gaps (gate/ctc_delivered.py). Caption times come from a different pass: SOURCE-master Whisper + VAD onset correction.'},
    'words': words, 'transcript_words': [{'w': s['w']} for s in speech], '_junk_words': speech, '_junk_words_src': 'plan:full delivered-audio words (delivered ASR + CTC), bound to this sha; speech_words carries only the chunk-onset subset for captions:sync',
    'source_audio': f'{HERE}/build/{seg}/his_mix.wav',
    'banned_source': '/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/02 App Screen Recordings and Screenshots/app-flow-generate-future-self.mp4',
    'banned_times': [26.5, 27.5, 29.5, 31.0],
    'watch_log': f'{G}/logs/watch_pass.json',
}
if os.path.exists(f'{G}/negative_events_scan.json'):
    plan['negative_events_scan'] = json.load(open(f'{G}/negative_events_scan.json'))
if os.path.exists(f'{G}/declare.json'):
    plan['declare'] = json.load(open(f'{G}/declare.json'))
json.dump(plan, open(f'{G}/plan.json', 'w'), indent=1)
print(f'{G}/plan.json  frames {frames}  joins {joins}  covered {covered}  states {len(states)}  speech {len(speech)}')
