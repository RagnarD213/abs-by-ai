"""DS-76 R1 complete Short: How To Do Pull-Ups (And What To Do If You Can't Do One).
Pieces/words from prepare.py, cutaways/graphics from records/visual-plan.json, presenter grade from look-options.json (recommended F).
Layout follows Dan's approved Hamstring Curls (DS-84) R2/R3: large two-line title over every exercise window, small header on Dan.
Every rgb24 pipe is encoded with an explicit BT.709 matrix (DS-84 R3 had to repair a default-601 encode)."""
from pathlib import Path
import sys, os, json, subprocess, numpy as np
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = R/'Media/video_edit/bin/ffmpeg'
os.environ['PATH'] = str(F.parent)+':'+os.environ['PATH']; sys.path.insert(0, str(R/'.claude/skills/_shared/renderq')); import renderq
renderq.hold_until_exit('DS-76 R1 complete Short', pool='heavy', group='DS-76')
sys.path.insert(0, str(R/'.claude/skills/_shared/hyperframes')); import vertical as V, composite as C; C.FF = str(F)
fps = 30000/1001; fr = lambda t: round(t*fps)
P = json.load(open(W/'edit-plan.json')); VP = json.load(open(W/'records/visual-plan.json')); L = json.load(open(W/'records/library.json'))
look = json.load(open(W/'look-options.json')); GK = next((x for x in sys.argv[1:] if not x.startswith('--')), None) or look['recommended']['colour']; grade = look['colours'][GK]['vf']
N = P['frames']; dur = N/fps; Q = W/'cache'; O = W/'review'; D = O/'media'; Q.mkdir(exist_ok=True); D.mkdir(parents=True, exist_ok=True)
TAG = ['-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709']
def ff(a): subprocess.run([str(F), '-nostdin', '-v', 'error', '-y']+list(map(str, a)), check=True)
def enc(): return ['-c:v', 'libx264', '-threads', os.environ.get('RENDERQ_CORES', '4'), '-crf', '18', '-preset', 'fast']+TAG
def rgb_in(out, n): return subprocess.Popen([str(F), '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-framerate', '30000/1001', '-i', '-', '-an',
                                            '-frames:v', str(n), '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p']+enc()+[str(out)], stdin=subprocess.PIPE)
def film(s):
    """C1882 source second -> film second, through the kept pieces (a time in a removed gap snaps to the next piece)."""
    for p in P['pieces']:
        if s < p['source_in']: return p['out']
        if s <= p['source_out']: return p['out']+s-p['source_in']
    return dur
# ---- timeline in film frames
assets = []
for u in VP['assets']:
    a, b = fr(film(u['a'])), fr(film(u['b'])); x, y, cw, ch = u['crop']; bh = 1532 if u.get('fullscreen') else round(1056*ch/cw)
    if u.get('fullscreen'): assert abs(cw/ch-1080/1920) < 0.002, (u['id'], 'full-screen crop must be 9:16')
    assert 388+bh <= 1920, (u['id'], 'window runs off the frame')
    assert u['start']+(b-a)/fps <= L[u['lib']]['duration']+0.02, (u['id'], 'library master too short')
    assets.append(dict(u, fa=a, fb=b, frames=b-a, box=[0, 0, 1080, 1920] if u.get('fullscreen') else [12, 388, 1068, 388+bh], film=[a/fps, b/fps]))
gfx = []
for g in VP['graphics']:
    a, b = fr(film(g['a'])), fr(film(g['b'])); gfx.append(dict(g, fa=a, fb=b, film=[a/fps, b/fps]))
for i, u in enumerate(assets):
    for v in assets[i+1:]: assert u['fb'] <= v['fa'] or v['fb'] <= u['fa'], ('overlap', u['id'], v['id'])
# ---- HyperFrames graphics (shared templates only)
hf = W/'hf'; scenes = []; seen = {}
for u in assets:
    if u.get('fullscreen'): continue
    key = tuple(u['box'])
    if key not in seen:
        gid = f"M{len(seen)+1:02d}"; seen[key] = gid; md = max(v['frames'] for v in assets if tuple(v['box']) == key)/fps
        scenes.append((V.HERE/'media-card/media-card.template.htm', dict(id=gid, dur=round(md+0.1, 3), canvas=[1080, 1920], hole=[12, 388, 1056, u['box'][3]-388], radius=20), ()))
    u['plate'] = str(hf/f"renders/{seen[key]}.mov")
big = VP['headers']['large']
# back-to-back windowed clips share one continuous large title (two watch judges: it blinked off and retyped at each clip-to-clip cut)
grp_start = {}
for u in assets:
    prev = next((v for v in assets if v['fb'] == u['fa'] and not v.get('fullscreen')), None)
    u['title_off'] = 0 if u.get('fullscreen') or prev is None else prev['title_off']+prev['frames']
head = dict(id='H01', dur=round(max(u['title_off']+u['frames'] for u in assets if not u.get('fullscreen'))/fps+0.1, 3), canvas=[1080, 350], drift=-2, line_px=118, accent=[44, 330, 64],
            lines=[dict(x=round((1080-V.H.text_w(s, 118))/2), y=y, s=s) for s, y in zip(big, [8, 164])])
small = dict(id='T01', dur=round(dur+0.1, 3), canvas=[1080, 90], drift=-2, line_px=40, accent=[44, 75, 64], lines=[dict(x=44, y=10, s=VP['headers']['small'])])
scenes += [(V.HERE/'title-card/title-card.template.htm', head, ()), (V.HERE/'title-card/title-card.template.htm', small, ())]
V.build(scenes, hf, render=True, snap=2)
manifest = []
for g in gfx:
    d = (g['fb']-g['fa'])/fps
    if g['kind'] == 'glass':
        ss, m = V.lt_scenes(dict(id=g['id'], a=0, b=d, topic=g['topic'], parts=[[g['point'], 0]], top_y=1660, drift=-3)); V.build(ss, hf, render=True, snap=2)
        manifest.append(dict(id=g['id'], a=g['film'][0], b=g['film'][1], kind='glass', mov=str(hf/f"renders/{g['id']}.mov"), mask=str(hf/f"renders/{g['id']}_mask.mov"), band=m['band'], box=m['box']))
    else:
        ss, m = V.title_scenes(g['id'], 0, d, g['eyebrow'], g['headline'], [r[0] for r in g['rows']])
        for row, (_, t) in zip(ss[0][1]['rows'], g['rows']): row['t'] = round(film(t)-g['film'][0], 3)
        V.build(ss, hf, render=True, snap=2); manifest.append(dict(id=g['id'], a=g['film'][0], b=g['film'][1], kind='opaque', mov=str(hf/f"renders/{g['id']}.mov")))
print('GRAPHICS_READY', flush=True)
# ---- presenter pieces, graded, native portrait 2160x3840 -> 1080x1920 (Original Portrait)
parts = []
for j, p in enumerate(P['pieces']):
    v = Q/f'{GK}-{j}.mp4'
    if not v.exists(): ff(['-ss', p['source_in'], '-i', p['source'], '-an', '-frames:v', p['frames'], '-vf', grade+',scale=1080:1920:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv', '-r', '30000/1001']+enc()+[v])
    parts.append(v)
cl = Q/f'concat-{GK}.txt'; cl.write_text(''.join(f"file '{p}'\n" for p in parts)); base = Q/f'{GK}-base.mp4'; ff(['-f', 'concat', '-safe', 0, '-i', cl, '-c', 'copy', base])
# ---- each insert: library master (approved C grade, untouched) in its window, plate + large header over it
for u in assets:
    out = Q/f"{u['id']}.mp4"
    if out.exists() and '--fresh' not in sys.argv: continue
    if u.get('fullscreen'):   # (Dan, R2) the clip fills the 9:16 frame; no window, plate or large title
        x, y, cw, ch = u['crop']
        ff(['-ss', u['start'], '-i', L[u['lib']]['path'], '-an', '-frames:v', u['frames'], '-vf', f"crop={cw}:{ch}:{x}:{y},{u['grade_fix']+',' if u.get('grade_fix') else ''}scale=1080:1920:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv", '-r', '30000/1001']+enc()+[out])
        print('CLIP_READY', u['id'], 'full screen', flush=True); continue
    bw = 1056; bh = u['box'][3]-388; x, y, cw, ch = u['crop']; nf = u['frames']
    rd = subprocess.Popen([str(F), '-v', 'error', '-ss', str(u['start']), '-i', L[u['lib']]['path'], '-frames:v', str(nf), '-vf',
                           f"crop={cw}:{ch}:{x}:{y},{u['grade_fix']+',' if u.get('grade_fix') else ''}"+f'scale={bw}:{bh}:in_color_matrix=bt709:in_range=tv,format=rgb24', '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    en = rgb_in(out, nf); pt = C._Track(u['plate'], 0, nf, True, (1080, 1920)); ht = C._Track(str(hf/'renders/H01.mov'), 0, u['title_off']+nf, False, (1080, 350))
    for i in range(nf):
        buf = rd.stdout.read(bw*bh*3); assert len(buf) == bw*bh*3, (u['id'], i, 'source exhausted')
        f = np.zeros((1920, 1080, 3), np.uint8); f[388:388+bh, 12:1068] = np.frombuffer(buf, np.uint8).reshape(bh, bw, 3)
        f = C.over(f, pt.frame(i)); f[:350] = ht.frame(u['title_off']+i); en.stdin.write(np.ascontiguousarray(f).tobytes())
    en.stdin.close(); assert en.wait() == 0; rd.stdout.close(); rd.wait(); print('CLIP_READY', u['id'], flush=True)
# ---- full picture
video = Q/f'picture-{GK}.mp4'
if not video.exists() or '--fresh' in sys.argv:
  en = rgb_in(video, N)
  comp = C.Compositor(manifest, wh=(1080, 1920)); tt = C._Track(str(hf/'renders/T01.mov'), 0, N, False, (1080, 90))
  trs = {u['id']: C._Track(str(Q/f"{u['id']}.mp4"), u['fa'], u['frames'], False, (1080, 1920)) for u in assets}
  for i, f in enumerate(C.reader(str(base), n=N, wh=(1080, 1920))):
      u = next((u for u in assets if u['fa'] <= i < u['fb']), None)
      if u:
          f = trs[u['id']].frame(i)
          if u.get('fullscreen'): f = comp.apply(f.copy(), i)   # the bottom glass title sits over the full-screen clip
      else:
          f = comp.apply(f.copy(), i)
          f[:90] = tt.frame(i)
      en.stdin.write(np.ascontiguousarray(f).tobytes())
  en.stdin.close(); assert en.wait() == 0
# ---- captions: one-line chunks, footer; above G01; none over the full-screen G02 card (it carries its own words)
words = json.load(open(W/'records/words.json')); chunks, cur = [], []
for w in words:
    if cur and (len(' '.join(x['w'] for x in cur+[w])) > 22 or len(cur) >= 4 or cur[-1]['w'][-1:] in '.?'): chunks.append(cur); cur = []
    cur.append(w)
if cur: chunks.append(cur)
def ts(t, srt=False):
    ms = round(t*1000); h = ms//3600000; m = ms//60000 % 60; s = ms//1000 % 60
    return f'{h:02d}:{m:02d}:{s:02d},{ms%1000:03d}' if srt else f'{h}:{m:02d}:{s:02d}.{ms%1000//10:02d}'
glass = sorted([g['a'], g['b']] for g in manifest if g['kind'] == 'glass'); g2 = next([g['a'], g['b']] for g in manifest if g['id'] == 'G02')
ass = ('[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n'
       'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
       'Style: Default,Arial,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,1,2,45,45,34,1\n\n[Events]\n'
       'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
srt, cues = [], []
for i, c in enumerate(chunks):
    a = max(0, c[0]['t0']); b = min(dur, c[-1]['t1']); b = max(b, min(dur, a+.35))
    if i+1 < len(chunks): b = min(max(b, min(chunks[i+1][0]['t0'], a+1.2)), chunks[i+1][0]['t0'])
    text = ' '.join(w['w'] for w in c); srt.append(f'{len(srt)+1}\n{ts(a, True)} --> {ts(b, True)}\n{text}\n')
    a2, b2 = a, b
    if a2 < g2[1] and b2 > g2[0]:
        if a2 >= g2[0]: a2 = max(a2, g2[1])
        else: b2 = min(b2, g2[0])
        if b2-a2 < 0.2: continue
    # above a glass bar only while it is on screen (split a phrase that straddles its edges)
    pts = sorted({a2, b2}|{t for g in glass for t in g if a2 < t < b2})
    for s0, s1 in zip(pts, pts[1:]):
        if s1-s0 < 0.04: continue
        yy = 1605 if any(g[0] <= (s0+s1)/2 < g[1] for g in glass) else 1710
        ass += f'Dialogue: 0,{ts(s0)},{ts(s1)},Default,,0,0,0,,{{\\pos(540,{yy})}}{text}\n'; cues.append(dict(a=s0, b=s1, text=text, y=yy))
NAME = "How To Do Pull-Ups - DS-76 R2"
(W/'captions.ass').write_text(ass); (O/f'{NAME}.srt').write_text('\n'.join(srt)); (W/'records/caption-cues.json').write_text(json.dumps(cues, indent=2))
master = O/f'{NAME} - 1080p.mp4'
ff(['-i', video, '-i', W/'audio/voice-selected.wav', '-map', '0:v', '-map', '1:a', '-frames:v', N, '-vf', f"scale=in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,ass={W}/captions.ass,format=yuv420p"]
   + enc()+['-c:a', 'aac', '-b:a', '192k', '-ar', 48000, '-ac', 2, '-movflags', '+faststart', master])
phone = O/f'{NAME} - REVIEW 540p.mp4'
ff(['-i', master, '-vf', 'scale=540:960:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv', '-c:v', 'libx264', '-threads', 2, '-crf', 20, '-preset', 'fast', '-pix_fmt', 'yuv420p']+TAG+['-c:a', 'copy', '-movflags', '+faststart', phone])
stills = {}
for u in assets: stills[u['id']] = (u['fa']+u['fb'])/2/fps
for g in manifest: stills[g['id']] = g['a']+min(4.0, (g['b']-g['a'])*0.8)
stills['P0'] = 7.0; stills['CTA'] = dur-2.0
for k, t in stills.items(): ff(['-ss', round(t, 3), '-i', master, '-frames:v', 1, '-vf', 'scale=540:960:in_color_matrix=bt709:in_range=tv', D/f'{k}.jpg'])
(W/'records/assembly.json').write_text(json.dumps(dict(duration=dur, frames=N, grade_key=GK, grade=grade, assets=assets, graphics=manifest, audio=str(W/'audio/voice-selected.wav'),
     master=str(master), phone=str(phone), stills=stills, presenter_crop='Original Portrait [0,0,2160,3840]', caption_mode='burned one-line + SRT sidecar'), indent=2, default=str))
print('BUILD_DONE', round(dur, 3), flush=True)
