'use strict';
const {randomUUID}=require('node:crypto');
const columns=[['planned','Planned for Today','dan'],['progress','In Progress','dan'],['completed','Completed','done']];
const today=()=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/Chicago',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
function simplify(input){
  const b=structuredClone(input);
  if(b.personalVersion===1)return b;
  b.legacyLayout={at:new Date().toISOString(),lists:structuredClone(b.lists),execution:structuredClone(b.execution||null)};
  const matches={planned:/^(Dan[’']s task queue|Planned for Today)$/i,progress:/^(Dan in progress|In Progress)$/i,completed:/^(Done|Completed)$/i};
  const chosen=columns.map(([role,name,tone])=>{
    const l=b.lists.find(l=>!l.archived&&matches[role].test(l.name))||{id:randomUUID()};
    return {...l,role,name,tone,archived:false};
  });
  const ids=new Set(chosen.map(l=>l.id));
  for(const c of b.cards){if(ids.has(c.listId)&&!c.plannedFor)c.plannedFor=today();if(c.run?.status==='queued'){c.run.status='cancelled';c.run.summary='The workboard is now for personal planning.';}}
  b.lists=[...chosen,...b.lists.filter(l=>!ids.has(l.id)).map(l=>({...l,archived:true,legacy:true}))];
  b.execution={...(b.execution||{}),enabled:false,paused:true};
  b.personalVersion=1;b.plans||={};b.preferences={...b.preferences,rewards:true};
  return b;
}
function makeInitial(){return {personalVersion:1,lists:columns.map(([role,name,tone])=>({id:randomUUID(),role,name,tone,archived:false})),cards:[],activity:[],plans:{},preferences:{rewards:true}};}
module.exports={simplify,makeInitial,today,columns};
