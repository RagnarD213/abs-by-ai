"""Ad 13 round 3: opener motion, Kling v3 start + end frame. usage: gen_opener.py <9x16|16x9> <tag>"""
import base64, json, os, sys, time, urllib.request
B = '/Volumes/Extreme/_edit_work/kit9x16/av11-ad13'
ar, tag = sys.argv[1], sys.argv[2]
mode = sys.argv[3] if len(sys.argv) > 3 else 'standard'
T = [l.split('=', 1)[1].strip().strip('"\'') for l in open(os.path.expanduser('~/.absbyai-secrets.env'))
     if l.startswith('REPLICATE_API_TOKEN=')][0]
def b64(p): return 'data:image/png;base64,' + base64.b64encode(open(p, 'rb').read()).decode()
prompt = ("Static locked-off camera on a tripod, no camera movement, no zoom. Real footage in a bright brick-wall gym. "
  "The middle-aged man in the grey t-shirt lying on the bench presses the barbell smoothly from just above his chest "
  "straight up to full arm extension in ONE single bench press rep, smiling with effort. The barbell stays perfectly "
  "rigid and straight, both weight plates stay round and solid. The silver humanoid robot standing behind the bench "
  "spots him: its two open hands follow just under the bar as it rises, then stay open below it. Its amber eyes glow steadily. "
  "The bald bearded personal trainer in the black polo walks slowly toward the camera carrying his cardboard box of "
  "belongings with both hands, and near the end turns his head to look back at the bench with a sad, defeated expression. "
  "Natural, realistic human motion at normal speed. Everyone keeps the same face, body and clothes throughout. "
  "The gym background, racks, windows and plants stay completely still.")
neg = ("camera movement, camera shake, zoom, pan, orbit, cuts, scene change, morphing, warping, bending barbell, "
  "wobbling plates, extra fingers, missing fingers, fused fingers, distorted hands, extra arms, extra people, "
  "face distortion, changing faces, flicker, text, letters, watermark, logo, slow motion, floating objects, "
  "objects appearing, objects disappearing, smoke, steam")
body = json.dumps({'input': {'prompt': prompt, 'negative_prompt': neg, 'start_image': b64(f'{B}/round2/opener/start_{ar}.png'),
    'end_image': b64(f'{B}/round2/opener/end_{ar}.png'), 'duration': 4, 'mode': mode, 'generate_audio': False}}).encode()
H = {'Authorization': 'Bearer ' + T, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
p = json.load(urllib.request.urlopen(urllib.request.Request(
    'https://api.replicate.com/v1/models/kwaivgi/kling-v3-video/predictions', data=body, headers=H)))
while p['status'] not in ('succeeded', 'failed', 'canceled'):
    time.sleep(10)
    p = json.load(urllib.request.urlopen(urllib.request.Request(p['urls']['get'], headers=H)))
out = p.get('output'); out = out[0] if isinstance(out, list) else out
if p['status'] == 'succeeded':
    urllib.request.urlretrieve(out, f'{B}/round3/opener/{tag}.mp4')
json.dump({'id': p['id'], 'status': p['status'], 'error': p.get('error'), 'metrics': p.get('metrics'), 'mode': mode,
           'prompt': prompt, 'negative': neg, 'ar': ar, 'when': time.strftime('%F %T')},
          open(f'{B}/round3/opener/{tag}.json', 'w'), indent=1)
print(tag, p['status'], p.get('error'), p.get('metrics'))
