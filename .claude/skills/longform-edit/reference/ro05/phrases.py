import json,sys
M="/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/"
def words(r):return json.load(open(f"{M}{r}.roll/words.json"))['words']
if __name__=='__main__':
  for r in sys.argv[1:]:
    w=words(r);print('##',r);line=[];st=None
    for i,x in enumerate(w):
      if st is None:st=x['start']
      line.append(x['word'].strip())
      nxt=w[i+1]['start'] if i+1<len(w) else 1e9
      if nxt-x['end']>=0.35 or x['word'].strip()[-1:] in '.?!' or len(line)>=16:
        print(f"{st:.2f}-{x['end']:.2f}|{nxt-x['end']:.2f}: {' '.join(line)}");line=[];st=None
