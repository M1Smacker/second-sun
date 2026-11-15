// Explicit positions for the Eyes widgets. Focus never chooses the scroll position.
(() => {
  if (window.SSEyesFlow) return;
  const pages = new Map();
  function savePages() {
    pages.forEach((page) => {
      if (page.host.isConnected) page.position = page.flow.remember();
    });
  }
  // Capture before Material removes the page, including browser Back and the book's Back button.
  document.addEventListener("click", savePages, true);
  window.addEventListener("popstate", savePages);
  window.addEventListener("pagehide", savePages);
  // A different tab may have saved newer answers. Re-enter through the normal loader then.
  window.addEventListener("storage", () => pages.clear());
  window.SSEyesFlow = function (container) {
    let pending = 0;
    const reduced = () => matchMedia("(prefers-reduced-motion: reduce)").matches;
    const remember = () => ({ x: scrollX, y: scrollY, focus: document.activeElement });
    function move(target, position) {
      const ticket = ++pending;
      requestAnimationFrame(() => requestAnimationFrame(() => {
        if (ticket !== pending || !container.isConnected) return;
        if (position) {
          if (position.focus && position.focus.isConnected) position.focus.focus({ preventScroll: true });
          scrollTo({ left: position.x, top: position.y, behavior: "instant" });
        } else {
          target.tabIndex = -1;
          target.focus({ preventScroll: true });
          const header = document.querySelector(".md-header");
          const top = header ? header.getBoundingClientRect().bottom : 0;
          scrollTo({ top: scrollY + target.getBoundingClientRect().top - top - 12, behavior: "instant" });
        }
      }));
    }
    function reveal(target = container) {
      if (reduced() || !target.animate) return;
      target.getAnimations().forEach((animation) => animation.cancel());
      target.animate([{ opacity: 0, transform: "translateY(6px)" }, { opacity: 1, transform: "translateY(0)" }],
        { duration: 200, easing: "cubic-bezier(0.22, 1, 0.36, 1)" });
    }
    const flow = { remember, move, reveal,
      keep(host, key, canRestore, onResume) { pages.set(key, { host, flow, canRestore, onResume, position: remember() }); }
    };
    return flow;
  };
  window.SSEyesFlow.resume = function (host, key) {
    const page = pages.get(key);
    if (!page || page.host.isConnected || !page.canRestore()) return false;
    host.replaceWith(page.host);
    if (page.onResume) page.onResume();
    page.flow.move(page.host, page.position);
    return true;
  };
})();
