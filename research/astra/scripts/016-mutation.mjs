// A disposable built-asset mutation. Source files are never edited here.
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const scratch = path.resolve('data/astra/016');
const asset = path.join(scratch, 'site/assets/tree.js');
const original = fs.readFileSync(asset, 'utf8');
const needle = 'class: "sst-node "';
if (!original.includes(needle)) throw new Error('Tree class declaration changed, mutation not applied');
const saved = new Map(['results.json', 'progress.json', 'tree.log'].map((name) => [name, fs.readFileSync(path.join(scratch, name))]));
const run = () => spawnSync(process.execPath, ['research/astra/scripts/016-run.mjs', 'tree'], { encoding: 'utf8', windowsHide: true, timeout: 120000 });
try {
  fs.writeFileSync(asset, original.replace(needle, 'class: "sst-removed-node "'));
  const negative = run();
  const failedLog = fs.readFileSync(path.join(scratch, 'tree.log'), 'utf8');
  fs.writeFileSync(path.join(scratch, 'mutation-tree.log'), failedLog);
  fs.writeFileSync(asset, original);
  const positive = run();
  const restoredLog = fs.readFileSync(path.join(scratch, 'tree.log'), 'utf8');
  fs.writeFileSync(path.join(scratch, 'restored-tree.log'), restoredLog);
  const result = { brokenAssetExit: negative.status, restoredAssetExit: positive.status, rejectedMissingNodes: negative.status === 1 && /Tree target missing/.test(failedLog), restoredPass: positive.status === 0 && JSON.parse(restoredLog).pass === true };
  fs.writeFileSync(path.join(scratch, 'mutation.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result));
  process.exitCode = result.rejectedMissingNodes && result.restoredPass ? 0 : 1;
} finally {
  fs.writeFileSync(asset, original);
  for (const [name, bytes] of saved) fs.writeFileSync(path.join(scratch, name), bytes);
}
