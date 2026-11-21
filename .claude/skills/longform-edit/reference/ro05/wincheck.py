import whisper,sys,subprocess,json
FF="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg"
m=whisper.load_model('small');src=sys.argv[1]
for t in [float(x) for x in sys.argv[2:]]:
    subprocess.run([FF,'-nostdin','-v','error','-y','-ss',str(max(0,t-4)),'-t','6.5','-i',src,'-ar','16000','-ac','1','/Volumes/Extreme/_edit_work/ro05/audio/_w.wav'])
    r=m.transcribe('/Volumes/Extreme/_edit_work/ro05/audio/_w.wav',language='en',condition_on_previous_text=False)
    print(f"{t:7.2f}: {r['text'].strip()}")
