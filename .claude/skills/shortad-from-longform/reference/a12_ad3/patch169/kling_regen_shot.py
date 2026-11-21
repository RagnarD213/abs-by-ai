import base64, json, sys, time, urllib.request, concurrent.futures as cf
S=sys.argv[1]; N=int(sys.argv[2]); tag=sys.argv[3]
T=open(S+'/.rt').read().strip()
img='data:image/png;base64,'+base64.b64encode(open('/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/batch1-ads/frames/s3_no_results_mirror.png','rb').read()).decode()
prompt=("Static locked-off camera, no camera movement. Real handheld-free documentary footage in a small home bathroom. "
 "An overweight man in a grey T-shirt stands side-on beside the sink, holding his shirt lifted, and looks down at his belly, "
 "then glances up at his reflection in the mirror cabinet and slowly shakes his head, disappointed. He keeps his mouth closed "
 "and breathes gently through his nose. His body stays facing the same direction the whole time; his reflection in the mirror "
 "matches his movements exactly. The mirror glass stays perfectly clear and sharp. Natural, subtle, realistic motion.")
neg=("breath, visible breath, steam, smoke, mist, fog, haze, condensation, fogged mirror, vapor, exhaling cloud, "
 "camera movement, camera orbit, zoom, turning around, spinning, morphing, warping, extra fingers, distorted hands, "
 "mismatched reflection, face distortion, mouth open, talking, flicker, text, watermark")
def run(i):
    body=json.dumps({'input':{'prompt':prompt,'negative_prompt':neg,'start_image':img,'duration':5,'mode':'standard','generate_audio':False}}).encode()
    r=urllib.request.Request('https://api.replicate.com/v1/models/kwaivgi/kling-v3-video/predictions',data=body,
        headers={'Authorization':'Bearer '+T,'Content-Type':'application/json'})
    p=json.load(urllib.request.urlopen(r))
    while p['status'] not in ('succeeded','failed','canceled'):
        time.sleep(10)
        p=json.load(urllib.request.urlopen(urllib.request.Request(p['urls']['get'],headers={'Authorization':'Bearer '+T})))
    out=p.get('output'); out=out[0] if isinstance(out,list) else out
    if p['status']=='succeeded':
        urllib.request.urlretrieve(out, f'{S}/gen/{tag}{i}.mp4')
    return i,p['status'],p.get('error'),p.get('metrics'),p['id']
with cf.ThreadPoolExecutor(N) as ex:
    for res in ex.map(run, range(N)): print(res, flush=True)
