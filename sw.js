const CACHE_NAME = 'walimurid-online-v1';
const STATIC_ASSETS = [
  './manifest.json',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap',
  'https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js'
];

// Install: Cache hanya aset statis luar (font & library)
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate: Bersihkan cache lama
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: NETWORK ONLY untuk HTML/Data agar selalu mutakhir
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Jika permintaan halaman HTML atau data Firestore, langsung ambil dari jaringan (Network Only)
  if (event.request.mode === 'navigate' || url.pathname.endsWith('.html') || url.origin.includes('firestore.googleapis.com')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // Aset statis lainnya (Font/Chart.js) menggunakan Network First dengan Cache Fallback
  event.respondWith(
    fetch(event.request).catch(() => caches.match(event.request))
  );
});
