'use strict';
const {randomUUID} = require('node:crypto');
const names = ['Unassigned tasks', 'Dan’s task queue', 'Codex task queue', 'Claude task queue', 'Dan in progress', 'Claude in progress', 'Codex in progress', 'Codex in review', 'Claude in review', 'Done'];
const colors = ['slate','green','amber','blue','rose','purple'];
class BoardError extends Error { constructor(message, status=400) { super(message); this.status=status; } }
function text(value, max, required=false) {
  if(typeof value !== 'string' || value.length>max || (required && !value.trim())) throw new BoardError('Please check the text length and required fields.');
  return value.trim();
}
function initial() { return {lists:names.map((name,i)=>({id:randomUUID(),name,tone:i===2||i===6||i===7?'codex':i===3||i===5||i===8?'claude':i===1||i===4?'dan':i===9?'done':'',archived:false})),cards:[],activity:[]}; }
function mutate(input, action, p={}, file) {
  const board=structuredClone(input), date=new Date().toISOString();
  const list=id=>{const x=board.lists.find(x=>x.id===id);if(!x)throw new BoardError('List not found.',404);return x;};
  const card=id=>{const x=board.cards.find(x=>x.id===id);if(!x)throw new BoardError('Card not found.',404);return x;};
  let note='', target=null, removedFile=null;
  function editable(c) { if(c.archived||list(c.listId).archived) throw new BoardError('Restore this card and its list before editing.'); }
  function move(items,item,index) { if(!Number.isInteger(index)||index<0||index>items.length)throw new BoardError('Invalid position.');const a=items.filter(x=>x.id!==item.id);a.splice(Math.min(index,a.length),0,item);return a; }
  switch(action) {
    case 'list.create': {
      if(board.lists.length>=50)throw new BoardError('This board supports up to 50 lists, including archived lists.');
      const name=text(p.name,100,true);board.lists.push({id:randomUUID(),name,tone:'',archived:false});note=`Created list: ${name}`;break;
    }
    case 'list.update': { const l=list(p.id);l.name=text(p.name,100,true);note=`Renamed list: ${l.name}`;break; }
    case 'list.move': { const l=list(p.id);if(l.archived)throw new BoardError('Restore this list first.');const active=move(board.lists.filter(x=>!x.archived),l,p.index);board.lists=[...active,...board.lists.filter(x=>x.archived)];note=`Moved list: ${l.name}`;break; }
    case 'list.archive': case 'list.restore': {const l=list(p.id);l.archived=action==='list.archive';note=`${l.archived?'Archived':'Restored'} list: ${l.name}`;break;}
    case 'card.create': {
      const l=list(p.listId);if(l.archived)throw new BoardError('Restore this list first.');
      if(board.cards.length>=2000)throw new BoardError('This board supports up to 2,000 cards, including archived cards.');
      const c={id:randomUUID(),listId:l.id,title:text(p.title,200,true),description:'',labels:[],dueDate:'',checklist:[],comments:[],attachments:[],archived:false,createdAt:date,updatedAt:date};board.cards.push(c);target=c.id;note=`Created card: ${c.title}`;break;
    }
    case 'card.update': {
      const c=card(p.id);editable(c);c.title=text(p.title,200,true);c.description=text(p.description,20000);
      if(!Array.isArray(p.labels)||p.labels.length>12)throw new BoardError('Use at most 12 labels.');
      c.labels=p.labels.map(l=>({name:text(l.name,40,true),color:colors.includes(l.color)?l.color:'slate'}));
      if(typeof p.dueDate!=='string'||(p.dueDate && (!/^\d{4}-\d{2}-\d{2}$/.test(p.dueDate)||!Number.isFinite(Date.parse(p.dueDate))||new Date(p.dueDate).toISOString().slice(0,10)!==p.dueDate)))throw new BoardError('Choose a valid due date.');
      c.dueDate=p.dueDate;c.updatedAt=date;target=c.id;note=`Updated card: ${c.title}`;break;
    }
    case 'card.move': {
      const c=card(p.id);editable(c);const l=list(p.listId);if(l.archived)throw new BoardError('Restore the destination list first.');
      const dest=board.cards.filter(x=>x.listId===l.id&&!x.archived);const ordered=move(dest,c,p.index);
      c.listId=l.id;c.updatedAt=date;const ids=new Set(ordered.map(x=>x.id));board.cards=[...board.cards.filter(x=>!ids.has(x.id)),...ordered];target=c.id;note=`Moved ${c.title} to ${l.name}`;break;
    }
    case 'card.archive': case 'card.restore': {const c=card(p.id);if(action==='card.restore'&&list(c.listId).archived)throw new BoardError('Restore the card’s list first.');c.archived=action==='card.archive';c.updatedAt=date;target=c.id;note=`${c.archived?'Archived':'Restored'} card: ${c.title}`;break;}
    case 'check.add': {const c=card(p.id);editable(c);if(c.checklist.length>=100)throw new BoardError('Checklist limit reached.');c.checklist.push({id:randomUUID(),text:text(p.text,500,true),done:false});target=c.id;note=`Added checklist item to ${c.title}`;break;}
    case 'check.update': case 'check.delete': {const c=card(p.id);editable(c);const item=c.checklist.find(x=>x.id===p.itemId);if(!item)throw new BoardError('Checklist item not found.',404);if(action==='check.delete')c.checklist=c.checklist.filter(x=>x.id!==item.id);else{if(typeof p.done!=='boolean')throw new BoardError('Invalid checklist state.');item.done=p.done;item.text=text(p.text,500,true);}target=c.id;note=`Updated checklist on ${c.title}`;break;}
    case 'comment.add': {const c=card(p.id);editable(c);if(c.comments.length>=200)throw new BoardError('Comment limit reached.');c.comments.push({id:randomUUID(),text:text(p.text,5000,true),createdAt:date});target=c.id;note=`Commented on ${c.title}`;break;}
    case 'attachment.add': {const c=card(p.id);editable(c);if(!file)throw new BoardError('Choose a file.');if(c.attachments.length>=10)throw new BoardError('Use at most 10 attachments per card.');const used=board.cards.reduce((sum,x)=>sum+x.attachments.reduce((n,a)=>n+a.size,0),0);if(used+file.size>100*1024*1024)throw new BoardError('The board’s 100 MB attachment limit is reached.');c.attachments.push({id:file.id,name:file.name,mime:file.mime,size:file.size,createdAt:date});target=c.id;note=`Attached ${file.name} to ${c.title}`;break;}
    case 'attachment.remove': {const c=card(p.id);editable(c);const a=c.attachments.find(x=>x.id===p.attachmentId);if(!a)throw new BoardError('Attachment not found.',404);c.attachments=c.attachments.filter(x=>x.id!==a.id);removedFile=a.id;target=c.id;note=`Removed attachment ${a.name} from ${c.title}`;break;}
    default: throw new BoardError('Unknown board action.');
  }
  if(target)card(target).updatedAt=date;
  board.activity.unshift({id:randomUUID(),at:date,text:note,cardId:target});board.activity=board.activity.slice(0,500);
  return {board,target,removedFile};
}
module.exports={initial,mutate,BoardError,colors};
