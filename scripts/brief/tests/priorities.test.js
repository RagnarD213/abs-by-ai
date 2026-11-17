'use strict';
const assert=require('node:assert/strict');
const {createStore}=require('../web/store');
const board={lists:[{id:'p',role:'planned'},{id:'i',role:'progress'},{id:'d',role:'completed'},{id:'old',role:'planned',archived:true}],cards:[{listId:'p',title:'Top',plannedFor:'2026-11-17'},{listId:'p',title:'Second',plannedFor:'2026-11-17'},{listId:'p',title:'Yesterday',plannedFor:'2026-11-16'},{listId:'p',title:'Removed',archived:true},{listId:'d',title:'Done'},{listId:'i',title:'In progress'},{listId:'old',title:'Legacy'}]};
const pool={query:async(sql)=>({rows:sql.includes('SELECT document FROM workboard_state')?[{document:board}]:[]})};
(async()=>{const r=await createStore(pool).readPriorities('2026-11-17');assert.deepEqual(r.rows.map(r=>r.title),['Top','Second','In progress']);board.cards.splice(0,2,board.cards[1],board.cards[0]);assert.equal((await createStore(pool).readPriorities('2026-11-17')).rows[0].title,'Second');console.log('priorities: live board ordering, date filter, completed/archived exclusion and reorder passed');})().catch(e=>{console.error(e);process.exitCode=1;});
