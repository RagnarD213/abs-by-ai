import json,re
from pathlib import Path
W=Path(__file__).resolve().parents[1]
c=json.loads((W/'cut.json').read_text());ws=c['words'];norm=lambda s:re.sub('[^a-z0-9 ]','',s.lower()).strip()
# Output timing comes from words in the selected cut, to be replaced by final audio alignment.
def t(phrase,after=0):
 tokens=phrase.split()
 for i in range(len(ws)-len(tokens)+1):
  if ws[i]['t']>=after and [norm(x['w']) for x in ws[i:i+len(tokens)]]==tokens:return ws[i]['t']
 raise ValueError(phrase)
scenes=[
 dict(id='P1',kind='phone',a=t('first generate an image') if False else t('first'),b=t('put it on'),copy='A Goal You Can See',source='Approved Dan sunglasses-to-pool app demonstration',identity='Dan before, AI-generated Dan goal',provenance='Previously approved simulated demonstration, not a new live recording'),
 dict(id='L1',kind='clip',a=t('put it on'),b=t('second'),copy='AI-GENERATED',source='A0074 phone lockscreen',identity='AI-generated Dan goal'),
 dict(id='P2',kind='phone',a=t('so the workout'),b=t('and third'),copy='A Plan Built Around You',source='Workout plan and nutrition plan screens',status='screen selection pending'),
 dict(id='P3',kind='phone',a=t('when life gets'),b=t('most guys never',after=40),copy='Support When Life Changes',source='Current AI trainer controls',status='authentic adjustment screen needed; do not fabricate UI behavior'),
 dict(id='CTA',kind='cta',a=t('tap the button'),b=c['dur']+.6,copy='Tap The Button Below / Get Started',source='Shared HyperFrames CTA',note='No ending URL mark per newer 2026-10-01 standing rule')]
json.dump({'job':'RA-13','category':'AD','timing_status':'source-word draft, final alignment pending','items':scenes},open(W/'plan_resolved.json','w'),indent=2)
print([(x['id'],x['a'],x['b']) for x in scenes])
