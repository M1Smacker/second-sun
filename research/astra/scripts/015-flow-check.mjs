// Run the existing local book browser checks with all scratch files confined to 015.
// Usage: node research/astra/scripts/015-flow-check.mjs --site=data/astra/015/site
import fs from 'node:fs';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
const site = process.argv.find(arg => arg.startsWith('--site='))?.slice(7);
const output = path.resolve('data/astra/015');
if (!site || !fs.existsSync(path.join(site, 'eyes/index.html'))) {
  console.error('BLOCKED: supply a local MkDocs build containing eyes/index.html.');
  process.exitCode = 1;
} else {
  const harness = path.join(output, 'site-check.mjs');
  const pidFile = path.join(output, `browser-${process.pid}.json`);
  const source = fs.readFileSync('research/burn-3-book/tools/site_check.mjs', 'utf8')
    .replace('`D:/second-sun/.cache/cdp-${tag}-${process.pid}`', JSON.stringify(path.join(output, 'cdp')) + ' + `-${tag}-${process.pid}`')
    // History now returns to the finish screen that launched it.
    .replace('await click("Back"); await click("Hard practice 20");', 'await click("Back"); await click("Another sitting"); await click("Hard practice 20");')
    .replace('let target;', `fs.writeFileSync(${JSON.stringify(pidFile)}, JSON.stringify({pid:proc.pid})); let target;`);
  fs.writeFileSync(harness, source, 'utf8');
  const server = spawn('node', ['research/burn-3-book/tools/serve.mjs', `--dir=${site}`, '--port=8491'], {stdio:'ignore'});
  try {
    await new Promise(resolve => setTimeout(resolve, 500));
    for (const mode of ['eyeslayout', 'eyes']) {
      const result = spawnSync('node', [harness, mode, 'http://127.0.0.1:8491/', `--site=${site}`], {encoding:'utf8', timeout:60000});
      const log = (result.stdout || '') + (result.stderr || '') + (result.error ? String(result.error) : '');
      fs.writeFileSync(path.join(output, `${mode}.log`), log, 'utf8');
      console.log(`${mode} exit=${result.status}\n${log}`);
      if (result.status !== 0) process.exitCode = 1;
      // Only the process recorded by this invocation is eligible for cleanup.
      if (fs.existsSync(pidFile)) {
        const {pid} = JSON.parse(fs.readFileSync(pidFile, 'utf8'));
        try { process.kill(pid); } catch (error) { if (error.code !== 'ESRCH') console.error(`Browser cleanup ${error.code}`); }
        fs.unlinkSync(pidFile);
      }
    }
  } finally { server.kill(); }
}
