// Small interactive demos. Material's instant navigation swaps pages without
// reloading, so (re)initialise on every page via document$.
const R_SUN_IN_EARTHS = 109.1;

function initDepthDemo(el) {
  const rp = el.querySelector('[name="rp"]'), rs = el.querySelector('[name="rs"]');
  const out = el.querySelector(".ss-demo__result"), dip = el.querySelector(".ss-demo__lc span");
  const update = () => {
    const depth = (rp.value / (rs.value * R_SUN_IN_EARTHS)) ** 2;   // fraction of light blocked
    el.querySelector('[name="rp_out"]').value = rp.value;
    el.querySelector('[name="rs_out"]').value = rs.value;
    const pct = depth * 100;
    const shown = depth >= 1 ? "100% (the 'planet' covers the whole star: not a planet!)"
      : `${pct < 0.1 ? pct.toFixed(4) : pct.toFixed(2)}% (${Math.round(depth * 1e6).toLocaleString()} ppm)`;
    out.textContent = `Depth: ${shown}`;
    dip.style.height = `${Math.max(2, Math.min(100, Math.sqrt(pct) * 30))}%`; // sqrt scale so tiny dips stay visible
  };
  rp.addEventListener("input", update);
  rs.addEventListener("input", update);
  update();
}

const start = () => document.querySelectorAll('.ss-demo[data-demo="depth"]').forEach(initDepthDemo);
if (typeof document$ !== "undefined") document$.subscribe(start); else start();
