'use strict';
(() => {
  const $=id=>document.getElementById(id), button=$('favorite-image');
  let source=null,current=null,next=null,busy=false,loading=false;
  const text=(id,value)=>{$(id).textContent=value;};
  const date=value=>new Date(value+'T12:00:00Z').toLocaleDateString('en-US',{timeZone:'America/Chicago',month:'short',day:'numeric',year:'numeric'});
  function node(tag,value){const e=document.createElement(tag);if(value!==undefined)e.textContent=value;return e;}
  async function request(url,options={}) {
    const controller=new AbortController(),timeout=setTimeout(()=>controller.abort(),15000);
    try {const response=await fetch(url,{credentials:'same-origin',cache:'no-store',...options,signal:controller.signal});
      if(response.status===401){location.replace('/brief-login');throw Error('Sign in to your private brief.');}
      if(!response.ok)throw Error(response.status===409 ? 'The displayed image changed. Reload the brief before saving.' : 'Change could not be confirmed. Refresh favorites before retrying.');
      return await response.json();
    } finally {clearTimeout(timeout);}
  }
  const displayed=()=>source && new URL($('daily-image').src,location.href).searchParams.get('sha256')===source.sha256 && $('daily-image').naturalWidth;
  function state(){button.disabled=busy || !displayed();button.setAttribute('aria-pressed',String(!!current?.active));button.textContent=busy ? 'Saving…' : current?.active ? 'Remove from wallpaper favorites' : 'Save to wallpaper favorites';}
  const write=(url,method,body)=>request(url,{method,headers:{'Content-Type':'application/json','X-Brief-Action':'favorite'},body:JSON.stringify(body)});
  async function change(sha256,active){return write('/api/brief/favorites/'+sha256,'PUT',{active});}
  function card(row){
    const box=node('article');box.className='favorite-card';const img=node('img');img.src=`/api/brief/favorites/${row.sha256}/image`;img.alt=`Private favorite from ${date(row.forDate)}`;img.loading='lazy';
    const label=node('p',`${date(row.forDate)} · ${row.active ? 'In favorites' : 'Removed, original retained'}`);
    const download=node('a','Download original');download.href=img.src;download.download='';
    const toggle=node('button',row.active ? 'Remove from favorites' : 'Restore to favorites');toggle.type='button';
    const status=node('p');status.className='note';status.setAttribute('role','status');
    toggle.addEventListener('click',async()=>{toggle.disabled=true;status.textContent='Saving…';try{
      const result=await change(row.sha256,!row.active);row=result.favorite;label.textContent=`${date(row.forDate)} · ${row.active ? 'In favorites' : 'Removed, original retained'}`;toggle.textContent=row.active ? 'Remove from favorites' : 'Restore to favorites';
      status.textContent=row.active ? result.wallpaper.message : 'Removed from rotation eligibility. Original retained; restore any time. Mac update pending.';
      if(source?.sha256===row.sha256){current=row;state();text('favorite-status',status.textContent);}
    }catch(e){status.textContent=e.message;}finally{toggle.disabled=false;}});
    box.append(img,label,download,toggle,status);return box;
  }
  async function favorites(reset=false){
    if(loading)return;loading=true;$('favorites-refresh').disabled=true;$('favorites-more').disabled=true;
    if(reset){next=null;$('favorites-grid').replaceChildren();}
    try{const result=await request('/api/brief/favorites'+(next ? '?after='+next : ''));for(const row of result.rows){$('favorites-grid').append(card(row));if(source?.sha256===row.sha256)current=row;}
      next=result.next;$('favorites-more').hidden=!next;text('favorites-status',result.rows.length || $('favorites-grid').children.length ? result.wallpaper.message : 'No favorites yet. Save an image above to start your private collection.');state();
    }catch(e){text('favorites-status',e.message);}finally{loading=false;$('favorites-refresh').disabled=false;$('favorites-more').disabled=false;}
  }
  let generation=0;
  async function initialize(){
    const ownGeneration=++generation;source=null;current=null;state();
    try{const data=await request('/api/brief/data'),expected=data.image;
      const url=new URL($('daily-image').src,location.href);
      if(ownGeneration!==generation)return;
      // Metadata can race publication or a page refresh. Never enable a choice
      // unless the image actually displayed is the exact original digest.
      if(!expected || !data.imageAvailable || url.searchParams.get('sha256')!==expected.sha256 || !$('daily-image').naturalWidth)return;
      source=expected;
      const manifest=await request('/api/brief/favorites/manifest');
      if(ownGeneration!==generation)return;
      current=manifest.rows.find(r=>r.sha256===expected.sha256)||null;state();
      text('favorite-status',current ? manifest.wallpaper.message : 'Save this original image to your private favorites.');
    }catch{if(ownGeneration===generation){source=null;state();text('favorite-status','Favorite status unavailable. Refresh the page to try again.');}}
  }
  $('daily-image').addEventListener('load',initialize);
  button.addEventListener('click',async()=>{
    if(busy || !displayed()){source=null;state();return;}busy=true;state();text('favorite-status','Saving your choice…');
    try{const result=current?.active ? await change(source.sha256,false) : await write('/api/brief/favorites','POST',{sha256:source.sha256,forDate:source.forDate});
      current=result.favorite;text('favorite-status',current.active ? result.wallpaper.message : 'Removed from rotation eligibility. Original retained; restore any time. Mac update pending.');
      if($('favorites-details').open)await favorites(true);
    }catch(e){text('favorite-status',e.message);}finally{busy=false;state();}
  });
  $('daily-image').addEventListener('error',()=>{generation++;source=null;state();});
  $('favorites-details').addEventListener('toggle',()=>{if($('favorites-details').open)favorites(true);});
  $('favorites-more').addEventListener('click',()=>favorites());$('favorites-refresh').addEventListener('click',()=>favorites(true));
  initialize();
})();
