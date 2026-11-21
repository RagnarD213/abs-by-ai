#!/usr/bin/env python3
from pathlib import Path
import shutil,json,ast
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'Short-form video content/covers/review/ds52-zepbound-free-20261102';R=BASE/'r3';P=BASE/'blind-review';D=P/'text-r3';D.mkdir(exist_ok=True)
old=P/'four-designs.html'
if not old.exists():shutil.copy2(P/'index.html',old)
css=next(ast.literal_eval(n.value) for n in ast.parse((ROOT/'scripts/covers/ds52-20261102/r2/review.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='css' for t in n.targets))
m=json.loads((R/'manifest.json').read_text())
for row in m['outputs']:
 p=ROOT/row['path'];shutil.copy2(p.with_suffix('.jpg'),D/f"Text-{row['variant']}-{row['platform']}.jpg")
for n in 'ABC':shutil.copy2(R/f'Text-{n}-profile.jpg',D/f'Text-{n}-profile.jpg')
shutil.copy2(R/'three-text-choices.jpg',D/'three-text-choices.jpg')
labels={'A':'Clean Bold','B':'High Contrast','C':'Heavy Headline'}
notes={'A':'One consistent bold typeface, centred lines and a large natural-proportion Free.','B':'Two bold lines, with white lettering on deep green for the strongest phone-size contrast.','C':'A heavier left-aligned headline and a large Free, with no stretched letters.'}
h=[f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zepbound Free: Three Text Choices</title><style>{css}</style></head><body><main><h1>Design 3. Three Clearer Text Options.</h1><p>Why Zepbound Is Actually Free</p><div class="note">Same selected image, green background and receipt layout. Only the text treatment changes. All lettering keeps its natural proportions. My recommendation: <strong>B</strong> for the clearest, boldest read on a phone.</div><p>Choose A, B or C in this chat. Each has Instagram and YouTube Shorts layouts plus the Instagram profile crop. Nothing is installed, uploaded or scheduled. Your approved R3 film is unchanged.</p><nav>']
for n in 'ABC':h.append(f'<a href="#text-{n}">{n}</a>')
h.append('</nav><a href="text-r3/three-text-choices.jpg"><img src="text-r3/three-text-choices.jpg" alt="Three clearer text variations, Instagram and YouTube"></a>')
for n in 'ABC':
 h.append(f'<section id="text-{n}"><h2>{n}. {labels[n]}</h2><p>{notes[n]}</p><div class="pair">')
 for p,label in [('instagram','Instagram'),('youtube','YouTube Shorts'),('profile','Instagram Profile Crop')]:
  h.append(f'<figure class="{"profile" if p=="profile" else ""}"><figcaption>{label}</figcaption><a href="text-r3/Text-{n}-{p}.jpg"><img loading="lazy" src="text-r3/Text-{n}-{p}.jpg" alt="Text {n}: {label}"></a></figure>')
 h.append('</div></section>')
h.append('<p><a href="four-designs.html">Earlier four designs</a> | <a href="original-eight.html">Original eight options</a></p><p>After your text choice, the remaining setup continues here.</p></main></body></html>')
(P/'index.html').write_text(''.join(h));print('Three text choices added to the same review URL.')
