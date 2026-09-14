import base64, json, sys, time, urllib.request, concurrent.futures as cf
S=sys.argv[1]
T=open(S+'/.rt').read().strip()
img='data:image/png;base64,'+base64.b64encode(open('/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/ad-assets/batch1-ads/frames/s3_no_results_mirror.png','rb').read()).decode()
prompt=("Static locked-off camera on a tripod, no camera movement. Realistic documentary footage in a small home bathroom. "
 "An overweight man in a grey T-shirt stands side-on beside the sink holding his shirt lifted with both hands, looking down at his belly "
 "with a quiet, disappointed expression. He barely moves: small natural breathing, a slow blink, a tiny tilt of the head down. "
 "His mouth stays closed the entire time. His head stays facing the same direction. His reflection in the mirror cabinet copies "
 "his exact pose and moves only when he moves. The mirror glass stays perfectly clear. Subtle, calm, realistic.")
neg=("breath, visible breath, steam, smoke, mist, fog, haze, condensation, fogged mirror, vapor, "
 "open mouth, talking, sighing, gasping, lips moving, head turning, looking up, looking at camera, "
 "camera movement, zoom, turning around, morphing, face changing, different person, hairline changing, "
 "extra fingers, distorted hands, reflection moving independently, mismatched reflection, flicker, text, watermark")
jobs=[('u',0,True),('u',1,True),('u',2,False),('u',3,False)]
def run(j):
    tag,i,end=j
    inp={'prompt':prompt,'negative_prompt':neg,'start_image':img,'duration':5,'mode':'standard','generate_audio':False}
    if end: inp['end_image']=img
    r=urllib.request.Request('https://api.replicate.com/v1/models/kwaivgi/kling-v3-video/predictions',data=json.dumps({'input':inp}).encode(),
        headers={'Authorization':'Bearer '+T,'Content-Type':'application/json'})
    p=json.load(urllib.request.urlopen(r))
    while p['status'] not in ('succeeded','failed','canceled'):
        time.sleep(10)
        p=json.load(urllib.request.urlopen(urllib.request.Request(p['urls']['get'],headers={'Authorization':'Bearer '+T})))
    out=p.get('output'); out=out[0] if isinstance(out,list) else out
    if p['status']=='succeeded': urllib.request.urlretrieve(out, f'{S}/gen/{tag}{i}.mp4')
    return tag+str(i),'end_image' if end else 'free',p['status'],p.get('error')
with cf.ThreadPoolExecutor(4) as ex:
    for res in ex.map(run, jobs): print(res, flush=True)
