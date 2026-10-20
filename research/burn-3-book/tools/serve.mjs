// Static test server for the book prototype (Node, no packages). Replaces tools/serve.py:
// on this PC Chrome left 4-17% of requests to Python's http.server hanging >5 s, and 0% with Node
// (measured 2026-10-19, see report "Stress tests").
// Behaves like GitHub Pages where it matters: dir/ -> dir/index.html, "/dir" -> 301 "/dir/",
// unknown path -> 404.html with status 404. Adds no-cache headers so rebuilds are seen at once.
// --fail=/path (repeatable) answers 404 for that exact path (tests the worker's skip-on-failure install).
// Usage: node serve.mjs --dir=site-proto/site --port=8471 [--fail=/quests/] [--fail=/quests/index.html]
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const get = (k, d) => (args.find((a) => a.startsWith(`--${k}=`)) || `=${d}`).split("=").slice(1).join("=");
const root = path.resolve(get("dir", "."));
const port = Number(get("port", 8471));
const fail = new Set(args.filter((a) => a.startsWith("--fail=")).map((a) => a.slice(7)));
const TYPES = { ".html": "text/html; charset=utf-8", ".css": "text/css", ".js": "text/javascript", ".json": "application/json",
  ".png": "image/png", ".svg": "image/svg+xml", ".xml": "application/xml", ".webmanifest": "application/manifest+json", ".gz": "application/gzip" };

function send(res, status, file) {
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(500); res.end("read error"); return; }
    res.writeHead(status, { "Content-Type": TYPES[path.extname(file)] || "application/octet-stream", "Cache-Control": "no-cache" });
    res.end(data);
  });
}

http.createServer((req, res) => {
  const urlPath = decodeURIComponent(new URL(req.url, "http://x").pathname);
  if (fail.has(urlPath)) { res.writeHead(404, { "Cache-Control": "no-cache" }); res.end("forced 404"); return; }
  const file = path.join(root, urlPath);
  if (!file.startsWith(root)) { res.writeHead(403); res.end(); return; }          // no path traversal
  fs.stat(file, (err, st) => {
    if (!err && st.isDirectory()) {
      if (!urlPath.endsWith("/")) { res.writeHead(301, { Location: urlPath + "/" }); res.end(); return; }
      const index = path.join(file, "index.html");
      return fs.existsSync(index) ? send(res, 200, index) : send(res, 404, path.join(root, "404.html"));
    }
    if (!err && st.isFile()) return send(res, 200, file);
    send(res, 404, path.join(root, "404.html"));
  });
}).listen(port, "127.0.0.1", () => console.log(`serving ${root} on http://127.0.0.1:${port}/ fail=${[...fail]}`));
