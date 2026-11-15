// Deterministic DOM simulation. Checks routing, focus, scroll calls and motion policy.
// It does not measure browser layout or replace the MkDocs browser checks.
// Run with node research/astra/scripts/015-flow-regression.mjs [--mutate].
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
const core = createRequire(import.meta.url)('../../../book/docs/assets/eyes-core.js');
let document, context, reduced = false, animations = 0, checks = 0;
const frames = [];
const listeners = new Map();
class Element {
  constructor(tag) {
    this.tagName = tag.toUpperCase(); this.children = []; this.parentElement = null;
    this.style = {}; this.dataset = {}; this.events = {}; this.className = ''; this.text = '';
  }
  get isConnected() { return this === document.body || !!this.parentElement?.isConnected; }
  get firstElementChild() { return this.children[0]; }
  get textContent() { return this.text + this.children.map(child => child.textContent).join(''); }
  set textContent(value) { this.replaceChildren(); this.text = String(value); }
  append(...children) {
    for (let child of children) {
      if (!(child instanceof Element)) { const text = new Element('#text'); text.text = String(child); child = text; }
      child.parentElement = this; this.children.push(child);
    }
  }
  replaceChildren(...children) {
    this.children.forEach(child => { child.parentElement = null; });
    this.children = []; this.text = ''; this.append(...children);
  }
  replaceWith(element) {
    const parent = this.parentElement, index = parent.children.indexOf(this);
    parent.children[index] = element; element.parentElement = parent; this.parentElement = null;
  }
  insertBefore(element, next) { element.parentElement = this; this.children.splice(this.children.indexOf(next), 0, element); }
  closest(selector) {
    if (selector === 'button[data-a]') return this.tagName === 'BUTTON' && this['data-a'] ? this : null;
    return this;
  }
  setAttribute(key, value) { this[key] = value; }
  addEventListener(type, fn) { (this.events[type] ||= []).push(fn); }
  focus() { document.activeElement = this; }
  click() {
    this.focus(); listeners.get('click')?.();
    for (let element = this; element; element = element.parentElement) {
      (element.events.click || []).forEach(fn => fn({ target: this }));
    }
    flush();
  }
  getContext() { return new Proxy({}, { get: () => () => {} }); }
  getBoundingClientRect() { return { width: 340, top: 400 - context.scrollY, bottom: 448 - context.scrollY }; }
  animate() { animations++; return { cancel() {} }; }
  getAnimations() { return []; }
  querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
  querySelectorAll(selector) {
    const parts = selector.split(' '), last = parts.pop();
    const matches = (element, part) => part.startsWith('.') ? element.className.split(' ').includes(part.slice(1)) : element.tagName === part.toUpperCase();
    const found = [];
    const visit = element => element.children.forEach(child => {
      if (matches(child, last)) {
        let ancestor = child.parentElement;
        for (let i = parts.length - 1; i >= 0; i--) {
          while (ancestor && !matches(ancestor, parts[i])) ancestor = ancestor.parentElement;
          if (ancestor) ancestor = ancestor.parentElement;
          else return visit(child);
        }
        found.push(child);
      }
      visit(child);
    });
    visit(this); return found;
  }
}
function flush() { while (frames.length) frames.shift()(); }
document = {
  body: new Element('body'), activeElement: null, createElement: tag => new Element(tag),
  querySelector: () => null, querySelectorAll: () => [],
  addEventListener(type, fn) { listeners.set(type, fn); },
  removeEventListener() {},
};
const storage = new Map();
context = vm.createContext({ document, console, Date, Math, Map, Set, Array, isFinite,
  scrollX: 0, scrollY: 0, requestAnimationFrame: fn => frames.push(fn),
  scrollTo(position) { context.scrollX = position.left || 0; context.scrollY = position.top; },
  matchMedia: () => ({ matches: reduced }),
  addEventListener(type, fn) { listeners.set(type, fn); },
  ResizeObserver: class { observe() {} },
  localStorage: { getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value), removeItem: key => storage.delete(key) },
  SSEyes: core,
});
context.window = context;
vm.runInContext(fs.readFileSync('book/docs/assets/eyes-flow.js', 'utf8'), context);
if (process.argv.includes('--mutate')) {
  const flow = context.SSEyesFlow;
  context.SSEyesFlow = element => ({ ...flow(element), move() {} });
  context.SSEyesFlow.resume = flow.resume;
}
const engine = process.argv.includes('--baseline')
  ? execFileSync('git', ['show', 'HEAD:book/docs/assets/demos.js'], { encoding: 'utf8' })
  : fs.readFileSync('book/docs/assets/demos.js', 'utf8');
vm.runInContext(engine, context);
const host = new Element('div'); document.body.append(host);
context.host = host;
context.source = { id: 'synthetic', compose: (_mode, n) => Array.from({ length: n }, () => ({})),
  build: () => ({ y: Array(216).fill(0), truth: 'none', kind: 'quiet', meta: {}, note: 'Synthetic noise' }) };
vm.runInContext('eyesEngine(host, source, SSEyes, {...source, id:"hard-synthetic"})', context);
flush();
const stage = () => host.querySelector('.ss-eyes');
const button = label => stage().querySelectorAll('button').find(b => b.textContent === label && !b.hidden);
const click = label => { assert.ok(button(label), `button ${label}`); button(label).click(); };
const check = (label, test) => { assert.ok(test, label); checks++; console.log(`pass: ${label}`); };
for (const label of ['Take the official test (30 curves)', 'Take the HARD test (30 curves)', '5']) {
  context.scrollY = 175; click(label);
  const count = label === '5' ? 5 : 30;
  for (let i = 0; i < count; i++) {
    click('No dip');
    if (i === 1) {
      context.scrollY = 199; click('\u25c0 Look at previous question'); click('Back to light curve 2');
      check(`${label}, look-back restores question position`, context.scrollY === 199);
    }
    click(i + 1 < count ? 'Next' : label === '5' ? 'See how you did' : 'Finish the test');
  }
  check(`${label}, finish heading focused`, document.activeElement === stage().firstElementChild);
  check(`${label}, finish controls immediately after score`, stage().children[2].className.includes('ss-eyes__finish-actions'));
  check(`${label}, finish scrolled below header`, context.scrollY === 388);
  context.scrollY = 217; click('Review this round'); click('Close the review');
  check(`${label}, review restores exact finish position`, context.scrollY === 217);
  check(`${label}, review restores its launch control focus`, document.activeElement.textContent === 'Review this round');
  click('My results'); click('Back');
  check(`${label}, results returns to finish`, !!stage().querySelector('.ss-eyes__score') && context.scrollY === 217);
  check(`${label}, results restores its launch control focus`, document.activeElement.textContent === 'My results');
  click('Another sitting');
  check(`${label}, home position and launcher focus restored`, context.scrollY === 175 && document.activeElement.textContent === label);
}
context.scrollY = 98; click('My results'); click('Back');
check('home results returns to original launcher position', context.scrollY === 98 && document.activeElement.textContent === 'My results');
// An idle page can be reattached after Material replaces the article.
context.scrollY = 123; listeners.get('click')();
document.body.replaceChildren();
const replacement = new Element('div'); document.body.append(replacement);
let attachedStore;
context.SSEyesCloud = { attach(store) { attachedStore = store; }, status: () => 'Mock uploader', onStatus() {} };
check('instant navigation reuses idle widget', context.SSEyesFlow.resume(replacement, 'eyes'));
flush();
check('instant navigation restores saved pixels and focus', context.scrollY === 123 && document.activeElement.isConnected);
check('resumed Eyes widget reconnects its own saved-round store', attachedStore === context.SSEyesStore);
click('5');
document.body.replaceChildren();
const fresh = new Element('div'); document.body.append(fresh);
check('unfinished round retains existing re-entry behavior', !context.SSEyesFlow.resume(fresh, 'eyes'));
const flow = context.SSEyesFlow(fresh);
reduced = true; const before = animations; flow.reveal();
check('reduced motion suppresses reveal', animations === before);
reduced = false; flow.reveal(); check('normal motion reveals', animations === before + 1);
check('new asset precedes widget scripts', fs.readFileSync('book/mkdocs.yml', 'utf8').indexOf('assets/eyes-flow.js') < fs.readFileSync('book/mkdocs.yml', 'utf8').indexOf('assets/rehearsal.js'));
// Mount the real rehearsal UI with a two-item synthetic deck.
const item = star => ({ star, cls: 'noise', tier: null, box_h: 3, tc: 1, t_lo: 0, t_hi: 1,
  p1: Array(24).fill(0), p2: Array(240).fill(0), sigma: 100, wp: 0.1, ws: 0.1, phase: 0.2, meta: {} });
context.fetch = async () => ({ ok: true, json: async () => ({ sessions: Array.from({ length: 8 }, () => [item(0), item(1)]) }) });
vm.runInContext(fs.readFileSync('book/docs/assets/rehearsal.js', 'utf8'), context);
const rehearsal = new Element('div'); rehearsal.className = 'ss-rehearsal'; rehearsal.dataset.deck = 'synthetic';
document.body.replaceChildren(rehearsal); context.SSRehearsal.mount(rehearsal);
await new Promise(resolve => setImmediate(resolve)); flush();
context.scrollY = 252; rehearsal.querySelector('.ss-rh__go').click();
for (let i = 0; i < 2; i++) {
  rehearsal.querySelector('.ss-rh__a').click(); rehearsal.querySelector('.ss-rh__lock').click();
  rehearsal.querySelector('.ss-rh__next').click();
}
const summary = rehearsal.querySelector('.ss-rh__results');
check('rehearsal finish controls follow its score', summary.children[2].textContent === 'Back to the start');
check('rehearsal finish focuses heading and scrolls', document.activeElement.tagName === 'H3' && context.scrollY === 388);
summary.children[2].click();
check('rehearsal returns to saved position and next launcher', context.scrollY === 252 && document.activeElement.textContent.startsWith('Start session 2'));
listeners.get('click')(); document.body.replaceChildren(fresh);
check('idle rehearsal can resume', context.SSEyesFlow.resume(fresh, 'rehearsal')); flush();
check('resumed rehearsal reconnects its own store', attachedStore !== context.SSEyesStore);
document.body.replaceChildren(fresh); listeners.get('storage')();
check('other-tab saves invalidate cached widgets', !context.SSEyesFlow.resume(fresh, 'rehearsal'));
console.log(`${checks} flow regression checks passed (DOM simulation, no browser geometry).`);
