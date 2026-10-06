'use strict';
const {initial,mutate,BoardError}=require('./model');
function createStore(pool,ready=Promise.resolve()) {
  let initialized;
  async function init() {
    if(!pool)throw new Error('Database unavailable');
    if(!initialized)initialized=Promise.resolve(ready).then(async()=>{
      await pool.query('CREATE TABLE IF NOT EXISTS workboard_state (id INTEGER PRIMARY KEY CHECK (id = 1), version INTEGER NOT NULL, document JSONB NOT NULL)');
      await pool.query('CREATE TABLE IF NOT EXISTS workboard_files (id TEXT PRIMARY KEY, bytes BYTEA NOT NULL)');
      await pool.query('INSERT INTO workboard_state (id, version, document) VALUES (1, 0, $1) ON CONFLICT (id) DO NOTHING',[JSON.stringify(initial())]);
    }).catch(e=>{initialized=null;throw e;});
    await initialized;
  }
  return {
    async read(){await init();const r=(await pool.query('SELECT version, document FROM workboard_state WHERE id = 1')).rows[0];return {version:r.version,...r.document};},
    async change(version,action,payload,file){
      if(!Number.isInteger(version)||version<0)throw new BoardError('A current board version is required.');
      await init();const client=await pool.connect();
      try {
        await client.query('BEGIN');
        const row=(await client.query('SELECT version, document FROM workboard_state WHERE id = 1 FOR UPDATE')).rows[0];
        if(row.version!==version)throw new BoardError('The board changed in another tab. Your draft is kept. Reload the latest board before saving again.',409);
        const result=mutate(row.document,action,payload,file);
        const updated=await client.query('UPDATE workboard_state SET version = version + 1, document = $1 WHERE id = 1 AND version = $2 RETURNING version',[JSON.stringify(result.board),version]);
        if(!updated.rows.length)throw new BoardError('The board changed. Reload before saving again.',409);
        if(file)await client.query('INSERT INTO workboard_files (id, bytes) VALUES ($1, $2)',[file.id,file.bytes]);
        if(result.removedFile)await client.query('DELETE FROM workboard_files WHERE id = $1',[result.removedFile]);
        await client.query('COMMIT');return {version:updated.rows[0].version,...result.board,target:result.target};
      } catch(e){await client.query('ROLLBACK');throw e;} finally{client.release();}
    },
    async file(id){await init();const board=await this.read();const meta=board.cards.flatMap(c=>c.attachments).find(a=>a.id===id);if(!meta)return null;const row=(await pool.query('SELECT bytes FROM workboard_files WHERE id = $1',[id])).rows[0];return row?{...meta,bytes:row.bytes}:null;}
  };
}
module.exports={createStore};
