// Search window: draws assets/data/watch.json (made by pipeline/watch_export.py; aggregates only). Refreshes every 30 s.
(() => {
  const RAW = "https://raw.githubusercontent.com/M1Smacker/second-sun/main/book/docs/assets/data/watch.json";
  const local = /^(localhost|127\.0\.0\.1)$/.test(location.hostname);
  const me = document.currentScript && document.currentScript.src;
  const own = me ? new URL("data/watch.json", me).href : "assets/data/watch.json";   // resolved from this script's own address, so it works at any page depth
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const pct = (a, b) => (b ? Math.min(100, Math.round((100 * a) / b)) : 0);
  const ago = (iso) => { const s = Math.max(0, Math.round((Date.now() - Date.parse(iso)) / 1000)); return s < 90 ? s + " s ago" : s < 5400 ? Math.round(s / 60) + " min ago" : Math.round(s / 3600) + " h ago"; };
  const bar = (name, a, b, note) => `<div class="sw-row"><div class="sw-lab"><b>${esc(name)}</b><span>${a.toLocaleString()} of ${b.toLocaleString()}</span></div><div class="sw-bar"><i style="width:${pct(a, b)}%"></i></div>${note ? `<small>${note}</small>` : ""}</div>`;
  const PHASE = { search: "Step 1 of 3 running: searching the light curves", sap: "Step 2 of 3 running: searching the raw-light twins", pdc: "Step 3 of 3 running: second look at the raw-light dips", finished: "Finished" };

  function draw(el, d) {
    const p = d.progress, ev = d.events, max = Math.max(1, ...ev.stopped_by.map((x) => x.n)), t = ev.tiers || {};
    const tot = Object.values(t).reduce((a, b) => a + b, 0);
    const tierRow = [["1A", "Kept: a second light curve agrees"], ["1L", "Kept: a second light curve weakly agrees"], ["1B", "Kept: no second light curve exists"], ["2", "Set aside: a check fired"], ["3", "Set aside: the second light curve says no"]];
    el.innerHTML = `
      <div class="sw-head"><span class="sw-pill sw-${d.phase}">${esc(PHASE[d.phase] || d.phase)}</span><span class="sw-upd">updated ${ago(d.updated)}</span></div>
      <p class="sw-label">${esc(d.label)}</p>
      ${d.blind ? '<p class="sw-blind"><b>Blind mode.</b> Real dips and upside-down dips are counted together here on purpose. Nobody, not even Claude, sees which star has what until the preregistered analysis is run once at the end.</p>' : ""}
      <h3>How far along</h3>
      ${bar("1. Search", p.search[0], p.search[1], p.eta_min != null ? `about ${p.per_min} per minute, about ${p.eta_min} min left` : "")}
      ${bar("2. Raw-light twin", p.sap[0], p.sap[1])}
      ${bar("3. Second look", p.pdc[0], p.pdc[1])}
      <p class="sw-small">Each unit is one star in one TESS sector. ${p.stars} stars in this run.</p>
      <h3>The checks, one by one</h3>
      <p class="sw-small">${ev.found.toLocaleString()} dips and dents were found. Each is stopped by the <b>first</b> check that fires, in this order. These are first-pass counts, before the final union step.</p>
      ${ev.stopped_by.map((x) => `<div class="sw-flag"><div class="sw-lab"><span>${esc(x.text)}</span><b>${x.n.toLocaleString()}</b></div><div class="sw-bar ${x.flag === "clean" ? "sw-keep" : ""}"><i style="width:${pct(x.n, max)}%"></i></div></div>`).join("")}
      <h3>Where they end up (first pass)</h3>
      ${tierRow.map(([k, txt]) => `<div class="sw-flag"><div class="sw-lab"><span>Tier ${k}. ${txt}</span><b>${(t[k] || 0).toLocaleString()}</b></div><div class="sw-bar ${k[0] === "1" ? "sw-keep" : ""}"><i style="width:${pct(t[k] || 0, tot)}%"></i></div></div>`).join("")}
      ${ev.by_kind ? `<p class="sw-small">Development run, split shown: real ${ev.by_kind.real.toLocaleString()}, upside-down ${(ev.by_kind.flip || 0).toLocaleString()}.</p>` : ""}
      <h3>The built-in self-test</h3>
      <p>Every star-sector gets fake planets pasted in as a test. The second light curve sees <b>${d.selftest.second_product_sees.toLocaleString()}</b> of <b>${d.selftest.fakes.toLocaleString()}</b> (${pct(d.selftest.second_product_sees, d.selftest.fakes)}%) clearly enough (SNR 4 or more). If this number collapsed, the machine would be broken.</p>
      <h3>Files</h3>
      <p>${d.files.read_ok.toLocaleString()} light-curve files read. Skipped: ${Object.keys(d.files.skipped).length ? Object.entries(d.files.skipped).map(([k, v]) => v.toLocaleString() + " (" + esc(k) + ")").join(", ") : "none"}. Products searched: ${Object.entries(d.files.products).map(([k, v]) => esc(k) + " " + v.toLocaleString()).join(", ")}.</p>
      <h3>Latest finished</h3>
      <table class="sw-tick"><tr><th>Time (UTC)</th><th>Star (TIC)</th><th>Sector</th><th>Files</th><th>Dips and dents</th></tr>${d.ticker.map((r) => `<tr><td>${r.at}</td><td>${r.tic}</td><td>${r.sector}</td><td>${r.files}</td><td>${r.events}</td></tr>`).join("")}</table>`;
  }

  async function load(el) {
    const custom = new URLSearchParams(location.search).get("src");
    const urls = custom ? [custom] : local ? [own, RAW] : [RAW + "?t=" + Math.floor(Date.now() / 60000), own];
    for (const u of urls) {
      try { const r = await fetch(u, { cache: "no-store" }); if (r.ok) return draw(el, await r.json()); } catch (e) { /* try the next source */ }
    }
    el.textContent = "No search data yet. The page fills in when a run is exporting.";
  }

  const start = () => { const el = document.getElementById("ss-watch"); if (el && !el.dataset.ready) { el.dataset.ready = "1"; load(el); setInterval(() => load(el), 30000); } };
  if (typeof document$ !== "undefined") document$.subscribe(start); else document.addEventListener("DOMContentLoaded", start);
})();
