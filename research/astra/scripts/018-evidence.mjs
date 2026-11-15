// Scratch-only negative control and settled Tree geometry. Source app stays intact.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const scratch = path.resolve('data/astra/018');
const site = path.join(scratch, 'site');
const tool = path.resolve('research/burn-3-book/tools/site_check.mjs');
const asset = path.join(site, 'assets/learn.js');
const original = fs.readFileSync(asset);
let server;

async function run(file, mode, name) {
  const child = spawn(process.execPath, [file, mode, 'http://127.0.0.1:8496/',
    `--site=${site}`, '--chrome-no-sandbox=1', `--profiles=${path.join(scratch, 'profiles')}`],
  { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  let output = '';
  child.stdout.on('data', data => { output += data; });
  child.stderr.on('data', data => { output += data; });
  const code = await new Promise((resolve, reject) => {
    child.once('exit', resolve);
    child.once('error', reject);
  });
  fs.writeFileSync(path.join(scratch, `${name}.log`), output);
  const result = output.split(/\r?\n/).filter(line => line.startsWith('{')).map(JSON.parse).at(-1);
  if (!result) throw new Error(`${name} produced no JSON result, exit ${code}`);
  return { code, result };
}

try {
  fs.writeFileSync(path.join(scratch, 'evidence-progress.json'), JSON.stringify({
    status: 'running', expectedFinish: new Date(Date.now() + 15 * 60000).toISOString()
  }));
  server = spawn(process.execPath, [path.resolve('research/burn-3-book/tools/serve.mjs'),
    `--dir=${site}`, '--port=8496'], { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'] });
  await new Promise((resolve, reject) => {
    server.stdout.once('data', resolve);
    server.once('error', reject);
    server.once('exit', code => reject(new Error(`Server exited ${code}`)));
  });
  // Four home checks, original layout criteria, with 2.5 seconds to settle.
  const diagnostic = fs.readFileSync(tool, 'utf8')
    .replace(/^const PAGES = .*;$/m, 'const PAGES = [""];')
    .replace('await sleep(300);', 'await sleep(2500);');
  const diagnosticPath = path.join(scratch, 'settled-layout.mjs');
  fs.writeFileSync(diagnosticPath, diagnostic);
  const settled = await run(diagnosticPath, 'layout', 'settled-layout');
  const text = original.toString('utf8');
  if (!text.includes('Math.abs(b) * tol')) throw new Error('Mutation target missing');
  fs.writeFileSync(asset, text.replace('Math.abs(b) * tol', 'Math.abs(b) * 0.25'));
  const mutation = await run(tool, 'learn', 'numeric-mutation');
  const rejected = mutation.result.fails.filter(message => message.includes('20% off')).length;
  if (mutation.code !== 1 || rejected === 0) throw new Error('Numeric mutation escaped detection');
  fs.writeFileSync(path.join(scratch, 'evidence-summary.json'), JSON.stringify({
    settled, mutation: { exit: mutation.code, checks: mutation.result.checks,
      numericRejectionsCaught: rejected, failedAssertions: mutation.result.fails.length }
  }, null, 2));
  fs.writeFileSync(path.join(scratch, 'evidence-progress.json'), JSON.stringify({ status: 'complete' }));
} catch (error) {
  fs.writeFileSync(path.join(scratch, 'evidence-progress.json'), JSON.stringify({ status: 'failed', error: String(error) }));
  process.exitCode = 1;
} finally {
  fs.writeFileSync(asset, original);
  fs.writeFileSync(path.join(scratch, 'asset-restored.json'), JSON.stringify({ equal: fs.readFileSync(asset).equals(original) }));
  if (server && server.exitCode === null) {
    const stopped = new Promise(resolve => server.once('exit', resolve));
    server.kill();
    await stopped;
  }
}
