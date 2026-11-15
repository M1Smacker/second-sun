// Local-only browser evidence, one Chrome at a time. Run from the worktree root.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
const scratch = path.resolve('data/astra/018');
const site = path.join(scratch, 'site');
const tools = path.resolve('research/burn-3-book/tools');
const selected = process.argv.slice(2);
const modes = selected.length ? selected : ['learn', 'layout', 'textfloor'];
const results = [];
let server;
async function startServer(fail = false) {
  server = spawn(process.execPath, [path.join(tools, 'serve.mjs'), `--dir=${site}`, '--port=8496', ...(fail ? ['--fail=/training/', '--fail=/training/index.html'] : [])], { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  const log = fs.createWriteStream(path.join(scratch, 'server.log'), { flags: 'a' });
  server.stdout.pipe(log); server.stderr.pipe(log);
  await new Promise((resolve, reject) => { server.stdout.once('data', resolve); server.once('error', reject); server.once('exit', (code) => reject(new Error('Server exited ' + code))); });
}
async function stopServer() {
  if (!server || server.exitCode !== null) return;
  const stopped = new Promise((resolve) => server.once('exit', resolve));
  server.kill(); await stopped;
}
function run(mode, options) {
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, [path.join(tools, 'site_check.mjs'), mode, 'http://127.0.0.1:8496/', `--site=${site}`, '--chrome-no-sandbox=1', `--profiles=${path.join(scratch, 'profiles')}`, `--debug=${path.join(scratch, mode + '-cdp.log')}`, ...options], { windowsHide: true });
    let output = '';
    child.stdout.on('data', (d) => { output += d; }); child.stderr.on('data', (d) => { output += d; });
    child.once('error', reject);
    const timeout = setTimeout(() => child.kill(), 600000);
    child.once('exit', (code) => {
      clearTimeout(timeout);
      fs.writeFileSync(path.join(scratch, `${mode}.log`), output);
      results.push({ mode, exit: code, output });
      fs.writeFileSync(path.join(scratch, 'results.json'), JSON.stringify(results, null, 2));
      resolve();
    });
  });
}
try {
  fs.writeFileSync(path.join(scratch, 'progress.json'), JSON.stringify({ status: 'running', expectedFinish: new Date(Date.now() + 15 * 60000).toISOString(), modes }));
  await startServer();
  for (const mode of modes) {
    let options = [];
    if (mode === 'fail404') { await stopServer(); await startServer(true); options = ['--failing=training/', '--missing=2']; }
    if (mode === 'images') {
      await stopServer(); await startServer();
      options = ['--gallery=labs/lab3-plot-and-read/', '--cap=150'];
    }
    if (mode === 'shots') { fs.mkdirSync(path.join(scratch, 'shots'), { recursive: true }); options = [`--out=${path.join(scratch, 'shots')}`]; }
    if (mode === 'hammer') options = ['--page=shelf/', '--asset=http://127.0.0.1:8496/assets/tree.js'];
    await run(mode, options);
  }
  fs.writeFileSync(path.join(scratch, 'progress.json'), JSON.stringify({ status: 'complete', modes, failed: results.filter((r) => r.exit !== 0).map((r) => r.mode) }));
  console.log(JSON.stringify(results.map(({ mode, exit }) => ({ mode, exit }))));
  process.exitCode = results.some((r) => r.exit !== 0) ? 1 : 0;
} catch (error) {
  fs.writeFileSync(path.join(scratch, 'progress.json'), JSON.stringify({ status: 'failed', error: String(error) }));
  throw error;
} finally { await stopServer(); }


