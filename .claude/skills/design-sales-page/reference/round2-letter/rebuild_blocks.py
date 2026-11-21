# Rebuild the paragraph numbering gen.py was written against (the first doc read) from the latest doc export.
import json, sys
b = json.load(open(sys.argv[1]))
out, seen_first_img = [], False
for x in b:
    t = x['text'].strip()
    if t.startswith('[NOTE FROM CLAUDE') or t.startswith('[CLAUDE: INSERT STILL IMAGE OF ME PROMPTING FIVE AI MODELS'):
        continue
    if t.startswith('[[IMG') and t.endswith(']]') and t.count('[[IMG') >= 1 and not t.replace(']]', '').split('[[IMG')[0].strip():
        if not seen_first_img:  # the original avatar source picture was block 21
            seen_first_img = True; out.append(x)
        continue
    out.append(x)
    if t.startswith('I thought my workout plan was good'):
        out.append({'tag': 'p', 'html': '[SHOW APP SCREEN: THE AI TRAINER READING THE BEFORE AND GOAL PICTURES]', 'text': '[SHOW APP SCREEN: THE AI TRAINER READING THE BEFORE AND GOAL PICTURES]'})
anchors = {5: 'I Fired My Personal Trainer', 21: '[[IMG', 23: 'Hi, I', 29: 'I Had A Bloated', 39: 'I Taught Millions', 46: 'The Old Way', 58: 'There Was A Revolution',
           64: 'Why Wasn', 68: 'My First AI Fitness Plan', 76: 'I Devoted My Life', 81: 'Different AI models', 95: 'How Did You Get', 100: 'Introducing Abs By AI',
           106: 'The Five Ways', 110: 'AI Hack #1', 117: 'A picture of a fitness model', 120: 'AI Hack #2', 122: '[SHOW APP SCREEN: THE AI TRAINER', 123: 'First, I was doing',
           130: 'AI Hack #3', 138: 'AI Hack #4', 145: 'AI Hack #5', 152: 'Try Abs By AI Free', 160: 'Your Trainer, Nutritionist', 168: 'Close this page',
           173: 'How much is it', 179: 'Who is this NOT for', 184: "I'll see you inside", 187: 'Sticky bottom'}
bad = [(i, a, out[i]['text'][:40] if i < len(out) else None) for i, a in anchors.items() if i >= len(out) or not out[i]['text'].strip().startswith(a)]
print('blocks:', len(out), 'anchor mismatches:', bad)
if not bad and len(out) == 188:
    json.dump(out, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0); print('wrote', sys.argv[2])
