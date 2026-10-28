"""RO-24 round 4 (from round 3's facts_r3.py, whole film): the facts the background planner reads (gsbg planner.py), on the new timeline. Who he talks about, the
numbers he says, where he talks about a transformation, every full-screen insert, the clip footage and photo pools.
Also writes plan overrides (bg_overrides.json): the editor's calls where the rules allow two answers.

  python3 facts_r4.py   ->  film_manifest_r4.json, facts.json, bg_overrides.json (round4/), then the planner
"""
import json, pathlib, sys
R2 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round2'); R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3'); R4 = R3.parent / 'round4'
sys.path.insert(0, str(R3 / 'recipe')); import timeline_r3 as TL
sys.path.insert(0, str(R4 / 'recipe')); from retime_r4 import r4_t, AT as RT_AT, CUT as RT_CUT
FPS = 30000 / 1001
OW = json.load(open(R2 / 'film_words.json'))
E = json.load(open(R4 / 'edl_r4.json'))                  # round 3 cut, Tracy's insert 66 frames shorter (retime_r4.py)
# ---- round 4 manifest: round 3's, with P4-P7 rebuilt (round4/hf) and G12/G14 re-rendered (round4/hf/gfx)
MAN = json.load(open(R3 / 'film_manifest_r3.json'))
NEWP = {m['id']: m for m in json.load(open(R4 / 'hf/photos_manifest.json'))}
FPS_ = 30000 / 1001
for m in MAN:
    if m['id'] != 'C_tracy' and m['a'] >= RT_AT / FPS_ - 1e-3: m['a'] = round(r4_t(m['a']), 4); m['b'] = round(r4_t(m['b']), 4)
    if m['id'] == 'C_tracy': m['b'] = round(RT_AT / FPS_, 4)
    if m['id'] in NEWP: m.update(a=NEWP[m['id']]['a'], b=NEWP[m['id']]['b'], mov=NEWP[m['id']]['mov'])
    if m['id'] in ('G12', 'G14'):
        m['mov'] = str(R4 / f"hf/gfx/renders/{m['id']}.mov")
        if m.get('mask'): m['mask'] = str(R4 / f"hf/gfx/renders/{m['id']}_mask.mov")
MAN.sort(key=lambda m: m['a'])
for x, y in zip(MAN, MAN[1:]):
    if x['kind'] == 'opaque' and y['kind'] == 'opaque': assert x['b'] <= y['a'] + 1e-3, (x['id'], y['id'])
json.dump(MAN, open(R4 / 'film_manifest_r4.json', 'w'), indent=1)
M = [m for m in MAN if not m['id'].startswith('C_')]      # the clip inserts come from the EDL below
INS = json.load(open(R3 / 'clips/inserts.json'))


def w(phrase, lo, hi=None):
    """old film start time of `phrase` (first word) at or after lo"""
    toks = phrase.lower().split()
    for i, x in enumerate(OW):
        if x['t0'] < lo - 0.01 or (hi and x['t0'] > hi): continue
        if all(i + k < len(OW) and OW[i + k]['w'].lower().strip('.,?!') .startswith(t.strip('.,?!')) for k, t in enumerate(toks)):
            return x['t0']
    raise SystemExit(f'not found: {phrase} after {lo}')


S = lambda t: r4_t(TL.shift_t(t))
W = lambda phrase, lo: round(S(w(phrase, lo)), 3)
P = lambda *a: [f'../round2/photos/{x}' if '/' in x and not x.startswith('photos/') else x for x in a]
R2P = lambda f: f'../round2/photos/{f}'
R3P = lambda f: f'photos/{f}'

people = {
 'Sharon Osbourne': dict(
    # clean shots of her in the full E! News video (no quote boxes over her): interview close-ups, Emmys, MS gala, podcast
    # (windows on measured shot changes: ffmpeg scene detection + an exact-time 1 fps sheet, clips/sharon_full_sheet_exact.jpg)
    # only steady stretches: no flashes, no transitions (R3 review F1/F2; flicker scan in the round 3 notes)
    clip=dict(src='clips/src/sharon_full.mp4', windows=[[54.6, 58.8], [12.4, 16.8], [88.5, 91.8], [119.1, 120.9]],
              after=[[12.4, 16.8], [54.6, 58.8]], focus=[0.45, 0.4]),
    stat='42 lb, Ozempic', big=['-42 LB', 'OZEMPIC'],
    photos=[R2P('sharon/sharon_a_recent_gaunt_2023_mayfair.jpg'), R3P('sharon/sharon_before_2019_emmys.jpg'),
            R3P('sharon/sharon_after_2024_chateau_marmont.jpg'), R2P('sharon/sharon_c_before_2012.jpg')],
    pairs=[dict(photos=[R3P('sharon/sharon_before_2019_million_little_pieces.jpg'), R3P('sharon/sharon_after_2025_villa_park_announcement.jpg')],
                years=['2019', '2025'], credits=['Getty Images', 'Samir Hussein/Getty Images for Live Nation UK'], crop_k=6.0),
           dict(photos=[R3P('sharon/sharon_before_2021_the_talk_set.jpg'), R2P('sharon/sharon_a_recent_gaunt_2023_mayfair.jpg')],
                years=['2021', '2023'], credits=['CBS via Getty Images', 'Splash News'], crop_k=3.6, top=0.7)]),
 'Fat Joe': dict(
    clip=dict(src='clips/src/fatjoe_full.mp4', windows=[[25.6, 30.8], [39.0, 42.8], [6.0, 8.75]], after=[[6.0, 8.75], [25.6, 30.8], [39.0, 40.6]], focus=[0.5, 0.4]),
    stat='200 lb, Ozempic', big=['-200 LB', 'OZEMPIC'],
    photos=[R2P('fatjoe/fatjoe_a_heaviest_2005.jpg'), R2P('fatjoe/fatjoe_b_recent_2023.jpg')],
    # P0 shows MTV TRL 2002 / ESPYs 2026, P3 Brown Sugar 2002 / Fanatics 2024: the panel gets the third pair
    pairs=[dict(photos=[R2P('fatjoe/fatjoe_a_heaviest_2005.jpg'), R2P('fatjoe/fatjoe_b_recent_2023.jpg')],
                years=['2005', '2023'], credits=['Timothy M. Moore (Wikimedia Commons)', 'Musicindustryscholar (Wikimedia Commons)'], crop_k=3.6, top=0.6)]),
 'Amy Schumer': dict(
    clip=dict(src='clips/src/amy.mp4', windows=[[12.42, 28.84]]), stat='50 lb, Mounjaro', big=['-50 LB', 'MOUNJARO'],
    photos=[R2P('amy/amy_recent_slim_2025_street.jpg')],
    pairs=[dict(photos=[R3P('amy/amy_before_2024_variety-power-of-women.jpg'), R3P('amy/amy_after_2026_lorne-premiere.jpg')],
                years=['2024', '2026'], credits=['George Chinsee/Variety via Getty Images', 'Cindy Ord/WireImage'], crop_k=6.5)]),
 'Meghan Trainor': dict(
    clip=dict(src='clips/src/meghan.mp4', windows=[[7.7, 24.3]]), stat='60 lb, Mounjaro', big=['-60 LB', 'MOUNJARO'],
    photos=[R2P('meghan/meghan_recent_slim_2025_the_paper_premiere.jpg')],
    pairs=[dict(photos=[R3P('meghan/meghan_before_2020_tommynow-london-fashion-week.jpg'), R2P('meghan/meghan_recent_slim_2025_baby2baby_gala.jpg')],
                years=['2020', '2025'], credits=['Mike Marsland/WireImage', 'Aude Guerrucci/Reuters'], crop_k=6.5)]),
 'Oprah Winfrey': dict(
    clip=dict(src='clips/src/oprah.mp4', windows=[[8.66, 23.4]]), stat='Down to 155 lb, GLP-1', big=['155 LB', 'GLP-1'],
    photos=[R2P('oprah/oprah_recent_2025_sydney.jpg')],
    pairs=[dict(photos=[R3P('oprah/oprah_before_2022_tiff-sidney-premiere.jpg'), R2P('oprah/oprah_recent_2025_abt_gala.jpg')],
                years=['2022', '2025'], credits=['Getty Images', 'Eugene Gologursky/Getty Images for American Ballet Theatre'], crop_k=6.5)]),
 'Tracy Morgan': dict(
    clip=dict(src='clips/src/tracy.mp4', windows=[[11.3, 24.64]]), stat='On Ozempic, gained 40 lb', big=['+40 LB', 'OZEMPIC'],
    photos=[R3P('tracy/tracy_after_2025_snl50-red-carpet.jpg'), R2P('tracy/tracy_recent_2026_tribeca_closeup.jpg')], pairs=[]),
}
# round 4: clean, steady muted-footage windows for the four later clips (whole source videos, scene-detected, flicker-scanned)
_CW = R4 / 'clipwin/windows.json'
if _CW.exists():
    _NM = {'amy': 'Amy Schumer', 'meghan': 'Meghan Trainor', 'oprah': 'Oprah Winfrey', 'tracy': 'Tracy Morgan'}
    for k, v in json.load(open(_CW)).items():
        people[_NM[k]]['clip'] = {x: v[x] for x in ('src', 'windows', 'after', 'focus', 'zoom', 'out_focus') if v.get(x)}
else:
    print('WARNING: no round4/clipwin/windows.json yet: the later clips keep round 3 defaults')
people['Oprah Winfrey']['clip'].update(windows=[[3223.52, 3226.81], [3250.5, 3253.59], [3272.27, 3277.07], [3259.26, 3261.26]],
                                     after=[[3223.52, 3226.81], [3250.5, 3253.59], [3272.27, 3277.07]])   # 3238.37-3244.37 dropped: her fist pumps beside Dan's head (review 4)
everyone = [R2P('fatjoe/fatjoe_a_heaviest_2005.jpg'), R2P('oprah/oprah_recent_2025_abt_gala.jpg'), R3P('amy/amy_before_2024_variety-power-of-women.jpg'),
            R3P('meghan/meghan_before_2019_star-wars-premiere-london.jpg'), R2P('sharon/sharon_a_recent_gaunt_2023_rollingstone_uk.jpg'), R2P('tracy/tracy_recent_2023_gotham_ball.jpg'),
            R2P('fatjoe/fatjoe_a_heaviest_2002.jpg'), R2P('oprah/oprah_recent_2024_critics_choice.jpg'),
            R2P('amy/amy_recent_slim_2025_red_dress.jpg'), R2P('meghan/meghan_recent_slim_2025_billboard.jpg'),
            R2P('sharon/sharon_a_recent_gaunt_2023_rollingstone_uk.jpg'), R3P('tracy/tracy_after_2025_snl50-red-carpet.jpg'),
            R2P('fatjoe/fatjoe_b_recent_2024.jpg'), R3P('amy/amy_before_2023_good-foundation-carnegie-hall.jpg'),
            R3P('meghan/meghan_before_2019_star-wars-premiere-london.jpg'), R3P('oprah/oprah_before_2023_wes-moore-reception.jpg'),
            R2P('sharon/sharon_c_before_2012.jpg'), R2P('tracy/tracy_recent_2023_gotham_ball.jpg'),
            R2P('fatjoe/fatjoe_a_heaviest_2005.jpg'), R2P('oprah/oprah_recent_2025_abt_gala.jpg'),
            R2P('amy/amy_earlier_2025_premiere.jpg'), R2P('meghan/meghan_recent_slim_2025_the_paper_premiere.jpg'),
            R3P('sharon/sharon_before_2019_emmys.jpg'), R3P('fatjoe/fatjoe_after_2026_espy-awards.jpg'),
            R3P('amy/amy_after_2026_lorne-premiere.jpg'), R3P('meghan/meghan_before_2020_tommynow-london-fashion-week.jpg'),
            R3P('oprah/oprah_before_2022_tiff-sidney-premiere.jpg'), R3P('sharon/sharon_after_2025_villa_park_announcement.jpg'),
            R2P('tracy/tracy_recent_2026_tribeca_closeup.jpg'), R2P('oprah/oprah_recent_2025_sydney.jpg')]

# who he talks about (old film seconds -> new)
sec = [(22.59, 114.75, 'Sharon Osbourne'), (114.75, 166.10, 'Fat Joe'), (180.11, 233.39, 'Amy Schumer'),
       (233.39, 287.02, 'Meghan Trainor'), (287.02, 301.17, 'Oprah Winfrey'), (301.17, 306.76, 'Tracy Morgan')]
nums = [(w('2', 76.0, 81.0), ['2.5 MG', 'OR LESS'], 'Sharon Osbourne'),
        (w('480', 116.0), ['-200 LB', 'OZEMPIC'], 'Fat Joe'),
        (w('30', 182.0), ['-30 LB', 'OZEMPIC'], 'Amy Schumer'),
        (w('20', 293.0), ['+20 LB', 'IN A YEAR OFF'], 'Oprah Winfrey'),
        (w('1', 331.5, 334.0), ['1.5 MG', 'A WEEK'], None)]
trans = [(46.91, 57.82, 'Sharon Osbourne'), (106.07, 114.75, 'Sharon Osbourne'), (141.66, 150.74, 'Fat Joe'),
         (189.84, 195.0, 'Amy Schumer'), (245.81, 252.0, 'Meghan Trainor')]

shots, inserts = [], []
for it in E['items']:
    t0, t1 = it['o0'] / FPS, it['o1'] / FPS
    if it['kind'] == 'shot': shots.append(dict(t0=round(t0, 4), t1=round(t1, 4), framing=it['framing']))
    else: inserts.append(dict(t0=round(t0, 4), t1=round(t1, 4), kind='clip', person=it['clip']))
for m in M:
    if m['kind'] == 'opaque':
        inserts.append(dict(t0=m['a'], t1=m['b'], kind='intro' if m['id'] == 'P0' else ('photo' if m['id'].startswith('P') else 'card'), id=m['id']))
# merge shots cut by an opaque item: the planner works on what is on screen
F = dict(shots=shots, inserts=sorted(inserts, key=lambda x: x['t0']), people=people, everyone=everyone,
         sections=[dict(t0=S(a), t1=S(b), person=p) for a, b, p in sec],
         numbers=[dict(t=S(t), lines=l, person=p) for t, l, p in nums],
         transformations=[dict(t0=S(a), t1=S(b), person=p) for a, b, p in trans],
         side_cards=[dict(t0=m['a'], t1=m['b']) for m in M if m['kind'] == 'overlay'],
         lower_thirds=[dict(t0=m['a'], t1=m['b'], id=m['id']) for m in M if m['kind'] == 'glass'])
json.dump(F, open(R4 / 'facts.json', 'w'), indent=1)
print('facts:', len(shots), 'shots,', len(F['inserts']), 'inserts')

# ---- the editor's calls where the rules allow two answers (first three minutes; round 4 reviews the rest)
SH = 'clips/src/sharon_full.mp4'
OVR = {
 'BG01': dict(photos=[R2P('fatjoe/fatjoe_a_heaviest_2005.jpg'), R2P('oprah/oprah_recent_2025_abt_gala.jpg'), R3P('amy/amy_before_2024_variety-power-of-women.jpg'),
                      R3P('meghan/meghan_before_2019_star-wars-premiere-london.jpg'), R2P('tracy/tracy_recent_2023_gotham_ball.jpg')],
              why='right after the intro: five cards, one per person not in the next photo scene (Sharon comes next, so no Sharon card)'),
 'BG03': dict(clip=dict(src=SH, windows=[[12.4, 16.8], [54.6, 58.8]], zoom=1.35, focus=[0.47, 0.42], out_focus=[0.45, 0.5]),
              why="right after Sharon Osbourne's clip: it keeps rolling, Dan reacts from the corner (zoomed so E!'s corner logo stays out of his corner)"),
 'BG04': dict(pair=dict(photos=[R3P('sharon/sharon_before_2021_the_talk_set.jpg'), R3P('sharon/sharon_after_2025_villa_park_announcement.jpg')],
                        years=['2021', '2025'], credits=['CBS via Getty Images', 'Getty Images for Live Nation UK'], crop_k=6.0, top=0.6),
              why='her own fault, Ozempic face: her before and after with 42 lb, Ozempic (a pair the photo scenes do not use)'),
 'BG05': dict(clip=dict(src=SH, windows=[[54.6, 58.8], [119.1, 120.9], [12.4, 16.8], [6.1, 7.85]], zoom=1.5, focus=[0.47, 0.42], out_focus=[0.33, 0.44]),
              why="blaming the medication, overdosing: her clip behind, Dan to the side (Dan: occasionally); zoomed so the E! logo stays off him"),
 'BG06': dict(lines=['ZEPBOUND', '2.5 MG', 'OR LESS'], line_times=[S(69.20) + 0.1, W('2', 78.0), W('or less', 78.5)], t1=S(86.25),
              why='he says the number: the drug from the cut ("high doses of Zepbound"), the dose lands on "2.5mg or less" and stays through "That\'s all you need"'),
 'BG07': dict(type='set', t0=S(86.25), clip=dict(src=SH, windows=[[54.6, 58.8], [12.4, 16.8], [88.5, 91.8]]),
              why='commentary (scare tactics, skeletons): the studio set, her clip on its TV (three steady stretches)'),
 'BG08': dict(type='soft', clip=dict(src=SH, windows=[[88.5, 91.8], [54.6, 58.8], [12.4, 13.2]]),
              why='commentary (very unlikely you would get this gaunt): her clip softened behind him'),
 'BG09': dict(type='cards', photos=[R3P('sharon/sharon_before_2019_emmys.jpg'), R3P('sharon/sharon_after_2024_chateau_marmont.jpg'),
                                    R2P('sharon/sharon_c_before_2012.jpg'), R2P('sharon/sharon_a_recent_gaunt_2023_rollingstone_uk.jpg')],
              why='ending up looking like Sharon Osbourne: four of her photos, the two not shown yet and the two seen longest ago'),
 'BG10': dict(clip=dict(src='clips/src/fatjoe_full.mp4', windows=[[6.0, 8.75], [25.6, 30.8], [39.0, 40.6]], focus=[0.5, 0.4]),
              why="right after Fat Joe's clip: it keeps rolling (steady stretches, no flashing carpets), Dan reacts from the corner"),
}
_cards = set(OVR['BG01']['photos'])
OVR['BG02'] = dict(photos=[p for p in everyone + [R3P('meghan/meghan_before_2020_tommynow-london-fashion-week.jpg'), R2P('fatjoe/fatjoe_b_recent_2023.jpg'),
                                                  R2P('meghan/meghan_recent_slim_2025_baby2baby_gala.jpg'), R2P('amy/amy_recent_slim_2025_street.jpg')]
                           if 'sharon' not in p and p not in _cards],
                   why='right after the intro: the photo wall, without Sharon (her photo scene comes next) and without the five intro cards')

# ---- round 4: the editor's calls after 2:50 (the planner's defaults, read line by line against what he says). Keyed by the
# segment that contains the time, so a changed id (BG24 is gone: P7 now starts where Tracy's clip ends) cannot misplace them.
sys.path.insert(0, '/Users/danielrose/Projects/Claude/Projects/Abs By AI/.claude/skills/_shared/greenscreen-bg'); import planner as PL
FJ = people['Fat Joe']['clip']; AMY = people['Amy Schumer']['clip']
RECENT = {'amy_before_2024_variety-power-of-women', 'amy_after_2026_lorne-premiere', 'meghan_before_2019_star-wars-premiere-london',
          'meghan_recent_slim_2025_the_paper_premiere', 'oprah_before_2022_tiff-sidney-premiere', 'oprah_recent_2025_abt_gala',
          'tracy_recent_2026_tribeca_closeup', 'meghan_before_2020_tommynow-london-fashion-week', 'meghan_recent_slim_2025_baby2baby_gala'}   # P4-P7 and the Meghan panel
ALLP = sorted(R2P(f'{q.parent.name}/{q.name}') for q in (R2 / 'photos').glob('*/*.jpg') if not q.name.startswith('._')) + \
       sorted(R3P(f'{q.parent.name}/{q.name}') for q in (R3 / 'photos').glob('*/*.jpg') if not q.name.startswith('._'))
WALL_SKIP = {pathlib.Path(p).stem for p in [R2P('amy/amy_recent_slim_2025_street.jpg'), R2P('oprah/oprah_recent_2025_sydney.jpg'), R2P('tracy/tracy_recent_2023_gotham_ball.jpg'), R2P('meghan/meghan_recent_slim_2025_billboard.jpg'), R3P('sharon/sharon_after_2024_chateau_marmont.jpg')]} | {'fatjoe_a_heaviest_2005', 'fatjoe_b_recent_2023', 'amy_recent_slim_2025_red_dress', 'oprah_before_2023_wes-moore-reception', 'oprah_recent_2024_critics_choice'}   # the 5:46 cards, the blurred photos, the Fat Joe panel
AT = [
 (175.0, dict(type='cards', person='Fat Joe', clip=None, photos=[R3P('fatjoe/fatjoe_before_2002_mtv-trl-times-square.jpg'), R2P('fatjoe/fatjoe_a_heaviest_2002.jpg'),
                                                                   R2P('fatjoe/fatjoe_b_recent_2024.jpg'), R3P('fatjoe/fatjoe_after_2026_espy-awards.jpg')],
              why="'he lost the weight over years by cutting carbs and by training': four of his photos across the years as floating cards "
                  "(his Page Six video has camera flashes or quote boxes on almost every frame; the round 4 review caught flashes behind you here)")),
 (200.0, dict(type='bigtype', person='Fat Joe', clip=None, photos=None, lines=['HUGE DOSE', '-20 LB', 'MICRODOSE'], line_times=[198.87, 203.31, 204.15],
              why="he says the numbers: 'HUGE DOSE' lands on 'a huge dose', '-20 LB' on 'losing 20 pounds', 'MICRODOSE' on 'on a microdose' (his photos are all used by "
                  "the cards and panel either side, and his footage flashes)")),
 (220.0, dict(type='soft', person='Fat Joe', clip=None, photos=[R2P('fatjoe/fatjoe_b_recent_2023.jpg')],
              why="'use it to make your diet easier... cut the carbs you overeat and keep training' is Fat Joe's lesson, and Amy is not "
                  "introduced until the next line: his 2023 photo softened behind (his one flash-free stretch of footage is only 2.3 s, and looping it read as a stutter: review 4)")),
 (260.0, dict(type='set', person='Amy Schumer',
              why="his friends who could not take the side effects, switched to Zepbound and got results: the studio set with Amy's "
                  "Howard Stern interview on its TV (she switched too); side was the planner's pick but she is not who he is talking about here")),
 (290.0, dict(type='soft', person='Amy Schumer', clip=dict(src=AMY['src'], windows=AMY['windows'], **{x: AMY[x] for x in ('focus', 'zoom') if x in AMY}),
              why="'if you tried Ozempic and it made you sick': Amy's clip (she got sick on Ozempic) softened behind; the set was just used")),
 (315.0, dict(clip=dict(src=people['Meghan Trainor']['clip']['src'], windows=[[13.0, 18.95], [72.42, 76.86]], **{x: people['Meghan Trainor']['clip'][x] for x in ('focus', 'zoom', 'out_focus') if x in people['Meghan Trainor']['clip']}),
              why="right after Meghan Trainor's clip: her two long clean shots keep rolling while Dan reacts from the corner (her short shots cut three "
                  "times and looped a 1 s scrap here: review 4)")),
 (340.0, dict(type='bigtype', person=None, clip=None, photos=None, lines=['7 DAYS', 'A WEEK'], line_times=[340.65, 341.13],
              why="he says the number: '7 DAYS' lands on 'seven days', 'A WEEK' on 'a week' (Meghan's interview has too few clean shots to fill the TV again)")),
 (350.0, dict(type='cards', person=None, clip=None, photos=[R2P('amy/amy_recent_slim_2025_street.jpg'), R2P('oprah/oprah_recent_2025_sydney.jpg'), R2P('tracy/tracy_recent_2023_gotham_ball.jpg'), R2P('meghan/meghan_recent_slim_2025_billboard.jpg'), R3P('sharon/sharon_after_2024_chateau_marmont.jpg')],
              why="'lifting weights and eating a high protein diet is mandatory... if you can't do these things, you shouldn't even start': "
                  "floating cards of the people this film covers (Meghan's interview has only two clean long shots, both used just before; "
                  "review 3 caught a 16-frame scrap of a third shot here)")),
 (358.0, dict(clip=None, photos=[R2P('amy/amy_recent_slim_2025_red_dress.jpg')],
              why="a left-third card is up: calm background, Dan to the side, a blurred Amy photo (no more Meghan footage: review 4 found it cutting and looping)")),
 (r4_t(430.0), dict(type='wall', photos=[p for p in dict.fromkeys(everyone + ALLP) if pathlib.Path(p).stem not in RECENT | WALL_SKIP][:24],
              why="'nearly everyone regains the weight they lost if they stop': the wall of all of them (no new idea for a person here)")),
 (r4_t(440.0), dict(lines=['1.5 MG', 'A WEEK'], line_times=[r4_t(438.93), r4_t(439.99)],
              why="he says his dose: '1.5mg' lands on '1 .5mg', 'A WEEK' on 'per week'")),
 (r4_t(455.0), dict(type='set', person='Amy Schumer', photos=None, clip=dict(src=AMY['src'], windows=[[62.15, 66.06], [13.03, 17.15], [40.29, 46.29]], focus=AMY['focus']),
              why="'maintaining your weight effortless': the studio set with Amy's interview on its TV (Fat Joe's photos had already been "
                  "used several times; review 2 caught them back to back here)")),
 (r4_t(468.0), dict(type='soft', person=None, clip=None, photos=[R3P('oprah/oprah_before_2023_wes-moore-reception.jpg')],
              why="a left-third card is up (step down slowly): calm background, Dan to the side, a blurred Oprah photo")),
 (r4_t(480.0), dict(type='set', person='Oprah Winfrey', clip=dict(src=people['Oprah Winfrey']['clip']['src'], windows=[[3223.52, 3226.81], [3272.27, 3277.07]],
                                                          **{x: people['Oprah Winfrey']['clip'][x] for x in ('focus',) if x in people['Oprah Winfrey']['clip']}),
              why="'far better results than stopping suddenly': Oprah, who stopped and regained, on the set's TV (not the pair the set before showed)")),
 (r4_t(510.0), dict(type='soft', person='Oprah Winfrey', clip=None, photos=[R2P('oprah/oprah_recent_2024_critics_choice.jpg')],
              why="the close and the end screen: calm background, Dan centre where the end-screen buttons were measured (round 2 window), "
                  "Oprah's photo softened behind (her footage cut 2 frames before Dan's cut here: review 4)")),
]
P = PL.plan(json.load(open(R4 / 'facts.json')))['segments']
for t, ov in AT:
    seg = next(x for x in P if x['t0'] <= t < x['t1'])
    assert seg['id'] not in OVR, seg['id']
    OVR[seg['id']] = ov
    print(f"override {seg['id']} {seg['t0']:.1f}-{seg['t1']:.1f}: {seg['type']} -> {ov.get('type', seg['type'])}")
json.dump(OVR, open(R4 / 'bg_overrides.json', 'w'), indent=1)
