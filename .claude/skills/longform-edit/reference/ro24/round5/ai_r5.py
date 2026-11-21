"""RO-24 round 5 AI motion inserts: each approved Flow take (clipcheck + fresh frame-reviewer PASS on the frames used,
checked here with require_pass) cut to its window, retimed to the slot, scaled to 1920x1080 at 30000/1001 with the round 2
AI-GENERATED chip, as an opaque full-screen item. Writes round5/ai/inserts/<ID>.mp4 and round5/ai_inserts.json for facts_r5.py.
  python3 ai_r5.py [--only A3,A4]"""
import json, subprocess, sys, pathlib
P = '/Users/danielrose/Projects/Claude/Projects/Abs By AI'
sys.path.insert(0, f'{P}/.claude/skills/_shared/framecheck'); from clipcheck import require_pass
R5 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round5'); V = R5 / 'ai/veo'; O = R5 / 'ai/inserts'; O.mkdir(parents=True, exist_ok=True)
FF = f'{P}/Media/video_edit/bin/ffmpeg'; FPS = 30000 / 1001; TF = 24.0
CHIP = '/Volumes/Expansion/_edit_work/RO-24/round2/broll/ai_chip.png'
def require_still(png):                                          # a still shot needs the frame gate's PASS stamp and a fresh reviewer's PASS
    st = json.load(open(png + '.framecheck.json')); rv = pathlib.Path(png).parent / 'framecheck' / (pathlib.Path(png).stem + '.review.md')
    assert st.get('verdict') == 'PASS', (png, 'frame gate verdict', st.get('verdict'))
    import hashlib; h = hashlib.sha256(open(png, 'rb').read()).hexdigest()
    assert h in (st.get('start_sha256'), st.get('end_sha256')), (png, 'changed since it was gated')
    assert rv.exists() and 'VERDICT: PASS' in rv.read_text(), (png, 'no PASS review', rv)
def fr(t): return round(round(t * FPS) / FPS, 4)                 # snap a film time to a frame edge
# id: [(take, f0, f1)] shots in order, slot (film seconds, round 5), what it replaces, the line
CLIPS = {
 'A3': dict(shots=[('A3-flow-t1.mp4', 18, 92)], a=133.40, b=136.45, replaces=[],
            note="AI A3 (Flow Veo 3.1 Fast, approved frames): the spooked newspaper reader over 'Stories like this are used to scare people out of taking Zepbound'"),
 'A4': dict(shots=[('A4-flow-t1.mp4', 12, 100)], a=180.35, b=183.95, replaces=[],
            note="AI A4: the waiter's pasta slid away over 'He said he stays away from the bread, the pasta, and the rice'; the Fat Joe lower third G04 sits over it from 181.7"),
}
OVR = R5 / 'ai/clips_override.json'
if OVR.exists(): CLIPS.update(json.load(open(OVR)))
only = set(sys.argv[sys.argv.index('--only') + 1].split(',')) if '--only' in sys.argv else None
out_p = R5 / 'ai_inserts.json'; done = {x['id']: x for x in json.load(open(out_p))} if out_p.exists() else {}
for cid, c in CLIPS.items():
    if only and cid not in only: continue
    cx = c.get('chip_x', 0)                                     # chip offset: a clip under a top-left card (A8 under G12) moves it right
    a, b = fr(c['a']), fr(c['b']); n_out = int(round((b - a) * FPS))
    src_s = sum((sh[2] - sh[1] + 1) / TF for sh in c['shots'] if sh[0] != 'still') or 1; k = (b - a) / src_s   # >1 slows, <1 speeds
    parts = []
    edges = [a] + [fr(t) for t in c.get('cuts', [])] + [b] if c.get('cuts') else None   # optional film-time shot cuts: each shot retimed to its own slot
    for i, sh in enumerate(c['shots']):
        pp = O / f'{cid}_{i}.mp4'
        if sh[0] == 'still':                                   # ['still', png, zoom_end, focus_x, focus_y]: slow push-in on a gated, reviewed AI frame
            _, png, z1, fx, fy = sh; require_still(png)
            n_i = int(round((edges[i + 1] - edges[i]) * FPS)) if i < len(c['shots']) - 1 else n_out - sum(p[1] for p in parts)
            vf = (f"[0:v]scale=7680:4320:flags=lanczos,zoompan=z='1+{z1 - 1:.4f}*on/{n_i - 1}':x='(iw-iw/zoom)*{fx}':y='(ih-ih/zoom)*{fy}'"
                  f":d={n_i}:s=1920x1080:fps=30000/1001,setsar=1[v];[v][1:v]overlay={cx}:0[o]")
            subprocess.run([FF, '-y', '-v', 'error', '-nostdin', '-loop', '1', '-i', png, '-i', CHIP, '-filter_complex', vf, '-map', '[o]',
                            '-frames:v', str(n_i), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                            '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', str(pp)], check=True)
            parts.append((pp, n_i)); continue
        take, f0, f1 = sh
        require_pass(str(V / take), frames=(f0, f1))
        if edges: k = (edges[i + 1] - edges[i]) / ((f1 - f0 + 1) / TF)
        n_i = int(round((f1 - f0 + 1) / TF * k * FPS)) if i < len(c['shots']) - 1 else n_out - sum(p[1] for p in parts)
        vf = (f"[0:v]trim=start_frame={f0}:end_frame={f1 + 1},setpts=(PTS-STARTPTS)*{k:.5f},fps=30000/1001,"
              f"scale=1920:1080:flags=lanczos,setsar=1[v];[v][1:v]overlay={cx}:0[o]")
        subprocess.run([FF, '-y', '-v', 'error', '-nostdin', '-i', str(V / take), '-i', CHIP, '-filter_complex', vf, '-map', '[o]',
                        '-frames:v', str(n_i), '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                        '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', str(pp)], check=True)
        parts.append((pp, n_i))
    mov = O / f'{cid}.mp4'
    if len(parts) == 1: parts[0][0].replace(mov)
    else:
        lst = O / f'{cid}.txt'; lst.write_text(''.join(f"file '{p}'\n" for p, _ in parts))
        subprocess.run([FF, '-y', '-v', 'error', '-nostdin', '-f', 'concat', '-safe', '0', '-i', str(lst), '-c', 'copy', str(mov)], check=True)
    done[cid] = dict(id=cid, a=a, b=b, mov=str(mov), replaces=c['replaces'], trims=c.get('trims', {}), note=c['note'], speed=round(1 / k, 3), cuts=c.get('cuts', []),
                     shots=[dict(still=sh[1], push=sh[2:]) if sh[0] == 'still' else dict(take=sh[0], frames=sh[1:]) for sh in c['shots']])
    print(cid, f'{a:.3f}-{b:.3f}', n_out, 'frames, speed', round(1 / k, 3), flush=True)
json.dump(sorted(done.values(), key=lambda x: x['a']), open(out_p, 'w'), indent=1)
