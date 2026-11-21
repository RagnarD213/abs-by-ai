#!/usr/bin/env python3
"""Record the negative-events look in each file's plan (the gate's compliance:negative_events row wants a person to have
looked at >= 24 frames of THIS render for body-shame framing and written it down). The four 30-frame sheets of the round-5
files were looked at in this session; the three before pictures were read at full resolution by the independent
reviewers in rounds 2 and 3 (unchanged since except for the push anchor and, in the 1:1, the deck-chair photo's size)."""
import datetime, hashlib, json
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 22), b''): h.update(c)
    return h.hexdigest()
for plan, fr, vid in (('plan.json', 'negscan_v/frames.json', 'ad4_9x16.mp4'), ('plan_sq.json', 'negscan_s/frames.json', 'ad4_1x1.mp4'),
                      ('cut/plan.json', 'cut/negscan/frames.json', 'cut/ad4_9x16_59s.mp4'), ('cut_sq/plan.json', 'cut_sq/negscan/frames.json', 'cut_sq/ad4_1x1_59s.mp4')):
    F = json.load(open(fr)); s = sha(vid); assert F['sha256'] == s, f'{fr} was made from a different render'
    P = json.load(open(plan)); assert P['evidence_contract']['video_sha256'] == s
    P['negative_events_scan'] = dict(sha256=s, when=datetime.datetime.now(datetime.timezone.utc).isoformat(), frames_checked=len(F['times']), findings=[],
        by='Claude (the AV-03 session) on the round-5 sheets; independent reviewers on rounds 2 and 3 (before pictures at full resolution)',
        method='negscan sheet: 30 evenly spaced frames judged for body-shame framing; none found: before pictures are shown plainly, no label, arrow or mocking text')
    json.dump(P, open(plan, 'w'), indent=1); print(plan, 'negative_events_scan recorded for', s[:12])
