// Minimal service worker: provides an offline fallback page for navigations
// and handles Web Push (morning summary) notifications. It never caches app
// pages or API/Stripe/analytics requests, so live behavior is unchanged
// whenever the network is available.
const CACHE = 'absbyai-v3';

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) => cache.addAll(['/offline.html', '/img/logo.png']))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(() => caches.match('/offline.html'))
    );
  }
});

// ── Web Push: show the morning summary notification ──
self.addEventListener('push', (event) => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; } catch (e) { data = {}; }
  const title = data.title || 'Victory Dashboard';
  const options = {
    body: data.body || 'Your morning summary is ready.',
    icon: '/img/icon-192.png',
    badge: '/img/icon-192.png',
    data: { url: data.url || '/dashboard' },
    tag: 'morning-summary',
    renotify: true,
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

// Focus an existing dashboard tab on click, or open one.
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || '/dashboard';
  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((wins) => {
      for (const w of wins) {
        if (w.url.includes('/dashboard') && 'focus' in w) return w.focus();
      }
      return clients.openWindow ? clients.openWindow(url) : null;
    })
  );
});
