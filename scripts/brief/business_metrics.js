'use strict';
// Read-only daily totals. Credentials and customer records never leave this process.
const fs=require('fs'),path=require('path'),os=require('os');
const KEYS=['newSignups','revenueYesterday','activeMembers','lifetimeRevenue','adSpendOverall','adSpendEngagement','adSpendTrials','visitorsAbs','visitorsSixpack','supplementRevenue','youtubeSubscribers','youtubeViews','latestLongViews','latestShortViews','instagramFollowers'];
function settings(){const s={...process.env};for(const line of fs.readFileSync(path.join(os.homedir(),'.absbyai-secrets.env'),'utf8').split('\n')){const m=line.match(/^([A-Z0-9_]+)=(.*)$/);if(m&&!s[m[1]])s[m[1]]=m[2].trim().replace(/^(['"])(.*)\1$/,'$2');}return s;}
async function json(url,options={}){const r=await fetch(url,{...options,signal:AbortSignal.timeout(25000)});if(!r.ok)throw Error('Source HTTP '+r.status);return r.json();}
function windowFor(now=new Date()){
 const today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Chicago',year:'numeric',month:'2-digit',day:'2-digit'}).format(now);
 const previous=new Date(today+'T12:00:00Z');previous.setUTCDate(previous.getUTCDate()-1);const day=previous.toISOString().slice(0,10);
 function midnight(d){const probe=new Date(d+'T00:00:00Z');const local=new Intl.DateTimeFormat('en-US',{timeZone:'America/Chicago',timeZoneName:'longOffset'}).formatToParts(probe).find(p=>p.type==='timeZoneName').value.replace('GMT','');return new Date(d+'T00:00:00'+local);}
 return {day,from:midnight(day),to:midnight(today)};
}
async function collect(now=new Date(),s=settings()){
 const w=windowFor(now),checkedAt=now.toISOString(),metrics=Object.fromEntries(KEYS.map(k=>[k,{value:null,source:'Unavailable',note:'Source not connected or not yet reported.'}]));
 const set=(key,value,source,note='')=>{if(!Number.isFinite(value)||value<0)throw Error('Invalid metric');metrics[key]={value,source,note};};
 const errors=[];
 async function task(name,fn){try{await fn();}catch(e){
  errors.push(name+': '+e.message);
  const affected={'Supplement revenue':['supplementRevenue'],'YouTube daily':['youtubeSubscribers','youtubeViews'],'Instagram':['instagramFollowers'],'Accounts':['newSignups','activeMembers'],'Revenue':['revenueYesterday','lifetimeRevenue'],'Visitors':['visitorsAbs','visitorsSixpack'],'Ads':['adSpendOverall','adSpendEngagement','adSpendTrials'],'YouTube':['latestLongViews','latestShortViews']}[name]||[];
  for(const key of affected)if(metrics[key].value===null)metrics[key].note=name+': '+e.message;
 }}
 await Promise.all([
 task('Accounts',async()=>{
  const {Client}=require('pg'),client=new Client({connectionString:s.DATABASE_PUBLIC_URL||s.DATABASE_URL,ssl:{rejectUnauthorized:false},connectionTimeoutMillis:10000});
  try{await client.connect();await client.query('BEGIN READ ONLY');await client.query("SET LOCAL statement_timeout='10s'");
   const r=(await client.query(`SELECT count(*) FILTER(WHERE created_at >= $1 AND created_at < $2) AS signups,
    count(*) FILTER(WHERE membership_status IN ('active','trialing') OR (membership_status='canceled' AND membership_period_end > $3)) AS members
    FROM users WHERE lower(email) NOT LIKE '%@example.com' AND lower(email) NOT LIKE '%@test.com'
    AND NOT (lower(email)=ANY($4::text[]))`,[w.from,w.to,now,(s.ADMIN_EMAILS||'').toLowerCase().split(',').map(x=>x.trim())])).rows[0];
   set('newSignups',Number(r.signups),'Account database','New accounts; excludes admin and example/test domains.');
   set('activeMembers',Number(r.members),'Membership database','Paid members, live trials and canceled members with remaining access; excludes complimentary accounts.');
  }finally{await client.query('ROLLBACK').catch(()=>{});await client.end();}
 }),
 task('Revenue',async()=>{
  if(!s.STRIPE_SECRET_KEY?.startsWith('sk_live_'))throw Error('Live Stripe credential unavailable');
  const stripe=require('stripe')(s.STRIPE_SECRET_KEY,{timeout:25000,maxNetworkRetries:1});let yesterday=0,lifetime=0,nonUSD=false;
  for await(const c of stripe.charges.list({limit:100})){if(c.paid&&c.status==='succeeded'){if(c.currency!=='usd'){nonUSD=true;continue;}lifetime+=c.amount;if(c.created>=w.from/1000&&c.created<w.to/1000)yesterday+=c.amount;}}
  if(nonUSD)throw Error('Multiple currencies require verified conversion');
  set('revenueYesterday',yesterday/100,'Stripe live charges','Gross successful USD collections before fees/refunds. Stripe only; other payment channels not included.');
  set('lifetimeRevenue',lifetime/100,'Stripe live charges','Gross successful USD collections before fees/refunds. Stripe only; other payment channels not included.');
 }),
 task('Visitors',async()=>{
  const host='lower(coalesce(properties.$host, domain(properties.$current_url)))';
  const query=`SELECT if(${host} IN ('absbyai.com','www.absbyai.com'),'absbyai.com','sixpackabs.com') AS site, uniq(person_id) FROM events WHERE event='$pageview' AND timestamp >= '${w.from.toISOString()}' AND timestamp < '${w.to.toISOString()}' AND ${host} IN ('absbyai.com','www.absbyai.com','sixpackabs.com','www.sixpackabs.com') GROUP BY site`;
  const r=await json('https://us.posthog.com/api/projects/'+(s.POSTHOG_PROJECT_ID||'458833')+'/query',{method:'POST',headers:{Authorization:'Bearer '+(s.POSTHOG_PERSONAL_KEY||s.POSTHOG_API_KEY),'Content-Type':'application/json'},body:JSON.stringify({query:{kind:'HogQLQuery',query}})});
  for(const [site,key] of [['absbyai.com','visitorsAbs'],['sixpackabs.com','visitorsSixpack']])set(key,Number(r.results.find(r=>r[0]===site)?.[1]||0),'PostHog','Unique tracked visitors yesterday; www combined.');
 }),
 task('Ads',async()=>{
  const ads=require('../ads/api/client');
  const account=await ads.search('SELECT customer.time_zone, customer.currency_code FROM customer LIMIT 1');
  if(account[0]?.customer.timeZone!=='America/Chicago'||account[0]?.customer.currencyCode!=='USD')throw Error('Account day/currency mismatch');
  const rows=await ads.search(`SELECT campaign.name, metrics.cost_micros FROM campaign WHERE segments.date = '${w.day}'`);
  let overall=0,engagement=0,trials=0;for(const r of rows){const amount=Number(r.metrics.costMicros||0)/1e6;overall+=amount;if(/^\[ENGAGEMENT\]/i.test(r.campaign.name))engagement+=amount;if(/^\[TRIAL\]/i.test(r.campaign.name))trials+=amount;}
  const token=s.META_ADS_TOKEN||s.FACEBOOK_PAGE_ACCESS_TOKEN;if(!token)throw Error('Meta spend unavailable; overall cannot be verified');
  const url=new URL('https://graph.facebook.com/v25.0/act_2143998876461525/insights');url.search=new URLSearchParams({fields:'spend',time_range:JSON.stringify({since:w.day,until:w.day}),level:'account',access_token:token});
  const meta=await json(url);const metaSpend=(meta.data||[]).reduce((n,r)=>n+Number(r.spend),0);
  set('adSpendOverall',Math.round((overall+metaSpend)*100)/100,'Google Ads + Meta','All Google campaigns plus Meta account spend.');
  const campaigns=new URL('https://graph.facebook.com/v25.0/act_2143998876461525/insights');campaigns.search=new URLSearchParams({fields:'spend,campaign_name',time_range:JSON.stringify({since:w.day,until:w.day}),level:'campaign',limit:'500',access_token:token});
  const split=await json(campaigns);let unclassified=false;for(const r of split.data||[]){if(/engagement|boost|follower/i.test(r.campaign_name))engagement+=Number(r.spend);else if(/trial/i.test(r.campaign_name))trials+=Number(r.spend);else if(Number(r.spend)>0)unclassified=true;}
  if(split.paging?.next)throw Error('Meta campaign pagination incomplete');
  set('adSpendEngagement',Math.round(engagement*100)/100,'Google Ads + Meta',unclassified?'Named engagement campaigns; some Meta spend is unclassified.':'Engagement campaigns across Google and Meta.');
  set('adSpendTrials',Math.round(trials*100)/100,'Google Ads + Meta',unclassified?'Named trial campaigns; some Meta spend is unclassified.':'Trial campaigns across Google and Meta.');
 }),
 task('YouTube',async()=>{
  const token=await json('https://oauth2.googleapis.com/token',{method:'POST',body:new URLSearchParams({client_id:s.GOOGLE_CLIENT_ID,client_secret:s.GOOGLE_CLIENT_SECRET,refresh_token:s.YOUTUBE_REFRESH_TOKEN,grant_type:'refresh_token'})});
  const headers={Authorization:'Bearer '+token.access_token};
  const url=new URL('https://youtubeanalytics.googleapis.com/v2/reports');url.search=new URLSearchParams({ids:'channel==MINE',startDate:w.day,endDate:w.day,metrics:'views,subscribersGained',dimensions:'day'});
  await task('YouTube daily',async()=>{const r=await json(url,{headers});const row=r.rows?.find(r=>r[0]===w.day);if(!row)throw Error('Yesterday not reported yet');set('youtubeViews',Number(row[1]),'YouTube Analytics','YouTube reporting day (Pacific time); may arrive late.');set('youtubeSubscribers',Number(row[2]),'YouTube Analytics','Gross subscribers gained, not net change; YouTube reporting day (Pacific time).');});
  const channel=await json('https://www.googleapis.com/youtube/v3/channels?part=contentDetails&mine=true',{headers});
  if(channel.items?.[0]?.id!==require('./native_youtube').CHANNEL)throw Error('Wrong channel');
  let cursor,found={};
  do{const u=new URL('https://www.googleapis.com/youtube/v3/playlistItems');u.search=new URLSearchParams({part:'contentDetails',playlistId:channel.items[0].contentDetails.relatedPlaylists.uploads,maxResults:'50',...(cursor?{pageToken:cursor}:{})});const page=await json(u,{headers});
   const ids=page.items.map(i=>i.contentDetails.videoId);if(!ids.length)break;
   const videos=await json('https://www.googleapis.com/youtube/v3/videos?part=snippet,status,contentDetails,statistics&id='+ids.join(','),{headers});
   // contentDetails duration alone cannot distinguish landscape <=3m from Shorts.
   // Verify the public Shorts redirect for each short candidate instead of guessing.
   for(const v of videos.items.filter(v=>v.status.privacyStatus==='public').sort((a,b)=>b.snippet.publishedAt.localeCompare(a.snippet.publishedAt))){
    const m=v.contentDetails.duration.match(/^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$/);if(!m)continue;const duration=Number(m[1]||0)*3600+Number(m[2]||0)*60+Number(m[3]||0);
    let short=false;if(duration<=180){const response=await fetch('https://www.youtube.com/shorts/'+v.id,{method:'HEAD',redirect:'follow',signal:AbortSignal.timeout(12000)});if(!response.ok)continue;short=new URL(response.url).pathname.startsWith('/shorts/');}
    const key=short?'latestShortViews':'latestLongViews';if(!found[key]){set(key,Number(v.statistics.viewCount),'YouTube Data API',v.snippet.title+' · Lifetime views, checked now.');found[key]=true;}
    if(found.latestShortViews&&found.latestLongViews)break;
   }cursor=page.nextPageToken;
  }while(cursor&&(!found.latestShortViews||!found.latestLongViews));
 }),
 task('Instagram',async()=>{
  const url=new URL('https://graph.facebook.com/v25.0/17841401601139982/insights');url.search=new URLSearchParams({metric:'follower_count',period:'day',since:String(Math.floor(w.from/1000)-86400),until:String(Math.floor(w.to/1000)+86400),access_token:s.META_ADS_TOKEN||s.FACEBOOK_PAGE_ACCESS_TOKEN});
  const r=await json(url);const values=r.data?.find(r=>r.name==='follower_count')?.values;
  const row=values?.find(r=>new Date(Date.parse(r.end_time)-86400000).toISOString().slice(0,10)===w.day);
  if(!row)throw Error('Yesterday not reported yet');set('instagramFollowers',Number(row.value),'Instagram Insights','New followers, not net change; Instagram reporting day.');
 }),
 task('Supplement revenue',async()=>{
  if(!s.SHOPIFY_ADMIN_ACCESS_TOKEN)throw Error('Shopify orders read access not connected');
  const url='https://1yar3v-ie.myshopify.com/admin/api/2026-10/graphql.json';
  const query=`query($after:String){orders(first:100,after:$after,query:"updated_at:>=${w.day}"){nodes{test transactions{kind status processedAt amountSet{shopMoney{amount currencyCode}}}}pageInfo{hasNextPage endCursor}}}`;
  let after=null,total=0;
  do{const r=await json(url,{method:'POST',headers:{'X-Shopify-Access-Token':s.SHOPIFY_ADMIN_ACCESS_TOKEN,'Content-Type':'application/json'},body:JSON.stringify({query,variables:{after}})});
   if(r.errors||!r.data?.orders)throw Error('Shopify orders report unavailable');
   for(const o of r.data.orders.nodes)if(!o.test)for(const t of o.transactions)if(['SALE','CAPTURE'].includes(t.kind)&&t.status==='SUCCESS'&&Date.parse(t.processedAt)>=w.from&&Date.parse(t.processedAt)<w.to){if(t.amountSet.shopMoney.currencyCode!=='USD')throw Error('Store currency is not USD');total+=Number(t.amountSet.shopMoney.amount);}
   after=r.data.orders.pageInfo.hasNextPage?r.data.orders.pageInfo.endCursor:null;
  }while(after);
  set('supplementRevenue',Math.round(total*100)/100,'SixPackAbs Shopify','Successful non-test sale/capture transactions; USD gross collections.');
 })
 ]);
 return {day:w.day,checkedAt,metrics,note:'Daily visitor, signup and Ads windows use Central time. Platform exceptions are stated beside the metric. Revenue currently covers Stripe only; supplement and app-store collections are not consolidated.',limitations:errors};
}
module.exports={collect,KEYS,windowFor};
if(require.main===module)collect().then(r=>process.stdout.write(JSON.stringify(r))).catch(()=>{console.error('Business totals unavailable');process.exitCode=1;});
