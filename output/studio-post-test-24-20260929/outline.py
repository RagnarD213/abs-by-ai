from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import xml.etree.ElementTree as ET
import json
R=Path(__file__).resolve().parent
D=Path('/System/Library/Fonts/Supplemental')
cache={}
def fontfile(f,w):
 if f=='Impact': return 'Impact.ttf'
 if f=='Arial Black':return 'Arial Black.ttf'
 if f=='Arial Narrow':return 'Arial Narrow Bold.ttf'
 return 'Arial Bold.ttf' if w>=600 else 'Arial.ttf'
def outlines(elem):
 family=elem.attrib['font-family'];weight=int(elem.attrib['font-weight']);key=fontfile(family,weight)
 if key not in cache:cache[key]=TTFont(D/key)
 f=cache[key];units=f['head'].unitsPerEm;sz=float(elem.attrib['font-size']);scale=sz/units;cmap=f.getBestCmap();gs=f.getGlyphSet();x=float(elem.attrib['x']);y=float(elem.attrib['y']);spacing=float(elem.attrib.get('letter-spacing',0));start=x
 group=ET.Element('g',{'aria-label':elem.text or '', 'fill':elem.attrib['fill']})
 for char in elem.text or '':
  name=cmap.get(ord(char),'.notdef');pen=SVGPathPen(gs);gs[name].draw(pen);p=pen.getCommands()
  if p:ET.SubElement(group,'path',{'d':p,'transform':f'translate({x:.3f} {y:.3f}) scale({scale:.6f} {-scale:.6f})'})
  x+=f['hmtx'].metrics[name][0]*scale+spacing
 return group,dict(text=elem.text,x=start,right=x,y=y,size=sz,family=family)
(R/'outlined').mkdir(exist_ok=True);bounds=[]
for file in sorted((R/'templates').glob('*.svg')):
 root=ET.parse(file).getroot()
 for j,el in enumerate(list(root)):
  if el.tag.endswith('text'):
   group,b=outlines(el);root.remove(el);root.insert(j,group);b['file']=file.name;bounds.append(b)
 ET.register_namespace('','http://www.w3.org/2000/svg');ET.ElementTree(root).write(R/'outlined'/file.name,encoding='unicode')
(R/'qa/text-bounds.json').write_text(json.dumps(bounds,indent=2))
print('Outlined fonts for stable export. Editable text preserved in templates/.')
print('Text beyond right safety margin:',[(x['file'],x['text'],round(x['right'])) for x in bounds if x['right']>1030])
