'use strict';
const crypto=require('crypto');
const INTERVAL=1800000;
function shuffled(values,random=n=>crypto.randomInt(n)) {
 const result=[...values];for(let i=result.length-1;i>0;i--){const j=random(i+1);[result[i],result[j]]=[result[j],result[i]];}return result;
}
function choose(images,displays,previous,now,random) {
 const ids=[...new Set(images)],target=Math.min(ids.length,displays.length);
 if(!ids.length)return [];
 const due=displays.filter(d=>!ids.includes(previous[d]?.sha256)||!(previous[d]?.nextChangeAt>now));
 const fixed=Object.fromEntries(displays.filter(d=>!due.includes(d)).map(d=>[d,previous[d].sha256]));
 for(const [noRepeat,distinct] of [[true,true],[false,true],[true,false],[false,false]]) {
  function search(index,choices) {
   if(index===due.length)return !distinct||new Set(Object.values(choices)).size>=target ? choices : null;
   const display=due[index];
   for(const sha of shuffled(ids,random)) {
    if(noRepeat&&ids.length>1&&previous[display]?.sha256===sha)continue;
    if(distinct&&ids.length>=displays.length&&Object.values(choices).includes(sha))continue;
    const result=search(index+1,{...choices,[display]:sha});if(result)return result;
   }
   return null;
  }
  const choices=search(0,fixed);if(choices)return due.map(id=>({id,sha256:choices[id],nextChangeAt:now+INTERVAL}));
 }
 throw Error('No wallpaper selection');
}
module.exports={choose,INTERVAL};
