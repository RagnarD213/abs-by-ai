#!/usr/bin/env python3
"""Build the 10/23 pool shoot documents from the shoot doc (used 2026-10-20).

    python3 tp_from_1023_doc.py doc.json out_dir "10-23 Pool Shoot"

doc.json is the saved output of the Docs connector's read_doc on the shoot doc (the source is only ever read).
Writes four HTML files into out_dir, plus built_seq.json (every non-empty line of each document, in order) for the
check after upload. Upload and verify: SKILL.md, "No Chrome: upload with rclone".

  Teleprompter 1 - Long Form                   the 7 "SCRIPT:" long-forms, then the 4 follow-along cue tracks
  Teleprompter 2 - Short Form (Part 1 of 2)    shorts 1 to 15
  Teleprompter 3 - Short Form (Part 2 of 2)    shorts 16 to 29
  Filming Document                             shoot notes, every script with its cues and notes, B-roll shot list

How it reads the 10/23 format (tp_from_shoot_doc.py reads the 10/17 one):
- A short is a Heading 3 "N. TITLE"; a follow-along is a Heading 3 under the FOLLOW-ALONG Heading 2; a long-form is a
  Heading 3 "SCRIPT: ...". Each runs to the next Heading 3 or Heading 2. The outlines section is left out entirely.
- "-" lines, "N spoken words..." note lines and "RO-33." id lines are notes. A paragraph that starts with [ and ends
  with ] is a cue (it may hold several [..] cues). "HOOK TAKES (alternate openers):" is a label; the bulleted lines
  under it are alternate first lines Dan films, so they go on the prompter (after the Subscribe line, label dropped).
- An empty paragraph inside a follow-along marks where a round cue stood: one blank line on the prompter (the source
  has two), none anywhere else (Dan, 2026-10-13). A soft line break starts a new paragraph.
- Titles stay as typed (shorts in CAPS with their number). Pending suggestions are read as accepted: the count printed
  must be 0.
"""
import json, re, html, sys, os

PST = 'style="color:#000000;font-weight:normal;font-style:normal"'
BST = 'style="color:#000000;font-weight:bold;font-style:normal"'
IST = 'style="color:#000000;font-weight:normal;font-style:italic"'
BREAK = '<p><br clear="all" style="page-break-before:always"></p>'
BLANK = '<p %s><br></p>' % PST
HOOK_LABEL = 'HOOK TAKES (alternate openers):'

def load(path):
    P, pend = [], 0
    for el in json.load(open(path))['content']['tabs'][0]['documentTab']['body']['content']:
        if 'paragraph' not in el: continue
        p, acc = el['paragraph'], ''
        for r in p['elements']:
            tr = r.get('textRun', {})
            if tr.get('suggestedInsertionIds') or tr.get('suggestedDeletionIds'): pend += 1
            if not tr.get('suggestedDeletionIds'): acc += tr.get('content', '')
        P.append({'i': el['startIndex'], 'style': p.get('paragraphStyle', {}).get('namedStyleType', ''),
                  'bullet': bool(p.get('bullet')), 't': acc.rstrip('\n')})
    return P, pend

def kind(p):
    t = p['t'].strip()
    if p['bullet']: return 'HOOK'
    if t == '': return 'EMPTY'
    if t == '-': return 'SEP'
    if re.match(r'^\d+ spoken words', t): return 'NOTE'
    if re.match(r'^RO-\d+\.$', t): return 'ID'
    if t == HOOK_LABEL: return 'LABEL'
    if t.startswith('[') and t.endswith(']'): return 'CUE'
    return 'SAY'

def parse(P):
    h2 = [k for k, p in enumerate(P) if p['style'] == 'HEADING_2']
    fa_h2 = next(k for k in h2 if P[k]['t'].startswith('LONG-FORM: FOLLOW-ALONG'))
    out_h2 = next(k for k in h2 if P[k]['t'].startswith('LONG-FORM OUTLINES'))
    first_h3 = next(k for k, p in enumerate(P) if p['style'] == 'HEADING_3')
    intro = [p for p in P[1:first_h3] if p['t'].strip() not in ('', '-')]
    items = []
    for k, p in enumerate(P):
        if p['style'] != 'HEADING_3' or not p['t'].strip(): continue
        t = p['t'].strip()
        if re.match(r'^\d+\. ', t): typ = 'short'
        elif t.startswith('SCRIPT: '): typ = 'long'
        elif fa_h2 < k < out_h2: typ = 'follow'
        else: continue                                   # an outline title: not filming material
        end = next((j for j in range(k + 1, len(P)) if P[j]['style'] in ('HEADING_2', 'HEADING_3')), len(P))
        paras = []
        for q in P[k + 1:end]:
            kd = kind(q)
            if kd in ('SAY', 'HOOK', 'CUE'):
                for part in q['t'].split('\x0b'):
                    s = part.strip()
                    if s: paras.append((kd, s))
            else: paras.append((kd, q['t'].strip()))
        while paras and paras[-1][0] in ('EMPTY', 'SEP'): paras.pop()
        items.append({'type': typ, 'title': t, 'tp_title': t[len('SCRIPT: '):] if typ == 'long' else t, 'paras': paras})
    return intro, P[fa_h2]['t'], P[fa_h2 + 1]['t'].strip(), P[h2[-1]]['t'], items

def words(it): return sum(len(t.split()) for k, t in it['paras'] if k in ('SAY', 'HOOK'))

def teleprompter(lst):
    parts, seq = ['<html><head><meta charset="utf-8"></head><body>'], []
    for n, it in enumerate(lst):
        if n: parts.append(BREAK)
        parts.append('<h2>%s</h2>' % html.escape(it['tp_title'])); seq.append(it['tp_title'])
        gap, said = False, False
        for kd, t in it['paras']:
            if kd == 'EMPTY' and it['type'] == 'follow': gap = True; continue
            if kd not in ('SAY', 'HOOK'): continue
            if gap and said: parts.append(BLANK)     # one blank line where a round cue stood
            gap, said = False, True
            parts.append('<p %s>%s</p>' % (PST, html.escape(t))); seq.append(t)
    parts.append('</body></html>')
    return '\n'.join(parts), seq

def linkify(t):
    h = re.sub(r'(https?://[^\s,\]]+)', lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)), html.escape(t))
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', h)          # **shot** = bold (Dan, 2026-10-22: shots bold, videos plain)

def plain(t): return t.replace('**', '')

def filming(intro, fa_h2, fa_note, lf_h2, items, broll):
    parts, seq = ['<html><head><meta charset="utf-8"></head><body>'], []
    def para(t, st=PST, blank=True):
        parts.append('<p %s>%s</p>' % (st, linkify(t))); seq.append(t)
        if blank: parts.append(BLANK)
    def head(tag, t): parts.append('<%s>%s</%s>' % (tag, html.escape(t), tag)); seq.append(t)
    def bullets(lst):
        parts.append('<ul>')
        for b in lst:
            if isinstance(b, tuple):
                parts.append('<li %s>%s<ul>%s</ul></li>' % (PST, linkify(b[0]), ''.join('<li %s>%s</li>' % (PST, linkify(c)) for c in b[1])))
                seq.append(plain(b[0])); seq.extend(plain(c) for c in b[1])
            else: parts.append('<li %s>%s</li>' % (PST, linkify(b))); seq.append(plain(b))
        parts.append('</ul>'); parts.append(BLANK)
    head('h1', DOC_TITLE)
    pending_b = []
    for p in intro:
        if p['bullet']: pending_b.append(p['t'].strip()); continue
        if pending_b: bullets(pending_b); pending_b = []
        para(p['t'].strip(), BST if p['t'].strip().endswith(':') else PST)
    if pending_b: bullets(pending_b)
    def script(it):
        head('h3', it['title']); hooks = []; gap = 0
        for kd, t in it['paras']:
            if kd == 'HOOK': hooks.append(t); continue
            if hooks: bullets(hooks); hooks = []
            if kd == 'EMPTY':
                if it['type'] == 'follow':
                    gap += 1
                    parts.append(BLANK)               # the source's empty paragraphs, on top of the usual blank line
                continue
            if kd == 'SEP': continue
            para(t, {'NOTE': IST, 'ID': IST, 'CUE': BST, 'LABEL': BST}.get(kd, PST))
        if hooks: bullets(hooks)
    head('h2', 'SHORT FORM: THE %d DEDICATED SHORTS' % sum(1 for it in items if it['type'] == 'short'))
    for it in items:
        if it['type'] == 'short': script(it)
    head('h2', fa_h2); para(fa_note)
    for it in items:
        if it['type'] == 'follow': script(it)
    head('h2', lf_h2)
    for it in items:
        if it['type'] == 'long': script(it)
    head('h2', 'B-ROLL SHOT LIST')
    if BROLL_URL: para('The same shots in one list, grouped by body part, no repeats: %s' % BROLL_URL)
    for title, lst in broll:
        head('h3', title); bullets(lst)
    parts.append('</body></html>')
    return '\n'.join(parts), seq

def cues(t): return [c.strip() for c in re.findall(r'\[([^\]]*)\]', t)]

def shots_in(t):
    """B-roll shots in one cue paragraph. "ALL FOUR" or "EACH MACHINE" points at the on-screen text in the same line,
    so that text goes with it."""
    cs = cues(t); text = next((c.split(':', 1)[1].strip() for c in cs if c.startswith('ON SCREEN TEXT:')), None)
    out = []
    for c in cs:
        m = re.match(r'^(?:OPEN ON )?B-ROLL:\s*(.*)$', c)
        if not m: continue
        s = m.group(1)
        if text and re.match(r'^(ALL|EACH)\b', s): s = '%s (on screen: %s)' % (s, text)
        out.append(s)
    return out

def broll_list(items):
    shorts = [it for it in items if it['type'] == 'short']
    longs = [it for it in items if it['type'] == 'long']
    gym_shorts = []
    for it in shorts:
        film, shots = None, []
        for kd, t in it['paras']:
            if kd != 'CUE': continue
            for c in cues(t):
                m = re.match(r'^FILM AT THE GYM ON FRIDAY, 16:9:\s*(.*)$', c)
                if m: film = m.group(1).rstrip('.')
            for sh in shots_in(t):
                if sh not in shots: shots.append(sh)
        gym_shorts.append(('%s: **%s**' % (it['title'], film), ['**%s**' % sh for sh in shots]))
    lf_shots = {}
    for it in longs:
        for kd, t in it['paras']:
            if kd != 'CUE': continue
            for sh in shots_in(t):
                ts = lf_shots.setdefault(sh, [])
                if it['tp_title'] not in ts: ts.append(it['tp_title'])
    gym_long = [('**%s**' % s, ['For: %s' % t for t in ts]) for s, ts in lf_shots.items()]
    cold = lambda lst: [it['tp_title'] for it in lst if any(kd == 'CUE' and c.startswith('COLD OPEN') for kd, t in it['paras'] for c in cues(t))]
    nhooks = sum(1 for it in shorts if any(kd == 'LABEL' for kd, _ in it['paras']))
    pool = ['The talking parts of all %d shorts: by the pool, shirtless, camera turned vertical like the 10/15 pool shorts. '
            '%d of them list two HOOK TAKES: film all three openers.' % (len(shorts), nhooks),
            ('Shorts that open cold on you by the pool (no B-roll before your first line):', cold(shorts)),
            'The %d long-form scripts: read by the pool, shirtless; Friday\'s gym B-roll cut in.' % len(longs),
            ('Long-forms that open cold on you by the pool:', cold(longs)),
            'The %d follow-along cue tracks: the spoken parts only. The 10/15 demo clips cover the exercises.'
            % sum(1 for it in items if it['type'] == 'follow')]
    editor = []
    for it in items:
        ps = it['paras']
        for n, (kd, t) in enumerate(ps):
            if kd != 'CUE': continue
            for c in cues(t):
                if re.match(r'^(AI |PLAY CLIP|SHOW CLIP)', c):
                    sub = ['For: %s' % it['tp_title']]
                    if c == 'AI CLIP TO ILLUSTRATE THIS':
                        nxt = next((s for k2, s in ps[n + 1:] if k2 == 'SAY'), None)
                        prv = next((s for k2, s in reversed(ps[:n]) if k2 == 'SAY'), None)
                        sub.append('Comes between "%s" and "%s"' % (prv, nxt))
                    editor.append(('**%s**' % c, sub))
    return [('Film at the gym on Friday (16:9): the shorts', gym_shorts),
            ('Film at the gym on Friday (16:9): the long-forms (many are the same shots as the shorts)', gym_long),
            ('Film at the gym on Friday (16:9): earlier videos and videos not scripted yet (from the 10/18 shot list)',
             [('**%s**' % sh, ['For: %s' % v for v in vs]) for sh, vs in EARLIER]),
            ('By the pool', pool),
            ('Editor: AI clips and outside clips', editor)]

# Shots on the 10/18 "Chosen Videos And Full B-Roll List" (doc 1XBOfCig7uB4vCnq5Gt76Lk-HdOlagF7YXoO3RrBdWeI) and the Edit
# Queue's blocked jobs (Handoffs/video-editing/jobs.json) that the 10/23 scripts do not already ask for, checked 2026-10-22.
# The pool, props, yard and home items on that list were moved to another day by Dan on 10-19 and stay out.
V = {'RO32': "I'm 41. Here Are The 10 Exercises I Do Every Week (RO-32, waiting on this footage)",
     'DS01': 'Top 5 Ab Exercises (DS-01, waiting on this footage)',
     'DS53': 'The Only 2 Exercises You Need For Bigger Arms (DS-53, waiting on this footage)',
     'DS72': 'Why Cables Beat Dumbbells For Building Muscle (DS-72, waiting on this footage)',
     'DS47': 'The Only 2 Exercises You Need For A V-Taper (DS-47)', 'RO21': 'What Every Body Fat Percentage Looks Like (On Me) (RO-21)',
     'RO23': 'I Ranked Every Ab Exercise From Worst To Best (RO-23)', 'RO24': 'Reacting To Celebrity Ozempic Transformations (RO-24)',
     'RO27': "It's Boring, But It Got Me Abs At 40 (RO-27)", 'RO29': 'Cortisol Belly Is Real, But TikTok Has It Wrong (RO-29)',
     'RO30': 'The Fastest Way To Lose Stubborn Love Handles (RO-30)', 'RO31': 'How To Get Rid Of Man Boobs (RO-31)',
     'LEGR': 'I Ranked Every Leg Exercise From Worst To Best (not scripted yet)',
     'BACKR': 'I Ranked Every Back Exercise From Worst To Best (not scripted yet)',
     'CHESTR': 'I Ranked Every Chest Exercise From Worst To Best (not scripted yet)',
     'ARMR': 'I Ranked Every Arm Exercise From Worst To Best (not scripted yet)',
     'VT': 'How To Get A V-Taper (long-form, not scripted yet)', 'CAB': 'How To Get Bigger Arms With Cables Only (not scripted yet)',
     'NOBENCH': 'How To Get A Bigger Chest Without Bench Pressing (not scripted yet)',
     'PU5': '5 Levels Of Pull-Ups: From Zero To Your First 10 (not scripted yet)'}
EARLIER = [(s, [V[k] for k in ks.split()]) for s, ks in [
    ('WALKING INTO THE GYM: FROM BEHIND, THEN FROM THE FRONT COMING THROUGH THE DOOR', 'RO32'),
    ('CHECKING IN AT THE FRONT DESK', 'RO32'),
    ('WIDE GYM SHOTS, 5 SECONDS EACH: THE RACKS, THE CABLE MACHINE, THE FLOOR', 'RO32'),
    ('TRAINING HARD: 3 OR 4 DIFFERENT HEAVY SETS, 5 SECONDS EACH', 'RO21 RO27 RO29 RO30 RO24'),
    ('EXERCISE BIKE, SIDE ANGLE: STEADY, THEN AN INTERVAL', 'RO32'),
    ('STAIRMASTER, SIDE AND FRONT, SHORT', 'RO32'),
    ('CABLE CRUNCHES WITH THE ROPE, SIDE ANGLE; CLOSE-UP OF THE RIBS CRUNCHING TOWARD THE HIPS; ONE WRONG REP PULLING WITH THE ARMS', 'DS01 RO32 DS72 RO23 RO21'),
    ("CAPTAIN'S CHAIR LEG RAISES, SIDE ANGLE; CLOSE-UP OF THE HIPS CURLING UP; ONE WRONG REP SWINGING", 'RO23 RO21'),
    ('DECLINE SIT-UPS WITH THE MEDICINE BALL OVERHEAD, SIDE ANGLE', 'RO23'),
    ('LEG PRESS, SIDE ANGLE, PLUS A WIDE SHOT OF THE MACHINE; CLOSE-UP OF THE KNEES STOPPING JUST SHORT OF LOCKED', 'RO32 RO27 LEGR'),
    ('HAMSTRING CURLS AND THE GLUTE BRIDGE MACHINE, SIDE ANGLE', 'RO32 LEGR'),
    ('SIDE ANGLE ONLY: LEG EXTENSIONS; CALF RAISE MACHINE; HACK SQUAT; SMITH MACHINE SQUAT; BARBELL SQUAT IN THE RACK; ROMANIAN DEADLIFTS', 'LEGR'),
    ('PULL-UPS FROM BEHIND, THEN A SIDE ANGLE', 'RO32 VT PU5 BACKR'),
    ('ASSISTED PULL-UP MACHINE; PULL-UP NEGATIVES; WEIGHTED PULL-UPS WITH A DIP BELT', 'PU5 BACKR'),
    ('LAT PULLDOWNS WITH THE LONG BAR, BACK AND FRONT ANGLE; CLOSE-UP OF THE WIDE GRIP', 'RO32 VT PU5 BACKR'),
    ('BARBELL T-BAR ROWS (AS WELL AS THE CHEST-SUPPORTED MACHINE)', 'RO32 BACKR'),
    ('REAR DELT MACHINE, BACK ANGLE', 'VT BACKR'),
    ('SIDE ANGLE ONLY: SINGLE-ARM DUMBBELL ROWS; BARBELL BENT-OVER ROWS', 'BACKR'),
    ('DUMBBELL SIDE LATERALS, FRONT ANGLE WITH THE MIRROR BEHIND; CLOSE-UP OF THE DUMBBELLS STOPPING AT SHOULDER HEIGHT', 'RO32 DS47 RO30 VT'),
    ('SIDE LATERAL MACHINE, FRONT ANGLE; SHOULDER PRESS MACHINE, SIDE ANGLE', 'VT'),
    ('CHEST FLIES, MACHINE AND DUMBBELLS', 'RO32 RO31 NOBENCH CHESTR'),
    ('CHEST PRESS MACHINE, INCLINE DUMBBELL PRESS AND DIPS', 'NOBENCH CHESTR'),
    ('SIDE ANGLE ONLY: CABLE CROSSOVERS', 'CHESTR NOBENCH'),
    ('CABLE CURLS, SIDE ANGLE; CLOSE-UPS OF THE ELBOWS PINNED AND THE ARMS STRAIGHT AT THE BOTTOM', 'DS53 DS72 RO32 CAB ARMR'),
    ('TRICEP PUSHDOWNS WITH THE BAR, SIDE ANGLE, CLOSE-UP OF THE LOCKOUT; PLUS THE ROPE PUSHDOWN', 'DS53 DS72 RO32 CAB ARMR'),
    ('OVERHEAD ROPE TRICEP EXTENSIONS, SIDE ANGLE; ROPE HAMMER CURLS ON THE CABLE', 'CAB ARMR'),
    ('DUMBBELL CURLS INTO A DROP SET; STRAIGHT BAR CURLS; EZ BAR CURLS, ALL SIDE ANGLE', 'ARMR'),
]]

# The B-roll document Dan asked for on 2026-10-22: shots only, no video names, no repeats, grouped by body part.
# Every shot from the Filming Document's B-roll list, merged. "**Name:**" is bold.
BROLL_DOC = [
    ('Around the gym', [
        '**Walking into the gym:** from behind, then from the front coming through the door. Film one take in the morning light if you can.',
        '**Putting your earbuds in**, then walking in.',
        '**Checking in at the front desk.**',
        '**Wide gym shots, 5 seconds each:** the racks, the cable machine, the floor. One busier shot with other members far off and unrecognizable.',
        '**Walking tall through the gym.**',
        '**Sitting down at a machine and setting the pin.**',
        '**Close-up: your hand moving the pin down the weight stack.**',
        '**At the dumbbell rack:** pick up a pair, put them back, take a heavier pair.',
        '**One hard set filmed to the last rep:** slow on the way down, the last reps visibly slowing.',
        '**Training hard:** 3 or 4 different heavy sets, 5 seconds each, on machines and cables (leg press, chest press machine, cable curls).',
        '**Finishing a set, then walking between sets** on the HOG center mats.',
        '**Stretching on the stretching mats** after the workout, 3 or 4 stretches.',
        '**Walking out of the gym.**',
        '**Shirtless mirror shot** after the workout.',
        '**The equipment you don\'t use, empty, 5 seconds each:** the squat rack, the deadlift platform, a flat bench with a loaded bar, a barbell set up for power cleans.']),
    ('Cardio', [
        '**Exercise bike, side angle:** a steady pace, then an interval.',
        '**Stairmaster, side and front:** a steady pace, then a few seconds of a fast interval. No music playing on camera. Keep it short for your knee.']),
    ('Abs', [
        '**Cable crunches with the rope:** kneeling, facing the stack, butt out, side angle. Close-up: ribs crunching toward the hips. Plus one wrong rep pulling with the arms.',
        "**Captain's chair leg raises:** side angle, 3 slow reps. Close-up: hips curling up at the top. Plus one wrong rep swinging.",
        '**Decline sit-ups holding a medicine ball overhead:** side angle, ball touching the floor behind you, then reaching for the ceiling, moving straight up and down. Close-up: elbows by the ears, arms not moving.']),
    ('Legs', [
        '**Leg press:** side angle, plus a wide shot of the machine. Close-ups: setting the seat; setting the safety stops; feet pushing through the heels; knees stopping just short of locked.',
        '**Hamstring curls:** side angle. Close-ups: toes pulled toward the shins; the squeeze at the top.',
        '**Glute bridge machine:** side angle. Close-up: the straight line from shoulders to knees at the top.',
        '**Side angle only (skip these first if you run short on time):** leg extensions; calf raise machine; hack squat; Smith machine squat; barbell squat in the rack; Romanian deadlifts.']),
    ('Back', [
        '**Pull-ups:** from behind so the lats show, then a side angle, 3 slow reps.',
        '**Pull-up negatives:** 3 slow lowers from the top of the bar.',
        '**Assisted pull-up machine.**',
        '**Weighted pull-ups with a dip belt.**',
        '**Lat pulldowns with the long bar, wide grip:** back angle, then front angle, 3 slow reps. Close-up: the wide grip.',
        '**Chest-supported T-bar rows, widest grip:** side angle, 3 slow reps. Close-ups: the wide grip on the handles; the squeeze at the top.',
        '**Barbell T-bar rows.**',
        '**Seated cable rows with the wide grip handle:** side angle. Close-ups: swapping the narrow handle for the wide one and clipping it on; shoulder blades squeezing.',
        '**Rear delt machine:** back angle.',
        '**Side angle only (skip these first if you run short on time):** single-arm dumbbell rows; barbell bent-over rows.']),
    ('Shoulders', [
        '**Shoulder press machine:** side angle, 3 slow reps. Close-ups: setting the seat; arms stopping at 90 degrees at the bottom.',
        '**Side lateral machine:** front angle.',
        '**Dumbbell side laterals:** front angle with the mirror behind. Close-up: dumbbells stopping at shoulder height.']),
    ('Chest', [
        '**Chest fly machine:** front angle, 3 slow reps. Close-ups: setting the seat; setting the starting position; the squeeze in front of the chest.',
        '**Dumbbell chest flies:** front angle, elbows bent 45 to 90 degrees. Close-up: the bottom of the rep, the press turning into a fly.',
        '**Chest press machine:** side angle, 3 slow reps. Close-ups: setting the seat and the range; handles at mid-chest.',
        '**Incline dumbbell press:** side angle, 3 slow reps. Dumbbells upright on the knees, lie back, flip them up; lower to just above chest level.',
        '**Dips:** side angle, upright with a slight lean. The assisted dip machine; bodyweight dips; weighted dips with your chain (about 20 lb), plus a close-up of the chain.',
        '**Side angle only (skip these first if you run short on time):** cable crossovers.']),
    ('Arms', [
        '**Cable curls:** side angle. Close-ups: elbows pinned; arms straight at the bottom.',
        '**Tricep pushdowns with the bar:** side angle, close-up of the lockout. Plus the rope pushdown.',
        '**Overhead rope tricep extensions:** side angle.',
        '**Rope hammer curls on the cable.**',
        '**EZ bar preacher curls:** side angle. Close-ups: armpits tight to the pad, elbows down; lowering to almost straight.',
        '**Dumbbell curls into a drop set:** heavy pair to the last rep, rack them, lighter pair, keep going.',
        '**Straight bar curls:** side angle.',
        '**EZ bar curls:** side angle.']),
    ('Talking at the gym, with the DJI mic', [
        '**Finish a set, then talk to camera while walking between sets** on the HOG center mats.',
        '**Talk to camera on the stretching mats** after the workout.']),
]
BROLL_NOTE = ('Every exercise: 16:9, 4K, 3 slow full reps, a 2 second hold before and after, room for a vertical crop. '
              'Side angle, then front angle, then the close-ups listed.')

def broll_doc(title):
    parts, seq = ['<html><head><meta charset="utf-8"></head><body>', '<h1>%s</h1>' % html.escape(title)], [title]
    parts.append('<p %s>%s</p>' % (PST, html.escape(BROLL_NOTE))); seq.append(BROLL_NOTE)
    for g, lst in BROLL_DOC:
        parts.append('<h2>%s</h2>' % html.escape(g)); seq.append(g)
        parts.append('<ul>' + ''.join('<li %s>%s</li>' % (PST, linkify(b)) for b in lst) + '</ul>'); seq.extend(plain(b) for b in lst)
    parts.append('</body></html>')
    return '\n'.join(parts), seq

if __name__ == '__main__':
    P, pend = load(sys.argv[1]); out_dir, prefix = sys.argv[2], sys.argv[3]; os.makedirs(out_dir, exist_ok=True)
    DOC_TITLE = '%s - Filming Document' % prefix
    BROLL_URL = sys.argv[4] if len(sys.argv) > 4 else None       # link to the B-roll document, once it exists
    print('pending suggestion runs in the source (read as accepted):', pend)
    intro, fa_h2, fa_note, lf_h2, items = parse(P)
    for it in items:
        for kd, t in it['paras']:
            if kd in ('SAY', 'HOOK') and ('[' in t or ']' in t): print('BRACKET IN SPOKEN LINE:', it['title'], t)
            if kd == 'EMPTY' and it['type'] != 'follow': pass
            if kd == 'HOOK' and it['type'] != 'short': print('BULLET OUTSIDE A SHORT:', it['title'], t)
    shorts = [it for it in items if it['type'] == 'short']
    num = lambda it: int(it['title'].split('.')[0])
    assert [num(s) for s in shorts] == list(range(1, len(shorts) + 1)), 'shorts not numbered 1..N in order'
    docs = [('%s - Teleprompter 1 - Long Form' % prefix, [it for it in items if it['type'] == 'long'] + [it for it in items if it['type'] == 'follow']),
            ('%s - Teleprompter 2 - Short Form (Part 1 of 2)' % prefix, [s for s in shorts if num(s) <= 15]),
            ('%s - Teleprompter 3 - Short Form (Part 2 of 2)' % prefix, [s for s in shorts if num(s) >= 16])]
    built = {}
    for name, lst in docs:
        h, seq = teleprompter(lst); open(os.path.join(out_dir, name + '.html'), 'w').write(h); built[name] = seq
        w = sum(words(it) for it in lst)
        print('%s: %d scripts, %d words, about %d pages' % (name, len(lst), w, round(w / 570)))
        for it in lst: print('    %5d  %s' % (words(it), it['tp_title']))
    flat = ' '.join(t for seq in built.values() for t in seq)
    print('teleprompter, must all be 0: brackets', flat.count('[') + flat.count(']'), '| http', flat.count('http'),
          '| "spoken words"', flat.count('spoken words'), '| HOOK TAKES', flat.count('HOOK TAKES'),
          '| id lines', len(re.findall(r'\bRO-\d+\.', flat)), '| "-" lines', sum(1 for s in built.values() for t in s if t == '-'))
    h, seq = filming(intro, fa_h2, fa_note, lf_h2, items, broll_list(items))
    open(os.path.join(out_dir, DOC_TITLE + '.html'), 'w').write(h); built[DOC_TITLE] = seq
    print('%s: %d lines, %d words' % (DOC_TITLE, len(seq), sum(len(t.split()) for t in seq)))
    bt = '%s - B-Roll Shot List' % prefix
    h, seq = broll_doc(bt); open(os.path.join(out_dir, bt + '.html'), 'w').write(h); built[bt] = seq
    print('%s: %d shots' % (bt, sum(len(l) for _, l in BROLL_DOC)))
    json.dump(built, open(os.path.join(out_dir, 'built_seq.json'), 'w'), ensure_ascii=False, indent=0)
