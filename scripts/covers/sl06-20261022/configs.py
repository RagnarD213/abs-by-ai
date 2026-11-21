#!/usr/bin/env python3
"""Write scripts/blotato/configs/sl06-short<N>-<slug>.json for the six SL-06 shorts from uploads.json. Captions are Dan's
own words from each short (delivered ASR, typos fixed); titles are Dan's cover text (2026-10-22); pinned comments and
closes by dan-voice-writer. Slots: Docs/SHORTS_RELEASE_CALENDAR.md (parent RO-12 YouTube Sun Nov 8, read live)."""
import json,sys
from pathlib import Path
here=Path(__file__).resolve().parent;sys.path.insert(0,str(here))
from build import COPY
OUT=here.parents[2]/'scripts/blotato/configs'
up=json.loads(Path('/Volumes/Expansion/_edit_work/sl06-publish/uploads.json').read_text())
NOTE="Not medical advice. Talk to your doctor."
TAGS="#Zepbound #Tirzepatide #GLP1 #FatLoss #AbsByAI"
S={
's1':dict(n=1,slug='reduce-glp1-side-effects',when='2026-11-09T15:00:00.000Z',
 hook="Here's why you should start Zepbound at 1 milligram to avoid the side effects.",
 body="For most of you watching this channel, you should be taking less than the standard 2.5 milligram minimum dose. I have found that a dose as small as 1 milligram can be beneficial for people who are already in excellent shape. Start at 1 milligram, then step up to 2, and then to 2.5. That gradual ramp avoids nearly all of the side effects that come from stepping up your dose: the nausea, the fatigue, the days where you feel like garbage. Most of that is the jump, not the drug. Once you've lost the weight, you can dial it down to maintain. I'm currently taking 1.5 milligrams a week, and that's a great long-term maintenance dose for me."),
's2':dict(n=2,slug='why-i-dont-use-the-kwikpen',when='2026-11-21T15:00:00.000Z',
 hook="Here's why I stopped using the pen to inject Zepbound and use a needle and vial instead.",
 body="The problem with the pen is that it's more difficult to get a dose outside standard doses. With a vial and a needle, adjusting your dose precisely is much easier. And once you get good with a needle, it is less painful than the pen. The pen fires the drug at its own speed. You control the needle. You get a vial and insulin syringes, the tiny ones, and your dose is measured in units on the side of the barrel. Your doctor or pharmacy will tell you how many units equals a milligram for the concentration you have. Then you just pull back to that line. If you can read a measuring cup, you can do this."),
's3':dict(n=3,slug='how-to-inject-zepbound',when='2026-11-28T15:00:00.000Z',credit="Clips: Seattle Children's and SynergenX on YouTube.",
 hook="Here's how to inject Zepbound with a needle, step by step. It takes about 10 seconds once you know what you're doing.",
 body="Inject into your thigh on the outer front part, right around the middle. Not the inside of your leg, not down by your knee. Pinch the fat: this is a subcutaneous injection, so it goes into fat, not muscle. Stick the needle in, not too deep. Inject slowly. Do not slam it in. Wait one second after it's all gone, then withdraw. A good stick is nearly painless and there is no blood. If you bled or it hurt, you went too deep, you were in the wrong spot, or you pushed the plunger too fast."),
's4':dict(n=4,slug='take-weight-loss-meds-thursday-evening',when='2026-12-01T15:00:00.000Z',
 hook="Here's why Thursday evening is the best time to inject Zepbound.",
 body="The medication is strongest in the first few days after your shot, and it fades towards the end of the week. For me, and for basically every guy I've talked to about this, the days that need the most help are the weekend. Friday night, Saturday, Sunday: that is where diets go to die. The dinner out, the drinks, the pizza with the family, the afternoon when you eat out of boredom. If you inject Thursday evening, your appetite suppression is at maximum strength Friday night through Sunday. If you inject on a Monday, you're spending your strongest days on the days you're going to win anyway."),
's5':dict(n=5,slug='how-to-avoid-rebound-weight-gain',when='2026-12-05T15:00:00.000Z',
 hook="Here's how to come off Zepbound without gaining the fat back.",
 body="I have watched multiple people lose a huge amount of fat on Zepbound, go off it, and then regain almost all of it. Instead of going off totally, lower your dose from 2.5 mg to 2. If you don't gain any weight, go down to 1.5. Keep lowering by half a mg per week as long as you stay at or below your goal weight. If you go above your goal weight, even by a tenth of a pound, you stay at your current dose. If you gain more than three pounds above goal weight, go back up half a milligram. Done this way, you can taper all the way off over a couple of months and hold your new body the entire time. Walk down the stairs instead of jumping off the roof."),
's6':dict(n=6,slug='how-much-protein-you-need-on-a-glp1',when='2026-12-08T15:00:00.000Z',
 hook="Here's how much protein you need on a GLP-1 so you lose fat and not muscle.",
 body="Studies have shown the average person loses a catastrophic amount of muscle on this medication. But you can avoid that by eating enough protein and weight training regularly. I have actually gained muscle and strength on Zepbound. Hitting your protein is harder when you're not hungry, so track your macros. Aim for at least 0.8 grams of protein per pound of lean body mass. In real life, that's a serious serving of protein at lunch and dinner, around 8 ounces each, and protein snacks in between: rotisserie chicken, sardines, jerky, eggs. Your snacks should be protein. Your snacks should not be carbs."),
}
W=json.loads((here/'voice.json').read_text())
for k,v in S.items():
 n=v['n'];title=COPY[k][2];u=lambda f:up[f'{k}:{f}']
 link=f"https://absbyai.com/?utm_source=youtube&utm_medium=short&utm_campaign=zepbound-tips&utm_content=sl06-short{n}"
 body=v['body']+"\n\n"+NOTE
 yd=(f"{v['hook']}\n\nTry your free Abs By AI preview: {link}\n\n{body}\n\nFull video on my channel: Top 5 Zepbound Tips To Lose Fat And Keep Your Muscle\n\n"
  +(v['credit']+"\n\n" if 'credit' in v else '')+"Some clips in this video are AI-generated.\n\n#Zepbound #Tirzepatide #GLP1 #FatLoss #Shorts")
 c={"content_type":"organic","source":f"Short-form video content/{COPY[k][1]}.mp4","slug":f"sl06-short{n}","campaign":"zepbound-tips","title":title,
  "video_url":u('master')['url'],"tiktok_video_url":u('tiktok')['url'],"instagram_cover_url":u('ig')['url'],"youtube_cover_url":u('yt')['url'],
  "main":v['when'],"keyword":"FOOD","ai_generated":True,"hook":v['hook'],"body":body,"close":W[str(n)]['close'],"tags":TAGS,
  "youtube_description":yd,"pinned_comment":W[str(n)]['pinned_comment'],
  "media_sha256":{"master":u('master')['sha256'],"tiktok":u('tiktok')['sha256'],"ig":u('ig')['sha256'],"yt":u('yt')['sha256']}}
 txt=json.dumps(c,indent=2,ensure_ascii=False)+"\n";assert '—' not in txt and '–' not in txt
 p=OUT/f"sl06-short{n}-{v['slug']}.json";p.write_text(txt);print(p.name)
