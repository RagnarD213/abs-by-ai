/* Shared local-review recovery. Reload media, never the page or review notes. */
(() => {
  'use strict';
  const IDLE = 60000, STALL = 10000, LIMIT = 2;
  const players = new Map();
  let lastTick = Date.now(), hiddenAt = 0;
  const source = v => v.getAttribute('src') || v.currentSrc || '';

  function attach(v) {
    if (players.has(v)) return;
    const box = document.createElement('div');
    box.className = 'review-recovery';
    box.style.cssText = 'display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:8px 0;font:13px/1.4 system-ui';
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = 'Reload video';
    button.style.cssText = 'font:inherit;padding:6px 10px;border:1px solid #b5cbd9;border-radius:6px;background:#fff;color:#215575;cursor:pointer';
    const status = document.createElement('span');
    status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    status.style.color = '#516676';
    box.append(button, status); v.insertAdjacentElement('afterend', box);
    const s = {lastProgress:Date.now(), lastTime:v.currentTime, retries:0, pending:null, source:source(v), status};
    players.set(v, s);
    function cancel() {
      if (s.pending) {
        clearTimeout(s.pending.timer);
        s.pending = null;
      }
    }
    function recover(manual = false) {
      if (!source(v) || s.pending || (!manual && s.retries >= LIMIT)) return;
      if (manual) s.retries = 0;
      s.retries++;
      const state = {src:source(v), time:v.currentTime || 0, rate:v.playbackRate,
        muted:v.muted, volume:v.volume, playing:!v.paused && !v.ended, restored:false};
      s.pending = state;
      status.textContent = 'Reloading video...';
      state.timer = setTimeout(() => {
        if (s.pending !== state) return;
        cancel();
        status.textContent = 'Video unavailable. Try Reload video or the download link.';
      }, 15000);
      // load() discards the stale decoder/buffer without touching page notes or controls.
      v.load();
    }
    button.addEventListener('click', () => recover(true));
    s.recover = recover;
    v.addEventListener('loadstart', () => {
      if (source(v) !== s.source) {
        cancel(); s.source = source(v); s.retries = 0; status.textContent = '';
      }
      s.lastProgress = Date.now(); s.lastTime = v.currentTime;
    });
    v.addEventListener('loadedmetadata', () => {
      const state = s.pending;
      if (!state) return;
      // Run after the page's own source-switch handlers.
      setTimeout(() => {
        if (s.pending !== state || source(v) !== state.src) return;
        v.muted = state.muted; v.volume = state.volume; v.playbackRate = state.rate;
        v.currentTime = Number.isFinite(v.duration) ? Math.min(state.time, Math.max(0, v.duration - .04)) : state.time;
        state.restored = true;
        if (v.readyState >= 2) finish();
      }, 0);
    });
    function finish() {
      const state = s.pending;
      if (!state || !state.restored || v.readyState < 2) return;
      cancel(); s.lastProgress = Date.now(); s.lastTime = v.currentTime;
      status.textContent = 'Video ready.';
      if (state.playing) v.play().catch(() => { status.textContent = 'Video ready. Press play to continue.'; });
    }
    v.addEventListener('loadeddata', finish);
    v.addEventListener('canplay', finish);
    v.addEventListener('timeupdate', () => {
      if (!s.pending && Math.abs(v.currentTime - s.lastTime) > .02) {
        s.lastProgress = Date.now(); s.lastTime = v.currentTime;
      }
    });
    v.addEventListener('playing', () => { s.lastProgress = Date.now(); });
    v.addEventListener('play', () => {
      if (Date.now() - s.lastProgress >= IDLE) recover();
      else s.lastProgress = Date.now();
    });
    v.addEventListener('error', () => {
      if (s.pending) return;
      recover();
      if (!s.pending) status.textContent = 'Video unavailable. Try Reload video or the download link.';
    });
  }
  function scan() { document.querySelectorAll('video').forEach(attach); }
  function resume() {
    const now = Date.now();
    if (hiddenAt && now - hiddenAt >= IDLE) {
      players.forEach((s, v) => { if (v.isConnected) s.recover(); });
    }
    hiddenAt = 0; lastTick = now;
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) hiddenAt = Date.now(); else resume();
  });
  window.addEventListener('pageshow', e => { if (e.persisted) players.forEach(s => s.recover()); });
  window.addEventListener('focus', () => { if (!document.hidden) resume(); });
  setInterval(() => {
    const now = Date.now(), woke = now - lastTick >= IDLE;
    lastTick = now;
    if (document.hidden) return;
    players.forEach((s, v) => {
      if (!v.isConnected) { players.delete(v); return; }
      if (woke || (!v.paused && !v.ended && !v.seeking && now - s.lastProgress >= STALL)) s.recover();
    });
  }, 2000);
  scan();
  new MutationObserver(scan).observe(document.documentElement, {childList:true, subtree:true});
})();
