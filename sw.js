// Second Sun offline cache (SITE-BLUEPRINT.md §6). hooks.py fills in VERSION, IMG_VERSION and SHELL.
// 1. Shell: every HTML page + CSS/JS/icons/search index, fetched in small batches at install.
//    A file that fails is skipped (and fetched at runtime later), so one bad file never kills offline mode.
// 2. Images: cached the first time they are viewed, capped at IMAGE_CAP entries, oldest out first.
// 3. Updates: a new worker WAITS. The page shows "Updated. Reload"; the worker takes over only when
//    the reader taps it (message SKIP_WAITING). No forced reloads mid-read.
const VERSION = "a11033b91d9f";
const IMG_VERSION = "ad846b6cf609";
const SHELL = ["404.html", "assets/book.js", "assets/data/toi1338-s98.json", "assets/data/watch.json", "assets/demos.js", "assets/extra.css", "assets/eyes-cloud.js", "assets/eyes-core.js", "assets/eyes-feedback.js", "assets/eyes-hard.js", "assets/eyes-strength.js", "assets/fonts/atkinson-hyperlegible-next-latin-wght-italic.woff2", "assets/fonts/atkinson-hyperlegible-next-latin-wght-normal.woff2", "assets/fonts/ibm-plex-mono-latin-400-normal.woff2", "assets/fonts/ibm-plex-mono-latin-500-normal.woff2", "assets/fonts/ibm-plex-sans-latin-400-normal.woff2", "assets/fonts/ibm-plex-sans-latin-600-normal.woff2", "assets/fonts/OFL-atkinson-hyperlegible-next.txt", "assets/fonts/OFL-ibm-plex-sans.txt", "assets/fonts/OFL-ibm-plex.txt", "assets/fonts/OFL-noto-sans-math.txt", "assets/fonts/OFL-noto-sans-symbols-2.txt", "assets/fonts/ss-cross.woff2", "assets/fonts/ss-symbols.woff2", "assets/glossary.json", "assets/icon-180.png", "assets/icon-512.png", "assets/images/favicon.png", "assets/img/nasa/ACD20-0045-002.jpg", "assets/img/nasa/PIA14724.jpg", "assets/img/nasa/PIA14725.jpg", "assets/javascripts/bundle.d7400e89.min.js", "assets/javascripts/workers/search.2c215733.min.js", "assets/observatory.css", "assets/shape.css", "assets/stylesheets/main.ec1eaa64.min.css", "assets/stylesheets/palette.ab4e12ef.min.css", "assets/watch.js", "book/01-stars-names-missions/index.html", "book/01-stars-names-missions/", "book/02-light-curves/index.html", "book/02-light-curves/", "book/03-our-data/index.html", "book/03-our-data/", "book/04-two-suns/index.html", "book/04-two-suns/", "book/05-wandering-transits/index.html", "book/05-wandering-transits/", "book/06-orbits-three-body/index.html", "book/06-orbits-three-body/", "book/07-noise-and-statistics/index.html", "book/07-noise-and-statistics/", "book/08-our-detector/index.html", "book/08-our-detector/", "book/09-fake-planets/index.html", "book/09-fake-planets/", "book/10-vetting/index.html", "book/10-vetting/", "book/11-pixels-and-neighbours/index.html", "book/11-pixels-and-neighbours/", "book/12-stanley/index.html", "book/12-stanley/", "book/13-your-workshop/index.html", "book/13-your-workshop/", "book/14-credit-and-publishing/index.html", "book/14-credit-and-publishing/", "book/15-mistakes-as-lessons/index.html", "book/15-mistakes-as-lessons/", "candidates/index.html", "candidates/", "claims/index.html", "claims/", "eyes/index.html", "eyes/", "field-notes/2026-10-19/index.html", "field-notes/2026-10-19/", "field-notes/2026-10-20/index.html", "field-notes/2026-10-20/", "field-notes/2026-10-21/index.html", "field-notes/2026-10-21/", "field-notes/2026-10-23/index.html", "field-notes/2026-10-23/", "field-notes/2026-10-24/index.html", "field-notes/2026-10-24/", "field-notes/2026-10-27/index.html", "field-notes/2026-10-27/", "field-notes/2026-10-28/index.html", "field-notes/2026-10-28/", "field-notes/2026-10-29/index.html", "field-notes/2026-10-29/", "field-notes/2026-10-30/index.html", "field-notes/2026-10-30/", "field-notes/index.html", "field-notes/", "glossary/index.html", "glossary/", "index.html", "./", "labs/lab0-workbench/index.html", "labs/lab0-workbench/", "labs/lab1-name-to-number/index.html", "labs/lab1-name-to-number/", "labs/lab2-get-the-data/index.html", "labs/lab2-get-the-data/", "labs/lab3-plot-and-read/index.html", "labs/lab3-plot-and-read/", "labs/lab4-find-a-dip/index.html", "labs/lab4-find-a-dip/", "labs/lab5-two-suns/index.html", "labs/lab5-two-suns/", "labs/lab6-fake-planets/index.html", "labs/lab6-fake-planets/", "labs/lab7-pixels/index.html", "labs/lab7-pixels/", "labs/lab8-read-stanley/index.html", "labs/lab8-read-stanley/", "labs/lab9-your-star/index.html", "labs/lab9-your-star/", "learn/index.html", "learn/", "learn/l1-dip-depth/index.html", "learn/l1-dip-depth/", "manifest.webmanifest", "parts/part1/cheat/index.html", "parts/part1/cheat/", "parts/part1/index.html", "parts/part1/", "parts/part1/labs/index.html", "parts/part1/labs/", "parts/part1/review/index.html", "parts/part1/review/", "parts/part2/cheat/index.html", "parts/part2/cheat/", "parts/part2/index.html", "parts/part2/", "parts/part2/labs/index.html", "parts/part2/labs/", "parts/part2/review/index.html", "parts/part2/review/", "parts/part3/cheat/index.html", "parts/part3/cheat/", "parts/part3/index.html", "parts/part3/", "parts/part3/labs/index.html", "parts/part3/labs/", "parts/part3/review/index.html", "parts/part3/review/", "parts/part4/cheat/index.html", "parts/part4/cheat/", "parts/part4/index.html", "parts/part4/", "parts/part4/labs/index.html", "parts/part4/labs/", "parts/part4/review/index.html", "parts/part4/review/", "parts/part5/cheat/index.html", "parts/part5/cheat/", "parts/part5/index.html", "parts/part5/", "parts/part5/labs/index.html", "parts/part5/labs/", "parts/part5/review/index.html", "parts/part5/review/", "parts/part6/cheat/index.html", "parts/part6/cheat/", "parts/part6/index.html", "parts/part6/", "parts/part6/labs/index.html", "parts/part6/labs/", "parts/part6/review/index.html", "parts/part6/review/", "progress/index.html", "progress/", "quests/index.html", "quests/", "reference/for-astronomers/index.html", "reference/for-astronomers/", "reference/prior-work/index.html", "reference/prior-work/", "reference/reading-list/index.html", "reference/reading-list/", "search/search_index.json", "sitemap.xml", "start/first-search/index.html", "start/first-search/", "start/how-to-read/index.html", "start/how-to-read/", "start/index.html", "start/", "start/journey/index.html", "start/journey/", "start/story-so-far/index.html", "start/story-so-far/", "versions/index.html", "versions/", "watch/index.html", "watch/"];
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
