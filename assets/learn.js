/* Twinlight, the Second Sun learning app (Claude, 15 Nov 2026; Book 3.0 phase 5).
   Home: Continue, Problems due, the unit map, My notes. Lesson reader: progress bar, contents sheet, the header hides while reading,
   margin notes, glossary sheet (Back closes it, the place never moves), highlights and notes, typed problems with worked solutions,
   formulas (KaTeX, our own copy), interactive plots of real TESS light, read-aloud. Everything is saved on this device only.
   Without JavaScript every lesson still reads in full: problems show their solutions behind a fold, links go to the glossary page. */
(() => {
  "use strict";
  const ME = document.currentScript && document.currentScript.src;
  if (!ME) return;
  const BASE = new URL("../", ME);                       // the site root
  const RM = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const get = (k, d) => { try { const v = localStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch (e) { return d; } };
  const set = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* private mode: nothing saved */ } };
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const today = () => new Date().toISOString().slice(0, 10);
  let DATA = null;
  const data = async () => DATA || (DATA = await fetch(new URL("assets/data/learn.json", BASE)).then((r) => r.json()).catch(() => ({ units: [] })));
  const lessons = (d) => d.units.flatMap((u) => u.lessons.map((l) => ({ ...l, unit: u })));

  /* ---------- sheet: one at a time, Back closes it, the page underneath never moves ---------- */
  let open = null;
  const sheet = (title, body, cls = "") => {
    const replacing = !!open;
    close(true);
    const s = el("div", "tw-sheet " + cls), card = el("div", "tw-sheet__card");
    card.setAttribute("role", "dialog"); card.setAttribute("aria-modal", "true"); card.setAttribute("aria-label", title);
    const head = el("div", "tw-sheet__head", `<strong>${esc(title)}</strong>`), x = el("button", "tw-x", "Close");
    x.type = "button"; x.addEventListener("click", () => close());
    head.append(x); card.append(head, body); s.append(card);
    s.addEventListener("click", (e) => { if (e.target === s) close(); });
    const back = document.activeElement, y = scrollY, style = document.body.getAttribute("style");
    const inerted = [...document.body.children].filter(e => !e.inert);
    inerted.forEach(e => e.inert = true);
    Object.assign(document.body.style, { position: "fixed", top: `-${y}px`, width: "100%" });
    document.documentElement.classList.remove("tw-hide");
    document.body.append(s);
    s.restore = () => {
      inerted.forEach(e => e.inert = false);
      if (style == null) document.body.removeAttribute("style"); else document.body.setAttribute("style", style);
      scrollTo(0, y); back?.focus({ preventScroll: true });
    };
    card.addEventListener("keydown", e => {
      if (e.key !== "Tab") return;
      const items = $$('button,a[href],input,select,textarea', card).filter(e => !e.disabled && e.getClientRects().length);
      if (e.shiftKey && document.activeElement === items[0]) { e.preventDefault(); items.at(-1).focus(); }
      else if (!e.shiftKey && document.activeElement === items.at(-1)) { e.preventDefault(); items[0].focus(); }
    });
    requestAnimationFrame(() => s.classList.add("is-open"));
    open = s;
    if (!replacing) history.pushState({ twSheet: 1 }, "");
    setTimeout(() => { if (open === s) (card.querySelector("button:not(.tw-x),a,input,select,textarea") || x).focus({ preventScroll: true }); }, RM ? 0 : 180);
    return card;
  };
  function close(silent) {
    if (!open) return;
    const s = open; open = null;
    s.inert = true;
    s.restore();
    s.classList.remove("is-open");
    setTimeout(() => s.remove(), RM ? 0 : 220);
    if (!silent && history.state && history.state.twSheet) history.back();
  }
  addEventListener("popstate", () => close(true));
  addEventListener("keydown", (e) => { if (e.key === "Escape" && open) close(); });

  /* ---------- formulas ---------- */
  const maths = (root) => {
    if (window.renderMathInElement) {
      try {
        renderMathInElement(root, { delimiters: [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }], throwOnError: false });
      } catch (e) { /* the TeX source stays readable */ }
    }
  };

  /* ---------- text ranges inside one block (used by highlights and read-aloud) ---------- */
  const textNodes = (b) => { const w = document.createTreeWalker(b, NodeFilter.SHOW_TEXT, { acceptNode: (n) => n.parentElement.closest(".katex-mathml") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT }); const out = []; while (w.nextNode()) out.push(w.currentNode); return out; };
  const plain = (b) => textNodes(b).map((n) => n.data).join("");
  const rangeAt = (b, s, e) => {
    const r = document.createRange(); let pos = 0, started = false;
    for (const n of textNodes(b)) {
      const L = n.data.length;
      if (!started && s <= pos + L) { r.setStart(n, Math.max(0, s - pos)); started = true; }
      if (started && e <= pos + L) { r.setEnd(n, Math.max(0, e - pos)); return r; }
      pos += L;
    }
    return started ? (r.setEnd(b, b.childNodes.length), r) : null;
  };
  const offsetIn = (b, node, off) => { let pos = 0; for (const n of textNodes(b)) { if (n === node) return pos + off; pos += n.data.length; } return -1; };

  /* ---------- the plot: real TESS light, touch or hover reads a point ---------- */
  const plot = async (box) => {
    let d;
    try { d = await fetch(new URL(`assets/data/lessons/${box.dataset.src}.json`, BASE)).then((r) => r.json()); } catch (e) { return; }
    const W = Math.max(280, Math.round(box.clientWidth - 30)), H = Math.round(Math.min(320, Math.max(220, W * 0.56))), L = 54, R = 12, T = 14, B = 40;   // one SVG unit = one screen pixel, so text stays at its real size
    // Light curves count days from the first point; other plots (a spectrum, a response curve) set xabs, xlab, read and star (RS-036 course).
    const t0 = d.xabs ? 0 : d.t[0], xs = d.t.map((t) => t - t0), xmin = d.xabs ? Math.min(...xs) : 0;
    const xmax = (d.xabs ? Math.max(...xs) : xs[xs.length - 1]) || 1, lo = Math.min(...d.f), hi = Math.max(...d.f), pad = (hi - lo) * 0.08 || 0.1;
    const y0 = lo - pad, y1 = hi + pad;
    const X = (x) => L + ((x - xmin) / (xmax - xmin || 1)) * (W - L - R), Y = (y) => T + (1 - (y - y0) / (y1 - y0)) * (H - T - B);
    const nice = (span) => { const p = Math.pow(10, Math.floor(Math.log10(span / 4))); return [1, 2, 5, 10].map((m) => m * p).find((s) => span / s <= 6); };
    const ys = nice(y1 - y0), xsStep = nice(xmax - xmin);
    let g = "";
    for (let v = Math.ceil(y0 / ys) * ys; v <= y1; v += ys) g += `<line class="tw-plot__grid" x1="${L}" x2="${W - R}" y1="${Y(v)}" y2="${Y(v)}"/><text class="tw-plot__tick" x="${L - 8}" y="${Y(v) + 4}" text-anchor="end">${+v.toFixed(3)}</text>`;
    for (let v = Math.ceil(xmin / xsStep - 1e-9) * xsStep; v <= xmax + 1e-9; v += xsStep) g += `<text class="tw-plot__tick" x="${X(v)}" y="${H - B + 18}" text-anchor="middle">${+v.toFixed(2)}</text>`;
    const pts = xs.map((x, i) => `<circle cx="${X(x).toFixed(1)}" cy="${Y(d.f[i]).toFixed(1)}" r="1.9"/>`).join("");
    box.innerHTML = `<figure class="tw-plot__fig"><figcaption><strong>${esc(d.title)}</strong> ${esc(d.note)}</figcaption>
      <svg viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.title)}: ${esc(d.y)} against ${esc(d.x)}">${g}
      <text class="tw-plot__lab" x="${(L + W - R) / 2}" y="${H - 4}" text-anchor="middle">${esc(d.xlab || "Days since the first point")}</text>
      <text class="tw-plot__lab" transform="translate(13 ${(T + H - B) / 2}) rotate(-90)" text-anchor="middle">${esc(d.y)}</text>
      <g class="tw-plot__pts">${pts}</g><line class="tw-plot__cross" y1="${T}" y2="${H - B}" x1="-9" x2="-9"/><circle class="tw-plot__dot" r="5" cx="-9" cy="-9"/></svg>
      <p class="tw-plot__read" aria-live="polite">Touch or hover the plot to read a point.</p><p class="tw-plot__src">${esc(d.source)}.${d.star === undefined ? ` Star: TIC ${d.tic}, a published two-sun planet system.` : d.star ? " " + esc(d.star) : ""}</p></figure>`;
    const svg = $("svg", box), cross = $(".tw-plot__cross", box), dot = $(".tw-plot__dot", box), read = $(".tw-plot__read", box);
    const at = (ev) => {
      const r = svg.getBoundingClientRect(), x = ((ev.clientX - r.left) / r.width) * W;
      const want = ((x - L) / (W - L - R)) * xmax;
      let i = 0, best = Infinity;
      xs.forEach((v, k) => { const dd = Math.abs(v - want); if (dd < best) { best = dd; i = k; } });
      cross.setAttribute("x1", X(xs[i])); cross.setAttribute("x2", X(xs[i]));
      dot.setAttribute("cx", X(xs[i])); dot.setAttribute("cy", Y(d.f[i]));
      read.textContent = d.read ? `${d.read.x} ${+xs[i].toFixed(2)} ${d.read.xu}: ${d.read.y} ${+d.f[i].toFixed(3)}${d.read.yu}` : `Day ${xs[i].toFixed(2)}: brightness ${d.f[i] >= 0 ? "+" : ""}${d.unit === "ppm" ? Math.round(d.f[i]) : d.f[i].toFixed(2)}${d.unit === "percent" ? "%" : d.unit === "ppm" ? " ppm" : ""} from normal.`;
    };
    svg.addEventListener("pointermove", at); svg.addEventListener("pointerdown", at);
  };

  /* ---------- problems: typed answer, instant check, a specific hint, the worked solution ---------- */
  const num = (s, unit = "") => {
    let t = String(s).trim().toLowerCase().replace(/\u2212/g, "-");
    const parts = /^([+\-]?[\d.,]+(?:\s*[×x]\s*10\^?[+\-]?\d+|e[+\-]?\d+)?)(?:\s*(.*))?$/.exec(t);
    if (!parts) return null;
    const aliases = { percent: ["percent", "%"], days: ["days", "day", "d"], hours: ["hours", "hour", "h"], years: ["years", "year", "yr"], points: ["points", "point"] };
    const suffix = (parts[2] || "").trim(), expected = unit.toLowerCase();
    if (suffix && !(aliases[expected] || [expected]).includes(suffix)) return null;
    t = parts[1].replace(/\s+/g, "").replace(/[×x]10\^?([+\-]?\d+)/i, "e$1");
    // A single comma with a short fractional part is decimal. Three-digit groups retain the book's thousands notation.
    if (/^[+\-]?(?:\d+,\d{1,2}|0,\d+)(?:e[+\-]?\d+)?$/.test(t)) t = t.replace(",", ".");
    else if (/^[+\-]?\d{1,3}(?:,\d{3})+(?:\.\d+)?(?:e[+\-]?\d+)?$/.test(t)) t = t.replace(/,/g, "");
    else if (t.includes(",")) return null;
    return Number.isFinite(+t) ? +t : null;
  };
  const same = (given, want, tol, abs, unit) => {
    const a = num(given, unit), b = num(want);
    if (a != null && b != null) return Math.abs(a - b) <= Math.max(abs || 0, Math.abs(b) * tol);
    return String(given).trim().toLowerCase().replace(/[.\s]+$/g, "") === String(want).trim().toLowerCase();
  };
  const dueKey = "tw-due";
  const due = () => get(dueKey, []);
  const setDue = (pid, entry) => { const l = due().filter((x) => x.pid !== pid); if (entry) l.push(entry); set(dueKey, l); };
  const problems = (lessonId, title) => {
    $$(".tw-prob").forEach((p, k) => {
      const pid = `${lessonId}-p${k + 1}`, answers = (p.dataset.answer || "").split("|"), tol = p.dataset.tol != null ? +p.dataset.tol : (p.dataset.abs != null ? 0 : 0.02), abs = +(p.dataset.abs || 0);   // an absolute tolerance alone means no relative one (2615.5 was accepted for 2625.3)
      let hints = {}; try { hints = JSON.parse(p.dataset.hints || "{}"); } catch (e) { /* no hints */ }
      p.id = p.id || `prob-${k + 1}`;
      const lab = (($("strong", p) || {}).textContent || "").trim().replace(/\.$/, ""), label = /^\d+$/.test(lab) ? `problem ${lab}` : (lab || `problem ${k + 1}`).toLowerCase();
      p.dataset.label = label;
      const sol = $("details.tw-sol", p);
      const f = el("form", "tw-answer"), inp = el("input"), btn = el("button", "tw-btn", "Check"), fb = el("p", "tw-fb");
      inp.type = "text"; inp.autocomplete = "off"; inp.setAttribute("aria-label", `Your answer to problem ${k + 1}`);
      inp.inputMode = answers.every((a) => num(a) != null && num(a) >= 0) ? "decimal" : "text";
      inp.placeholder = p.dataset.unit ? `Answer in ${p.dataset.unit}` : "Your answer";
      btn.type = "submit"; fb.setAttribute("aria-live", "polite");
      f.append(inp, btn); p.insertBefore(f, sol); p.insertBefore(fb, sol);
      const state = get("tw-prob", {});
      if (state[pid] === "right") { p.classList.add("is-right"); fb.textContent = "You got this one right before."; }
      f.addEventListener("submit", (e) => {
        e.preventDefault();
        const v = inp.value; if (!v.trim()) { fb.textContent = "Type an answer first, or open the worked solution."; return; }
        const s = get("tw-prob", {});
        if (answers.some((a) => same(v, a, tol, abs, p.dataset.unit))) {
          p.classList.remove("is-wrong"); p.classList.add("is-right");
          fb.innerHTML = "<strong>Right.</strong> " + esc(p.dataset.why || "Open the worked solution to compare your steps.");
          s[pid] = "right"; set("tw-prob", s); setDue(pid, null);
          if (sol) sol.open = true;
        } else {
          p.classList.remove("is-right"); p.classList.add("is-wrong");
          const h = Object.keys(hints).find((w) => same(v, w, tol, abs, p.dataset.unit));
          fb.innerHTML = "<strong>Not yet.</strong> " + esc(h ? hints[h] : "Try once more, or open the worked solution and follow each step.");
          s[pid] = "wrong"; set("tw-prob", s);
          setDue(pid, { pid, lesson: lessonId, title, url: location.pathname.replace(/[^/]*$/, ""), n: k + 1, label, at: today() });
        }
      });
    });
  };

  /* ---------- glossary words open a sheet; the page stays where it is ---------- */
  let GLOSS = null;
  const glossary = () => {
    document.addEventListener("click", async (e) => {
      const a = e.target.closest && e.target.closest('.md-typeset a[href*="glossary/#"]');
      if (!a || e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      e.preventDefault(); e.stopImmediatePropagation();
      if (!GLOSS) { try { GLOSS = await fetch(new URL("assets/glossary.json", BASE)).then((r) => r.json()); } catch (err) { GLOSS = {}; } }
      const hit = GLOSS[decodeURIComponent(a.hash.slice(1))];
      if (!hit) { location.href = a.href; return; }
      const body = el("div", "tw-sheet__body", `<p>${esc(hit[1])}</p><p><a href="${esc(a.href)}">Open the full glossary</a></p>`);
      sheet(hit[0], body, "tw-sheet--word");
    }, true);
  };

  /* ---------- highlights and notes (this device) ---------- */
  const HLK = "tw-hl";
  const blocksOf = (art) => $$(":scope > p, :scope > ul > li, :scope > ol > li, .admonition > p, .tw-mn > p", art).filter((b) => !b.closest(".tw-pn,.tw-kicker,.tw-prob form,.tw-plot"));
  const highlights = (art, lessonId, title) => {
    const blocks = blocksOf(art), key = location.pathname;
    const all = () => get(HLK, {}), mine = () => all()[key] || [];
    const save = (list) => { const a = all(); if (list.length) a[key] = list; else delete a[key]; set(HLK, a); };
    const paint = () => {
      $$("mark.tw-hl", art).forEach((m) => m.replaceWith(...m.childNodes));
      blocks.forEach((b) => b.normalize());
      mine().forEach((h, i) => {
        const b = blocks[h.b]; if (!b || plain(b).slice(h.s, h.e) !== h.text) return;     // the lesson changed: kept in My notes, not drawn
        const r = rangeAt(b, h.s, h.e); if (!r) return;
        try { const m = el("mark", "tw-hl" + (h.note ? " has-note" : "")); m.dataset.i = i; m.append(r.extractContents()); r.insertNode(m); } catch (e) { /* spans an element edge: skip */ }
      });
    };
    paint();
    const pill = el("div", "tw-pill"); pill.hidden = true;
    pill.innerHTML = '<button type="button" data-a="hl">Highlight</button><button type="button" data-a="note">Add a note</button>';
    document.body.append(pill);
    let pend = null;
    const where = () => {
      const s = getSelection(); if (!s.rangeCount || s.isCollapsed) { pill.hidden = true; pend = null; return; }
      const r = s.getRangeAt(0), b = blocks.find((x) => x.contains(r.startContainer) && x.contains(r.endContainer));
      if (!b || r.startContainer.nodeType !== 3 || r.endContainer.nodeType !== 3) { pill.hidden = true; pend = null; return; }
      const st = offsetIn(b, r.startContainer, r.startOffset), en = offsetIn(b, r.endContainer, r.endOffset);
      if (st < 0 || en <= st) { pill.hidden = true; return; }
      pend = { b: blocks.indexOf(b), s: st, e: en, text: plain(b).slice(st, en) };
      const box = r.getBoundingClientRect();
      pill.hidden = false;
      pill.style.top = `${Math.max(8, box.top + scrollY - 48)}px`;
      pill.style.left = `${Math.min(innerWidth - 220, Math.max(8, box.left + box.width / 2 - 100))}px`;
    };
    document.addEventListener("selectionchange", () => { clearTimeout(where.t); where.t = setTimeout(where, 250); });
    const add = (note, selection = pend) => { if (!selection) return; const l = mine(); l.push({ ...selection, note: note || "", lesson: lessonId, title, at: today() }); save(l); pend = null; getSelection().removeAllRanges(); pill.hidden = true; paint(); };
    const noteSheet = (h, i) => {
      const selection = pend && { ...pend };
      const body = el("div", "tw-sheet__body");
      body.innerHTML = `<blockquote>${esc(h ? h.text : pend.text)}</blockquote><label class="tw-lab" for="tw-note">Your note</label><textarea id="tw-note" rows="4"></textarea><div class="tw-row"><button type="button" class="tw-btn" data-a="save">Save</button>${h ? '<button type="button" class="tw-btn tw-btn--quiet" data-a="del">Remove highlight</button>' : ""}</div>`;
      $("textarea", body).value = h ? h.note : "";
      const card = sheet(h ? "Your highlight" : "Add a note", body);
      $("textarea", card).focus({ preventScroll: true });
      body.addEventListener("click", (e) => {
        const a = e.target.dataset.a; if (!a) return;
        if (a === "save") { const v = $("textarea", body).value.trim(); if (h) { const l = mine(); l[i].note = v; save(l); paint(); } else add(v, selection); close(); }
        if (a === "del") { const l = mine(); l.splice(i, 1); save(l); paint(); close(); }
      });
    };
    pill.addEventListener("pointerdown", (e) => e.preventDefault());               // keep the selection while tapping
    pill.addEventListener("click", (e) => { const a = e.target.dataset.a; if (a === "hl") add(""); if (a === "note" && pend) noteSheet(null); });
    art.addEventListener("click", (e) => { const m = e.target.closest("mark.tw-hl"); if (m && getSelection().isCollapsed) noteSheet(mine()[+m.dataset.i], +m.dataset.i); });
    const m = location.hash.match(/^#twb=(\d+)$/);                                   // from My notes: go to that paragraph
    if (m && blocks[+m[1]]) { const b = blocks[+m[1]]; setTimeout(() => { b.scrollIntoView({ block: "center" }); b.classList.add("tw-flash"); }, 60); }
    return blocks;
  };

  /* ---------- read aloud ---------- */
  const TEX = [[/\\frac\{([^{}]+)\}\{([^{}]+)\}/g, "$1 over $2"], [/\\sqrt\[3\]\{([^{}]+)\}/g, "the cube root of $1"], [/\\sqrt\{([^{}]+)\}/g, "the square root of $1"], [/\^\{?2\}?/g, " squared"], [/\^\{?3\}?/g, " cubed"],
    [/\^\{([^{}]+)\}/g, " to the power $1"], [/\^(\w)/g, " to the power $1"], [/_\{([^{}]+)\}/g, " $1"], [/_(\w)/g, " $1"], [/\\times/g, " times "], [/\\cdot/g, " times "],
    [/\\approx/g, " is about "], [/\\Delta\s*/g, "delta "], [/\\pi/g, "pi"], [/\\text\{([^{}]+)\}/g, "$1"], [/\\mathrm\{([^{}]+)\}/g, "$1"], [/=/g, " equals "], [/\\%/g, " percent"],
    [/-/g, " minus "], [/\+/g, " plus "], [/[{}\\]/g, " "]];
  const say = (tex) => TEX.reduce((s, [a, b]) => s.replace(a, b), tex).replace(/\s+/g, " ").trim();
  const speakText = (b) => {
    const c = b.cloneNode(true);
    $$(".katex", c).forEach((k) => { const a = $('annotation[encoding="application/x-tex"]', k); k.replaceWith(" " + (a ? say(a.textContent) : k.textContent) + " "); });
    $$(".katex-display", c).forEach((k) => k.replaceWith(" " + k.textContent + " "));
    return c.textContent.replace(/\s+/g, " ").trim();
  };
  const listen = (art) => {
    if (!("speechSynthesis" in window)) return null;
    const S = speechSynthesis;
    const blocks = $$(":scope > h1, :scope > h2, :scope > h3, :scope > p, :scope > ul > li, :scope > ol > li, .admonition > p, .admonition-title, .tw-mn > p, :scope > .arithmatex", art)
      .filter((b) => !b.closest(".tw-pn,.tw-kicker,.tw-plot,.tw-sol,form") && b.textContent.trim());
    let idx = -1, on = false, timer = null, hl = null;
    const voices = () => S.getVoices().filter((v) => /^en/i.test(v.lang));
    const pickVoice = () => { const name = get("tw-voice", ""), vs = voices(); return vs.find((v) => v.name === name) || vs.find((v) => v.default) || vs[0] || null; };
    const mark = (b, s, e) => {
      $$(".tw-speaking").forEach((x) => x.classList.remove("tw-speaking"));
      b.classList.add("tw-speaking");
      if (window.CSS && CSS.highlights && s != null && !b.querySelector(".katex")) { const r = rangeAt(b, s, e); if (r) { hl = new Highlight(r); CSS.highlights.set("tw-say", hl); } }
      else if (window.CSS && CSS.highlights) CSS.highlights.delete("tw-say");
    };
    const stop = () => { on = false; S.cancel(); clearTimeout(timer); $$(".tw-speaking").forEach((x) => x.classList.remove("tw-speaking")); if (window.CSS && CSS.highlights) CSS.highlights.delete("tw-say"); ui(); };
    const playFrom = (i) => {
      S.cancel(); on = true; idx = i; ui();
      const next = () => {
        if (!on) return;
        if (idx >= blocks.length) { stop(); return; }
        const b = blocks[idx], txt = speakText(b), hasMath = !!b.querySelector(".katex");
        b.scrollIntoView({ block: "center", behavior: RM ? "auto" : "smooth" });
        const parts = hasMath ? [[txt, null, null]] : (() => { const p = plain(b), out = []; const rx = /[^.!?]+[.!?]*["')\]]*\s*/g; let m; while ((m = rx.exec(p))) if (m[0].trim()) out.push([m[0], m.index, m.index + m[0].trimEnd().length]); return out.length ? out : [[p, 0, p.length]]; })();
        let j = 0;
        const one = () => {
          if (!on) return;
          if (j >= parts.length) { idx++; next(); return; }
          const [t, s, e] = parts[j++];
          const u = new SpeechSynthesisUtterance(t), v = pickVoice();
          if (v) u.voice = v;
          u.rate = get("tw-rate", 1);
          u.onstart = () => mark(b, s, e);
          u.onend = one; u.onerror = (ev) => { if (ev.error !== "interrupted" && ev.error !== "canceled") one(); };
          S.speak(u);
        };
        one();
      };
      next();
    };
    let bar = null;
    const ui = () => { if (bar) { $("[data-a=play]", bar).textContent = on ? "Pause" : "Play"; bar.classList.toggle("is-on", on); } };
    const panel = () => {
      const body = el("div", "tw-sheet__body tw-listen");
      const vs = voices();
      body.innerHTML = `<p class="tw-quiet">Reads the lesson aloud and follows along. While it plays, tap any paragraph to jump there.</p>
        <div class="tw-row"><button type="button" class="tw-btn" data-a="play">${on ? "Pause" : "Play"}</button><button type="button" class="tw-btn tw-btn--quiet" data-a="top">From the top</button></div>
        <label class="tw-lab" for="tw-voice">Voice</label><select id="tw-voice">${vs.map((v) => `<option${pickVoice() && v.name === pickVoice().name ? " selected" : ""}>${esc(v.name)}</option>`).join("") || "<option>System voice</option>"}</select>
        <label class="tw-lab" for="tw-rate">Speed <output>${get("tw-rate", 1)}×</output></label><input id="tw-rate" type="range" min="0.6" max="1.8" step="0.1" value="${get("tw-rate", 1)}">
        <label class="tw-lab" for="tw-sleep">Sleep timer</label><select id="tw-sleep"><option value="0">Off</option><option value="10">10 minutes</option><option value="20">20 minutes</option><option value="30">30 minutes</option><option value="45">45 minutes</option></select>`;
      bar = sheet("Listen", body, "tw-sheet--listen");
      body.addEventListener("click", (e) => {
        const a = e.target.dataset.a;
        if (a === "play") { if (on) stop(); else playFrom(Math.max(0, idx)); }
        if (a === "top") playFrom(0);
      });
      $("#tw-voice", body).addEventListener("change", (e) => { set("tw-voice", e.target.value); if (on) playFrom(idx); });
      $("#tw-rate", body).addEventListener("input", (e) => { set("tw-rate", +e.target.value); $("output", body).textContent = `${e.target.value}×`; });
      $("#tw-rate", body).addEventListener("change", () => { if (on) playFrom(idx); });
      $("#tw-sleep", body).addEventListener("change", (e) => { clearTimeout(timer); if (+e.target.value) timer = setTimeout(stop, +e.target.value * 60000); });
    };
    art.addEventListener("click", (e) => {
      if (!on || e.target.closest("a,button,input,mark,summary,.tw-plot")) return;
      const i = blocks.findIndex((b) => b.contains(e.target)); if (i >= 0) playFrom(i);
    });
    addEventListener("pagehide", () => S.cancel());
    S.onvoiceschanged = () => {};
    return { panel, stop };
  };

  /* ---------- the lesson page ---------- */
  const lesson = async (kick) => {
    const id = kick.dataset.lesson, art = $("article.md-content__inner") || $(".md-content__inner");
    const title = (($("h1", art) || {}).textContent || id).replace(/¶/g, "").trim();
    document.documentElement.classList.add("tw-reading");
    maths(art);
    const plotsReady = Promise.all($$(".tw-plot[data-src]").map(plot));
    let rw = innerWidth, rt = 0;
    addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (Math.abs(innerWidth - rw) > 40) { rw = innerWidth; $$(".tw-plot[data-src]").forEach(plot); } }, 300); });
    problems(id, title);
    glossary();
    highlights(art, id, title);
    const voice = listen(art);
    // progress bar, place saving, header hiding
    const bar = el("div", "tw-bar", "<i></i>"); document.body.append(bar);
    const fill = $("i", bar);
    let lastY = scrollY, saveT = 0;
    const onScroll = () => {
      if (open) return;
      const max = document.documentElement.scrollHeight - innerHeight, f = max > 0 ? Math.min(1, scrollY / max) : 1;
      fill.style.transform = `scaleX(${f})`;
      if (scrollY > 80 && scrollY > lastY + 2 && !open) document.documentElement.classList.add("tw-hide");
      if (scrollY < lastY - 6 || scrollY < 80) document.documentElement.classList.remove("tw-hide");
      lastY = scrollY;
      const px = scrollY;
      clearTimeout(saveT); saveT = setTimeout(() => set("tw-place", { id, title, url: location.pathname, y: f, px, width: innerWidth, at: Date.now() }), 400);
    };
    const savedPlace = get("tw-place", null);
    await plotsReady;
    await document.fonts.ready;
    await Promise.all($$("img", art).map(img => img.decode().catch(() => {})));
    const edge = el("button", "tw-edge"); edge.type = "button"; edge.setAttribute("aria-label", "Show the menu");
    edge.addEventListener("click", () => document.documentElement.classList.remove("tw-hide")); document.body.append(edge);
    // resume at the exact place when opened from Continue
    try {
      if (sessionStorage.getItem("tw-resume") === location.pathname) {
        sessionStorage.removeItem("tw-resume");
        const p = savedPlace;
        if (p && p.url === location.pathname) {
          if (document.readyState !== "complete") await new Promise(resolve => addEventListener("load", resolve, { once: true }));
          await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
          const y = p.width === innerWidth && Number.isFinite(p.px) ? p.px : p.y * (document.documentElement.scrollHeight - innerHeight);
          scrollTo(0, y);
        }
      }
    } catch (e) { /* storage blocked */ }
    lastY = scrollY;
    addEventListener("scroll", onScroll, { passive: true }); onScroll();
    // finished: the end links come into view (checked on scroll; no IntersectionObserver, which some hidden or old views never fire)
    const end = $(".tw-pn");
    let finished = false;
    const finish = () => {
      if (finished || !end || end.getBoundingClientRect().top > innerHeight - 40) return;
      finished = true;
      const d = get("tw-done", {}); if (!d[id]) { d[id] = today(); set("tw-done", d); }
      const st = get("tw-prob", {});
      $$(".tw-prob").forEach((p, k) => { const pid = `${id}-p${k + 1}`; if (st[pid] !== "right" && !due().some((x) => x.pid === pid)) setDue(pid, { pid, lesson: id, title, url: location.pathname, n: k + 1, label: p.dataset.label, at: today() }); });
    };
    addEventListener("scroll", () => { clearTimeout(finish.t); finish.t = setTimeout(finish, 300); }, { passive: true });
    // the reader's tools
    const tools = el("div", "tw-tools");
    tools.innerHTML = `<button type="button" data-a="toc" aria-label="Contents">Contents</button>${voice ? '<button type="button" data-a="listen">Listen</button>' : ""}<a href="${new URL("learn/", BASE).pathname}">Home</a>`;
    document.body.append(tools);
    tools.addEventListener("click", async (e) => {
      const a = e.target.dataset.a;
      if (a === "listen" && voice) voice.panel();
      if (a === "toc") {
        const d = await data(), done = get("tw-done", {}), body = el("div", "tw-sheet__body tw-toc");
        const hs = $$("h2[id]", art);
        body.innerHTML = (hs.length ? `<p class="tw-lab">In this lesson</p><ul class="tw-toc__here">${hs.map((h) => `<li><a href="#${h.id}">${esc(h.textContent.replace(/¶$/, ""))}</a></li>`).join("")}</ul>` : "") +
          d.units.map((u) => `<p class="tw-lab">Unit ${u.n} · ${esc(u.title)}</p><ul>${u.lessons.map((l) => l.url
            ? `<li class="${l.id === id ? "is-here" : ""}"><a href="${new URL(l.url, BASE).pathname}">${l.id} ${esc(l.title)}</a>${done[l.id] ? ' <span class="tw-tick" aria-label="done">✓</span>' : ""}</li>`
            : `<li class="is-soon">${l.id} ${esc(l.title)} <small>coming</small></li>`).join("")}</ul>`).join("");
        sheet("Contents", body, "tw-sheet--side");
        body.addEventListener("click", (ev) => { const l = ev.target.closest('a[href^="#"]'); if (l) { ev.preventDefault(); close(); setTimeout(() => $(l.getAttribute("href")).scrollIntoView({ behavior: RM ? "auto" : "smooth" }), 240); } });
      }
    });
  };

  /* ---------- the home screen ---------- */
  const home = async (root) => {
    const d = await data(), all = lessons(d), live = all.filter((l) => l.url), done = get("tw-done", {}), place = get("tw-place", null), hl = get(HLK, {});
    const dueL = due().sort((a, b) => a.lesson.localeCompare(b.lesson, undefined, { numeric: true }) || a.n - b.n);
    const url = (l) => new URL(l.url, BASE).pathname;
    const stopped = place && live.find((l) => l.id === place.id && !(done[l.id] && place.y > 0.9));
    const cont = stopped || live.find((l) => !done[l.id]) || live[0];
    const nDone = live.filter((l) => done[l.id]).length;
    const notes = Object.entries(hl).flatMap(([u, list]) => list.map((h) => ({ ...h, url: u })));
    let h = "";
    if (cont) {
      const started = !!stopped && stopped.id === cont.id;
      h += `<a class="tw-continue" href="${url(cont)}" data-resume="${started ? url(cont) : ""}"><small>${started ? "Continue where you stopped" : nDone ? "Next lesson" : "Start here"}</small><strong>${cont.id} ${esc(cont.title)}</strong>
        <span class="tw-continue__meta">Unit ${cont.unit.n} · ${esc(cont.unit.title)}${cont.minutes ? ` · ${cont.minutes} min` : ""}</span>${started ? `<span class="tw-continue__bar"><i style="transform:scaleX(${Math.max(0.03, place.y)})"></i></span>` : ""}</a>`;
    }
    h += `<div class="tw-stats"><div><strong>${nDone}</strong><span>of ${live.length} lessons read</span></div><div><strong>${dueL.length}</strong><span>problems due</span></div><div><strong>${notes.length}</strong><span>highlights and notes</span></div></div>`;
    if (dueL.length) h += `<h2>Problems due</h2><p class="tw-quiet">Ones you missed or skipped. Try them again a day or two later: that is when practice does the most.</p><ul class="tw-due">${dueL.map((x) => `<li><a href="${esc(x.url)}#prob-${x.n}">${esc(x.lesson)} ${esc(x.title)}, ${esc(x.label || "problem " + x.n)}</a></li>`).join("")}</ul>`;
    h += `<h2>The units</h2><div class="tw-units">${d.units.map((u) => {
      const ls = u.lessons, got = ls.filter((l) => done[l.id]).length, any = ls.some((l) => l.url);
      return `<section class="tw-unit${any ? "" : " is-soon"}"><header><span class="tw-unit__n">${u.n}</span><div><strong>${esc(u.title)}</strong><small>${any ? `${got} of ${ls.length} read` : "coming"}</small></div></header><ol>${ls.map((l) => l.url
        ? `<li class="${done[l.id] ? "is-done" : ""}"><a href="${url(l)}">${esc(l.title)}</a>${done[l.id] ? '<span class="tw-tick" aria-label="read">✓</span>' : ""}</li>`
        : `<li class="is-soon">${esc(l.title)}</li>`).join("")}</ol></section>`;
    }).join("")}</div>`;
    if (notes.length) h += `<h2>My notes</h2><ul class="tw-notes">${notes.map((n) => `<li><a href="${esc(n.url)}#twb=${n.b}"><small>${esc(n.lesson)} ${esc(n.title)}</small><span class="tw-notes__q">${esc(n.text)}</span>${n.note ? `<span class="tw-notes__n">${esc(n.note)}</span>` : ""}</a></li>`).join("")}</ul>`;
    h += `<p class="tw-quiet tw-device">Your place, problems and notes are saved on this device only.</p>`;
    root.innerHTML = h;
    root.classList.add("is-ready");
    $$(".tw-units .tw-unit", root).forEach((s, i) => (s.style.animationDelay = `${Math.min(i, 6) * 45}ms`));
    root.addEventListener("click", (e) => { const a = e.target.closest("[data-resume]"); if (a && a.dataset.resume) { try { sessionStorage.setItem("tw-resume", a.dataset.resume); } catch (err) { /* fine */ } } });
  };

  const start = () => {
    const kick = $(".tw-kicker[data-lesson]"), root = $("#tw-home");
    if (kick) lesson(kick);
    else if (root) home(root);
  };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
