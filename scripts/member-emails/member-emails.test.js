#!/usr/bin/env node
'use strict';
const assert = require('node:assert/strict');
const { newDb } = require('pg-mem');
const { createMemberEmails } = require('../../member-emails');

(async () => {
  const memory = newDb();
  const { Pool } = memory.adapters.createPg();
  const db = new Pool();
  await db.query(`CREATE TABLE users(id integer primary key,email text,membership_status text,membership_period_end timestamptz);
    CREATE TABLE programs(id integer primary key,user_id integer);
    CREATE TABLE member_email_enrollments(user_id integer primary key,payment_reference text,started_at timestamptz default now(),next_at timestamptz,step integer default 0,opted_out boolean default false);
    CREATE TABLE member_email_deliveries(send_key text primary key,user_id integer,payload jsonb,first_attempt_at timestamptz,lease_until timestamptz,sent_at timestamptz,provider_id text,blocked boolean default false,last_error text);`);
  let current = new Date('2026-11-14T20:00:00Z');
  const calls = []; let fail = false;
  const options = { db, apiKey:'test', from:'team@example.test', replyTo:'help@example.test',
    siteUrl:'https://absbyai.com', secret:'test-secret', address:'Business address', now:()=>current,
    optedOut:email=>email==='optedout@fixture.test',
    fetch:async (url, options)=>{ calls.push(options); if(fail) return {ok:false,status:429,text:async()=>'rate limited'};
      return {ok:true,json:async()=>({id:'provider-'+calls.length})}; } };
  const service = createMemberEmails({ ...options, followupsEnabled:true });
  const add = (id,email,status='active',end=null)=>db.query('INSERT INTO users VALUES($1,$2,$3,$4)',[id,email,status,end]);
  await add(1,'member@fixture.test');
  await add(2,'trial@fixture.test','trialing');
  await add(3,'pastdue@fixture.test','past_due');
  await add(4,'test@example.com');
  await add(5,'optedout@fixture.test');
  await add(6,'expired@fixture.test','active',new Date('2026-11-01'));
  await add(7,'unpaid@fixture.test'); // no confirmed payment enrollment
  for(let id=1;id<=6;id++) await service.enroll(id,'paid:'+id);
  await service.enroll(1,'duplicate-paid-webhook');
  assert.equal((await db.query('SELECT * FROM member_email_enrollments WHERE user_id=1')).rows.length,1);
  await Promise.all([service.sweep(),service.sweep()]);
  assert.equal(calls.length,1,'concurrent sweeps deliver once; trials, past due, expired, test, opted-out and unconfirmed users excluded');
  assert.equal(JSON.parse(calls[0].body).subject,'Getting started with your Abs By AI membership');
  assert.equal(calls[0].headers['Idempotency-Key'],'member-checkin/1/0');
  await service.sweep(); assert.equal(calls.length,1,'no repeat before next due time');
  current = new Date(current.getTime()+2*86400000);
  await createMemberEmails(options).sweep();
  assert.equal(calls.length,1,'default welcome-only mode suppresses all follow-ups');
  await db.query('INSERT INTO programs VALUES(1,1)');
  fail=true; await service.sweep(); assert.equal(calls.length,2);
  assert.equal((await db.query('SELECT step FROM member_email_enrollments WHERE user_id=1')).rows[0].step,1,'failed send does not advance');
  // After a transient failure the retry must have exactly the same request.
  current=new Date(current.getTime()+6*60000); fail=false;
  await service.sweep(); assert.equal(calls.length,3);
  assert.equal(calls[1].body,calls[2].body);
  assert.equal(calls[1].headers['Idempotency-Key'],calls[2].headers['Idempotency-Key']);
  assert.equal(JSON.parse(calls[2].body).subject,'Your next workout in Abs By AI');
  assert.equal(await service.unsubscribe(1,'wrong'),false);
  const url=new URL(service.unsubscribeUrl(1));
  assert.equal(await service.unsubscribe('1',url.searchParams.get('token')),true);
  current=new Date(current.getTime()+8*86400000); await service.sweep(); assert.equal(calls.length,3,'unsubscribe stops check-ins');
  // A crash after acceptance and before sequence advance is recovered without
  // resending a message already marked sent.
  await add(8,'recovery@fixture.test'); await service.enroll(8,'paid:8');
  await db.query(`INSERT INTO member_email_deliveries(send_key,user_id,payload,sent_at) VALUES('member-checkin/8/0',8,'{}',$1)`,[current]);
  await service.sweep(); assert.equal(calls.length,3);
  assert.equal((await db.query('SELECT step FROM member_email_enrollments WHERE user_id=8')).rows[0].step,1);
  // An uncertain old attempt cannot be blindly resent outside provider dedupe.
  await add(9,'uncertain@fixture.test'); await service.enroll(9,'paid:9');
  await db.query(`INSERT INTO member_email_deliveries(send_key,user_id,payload,first_attempt_at) VALUES('member-checkin/9/0',9,'{}',$1)`,[new Date(current.getTime()-25*3600000)]);
  await service.sweep(); assert.equal(calls.length,3);
  assert.equal((await db.query("SELECT blocked FROM member_email_deliveries WHERE send_key='member-checkin/9/0'")).rows[0].blocked,true);
  await db.end(); console.log('Member email tests passed: enrollment, eligibility, concurrency, delays, retry, opt-out and crash recovery.');
})().catch(error=>{console.error(error);process.exitCode=1;});
