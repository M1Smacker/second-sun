// Second Sun offline cache (SITE-BLUEPRINT.md §6). hooks.py fills in VERSION, IMG_VERSION and SHELL.
// 1. Shell: every HTML page + CSS/JS/icons/search index, fetched in small batches at install.
//    A file that fails is skipped (and fetched at runtime later), so one bad file never kills offline mode.
// 2. Images: cached the first time they are viewed, capped at IMAGE_CAP entries, oldest out first.
// 3. Fresh first (bug 62, 2 Nov 2026): every page, style, script and data file asks the network first
//    (revalidating, so GitHub's 10 minute browser copy never wins) and waits at most FRESH_MS; offline or
//    slow, the saved copy answers exactly as before. So a refresh always brings the newest book while online.
//    Fonts stay cache-first (they never change in place); images keep their own cache.
// 4. Updates: a new worker WAITS. The page shows "Updated. Reload"; the worker takes over only when
//    the reader taps it (message SKIP_WAITING). No forced reloads mid-read. A worker that installs deletes the
//    shell caches of workers that were replaced before they ever ran (only the active worker's cache and its own stay).
const VERSION = "__VERSION__";
const IMG_VERSION = "__IMG_VERSION__";
const SHELL = __SHELL__;
const SHELL_CACHE = "ss-shell-" + VERSION;
const IMAGE_CACHE = "ss-images-" + IMG_VERSION;
const META_CACHE = "ss-meta";                       // one entry: the shell cache of the worker that is running
const IMAGE_CAP = 150;
const BATCH = 8;
const FRESH_MS = 3000;

const abs = (p) => new URL(p, self.registration.scope).href;
const SHELL_SET = new Set(SHELL.map(abs));
const isImage = (url) => /\.(png|jpe?g|gif|webp|avif|svg)$/i.test(url.pathname);
const isFont = (url) => /\.(woff2?|ttf|otf)$/i.test(url.pathname);

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

// Delete the shell caches of workers that were replaced while waiting. Needs the note the running worker left
// at activation; with no note (first install, or the worker before this change) nothing is deleted.
async function pruneReplaced() {
  const note = await (await caches.open(META_CACHE)).match("active");
  if (!note) return;
  const running = await note.text();
  const keys = await caches.keys();
  await Promise.all(keys.filter((k) => k.startsWith("ss-shell-") && k !== SHELL_CACHE && k !== running).map((k) => caches.delete(k)));
}

self.addEventListener("install", (e) => e.waitUntil(precache().then(pruneReplaced)));

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys
        .filter((k) => k.startsWith("ss-") && k !== SHELL_CACHE && k !== IMAGE_CACHE && k !== META_CACHE)
        .map((k) => caches.delete(k))))
      .then(() => caches.open(META_CACHE))
      .then((meta) => meta.put("active", new Response(SHELL_CACHE)))
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

// Network first, with the saved copy as the fallback (offline, a server error, or slower than FRESH_MS).
// A late network answer still refreshes the saved copy. Redirects (/learn -> /learn/) pass straight through.
async function freshFirst(e, req) {
  let saved = Promise.resolve();
  const net = fetch(req, { cache: "no-cache" }).then((res) => {
    if (res.status >= 500) throw new Error(String(res.status));
    if (res.ok && res.type === "basic" && !res.redirected) {
      const copy = res.clone();
      saved = caches.open(SHELL_CACHE).then((c) => c.put(req, copy)).catch(() => {});
    }
    return res;
  });
  e.waitUntil(net.then(() => saved, () => {}));
  const first = await Promise.race([net.then((r) => r, () => null), new Promise((done) => setTimeout(done, FRESH_MS, null))]);
  return first || fromShell(req);                   // null = offline, a server error, or too slow
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
  e.respondWith(isImage(url) && !SHELL_SET.has(url.href) ? fromImages(req) : isFont(url) ? fromShell(req) : freshFirst(e, req));
});
