from pathlib import Path
from PIL import Image,ImageOps,ImageCms,ImageDraw
import json,hashlib,base64,html,shutil
ROOT=Path(__file__).resolve().parent
LIB=ROOT.parents[1]/'photos/finalized social media photos'
SOURCES=['blue-100','blue-145','blue-11','blue-247','blue-175','white-42','blue-110','gray-2','gray-4','blue-269','gray-38','blue-76','blue-201','blue-177','white-25','blue-139','blue-127','blue-5','blue-109','blue-164','blue-221','blue-249','blue-192','gray-67','blue-123','blue-188','blue-266']
STYLES=['Original studio','Warm architecture','Training space','Outdoor athlete','Magazine feature','Topic cover','Practical carousel','Myth and better question','Jelly Beans design family']
TITLES=[
'Put your workout on the calendar','Make the next meal easier','Missed a day? Keep going',
'A plan that fits your life','Fewer food decisions','Give the week a second chance',
'The workout starts before you arrive','Make lunch the easy decision','Your next session still counts',
'Choose a place you want to train','Sort dinner before you head out','Keep a backup route',
'MAKE TIME','FEWER DECISIONS','START AGAIN',
'TOO BUSY\nTO TRAIN?','LUNCH.\nSORTED.','MISSED\nA DAY?',
'YOUR NEXT\n7 DAYS.','LUNCH,\nPLANNED.','YOUR\nPLAN B.',
'I need a free hour.','Every meal must be different.','I missed Monday.']
CAPS=[
"Put your next workout on the calendar before the week fills up. Pick the time, the place and what you plan to do. If the trip to the gym keeps stopping you, choose a home option. What time is your next session?",
"Make tomorrow's lunch a decision you handle today. Pick something you already like, check what you have and get it ready. A prepared meal can help when cooking is the part that keeps falling through. What's your easiest repeat lunch?",
"Missed a workout? Leave that day where it is. Look at the next opening in your calendar and choose a session you can actually do. You don't need a new Monday to make the next decision.",
"I have a home gym and I still pay for a gym membership. The point is having an option that works with your life. If the commute keeps getting in the way, take it out of the plan and start at home.",
"I use a meal prep service. Having food ready removes one more decision from a busy day. You can do the same kind of planning with food you prepare yourself. Choose the meals, get them ready and know what's for lunch before you're hungry.",
"You don't have to throw away the whole week because the plan changed. Look at the days you still have. Choose one thing you can put back in place today, then decide when you'll do it.",
"Choose your workout before you arrive. Save the plan, get your clothes ready and decide when you need to leave. Keep the first decision at the gym about doing the session, not scrolling for a different one.",
"Give lunch a place in your training plan. Decide what you'll eat and where it will come from before you head out. Prepared food, something from home or a planned order: pick an option you can repeat.",
"The last session is already done, or it didn't happen. Either way, the next one still needs a plan. Pick the time and place. If your schedule changed, change the appointment with it.",
"Choose a training setting you want to come back to. Then make the practical part clear: when you're going, what you're doing and how you'll get there. The setting can change. The appointment still matters.",
"Before you head out, decide what you'll eat when you get home. Put a meal in place or choose your order ahead of time. It is one less thing to figure out when you're tired and hungry.",
"Have a backup for the thing most likely to stop you. If getting to your usual training place falls through, know where you can train at home. Write the backup down while the week is still calm.",
"I built a home gym and still use a gym membership. I like having options. If the drive is the reason your workout never happens, start with a plan you can do at home. Make the place fit the time you actually have.",
"Meal prep is one way I make food simpler. You don't need to invent a different lunch every day. Pick a few meals you enjoy and decide how you'll have them ready. Variety can come from rotating your favorites.",
"A missed day needs a next step, not a speech about starting your whole life over. Pick the next available time. Get your things ready. Give yourself a clear place to begin again.",
"Too busy to train? Look at the whole appointment, including packing and travel. If the commute is the obstacle, try a home session from a plan you already know. Put that version on the calendar and prepare the space ahead of time.",
"Lunch sorted means fewer decisions in the middle of the day. Choose two lunches you enjoy, check the ingredients or order details, and decide which days you'll use them. Keep another easy option for the day your plan changes.",
"Missed a day? Decide what happens next. Open the calendar, choose a realistic time and set out what you need. If that time falls through, use the backup you picked in advance. The next action is the useful part.",
"Save this for your next weekly reset. Choose your training times, make a simple food plan and write down what actually happened. At the end of the week, use that record to make next week's plan more realistic.",
"Make lunch easier before the week starts. Pick two familiar meals, check what you need and decide how they will be ready. Use the last slide as your planning checklist. What lunch would you put on repeat?",
"Your backup plan should be specific enough to use on a busy day. Name the obstacle, choose an alternative and write down when you'll switch. Save the checklist and fill it in before you need it.",
"You don't have to wait for a perfect free hour to put a workout in your calendar. Start by finding the time you have, choose an appropriate session from a plan you know, and prepare the space. A home option can remove the commute.",
"Repeating a lunch you enjoy is a planning choice. You can still rotate meals and ingredients across the week. Pick two familiar options, make a shopping or ordering list and keep a backup for the day you need it.",
"Missing Monday doesn't make Tuesday disappear. Name what got in the way, choose your next opening and make one useful preparation now. Swipe for a practical restart, then save the final checklist."
]
# Practical planning guidance adapted from Dan's verified home-training and meal-prep themes.
LESSONS={
'S07-A':[
('01','CHOOSE YOUR\nTRAINING TIMES.','Start with the week you actually have.', ['Pick a time and place for each session.','Use a workout plan you already know.','Choose a backup if travel gets in the way.'],'Write the first appointment in your calendar.'),
('02','MAKE FOOD\nEASIER.','Decide before the busy part of the day.', ['Choose two familiar lunches.','Check what is already in the kitchen.','Plan when to prepare, buy or order them.'],'Put the next lunch in place today.'),
('03','KEEP A SIMPLE\nRECORD.','Track the plan you actually followed.', ['Mark the sessions you completed.','Note which meals were easiest to repeat.','Write down the obstacle that came up.'],'Use the record to adjust next week.'),
('CHECKLIST','YOUR WEEK,\nREADY TO GO.','Save this and fill in the blanks.', ['Training times: __________________','Lunch choices: __________________','Backup option: __________________','Weekly review: __________________'],'Keep what worked. Adjust what did not.')],
'S07-B':[
('01','PICK TWO\nLUNCHES.','Choose meals you already enjoy.', ['List two lunches you would happily repeat.','Rotate those choices across the week.','Leave room to change the plan.'],'Example: chicken and rice; a bean bowl.'),
('02','CHECK WHAT\nYOU NEED.','Turn the choices into a short list.', ['Check the fridge, freezer and cupboard.','List the ingredients you are missing.','Or choose your prepared-meal order.'],'Buy for the lunches you actually planned.'),
('03','GIVE LUNCH\nA TIME.','Decide how it will be ready.', ['Choose when to prepare or collect the food.','Follow storage and reheating instructions.','Pick a backup for a day away from home.'],'Make the plan before the lunch rush.'),
('CHECKLIST','LUNCH\nIS HANDLED.','Save this for your next food shop.', ['Lunch one: ______________________','Lunch two: ______________________','Buy or order: ____________________','Backup meal: ____________________'],'Repeat your favorites. Rotate when you want.')],
'S07-C':[
('01','NAME THE\nOBSTACLE.','Be specific about what gets in the way.', ['Is it the commute?','A meeting that often runs late?','Equipment you cannot always get to?'],'Solve the obstacle you actually have.'),
('02','CHOOSE YOUR\nBACKUP.','Make it something you can use.', ['Pick a familiar home-workout option.','Choose the space and any equipment.','Save the plan where you can find it.'],'Example: if travel fails, use the home plan.'),
('03','SET THE\nSWITCH POINT.','Decide when the backup takes over.', ['Write down the situation that triggers it.','Choose the time for the backup session.','Get the space ready in advance.'],'If the late meeting runs over, use Plan B.'),
('CHECKLIST','WRITE YOUR\nPLAN B.','Save this and make it yours.', ['If this happens: __________________','I will do this: ____________________','At this time: _____________________','I need to prepare: ________________'],'A backup works best when it is already chosen.')],
'S08-A':[
('REFRAME','CHECK THE\nTIME YOU HAVE.','An empty hour is not the only opening.', ['Look at the full appointment, including travel.','Find a realistic opening in your day.','Choose a suitable session from a familiar plan.'],'Start with your calendar, then choose the session.'),
('EXAMPLE','TAKE OUT\nTHE COMMUTE.','When travel is the thing stopping you.', ['Use a home option from your workout plan.','Prepare the space before the planned time.','Keep the gym for days when the trip fits.'],'The place can change with your schedule.'),
('ACTION','MAKE ONE\nAPPOINTMENT.','Decide the details now.', ['Write down the time.','Save the workout you plan to use.','Set out the equipment you need.'],'No browsing for a new plan at the last minute.'),
('SAVE THIS','YOUR NEXT\nSESSION.','A simple planning card.', ['Time: ___________________________','Place: __________________________','Workout plan: ___________________','Backup: _________________________'],'Choose the appointment you can actually keep.')],
'S08-B':[
('REFRAME','REPEAT\nYOUR FAVORITES.','A familiar lunch can simplify your day.', ['Choose meals you enjoy eating.','Rotate a few choices through the week.','Change ingredients when you want variety.'],'Repeating lunch does not mean one food forever.'),
('EXAMPLE','TWO LUNCHES.\nONE LIST.','Start with a small, useful menu.', ['Pick one lunch for the days you are home.','Pick another for the days you are out.','List what you need to buy or order.'],'Keep the menu realistic for your actual week.'),
('ACTION','MAKE THE\nNEXT ONE EASY.','Put tomorrow\'s lunch in place.', ['Check the food you already have.','Decide how the meal will be ready.','Choose an alternative if plans change.'],'Follow the food\'s storage and reheating directions.'),
('SAVE THIS','YOUR REPEAT\nLUNCH LIST.','Fill this in before the week starts.', ['Favorite one: ____________________','Favorite two: ____________________','Buy or order: ____________________','Backup: _________________________'],'Simple enough to use. Flexible enough to change.')],
'S08-C':[
('REFRAME','MONDAY IS\nONE DAY.','Look at the time that is still available.', ['Do not erase the rest of the week.','Open your calendar.','Choose the next realistic training time.'],'Make the next decision useful.'),
('EXAMPLE','CHANGE THE\nAPPOINTMENT.','Move the plan to where it can happen.', ['Late meeting on Monday?','Find an opening on another day.','Use your backup if the usual place will not fit.'],'A changed plan can still be a clear plan.'),
('ACTION','PREPARE\nONE THING.','Make the next start easier.', ['Set out your training clothes.','Save the session you will use.','Decide when you need to begin.'],'Choose one preparation and do it now.'),
('SAVE THIS','YOUR RESTART\nCHECKLIST.','Use this after a missed day.', ['Next session: ____________________','Time and place: __________________','Prepare now: ____________________','Backup: _________________________'],'Restart with one appointment, not a perfect week.')]
}
# Round 2: Dan requested the two copy swaps, martial arts copy and three additions.
TITLES[3],TITLES[7]=TITLES[7],TITLES[3]
CAPS[3],CAPS[7]=CAPS[7],CAPS[3]
TITLES[11]='Train martial arts. Lift weights too.'
CAPS[11]="Martial arts can burn calories, challenge your cardio and give you a reason to keep showing up. It is a great way to stay active, build fitness and support getting leaner. But I would not use it as a replacement for weight training. Lifting builds and maintains the muscle you want to keep as you lose fat. Pair the two, leave room to recover, and keep your food intake aligned with your goal. Train your conditioning and your strength."
TITLES.extend(['MAKE TIME.\nGET STRONG.','LUNCH.\nHANDLED.','TRAIN HARD.\nLIFT TOO.'])
CAPS.extend([
"Make strength training an appointment you can keep. Choose the time, save the workout and get your space ready. If getting to the gym is the obstacle, have a home option ready. The useful plan is the one that fits into your actual day.",
"Lunch gets easier when the decision is already made. Choose a meal you enjoy, get the ingredients or order in place, and keep a second option for busy days. You do not need a brand-new menu every afternoon. You need something you can repeat.",
"Martial arts can challenge your cardio and help you burn calories. Weight training builds and maintains muscle. Make room for both in your week, with enough recovery between hard sessions. Getting leaner also depends on what you eat, so give your food plan the same attention as your training."
])
posts=[]
for i,s in enumerate(SOURCES):
 st=i//3+1; v='ABC'[i%3]; ident=f'S{st:02}-{v}'
 cap=CAPS[i]
 if st in [2,3,4,9]:cap+='\n\nReal studio photograph of me. The background was created with AI.'
 posts.append(dict(id=ident,number=i+1,style=st,style_name=STYLES[st-1],source='studio-'+s,topic=['Training time','Repeatable meals','Restart and backup'][i%3],title=TITLES[i],caption=cap,slides=5 if st in [7,8] else 1))
for p in posts:
 if p['id'] in ['S04-C','S09-C']:p['topic']='Martial arts and weight training'
 if p['id']=='S02-A':p['topic']='Repeatable meals'
 if p['id']=='S03-B':p['topic']='Training time'
(ROOT/'posts.json').write_text(json.dumps(posts,indent=2))
# Three close portraits use a conservative waistband crop. No leg opening survives.
CROPS={'studio-blue-11':3650,'studio-blue-5':3570,'studio-gray-67':3810}
meta=[]
previous={m['id']:m for m in json.loads((ROOT/'source-map.json').read_text())} if (ROOT/'source-map.json').exists() else {}
for p in posts:
 old=previous.get(p['id'])
 if old and Path(old['source']).name==p['source']+'_FINAL_PRIMARY.jpg':
  p['crop']=old['crop'];p['source_sha256']=old['sha256'];p['asset_size']=Image.open(ROOT/'assets'/(p['source']+'.png')).size;meta.append(old);continue
 name=p['source']; orig=LIB/(name+'_FINAL_PRIMARY.jpg'); im=Image.open(orig).convert('RGB'); cut=Image.open(LIB/'_cutouts'/(name+'_CUTOUT.png')).convert('RGBA'); alpha=cut.getchannel('A'); exact=im.copy().convert('RGBA');exact.putalpha(alpha)
 bbox=alpha.getbbox(); bottom=CROPS.get(name,im.height)
 box=(max(0,bbox[0]-20),max(0,bbox[1]-20),min(im.width,bbox[2]+20),bottom)
 exact=exact.crop(box); exact.thumbnail((1500,2000),Image.Resampling.LANCZOS); exact.save(ROOT/'assets'/(name+'.png'))
 mono=ImageOps.grayscale(exact).convert('RGBA');mono.putalpha(exact.getchannel('A'));mono.save(ROOT/'assets'/(name+'-mono.png'))
 # Photograph frame keeps the original studio pixels.
 top=max(0,bbox[1]-130); h=bottom-top; w=min(im.width,round(h*.8));left=max(0,min(im.width-w,round((bbox[0]+bbox[2]-w)/2)))
 photo=im.crop((left,top,left+w,top+round(w/0.8)));photo=photo.resize((1080,1350),Image.Resampling.LANCZOS);photo.save(ROOT/'assets'/(name+'-photo.jpg'),quality=97)
 p['crop']=dict(person_box=list(box),photographic_box=[left,top,left+w,top+round(w/.8)],waistband_crop=name in CROPS)
 p['source_sha256']=hashlib.sha256(orig.read_bytes()).hexdigest()
 p['asset_size']=exact.size
 meta.append(dict(id=p['id'],source=str(orig),sha256=p['source_sha256'],crop=p['crop'],shirtless=True))
(ROOT/'source-map.json').write_text(json.dumps(meta,indent=2))
# White cutout outline for the three new portrait designs.
from PIL import ImageFilter
for p in posts:
 if p['style']!=9: continue
 im=Image.open(ROOT/'assets'/(p['source']+'.png')).convert('RGBA')
 canvas=Image.new('RGBA',(im.width+48,im.height+48));canvas.alpha_composite(im,(24,24))
 alpha=canvas.getchannel('A').filter(ImageFilter.MaxFilter(25))
 white=Image.new('RGBA',canvas.size,'white');white.putalpha(alpha);white.alpha_composite(canvas)
 white.save(ROOT/'assets'/(p['source']+'-outline.png'))
N='#09203e';B='#165bea';ICE='#dcedf6';PAPER='#f6f4ed'
def esc(t):return html.escape(str(t))
def rect(x,y,w,h,fill,rx=0):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
def text(t,x,y,size=40,color=N,font='Arial',weight=400,spacing=0):
 return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" fill="{color}">{esc(t)}</text>'
def lines(t,x,y,size=100,color=N,font='Impact',leading=1.05):return ''.join(text(v,x,y+j*size*leading,size,B if v in ['TRAIN?','SORTED.','A DAY?','TODAY?','to REPEAT?'] else color,font) for j,v in enumerate(t.split('\n')))
def picture(path,x,y,w,h):
 path=ROOT/path; mime='image/png' if path.suffix=='.png' else 'image/jpeg';uri='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode()
 return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="none" href="{uri}"/>'
def person(p,x,y,w,h,mono=False):
 name=p['source']+('-mono' if mono else '')+'.png';aw,ah=p['asset_size']; scale=min(w/aw,h/ah);ww=aw*scale;hh=ah*scale
 return picture(Path('assets')/name,x+(w-ww)/2,y+h-hh,ww,hh)
def footer(p,slide=1):
 return rect(64,1262,952,2,'#afbfce')+text('DAN ROSE',64,1311,23,N,'Arial',700,3)+text(f'{slide} / {p["slides"]}',945,1311,25,N)
def wrap(t,lim):
 import textwrap
 return '\n'.join(textwrap.wrap(t,lim))
def generate(p,slide):
 st=p['style'];var='ABC'.index(p['id'][-1]);s=''
 if st==1:
  s=picture(Path('assets')/('studio-blue-11-photo-r2.png' if p['id']=='S01-C' else p['source']+'-photo.jpg'),0,0,1080,1350)
 elif st in [2,3,4]:
  s=picture(Path('assets')/f'background-{st:02}.jpg',0,0,1080,1350)+person(p,30,65,1020,1380)
  s+=rect(40,26,326,38,'#f6f4ed',4)+text('REAL PHOTO / AI BACKGROUND',52,52,19,N,'Arial',700)
 elif st==5:
  s=rect(0,0,1080,1350,PAPER)
  s+=text('STRENGTH / FOOD / CONSISTENCY',60,62,23,N,'Arial',700,3)
  if var==1:
   s+=lines('FEWER\nDECISIONS',55,195,134,'#111','Impact',.95)
  else:
   s+=text(['MAKE TIME','','START AGAIN'][var],55,242,177 if var==0 else 157,'#111','Impact')
  s+=rect(60,337,960,4,'#111')
  s+=person(p,429,379,651,971,True)
  points=[
   [('BOOK THE','SESSION','Choose a time you can keep.'),('SKIP THE','COMMUTE','Have a home option ready.'),('KEEP A','PLAN B','Know your next best option.')],
   [('PICK YOUR','FAVORITES','A few lunches you enjoy.'),('PREP IT','ONCE','Make the busy days easier.'),('REPEAT.','ROTATE.','Simple does not mean boring.')],
   [('ONE DAY','IS ONE DAY','Keep the rest of your week.'),('CHOOSE THE','NEXT STEP','Put a session on the calendar.'),('GET YOUR','GEAR READY','Make the next start easier.')]
  ][var]
  for j,(a,b,c) in enumerate(points):
   y=472+j*253
   s+=text(f'0{j+1}',62,y,23,B,'Arial',700,2)+rect(62,y+15,62,4,B)
   s+=lines(a+'\n'+b,60,y+79,51,'#111','Impact',1.03)
   s+=lines(wrap(c,24),62,y+169,25,N,'Arial',1.3)
  s+=text('WITH DAN ROSE',62,1298,22,N,'Arial',700,2)
 elif st==6:
  s=rect(0,0,1080,1350,ICE)+text('THE RESET',64,77,25,N,'Arial',700,5)+rect(64,99,245,4,B)
  if p['crop']['waistband_crop']:
   s+=person(p,485,350,790,1000)
  else:s+=person(p,492,160,640,1190)
  title=['TOO BUSY\nTO\nTRAIN?','LUNCH.\nSORTED.','MISSED\nA DAY?'][var]
  s+=lines(title,60,280,135,N)
  s+=rect(64,765,92,7,B)
  s+=lines(['Start with the time\nyou actually have.','Pick two lunches.\nMake the next one easy.','Choose the next\nappointment.'][var],64,850,35,N,'Arial',1.45)
  s+=text('DAN ROSE',64,1295,24,N,'Arial',700,3)
 elif st==9:
  theme=['training','lunch','martial'][var]
  s=picture(Path('assets')/f'jelly-{theme}.png',0,0,1080,1350)
  s+=rect(0,0,1080,345,'#080b0e')
  for j,line in enumerate(p['title'].split('\n')):
   s+=text(line,54,160+j*139,145 if var!=2 else 141,'white' if j==0 else ['#4dd8ff','#9efb91','#ff645c'][var],'Impact')
  # Original photograph with a crisp white outline, composited locally.
  name=p['source']+'-outline.png'
  aw,ah=Image.open(ROOT/'assets'/name).size
  w=990 if var==0 else 880; h=w*ah/aw
  x=(1080-w)/2 if var==0 else 175
  s+=picture(Path('assets')/name,x,390,w,h)
  s+=f'<rect x="24" y="24" width="1032" height="1302" rx="24" fill="none" stroke="white" stroke-width="4"/>'
  s+=rect(40,1305,1000,5,['#4dd8ff','#9efb91','#ff645c'][var])
 elif st==7 and slide==1:
  s=rect(0,0,1080,1350,PAPER)+text('THE SAVEABLE SERIES',64,73,23,N,'Arial',700,3)+rect(64,100,952,3,B)
  s+=person(p,526,405,554,840)
  s+=lines(p['title'],63,247,131,N)
  s+=text(['A simple weekly reset.','Fewer decisions at lunchtime.','For the days that change.'][var],65,445,33,N,'Arial',700)
  items=[['Choose your training times','Make food easier','Keep a simple record'],['Pick two familiar lunches','Check what you need','Decide how they will be ready'],['Name the obstacle','Choose your backup','Set the switch point']][var]
  for j,t in enumerate(items):
   s+=text('0'+str(j+1),65,730+j*115,34,B,'Arial',700)+lines(wrap(t,21),128,730+j*115,32,N,'Arial',1.25)
  s+=text('Swipe for the checklist >',65,1188,27,N,'Arial',700)+footer(p)
 elif st==8 and slide==1:
  s=rect(0,0,1080,1350,ICE)+text('THE MINDSET RESET',64,74,24,N,'Arial',700,4)
  s+=person(p,557,298,570,952)
  s+=rect(40,133,525,408,'#f2f3f3',12)+rect(40,568,525,459,'#f7fbfe',12)
  s+=text('THE MYTH',65,198,24,'#546378','Arial',700,3)
  s+=lines(['I need a\nfree hour.','Every meal\nmust be\ndifferent.','I missed\nMonday.\nWeek ruined.'][var],65,282,67,N,'Arial Narrow',1.1)
  s+=text('THE BETTER QUESTION',65,632,23,B,'Arial',700,1)
  s+=lines(['What time\ndo I have\nTODAY?','What can I\nmake easy\nto REPEAT?','What can\nI do\nTODAY?'][var],65,724,65,N,'Arial Narrow',1.12)
  s+=text('Swipe for a practical next step >',64,1174,27,N,'Arial',700)+footer(p)
 else:
  label,title,sub,items,payoff=LESSONS[p['id']][slide-2]
  s=rect(0,0,1080,1350,PAPER if st==7 else ICE)+text('THE SAVEABLE SERIES' if st==7 else 'THE MINDSET RESET',64,74,24,N,'Arial',700,3)+rect(64,103,952,3,B)
  s+=text(label,65,170,30,B,'Arial',700,2)+lines(title,63,302,106,N)
  s+=text(sub,65,484,35,N,'Arial',400)
  for j,t in enumerate(items):
   y=572+j*137
   s+=rect(64,y-30,48,48,'white',5)+text('0'+str(j+1) if slide<5 else '',72,y+4,24,B,'Arial',700)
   if slide==5:s+=f'<rect x="78" y="{y-15}" width="19" height="19" fill="none" stroke="{B}" stroke-width="2"/>'
   s+=lines(wrap(t,34),140,y+6,44,N,'Arial',1.2)
  s+=rect(64,1130,952,93,N,8)+lines(wrap(payoff,48),88,1167,32,'white','Arial',1.2)+footer(p,slide)
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1350" viewBox="0 0 1080 1350">'+s+'</svg>'
 assert '\u2014' not in svg and '\u2013' not in svg
 out=ROOT/'templates'/f'{p["id"]}-{slide:02}.svg';out.write_text(svg)
for p in posts:
 for slide in range(1,p['slides']+1):generate(p,slide)
(ROOT/'posts.json').write_text(json.dumps(posts,indent=2))
(ROOT/'captions.txt').write_text('\n\n'.join(p['id']+' | '+p['title'].replace('\n',' ')+'\n'+p['caption'] for p in posts)+'\n')
print('Built 27 posts, 51 editable SVG layouts and cropped person layers.')
