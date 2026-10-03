#!/usr/bin/env python3
"""One isolated RO-17 graphics proof. Does not write to RO-17 or export a full film.
Plan: same four snack names and calorie copy, reveals on mapped words.
Both comparison players use the identical clean presenter base, fixed side layout,
and identical excerpt audio. Original draft excerpt is also linked for provenance.
Usage: ro17_hyperframes.py plan|render|finish --out /Volumes/.../proof
"""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'scripts/video'))
import hyperframes_graphics as H
C = H.module('composite')
B = H.module('hfbuild').B
SOURCE = Path('/Volumes/Extreme/_edit_work/RO-17')
A = 338.136; Z = 398.123
F0 = C.fr(A); F1 = C.fr(Z); N = F1 - F0
FF = C.FF


def dump(path, data): path.write_text(json.dumps(data, indent=2) + '\n')
def run(cmd): subprocess.run([str(x) for x in cmd], check=True)
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda:f.read(4*1024*1024), b''): h.update(b)
    return h.hexdigest()


def plan(out):
    out.mkdir(parents=True, exist_ok=True)
    words = [dict(w=w['word'].strip(), t0=w['start'], t1=w['end']) for w in json.loads((SOURCE / 'recipe/mapped-words.json').read_text())]
    dump(out / 'words_out.json', words)
    # Empty heading retains the old graphic's exact four food names, without new copy.
    p = [dict(id='alternatives', kind='l3', t0=340.356, t1=390.21, heading=[],
              points=['SARDINES', 'HARD-BOILED EGGS', 'ROTISSERIE CHICKEN', 'CHIPOTLE PROTEIN CUP'],
              reveal=['Sardines A can', 'hard boiled eggs', 'rotisserie chicken', 'the protein comes from Chipotle'],
              start='Here\'s what I eat', end='the chicken one'),
         dict(id='chipotle', kind='lt', t0=390.21, t1=398.123, topic='CHIPOTLE PROTEIN CUP',
              point='$7', parts=[['$7', '7']], start='the chicken one', end='you get hungry')]
    dump(out / 'plan_resolved.json', p)
    # Actual source shot joins. Card edges have no nearby join, so both proof players
    # retain the same fixed side layout for the whole excerpt, avoiding a fake reframe cut.
    shots = json.loads((SOURCE / 'recipe/timeline.json').read_text())['pieces']
    dump(out / 'shots.json', shots)
    originals = [SOURCE / 'RO-17-3-Healthy-Foods-That-Made-Me-Fat-DRAFT.mp4', SOURCE / 'RO-17-PICTURE-DRAFT.mp4', SOURCE / 'cache/RO-17-BASE.mp4']
    dump(out / 'originals.json', {str(p):sha(p) for p in originals})
    H.build(out / 'plan_resolved.json', out / 'words_out.json', out / 'shots.json', out / 'hf', render=False)
    dump(out / 'graphics.edit-sheet-rows.json', H.edit_sheet_graphics(out / 'plan_resolved.json', out / 'words_out.json', out / 'hf'))


def render(out):
    H.build(out / 'plan_resolved.json', out / 'words_out.json', out / 'shots.json', out / 'hf')
    src = SOURCE / 'RO-17-3-Healthy-Foods-That-Made-Me-Fat-DRAFT.mp4'
    # One audio file is copied into BOTH proof players without processing or new effects.
    run([FF, '-v', 'error', '-y', '-ss', str(F0/C.FPS), '-i', src, '-t', str(N/C.FPS), '-vn', '-c:a', 'copy', out/'audio.m4a'])
    run([FF, '-v', 'error', '-y', '-i', SOURCE/'cache/RO-17-BASE.mp4', '-vf', f'trim=start_frame={F0}:end_frame={F1},setpts=PTS-STARTPTS', '-an', '-c:v', 'libx264', '-crf', '12', '-preset', 'fast', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', out/'base.mp4'])
    old = [e for e in json.loads((SOURCE/'recipe/graphics.json').read_text()) if e['end']>A and e['start']<Z]
    layers = [(e, Image.open(e['path']).convert('RGBA')) for e in old]
    comp = H.load_compositor(out/'hf')
    enc = {}
    for key in ('old','new'):
        enc[key] = subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-framerate','30000/1001','-i','-', '-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-preset','fast','-crf','16','-threads','3','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(out/(key+'.picture.mp4'))],stdin=subprocess.PIPE)
    for i, frame in enumerate(C.reader(str(out/'base.mp4'))):
        g = F0+i
        if i % 300 == 0: print(f'Comparison frame {i}/{N}', flush=True)
        base = B.shift_presenter(Image.fromarray(frame), dx=350, c0=450, wall_w=450)
        oldim = base.convert('RGBA')
        for e, layer in layers:
            if C.fr(e['start'])<=g<C.fr(e['end']): oldim=Image.alpha_composite(oldim,layer)
        enc['old'].stdin.write(oldim.convert('RGB').tobytes())
        enc['new'].stdin.write(np.ascontiguousarray(comp.apply(np.asarray(base),g)).tobytes())
    for key,p in enc.items():
        p.stdin.close()
        if p.wait(): raise RuntimeError('encode failed '+key)
        run([FF,'-v','error','-y','-i',out/(key+'.picture.mp4'),'-i',out/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',out/(key+'.mp4')])
    # Native old draft excerpt for reference, separate from the fair graphics comparison.
    run([FF,'-v','error','-y','-ss',str(F0/C.FPS),'-i',src,'-t',str(N/C.FPS),'-c:v','libx264','-crf','18','-preset','fast','-c:a','copy','-movflags','+faststart',out/'original-draft.mp4'])


def refresh(out):
    """Reuse the already-rendered side list; only extend/rebuild the price tail."""
    old_f0=C.fr(337.036); split=C.fr(390.21)
    saved=out/'first-pass';saved.mkdir(exist_ok=True)
    for key in ('old','new'):
        if not (saved/(key+'.mp4')).exists(): (out/(key+'.mp4')).rename(saved/(key+'.mp4'))
    H.build(out/'plan_resolved.json',out/'words_out.json',out/'shots.json',out/'hf')
    for key in ('old','new'):
        run([FF,'-v','error','-y','-i',saved/(key+'.mp4'),'-vf',f'trim=start_frame={F0-old_f0}:end_frame={split-old_f0},setpts=PTS-STARTPTS','-an','-c:v','libx264','-crf','16','-preset','fast','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',out/(key+'.head.mp4')])
    run([FF,'-v','error','-y','-i',SOURCE/'cache/RO-17-BASE.mp4','-vf',f'trim=start_frame={split}:end_frame={F1},setpts=PTS-STARTPTS','-an','-c:v','libx264','-crf','12','-preset','fast','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',out/'tail-base.mp4'])
    comp=H.load_compositor(out/'hf')
    old_layer=Image.open(SOURCE/'graphics/chipotle.png').convert('RGBA')
    enc={}
    for key in ('old','new'):
        enc[key]=subprocess.Popen([FF,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-framerate','30000/1001','-i','-','-vf','scale=out_color_matrix=bt709:out_range=tv,format=yuv420p','-c:v','libx264','-crf','16','-preset','fast','-threads','3','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',str(out/(key+'.tail.mp4'))],stdin=subprocess.PIPE)
    for i,frame in enumerate(C.reader(str(out/'tail-base.mp4'))):
        g=split+i;base=B.shift_presenter(Image.fromarray(frame),dx=350,c0=450,wall_w=450)
        old=base.convert('RGBA')
        if C.fr(390)<=g<C.fr(398):old=Image.alpha_composite(old,old_layer)
        enc['old'].stdin.write(old.convert('RGB').tobytes())
        enc['new'].stdin.write(np.ascontiguousarray(comp.apply(np.asarray(base),g)).tobytes())
    for key,p in enc.items():
        p.stdin.close()
        if p.wait():raise RuntimeError('tail encode failed')
    run([FF,'-v','error','-y','-ss',str(F0/C.FPS),'-i',SOURCE/'RO-17-3-Healthy-Foods-That-Made-Me-Fat-DRAFT.mp4','-t',str(N/C.FPS),'-vn','-c:a','copy',out/'audio.m4a'])
    for key in ('old','new'):
        concat=out/(key+'.concat.txt');concat.write_text(''.join("file '"+str(out/(key+'.'+part+'.mp4'))+"'\n" for part in ('head','tail')))
        run([FF,'-v','error','-y','-f','concat','-safe','0','-i',concat,'-i',out/'audio.m4a','-map','0:v','-map','1:a','-c','copy','-movflags','+faststart',out/(key+'.mp4')])
    run([FF,'-v','error','-y','-ss',str(F0/C.FPS),'-i',SOURCE/'RO-17-3-Healthy-Foods-That-Made-Me-Fat-DRAFT.mp4','-t',str(N/C.FPS),'-c:v','libx264','-crf','18','-preset','fast','-c:a','copy','-movflags','+faststart',out/'original-draft.mp4'])


def finish(out):
    for name in ('old', 'new'):
        data=json.loads(subprocess.check_output([FF.replace('ffmpeg','ffprobe'),'-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,width,height,r_frame_rate','-of','json',str(out/(name+'.mp4'))],text=True))['streams'][0]
        assert int(data['nb_frames']) == N and (data['width'],data['height']) == (1920,1080), data
    report = H.verify(out/'hf', out/'new.mp4', F0/C.FPS, out/'checks')
    originals=json.loads((out/'originals.json').read_text())
    assert all(sha(p)==v for p,v in originals.items()), 'An original changed'
    for name in ('old','new'):
        # Hash encoded audio packet data, excluding shifted timestamps.
        r=subprocess.run([FF,'-v','error','-i',str(out/(name+'.mp4')),'-map','0:a','-c','copy','-f','hash','-hash','sha256','-'],capture_output=True,text=True,check=True)
        (out/(name+'.audio.sha')).write_text(r.stdout)
    assert (out/'old.audio.sha').read_text()==(out/'new.audio.sha').read_text()
    stills=out/'stills';stills.mkdir(exist_ok=True)
    for iid,t in [('alternatives',389.0),('chipotle',397.10)]:
        for key in ('old','new'):
            still_t = 348.0 if iid == 'alternatives' and key == 'old' else t
            img=next(C.reader(str(out/(key+'.mp4')),C.fr(still_t)-F0,1))
            Image.fromarray(img).save(stills/(iid+'-'+key+'.jpg'),quality=92)
    write_sheet(out)
    context = out/'context'; context.mkdir(exist_ok=True)
    for it in json.loads((out/'plan_resolved.json').read_text()):
        lo=max(0,it['t0']-F0/C.FPS-3); hi=min(N/C.FPS,it['t1']-F0/C.FPS+3)
        run([FF,'-v','error','-y','-ss',str(lo),'-i',out/'new.mp4','-t',str(hi-lo),'-vf','scale=960:540','-c:v','libx264','-crf','21','-preset','fast','-c:a','copy','-movflags','+faststart',context/(it['id']+'-context - REVIEW 540p.mp4')])
    dump(out/'proof-receipt.json',dict(range=[F0/C.FPS,F1/C.FPS],frames=N,seconds=N/C.FPS,
          version=H.VERSION,checks=report,originals_unchanged=True,audio_payload_identical=True,
          limits=['Graphics-only comparison, both use the same clean presenter layer; draft stock placeholders excluded from both.',
                  'Fixed presenter shift shared by both players; existing source cuts/grade retained.',
                  'Old graphic copy is unchanged; timing changes deliberately to match speech.',
                  'No approved/full video rebuilt or uploaded; proof is pending Dan review.']))


def write_sheet(out):
    """Record the proof's actual cut, configs and measured heads, never invented raw facts."""
    import statistics
    checks = H.module('checks')
    frames = sorted((out/'checks/frames').glob('*.png'))
    face_lines=subprocess.run([checks.facebox_bin()]+[str(p) for p in frames],capture_output=True,text=True,check=True).stdout.splitlines()
    faces={int(Path(path).stem):list(map(int,box.split())) for path,box in (line.split('\t') for line in face_lines) if box not in ('none','error')}
    masks=out/'checks/masks'
    todo=[p for p in frames if not (masks/(p.stem+'.mask.png')).exists()]
    if todo:run([checks.PERSONMASK,masks]+todo)
    tl=json.loads((SOURCE/'recipe/timeline.json').read_text())['pieces']
    edl=[];framing=[]
    crops={'full':[3840,2160,0,0],'punch-1':[3584,2016,128,72],'punch-2':[3456,1944,192,84]}
    for piece in tl:
        lo=max(F0,piece['out_f0']);hi=min(F1,piece['out_f1'])
        if lo>=hi:continue
        cw,ch,cx,cy=crops[piece['crop']];samples=[]
        for g,fb in faces.items():
            if not lo<=g<hi:continue
            mk=np.asarray(Image.open(masks/(str(g)+'.mask.png')).convert('L').resize((1920,1080)))>127
            hx=(fb[0]+fb[2])/2;fw=fb[2]-fb[0]
            x0=max(0,int(hx-.6*fw));x1=min(1920,int(hx+.6*fw))
            ys=np.nonzero(mk[:,x0:x1].mean(axis=1)>=.2)[0];ys=ys[ys<fb[3]]
            if len(ys):samples.append(dict(hair_top=float(ys.min())*ch/1080+cy,cx=(hx-350)*cw/1920+cx,chin=fb[3]*ch/1080+cy))
        if not samples:raise RuntimeError('No measured head on proof segment '+str(piece['index']))
        src=piece['src_in']+(lo-piece['out_f0'])/C.FPS
        edl.append(dict(roll='C1713',src_in=src,src_out=src+(hi-lo)/C.FPS,src_f0=C.fr(src),out_in=(lo-F0)/C.FPS,out_out=(hi-F0)/C.FPS,out_f0=lo-F0,out_f1=hi-F0,shot=piece['index'],audio={'src_in':lo/C.FPS,'src_out':hi/C.FPS},join='first' if not edl else 'cut'))
        framing.append(dict(name=piece['crop'],crop=[cw,ch,cx,cy],head=dict(hair_top=min(q['hair_top'] for q in samples),cx=statistics.median(q['cx'] for q in samples),chin=statistics.median(q['chin'] for q in samples)),measured='Apple Vision face and head-band person mask on every tenth graphic frame, mapped back through known crop/350px fixed shift; proof sampling, not full-film hair clearance.',shift=dict(dx=350,c0=450,wall_w=450)))
    words=[dict(w=w['w'],t0=max(0,w['t0']-F0/C.FPS),t1=min(N/C.FPS,w['t1']-F0/C.FPS)) for w in json.loads((out/'words_out.json').read_text()) if F0/C.FPS<=w['t0']<F1/C.FPS]
    graphics=H.edit_sheet_graphics(out/'plan_resolved.json',out/'words_out.json',out/'hf')
    for g in graphics:
        g['t0']-=F0/C.FPS;g['t1']-=F0/C.FPS
        cfg=g['config'];cfg['a']-=F0/C.FPS;cfg['b']-=F0/C.FPS
        if g['template']=='side-list':cfg['reveal']=[t-F0/C.FPS for t in cfg['reveal']]
        else:cfg['parts']=[[text,t-F0/C.FPS] for text,t in cfg['parts']]
        for d in g['driven_by']:d['t']-=F0/C.FPS
    run([FF,'-v','error','-y','-ss',str(F0/C.FPS),'-i',SOURCE/'audio/voice_raw.wav','-t',str(N/C.FPS),'-c:a','pcm_s16le',out/'untreated.wav'])
    source='/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1713.MP4'
    sheet=dict(schema='abs-edit-sheet/1',job='RO-17-HF-PROOF',title='RO-17 isolated HyperFrames proof',type='LFC',editor='codex',
        video=dict(master=str(out/'new.mp4'),sha256=sha(out/'new.mp4'),fps='30000/1001',frames=N,duration=N/C.FPS,width=1920,height=1080,rolls={'C1713':dict(path=source,width=3840,height=2160,fps='30000/1001')}),
        grade=dict(filter='eq=gamma=1.28:contrast=1.04:saturation=0.92,unsharp=5:5:0.25:5:5:0',order='after_scale_1080',decode='bt709',note='Inherited unchanged from RO-17 clean cached base.'),
        edl=edl,framing=framing,words=dict(list=words,timing='mapped-source',fixes=[]),graphics=graphics,pictures=[],
        audio=dict(mix=str(out/'new.mp4'),untreated=str(out/'untreated.wav'),chain='Original draft excerpt audio, copied identically into both proof players. No processing.'),
        approvals=dict(status='pending',round='graphics-method proof',decisions=[]),
        provenance=dict(written='2026-10-03',by='Codex',build_dir=str(out),inputs={**json.loads((out/'originals.json').read_text()), **{str(out/name):sha(out/name) for name in ('plan_resolved.json','words_out.json','hf/manifest.json')}}))
    sheet_path=out/'new.mp4.edit-sheet.json';dump(sheet_path,sheet)
    run([sys.executable,H.SHARED.parent/'edit-sheet/validate.py',sheet_path,'--hash','--json',out/'edit-sheet-validation.json'])


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('stage',choices=['plan','render','refresh','finish']);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();globals()[args.stage](args.out)
