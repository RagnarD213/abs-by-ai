'use strict';
// Private read-only snapshot. Tokens stay in memory and never enter the output.
const fs = require('fs'), os = require('os'), path = require('path');
const CHANNEL = 'UC236gjadarHAhEhOMYNGJ9g';
async function collect(fetcher = fetch, settings, extraIds = []) {
  const s = settings || {...process.env};
  if (!settings) for (const line of fs.readFileSync(path.join(os.homedir(), '.absbyai-secrets.env'),'utf8').split('\n')) {
    const m=line.match(/^([A-Z0-9_]+)=(.*)$/); if(m&&!s[m[1]])s[m[1]]=m[2].trim().replace(/^(['"])(.*)\1$/,'$2');
  }
  const tokenResponse = await fetcher('https://oauth2.googleapis.com/token',{method:'POST',signal:AbortSignal.timeout(15000),body:new URLSearchParams({client_id:s.GOOGLE_CLIENT_ID,client_secret:s.GOOGLE_CLIENT_SECRET,refresh_token:s.YOUTUBE_REFRESH_TOKEN,grant_type:'refresh_token'})});
  const token = await tokenResponse.json();
  if(!tokenResponse.ok||!token.access_token)throw new Error('YouTube existing credential refresh HTTP '+tokenResponse.status);
  async function get(resource,params) {
    const url=new URL('https://www.googleapis.com/youtube/v3/'+resource);url.search=new URLSearchParams(params);
    const response=await fetcher(url,{headers:{Authorization:'Bearer '+token.access_token},signal:AbortSignal.timeout(15000)});
    if(!response.ok)throw new Error('YouTube '+resource+' HTTP '+response.status);
    return response.json();
  }
  const channels=await get('channels',{part:'id,snippet,contentDetails',mine:'true'});
  if(channels.items?.length!==1||channels.items[0].id!==CHANNEL)throw new Error('YouTube channel identity does not match the approved channel');
  const channel=channels.items[0], ids=[], seen=new Set();let cursor;
  do {
    const page=await get('playlistItems',{part:'contentDetails',playlistId:channel.contentDetails.relatedPlaylists.uploads,maxResults:'50',...(cursor?{pageToken:cursor}:{})});
    ids.push(...page.items.map(i=>i.contentDetails.videoId));cursor=page.nextPageToken;
    if(cursor&&seen.has(cursor))throw new Error('Repeated YouTube uploads cursor');if(cursor)seen.add(cursor);
  } while(cursor);
  const requested=[...new Set([...ids,...extraIds.filter(id=>/^[A-Za-z0-9_-]{11}$/.test(id))])],videos=[];
  for(let i=0;i<requested.length;i+=50){const page=await get('videos',{part:'snippet,status,contentDetails',id:requested.slice(i,i+50).join(',')});videos.push(...page.items);}
  const publicChecks=Object.fromEntries(extraIds.map(id=>{const v=videos.find(v=>v.id===id);return [id,!v?'missing':v.snippet.channelId!==CHANNEL?'wrong_channel':v.status.privacyStatus];}));
  return {status:'ok',checkedAt:new Date().toISOString(),channel:{id:channel.id,title:channel.snippet.title},uploadsEnumerated:ids.length,uniqueUploads:new Set(ids).size,publicChecks,videos:videos.filter(v=>v.snippet?.channelId===CHANNEL)};
}
if(require.main===module)collect(fetch,undefined,JSON.parse(fs.readFileSync(0,'utf8')||'[]')).then(result=>process.stdout.write(JSON.stringify(result))).catch(error=>{process.stdout.write(JSON.stringify({status:'error',checkedAt:new Date().toISOString(),reason:error.message}));process.exitCode=1;});
module.exports={collect,CHANNEL};
