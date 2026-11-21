const fs=require('fs'),os=require('os'),path=require('path');
const project='/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const ads=require(path.join(project,'scripts/ads/api/client.js'));
async function main(){
const s={...process.env};for(const line of fs.readFileSync(path.join(os.homedir(),'.absbyai-secrets.env'),'utf8').split('\n')){const m=line.match(/^([A-Z0-9_]+)=(.*)$/);if(m&&!s[m[1]])s[m[1]]=m[2].replace(/^"|"$/g,'');}
const tr=await fetch('https://oauth2.googleapis.com/token',{method:'POST',body:new URLSearchParams({client_id:s.GOOGLE_CLIENT_ID,client_secret:s.GOOGLE_CLIENT_SECRET,refresh_token:s.YOUTUBE_REFRESH_TOKEN,grant_type:'refresh_token'})});const tok=await tr.json();if(!tok.access_token)throw Error('YouTube token refresh failed');
async function yt(endpoint,params){const r=await fetch('https://www.googleapis.com/youtube/v3/'+endpoint+'?'+new URLSearchParams(params),{headers:{Authorization:'Bearer '+tok.access_token}});const j=await r.json();if(!r.ok)throw Error(j.error?.message||'YouTube read failed');return j;}
const ch=await yt('channels',{part:'id,contentDetails',mine:'true'});const channel=ch.items.find(x=>x.id==='UC236gjadarHAhEhOMYNGJ9g');if(!channel)throw Error('Expected channel missing');
const pl=await yt('playlistItems',{part:'snippet,contentDetails',playlistId:channel.contentDetails.relatedPlaylists.uploads,maxResults:'50'});
const hits=pl.items.filter(x=>/most guys|ra.?13/i.test(x.snippet.title)).map(x=>({title:x.snippet.title,id:x.contentDetails.videoId,publishedAt:x.snippet.publishedAt}));
const campaign=await ads.search('SELECT campaign.id, campaign.name, campaign.status, campaign_budget.id, campaign_budget.amount_micros FROM campaign WHERE campaign.id = 24316364155');
const groups=await ads.search("SELECT ad_group.id, ad_group.name, ad_group.status FROM ad_group WHERE campaign.id = 24316364155 AND ad_group.status != 'REMOVED'");
const ref=await ads.search('SELECT ad_group.id, ad_group.name, ad_group.target_cpa_micros FROM ad_group WHERE ad_group.id = 199824307366');
const urls=await ads.search("SELECT ad_group.id, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status, ad_group_ad.ad.final_urls FROM ad_group_ad WHERE campaign.id = 24316364155 AND ad_group_ad.status != 'REMOVED'");
const audience=await ads.search("SELECT ad_group_criterion.audience.audience FROM ad_group_criterion WHERE ad_group.id = 206348100928 AND ad_group_criterion.type = 'AUDIENCE' AND ad_group_criterion.status != 'REMOVED'");
const result={at:new Date().toISOString(),channel:channel.id,recentUploadsChecked:pl.items.length,oldestRecentUpload:pl.items.at(-1)?.snippet.publishedAt,matchingYouTubeUploads:hits,campaign,referenceCpa:ref,audience,matchingAdGroups:groups.filter(x=>/ra.?13|most guys/i.test(x.adGroup.name)),campaignUrls:urls};
fs.writeFileSync(path.join(__dirname,'preflight.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify({channel:channel.id,recentUploadsChecked:pl.items.length,matchingYouTubeUploads:hits,matchingAdGroups:result.matchingAdGroups,campaign,referenceCpa:ref,audience,finalUrlHosts:[...new Set(urls.flatMap(x=>x.adGroupAd.ad.finalUrls).map(u=>new URL(u).host))]},null,2));await ads.close();
}
main().catch(async e=>{console.error(e.message);await ads.close();process.exit(1)});
