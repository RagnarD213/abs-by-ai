"""File the exact Dan-approved R3 movies. No encoding, QA rewriting or uploads."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import re
import shutil
import sys

ROOT = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
WORK = Path('/Volumes/Extreme/_edit_work/SL-11/round3')
DEST = ROOT / 'Short-form video content/SL-11 The Vacuum'
BACKUP = Path('/Volumes/Extreme/Short-form video content/SL-11 The Vacuum')
QUOTE = 'All three look good. Finalize them and prepare the Codex handoff for cover images and upload setup.'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

def copy_exact(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        assert sha(src) == sha(dst), f'Refusing to overwrite different file: {dst}'
    else:
        shutil.copy2(src, dst)
    assert sha(src) == sha(dst)

def main():
    manifest = json.loads((WORK / 'delivery-manifest.json').read_text())
    # Prior-round records are historical and remain immutable.
    for p in json.loads((WORK / 'preserved-files.json').read_text()):
        assert sha(p['path']) == p['sha256'], p['path']
    sys.path.insert(0, str(ROOT / '.claude/skills/_shared/deliver'))
    import gate
    rows = []
    for row in manifest['files']:
        s = row['short']
        src = Path(row['delivery'])
        assert sha(src) == row['sha256'] == sha(row['file'])
        gate.require_stamp(str(src))
        audio = json.loads(Path(str(src) + '.audio_gate.json').read_text())
        assert audio['verdict'] == 'PASS' and audio['sha256'] == row['sha256']
        out = DEST / f'The Vacuum - Short {s} - {row["title"]} - R3 FINAL.mp4'
        copy_exact(src, out)
        for suffix in ('.audio_gate.json', '.deliver_gate.json'):
            copy_exact(Path(str(src) + suffix), Path(str(out) + suffix))
        gate.require_stamp(str(out))
        plan = json.loads((WORK / 'build' / s / 'gate/plan.json').read_text())
        cues_path = WORK.parent / 'round1/build' / s / 'cues.json'
        cues = json.loads(cues_path.read_text())
        # The full R3 kept the full R1 caption states and native timeline.
        assert len(cues) == len(plan['caption_states'])
        for c, state in zip(cues, plan['caption_states']):
            assert sha(c['png']) == sha(state['image'])
            assert abs(c['f0'] * 1001 / 30000 - state['beat'][0]) < .0001
            assert abs(c['f1'] * 1001 / 30000 - state['beat'][1]) < .0001
            assert c['f1'] <= row['frames']
        srt_source = Path(plan['srt'])
        blocks = re.split(r'\n\s*\n', srt_source.read_text().strip())
        assert len(blocks) == len(cues)
        for block, cue in zip(blocks, cues):
            assert ' '.join(block.splitlines()[2:]).strip() == cue['text'].strip()
        srt = out.with_suffix('.srt')
        copy_exact(srt_source, srt)
        transcript = out.with_suffix('.transcript.txt')
        text = ' '.join(c['text'] for c in cues) + '\n'
        if transcript.exists():
            assert transcript.read_text() == text
        else:
            transcript.write_text(text)
        for p in [out, srt, transcript, Path(str(out)+'.audio_gate.json'), Path(str(out)+'.deliver_gate.json')]:
            copy_exact(p, BACKUP / p.name)
        rows.append(dict(short=s, title=row['title'], master=str(out), sha256=sha(out),
                         md5=hashlib.md5(out.read_bytes()).hexdigest(), bytes=out.stat().st_size,
                         frames=row['frames'], seconds=row['seconds'], srt=str(srt),
                         srt_sha256=sha(srt), caption_cues=len(cues),
                         transcript=str(transcript), extreme=str(BACKUP/out.name),
                         source_review=row['file'], audio_gate='PASS', delivery_gate='PASS',
                         caption_source=str(srt_source), caption_state_proof=str(cues_path),
                         ending=' '.join(c['text'] for c in cues[-8:])))
    approval = dict(job='SL-11', round=3, status='finalized',
                    approved_at=datetime.now(ZoneInfo('America/Chicago')).isoformat(),
                    approved_date='2026-10-28', approved_by='Dan', exact_words=QUOTE,
                    approval_source='Direct user message in chat 01a183c0-a300-7f30-a67f-53dc4607d97c',
                    category='ORGANIC CONTENT / SFL', selected_intro=1,
                    complete_films_approved=True, media_changed_at_finalization=False,
                    covers_approved=False, social_uploaded=False, scheduled=False,
                    review_manifest=str(WORK/'delivery-manifest.json'), files=rows)
    p = DEST / 'approval.json'
    if p.exists():
        old=json.loads(p.read_text())
        assert old['files']==rows and old['exact_words']==QUOTE
        approval=old
    else:
        p.write_text(json.dumps(approval,indent=2)+'\n')
    for target in [BACKUP/'approval.json', WORK/'finalization-approval.json', ROOT/'Handoffs/video-editing/SL-11-R3-approval.json']:
        copy_exact(p,target)
    print(json.dumps(dict(status='finalized', project=str(DEST), extreme=str(BACKUP),
                          movies=len(rows), files=[dict(short=r['short'],sha256=r['sha256'],bytes=r['bytes'],caption_cues=r['caption_cues']) for r in rows]),indent=2))

if __name__ == '__main__':
    main()
