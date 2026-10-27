import sys, json, os, re, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'dl')
# family key -> (npm package, regex of file names to keep)
FAMS = {
    'atkinson':   ('@fontsource-variable/atkinson-hyperlegible-next', r'-wght-(normal|italic)\.woff2$'),
    'literata':   ('@fontsource-variable/literata', r'-(wght|opsz)-(normal|italic)\.woff2$'),
    'plexsans':   ('@fontsource/ibm-plex-sans', r'-(400|600)-(normal|italic)\.woff2$'),
    'plexmono':   ('@fontsource/ibm-plex-mono', r'-(400|500)-normal\.woff2$'),
    'inter':      ('@fontsource-variable/inter', r'-wght-normal\.woff2$'),
    'notosans':   ('@fontsource-variable/noto-sans', r'-wght-normal\.woff2$'),
    'notomath':   ('@fontsource/noto-sans-math', r'-400-normal\.woff2$'),
    'notosym2':   ('@fontsource/noto-sans-symbols-2', r'-400-normal\.woff2$'),
    'notosym':    ('@fontsource-variable/noto-sans-symbols', r'-wght-normal\.woff2$'),
    'stixtext':   ('@fontsource/stix-two-text', r'-400-normal\.woff2$'),
}
import subprocess
def get(url):
    r=subprocess.run(['curl','-sSL','--fail','-A','curl/8.5',url],capture_output=True)
    if r.returncode: raise RuntimeError('curl %d %s'%(r.returncode,r.stderr.decode()[:120]))
    return r.stdout
log = {}
for key, (pkg, rx) in FAMS.items():
    d = os.path.join(OUT, key)
    os.makedirs(d, exist_ok=True)
    try:
        meta = json.loads(get(f'https://data.jsdelivr.com/v1/packages/npm/{pkg}'))
        ver = meta['tags']['latest']
        flat = json.loads(get(f'https://data.jsdelivr.com/v1/packages/npm/{pkg}@{ver}?structure=flat'))
    except Exception as e:
        print(key, 'LIST FAILED', e); continue
    names = [f['name'] for f in flat['files'] if f['name'].startswith('/files/') and re.search(rx, f['name'])]
    lic = [f['name'] for f in flat['files'] if f['name'].upper().startswith('/LICENSE')]
    print(key, pkg, ver, len(names), 'files', lic)
    log[key] = {'pkg': pkg, 'version': ver, 'files': []}
    for n in names:
        fn = n.split('/')[-1]
        dest = os.path.join(d, fn)
        if not os.path.exists(dest):
            try:
                data = get(f'https://cdn.jsdelivr.net/npm/{pkg}@{ver}{n}')
                open(dest, 'wb').write(data)
            except Exception as e:
                print('  fail', fn, e); continue
        log[key]['files'].append(fn)
    # licence text
    for l in lic[:1]:
        try:
            open(os.path.join(d, 'LICENSE.txt'), 'wb').write(get(f'https://cdn.jsdelivr.net/npm/{pkg}@{ver}{l}'))
        except Exception as e:
            print('  no licence', e)
json.dump(log, open(os.path.join(HERE, 'dl_log.json'), 'w', encoding='utf-8'), indent=1)
