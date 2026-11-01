#!/usr/bin/env python3
"""Alcohol And Abs Shorts (SL-10) cover prompts, 2026-11-01. Writes one prompt file per image.

A/B/D/E: Codex AI Dan. C: Codex empty plate for a real studio cutout. F/G/H: the three Google options (blind test), extra
designs, not copies of the five. All Dan images get the real identity references.
    python3 scripts/covers/sl10-20261101/prompts.py
"""
from pathlib import Path
HERE = Path(__file__).parent
COMMON = ("Portrait 9:16 photorealistic premium fitness editorial photograph for a short-video cover. No letters, words, captions, "
 "numbers, logos, brand names, badges, arrows, watermarks or graphics anywhere; every bottle, can, glass and box is plain with no "
 "printed label. The attached photos are the real identity reference for Dan: accurately preserve his distinctive East Asian face, "
 "short styled black hair with shaved sides, age early 40s, skin tone, black rectangular glasses and natural lean build. Lean and "
 "shredded, not bulky, same size as the reference, no added muscle mass. Natural anatomy: exactly two arms, two hands with five "
 "fingers each. No artificial facial smoothing. Entire head and hair visible with comfortable clearance. ")
ABS = ("Clear six-pack and obliques fully visible, nothing held across his abs. Shirtless, olive-green mid-thigh athletic shorts "
 "(never briefs). ")
TOP = "Dan entirely BELOW the top 32 percent of the frame, and keep the top 30 percent as quiet plain background for a headline added later. "
BOTTOM = ("Dan's head near the top of the frame with clear room above his hair, his head and torso down to the hips in the upper 62 percent "
 "of the frame; the bottom 35 percent is dark and uncluttered for a headline added later. ")
PLATE = ("Portrait 9:16 photorealistic premium background photograph for a short-video cover. No people, no hands, no letters, words, "
 "numbers, logos, labels or watermarks anywhere; every bottle, can and glass is plain. Keep the top 30 percent quiet and dark, and "
 "the props in the left half of the frame, because a person is added on the right later. ")
S = {
 's1': {  # Your Drinks Should Taste Bad
  'A': (TOP, ABS, "Scene: an outdoor poolside bar at dusk with warm string lights. Dan stands behind a dark stone bar top that sits just below his hips. He has just taken a sip of a tall clear vodka and soda with ice and a lime wedge and pulls a big comic wince: eyes squeezed shut, lips puckered, head tilted back, glass held out at shoulder height. On the bar: a plain clear bottle, a plain silver soda can and a cut lime."),
  'B': (TOP, "Fitted thin black tank top that clings to his chest and abs so the six-pack outline shows through the fabric, defined arms and shoulders with visible veins. ", "Scene: a dim stylish home bar at night with warm side light and shelves of plain bottles behind. Dan stands behind a dark wood bar. He has just tasted a short glass of clear spirit with ice and stares down at the glass in disbelief, nose wrinkled, one eyebrow up, a bitter grimace. His other hand rests on the bar top by a plain clear bottle."),
  'C': (None, None, "Scene: a dark moody home bar at night, warm side light. On a dark wood bar top at left: a tall clear highball of vodka and soda with ice and a lime wedge, a plain silver soda can, and a cut lime. Blurred shelves of plain bottles behind."),
  'D': (BOTTOM, ABS, "Scene: an outdoor bar at golden hour by a pool. Dan pushes away a huge pink frozen margarita with a sugar rim and a paper umbrella, his flat palm toward it, and holds up a tall clear glass of soda water with lime in the other hand. Relaxed closed-mouth smile, looking at camera."),
  'E': (TOP, ABS, "Scene: a warm-lit cocktail bar at night. Dan sits on a stool at the bar, caught eating a giant frozen margarita with a long dessert spoon as if it were an ice cream sundae: the glass is topped with whipped cream, sprinkles and a cherry. He looks at camera with a raised eyebrow, spoon halfway to his mouth, torso open toward camera."),
  'F': (TOP, ABS, "Scene: a sunny beach bar. Dan holds up a small shot glass of clear spirit in one hand and bites a lime wedge from the other, one eye shut, sour face, shoulders hunched up in a funny shudder."),
  'G': (TOP, ABS, "Scene: a poolside bar at dusk. Exactly six empty margarita glasses with sugar rims stand in a neat row on the bar in front of Dan. He looks down at them with one hand on the back of his head and a sheepish, regretful grin. The bar sits below his hips."),
  'H': (BOTTOM, ABS, "Scene: a stylish outdoor bar at dusk. Dan pours soda water from a plain silver can into a tall glass of vodka and ice, looking at camera with a skeptical sideways look. A cut lime and a plain clear bottle on the bar."),
 },
 's2': {  # Your Nightly Wine Is Killing Your Abs
  'A': (TOP, ABS, "Scene: a warm-lit living room at night. Exactly fourteen full glasses of red wine stand in two neat rows of seven on a long low dark wood table in front of Dan. He stands behind the table with one hand on top of his head, eyes wide, shocked, looking at the rows of glasses, his other hand is empty and open. The table sits below his knees so his whole torso shows."),
  'B': (TOP, ABS, "Scene: a dark living room at night lit only by the blue glow of a television off camera and one warm lamp. Dan sits upright on the edge of a sofa holding a large glass of red wine, caught in the act, a guilty sideways glance at camera, closed mouth. A plain dark wine bottle on the side table."),
  'C': (None, None, "Scene: a dark moody room at night with a warm candle. At left on a dark wood table: a plain dark wine bottle with no label and a large glass of red wine. Soft bokeh behind."),
  'D': (BOTTOM, ABS, "Scene: an outdoor bar under a pergola at dusk, warm lights. Dan stands at a black sink and pours a full large glass of red wine down the drain with one hand, big easy thumbs up with the other, friendly closed-mouth smile at camera."),
  'E': (TOP, "", "Scene: one picture split straight down the middle by a thin vertical seam, both halves in the same warm living room at night, the same man twice. LEFT half: Dan shirtless, ripped, clear six-pack, olive-green athletic shorts, holding a tall glass of water, relaxed smile. RIGHT half: the same man about 40 pounds heavier, whole and clothed in a plain grey t-shirt that fits him, soft round face, holding a large glass of red wine, tired look, no hands touching his body. Same height, same camera, both from head to mid-thigh."),
  'F': (TOP, ABS, "Scene: a patio at dusk. Dan pours from a plain dark wine bottle into a huge glass that is already overflowing a little, looking at camera in comic surprise, mouth open, eyebrows up."),
  'G': (TOP, ABS, "Scene: a dim stone wine cellar with rows of plain bottles. Dan stands with a glass of red wine in one hand and his other hand on his chin, looking at the glass with a worried frown of doubt."),
  'H': (TOP, ABS, "Scene: a patio sofa at night with warm lanterns. Dan stands by a low table, wagging one finger at a large glass of red wine on the table and shaking his head, smiling knowingly at camera."),
 },
 's3': {  # Stop Drinking 3 Hours Before Bed
  'A': (TOP, ABS, "Scene: a dark bedroom at 3 in the morning, cold blue moonlight through the blinds and one dim lamp. Dan stands upright beside a rumpled bed, torso open to camera, wide awake and wrecked: heavy dark bags under his eyes, bloodshot eyes, messy hair, thousand-yard stare at camera, like a sleep-deprived zombie, but still ripped. On the nightstand: a half-empty glass of red wine and a round analog clock with hands at 3 o'clock and tick marks but no numerals. A matte black ring on his finger."),
  'B': (TOP, ABS, "Scene: a poolside bar at dusk. A hand from the side of the frame tries to refill Dan's glass with a plain bottle. Dan covers the top of his glass with his flat palm and taps his wristwatch with a finger of the other hand, friendly firm smile at camera: he is done for the night."),
  'C': (None, None, "Scene: a dark calm bedroom at night, moonlight on white sheets. At left on a nightstand: a round analog clock with hands at 3 o'clock with tick marks but no numerals, and one short glass of whiskey with ice."),
  'D': (BOTTOM, ABS, "Scene: a bedroom in early grey morning light. Dan sits on the edge of the bed, messy hair, tired eyes, staring in shock at the matte black ring on his raised hand, which gives off a faint glow, mouth slightly open."),
  'E': (TOP, ABS, "Scene: a warm living room at dusk. Dan holds a big round analog wall clock under one arm like a football, its hands at 8 o'clock with tick marks but no numerals, and raises a cocktail glass in a last toast with the other hand, friendly grin at camera."),
  'F': (TOP, ABS, "Scene: seen from above, Dan lies on his back on white sheets in a dark bedroom at night, wide awake, staring straight up at camera with dark bags under his eyes. An empty wine glass on the nightstand beside him."),
  'G': (TOP, ABS, "Scene: a calm bedroom at night. Dan stands by the bed with a tall glass of water in one hand, pointing at a round analog clock on the nightstand with the other, hands at 8 o'clock with tick marks but no numerals. Knowing smile at camera."),
  'H': (TOP, ABS, "Scene: bright morning sun in a bedroom. Dan stands by the unmade bed in the middle of a giant yawn, eyes shut, holding a mug of black coffee, dark bags under his eyes."),
 },
 's4': {  # What Killed My Urge To Drink
  'A': (TOP, ABS, "Scene: a backyard pool party at golden hour. Laughing friends behind him, all whole and holding beers. Dan stands in front, a friend's hand from the side offers him a beer, and he politely holds up a flat palm, holding a clear glass of sparkling water in the other hand, relaxed closed-mouth smile at camera, totally at ease."),
  'B': ("", "Unbuttoned short-sleeve black shirt hanging open, showing his clear six-pack and obliques. Dark jeans. ", "Scene: a busy warm-lit bar at night with friends cheering behind. Dan sits on a bar stool turned toward camera with a full untouched pint of beer on the bar beside him. He gives a bored shrug with both palms up and an unimpressed expression, not interested at all. Dan below the top 32 percent of the frame, top 30 percent quiet dark background."),
  'C': (None, None, "Scene: a warm crowded bar at night, out of focus golden bokeh lights. At left on a dark bar top: several full pints of beer and a row of shot glasses. No people."),
  'D': (BOTTOM, ABS, "Scene: a pool deck at dusk. Dan stands behind a small table holding up a plain white unlabeled injector pen in one hand, looking at it with a small amazed smile, and sliding a full glass of beer away across the table with the other hand."),
  'E': (TOP, ABS, "Scene: the morning after a big backyard party, bright sun. The yard is full of empty plain red cups and bottles, two friends asleep in lawn chairs behind him. Dan stands in the middle fresh and smiling, sipping from a clear bottle of water, eyebrows up at camera."),
  'F': (TOP, ABS, "Scene: a beach bar at sunset. Dan leans on the bar with his chin on one hand, looking down at a full glass of beer with total boredom. A full beer, untouched. Relaxed, unbothered."),
  'G': (TOP, ABS, "Scene: a backyard cookout at dusk. Friends behind him raise beers. Dan stands in front raising a clear can of sparkling water with no label, big easy grin at camera."),
  'H': (TOP, ABS, "Scene: a sunny pool party. Friends behind him hold beers. Dan stands in front with both hands empty and open at his sides, shrugging with a calm smile, at ease, no drink at all."),
 },
}
def main():
    for pack, letter in (('prompts', 'ABCDE'), ('prompts-google', 'FGH')):
        (HERE/pack).mkdir(exist_ok=True)
    for s, d in S.items():
        for k, (place, wear, scene) in d.items():
            text = PLATE+scene if place is None else COMMON+wear+place+scene
            pack = 'prompts-google' if k in 'FGH' else 'prompts'
            (HERE/pack/f'{s}-{k}.txt').write_text(text+'\n')
    print('written')
if __name__ == '__main__':
    main()
