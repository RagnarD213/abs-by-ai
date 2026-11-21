'use strict';
// Original bytes and provenance remain in the private database, never public assets.
const crypto = require('crypto');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const metadata = row => ({sha256:row.sha256, forDate:row.for_date, mime:row.mime,
  sizeBytes:row.size_bytes, publishedAt:row.published_at, favoritedAt:row.favorited_at,
  active:row.active, updatedAt:row.updated_at});
const columns = 'sha256,for_date,mime,size_bytes,published_at,favorited_at,active,updated_at';
class FavoriteConflict extends Error {}
function createFavoritesStore(pool, init) {
  async function transaction(work) {
    await init(); const client = await pool.connect();
    try { await client.query('BEGIN'); const result=await work(client); await client.query('COMMIT'); return result; }
    catch(error) { await client.query('ROLLBACK'); throw error; }
    finally { client.release(); }
  }
  return {
    async favoriteImage(sha256, forDate, now) {
      return transaction(async client => {
        // Lock the displayed source before reading provenance. Concurrent publication
        // can cause a safe 409, but can never silently save different bytes/date.
        const image=(await client.query('SELECT mime,bytes FROM brief_image WHERE id=1 FOR SHARE')).rows[0];
        const document=(await client.query('SELECT document FROM brief_document WHERE id=1 FOR SHARE')).rows[0]?.document;
        const existing=(await client.query(`SELECT ${columns} FROM brief_favorites WHERE sha256=$1`,[sha256])).rows[0];
        if(existing) {
          if(existing.for_date!==forDate) throw new FavoriteConflict();
          if(!existing.active) await client.query('UPDATE brief_favorites SET active=true,updated_at=$2 WHERE sha256=$1',[sha256,new Date(now)]);
        } else {
          const source=document?.image;
          if(!image || !source || !document.imageAvailable || source.sha256!==sha256 || source.forDate!==forDate ||
              source.mime!==image.mime || source.sizeBytes!==image.bytes.length || hash(image.bytes)!==sha256) throw new FavoriteConflict();
          await client.query(`INSERT INTO brief_favorites (sha256,for_date,mime,bytes,size_bytes,published_at,favorited_at,active,updated_at)
            VALUES ($1,$2,$3,$4,$5,$6,$7,true,$7) ON CONFLICT (sha256) DO NOTHING`,
          [sha256,source.forDate,image.mime,image.bytes,image.bytes.length,source.publishedAt,new Date(now)]);
          // A concurrent first save and remove is serialized by this row update.
          await client.query('UPDATE brief_favorites SET active=true WHERE sha256=$1',[sha256]);
        }
        return metadata((await client.query(`SELECT ${columns} FROM brief_favorites WHERE sha256=$1`,[sha256])).rows[0]);
      });
    },
    async setFavorite(sha256,active,now) {
      await init();
      const row=(await pool.query(`UPDATE brief_favorites SET active=$2,updated_at=$3 WHERE sha256=$1 AND active<>$2 RETURNING ${columns}`,[sha256,active,new Date(now)])).rows[0];
      return row ? metadata(row) : this.favorite(sha256);
    },
    async favorite(sha256) { await init(); const row=(await pool.query(`SELECT ${columns} FROM brief_favorites WHERE sha256=$1`,[sha256])).rows[0]; return row ? metadata(row) : null; },
    async favoriteBytes(sha256) { await init(); return (await pool.query('SELECT mime,bytes FROM brief_favorites WHERE sha256=$1',[sha256])).rows[0] || null; },
    async listFavorites(after='') {
      await init(); const rows=(await pool.query(`SELECT ${columns} FROM brief_favorites WHERE sha256>$1 ORDER BY sha256 LIMIT 25`,[after])).rows;
      return {rows:rows.slice(0,24).map(metadata),next:rows.length>24 ? rows[23].sha256 : null};
    },
    async favoriteManifest() {
      await init(); const rows=(await pool.query(`SELECT ${columns} FROM brief_favorites WHERE active=true ORDER BY sha256`)).rows.map(metadata);
      const version=hash(JSON.stringify(rows));
      const receipt=(await pool.query('SELECT receipt FROM brief_wallpaper_sync WHERE id=1')).rows[0]?.receipt || null;
      return {version,rows,receipt,feedbackPolicy:'Active favorites are positive feedback. Unselected and removed images are neutral.'};
    },
  };
}
function wallpaperStatus(manifest,now) {
  const r=manifest.receipt;
  if(!r) return {state:'pending_setup',message:'Saved privately. Waiting for Mac wallpaper setup.'};
  if(!Number.isFinite(Date.parse(r.checkedAt)) || now-Date.parse(r.checkedAt)>5*60000 || Date.parse(r.checkedAt)>now+30000) return {state:'pending',message:'Saved privately. Waiting for the Mac to reconnect.'};
  if(r.version!==manifest.version || r.displayCount!==3 || r.rotationIntervalSeconds!==1800 || !Array.isArray(r.displays) || r.displays.length!==3 || new Set(r.displays.map(d=>d.id)).size!==3) return {state:'pending',message:'Saved privately. Waiting for all three Mac screens to sync.'};
  return {state:'confirmed',message:'Confirmed in the wallpaper collection for all three Mac screens.',checkedAt:r.checkedAt};
}
function installFavorites(router,{store,owner,origin,now}) {
  const id = value => typeof value==='string' && /^[a-f0-9]{64}$/.test(value);
  const mutate=(req,res,next)=>req.headers.origin===origin && req.headers['x-brief-action']==='favorite' ? next() : res.sendStatus(403);
  const express=require('express');
  router.get('/api/brief/favorites',owner,async(req,res)=>{
    if(req.query.after!==undefined && !id(req.query.after)) return res.sendStatus(400);
    try { const [list,manifest]=await Promise.all([store.listFavorites(req.query.after),store.favoriteManifest()]);return res.json({...list,wallpaper:wallpaperStatus(manifest,now())}); }
    catch {return res.status(503).json({error:'Private favorites unavailable'});}
  });
  router.get('/api/brief/favorites/manifest',owner,async(req,res)=>{
    try { const manifest=await store.favoriteManifest();return res.json({...manifest,wallpaper:wallpaperStatus(manifest,now())}); }
    catch {return res.status(503).json({error:'Private favorites unavailable'});}
  });
  router.get('/api/brief/favorites/:id/image',owner,async(req,res)=>{
    if(!id(req.params.id)) return res.sendStatus(400);
    try { const image=await store.favoriteBytes(req.params.id);if(!image || !['image/png','image/jpeg'].includes(image.mime))return res.sendStatus(404);
      if(hash(image.bytes)!==req.params.id)return res.sendStatus(503);
      res.set({'X-Brief-Image-SHA256':req.params.id,'Content-Disposition':`attachment; filename="favorite-${req.params.id}.${image.mime==='image/png' ? 'png' : 'jpg'}"`});return res.type(image.mime).send(image.bytes);
    } catch {return res.status(503).json({error:'Private favorite unavailable'});}
  });
  router.post('/api/brief/favorites',owner,mutate,express.json({limit:'1kb'}),async(req,res)=>{
    if(!req.body || Object.keys(req.body).sort().join(',')!=='forDate,sha256' || !id(req.body.sha256) || !/^\d{4}-\d{2}-\d{2}$/.test(req.body.forDate))return res.sendStatus(400);
    try {const favorite=await store.favoriteImage(req.body.sha256,req.body.forDate,now());return res.json({favorite,wallpaper:wallpaperStatus(await store.favoriteManifest(),now())});}
    catch(error){return res.status(error instanceof FavoriteConflict ? 409 : 503).json({error:error instanceof FavoriteConflict ? 'The displayed image changed. Reload the brief before saving.' : 'Favorite save could not be confirmed'});}
  });
  router.put('/api/brief/favorites/:id',owner,mutate,express.json({limit:'1kb'}),async(req,res)=>{
    if(!id(req.params.id) || !req.body || Object.keys(req.body).join(',')!=='active' || typeof req.body.active!=='boolean')return res.sendStatus(400);
    try {const favorite=await store.setFavorite(req.params.id,req.body.active,now());if(!favorite)return res.sendStatus(404);return res.json({favorite,wallpaper:wallpaperStatus(await store.favoriteManifest(),now())});}
    catch {return res.status(503).json({error:'Favorite change could not be confirmed'});}
  });
}
module.exports={createFavoritesStore,installFavorites,wallpaperStatus,FavoriteConflict};
