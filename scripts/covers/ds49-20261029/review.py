from pathlib import Path
import json
LABELS = {
    'A': 'Pouring It In The Trash, Yellow Headline',
    'B': 'Coconut Water Next To A Can Of Coke, White And Cyan',
    'C': 'Real Studio Photo Over Coconut Water And Sugar Cubes',
    'D': 'Pointing At The Sugar, Large Bottom Title',
    'E': 'No Thanks To A Fresh Coconut, White And Gold',
}
from build import OUT, ROOT
R = OUT/'ds49'; manifest = json.loads((R/'manifest.json').read_text())
parts = ['''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Coconut Water: Five Cover Choices</title><style>
*{box-sizing:border-box}body{margin:0;background:#101823;color:#f1f5f9;font:17px/1.5 -apple-system,BlinkMacSystemFont,Arial,sans-serif}main{max-width:1300px;margin:0 auto;padding:32px 22px}h1{font-size:36px;margin:0 0 12px}p{max-width:850px;color:#cbd5e1}.nav{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}a{color:#64e4f3}.nav a{padding:8px 22px;background:#233147;border-radius:8px;text-decoration:none}.notice{padding:18px 22px;border:1px solid #36506a;border-radius:12px;background:#182437}section{margin:28px 0;padding:24px;background:#182230;border:1px solid #344156;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr 0.75fr;gap:22px;align-items:start}.pair img{width:100%;height:auto;border-radius:6px}figure{margin:0}figcaption{font-size:15px;margin:0 0 10px;color:#cbd5e1}h2{margin:0 0 20px}small{color:#b1bfd1}.sheet{max-width:100%;border-radius:10px}.tip{color:#ffd74f} @media(max-width:700px){main{padding:20px 12px}.pair{grid-template-columns:1fr 1fr;gap:12px}.grid{grid-column:1/3;max-width:240px}section{padding:16px}h1{font-size:28px}}
</style></head><body><main><h1>Why I Stopped Drinking Coconut Water</h1><p>Five cover choices. Each one has an Instagram layout, a YouTube Shorts layout and the Instagram profile-grid crop. Click a picture for its full-size file.</p><div class="notice"><strong>Pick A to E in this chat.</strong><p class="tip">My recommendation: A. It acts the title out (you pouring coconut water into the trash), your face and abs read well, and the yellow headline is the look you pick most often.</p><small>Your approved R2 film is untouched. Nothing has been uploaded or scheduled. C uses your original studio photo (blue-222, green shorts); A, B, D and E are Codex images made from your real identity reference. All five made on your ChatGPT subscription; no paid image API.</small><p>Planned date after your pick: <strong>Mon Dec 21, 6 PM Central</strong>, one week after the other coconut water Short (Dec 14). The only earlier open slot, Mon Nov 23, is held for the Hamstring Curls how-to.</p></div><div class="nav">''']
for k in LABELS: parts.append(f'<a href="#{k}">{k}</a>')
parts.append('</div><a href="five-cover-choices.jpg"><img class="sheet" src="five-cover-choices.jpg" alt="All five cover choices in both layouts"></a>')
for k in LABELS:
    parts.append(f'<section id="{k}"><h2>{k}. {LABELS[k]}</h2><div class="pair">')
    for plat in ['instagram', 'youtube']:
        row = next(q for q in manifest['outputs'] if q['letter'] == k and q['platform'] == plat); rel = Path(row['path']).relative_to(R.relative_to(ROOT)).as_posix()
        parts.append(f'<figure><figcaption>{"Instagram" if plat == "instagram" else "YouTube Shorts"}</figcaption><a href="{rel}"><img loading="lazy" src="{rel}" alt="{k}, {plat} layout"></a></figure>')
    parts.append(f'<figure class="grid"><figcaption>Instagram profile crop</figcaption><img loading="lazy" src="grid/{k}.jpg" alt="{k}, actual Instagram 3:4 crop"></figure></div></section>')
parts.append('<p>After your pick: upload the film and covers, queue YouTube, Facebook, Instagram and TikTok for Dec 21 (or the shared waiting list if Blotato is full) and read the schedules back. The Google Drive backup is already done and checked.</p></main></body></html>')
(R/'index.html').write_text(''.join(parts)); print(R/'index.html')
