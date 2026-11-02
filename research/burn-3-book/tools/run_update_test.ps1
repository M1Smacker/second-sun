# Re-runnable offline-worker UPDATE test (bug 62, 2 Nov 2026). Run it whenever book/sw-template.js changes.
# It clones the committed main into D:\ss-update-test\repo (scratch, outside the working tree), builds the book, serves it the way
# GitHub Pages does (--maxage=600), then publishes versions B and C of the home page from inside the test and checks in headless Chrome:
# a reopen shows the new version at once, the update line appears once, a replaced waiting worker's cache is deleted, Reload reloads once,
# and the new worker still works offline. Usage:  .\run_update_test.ps1     Takes about 2 minutes. Commit and push first (it tests the pushed main).
$ErrorActionPreference = "Continue"
$work = "D:\ss-update-test"; $repo = "$work\repo"; $live = "D:\second-sun"; $tools = "$live\research\burn-3-book\tools"
$env:XDG_CACHE_HOME = "$live\.cache"
New-Item -ItemType Directory -Force $work | Out-Null
if (Test-Path "$repo\.git") { git -C $repo fetch --quiet --depth 1 origin main; git -C $repo reset --quiet --hard origin/main }
else { git clone --quiet --depth 1 "https://github.com/M1Smacker/second-sun.git" $repo }
if (-not (git -C $repo ls-files book/data/claims.csv)) { Copy-Item "$live\book\data\claims.csv" "$repo\book\data\claims.csv" -Force }
Push-Location "$repo\book"; & "$live\.venv-docs\Scripts\mkdocs.exe" build --strict -q 2>&1 | Out-Null; Pop-Location
$srv = Start-Process node -ArgumentList "$tools\serve.mjs", "--dir=$repo\book\site", "--port=8491", "--maxage=600" -PassThru -WindowStyle Hidden
Start-Sleep -Seconds 2
try {
    $o = & node "$tools\site_check.mjs" update "http://127.0.0.1:8491/" "--proto=$repo\book" "--mkdocs=$live\.venv-docs\Scripts\mkdocs.exe" "--site=$repo\book\site" 2>&1 | Out-String
    Write-Host $o
    if ($LASTEXITCODE -ne 0) { exit 1 }
}
finally { Stop-Process -Id $srv.Id -Force -ErrorAction SilentlyContinue }
