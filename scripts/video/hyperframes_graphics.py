#!/usr/bin/env python3
"""Codex entrypoint to shared HyperFrames. No renderer or template lives here.

build(plan, words, shots, out) runs the shared graphics pass.
load_compositor(out) returns the shared RGB Compositor for a film-frame loop.
verify(out, film, film_t0, check_dir) runs shared composite checks.
edit_sheet_graphics(plan, words, out) records exact configs and spoken drivers.
All paths passed by a video builder should be absolute.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
# Shared installation includes local Vision binaries and fonts that Git does not carry.
SHARED = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI/.claude/skills/_shared/hyperframes')
VERSION = '0.8.97'


def module(name):
    spec = importlib.util.spec_from_file_location('codex_shared_' + name, SHARED / (name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build(plan, words, shots, out, render=True):
    """Reject unanchored scene edges/parts before invoking the canonical pass."""
    if module('hfbuild').VERSION != VERSION:
        raise RuntimeError('Shared HyperFrames version changed; expected ' + VERSION)
    P = module('from_plan')
    W = P.Words(words)
    items = json.loads(Path(plan).read_text())
    starts = [w['t0'] for w in W.w]
    for it in items:
        if not P.tkind(it):
            continue
        for key in ('t0', 't1'):
            if not any(abs(it[key] - t) <= 0.001 for t in starts):
                raise ValueError(f"{it['id']}: {key} must be a mapped word start before shot snapping")
        for key, edge in (('start', 't0'), ('end', 't1')):
            phrase = it.get(key)
            if not isinstance(phrase, str) or not phrase.strip():
                raise ValueError(f"{it['id']}: {key} must name the phrase that sets {edge}")
            word_t = W.at(phrase, it['t0'] - 1, it['t1'] + 0.001, key)
            if abs(word_t - it[edge]) > 0.001:
                raise ValueError(f"{it['id']}: {edge} disagrees with phrase {phrase!r}")
        if it['kind'] == 'lt':
            drivers = [p[1] for p in it.get('parts', [])]
            drivers += [it['bar'][k] for k in ('grow', 'shrink', 'land')] if it.get('bar') else []
        elif it['kind'] == 'l3':
            drivers = it['reveal']
        elif it['kind'] == 'cycle':
            drivers = list(it.get('reveal', it.get('flip', {})).values()) + [it['close'], it['pulse']]
            if 'title_swap' in it: drivers += [it['title_swap']]
        else:
            drivers = [it['eyebrow'][1]] + [p[1] for p in it['headline']]
            if it.get('detail'): drivers += [it['detail'][1]]
            if it.get('sweep') is not None: drivers += [it['sweep']]
        if not drivers or any(not isinstance(p, str) or not p.strip() for p in drivers):
            raise ValueError(f"{it['id']}: every reveal must name a spoken phrase")
    cmd = [sys.executable, str(SHARED / 'from_plan.py'), '--plan', str(plan), '--words', str(words), '--out', str(out)]
    if shots: cmd += ['--shots', str(shots)]
    if render: cmd += ['--render']
    subprocess.run(cmd, check=True)
    return json.loads((Path(out) / 'manifest.json').read_text())


def load_compositor(out, wh=None):
    manifest = json.loads((Path(out) / 'manifest.json').read_text())
    for m in manifest:
        for k in ('mov', 'mask'):
            if k in m and not Path(m[k]).is_file():
                raise FileNotFoundError(m[k])
    return module('composite').Compositor(manifest, wh=wh)


def verify(out, film, film_t0, check_dir):
    subprocess.run([sys.executable, str(SHARED / 'checks.py'), str(Path(out) / 'manifest.json'),
                    '--film', str(film), '--film-t0', str(film_t0), '--out', str(check_dir)], check=True)
    report = json.loads((Path(check_dir) / 'checks.json').read_text())
    # A shared PASS with no face/person measurement is not evidence of clearance.
    for it in report['items']:
        if not it['frames']: raise ValueError(f"{it['id']}: no composite frames checked")
        if it['template'] == 'lower-third' and (it.get('min_face_gap') is None or it.get('no_face')):
            raise ValueError(f"{it['id']}: face clearance was not measured on every sampled frame")
        if it['template'] in ('side-list', 'cycle') and it.get('min_clear') is None:
            raise ValueError(f"{it['id']}: person clearance was not measured")
    return report


def edit_sheet_graphics(plan, words, out):
    P = module('from_plan'); W = P.Words(words)
    items = {x['id']: x for x in json.loads(Path(plan).read_text())}
    rows = []
    for m in json.loads((Path(out) / 'manifest.json').read_text()):
        cfg = json.loads((Path(out) / 'configs' / m['template'] / (m['id'] + '.json')).read_text())[0]
        it = items[m['id']]
        if m['template'] == 'lower-third': text = [cfg['topic']] + [p[0] for p in cfg['parts']]
        elif m['template'] == 'side-list': text = ([cfg['heading']] if isinstance(cfg['heading'], str) else cfg['heading']) + cfg['items']
        elif m['template'] == 'before-card': text = [cfg['eyebrow'][0]] + [p[0] for p in cfg['headline']] + ([cfg['detail'][0]] if cfg.get('detail') else [])
        else:
            text = [cfg['title']] + cfg['boxes']
            if cfg.get('old_title'): text += [cfg['old_title']] + cfg['old_boxes']
        if cfg.get('label'): text += [cfg['label']]
        drivers = [dict(part='in', phrase=it['start'], t=cfg['a']), dict(part='out', phrase=it['end'], t=cfg['b'])]
        if m['template'] == 'lower-third':
            pairs = [(text, phrase, t) for (text, phrase), (_, t) in zip(it['parts'], cfg['parts'])]
            if it.get('bar'): pairs += [(k, it['bar'][k], cfg['bar'][k]) for k in ('grow', 'shrink', 'land')]
        elif m['template'] == 'side-list':
            pairs = list(zip(cfg['items'], it['reveal'], cfg['reveal']))
        elif m['template'] == 'before-card':
            pairs = [(cfg['eyebrow'][0], it['eyebrow'][1], cfg['eyebrow'][1])]
            pairs += [(text, phrase, t) for (text, phrase), (_, t) in zip(it['headline'], cfg['headline'])]
            if it.get('detail'): pairs += [(cfg['detail'][0], it['detail'][1], cfg['detail'][1])]
            if it.get('sweep'): pairs += [('sweep', it['sweep'], cfg['sweep'])]
        else:
            key = 'flip' if it.get('cycle_kind') == 'flip' else 'reveal'
            pairs = [(k, ph, cfg[key][k]) for k, ph in it[key].items()]
            pairs += [(k, it[k], cfg[k]) for k in ('close', 'pulse')]
            if it.get('title_swap'): pairs += [('title_swap', it['title_swap'], cfg['title_swap'])]
        drivers += [dict(part=part, phrase=phrase, t=t) for part, phrase, t in pairs]
        rows.append(dict(id=m['id'], template=m['template'], config=cfg, text=text,
                         t0=m['a'], t1=m['b'], layer={'opaque':'full', 'glass':'overlay', 'overlay':'side'}[m['kind']], driven_by=drivers))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    b = sub.add_parser('build')
    for key in ('plan', 'words', 'out'): b.add_argument('--' + key, required=True)
    b.add_argument('--shots'); b.add_argument('--configs-only', action='store_true')
    v = sub.add_parser('verify')
    for key in ('out', 'film', 'check-dir'): v.add_argument('--' + key, required=True)
    v.add_argument('--film-t0', type=float, default=0)
    a = ap.parse_args()
    if a.command == 'build': build(a.plan, a.words, a.shots, a.out, not a.configs_only)
    else: verify(a.out, a.film, a.film_t0, a.check_dir)


if __name__ == '__main__': main()
