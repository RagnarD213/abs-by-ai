'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const html=fs.readFileSync(require.resolve('../web/page.html'),'utf8');
let focused=null,pausedCount=0,backCount=0,pushCount=0;
class Node {
 constructor(tag='div'){this.tag=tag;this.children=[];this.events={};this.attributes={};this.style={};this.textContent='';this.className='';this.hidden=false;this.paused=true;this.duration=43;this.videoWidth=1080;this.videoHeight=1920;this.currentTime=.001;this.open=false;}
 append(...n){this.children.push(...n);} prepend(...n){this.children.unshift(...n);} replaceChildren(...n){this.children=n;}
 addEventListener(k,f){(this.events[k]||=[]).push(f);} fire(k,e={}){return Promise.all((this.events[k]||[]).map(f=>f(e)));}
 setAttribute(k,v){this.attributes[k]=v;}getAttribute(k){return this.attributes[k]||null;}removeAttribute(k){delete this.attributes[k];if(k==='src')this.src='';}
 querySelector(tag){for(const n of this.children){if(n.tag===tag)return n;const found=n.querySelector?.(tag);if(found)return found;}return null;}
 getContext(){return {drawImage(){}};}getClientRects(){return this.hidden?[]:[{}];} focus(){focused=this;}showModal(){this.open=true;}close(){this.open=false;}load(){}
 pause(){this.paused=true;pausedCount++;}async play(){this.paused=false;await this.fire('play');}
}
const nodes=Object.fromEntries([...html.matchAll(/id="([^"]+)"/g)].map(m=>[m[1],new Node()]));const original=new Node('button'),body=new Node();body.style.overflow='auto';
const listeners={};const scope={document:{getElementById:id=>nodes[id]||null,createElement:tag=>new Node(tag),body,get activeElement(){return focused||original;}},window:{addEventListener:(k,f)=>listeners[k]=f},history:{pushState(){pushCount++;},back(){backCount++;listeners.popstate?.();}},location:{replace(){}},fetch:async()=>({status:503,ok:false}),Date,Intl,AbortController,setTimeout,clearTimeout};
vm.runInNewContext(fs.readFileSync(require.resolve('../web/page.js'),'utf8'),scope);
(async()=>{
 await new Promise(r=>setImmediate(r));
 assert(!html.includes('id="queue-coverage"'));assert(!html.includes('id="queue-flags"'));assert(!html.includes('id="public-coverage"'));
 const box=new Node();scope.preview(box,'a'.repeat(64),'https://source/cover.jpg','https://source/video.mp4','instagram',null,'Instagram scheduled');
 const video=box.querySelector('video'),image=box.querySelector('img');assert.equal(video.preload,'metadata');assert.equal(video.controls,false);assert(video.src.endsWith('#t=0.001'));assert(image,'Cover is displayed separately from the video');
 await video.fire('loadedmetadata');await video.fire('loadeddata');assert.equal(video.hidden,false);
 await image.fire('click');assert(nodes['media-viewer'].open);assert.equal(body.style.overflow,'hidden');assert.equal(pushCount,1);assert(nodes['viewer-content'].querySelector('img'));
 nodes['media-viewer'].querySelectorAll=()=>[nodes['viewer-close'],nodes['viewer-prev'],nodes['viewer-next']];
 await nodes['media-viewer'].fire('keydown',{key:'Tab',shiftKey:true,preventDefault(){}});assert.equal(focused,nodes['viewer-next'],'Reverse Tab wraps inside the dialog');
 await nodes['media-viewer'].fire('keydown',{key:'Tab',shiftKey:false,preventDefault(){}});assert.equal(focused,nodes['viewer-close'],'Tab wraps to Close');
 await nodes['viewer-next'].fire('click');const large=nodes['viewer-content'].querySelector('video');assert(large.controls);assert.equal(large.preload,'auto');assert.equal(video.paused,true,'Card never plays behind the viewer');
 await nodes['viewer-content'].querySelector('button').fire('click');assert.equal(large.paused,false);
 await nodes['viewer-prev'].fire('click');assert.equal(large.paused,true);assert.equal(large.src,'','Switch unloads the previous video');
 await nodes['viewer-close'].fire('click');assert(!nodes['media-viewer'].open);assert.equal(body.style.overflow,'auto');assert.equal(focused,original);assert.equal(backCount,1);
 await image.fire('click');listeners.popstate();assert(!nodes['media-viewer'].open,'Browser Back closes the viewer');
 await image.fire('click');await nodes['media-viewer'].fire('cancel',{preventDefault(){}});assert(!nodes['media-viewer'].open,'Escape closes the viewer');assert.equal(body.style.overflow,'auto');
 const tt=new Node();scope.preview(tt,'b'.repeat(64),null,'https://source/tiktok.mp4','tiktok',0,'TikTok');const tv=tt.querySelector('video');await tv.fire('loadeddata');assert.equal(tt.querySelector('canvas').hidden,false);assert(pausedCount>0);
 console.log('media_viewer: separate covers, first-frame preload, full-size playback, switching, Escape, Back, focus and scroll restoration passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
