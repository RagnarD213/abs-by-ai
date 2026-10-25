"""RO-24 round 3: the facts the background planner reads (gsbg planner.py), on the new timeline. Who he talks about, the
numbers he says, where he talks about a transformation, every full-screen insert, the clip footage and photo pools.
Also writes plan overrides (bg_overrides.json): the editor's calls where the rules allow two answers.

  python3 facts_r3.py   ->  facts.json, bg_overrides.json
"""
import json, pathlib, sys
R2 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round2'); R3 = pathlib.Path('/Volumes/Expansion/_edit_work/RO-24/round3')
sys.path.insert(0, str(R3 / 'recipe')); import timeline_r3 as TL
FPS = 30000 / 1001
OW = json.load(open(R2 / 'film_words.json'))
E = json.load(open(R3 / 'edl_r3.json')); M = json.load(open(R3 / 'manifest_r2_mapped.json'))
INS = json.load(open(R3 / 'clips/inserts.json'))


def w(phrase, lo, hi=None):
    """old film start time of `phrase` (first word) at or after lo"""
    toks = phrase.lower().split()
    for i, x in enumerate(OW):
        if x['t0'] < lo - 0.01 or (hi and x['t0'] > hi): continue
        if all(i + k < len(OW) and OW[i + k]['w'].lower().strip('.,?!') .startswith(t.strip('.,?!')) for k, t in enumerate(toks)):
            return x['t0']
    raise SystemExit(f'not found: {phrase} after {lo}')


S = TL.shift_t
P = lambda *a: [f'../round2/photos/{x}' if '/' in x and not x.startswith('photos/') else x for x in a]
R2P = lambda f: f'../round2/photos/{f}'
R3P = lambda f: f'photos/{f}'

people = {
 'Sharon Osbourne': dict(
    # clean shots of her in the full E! News video (no quote boxes over her): interview close-ups, Emmys, MS gala, podcast
    clip=dict(src='clips/src/sharon_full.mp4', windows=[[52.0, 57.9], [66.0, 71.9], [6.0, 7.9], [36.0, 37.8], [82.0, 83.6], [118.0, 124.0]],
              after=[[12.0, 17.6], [88.0, 91.9]], focus=[0.45, 0.4]),
    stat='42 lb, Ozempic', big=['-42 LB', 'OZEMPIC'],
    photos=[R2P('sharon/sharon_a_recent_gaunt_2023_mayfair.jpg'), R3P('sharon/sharon_before_2019_emmys.jpg'),
            R3P('sharon/sharon_after_2024_chateau_marmont.jpg'), R2P('sharon/sharon_c_before_2012.jpg')],
    pairs=[dict(photos=[R3P('sharon/sharon_before_2019_million_little_pieces.jpg'), R3P('sharon/sharon_after_2025_villa_park_announcement.jpg')],
                years=['2019', '2025'], credits=['Getty Images', 'Samir Hussein/Getty Images for Live Nation UK'], crop_k=6.0),
           dict(photos=[R3P('sharon/sharon_before_2021_the_talk_set.jpg'), R2P('sharon/sharon_a_recent_gaunt_2023_mayfair.jpg')],
                years=['2021', '2023'], credits=['CBS via Getty Images', 'Splash News'], crop_k=3.6, top=0.7)]),
 'Fat Joe': dict(
    clip=dict(src='clips/src/fatjoe_full.mp4', windows=[[26.0, 31.9], [38.0, 43.5], [4.5, 13.5]], after=[[4.5, 13.5], [26.0, 31.9]], focus=[0.5, 0.4]),
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
         side_cards=[dict(t0=m['a'], t1=m['b']) for m in M if m['kind'] == 'overlay'])
json.dump(F, open(R3 / 'facts.json', 'w'), indent=1)
print('facts:', len(shots), 'shots,', len(F['inserts']), 'inserts')

# ---- the editor's calls where the rules allow two answers (first three minutes; round 4 reviews the rest)
SH = 'clips/src/sharon_full.mp4'
OVR = {
 'BG04': dict(pair=dict(photos=[R3P('sharon/sharon_before_2021_the_talk_set.jpg'), R3P('sharon/sharon_after_2025_villa_park_announcement.jpg')],
                        years=['2021', '2025'], credits=['CBS via Getty Images', 'Samir Hussein/Getty Images for Live Nation UK'], crop_k=6.0, top=0.6),
              why='her own fault, Ozempic face: her before and after with 42 lb, Ozempic (a pair the photo scenes do not use)'),
 'BG05': dict(clip=dict(src=SH, windows=[[52.0, 57.9], [66.0, 71.9]], zoom=1.22, focus=[0.47, 0.42], out_focus=[0.33, 0.44]),
              why="blaming the medication, overdosing: her clip behind, Dan to the side (Dan: occasionally)"),
 'BG07': dict(type='set', clip=dict(src=SH, windows=[[6.0, 7.9], [36.0, 37.8], [118.0, 124.0], [82.0, 83.6], [12.0, 17.6]]),
              why='commentary (scare tactics, skeletons): the studio set, her clip on its TV'),
 'BG08': dict(type='soft', clip=dict(src=SH, windows=[[88.0, 91.9], [66.0, 71.9]]),
              why='commentary (very unlikely you would get this gaunt): her clip softened behind him'),
 'BG09': dict(type='cards', photos=[R3P('sharon/sharon_before_2019_emmys.jpg'), R3P('sharon/sharon_after_2024_chateau_marmont.jpg'),
                                    R2P('sharon/sharon_c_before_2012.jpg'), R2P('sharon/sharon_a_recent_gaunt_2023_mayfair.jpg'),
                                    R3P('sharon/sharon_before_2019_million_little_pieces.jpg'), R2P('sharon/sharon_b_face_closeup_2023_claridges.jpg')],
              why='ending up looking like Sharon Osbourne: her photos, before and after, floating around him'),
}
json.dump(OVR, open(R3 / 'bg_overrides.json', 'w'), indent=1)
