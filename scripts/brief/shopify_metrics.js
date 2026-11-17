'use strict';
// Aggregate reports from the connected Shopify tools; no customer data or token.
const SHOP='1yar3v-ie.myshopify.com';
function validateReport(r,day,now=Date.now()){
 if(!r||r.schemaVersion!==1||r.shopDomain!==SHOP||r.currency!=='USD'||r.timezone!=='America/Chicago'||r.day!==day||r.testPaymentsExcluded!==true||r.lifetimeComplete!==true)throw Error('Shopify report identity, day or coverage mismatch');
 const at=Date.parse(r.checkedAt),age=now-at;
 if(!Number.isFinite(at)||age<0||age>30*60000)throw Error('Shopify report needs a fresh connected-tool read');
 for(const k of ['yesterdayGrossCollected','lifetimeGrossCollected'])if(!Number.isFinite(r[k])||r[k]<0)throw Error('Invalid Shopify collection total');
 if(r.lifetimeGrossCollected<r.yesterdayGrossCollected)throw Error('Shopify lifetime coverage incomplete');
 return r;
}
function applyReport(metrics,r){
 metrics.supplementRevenue={value:r.yesterdayGrossCollected,source:'SixPackAbs Shopify payments',note:'Successful USD sales/captures after discounts, before fees/refunds. Test orders excluded.'};
 for(const [key,field] of [['revenueYesterday','yesterdayGrossCollected'],['lifetimeRevenue','lifetimeGrossCollected']]){
  const m=metrics[key];
  // Only add to a fresh Stripe-only result. Reapplying never adds Shopify twice.
  if(m?.source==='Stripe live charges'&&Number.isFinite(m.value))metrics[key]={value:Math.round((m.value+r[field])*100)/100,source:'Stripe + Shopify',note:'Successful USD collections before fees/refunds, across app web payments and SixPackAbs. Apple app-store revenue is not included.'};
 }
 return metrics;
}
function reportFromAnalytics(input,day,now=Date.now()){
 const shop=input.shop, daily=input.daily, lifetime=input.lifetime;
 if(!shop||shop.myshopifyDomain!==SHOP||shop.currencyCode!=='USD'||shop.ianaTimezone!=='America/Chicago')throw Error('Wrong Shopify store/currency/timezone');
 const localDay=value=>new Intl.DateTimeFormat('en-CA',{timeZone:'America/Chicago',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(value));
 const firstDay=localDay(shop.createdAt),today=localDay(now);
 function amount(report,from,through){
  const query=`FROM payments SHOW gross_payments SINCE ${from} UNTIL ${through}`;
  if(report?.shopDomain!==SHOP||report.currencyCode!=='USD'||report.query!==query||report.rowCount!==1||report.rows?.length!==1)throw Error('Shopify payment report range/coverage mismatch');
  const i=report.columns.findIndex(c=>c.name==='gross_payments');if(i<0)throw Error('Payment column missing');
  const value=Number(report.rows[0][i]);if(!Number.isFinite(value)||value<0)throw Error('Invalid payment value');return value;
 }
 return validateReport({schemaVersion:1,shopDomain:SHOP,currency:'USD',timezone:'America/Chicago',day,checkedAt:input.checkedAt,
  yesterdayGrossCollected:amount(daily,day,day),lifetimeGrossCollected:amount(lifetime,firstDay,today),testPaymentsExcluded:true,lifetimeComplete:true,
  coverageFrom:shop.createdAt,source:'Connected Shopify Analytics gross_payments; test transactions excluded by Shopify payment reports'},day,now);
}
module.exports={validateReport,applyReport,reportFromAnalytics,SHOP};
if(require.main===module){
 try{
  const fs=require('fs'),path=require('path'),[inputFile,outputFile]=process.argv.slice(2);
  if(!inputFile||!outputFile)throw Error('Usage: shopify_metrics.js <private connected-tool reports.json> <private shopify-report.json>');
  for(const file of [inputFile,outputFile])for(let p=path.dirname(path.resolve(file));;p=path.dirname(p)){if(fs.existsSync(path.join(p,'.git')))throw Error('Reports must stay outside Git');if(p===path.dirname(p))break;}
  const now=new Date(),day=require('./business_metrics').windowFor(now).day;
  const result=reportFromAnalytics(JSON.parse(fs.readFileSync(inputFile,'utf8')),day,now.getTime());
  fs.writeFileSync(outputFile+'.tmp',JSON.stringify(result,null,2),{mode:0o600});fs.renameSync(outputFile+'.tmp',outputFile);
  console.log(JSON.stringify({day:result.day,shop:result.shopDomain,recorded:true}));
 }catch(e){console.error(e.message);process.exitCode=1;}
}
