// Browser helper for the pinned question comment. NOT a Node script: its text is run inside a
// youtube.com/watch tab with the Chrome tool's javascript_exec. Procedure: Docs/PINNED_COMMENTS.md.
// Each step is its own call, with a small screenshot between steps (the tab is in the background
// and YouTube only opens its menu and dialog when a frame is drawn).
(() => {
  const s = (ms) => new Promise((r) => setTimeout(r, ms));
  const n = (x) => x.replace(/\s+/g, ' ').trim();
  const q = (a, b = document) => [...b.querySelectorAll(a)];
  const w = async (f, k = 24) => { for (let i = 0; i < k; i++) { const r = f(); if (r) return r; await s(500); } throw new Error('timeout ' + f); };
  const BOX = 'ytd-comment-simplebox-renderer';
  let T = '';
  const thread = () => q('ytd-comment-thread-renderer').find((x) => x.querySelector('#content-text') && n(x.querySelector('#content-text').innerText) === T);
  const pinned = () => q('#pinned-comment-badge').some((x) => /Pinned/.test(x.innerText));
  window.H = {
    // Has the comment box loaded? Never throws. false = scroll the page again with the mouse.
    t: async () => { try { await w(() => document.querySelector(`${BOX} #placeholder-area`), 12); return true; } catch (e) { return false; } },
    // Open the comment box and focus it. Refuses when a pinned comment or this text is already there.
    a: async (text) => {
      T = text;
      const v = document.querySelector('video'); if (v) v.pause();
      const b = await w(() => document.querySelector(`${BOX} #placeholder-area`));
      await s(1500);
      if (pinned()) throw new Error('already pinned');
      if (thread()) throw new Error('already posted');
      b.scrollIntoView({ block: 'center' }); b.click(); await s(1200);
      const e = document.querySelector(`${BOX} #contenteditable-root`); e.focus();
      if (document.activeElement !== e) throw new Error('no focus');
      return 'ready';   // now TYPE the text with the keyboard tool
    },
    b1: () => { const e = document.querySelector(`${BOX} #contenteditable-root`); if (n(e.innerText) !== T) throw new Error('mismatch ' + e.innerText); document.querySelector(`${BOX} #submit-button button`).click(); return 'sent'; },
    b2: async () => { (await w(thread)).querySelector('#action-menu button').click(); return 'menu'; },
    b3: async () => { const it = await w(() => q('ytd-menu-popup-renderer ytd-menu-navigation-item-renderer,ytd-menu-popup-renderer ytd-menu-service-item-renderer').find((x) => x.innerText.trim() === 'Pin')); (it.querySelector('tp-yt-paper-item') || it).click(); return 'pin'; },
    b4: async () => { (await w(() => { const d = q('tp-yt-paper-dialog').find((x) => x.style.display !== 'none' && x.querySelector('yt-confirm-dialog-renderer')); return d && q('button', d).find((x) => x.innerText.trim() === 'Pin'); })).click(); return 'ok'; },
    b5: async () => { await w(pinned); return location.search + ' PINNED'; },
  };
})();
