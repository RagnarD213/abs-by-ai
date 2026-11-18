/* Silent automation, paused sound-ready owner handoff. Exported media is untouched. */
(() => {
  'use strict';
  if (window.__absReviewPlayerLoaded) return;
  window.__absReviewPlayerLoaded = true;
  const IDLE = 60000, STALL = 10000, LIMIT = 2;
  const players = new Map();
  let mode = 'automation', explicitChecks = false, gesture = false, gestureVersion = 0;
  let lastTick = Date.now(), hiddenAt = 0, workflowStatus;
  const source = v => v.getAttribute('src') || v.currentSrc || '';
  const silence = v => { v.muted = true; v.defaultMuted = true; };
  const disableAutoplay = v => { v.autoplay = false; v.removeAttribute('autoplay'); };
  const isPaused = v => v.paused === true;

  function pauseSilent(v) {
    silence(v); disableAutoplay(v);
    try { v.pause(); } catch (_) { return false; }
    return isPaused(v);
  }
  function armOwner(v, s) {
    // Never enable sound on playing media. Do not change the chosen volume.
    if (!isPaused(v)) return false;
    disableAutoplay(v);
    v.defaultMuted = false; v.muted = false;
    s.ownerReady = true; s.lastProgress = Date.now();
    return isPaused(v) && !v.muted;
  }
  function state() {
    return {mode, players:[...players].filter(([v]) => v.isConnected).map(([v,s]) => ({
      id:v.id || '', paused:isPaused(v), muted:v.muted, volume:v.volume,
      ownerReady:s.ownerReady, recovering:!!s.pending, failed:s.failed
    }))};
  }
  function beginChecks() {
    mode = 'automation'; explicitChecks = true; gesture = false;
    scan();
    let ok = true;
    players.forEach((s,v) => {
      s.cancel(); s.ownerReady = false; s.ownerPlaying = false;
      if (v.isConnected && !pauseSilent(v)) ok = false;
    });
    if (workflowStatus) workflowStatus.textContent = 'Silent checks: playback stays muted.';
    return {ok, ...state()};
  }
  function handoff() {
    mode = 'automation'; gesture = false; explicitChecks = true;
    scan();
    // Cancel stale recoveries before pausing ALL players. A failure leaves all muted.
    let ok = true;
    players.forEach((s,v) => {
      s.cancel(); s.ownerReady = false; s.ownerPlaying = false;
      if (v.isConnected && (!pauseSilent(v) || s.failed)) ok = false;
    });
    if (ok) {
      mode = 'owner';
      try { players.forEach((s,v) => { if (v.isConnected && !armOwner(v,s)) ok = false; }); }
      catch (_) { ok = false; }
    }
    if (!ok) {
      mode = 'automation';
      players.forEach((s,v) => { s.ownerReady = false; s.ownerPlaying = false; pauseSilent(v); });
    } else {
      explicitChecks = false;
      // A reloaded owner link must not fall back to the task's automation URL.
      try {
        const url = new URL(window.location.href);
        if (url.searchParams.get('review_mode') === 'automation') {
          url.searchParams.delete('review_mode');
          window.history.replaceState(null, '', url.href);
        }
      } catch (_) { /* Unsupported history does not weaken the paused-only handoff. */ }
    }
    if (workflowStatus) workflowStatus.textContent = ok
      ? 'Paused. Sound is ready for your Play click.'
      : 'Handoff incomplete: a player could not pause or recover. All players remain muted.';
    return {ok, ...state()};
  }

  function attach(v) {
    if (players.has(v)) return players.get(v);
    silence(v); disableAutoplay(v);
    const box = document.createElement('div');
    box.className = 'review-recovery';
    box.style.cssText = 'display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:8px 0;font:13px/1.4 system-ui';
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = v.tagName === 'AUDIO' ? 'Reload audio' : 'Reload video';
    button.style.cssText = 'font:inherit;padding:6px 10px;border:1px solid #b5cbd9;border-radius:6px;background:#fff;color:#215575;cursor:pointer';
    const status = document.createElement('span');
    status.setAttribute('role', 'status'); status.setAttribute('aria-live', 'polite');
    box.append(button, status); v.insertAdjacentElement('afterend', box);
    const s = {lastProgress:Date.now(), lastTime:v.currentTime, retries:0, lastAttempt:0,
      pending:null, source:source(v), status, ownerReady:false, ownerPlaying:false, ownerSource:'', failed:false};
    players.set(v, s);
    function cancel() {
      if (s.pending) { clearTimeout(s.pending.timer); s.pending = null; }
    }
    s.cancel = cancel;
    function recover(manual = false) {
      if (Date.now() - s.lastAttempt > IDLE) s.retries = 0;
      if (!source(v) || s.pending || (!manual && s.retries >= LIMIT)) return;
      if (manual) s.retries = 0;
      s.retries++; s.lastAttempt = Date.now();
      const restore = {src:source(v), time:v.currentTime || 0, rate:v.playbackRate,
        resumeSilent:mode === 'automation' && !v.paused && !v.ended, restored:false};
      s.ownerReady = false; s.ownerPlaying = false; s.failed = false;
      if (!pauseSilent(v)) { s.failed = true; status.textContent = 'Could not pause. Player remains muted.'; return; }
      s.pending = restore;
      status.textContent = 'Reloading video...';
      restore.timer = setTimeout(() => {
        if (s.pending !== restore) return;
        cancel(); s.failed = true; pauseSilent(v);
        status.textContent = 'Video unavailable. Try Reload video or the download link.';
      }, 15000);
      v.load();
    }
    button.addEventListener('click', () => recover(true));
    s.recover = recover;
    v.addEventListener('loadstart', () => {
      const ownerStart = mode === 'owner' && s.ownerPlaying && s.ownerSource === source(v);
      if (!ownerStart) {
        silence(v); disableAutoplay(v); s.ownerReady = false;
        if (mode === 'owner' && !s.pending) {
          if (pauseSilent(v)) armOwner(v,s);
        }
      }
      if (source(v) !== s.source) {
        cancel(); s.source = source(v); s.retries = 0; s.failed = false; status.textContent = '';
      }
      s.lastProgress = Date.now(); s.lastTime = v.currentTime;
    });
    v.addEventListener('loadedmetadata', () => {
      const restore = s.pending;
      if (!restore) return;
      setTimeout(() => {
        if (s.pending !== restore || source(v) !== restore.src) return;
        silence(v); v.playbackRate = restore.rate;
        v.currentTime = Number.isFinite(v.duration) ? Math.min(restore.time, Math.max(0, v.duration - .04)) : restore.time;
        restore.restored = true;
        if (v.readyState >= 2) finish();
      }, 0);
    });
    function finish() {
      const restore = s.pending;
      if (!restore || !restore.restored || v.readyState < 2) return;
      cancel(); s.failed = false; s.lastProgress = Date.now(); s.lastTime = v.currentTime;
      if (mode === 'automation') {
        silence(v);
        if (restore.resumeSilent) v.play().catch(() => { status.textContent = 'Video ready. Press play to continue.'; });
        else v.pause();
      } else if (pauseSilent(v)) armOwner(v,s);
      status.textContent = 'Video ready. Press play to continue.';
    }
    v.addEventListener('loadeddata', finish);
    v.addEventListener('canplay', finish);
    v.addEventListener('timeupdate', () => {
      if (!s.pending && Math.abs(v.currentTime - s.lastTime) > .02) {
        s.lastProgress = Date.now(); s.lastTime = v.currentTime;
      }
    });
    v.addEventListener('playing', () => { s.lastProgress = Date.now(); });
    v.addEventListener('pause', () => { s.ownerPlaying = false; });
    v.addEventListener('play', () => {
      if (mode === 'automation') {
        silence(v);
        // A newly selected source is already loading. An idle reload here can
        // cancel its first Play before loadstart updates the recorded source.
        if (source(v) === s.source && Date.now() - s.lastProgress >= IDLE) recover();
      } else if (!v.muted && s.ownerReady) {
        s.ownerPlaying = true; s.ownerSource = source(v);
      }
      s.lastProgress = Date.now();
    });
    v.addEventListener('error', () => {
      s.failed = true;
      if (s.pending) return;
      recover();
      if (!s.pending) status.textContent = 'Video unavailable. Try Reload video or the download link.';
    });
    if (mode === 'owner' && pauseSilent(v)) armOwner(v,s);
    return s;
  }

  // Trusted owner gestures may use native controls or the page's context buttons.
  // Tasks MUST enter automation mode first; browser input cannot identify its human/agent origin.
  const ownerGesture = e => {
    if (!e.isTrusted) return;
    gesture = true;
    const version = ++gestureVersion;
    if (mode === 'owner') {
      const path = typeof e.composedPath === 'function' ? e.composedPath() : [e.target];
      const media = path.find(node => players.has(node));
      if (media) {
        const s = players.get(media);
        s.ownerPlaying = true; s.ownerSource = source(media);
      }
    }
    setTimeout(() => { if (version === gestureVersion) gesture = false; }, 0);
  };
  for (const event of ['pointerdown', 'pointerup', 'click', 'keydown']) {
    document.addEventListener(event, ownerGesture, true);
  }
  if (typeof HTMLMediaElement !== 'undefined') {
    const play = HTMLMediaElement.prototype.play;
    HTMLMediaElement.prototype.play = function (...args) {
      const s = attach(this);
      if (mode === 'owner' && gesture) {
        if (this.paused && !s.pending && (!s.ownerReady || s.source !== source(this))) {
          if (!armOwner(this,s)) return Promise.reject(new Error('Owner playback could not be prepared safely'));
        }
        s.ownerPlaying = true; s.ownerSource = source(this);
      } else if (mode === 'automation') {
        silence(this); s.ownerReady = false; s.ownerPlaying = false;
      } else {
        // Late page callbacks must neither autoplay nor re-mute a paused owner player.
        // Explicit automated checks use beginChecks(), where real playback stays muted.
        return Promise.resolve();
      }
      return play.apply(this, args);
    };
  }
  function scan() { document.querySelectorAll('video, audio').forEach(attach); }
  function initialize() {
    scan();
    const bar = document.createElement('div');
    bar.className = 'review-audio-workflow';
    bar.style.cssText = 'display:flex;gap:8px;align-items:center;flex-wrap:wrap;padding:8px;font:13px system-ui';
    const start = document.createElement('button'), done = document.createElement('button');
    start.type = done.type = 'button';
    start.textContent = 'Start silent checks'; done.textContent = 'Finish checks for owner';
    start.addEventListener('click', beginChecks); done.addEventListener('click', handoff);
    workflowStatus = document.createElement('span'); workflowStatus.setAttribute('role','status');
    bar.append(start, done, workflowStatus);
    if (document.body) document.body.insertAdjacentElement('afterbegin', bar);
    const automationURL = new URLSearchParams(window.location.search).get('review_mode') === 'automation';
    if (explicitChecks || automationURL) beginChecks(); else handoff();
  }
  window.AbsReviewAudio = {beginChecks, handoff, state};
  function resume() {
    const now = Date.now();
    if (hiddenAt && now - hiddenAt >= IDLE) players.forEach((s,v) => { if (v.isConnected) s.recover(); });
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
    players.forEach((s,v) => {
      if (!v.isConnected) { players.delete(v); return; }
      if ((woke && now - s.lastProgress >= STALL) || (!v.paused && !v.ended && !v.seeking && now - s.lastProgress >= STALL)) s.recover();
    });
  }, 2000);
  scan();
  new MutationObserver(scan).observe(document.documentElement, {childList:true, subtree:true});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, {once:true});
  else initialize();
})();
/* Real full screen for every review page (Dan, 2026-11-16, WV-03 R7: "the full screen control ... is NOT working").
   The Claude app's side pane refuses true full screen (requestFullscreen is denied there), so a page's own "Full screen"
   button could only stretch the video inside the pane and the native control is greyed out. In owner mode this module
   sends the video to VLC on the Mac instead (POST /__fullscreen to the review server, which opens the same file full
   screen at the same moment, with sound), pausing the in-page player. It catches: any button whose text is exactly
   "Full screen" (or [data-review-fullscreen]), a double-click on a video, and a refused native full-screen request.
   In silent-check (automation) mode it never opens anything, so tasks stay silent. If the server cannot open VLC, the
   page's own button runs as before. */
(() => {
  'use strict';
  if (window.__absReviewFullscreenLoaded) return;
  window.__absReviewFullscreenLoaded = true;
  let failedAt = 0, openedAt = 0, gestureAt = 0, busy = false;
  const owner = () => { try { return !!window.AbsReviewAudio && window.AbsReviewAudio.state().mode === 'owner'; } catch (_) { return false; } };
  const isVideo = el => !!el && el.tagName === 'VIDEO';
  const visible = v => { try { const r = v.getBoundingClientRect(); return r.width > 40 && r.height > 40; } catch (_) { return false; } };
  function pick(btn) {
    const all = [...document.querySelectorAll('video')];
    const named = btn && btn.dataset && (btn.dataset.video || btn.dataset.reviewFullscreen);
    if (named) { const v = document.getElementById(named); if (isVideo(v)) return v; }
    const playing = all.find(v => !v.paused && !v.ended);
    if (playing) return playing;
    for (let box = btn && btn.parentElement; box && box !== document.body; box = box.parentElement) {
      const v = [...box.querySelectorAll('video')].find(visible);
      if (v) return v;
    }
    return all.filter(visible).sort((a, b) => b.clientWidth * b.clientHeight - a.clientWidth * a.clientHeight)[0] || all[0] || null;
  }
  function toast(text) {
    let t = document.getElementById('abs-fs-toast');
    if (!t) {
      t = document.createElement('div'); t.id = 'abs-fs-toast'; t.setAttribute('role', 'status');
      t.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);z-index:2147483647;background:#0b1e33;color:#fff;' +
        'border:1px solid #4aa3ff;border-radius:10px;padding:10px 14px;font:14px system-ui;max-width:90vw;box-shadow:0 6px 24px #0008';
      document.body.appendChild(t);
    }
    t.textContent = text; t.style.display = 'block';
    clearTimeout(t._h); t._h = setTimeout(() => { t.style.display = 'none'; }, 6000);
  }
  async function openExternal(v) {
    if (!v) throw new Error('no video on this page');
    const src = v.currentSrc || v.getAttribute('src') || '';
    if (!src) throw new Error('video has no source yet');
    const t = Number.isFinite(v.currentTime) ? v.currentTime : 0;
    try { v.pause(); } catch (_) {}
    const r = await fetch('/__fullscreen', {method: 'POST', headers: {'Content-Type': 'application/json'},
                                            body: JSON.stringify({src, t, page: location.pathname})});
    let j = {}; try { j = await r.json(); } catch (_) {}
    if (!r.ok || !j.ok) throw new Error(j.error || ('server answered ' + r.status));
    toast('Playing full screen in ' + (j.player || 'VLC') + ' from ' + Math.floor(t / 60) + ':' + String(Math.floor(t % 60)).padStart(2, '0') +
          '. Press Esc or Cmd-Q there to come back.');
    return j;
  }
  async function open(v, fallback) {
    if (busy || Date.now() - openedAt < 2500) return;     // one click opens VLC once
    busy = true; openedAt = Date.now();
    try { await openExternal(v); }
    catch (e) { failedAt = Date.now(); if (fallback) fallback(); else toast('Full screen could not open: ' + e.message); }
    finally { busy = false; }
  }
  const isFsButton = el => !!el && (el.hasAttribute && el.hasAttribute('data-review-fullscreen') ||
    /^\s*full\s*-?\s*screen\s*$/i.test(el.textContent || ''));
  document.addEventListener('click', e => {
    const btn = e.target && e.target.closest ? e.target.closest('button, a, [role="button"]') : null;
    if (!isFsButton(btn) || !owner()) return;          // silent checks: the page's own in-pane behaviour only
    if (btn.dataset.absFsBypass) { delete btn.dataset.absFsBypass; return; }
    e.preventDefault(); e.stopImmediatePropagation();
    open(pick(btn), () => { btn.dataset.absFsBypass = '1'; btn.click(); });
  }, true);
  document.addEventListener('dblclick', e => {
    const v = e.target && e.target.closest ? e.target.closest('video') : null;
    if (!v || !owner()) return;
    e.preventDefault(); open(v);
  }, true);
  document.addEventListener('pointerdown', () => { if (owner()) gestureAt = Date.now(); }, true);
  document.addEventListener('fullscreenerror', e => {
    // only a refusal caused by the owner's own click just now (a native full-screen control); never loop after a failed VLC attempt
    if (!owner() || Date.now() - gestureAt > 1500 || Date.now() - failedAt < 3000) return;
    const el = e.target, v = isVideo(el) ? el : (el && el.querySelector ? el.querySelector('video') : null);
    if (v) open(v);
  });
  // Every video (2026-11-18, Dan on Joint Vigor R4: "make full screen controls work"): in the app's side pane the
  // player's own full-screen icon does nothing and fires no fullscreenerror, so the VLC hand-off above never ran. The
  // dead native icon is hidden and every video gets a permanent "Full screen" button right under it (handled by the
  // click capture above: VLC in owner mode). Double-click and the F key do the same. Plus the small hover chip.
  function enableNative() {
    let vids = []; try { vids = [...document.querySelectorAll('video')]; } catch (_) { return; }
    vids.forEach(v => {
      const list = (v.getAttribute('controlslist') || '').split(/\s+/).filter(x => x && x.toLowerCase() !== 'nofullscreen');
      list.push('nofullscreen');
      v.setAttribute('controlslist', list.join(' '));
      if (v.hasAttribute('data-abs-fs-nobutton') || v.__absFsButton || !v.parentNode) return;
      const next = v.nextElementSibling;
      if (next && next.hasAttribute && next.hasAttribute('data-review-fullscreen')) { v.__absFsButton = next; return; }
      const b = document.createElement('button'); b.type = 'button'; b.textContent = '⤢ Full screen';
      b.setAttribute('data-review-fullscreen', v.id || ''); b.setAttribute('data-abs-fs-button', '');
      b.style.cssText = 'display:inline-block;margin:6px 0 2px;padding:5px 12px;border-radius:8px;border:1px solid #4aa3ff;' +
        'background:#0b1e33;color:#fff;font:600 13px system-ui;cursor:pointer';
      v.__absFsButton = b; v.insertAdjacentElement('afterend', b);
    });
  }
  document.addEventListener('keydown', e => {
    if ((e.key !== 'f' && e.key !== 'F') || e.metaKey || e.ctrlKey || e.altKey || !owner()) return;
    const t = e.target; if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName || ''))) return;
    const v = pick(null); if (v) { e.preventDefault(); open(v); }
  }, true);
  let chip = null, chipVideo = null, chipHide = 0;
  function showChip(v) {
    if (!owner() || !visible(v)) return;
    if (!chip) {
      chip = document.createElement('button'); chip.type = 'button'; chip.textContent = '\u2922 Full screen';
      chip.setAttribute('data-abs-fs-chip', '');
      chip.style.cssText = 'position:fixed;z-index:2147483646;padding:5px 9px;border-radius:8px;border:1px solid #4aa3ff;' +
        'background:#0b1e33e6;color:#fff;font:600 12px system-ui;cursor:pointer';
      chip.addEventListener('click', e => { e.preventDefault(); e.stopPropagation(); if (chipVideo) open(chipVideo); });
      chip.addEventListener('mouseenter', () => clearTimeout(chipHide));
      chip.addEventListener('mouseleave', () => { chipHide = setTimeout(() => { chip.style.display = 'none'; }, 400); });
      document.body.appendChild(chip);
    }
    chipVideo = v; clearTimeout(chipHide);
    const r = v.getBoundingClientRect();
    chip.style.top = Math.max(4, r.top + 8) + 'px'; chip.style.left = Math.max(4, r.right - 112) + 'px'; chip.style.display = 'block';
  }
  document.addEventListener('mouseover', e => {
    const v = e.target && e.target.closest ? e.target.closest('video') : null;
    if (v) { enableNative(); showChip(v); }
  }, true);
  document.addEventListener('mouseout', e => {
    const v = e.target && e.target.closest ? e.target.closest('video') : null;
    if (v && chip) { clearTimeout(chipHide); chipHide = setTimeout(() => { chip.style.display = 'none'; }, 600); }
  }, true);
  window.addEventListener('scroll', () => { if (chip) chip.style.display = 'none'; }, true);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', enableNative, {once: true}); else enableNative();
  document.addEventListener('loadstart', enableNative, true);   // videos added later (media events do not bubble; capture sees them)
  window.AbsReviewFullscreen = {open: v => open(v), pick};
})();
