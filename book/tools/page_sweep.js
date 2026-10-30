// Book page sweep (30 Oct 2026). Paste into the console of the LIVE book (or a local build) in a browser tab, then run:
//   const urls = [...(await (await fetch('/second-sun/sitemap.xml')).text()).matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => new URL(m[1]).pathname);
//   for (const u of urls) window.__res.push(await window.__check(u)); window.__res.filter(r => !r.ok || r.overflow || r.badImg || r.errs)
// It opens every page the way a reader does (a click on a link, so Material's instant navigation runs), waits 0.9 s, and records:
// load ok, horizontal overflow, broken images, text length, one h1, duplicate ids, bad in-page anchors, small tap targets, script errors.
// Run it once at 1440x900 and once at 375x812 (reload the page after resizing). Scroll behaviour needs REAL wheel events (scrollTo does not trigger the tab bug):
// scroll down one tick, then up ten, and read document.querySelector('.md-tabs').hasAttribute('hidden') and its height.
window.__errs = []; window.__res = [];
addEventListener('error', e => window.__errs.push({ m: String(e.message).slice(0, 120), p: location.pathname }));
addEventListener('unhandledrejection', e => window.__errs.push({ m: 'rej ' + String(e.reason).slice(0, 120), p: location.pathname }));
const wait = (ms) => new Promise(r => setTimeout(r, ms));
window.__check = async (path) => {
  const a = document.createElement('a'); a.href = path; a.style.cssText = 'position:fixed;left:0;top:0'; document.body.appendChild(a);
  const before = location.pathname; a.click(); a.remove();
  let ok = path === before; for (let k = 0; k < 50 && !ok; k++) { await wait(100); ok = location.pathname === path; }
  await wait(900);
  const iw = innerWidth, de = document.documentElement, main = document.querySelector('.md-content__inner'), r = { path, ok };
  if (!ok) { r.stuck = location.pathname; return r; }
  r.overflow = de.scrollWidth - iw > 1 ? de.scrollWidth - iw : 0;
  r.badImg = [...document.images].filter(i => i.complete && i.naturalWidth === 0 && i.src).length;
  r.textLen = main ? main.innerText.length : -1;
  r.h1 = document.querySelectorAll('.md-content h1').length;
  const ids = [...document.querySelectorAll('[id]')].map(e => e.id); r.dupIds = ids.length - new Set(ids).size;
  r.badAnchors = [...document.querySelectorAll('.md-content a[href^="#"]')].filter(x => x.getAttribute('href').length > 1 && !document.getElementById(decodeURIComponent(x.getAttribute('href').slice(1)))).length;
  r.smallTap = [...document.querySelectorAll('.md-content a, .md-content button, .md-content summary, .md-header button, .md-header label')].filter(e => !e.classList.contains('headerlink')).filter(e => { const b = e.getBoundingClientRect(); return b.width > 0 && b.height > 0 && (b.height < 40 || b.width < 40) && getComputedStyle(e).display !== 'inline'; }).length;
  r.errs = window.__errs.filter(e => e.p === path).length;
  return r;
};
