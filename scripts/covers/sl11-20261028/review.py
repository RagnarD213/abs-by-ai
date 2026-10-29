from pathlib import Path
import json,html
from build import OUT,ROOT,SHORTS
names={'a':'Standing Stomach Vacuum','b':'Stop Holding Your Breath','c':'One 20-Second Vacuum Every Morning'}
labels={'A':'Yellow Headline, AI Dan','B':'White And Cyan, AI Dan','C':'Real Studio Photograph','D':'Large Bottom Title, AI Dan','E':'White And Gold, AI Dan'}
rec=json.loads((OUT/'recommendations.json').read_text()) if (OUT/'recommendations.json').exists() else {}
parts=['''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Vacuum: Cover Choices</title><style>*{box-sizing:border-box}body{margin:0;background:#101823;color:#f1f5f9;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1320px;margin:auto;padding:32px 22px}h1{font-size:36px;margin:0 0 12px}p{max-width:960px;color:#cbd5e1}a{color:#64e4f3}.nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.nav a{padding:9px 18px;background:#233147;border-radius:8px;text-decoration:none}.notice{padding:18px 22px;border:1px solid #36506a;border-radius:12px;background:#182437}.short{margin-top:60px;border-top:2px solid #526882;padding-top:20px}article{margin:24px 0;padding:24px;background:#182230;border:1px solid #344156;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr .75fr;gap:22px;align-items:start}.pair img{width:100%;height:auto;border-radius:6px}figure{margin:0}figcaption{font-size:15px;margin:0 0 10px;color:#cbd5e1}h2{font-size:30px}h3{margin:0 0 20px}.sheet{width:100%;border-radius:10px}.tip{color:#ffd74f}small{color:#b1bfd1}@media(max-width:700px){main{padding:20px 12px}.pair{grid-template-columns:1fr 1fr;gap:12px}.grid{grid-column:1/3;max-width:220px}article{padding:14px}h1{font-size:28px}}
</style></head><body><main><h1>The Vacuum: Cover Choices</h1><p>Three approved Shorts. Five distinct cover choices for each, with separate Instagram and YouTube Shorts layouts. Click any image to see the full-size file.</p><div class="notice"><strong>Reply with one cover letter for each Short.</strong><p>Example: Standing: B; Breathing: A; Morning: D.</p><small>Your approved films and sound are preserved. These covers await your first review. Nothing has been uploaded or scheduled. Option C uses your original studio photograph; A, B, D and E use Codex images based on your real identity photo.</small></div><nav class="nav">''']
for key in SHORTS:parts.append(f'<a href="#short-{key}">{names[key]}</a>')
parts.append('</nav>')
for key in SHORTS:
 r=OUT/key;m=json.loads((r/'manifest.json').read_text());parts.append(f'<section class="short" id="short-{key}"><h2>{names[key]}</h2>')
 if key in rec:parts.append(f'<p class="tip">My recommendation: {html.escape(rec[key])}</p>')
 parts.append(f'<a href="{key}/five-cover-choices.jpg"><img class="sheet" src="{key}/five-cover-choices.jpg" alt="All five {names[key]} choices, Instagram above and YouTube below"></a>')
 for letter in 'ABCDE':
  parts.append(f'<article id="{key}-{letter}"><h3>{letter}. {labels[letter]}</h3><div class="pair">')
  for plat in ['instagram','youtube']:
   row=next(q for q in m['outputs'] if q['letter']==letter and q['platform']==plat);rel=(ROOT/row['path']).relative_to(OUT).as_posix();parts.append(f'<figure><figcaption>{"Instagram" if plat=="instagram" else "YouTube Shorts"}</figcaption><a href="{rel}"><img loading="lazy" src="{rel}" alt="{names[key]}, {letter}, {plat}"></a></figure>')
  parts.append(f'<figure class="grid"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="{key}/grid/{letter}.jpg" alt="{names[key]}, {letter}, actual profile crop"></figure></div></article>')
 parts.append('</section>')
parts.append('<p>After your picks, I will finish organic upload setup for YouTube, Instagram @danrosefit, Facebook and TikTok. Release slots must follow the parent video and match the current calendar and queue.</p></main></body></html>')
(OUT/'index.html').write_text(''.join(parts));print(OUT/'index.html')
