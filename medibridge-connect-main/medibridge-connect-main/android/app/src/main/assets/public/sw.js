// MediBridge AI - Service Worker
// Version-based cache busting
const CACHE_VERSION = 'v1.0.0';
const STATIC_CACHE = `medibridge-static-${CACHE_VERSION}`;
const DYNAMIC_CACHE = `medibridge-dynamic-${CACHE_VERSION}`;
const API_CACHE = `medibridge-api-${CACHE_VERSION}`;

// Assets to pre-cache during install (app shell)
const STATIC_ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/icon-192x192.png',
  '/icon-512x512.png',
  '/favicon.ico',
];

// API patterns that should use Network First strategy
const API_PATTERNS = [
  /\/api\//,
  /\/auth\//,
  /localhost:8000/,
  /127\.0\.0\.1:8000/,
];

// Resources that should never be cached
const NO_CACHE_PATTERNS = [
  /\/ws\//,           // WebSocket connections
  /hot-update/,       // HMR updates
  /__vite/,           // Vite dev server internals
  /node_modules/,     // Dev dependencies
  /\.map$/,           // Source maps
];

// =====================================================
// INSTALL EVENT - Pre-cache static assets (app shell)
// =====================================================
self.addEventListener('install', (event) => {
  console.log('[SW] Installing Service Worker...');
  
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then((cache) => {
        console.log('[SW] Pre-caching app shell');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        // Force the new service worker to become active immediately
        return self.skipWaiting();
      })
      .catch((err) => {
        console.error('[SW] Pre-cache failed:', err);
      })
  );
});

// =====================================================
// ACTIVATE EVENT - Clean up old caches
// =====================================================
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating Service Worker...');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((name) => {
              // Delete caches that don't match current version
              return name.startsWith('medibridge-') && 
                     name !== STATIC_CACHE && 
                     name !== DYNAMIC_CACHE && 
                     name !== API_CACHE;
            })
            .map((name) => {
              console.log('[SW] Deleting old cache:', name);
              return caches.delete(name);
            })
        );
      })
      .then(() => {
        // Claim all open clients immediately
        return self.clients.claim();
      })
  );
});

// =====================================================
// FETCH EVENT - Serve from cache or network
// =====================================================
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') return;

  // Skip requests that should never be cached
  if (NO_CACHE_PATTERNS.some((pattern) => pattern.test(request.url))) return;

  // Skip chrome-extension and other non-http(s) schemes
  if (!request.url.startsWith('http')) return;

  // ---- Strategy: Network First for API calls ----
  if (API_PATTERNS.some((pattern) => pattern.test(request.url))) {
    event.respondWith(networkFirst(request, API_CACHE));
    return;
  }

  // ---- Strategy: Cache First for static assets ----
  if (isStaticAsset(request.url)) {
    event.respondWith(cacheFirst(request, STATIC_CACHE));
    return;
  }

  // ---- Strategy: Stale While Revalidate for navigation & dynamic content ----
  if (request.mode === 'navigate') {
    event.respondWith(networkFirstWithFallback(request));
    return;
  }

  // ---- Default: Cache First with Network Fallback ----
  event.respondWith(cacheFirst(request, DYNAMIC_CACHE));
});

// =====================================================
// CACHING STRATEGIES
// =====================================================

/**
 * Cache First: Try cache, fallback to network, then cache the response
 */
async function cacheFirst(request, cacheName) {
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }

  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (err) {
    // Return offline fallback for images
    if (request.destination === 'image') {
      return new Response(
        '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><rect fill="#f0f9ff" width="200" height="200"/><text fill="#0891b2" font-size="14" x="50%" y="50%" text-anchor="middle" dy=".3em">Offline</text></svg>',
        { headers: { 'Content-Type': 'image/svg+xml' } }
      );
    }
    throw err;
  }
}

/**
 * Network First: Try network, fallback to cache
 */
async function networkFirst(request, cacheName) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (err) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return a JSON error for API requests when offline
    return new Response(
      JSON.stringify({ 
        error: 'offline', 
        message: 'You are currently offline. Please check your connection.' 
      }),
      { 
        status: 503, 
        headers: { 'Content-Type': 'application/json' } 
      }
    );
  }
}

/**
 * Network First with Offline Fallback for navigation requests
 */
async function networkFirstWithFallback(request) {
  try {
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      const cache = await caches.open(DYNAMIC_CACHE);
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  } catch (err) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return the cached index.html for SPA navigation fallback
    const fallback = await caches.match('/index.html');
    if (fallback) {
      return fallback;
    }
    
    // Ultimate fallback: offline page
    return new Response(getOfflinePage(), {
      headers: { 'Content-Type': 'text/html' }
    });
  }
}

// =====================================================
// HELPER FUNCTIONS
// =====================================================

function isStaticAsset(url) {
  const staticExtensions = [
    '.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', 
    '.ico', '.woff', '.woff2', '.ttf', '.eot', '.webp'
  ];
  return staticExtensions.some((ext) => url.includes(ext));
}

function getOfflinePage() {
  return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>MediBridge AI - Offline</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: 'Inter', system-ui, sans-serif;
          background: linear-gradient(160deg, #f0f9ff, #ecfdf5);
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
        }
        .offline-container {
          text-align: center;
          max-width: 480px;
          padding: 3rem 2rem;
          background: white;
          border-radius: 1.5rem;
          box-shadow: 0 8px 30px -8px rgba(8, 145, 178, 0.15);
        }
        .offline-icon {
          width: 80px;
          height: 80px;
          margin: 0 auto 1.5rem;
          background: linear-gradient(135deg, #0891b2, #10b981);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .offline-icon svg {
          width: 40px;
          height: 40px;
          fill: white;
        }
        h1 {
          font-size: 1.5rem;
          font-weight: 700;
          color: #1e3a5f;
          margin-bottom: 0.75rem;
        }
        p {
          color: #64748b;
          line-height: 1.6;
          margin-bottom: 1.5rem;
        }
        button {
          background: linear-gradient(135deg, #0891b2, #10b981);
          color: white;
          border: none;
          padding: 0.75rem 2rem;
          font-size: 1rem;
          font-weight: 600;
          border-radius: 0.75rem;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(8, 145, 178, 0.3);
        }
        button:active { transform: translateY(0); }
      </style>
    </head>
    <body>
      <div class="offline-container">
        <div class="offline-icon">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M1 1l22 22M16.72 11.06A10.94 10.94 0 0119 12.55M5 12.55a10.94 10.94 0 015.17-2.39M10.71 5.05A16 16 0 0122.56 9M1.42 9a15.91 15.91 0 014.7-2.88M8.53 16.11a6 6 0 016.95 0M12 20h.01" 
              fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        <h1>You're Offline</h1>
        <p>It looks like you've lost your internet connection. Some features of MediBridge AI require an active connection. Please check your network and try again.</p>
        <button onclick="window.location.reload()">Try Again</button>
      </div>
    </body>
    </html>
  `;
}

// =====================================================
// PUSH NOTIFICATION SUPPORT
// =====================================================
self.addEventListener('push', (event) => {
  console.log('[SW] Push notification received');

  let data = {
    title: 'MediBridge AI',
    body: 'You have a new notification',
    icon: '/icon-192x192.png',
    badge: '/icon-192x192.png',
    tag: 'medibridge-notification',
  };

  if (event.data) {
    try {
      const payload = event.data.json();
      data = { ...data, ...payload };
    } catch (e) {
      data.body = event.data.text();
    }
  }

  const options = {
    body: data.body,
    icon: data.icon || '/icon-192x192.png',
    badge: data.badge || '/icon-192x192.png',
    tag: data.tag || 'medibridge-notification',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/',
      dateOfArrival: Date.now(),
    },
    actions: data.actions || [
      { action: 'open', title: 'Open App' },
      { action: 'dismiss', title: 'Dismiss' },
    ],
  };

  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
  console.log('[SW] Notification click received');
  event.notification.close();

  const urlToOpen = event.notification.data?.url || '/';

  if (event.action === 'dismiss') return;

  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true })
      .then((clientList) => {
        // If the app is already open, focus it
        for (const client of clientList) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            client.navigate(urlToOpen);
            return client.focus();
          }
        }
        // Otherwise open a new window
        return self.clients.openWindow(urlToOpen);
      })
  );
});

// Handle background sync (for offline form submissions)
self.addEventListener('sync', (event) => {
  console.log('[SW] Background sync:', event.tag);
  
  if (event.tag === 'sync-appointments') {
    event.waitUntil(syncAppointments());
  }
});

async function syncAppointments() {
  // Placeholder for syncing queued appointments when back online
  console.log('[SW] Syncing queued appointments...');
}

// Periodic background sync (when supported)
self.addEventListener('periodicsync', (event) => {
  if (event.tag === 'health-check') {
    event.waitUntil(performHealthCheck());
  }
});

async function performHealthCheck() {
  console.log('[SW] Performing periodic health check...');
}
