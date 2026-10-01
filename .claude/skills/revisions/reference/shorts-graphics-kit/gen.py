import json,subprocess,urllib.request,time,re,os,sys
DOC='1ib0VbJ3dqnqci-8seSpzR2DNf0-kKolWlyVe_-flWus'
fid=open('kit/folder_id.txt').read().strip()
ls=json.load(open('kit/upload_ls.json')); ids={x['Path']:x['ID'] for x in ls}
folders={'ds05_abs_v2':'1 Why Having Abs Beats Being A Fat Millionaire','ds06_bodyfat_v2':'2 What Every Body Fat Percentage Looks Like','ds07_top3ai_v1':'3 Top 3 Ways To Use AI To Get Abs','ds09_maketime_v1':'4 How To Make Time To Work Out','ds10_zepbound_v1':'5 3 Unexpected Ways','ds11_weigh_v1':'6 Why You Must Weigh Yourself Daily','ad13_hq':'7 The #1 Change I Made To Get Abs At 40'}
def tc(t): return f"{int(t//60)}:{t%60:04.1f}"
FOLDER=f"https://drive.google.com/drive/folders/{fid}"; lab=f"https://drive.google.com/drive/folders/{ids['0 Labels']}"
top=f'''## GRAPHICS - NEW LOCKED STYLE FOR ALL SHORT FORM VIDEOS

I've decided on the graphic style for all short form videos, and I made every graphic for these seven videos for you, so you don't have to build any of them. **Take your title bars and chips off and use these files instead.** The captions stay as they are.

- All the graphics are in this folder, one folder per video, with a READ ME:
    - {FOLDER}
- Every file is a 1080x1920 .mov with a transparent background. **Put it on the top video track at 100% scale, lined up with the frame, and do not move or resize it.** It is already placed above my head.
- The file name gives the time it starts in the cut you sent me, and each file already runs the right length with its own animation in and out. If a start time moves after your changes, keep the graphic on the same words.
- Each video's folder has a "stills" folder with a PNG of every graphic, in case you need to hold one longer.
- The labels are in the "0 Labels" folder. **AI-GENERATED goes on every AI picture and AI clip for the whole time it is on screen. The real picture label goes on photo shoot pictures of me.** Never over a face or abs.
    - {lab}
- **Take AbsByAI.com off the end of every video.** I'm not putting it on screen at the end any more.
- Each video below has a GRAPHICS list with the time, the text and the link for every graphic in it.
'''
order=list(folders); secs=[]
for n in order:
    s=open(f'out/{n}.md').read().strip()
    gs=json.load(open(f'out/{n}.graphics.json'))
    files={f[:3]:f for f in os.listdir(f'kit/{n}/mov') if f.endswith('.mov') and not f.startswith('.')}
    lines=["- **\\*\\*GRAPHICS - USE THESE FILES\\*\\***","    - **Take your title bar and chips off this video and use these instead.** Each one starts at the time shown."]
    ai=[];real=[]
    for g in gs:
        span=f"{tc(g['t0'])} - {tc(g['t1'])}"
        if g['kind']=='label_ai': ai.append(span); continue
        if g['kind']=='label_real': real.append(span); continue
        i=ids[f"{folders[n]}/{files[g['id']]}"]
        lines.append(f"    - {span}: \"{('KEY POINT: ' if g['kind']=='keypoint' else '')+g['text']}\"")
        lines.append(f"        - https://drive.google.com/file/d/{i}/view")
    if ai: lines.append("    - AI-GENERATED label, from the Labels folder, on every AI picture and clip: "+", ".join(ai))
    if real: lines.append("    - Real picture label, from the Labels folder, on: "+", ".join(real))
    k=s.index("**\\*\\*TIMESTAMPED REVISIONS\\*\\***")
    s=s[:k].rstrip()+"\n"+"\n".join(lines)+"\n\n"+s[k:]
    s=s.replace("Wait until the graphic style is locked before making this.","I made this graphic for you, it is in the GRAPHICS list above.")
    secs.append(s)
doc=top+"\n"+"\n\n".join(secs)+"\n"
rep=[
("**Use the same AI GENERATED chip you put on the picture at 0:08, in the top left corner of the clip, about 50% larger, for the whole time the clip is on screen.** One label style for every AI picture and clip.","**Use the AI-GENERATED label from the Labels folder on every AI picture and clip, for the whole time each one is on screen.** One label style for all of them."),
("**Change the text to \"KEY POINT: You're Probably One Category FATTER Than You Think\".** Title Capitalization, with only FATTER in full caps.","**Replace your chip with the key point graphic I made.**"),
("**Change it to \"KEY POINT: Let AI Handle Your Goal Picture, Your Macros And Your SUPPLEMENTS\", and put the captions back on this line.**","**Take the chip off, use the key point graphic I made (\"KEY POINT: Let AI Handle Your Goal Picture, Macros And SUPPLEMENTS\"), and put the captions back on this line.**"),
]
for a,b in rep:
    assert a in doc,a[:40]; doc=doc.replace(a,b)
assert chr(8212) not in doc and chr(8211) not in doc and 'AbsByAI.com mark' not in doc, [l for l in doc.splitlines() if 'AbsByAI.com mark' in l]
open('out/ALL_v2.md','w').write(doc); print(len(doc))
if '--upload' in sys.argv:
    rc=subprocess.check_output(['which','rclone']).decode().strip(); subprocess.run([rc,'about','gdrive:'],capture_output=True)
    tok=json.loads(json.loads(subprocess.check_output([rc,'config','dump']))['gdrive']['token'])['access_token']
    req=urllib.request.Request(f'https://www.googleapis.com/upload/drive/v3/files/{DOC}?uploadType=media',data=doc.encode(),method='PATCH',headers={'Authorization':'Bearer '+tok,'Content-Type':'text/markdown'})
    print(urllib.request.urlopen(req).read()[:120])
