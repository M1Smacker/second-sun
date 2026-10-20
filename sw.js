// Second Sun offline cache (SITE-BLUEPRINT.md §6). hooks.py fills in VERSION, IMG_VERSION and SHELL.
// 1. Shell: every HTML page + CSS/JS/icons/search index, fetched in small batches at install.
//    A file that fails is skipped (and fetched at runtime later), so one bad file never kills offline mode.
// 2. Images: cached the first time they are viewed, capped at IMAGE_CAP entries, oldest out first.
// 3. Updates: a new worker WAITS. The page shows "Updated. Reload"; the worker takes over only when
//    the reader taps it (message SKIP_WAITING). No forced reloads mid-read.
const VERSION = "8f44a349ecc1";
const IMG_VERSION = "377fe18f1a63";
const SHELL = ["404.html", "assets/book.js", "assets/demos.js", "assets/extra.css", "assets/fonts/ibm-plex-mono-latin-400-normal.woff2", "assets/fonts/ibm-plex-mono-latin-500-normal.woff2", "assets/fonts/ibm-plex-sans-latin-500-normal.woff2", "assets/fonts/ibm-plex-sans-latin-600-normal.woff2", "assets/fonts/OFL-ibm-plex.txt", "assets/fonts/OFL-source-serif-4.txt", "assets/fonts/source-serif-4-latin-400-italic.woff2", "assets/fonts/source-serif-4-latin-400-normal.woff2", "assets/fonts/source-serif-4-latin-600-normal.woff2", "assets/icon-180.png", "assets/icon-512.png", "assets/images/favicon.png", "assets/javascripts/bundle.d7400e89.min.js", "assets/javascripts/workers/search.2c215733.min.js", "assets/observatory.css", "assets/stylesheets/main.ec1eaa64.min.css", "assets/stylesheets/palette.ab4e12ef.min.css", "book/ch1-two-suns/index.html", "book/ch1-two-suns/", "book/ch2-light-curves/index.html", "book/ch2-light-curves/", "book/ch3-wandering-transits/index.html", "book/ch3-wandering-transits/", "book/ch4-our-detector/index.html", "book/ch4-our-detector/", "book/ch5-vetting/index.html", "book/ch5-vetting/", "book/ch6-our-data/index.html", "book/ch6-our-data/", "book/credit-and-publishing/index.html", "book/credit-and-publishing/", "candidates/index.html", "candidates/", "claims/index.html", "claims/", "glossary/index.html", "glossary/", "index.html", "./", "learn/index.html", "learn/", "learn/l1-dip-depth/index.html", "learn/l1-dip-depth/", "manifest.webmanifest", "progress/index.html", "progress/", "quests/index.html", "quests/", "search/search_index.json", "sitemap.xml"];
const SHELL_CACHE = "ss-shell-" + VERSION;
const IMAGE_CACHE = "ss-images-" + IMG_VERSION;
const IMAGE_CAP = 150;
const BATCH = 8;

const abs = (p) => new URL(p, self.registration.scope).href;
const SHELL_SET = new Set(SHELL.map(abs));
const isImage = (url) => /\.(png|jpe?g|gif|webp|avif|svg)$/i.test(url.pathname);

async function precache() {
  const cache = await caches.open(SHELL_CACHE);
  for (let i = 0; i < SHELL.length; i += BATCH) {
    await Promise.allSettled(SHELL.slice(i, i + BATCH).map(async (p) => {
      const res = await fetch(new Request(abs(p), { cache: "no-cache" }));   // revalidate: never precache a stale HTTP-cached copy
      if (!res.ok || res.redirected) throw new Error(`${res.status} ${p}`);
      await cache.put(abs(p), res);
    }));
  }
}

self.addEventListener("install", (e) => e.waitUntil(precache()));

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys
        .filter((k) => k.startsWith("ss-") && k !== SHELL_CACHE && k !== IMAGE_CACHE)
        .map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (e) => {
  if (e.data && e.data.type === "SKIP_WAITING") self.skipWaiting();
});

async function fromShell(req) {
  const cache = await caches.open(SHELL_CACHE);
  const hit = await cache.match(req, { ignoreSearch: true });
  if (hit) return hit;
  // "/learn" -> "/learn/" (the cached pretty URL): one redirect, and the target ends in "/" so it can't loop
  const url = new URL(req.url);
  if (req.mode === "navigate" && !url.pathname.endsWith("/") && !/\.[a-z0-9]+$/i.test(url.pathname)) {
    const slashed = url.origin + url.pathname + "/" + url.search;
    if (await cache.match(slashed, { ignoreSearch: true })) return Response.redirect(slashed, 301);
  }
  try {
    const res = await fetch(req);
    // fill in anything the install skipped; never store redirects or other origins
    if (res.ok && res.type === "basic" && !res.redirected) await cache.put(req, res.clone());
    return res;
  } catch (err) {
    if (req.mode === "navigate") {
      const notFound = await cache.match(abs("404.html"));
      if (notFound) return notFound;
    }
    return Response.error();
  }
}

async function trimImages(cache) {
  const keys = await cache.keys();                  // insertion order = oldest first
  for (let i = 0; i < keys.length - IMAGE_CAP; i++) await cache.delete(keys[i]);
}

async function fromImages(req) {
  const cache = await caches.open(IMAGE_CACHE);
  const hit = await cache.match(req, { ignoreSearch: true });
  if (hit) return hit;
  try {
    const res = await fetch(req);
    if (res.ok && res.type === "basic") {
      await cache.put(req, res.clone());
      await trimImages(cache);
    }
    return res;
  } catch (err) {
    if (req.mode === "navigate") {                // opening an unvisited image offline: show the 404 page
      const notFound = await (await caches.open(SHELL_CACHE)).match(abs("404.html"));
      if (notFound) return notFound;
    }
    return Response.error();
  }
}

self.addEventListener("fetch", (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== self.location.origin || url.pathname.endsWith("/sw.js")) return;
  e.respondWith(isImage(url) && !SHELL_SET.has(url.href) ? fromImages(req) : fromShell(req));
});
