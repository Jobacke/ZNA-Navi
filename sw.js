// ZNA-Navi Service Worker – App startet auch ohne Netz
const CACHE = 'zna-navi-1.4.1'; // bei jeder neuen Version anpassen
const FILES = ['./', './index.html', './version.json', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png', './favicon-64.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return; // API-Aufrufe nicht cachen
  // Netz zuerst (damit Updates ankommen), bei Funkloch aus dem Cache
  // Immer beim Server nachfragen (GitHub Pages cacht sonst bis zu 10 Min.), bei Funkloch Cache
  e.respondWith(
    fetch(e.request.url, { cache: 'no-cache', credentials: 'same-origin' })
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html')))
  );
});
