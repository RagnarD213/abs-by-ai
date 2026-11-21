'use strict';
const assert=require('node:assert/strict');
const {windowFor,KEYS}=require('../business_metrics');
for(const [now,hours] of [['2026-11-02T15:00:00Z',25],['2026-03-09T15:00:00Z',23],['2026-11-17T15:00:00Z',24]]){
 const w=windowFor(new Date(now));assert.equal((w.to-w.from)/3600000,hours);
}
const {validate}=require('../web/document');
const base={schemaVersion:1,forDate:'2026-11-17',generatedAt:'2026-11-17T14:00:00Z',timezone:'America/Chicago',editionType:'daily',routineEnabled:false,focus:{status:'missing',task:'',why:'',source:'Dashboard'},business:{day:'2026-11-16',checkedAt:'2026-11-17T14:00:00Z',metrics:{newSignups:{value:0,source:'Accounts'},revenueYesterday:{value:null,source:'Unavailable'}}}};
const result=validate(base,Date.parse('2026-11-17T15:00:00Z'));assert.equal(Object.keys(result.business.metrics).length,KEYS.length);assert.equal(result.business.metrics.newSignups.value,0);assert.equal(result.business.metrics.revenueYesterday.value,null);
assert.throws(()=>validate({...base,business:{...base.business,metrics:{newSignups:{value:-1}}}},Date.parse('2026-11-17T15:00:00Z')));
console.log('business_metrics: DST-aware full Central days, explicit unknowns, true zero, invalid negative counts passed');
