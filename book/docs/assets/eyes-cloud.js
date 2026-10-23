/* Eyes mode cloud backup. Every finished (or abandoned) round is sent to the private Firestore project by itself, the moment it ends, or as soon
   as the internet is back. Nobody has to copy, paste or send anything (Ahmed's rule). Browser: window.SSEyesCloud. Node: module.exports (tested by
   book/tools/test_eyes_cloud.mjs). The document shape and the "create once, never change" behaviour are fixed by the published Firestore rules
   (research/firebase-setup-steps.md); the apiKey below is Firebase's public web key (every Firebase site shows it), the rules are the protection. */
(function (root, factory) {
  const api = factory(root);
  if (typeof module === "object" && module.exports) module.exports = api; else root.SSEyesCloud = api;
})(typeof self !== "undefined" ? self : this, function (root) {
  "use strict";
  const DEFAULTS = { project: "second-sun-faea5", apiKey: "AIzaSyBogX_Jte_4fahJ1Ovp3y-twCmxheLTSxY", base: "https://firestore.googleapis.com" };
  const BACKOFF = [5000, 15000, 60000, 300000], REFUSED_RETRY = 600000, POLL_MS = 15000;

  function createUploader(o) {
    const store = o.store, core = o.core, cfg = Object.assign({}, DEFAULTS, o.config || {});
    const doFetch = o.fetch, setT = o.setTimer || ((f, ms) => setTimeout(f, ms)), clearT = o.clearTimer || ((t) => clearTimeout(t));
    const isOnline = o.isOnline || (() => true), timeoutMs = o.timeoutMs === undefined ? 20000 : o.timeoutMs;
    const listeners = [];
    let sending = false, timer = null, failures = 0, state = "idle", stopped = false;

    const url = (id) => `${cfg.base}/v1/projects/${cfg.project}/databases/(default)/documents/eyes_rounds?documentId=${encodeURIComponent(id)}&key=${encodeURIComponent(cfg.apiKey)}`;
    const pending = () => store.unsynced().length;
    const syncedCount = () => store.rounds().filter((r) => r.sync).length;

    const paused = !!o.paused;                                                // a test copy of the book must never write to Ahmed's real cloud data
    function status() {
      if (paused) return "Cloud backup is paused on this test copy of the book. Rounds are kept on this device only.";
      const p = pending();
      if (sending || (p && state === "idle")) return "Cloud backup: sending your round...";
      if (p && state === "refused") return `Cloud backup: ${p} round(s) could not be sent yet. They stay on this device and the book keeps trying.`;
      if (p) return `Cloud backup: ${p} round(s) waiting for the internet. They will send themselves.`;
      const s = syncedCount();
      return s ? `Cloud backup: all ${s} finished round(s) are safe in the cloud, and Claude can read them.`
               : "Cloud backup is on. Each finished round is sent by itself, even if you are offline at the time.";
    }
    const notify = () => listeners.forEach((f) => { try { f(status()); } catch (e) { /* a listener must never break sending */ } });

    function schedule() {
      if (timer || stopped) return;
      // while the device knows it is offline there is nothing to try: wait for the browser's "online" event, with a slow safety check
      const delay = state === "refused" ? REFUSED_RETRY : !isOnline() ? POLL_MS : BACKOFF[Math.min(Math.max(failures - 1, 0), BACKOFF.length - 1)];
      timer = setT(() => { timer = null; flush(); }, delay);
    }

    async function sendOne(r) {
      const body = JSON.stringify(core.toFirestoreBody(r, store.device));
      const init = { method: "POST", headers: { "Content-Type": "application/json" }, body };
      if (body.length < 60000) init.keepalive = true;                     // lets a send finish even if the page is closing
      let t = null;
      if (timeoutMs && typeof AbortController !== "undefined") { const c = new AbortController(); init.signal = c.signal; t = setT(() => c.abort(), timeoutMs); }
      try { return (await doFetch(url(r.id), init)).status; } finally { if (t) clearT(t); }
    }

    // Sends every finished round the cloud does not have yet, oldest first. Safe to call at any time and as often as you like.
    async function flush() {
      if (stopped || sending || paused) return;
      if (!pending()) { state = "idle"; failures = 0; notify(); return; }
      if (!isOnline()) { state = "offline"; failures = Math.max(failures, 1); schedule(); notify(); return; }
      sending = true; state = "sending"; notify();
      const tried = new Set(); let netFail = false;
      while (!netFail) {
        const next = store.unsynced().filter((r) => !tried.has(r.id)).sort((a, b) => a.t0 - b.t0)[0];
        if (!next) break;
        tried.add(next.id);
        let code;
        try { code = await sendOne(next); } catch (e) { netFail = true; break; }
        if (code === 200 || code === 409) store.markSynced(next.id);       // 409: the cloud already has this round (an earlier answer was lost): that is success
        else if (code === 429 || code >= 500) netFail = true;               // busy or down: try again later
        /* 400/403: the cloud refused this round as it is; leave it queued, keep going with the others */
      }
      sending = false;
      if (netFail) { state = "offline"; failures++; schedule(); }
      else if (pending()) { state = "refused"; failures++; schedule(); }
      else { state = "idle"; failures = 0; if (timer) { clearT(timer); timer = null; } }
      notify();
    }

    return { flush, status, onStatus: (f) => listeners.push(f), stop() { stopped = true; if (timer) { clearT(timer); timer = null; } }, get state() { return state; } };
  }

  // ---- browser wiring: one uploader per page visit, started by the Eyes screen ----
  let current = null;
  function attach(store) {
    if (current) current.dispose();
    const core = root.SSEyes, cfg = {};
    if (root.SSEYES_CLOUD_BASE) cfg.base = root.SSEYES_CLOUD_BASE;           // tests only: a mock server instead of Firestore
    const host = (root.location && root.location.hostname) || "";
    const testCopy = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(host) && !root.SSEYES_CLOUD_BASE && !root.SSEYES_CLOUD_ALLOW_LOCAL;   // only the real end-to-end test sets ALLOW_LOCAL
    const up = createUploader({ store, core, fetch: (u, i) => root.fetch(u, i), config: cfg, paused: testCopy, isOnline: () => root.navigator.onLine !== false });
    const go = () => up.flush(), vis = () => { if (root.document.visibilityState === "visible") up.flush(); };
    store.onChange((ev) => { if (ev === "finish" || ev === "recover") up.flush(); });
    root.addEventListener("online", go); root.document.addEventListener("visibilitychange", vis);
    const poll = root.setInterval(() => { if (store.unsynced().length) up.flush(); }, POLL_MS);
    up.dispose = () => { up.stop(); root.removeEventListener("online", go); root.document.removeEventListener("visibilitychange", vis); root.clearInterval(poll); };
    current = up; up.flush();                                                 // also sends anything left over from earlier visits
    return up;
  }

  return { createUploader, attach, DEFAULTS,
           status: () => (current ? current.status() : "Cloud backup: not started."),
           onStatus: (f) => { if (current) current.onStatus(f); } };
});
