// Search window: draws the JSON made by pipeline/watch_export.py (counts, charts and event pictures). It fetches again every 60 s and redraws; nothing to tap.
// Source order: GitHub API on the data branch (about 1 min behind the search), then raw.githubusercontent (up to 5 min behind), then the snapshot shipped with the book.
(() => {
  const REPO = "M1Smacker/second-sun";
  const API = `https://api.github.com/repos/${REPO}/contents/watch.json?ref=watch-data`;
  const RAW = `https://raw.githubusercontent.com/${REPO}/watch-data/watch.json`;
  const me = document.currentScript && document.currentScript.src;
  const own = me ? new URL("data/watch.json", me).href : "assets/data/watch.json";
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const pct = (a, b) => (b ? Math.min(100, Math.round((100 * a) / b)) : 0);
  const num = (n) => (n == null ? "n/a" : Number(n).toLocaleString());
  const dur = (s) => (s < 90 ? Math.round(s) + " s" : s < 5400 ? Math.round(s / 60) + " min" : (s / 3600).toFixed(1) + " h");
  const PHASE = { search: "Pass 1 of 3: searching the light curves", sap: "Pass 2 of 3: searching the raw-light twins", pdc: "Pass 3 of 3: second look at the raw-light dips", finished: "All three passes finished" };
  const STAGES = [
    ["Read the light-curve files", (d) => `${num(d.files.read_ok)} files read`, ["search", "sap"]],
    ["Hide the star's own eclipses, flatten slow drifts", () => "10-minute bins, 2-day smoothing", ["search", "sap"]],
    ["Look for dips: 9 box lengths, real and upside-down", (d) => `${num(d.events.found)} dips and dents found`, ["search", "sap"]],
    ["Nine safety checks, one after another", (d) => `${num((d.events.stopped_by.find((x) => x.flag === "clean") || {}).n)} passed them all`, ["search", "sap"]],
    ["Ask a second light curve of the same star", (d) => `self-test: ${pct(d.selftest.second_product_sees, d.selftest.fakes)}% of fake planets seen`, ["pdc"]],
    ["Sort into tiers", (d) => `tier 1 kept: ${num(["1A", "1L", "1B"].reduce((a, k) => a + ((d.events.tiers || {})[k] || 0), 0))}`, []],
  ];
  const EVERY = Math.max(5, Number(new URLSearchParams(location.search).get("every")) || 60);   // seconds between checks; 60 keeps us inside GitHub's rate limit
  let data = null, fetchedAt = 0, lastError = "";

  const bar = (name, a, b, note, keep) => `<div class="sw-row"><div class="sw-lab"><b>${esc(name)}</b><span>${num(a)} of ${num(b)} (${pct(a, b)}%)</span></div><div class="sw-bar ${keep ? "sw-keep" : ""}"><i style="width:${pct(a, b)}%"></i></div>${note ? `<small>${note}</small>` : ""}</div>`;
  const row = (txt, n, max, keep) => `<div class="sw-flag"><div class="sw-lab"><span>${esc(txt)}</span><b>${num(n)}</b></div><div class="sw-bar ${keep ? "sw-keep" : ""}"><i style="width:${pct(n, max)}%"></i></div></div>`;

  function chart(h, key, label) {
    const pts = (h || []).filter((p) => p[key] != null);
    if (pts.length < 2) return `<p class="sw-small">${esc(label)}: chart starts after a few minutes.</p>`;
    const W = 320, H = 70, t0 = pts[0].t, t1 = pts[pts.length - 1].t, ymax = Math.max(1, ...pts.map((p) => p[key]));
    const xy = pts.map((p) => `${(((p.t - t0) / Math.max(1, t1 - t0)) * W).toFixed(1)},${(H - 4 - (p[key] / ymax) * (H - 10)).toFixed(1)}`).join(" ");
    return `<svg viewBox="0 0 ${W} ${H}" class="sw-chart" role="img" aria-label="${esc(label)} over time"><polyline points="${xy}" fill="none" stroke="var(--ss-accent)" stroke-width="2"/></svg><div class="sw-lab"><small>${esc(label)} (highest ${num(ymax)})</small><small>last ${dur(t1 - t0)}</small></div>`;
  }

  function pic(c) {
    const W = 340, H = 170, L = 46, R = 8, T = 8, B = 26, X0 = -36, X1 = 36;
    const lo = Math.min(...c.y, -c.depth * 1.15, 0), hi = Math.max(...c.y, 0), sx = (v) => L + ((v - X0) / (X1 - X0)) * (W - L - R), sy = (v) => T + ((hi - v) / Math.max(1, hi - lo)) * (H - T - B);
    const dots = c.x.map((x, i) => `<circle cx="${sx(x).toFixed(1)}" cy="${sy(c.y[i]).toFixed(1)}" r="1.5"/>`).join("");
    const gaps = c.gaps.map((g) => `<line x1="${sx(g).toFixed(1)}" x2="${sx(g).toFixed(1)}" y1="${T}" y2="${H - B}" class="sw-gap"/>`).join("");
    const xt = [-36, -24, -12, 0, 12, 24, 36].map((v) => `<text x="${sx(v)}" y="${H - 12}" text-anchor="middle">${v}</text>`).join("");
    const yt = [lo, 0, hi].map((v) => `<text x="${L - 4}" y="${sy(v) + 3}" text-anchor="end">${Math.round(v)}</text>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" class="sw-pic" role="img" aria-label="Light curve of TIC ${c.tic} around a dip"><rect x="${sx(-c.dur / 2)}" y="${T}" width="${sx(c.dur / 2) - sx(-c.dur / 2)}" height="${H - T - B}" class="sw-box"/>${gaps}<line x1="${L}" x2="${W - R}" y1="${sy(0)}" y2="${sy(0)}" class="sw-zero"/><g class="sw-dots">${dots}</g><g class="sw-ax">${xt}${yt}<text x="${(L + W - R) / 2}" y="${H - 1}" text-anchor="middle">hours from the dip</text></g></svg>`;
  }
  const KIND = { real: "the star's real light", flip: "the upside-down copy (the star's light flipped, so noise shows as a dip)" };
  const card = (c) => `<figure class="sw-card">${pic(c)}<figcaption><b>TIC ${c.tic}, sector ${c.sector}</b> <small>${c.at} UTC</small><br>${c.dur} h dip, ${num(c.depth)} ppm deep, signal-to-noise ${c.snr}.<br>${["1A", "1L", "1B"].includes(c.tier) ? "<b>Kept (tier 1).</b> No check stopped it." : "<b>Set aside (tier " + esc(c.tier) + ").</b> " + esc(c.what)}${c.kind ? `<br><small>Drawn from ${KIND[c.kind]}.</small>` : ""}</figcaption></figure>`;

  const funnel = (L) => { const mx = Math.max(1, ...L.stages.map((s) => s.both)); return L.stages.map((s) => `<div class="sw-flag"><div class="sw-lab"><span>${esc(s.label)}</span><b>${s.real == null ? num(s.both) : `${num(s.real)} real, ${num(s.flip)} upside-down`}</b></div><div class="sw-bar sw-keep"><i style="width:${pct(s.real == null ? s.both : s.real, mx)}%"></i></div>${s.real == null ? "" : `<div class="sw-bar"><i style="width:${pct(s.flip, mx)}%"></i></div>`}</div>`).join(""); };
  const leadCard = (c) => `<figure class="sw-card">${c.x && c.x.length ? pic(c) : '<p class="sw-small">No picture could be drawn for this one.</p>'}<figcaption><b>Lead ${esc(c.id)}: TIC ${c.tic}, sector ${c.sector}</b> <small>BTJD ${c.center}</small><br>${c.dur} h dip, ${num(c.depth)} ppm deep, signal-to-noise ${c.snr}. This star has ${c.events} confirmed ${c.events === 1 ? "dip" : "dips"} in the run.<ul class="sw-checks">${c.checks.map((k) => `<li class="sw-c-${k.s}">${esc(k.t)}</li>`).join("")}</ul><b>Next check:</b> ${esc(c.next)}</figcaption></figure>`;
  const leadsHtml = (d) => {
    const L = d.leads;
    if (!L) return "";
    return `<h3>What the search found</h3><p class="sw-verdict">${esc(L.verdict)}</p>${L.scored ? `<p class="sw-verdict">${esc(L.scored)}</p>` : ""}${funnel(L)}<p class="sw-small">${L.blind ? "Real and upside-down are pooled while the run is blind." : (L.final ? "The upside-down numbers are how many false alarms to expect. These are the counts the scorecard uses: all checks applied, the best light curve of each star in each sector, the cleaned-light half of the search." : "The upside-down numbers are how many false alarms to expect. Running counts, before the last checks; each unit is a star in one sector.")}${L.known ? ` ${num(L.known)} confirmed ${L.known === 1 ? "star is" : "stars are"} already known TOI or planet hosts and not counted as leads.` : ""} A lead is not a planet. It passed every check, still needs 2 or 3 more, and becomes a candidate only with two keys (see the Candidates page).</p>${L.cards && L.cards.length ? `<div class="sw-cards">${L.cards.map(leadCard).join("")}</div>` : ""}`;
  };

  function light() {
    if (!data) return ["off", "No data yet", ""];
    const age = (Date.now() - Date.parse(data.updated)) / 1000, w = data.machine && data.machine.workers, loop = data.loop_s || 60, stale = Math.max(180, 3 * loop + 60);
    if (data.phase === "finished") return ["done", "FINISHED", "All three passes are complete."];
    if (age > stale) return ["stale", "NOT UPDATING", `No new numbers for ${dur(age)}. The search is paused, the computer is asleep, or this is old data.`];
    if (w === 0) return ["warn", "WATCHING, NO SEARCH PROCESS FOUND", "No search process is running on the computer."];
    return ["live", "RUNNING", w ? `${w} search processes working` : "fresh numbers"];
  }

  function paintLight() {
    const el = document.getElementById("sw-light"), age = document.getElementById("sw-age");
    if (!el) return;
    const [cls, head, sub] = light();
    el.className = "sw-light sw-l-" + cls; el.innerHTML = `<span class="sw-dot"></span><span><b>${head}</b><br><small>${esc(sub)}</small></span>`;
    if (age && data) age.textContent = `numbers ${dur((Date.now() - Date.parse(data.updated)) / 1000)} old · next refresh in ${Math.max(0, EVERY - Math.round((Date.now() - fetchedAt) / 1000))} s${lastError ? " · " + esc(lastError) : ""}`;
  }

  function draw(el, d) {
    const open = [...el.querySelectorAll("details[open]")].map((x) => x.dataset.k);
    const p = d.progress, ev = d.events, t = ev.tiers || {}, max = Math.max(1, ...ev.stopped_by.map((x) => x.n)), tot = Object.values(t).reduce((a, b) => a + b, 0), r = d.run || {}, s = r.settings || {}, m = d.machine || {};
    const boxMax = Math.max(1, ...Object.values(ev.boxes || {})), bandMax = Math.max(1, ...Object.values(ev.bands || {}));
    const active = (st) => (st[2].includes(d.phase) ? " sw-active" : "");
    const tiers = [["1A", "Kept: a second light curve agrees"], ["1L", "Kept: a second light curve weakly agrees"], ["1B", "Kept: no second light curve exists"], ["2", "Set aside: a safety check fired"], ["3", "Set aside: the second light curve says no"]];
    el.innerHTML = `
      <div id="sw-light" class="sw-light"></div>
      <p class="sw-small" id="sw-age"></p>
      <h3>Right now</h3>
      <p class="sw-now"><b>${esc(PHASE[d.phase] || d.phase)}.</b> ${p.eta_min != null ? `About ${p.per_min} star-sectors a minute, roughly ${p.eta_min} minutes left in this pass.` : ""}</p>
      ${d.notes && d.notes.length ? `<p class="sw-note"><small>${esc(d.notes[0].at.slice(11, 16))} UTC, note from Claude</small><br>${esc(d.notes[0].text)}</p>` : ""}
      <p class="sw-small">${esc(d.label)}</p>
      ${d.blind ? '<p class="sw-blind"><b>Blind run.</b> Real and upside-down dips are pooled, and pictures do not say which kind they are, until the final analysis is done. That keeps the test honest.</p>' : ""}
      ${leadsHtml(d)}
      <h3>The path every star takes</h3>
      <div class="sw-flow">${STAGES.map((st, i) => `<div class="sw-stage${active(st)}"><small>${i + 1}</small><b>${esc(st[0])}</b><span>${esc(st[1](d))}</span></div>${i < STAGES.length - 1 ? '<div class="sw-arrow">&#8595;</div>' : ""}`).join("")}</div>
      <h3>Pictures from the search</h3>
      <p class="sw-small">Real TESS light from the star, 36 hours either side of a dip, in 10-minute bins. The shaded box is where the search saw the dip. Dashed lines are gaps in the data. Up is brighter, down is dimmer; the numbers on the left are ppm from the star's usual level.${d.blind ? " In the sealed run some pictures are the upside-down copy, drawn the same way and not labelled, so the final test stays fair." : ""}</p>
      ${d.gallery && d.gallery.kept.length ? `<h4>Kept</h4><div class="sw-cards">${d.gallery.kept.map(card).join("")}</div>` : ""}
      ${d.gallery && d.gallery.stopped.length ? `<h4>Stopped by a check</h4><div class="sw-cards">${d.gallery.stopped.map(card).join("")}</div>` : ""}
      <h3>How far along</h3>
      ${bar("Pass 1: search", p.search[0], p.search[1], "")}
      ${bar("Pass 2: raw-light twin", p.sap[0], p.sap[1], "")}
      ${bar("Pass 3: second look", p.pdc[0], p.pdc[1], "")}
      <p class="sw-small">Each unit is one star in one TESS sector. ${num(p.stars)} stars in this run.</p>
      <h3>Speed</h3>
      ${chart(d.history, "per_min", "star-sectors per minute")}
      ${chart(d.history, "done", "star-sectors finished")}
      <h3>The nine safety checks</h3>
      <p class="sw-small">${num(ev.found)} dips and dents were found. Each one is stopped by the <b>first</b> check that fires, in this order. First-pass counts, before the final union step.</p>
      ${ev.stopped_by.map((x) => row(x.text, x.n, max, x.flag === "clean")).join("")}
      <h3>Where they end up (first pass)</h3>
      ${tiers.map(([k, txt]) => row(`Tier ${k}. ${txt}`, t[k] || 0, tot, k[0] === "1")).join("")}
      ${ev.by_kind ? `<p class="sw-small">Development run, split shown: real ${num(ev.by_kind.real)}, upside-down ${num(ev.by_kind.flip || 0)}.</p>` : ""}
      <h3>What kind of dips is it finding?</h3>
      <p class="sw-small">By box length in hours (how long the dip lasts):</p>
      ${Object.entries(ev.boxes || {}).map(([k, v]) => row(k + " h", v, boxMax)).join("")}
      <p class="sw-small">By strength (signal-to-noise; 7 is the bar):</p>
      ${Object.entries(ev.bands || {}).map(([k, v]) => row(k, v, bandMax)).join("")}
      <h3>The built-in self-test</h3>
      <p>Every star-sector gets fake planets pasted in as a test. The second light curve sees <b>${num(d.selftest.second_product_sees)}</b> of <b>${num(d.selftest.fakes)}</b> (${pct(d.selftest.second_product_sees, d.selftest.fakes)}%) clearly enough (signal-to-noise 4 or more). A sudden drop here means something is broken.</p>
      <h3>Files</h3>
      <p>${num(d.files.read_ok)} light-curve files read. Skipped: ${Object.keys(d.files.skipped).length ? Object.entries(d.files.skipped).map(([k, v]) => num(v) + " (" + esc(k) + ")").join(", ") : "none"}. Products searched: ${Object.entries(d.files.products).map(([k, v]) => esc(k) + " " + num(v)).join(", ")}.</p>
      <h3>Latest finished</h3>
      <table class="sw-tick"><tr><th>Time (UTC)</th><th>Star (TIC)</th><th>Sector</th><th>Files</th><th>Dips and dents</th></tr>${d.ticker.map((x) => `<tr><td>${x.at}</td><td>${x.tic}</td><td>${x.sector}</td><td>${x.files}</td><td>${x.events}</td></tr>`).join("")}</table>
      ${d.notes && d.notes.length > 1 ? `<h3>Notes from Claude</h3>${d.notes.map((n) => `<p class="sw-small"><b>${esc(n.at.slice(5, 16).replace("T", " "))}</b> ${esc(n.text)}</p>`).join("")}` : ""}
      <details data-k="tech" class="sw-tech"><summary>Technical details</summary>
        <table class="sw-tick">
          <tr><td>Version</td><td>${esc(r.version || "")}</td></tr>
          <tr><td>Settings fingerprint</td><td>${esc(r.hash ? r.hash.slice(0, 12) : "none")}</td></tr>
          <tr><td>Code commit</td><td>${esc(r.git_commit || "n/a")}</td></tr>
          <tr><td>Run folder</td><td>${esc(r.folder || "")}</td></tr>
          <tr><td>Started</td><td>${esc(d.started || "n/a")}</td></tr>
          <tr><td>Signal-to-noise bar</td><td>${num(s.snr_bar)}</td></tr>
          <tr><td>Box lengths (h)</td><td>${esc((s.boxes_h || []).join(", ") || "n/a")}</td></tr>
          <tr><td>Time bin (days)</td><td>${num(s.bin_days)}</td></tr>
          <tr><td>Study switches</td><td>${esc((s.options || []).join(", ") || "none")}</td></tr>
          <tr><td>Refresh</td><td>every 60 s; the numbers run 1 to 2 minutes behind the computer</td></tr>
          <tr><td>Computer</td><td>${m.workers == null ? "n/a" : m.workers + " search processes"}, CPU ${m.cpu == null ? "n/a" : m.cpu + "%"}</td></tr>
        </table>
        <p class="sw-small"><b>Words.</b> <i>SNR</i>: how many times stronger a dip is than the noise. <i>Box</i>: a flat-bottomed dip of fixed length that we slide along the star's light. <i>Upside-down copy</i>: the same light flipped, so noise makes bumps instead of dips; it counts how often noise alone fakes a dip. <i>Tier 1</i>: no known innocent cause. <i>Union</i>: merging the cleaned light and the raw-light twin into one list. <i>Blind</i>: real and fake-direction counts pooled.</p>
      </details>`;
    open.forEach((k) => { const x = el.querySelector(`details[data-k="${k}"]`); if (x) x.open = true; });
    paintLight();
  }

  async function grab(urls) {
    for (const [u, opt] of urls) {
      try { const r = await fetch(u, opt); if (r.ok) return await r.json(); lastError = "GitHub answered " + r.status; } catch (e) { lastError = "could not reach GitHub"; }
    }
    return null;
  }

  async function load(el) {
    const custom = new URLSearchParams(location.search).get("src");
    const urls = custom ? [[custom, { cache: "no-store" }]] : [[API, { cache: "no-cache", headers: { Accept: "application/vnd.github.raw+json" } }], [RAW + "?t=" + Math.floor(Date.now() / 60000), { cache: "no-store" }], [own, { cache: "no-store" }]];
    const d = await grab(urls);
    fetchedAt = Date.now();
    if (d) { lastError = ""; if (!data || d.updated !== data.updated) { data = d; draw(el, d); } else data = d; }
    else if (!data) el.textContent = "No search is running yet.";
    paintLight();
  }

  const start = () => {
    const el = document.getElementById("ss-watch");
    if (!el || el.dataset.ready) return;
    el.dataset.ready = "1"; load(el);
    setInterval(() => load(el), EVERY * 1000);
    setInterval(paintLight, 1000);
  };
  if (typeof document$ !== "undefined") document$.subscribe(start); else document.addEventListener("DOMContentLoaded", start);
})();
