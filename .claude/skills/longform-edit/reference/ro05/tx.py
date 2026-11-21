import whisper,json,sys
m=whisper.load_model('small')
r=m.transcribe(sys.argv[1],word_timestamps=True,condition_on_previous_text=False,language='en')
json.dump(r,open(sys.argv[2],'w'))
print('done',len(r['segments']))
