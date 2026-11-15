/* Tree design A, rendered from the build-time Tree data. */
(() => {
  "use strict";
  const host = document.getElementById("ss-tree");
  if (!host) return;
  const WIDE = matchMedia("(min-width:900px)");
  const esc = s => String(s ?? "").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[c]);
  const S = {
    get(key) {
      try { return localStorage.getItem(key); }
      catch { return null; }
    },
    set(key, value) {
      try { localStorage.setItem(key, value); }
      catch { /* Storage can be unavailable in private browsing. */ }
    },
  };
  const NS = "http://www.w3.org/2000/svg";
  const el = (tag, attributes, parent) => {
    const element = document.createElementNS(NS, tag);
    for (const key in attributes) element.setAttribute(key, attributes[key]);
    if (parent) parent.append(element);
    return element;
  };
  const fmt = iso => iso ? new Date(iso.length>10?iso:iso+"T12:00").toLocaleDateString(undefined,{day:"numeric",month:"short",year:"numeric"}) : "";
  const stat = s => `<span class="ssta-st ssta-status">${esc(s)}</span>`;
  let D, nodes={}, leaves={}, view=S.get("sst-view")==="journey"?"journey":"mission", chosen="1", query="", showNew=false;
  let openState=null, restoring=false, returnFocus=null;
  const expanded={"1":true,"2":true,"3":true,"4":true}, newIds=new Set();
  fetch(host.dataset.src, { cache: "no-cache" })
    .then(response => {
      if (!response.ok) throw Error(response.status);
      return response.json();
    })
    .then(start)
    .catch(() => {
      host.classList.add("sst-failed");
      host.querySelector(".ssta-page")?.remove();
      host.querySelector(".sst-static")?.removeAttribute("hidden");
    });

  function start(data) {
    D=data; D.nodes.forEach(n=>nodes[n.id]=n);D.leaves.forEach(l=>leaves[l.id]=l);
    const last=S.get("sst-last-visit");if(last)D.leaves.forEach(l=>{if((l.when||"")>last)newIds.add(l.id);});
    host.querySelector(".sst-static")?.setAttribute("hidden","");host.classList.add("sst");
    host.insertAdjacentHTML("afterbegin",`<div class="ssta-page"><div class="ssta-top"><h1>The Tree</h1><nav><a href="field-notes/">Field notes &#8250;</a><a href="watch/">Search window &#8250;</a></nav></div>${D.now?`<p class="sst-now"><b>Now:</b> ${esc(D.now.replace(/^Now\s*(\([^)]*\))?:\s*/, "$1 ").trim())}</p>`:""}
      <div class="sst-bar"><div class="sst-seg" role="group" aria-label="Tree view"><button type="button" data-view="mission">Mission</button><button type="button" data-view="journey">Journey</button></div>
      <label class="sst-search"><input type="search" placeholder="Search the Tree" aria-label="Search the Tree" autocomplete="off" enterkeyhint="search"></label>
      ${newIds.size?`<button type="button" class="sst-new" aria-pressed="false"><b>${newIds.size}</b> new</button><button type="button" class="sst-read" hidden>Mark updates read</button>`:""}</div>
      <p class="sst-results" role="status" hidden>No matches</p><div class="sst-view"></div></div>`);
    host.addEventListener("click",onClick);
    const input=host.querySelector(".sst-search input");
    input.addEventListener("input",()=>{query=input.value.trim().toLowerCase();applyFilter();});
    input.addEventListener("keydown",e=>{
      if(e.key==="Escape"){input.value="";query="";applyFilter();}
      if(e.key!=="Enter")return;
      e.preventDefault();query=input.value.trim().toLowerCase();const m=applyFilter();if(!query)return;
      const id=m?.direct.values().next().value || m?.nn.values().next().value;
      if(id){if(id.includes("."))chosen=id.split(".")[0];if(view!=="mission"){view="mission";S.set("sst-view",view);}render();openNode(id);}
      else if(m?.ln.size)openLeaf(m.ln.values().next().value);
    });
    if(!last)S.set("sst-last-visit",D.generated);
    render();
    WIDE.addEventListener("change",()=>{const key=openState?.key;removeCard();render();if(key)restore(key);});
    addEventListener("resize",drawLayout);
    // Font metrics can change card heights after the first layout.
    document.fonts?.ready.then(drawLayout);
    const observer=new ResizeObserver(()=>requestAnimationFrame(drawLayout));observer.observe(host.querySelector(".sst-view"));
    addEventListener("popstate",()=>{removeCard();const key=history.state?.sst || hashKey();if(key)restore(key);});
    addEventListener("hashchange",()=>{const key=hashKey();if(key!==openState?.key){removeCard();if(key)restore(key);}});
    addEventListener("keydown",e=>{if(e.key==="Escape"&&openState)closeCard();});
    const key=hashKey();if(key)restore(key);
  }
  function hashKey() {
    const match = /^#([nl])=(.+)$/.exec(location.hash);
    if (!match) return null;
    try { return match[1] + ":" + decodeURIComponent(match[2]); }
    catch { return null; }
  }

  function onClick(event) {
    const viewButton = event.target.closest("[data-view]");
    if (viewButton) {
      if (view === viewButton.dataset.view) return;
      removeCard();
      clearHash();
      view = viewButton.dataset.view;
      S.set("sst-view", view);
      render();
      return;
    }
    const branchButton = event.target.closest("[data-pb]");
    if (branchButton) {
      chosen = branchButton.dataset.pb;
      render();
      host.querySelector(".ssta-phrows").scrollIntoView({ block: "nearest" });
      return;
    }
    const toggle = event.target.closest("[data-toggle]");
    if (toggle) {
      expanded[toggle.dataset.toggle] = !expanded[toggle.dataset.toggle];
      render();
      return;
    }
    const nodeButton = event.target.closest("[data-node]");
    if (nodeButton) {
      event.preventDefault();
      openNode(nodeButton.dataset.node);
      return;
    }
    const leafButton = event.target.closest("[data-leaf]");
    if (leafButton) {
      event.preventDefault();
      openLeaf(leafButton.dataset.leaf);
      return;
    }
    if (event.target.closest(".sst-new")) {
      showNew = !showNew;
      host.querySelector(".sst-new").setAttribute("aria-pressed", String(showNew));
      host.querySelector(".sst-read").hidden = !showNew;
      applyFilter();
    }
    if (event.target.closest(".sst-read")) {
      S.set("sst-last-visit", D.generated);
      newIds.clear();
      showNew = false;
      host.querySelector(".sst-new").remove();
      host.querySelector(".sst-read").remove();
      applyFilter();
    }
  }

  function filters() {
    if (!query && !showNew) return null;
    const leafMatches = new Set(), nodeMatches = new Set(), direct = new Set();
    D.leaves.forEach(leaf => {
      const text = [leaf.plain, leaf.why, leaf.explanation, leaf.technical, ...(leaf.ids || [])].join(" ").toLowerCase();
      if ((!query || text.includes(query)) && (!showNew || newIds.has(leaf.id))) {
        leafMatches.add(leaf.id);
        nodeMatches.add(leaf.node);
        (leaf.also || []).forEach(id => nodeMatches.add(id));
      }
    });
    if (query && !showNew) {
      D.nodes.forEach(node => {
        const text = [node.id, node.title, node.sub, node.plain, node.status_text].join(" ").toLowerCase();
        if (text.includes(query)) {
          direct.add(node.id);
          nodeMatches.add(node.id);
        }
      });
    }
    [...nodeMatches].forEach(id => {
      if (nodes[id]?.parent in nodes) nodeMatches.add(nodes[id].parent);
    });
    return { ln: leafMatches, nn: nodeMatches, direct };
  }

  function applyFilter() {
    const matches = filters();
    host.querySelector(".sst-results").hidden = !matches || !!(matches.nn.size || matches.ln.size);
    host.querySelectorAll("[data-node]").forEach(element => {
      element.classList.toggle("is-dim", !!matches && !matches.nn.has(element.dataset.node));
      element.classList.toggle("is-match", !!matches && matches.nn.has(element.dataset.node));
    });
    host.querySelectorAll(".sst-day").forEach(day => {
      day.hidden = !!matches && ![...day.querySelectorAll("[data-leaf]")].some(leaf => matches.ln.has(leaf.dataset.leaf));
    });
    return matches;
  }

  function goalHTML(){return `<div class="ssta-goal ssta-box"><span class="ssta-eyebrow">Goal</span><h2>${esc(D.goal.tree.split(/\.\s/)[0].replace(/\.$/,""))}.</h2></div>`;}
  function scoreHTML(){const b=D.bench;return `<div class="ssta-score ssta-box"><span class="ssta-eyebrow">Petrova scoreboard</span><p>${esc(b.label)} catches ${Math.round(b.rate)}% of Saturn-like test planets.</p><div class="ssta-meter" role="img" aria-label="${b.rate} percent, range ${b.lower} to ${b.upper} percent"><i style="width:${b.rate}%"></i><b style="left:${b.lower}%;width:${b.upper-b.lower}%"></b><u style="left:${b.rate}%"></u></div><div class="ssta-foot"><span class="ssta-mono">Range ${Math.round(b.lower)} to ${Math.round(b.upper)}%</span><strong>${esc(b.verdict)}</strong></div></div>`;}
  function chipsHTML(){return `<div class="ssta-chips">${[D.path.active,D.path.next].map((p,i)=>{if(!p)return "";const title=nodes[p.id]?.title||p.title;return `${i?'<span class="ssta-dash" aria-hidden="true"></span>':""}<button type="button" class="ssta-chip ssta-box" ${p.id?`data-node="${esc(p.id)}"`:"disabled"} title="${esc(p.title)}"><span class="ssta-dot ${i?"":"ssta-on"}" aria-hidden="true"></span><span><b>${esc(title)}</b>${stat(i?"NEXT":"ACTIVE")}</span><span class="ssta-chev" aria-hidden="true">&#8250;</span></button>`;}).join("")}</div>`;}
  function rowHTML(id){const n=nodes[id];return `<li><button type="button" class="ssta-row sst-item" data-node="${id}" aria-current="${openState?.key==="n:"+id}"><span class="ssta-id">${id}</span><span class="ssta-t t">${esc(n.title)}${n.sub?`<small>${esc(n.sub)}</small>`:""}</span><span class="ssta-loss">${n.loss?n.loss.count:""}</span>${stat(n.status)}<span class="ssta-chev" aria-hidden="true">&#8250;</span></button></li>`;}
  function branchHTML(id){const n=nodes[id];return `<section class="ssta-br ssta-box" data-branch="${id}"><button type="button" class="ssta-br-h" data-toggle="${id}" aria-expanded="${expanded[id]}"><span class="ssta-n">${id}</span><span><h3>${esc(n.title)}</h3><p>${esc(n.sub)}</p></span>${stat(n.status)}<span class="ssta-tog" aria-hidden="true">${expanded[id]?"−":"+"}</span></button>${expanded[id]?`<ul class="ssta-rows">${n.children.map(rowHTML).join("")}</ul>`:""}</section>`;}
  function render(){
    host.querySelectorAll("[data-view]").forEach(b=>b.setAttribute("aria-pressed",String(b.dataset.view===view)));
    const v=host.querySelector(".sst-view");
    let html;
    if(view==="journey")html=journeyHTML();
    else html=`<div class="ssta-mission"><svg class="ssta-vine" aria-hidden="true"></svg><div class="ssta-pc-head">${goalHTML()}${scoreHTML()}</div>${chipsHTML()}${WIDE.matches?`<div class="ssta-pc-tree"><div class="ssta-colL">${["1","4"].map(branchHTML).join("")}</div><div class="ssta-colR">${["2","3"].map(branchHTML).join("")}</div></div>`:`<div class="ssta-phtree"><svg class="ssta-vine" aria-hidden="true"></svg>${["1","2","3","4"].map((id,i)=>`<button type="button" class="ssta-phcard ssta-box ${i%2?"ssta-r":"ssta-l"}" data-pb="${id}" aria-expanded="${chosen===id}"><h3>${esc(nodes[id].title)}</h3><span class="ssta-tog" aria-hidden="true">${chosen===id?"−":"+"}</span>${stat(nodes[id].status)}${id==="2"?`<p>${esc(nodes[id].sub)}</p>`:""}</button>`).join("")}</div><section class="ssta-phrows ssta-br ssta-box"><div class="ssta-br-h"><h3>${esc(nodes[chosen].title)}</h3><p>${esc(nodes[chosen].sub)}</p></div><ul class="ssta-rows">${nodes[chosen].children.map(rowHTML).join("")}</ul></section>`}</div>`;
    // Keep an existing desktop panel alive while expanding a branch.
    const card=openState?.card&&!openState.restore?openState.card:null;
    v.innerHTML=`<div class="ssta-pc-cols"><div class="ssta-main">${html}</div><aside class="ssta-detail-slot" aria-label="Node details"></aside></div>`;
    if(card)host.querySelector(".ssta-detail-slot").append(card);
    applyFilter();requestAnimationFrame(drawLayout);
  }
  function journeyHTML(){
    const phases=D.phases.slice().sort((a,b)=>b.from.localeCompare(a.from));
    const days=D.days.slice().sort((a,b)=>b.date.localeCompare(a.date));
    return `<div class="sst-journey">${phases.map((p,i)=>`<section class="sst-phase"><h2>${esc(p.title)}</h2><p>${esc(p.plain)}</p><small>From ${esc(fmt(p.from))}</small></section>${days.filter(d=>d.date>=p.from&&d.date<(i?phases[i-1].from:"9999")).map(d=>`<section class="sst-day" data-date="${d.date}"><h3>${esc(fmt(d.date))}</h3><div class="sst-dl">${d.diary?`<a class="sst-diary" href="${esc(d.diary)}">Diary entry for this day</a>`:""}${d.leaves.slice().reverse().map(id=>`<button type="button" data-leaf="${esc(id)}">${esc(leaves[id].plain)}</button>`).join("")}</div></section>`).join("")}`).join("")}</div>`;
  }
  function drawLayout(){
    const mission=host.querySelector(".ssta-mission");if(!mission)return;
    const outer=mission.querySelector(":scope > .ssta-vine");
    if(!WIDE.matches){outer.innerHTML="";outer.setAttribute("width",0);outer.setAttribute("height",0);placePhone();return;}
    const o=mission.getBoundingClientRect(),tree=mission.querySelector(".ssta-pc-tree"),goal=mission.querySelector(".ssta-goal").getBoundingClientRect();
    outer.setAttribute("width",o.width);outer.setAttribute("height",o.height);
    if(!tree)return;
    const cards=[...tree.querySelectorAll(".ssta-br")];const lowest=Math.max(...cards.map(b=>b.getBoundingClientRect().bottom-o.top));
    const targets=cards.map(b=>{const r=b.getBoundingClientRect(),y=r.top-o.top+34;return {x:b.closest(".ssta-colL")?r.right-o.left:r.left-o.left,y,join:y+58};});
    drawVine(outer,{cx:o.width/2,top:goal.bottom-o.top,bottom:lowest+50,targets,k:Math.min(1,o.width/800),twigs:[[.33,-1,40],[.55,1,40],[.75,-1,40]]});
  }
  function placePhone(){
    const box=host.querySelector(".ssta-phtree");if(!box)return;
    const cards=[...box.querySelectorAll(".ssta-phcard")],bottom={l:0,r:0};let prev=0,max=0;
    const targets=cards.map((c,i)=>{const side=i%2?"r":"l",top=Math.max(i?prev+58:14,bottom[side]?bottom[side]+14:0);c.style.top=top+"px";bottom[side]=top+c.offsetHeight;prev=top;max=Math.max(max,bottom[side]);return {x:side==="l"?c.offsetWidth:box.clientWidth-c.offsetWidth,y:top+26,join:top+52};});
    const h=max+110;box.style.height=h+"px";const svg=box.querySelector("svg");svg.setAttribute("width",box.clientWidth);svg.setAttribute("height",h);
    drawVine(svg,{cx:box.clientWidth/2,top:0,bottom:max+30,targets,k:.78,twigs:[]});
  }

  function workHTML(n){const hist=n.history||[];return hist.length?`<div class="ssta-work"><span class="ssta-eyebrow">Work under this node</span>${hist.map(id=>{const l=leaves[id],tag=(l.ids||[]).join(" ").match(/(?:FIX|RS-|T|Codex )\s*\d+/)?.[0]||fmt(l.date);return `<button type="button" data-expand="${esc(id)}" aria-expanded="false"><span class="ssta-tag">${esc(tag)}</span><span>${esc(l.plain)}</span><span class="ssta-chev" aria-hidden="true">&#8250;</span></button>`;}).join("")}</div>`:"";}
  function nodeHTML(id){
    if(id==="goal")return `<p class="ssta-crumb">Goal</p><h2>${esc(D.goal.title)}</h2><p>${esc(D.goal.plain)}</p>`;
    const n=nodes[id],b=nodes[n.parent],note=(n.status_text||"").replace(new RegExp("^"+n.status+"[\\s:.,]*"),"").replace(/^\((.*)\)\.?$/,"$1");
    const report=(n.history||[]).flatMap(id=>leaves[id].links||[])[0];
    return `<p class="ssta-crumb">${esc(b?.title||"The Tree")} / ${id}</p><h2>${esc(n.title)}</h2><div class="ssta-pill">${stat(n.status)}<span>${esc(note)}</span></div><div><h4>What it is</h4><p>${esc(n.plain)}</p></div>
      ${n.why?`<div><h4>Why it matters</h4><p>${esc(n.why)}</p></div>`:""}
      ${n.loss?`<div class="ssta-metric"><div class="ssta-big">${n.loss.count} of ${n.loss.total}<span>test planets lost</span></div><div class="ssta-meter"><i style="width:${n.loss.count/n.loss.total*100}%"></i></div></div>`:""}
      ${n.children?`<div class="ssta-work">${n.children.map(id=>`<button type="button" data-node="${id}">${esc(nodes[id].title)}</button>`).join("")}</div>`:""}${workHTML(n)}
      <div class="ssta-links">${report?`<a href="${esc(report.url)}">Read more &#8594;</a>`:`<a href="https://github.com/M1Smacker/second-sun/blob/main/research/TREE.md">Read more &#8594;</a>`}<a href="${esc(n.lesson || "learn/")}">Learn this &#8594;</a></div>`;
  }
  function leafBody(l){return `${l.why?`<h4>Why it matters</h4><p>${esc(l.why)}</p>`:""}${l.explanation?`<p>${esc(l.explanation)}</p>`:""}${l.technical?`<p>${esc(l.technical)}</p>`:""}${(l.links||[]).map(link=>`<div class="ssta-links"><a href="${esc(link.url)}">Read more &#8594;</a></div>`).join("")}`;}
  function openNode(id){if(id!=="goal"&&!nodes[id])return;showCard(nodeHTML(id),"n:"+id);}
  function openLeaf(id){const l=leaves[id];if(l)showCard(`<p class="ssta-crumb">${esc(l.node)} / ${esc(fmt(l.date))}</p><h2>${esc(l.plain)}</h2>${leafBody(l)}<div class="ssta-links"><a href="#n=${esc(l.node)}" data-node="${esc(l.node)}">Back to ${esc(nodes[l.node]?.title)}</a></div>`,"l:"+id);}
  function restore(key){restoring=true;try{if(key.startsWith("n:"))openNode(key.slice(2));else if(key.startsWith("l:"))openLeaf(key.slice(2));}finally{restoring=false;}}
  // FIX 100 CX2-02 (Codex 021): the PC panel is docked to the screen, below the header, over its own reserved column, so the whole
  // panel and its Close button stay visible however far the page is scrolled (sticky let it run off the bottom or slide under the header).
  function dock(card) {
    const slot = host.querySelector(".ssta-detail-slot");
    if (!slot || !card || !card.isConnected || !card.classList.contains("ssta-pc-detail")) return;
    // Clear the header and, while it shows (at the top of the page), the menu tabs bar under it (WebKit hit it, 15 Nov 2026).
    const bars = [document.querySelector(".md-header"), document.querySelector(".md-tabs")].filter((e) => e && !e.hidden && e.getClientRects().length);
    const r = slot.getBoundingClientRect(), top = Math.round(Math.max(0, ...bars.map((e) => e.getBoundingClientRect().bottom)) + 16);
    Object.assign(card.style, { position: "fixed", top: top + "px", left: Math.round(r.left) + "px", width: Math.round(r.width) + "px", maxHeight: (innerHeight - top - 16) + "px", marginTop: "0" });
  }
  addEventListener("scroll", () => { if (openState && openState.card) dock(openState.card); }, { passive: true });
  addEventListener("resize", () => { if (openState && openState.card) dock(openState.card); });
  function showCard(html, key) {
    const replacing = !!openState;
    if (!replacing) returnFocus = document.activeElement;
    removeCard(false);
    const sheet = !WIDE.matches;
    const card = document.createElement("div");
    card.className = sheet ? "sst-sheet sst" : "sst-card ssta-pc-detail ssta-box";
    card.setAttribute("role", sheet ? "dialog" : "region");
    card.setAttribute("aria-label", "Tree details");
    if (sheet) card.setAttribute("aria-modal", "true");
    card.innerHTML = `${sheet ? '<div class="sst-grab" aria-hidden="true"></div>' : ""}
      <div class="ssta-detail"><button type="button" class="sst-x" aria-label="Close">&times;</button>${html}</div>`;
    let scrim = null, unlock = null;
    if (sheet) {
      scrim = document.createElement("div");
      scrim.className = "sst-scrim";
      scrim.onclick = closeCard;
      document.body.append(scrim, card);
      const pageY = scrollY;
      const bodyStyle = document.body.getAttribute("style");
      const inerted = [...document.body.children].filter(element => element !== card && element !== scrim && !element.inert);
      inerted.forEach(element => element.inert = true);
      Object.assign(document.body.style, { position: "fixed", top: `-${pageY}px`, width: "100%" });
      unlock = () => {
        inerted.forEach(element => element.inert = false);
        if (bodyStyle === null) document.body.removeAttribute("style");
        else document.body.setAttribute("style", bodyStyle);
        scrollTo(0, pageY);
      };
      card.addEventListener("keydown", event => {
        if (event.key !== "Tab") return;
        const items = [...card.querySelectorAll("button,a[href]")].filter(element => element.getClientRects().length);
        if (event.shiftKey && document.activeElement === items[0]) {
          event.preventDefault();
          items.at(-1).focus();
        } else if (!event.shiftKey && document.activeElement === items.at(-1)) {
          event.preventDefault();
          items[0].focus();
        }
      });
    } else {
      host.querySelector(".ssta-detail-slot").append(card);
      dock(card);
      // Older WebKit builds need an explicit fallback for scroll chaining.
      if (!CSS.supports("overscroll-behavior-y", "contain")) {
        card.dataset.wheelContain = "manual";
        card.addEventListener("wheel", event => {
          if (event.ctrlKey) return;
          event.preventDefault();
          const unit = event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? card.clientHeight : 1;
          card.scrollTop += event.deltaY * unit;
        }, { passive: false });
      }
    }
    openState = { card, scrim, restore: unlock, key };
    if (!restoring) {
      const url = new URL(location.href);
      url.hash = key[0] + "=" + encodeURIComponent(key.slice(2));
      const method = replacing ? "replaceState" : "pushState";
      history[method]({ ...history.state, sst: key }, "", url);
    }
    card.querySelector(".sst-x").onclick = closeCard;
    card.addEventListener("click", event => {
      const nodeButton = event.target.closest("[data-node]");
      if (nodeButton) {
        event.preventDefault();
        event.stopPropagation();
        openNode(nodeButton.dataset.node);
        return;
      }
      const expandButton = event.target.closest("[data-expand]");
      if (!expandButton) return;
      const isOpen = expandButton.getAttribute("aria-expanded") === "true";
      expandButton.setAttribute("aria-expanded", String(!isOpen));
      expandButton.querySelector("span:nth-child(2)").classList.toggle("ssta-expanded", !isOpen);
      if (isOpen) {
        expandButton.nextElementSibling?.remove();
      } else {
        const body = document.createElement("div");
        body.className = "ssta-work-body";
        body.innerHTML = leafBody(leaves[expandButton.dataset.expand]);
        expandButton.after(body);
      }
    });
    host.querySelectorAll(".ssta-row").forEach(element => element.setAttribute("aria-current", String(key === "n:" + element.dataset.node)));
    card.querySelector(".sst-x").focus({ preventScroll: true });
  }

  function removeCard(focus = true) {
    const state = openState;
    if (!state) return;
    openState = null;
    state.restore?.();
    state.card.remove();
    state.scrim?.remove();
    if (focus && returnFocus?.isConnected) returnFocus.focus({ preventScroll: true });
    host.querySelectorAll(".ssta-row").forEach(element => element.setAttribute("aria-current", "false"));
  }

  function clearHash() {
    const url = new URL(location.href);
    url.hash = "";
    const state = { ...history.state };
    delete state.sst;
    history.replaceState(state, "", url);
  }

  function closeCard() {
    if (!openState) return;
    removeCard();
    clearHash();
  }

  const leafAt = (g, x, y, ang, s) => el("path", { d: `M0,0 C${s * .3},${-s * .42} ${s * .78},${-s * .38} ${s},0 C${s * .78},${s * .38} ${s * .3},${s * .42} 0,0Z M1,0 L${s * .85},0`, transform: `translate(${x.toFixed(1)},${y.toFixed(1)}) rotate(${ang})`, fill: "none", stroke: "var(--ssta-gold-2)", "stroke-width": 1.3, "stroke-linejoin": "round" }, g);
  // trunk from top to bottom, a branch to each card, a leaf on each branch, twigs, roots at the base
  function drawVine(svg, o) {
    const { cx, top, bottom, targets, k, twigs } = o;
    svg.innerHTML = "";
    const g = el("g", {}, svg);
    const H = bottom - top;
    const sway = (y) => cx + Math.sin(((y - top) / H) * Math.PI * 1.6) * 16 * k - Math.sin(((y - top) / H) * Math.PI * 4.2) * 4 * k;
    let d = `M${sway(top).toFixed(1)},${top}`;
    for (let y = top + 6; y <= bottom; y += 6) d += ` L${sway(y).toFixed(1)},${y}`;
    el("path", { d, fill: "none", stroke: "var(--ssta-gold)", "stroke-width": 2 * k, "stroke-linecap": "round", class: "ssta-vine-path" }, g);
    targets.forEach((t, i) => {
      const y0 = t.join, x0 = sway(y0), side = Math.sign(t.x - x0) || 1, dx = t.x - x0;
      const c1x = x0 + dx * .18, c1y = y0 - (y0 - t.y) * .55, c2x = x0 + dx * .55, c2y = t.y + 2;
      el("path", { d: `M${x0.toFixed(1)},${y0} C${c1x.toFixed(1)},${c1y.toFixed(1)} ${c2x.toFixed(1)},${c2y.toFixed(1)} ${t.x.toFixed(1)},${t.y}`, fill: "none", stroke: "var(--ssta-gold)", "stroke-width": 1.4 * k, class: "ssta-vine-path" }, g);
      const lx = x0 + dx * .3, ly = y0 - (y0 - t.y) * .62 - 4 * k;
      leafAt(g, lx, ly, side > 0 ? -38 : 218, 22 * k);
      el("circle", { cx: x0.toFixed(1), cy: y0, r: 3.6 * k, fill: "var(--ss-bg)", stroke: "var(--ssta-gold)", "stroke-width": 1.3 }, g);
    });
    (twigs || []).forEach(([fy, side, len]) => {
      const y = top + H * fy, x = sway(y), ex = x + side * len * k, ey = y - 18 * k;
      el("path", { d: `M${x.toFixed(1)},${y.toFixed(1)} C${(x + side * len * .3 * k).toFixed(1)},${(y + 6 * k).toFixed(1)} ${(x + side * len * .7 * k).toFixed(1)},${(ey - 4).toFixed(1)} ${ex.toFixed(1)},${ey.toFixed(1)}`, fill: "none", stroke: "var(--ssta-gold-2)", "stroke-width": 1.1 * k }, g);
      leafAt(g, ex, ey, side > 0 ? -24 : 204, 26 * k);
    });
    const rx = sway(bottom);
    [[-150, 40, .7], [-110, 70, .55], [-45, 82, .6], [25, 86, .6], [80, 66, .55], [140, 38, .7]].forEach(([dx, dy, o2]) =>
      el("path", { d: `M${rx.toFixed(1)},${bottom - 34 * k} C${(rx + dx * .15 * k).toFixed(1)},${bottom + dy * .25 * k} ${(rx + dx * .6 * k).toFixed(1)},${bottom + dy * .75 * k} ${(rx + dx * k).toFixed(1)},${bottom + dy * k}`, fill: "none", stroke: "var(--ssta-gold-dim)", "stroke-width": 1.1, opacity: o2 }, g));
    el("path", { d: `M${rx.toFixed(1)},${bottom - 4} L${(rx - 2).toFixed(1)},${bottom + 52 * k}`, stroke: "var(--ssta-gold)", "stroke-width": 2 * k, fill: "none", "stroke-linecap": "round" }, g);
  }


})();
