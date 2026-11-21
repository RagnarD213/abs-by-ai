#!/usr/bin/env python3
"""Validate review evidence completeness and freeze notes before benchmark reveal.
This verifies bookkeeping, not editorial quality or Dan's approval. Rules stay in SKILL.md.
Usage: review_record.py RECORD [--freeze NOTES SUMMARY] [--blind]
"""
import argparse, datetime, hashlib, json, math
from pathlib import Path


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def validate(d, base):
    errors = []
    proofs = {}
    def err(s): errors.append(s)
    def proof(ref, label):
        if not isinstance(ref, str) or not ref:
            err(label + ': missing evidence'); return
        p = (base / ref).resolve()
        if not p.is_file() or not p.stat().st_size:
            err(label + ': evidence absent or empty'); return
        proofs[str(p)] = sha(p)
    def number(v): return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)
    src = d.get('source', {})
    p = Path(src.get('path', ''))
    if not p.is_file() or sha(p) != src.get('sha256'):
        err('source: missing file or changed hash')
    duration = src.get('duration', 0)
    if not number(duration) or duration <= 0:
        err('source: invalid duration'); duration = 0
    for mode in ('picture', 'motion', 'audio'):
        spans = d.get('coverage', {}).get(mode, [])
        end = 0.0
        valid = []
        for n, span in enumerate(spans):
            a, b = span.get('start'), span.get('end')
            if not number(a) or not number(b) or not 0 <= a < b <= duration + .001:
                err(mode + ': invalid interval'); continue
            valid.append((a, b))
            if not span.get('reviewer') or not span.get('method') or not span.get('observations'):
                err(mode + ': reviewer, method and observations required')
            proof(span.get('evidence'), f'{mode} span {n}')
        for a, b in sorted(valid):
            if a > end + .001: err(mode + f': uncovered {end:.3f}-{a:.3f}')
            end = max(end, b)
        if end < duration - .001 or not valid: err(mode + ': incomplete runtime coverage')
    for name in ('joins', 'ai_shots', 'text_panels'):
        inv = d.get(name, {})
        if inv.get('inventory_complete') is not True:
            err(name + ': inventory not confirmed complete')
        items = inv.get('items', [])
        if not items and not inv.get('none_reason'):
            err(name + ': empty inventory needs a reason')
        for n, item in enumerate(items):
            label = f'{name} {n}'
            if not item.get('observation') or item.get('disposition') not in ('editor_item', 'retained', 'private_summary'):
                err(label + ': observation and resolved disposition required')
            if name == 'joins':
                t = item.get('time')
                if not number(t) or not 0 <= t <= duration: err(label + ': invalid time')
                fields = ('native_frames', 'motion_audio')
            else:
                a, b = item.get('start'), item.get('end')
                if not number(a) or not number(b) or not 0 <= a < b <= duration: err(label + ': invalid span')
                fields = ('consecutive_fullres', 'last_two_seconds', 'regions', 'motion') if name == 'ai_shots' else ('fullres', 'speech_timing')
                if name == 'text_panels' and not item.get('transcription'): err(label + ': missing verbatim text')
            for field in fields: proof(item.get(field), label + ' ' + field)
    for key in ('audio_measurements', 'framing_evidence', 'library_pass', 'calibration_selfcheck'):
        proof(d.get(key), key)
    if d.get('unresolved') != []: err('unresolved judgments remain or are not declared')
    return errors, proofs


def freeze(record, notes, summary, blind=False):
    record = Path(record); base = record.resolve().parent
    d = json.loads(record.read_text()); errors, proofs = validate(d, base)
    if blind and d.get('benchmark_unseen') is not True:
        errors.append('blind test requires a genuinely unseen benchmark')
    for p in (Path(notes), Path(summary)):
        if not p.is_file() or not p.stat().st_size: errors.append('notes or summary missing'); continue
        if any(c in p.read_text() for c in ('\u2013', '\u2014')): errors.append('prohibited dash in '+str(p))
        proofs[str(p.resolve())] = sha(p)
    if errors: raise ValueError('\n'.join(errors))
    proofs[str(record.resolve())] = sha(record)
    target = record.with_suffix('.freeze.json')
    receipt = {'frozen_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'test_type': 'blind' if blind else 'regression', 'source': d['source'],
               'files_sha256': proofs, 'editorial_pass': None,
               'meaning': 'Evidence bookkeeping complete. Quality requires adjudication after reveal.'}
    with target.open('x') as f: json.dump(receipt, f, indent=2)
    return target


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('record', type=Path); ap.add_argument('--freeze', nargs=2, metavar=('NOTES', 'SUMMARY'))
    ap.add_argument('--blind', action='store_true'); a = ap.parse_args()
    if a.freeze:
        try: print(freeze(a.record, *a.freeze, blind=a.blind))
        except (ValueError, FileExistsError) as e: print(e); return 1
    else:
        d = json.loads(a.record.read_text()); errors, _ = validate(d, a.record.resolve().parent)
        print(json.dumps({'bookkeeping_complete': not errors, 'editorial_pass': None, 'errors': errors}, indent=2))
        return int(bool(errors))
    return 0

if __name__ == '__main__': raise SystemExit(main())
