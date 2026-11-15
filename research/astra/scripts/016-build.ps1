$ErrorActionPreference = 'Stop'
$root = (Resolve-Path "$PSScriptRoot/../../..").Path
$scratch = Join-Path $root 'data/astra/016'
$bootstrap = Join-Path $scratch 'bootstrap'
New-Item -ItemType Directory -Force $bootstrap | Out-Null
# The existing MkDocs hook writes generated Tree data into docs. Redirect that
# generated output while leaving the book's source bytes untouched.
@'
import sys
from pathlib import Path
root = Path.cwd().parent
sys.path.insert(0, str(root / 'research/tree'))
import brain_build
brain_build.OUT = root / 'data/astra/016/generated-tree.json'
# The hook and MkDocs must read the newly generated copy for this build.
# Both redirects are limited to this single generated asset.
import shutil
source = root / 'book/docs/assets/data/tree.json'
read_text = Path.read_text
copyfile = shutil.copyfile
def tree_read(self, *args, **kwargs):
    return read_text(brain_build.OUT if self == source else self, *args, **kwargs)
def tree_copy(src, dst, *args, **kwargs):
    return copyfile(brain_build.OUT if Path(src) == source else src, dst, *args, **kwargs)
Path.read_text = tree_read
shutil.copyfile = tree_copy
'@ | Set-Content (Join-Path $bootstrap 'sitecustomize.py') -Encoding utf8
$env:PYTHONPATH = $bootstrap
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:XDG_CACHE_HOME = Join-Path $scratch 'cache'
Push-Location (Join-Path $root 'book')
try {
    & 'D:\second-sun\.venv-docs\Scripts\mkdocs.exe' build --strict -d (Join-Path $scratch 'site')
    if ($LASTEXITCODE -ne 0) { throw 'Strict MkDocs build failed' }
    Copy-Item -LiteralPath 'archive-v2' -Destination (Join-Path $scratch 'site/v2') -Recurse
} finally { Pop-Location }
