"""Write the four Blotato configs (DS-02/03/07/11). Captions are Dan's own spoken words from the finished Shorts,
lightly cleaned. Media URLs, release time and pinned comment are filled after Dan's cover picks (upload.py)."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent));from plan import P,SHORTS
CLOSE="Subscribe and go to SixPackAbs.com for all my newest videos."
SRC={'ds02':'How Getting Abs Looksmaxxes Your Face - DS-02/How Getting Abs Looksmaxxes Your Face | muhammad | 9x16 | V3 HD.mp4',
 'ds03':'The 3 Most Important Supplements For Men - DS-03/The 3 Most Important Supplements For Men | muhammad | 9x16 | V3 HD.mp4',
 'ds07':'Top 3 Ways To Use AI To Get Abs - DS-07/Top 3 Ways To Use AI To Get Abs | muhammad | 9x16 | V5 HD.mp4',
 'ds11':'Why You Must Weigh Yourself Daily - DS-11/Why You Must Weigh Yourself Daily | muhammad | 9x16 | V4 HD.mp4'}
PIN={'ds02':"When you leaned out, what changed first on your face? Your jawline, your cheekbones or your skin?",
 'ds03':"How many supplements are you taking every day right now?",
 'ds07':"Which one of these three would you try first: the AI ab picture on your lock screen, photo macro tracking, or the supplement audit?",
 'ds11':"How often do you step on the scale right now? Daily, weekly, or never?"}  # dan-voice-writer, 2026-10-26
C={
 'ds02':dict(slug='ds02-getting-abs-looksmaxxes-your-face',campaign='getting-abs-face',keyword='ABS',
  hook="Getting abs makes your face look way better, and I'll prove it to you.",
  body="Here's my face when I was 200 pounds. Bloated, puffy, and breaking out. Here's my face now.\n\nGetting lean enough to get abs improves your face in three ways. First, it defines your jawline. You go from a soft, puffy double chin to a jawline you'll want to show off. Second, it sharpens your cheekbones. If your face is round and bloated right now, losing belly fat makes it look more angular and masculine. Third, cleaning up your diet fixes your skin. I was shocked by how much less I broke out after getting lean.\n\nAnd here's what nobody tells you: your face leans out before your abs show up. You'll see it months before anyone sees a six-pack.",
  tags="#Abs #Looksmaxxing #FatLoss #Fitness #Shorts"),
 'ds03':dict(slug='ds03-3-most-important-supplements-for-men',campaign='supplements-for-men',keyword='FOOD',
  hook="These are the three most important supplements for men. If you take nothing else, take these.",
  body="Number one, fish oil. If you only take one supplement, make it this one. Heart, joints, recovery, skin and hair. It's the most proven supplement there is, and most men eat almost no fish.\n\nNumber two, vitamin D. About 70% of people are deficient. Fixing it raises your testosterone, your immunity and your workout performance. I take 5,000 IU a day in liquid form. It's cheaper and easier to dose.\n\nNumber three, magnesium. Take this one at night. It improves your sleep, and your sleep decides whether you build muscle and control your appetite the next day.\n\nHere's what nobody selling you supplements will say: they're about 5% of your results. Your nutrition, your training and your sleep matter far more. Three supplements taken daily beats a stack of ten you never take.",
  tags="#Supplements #MensHealth #FishOil #VitaminD #Shorts"),
 'ds07':dict(slug='ds07-top-3-ways-to-use-ai-to-get-abs',campaign='ai-to-get-abs',keyword='COACH',
  hook="Here are the top three ways to use AI to get abs.",
  body="Number one, use AI to generate a picture of yourself with abs. Then set it as your lock screen so you see it 40 times a day. That keeps you laser focused on your goal.\n\nNumber two, track your macros with AI. Take a picture of your plate and it reads the calories and protein back to you. No weighing, no calculating, no logging.\n\nNumber three, audit your supplements. Photograph every bottle on the counter and it tells you what's doing nothing and what you're missing. Most guys are wasting real money every month on pills that do nothing.\n\nAI is an incredibly powerful tool for getting abs if you use it the right way.",
  tags="#AI #Abs #FatLoss #Fitness #Shorts"),
 'ds11':dict(slug='ds11-why-you-must-weigh-yourself-daily',campaign='weigh-daily',keyword='TRACK',
  hook="You have to weigh yourself every single day. Trying to get abs without weighing yourself daily is like trying to get rich while never looking at your bank account.",
  body="First, you catch fat gain while it's still small. Two pounds is one bad weekend, and you fix it in three days. Ten pounds is four months of dieting to undo.\n\nSecond, you learn what actually makes you gain weight. Watch the number after a night of drinking, after bad sleep and after a restaurant meal. Within four weeks you'll know your problem foods from your own data.\n\nThird, it takes 10 seconds. Weigh in first thing after the bathroom, before you eat or drink anything, and never react to one day. Watch the weekly average, because your weight swings three pounds on water alone.",
  tags="#WeightLoss #FatLoss #Abs #Fitness #Shorts"),
}
def utm(src,c,s):return f"https://absbyai.com/?utm_source={src}&utm_medium=short&utm_campaign={c['campaign']}&utm_content={c['slug']}"
for k,c in C.items():
 p=P/'scripts/blotato/configs'/(c['slug']+'.json');old=json.loads(p.read_text()) if p.exists() else {}
 text=f"{c['hook']}\n\n{c['body']}\n\n{CLOSE}"
 yt=f"{text}\n\nAbs By AI: {utm('youtube',c,k)}\n\n{c['tags']}"
 cfg=dict(content_type='organic',source=str(P/'Short-form video content'/SRC[k]),title=SHORTS[k]['title'],slug=c['slug'],campaign=c['campaign'],
  video_url=old.get('video_url',''),tiktok_video_url=old.get('tiktok_video_url',''),instagram_cover_url=old.get('instagram_cover_url',''),youtube_cover_url=old.get('youtube_cover_url',''),
  main=old.get('main',''),keyword=c['keyword'],ai_generated=True,hook=c['hook'],body=c['body'],close=CLOSE,tags=c['tags'],youtube_description=yt,
  pinned_comment=PIN[k],instagram_first_comment=f"Abs By AI: {utm('instagram',c,k)}",
  caption_overrides=dict(facebook=f"{text}\n\nAbs By AI: {utm('facebook',c,k)}\n\n{c['tags']}",instagram=f"{text}\n\nMore at AbsByAI.com. Link in bio.\n\n{c['tags']}",tiktok=f"{text}\n\nAbs By AI: {utm('tiktok',c,k)}\n\n{c['tags']}"))
 assert '—' not in json.dumps(cfg,ensure_ascii=False) and '–' not in json.dumps(cfg,ensure_ascii=False)
 p.write_text(json.dumps(cfg,indent=2,ensure_ascii=False)+'\n');print(p.name,len(yt))
