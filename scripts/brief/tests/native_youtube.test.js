'use strict';
const assert=require('node:assert/strict'),{collect,CHANNEL}=require('../native_youtube'),{mediaURL}=require('../web/social');
(async()=>{
 let calls=[];
 const mock=async(url,options)=>{
  calls.push({url:String(url),method:options.method||'GET'});
  let data;
  if(String(url).includes('oauth2'))data={access_token:'never-output-this-token'};
  else if(String(url).includes('/channels?'))data={items:[{id:CHANNEL,snippet:{title:'Dan Rose Fitness'},contentDetails:{relatedPlaylists:{uploads:'uploads'}}}]};
  else if(String(url).includes('/playlistItems?'))data=new URL(url).searchParams.has('pageToken')?{items:[{contentDetails:{videoId:'second'}}]}:{items:[{contentDetails:{videoId:'first'}}],nextPageToken:'next'};
  else data={items:[{id:'first',snippet:{channelId:CHANNEL},status:{privacyStatus:'private',publishAt:'2026-10-13T22:00:00Z'}}]};
  return {ok:true,status:200,json:async()=>data};
 };
 const settings={GOOGLE_CLIENT_ID:'id',GOOGLE_CLIENT_SECRET:'secret',YOUTUBE_REFRESH_TOKEN:'refresh'};
 const result=await collect(mock,settings);assert.equal(result.uploadsEnumerated,2);assert.equal(result.channel.id,CHANNEL);assert(!JSON.stringify(result).includes('never-output'));
 assert(calls.every(c=>c.method==='GET'||c.url==='https://oauth2.googleapis.com/token'));
 await assert.rejects(collect(async(url,options)=>String(url).includes('oauth2')?mock(url,options):{ok:true,status:200,json:async()=>({items:[{id:'wrong'}]})},settings),/identity/);
 assert(mediaURL('https://i9.ytimg.com/vi/D9v9POAKe_Q/maxresdefault.jpg?sqp=x&rs=y'));
 assert.equal(mediaURL('https://i9.ytimg.com/vi/D9v9POAKe_Q/maxresdefault.jpg?redirect=http://127.0.0.1'),null);
 assert.equal(mediaURL('https://i9.ytimg.com.evil/vi/D9v9POAKe_Q/maxresdefault.jpg'),null);
 console.log('native_youtube: channel pin, pagination, token privacy, GET-only video reads and exact signed-thumbnail provider guard passed');
})().catch(e=>{console.error(e);process.exitCode=1;});
