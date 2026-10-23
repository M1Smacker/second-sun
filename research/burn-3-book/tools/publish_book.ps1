# Publish the book to GitHub Pages (https://m1smacker.github.io/second-sun/) WITHOUT touching main.
#
# What it does: fresh clone of the COMMITTED main -> strict build into a scratch folder -> safety checks ->
# commit the built site to the gh-pages branch from a separate scratch clone -> push. GitHub Pages serves gh-pages.
# Your working tree, your git state and port 8471 are never touched. Only gh-pages is pushed (never main, never --force).
#
# Usage (PowerShell):  .\publish_book.ps1            build, check, publish
#                      .\publish_book.ps1 -DryRun    build + checks only, no push
#                      .\publish_book.ps1 -Test      also run the browser tests (layout, offline, JS off) on a spare port
# Scratch folder: D:\ss-pages-work (outside the repo). Takes about a minute.
param([switch]$DryRun, [switch]$Test)

$ErrorActionPreference = "Continue"            # git writes progress to stderr; PowerShell 5.1 would treat that as an error under "Stop"
$work    = "D:\ss-pages-work"
$src     = "$work\src"
$build   = "$work\build"
$pub     = "$work\pub"
$live    = "D:\second-sun"                     # the working tree: read only, used for one ignored file (see below)
$mkdocs  = "$live\.venv-docs\Scripts\mkdocs.exe"
$url     = "https://m1smacker.github.io/second-sun/"
$repoUrl = "https://github.com/M1Smacker/second-sun.git"
$env:XDG_CACHE_HOME = "$live\.cache"           # never write caches to C:

function Run {                                  # run a native command, stop on a non-zero exit code
    $exe = $args[0]; $rest = @($args | Select-Object -Skip 1)
    & $exe @rest
    if ($LASTEXITCODE -ne 0) { throw "FAILED (exit $LASTEXITCODE): $exe $($rest -join ' ')" }
}
function Step($t) { Write-Host "`n== $t" -ForegroundColor Cyan }

New-Item -ItemType Directory -Force $work | Out-Null

Step "1. Fresh clone of committed main (scratch)"
# LF everywhere (core.autocrlf=false), so the same commit always builds to the same bytes. A scratch clone made with
# the Windows default (CRLF) is deleted and re-cloned; it only ever holds a copy of GitHub's main.
if ((Test-Path "$src\.git") -and ((git -C $src config core.autocrlf) -ne "false")) { Remove-Item -Recurse -Force $src }
if (Test-Path "$src\.git") { Run git -C $src fetch --quiet --depth 1 origin main; Run git -C $src reset --quiet --hard origin/main }
else { Run git clone --quiet --depth 1 -c core.autocrlf=false $repoUrl $src }
$mainHash = (git -C $src rev-parse --short HEAD).Trim()
Write-Host "building main at $mainHash"

Step "2. Known repo problem: book/data/claims.csv is git-ignored (.gitignore has 'data/') so a clean clone cannot build"
$tracked = (git -C $src ls-files book/data/claims.csv)
if ($tracked) { Write-Host "claims.csv is tracked in the clone: good" }
else {
    New-Item -ItemType Directory -Force "$src\book\data" | Out-Null
    Copy-Item "$live\book\data\claims.csv" "$src\book\data\claims.csv" -Force
    Write-Host "WARNING: copied claims.csv from the working tree. Fix at the source: add '!book/data/' to .gitignore and commit book/data/claims.csv." -ForegroundColor Yellow
}

Step "2b. Mission readiness rules still hold (negative and positive tests, run on the committed copy)"
Run "$live\.venv-docs\Scripts\python.exe" "$src\book\tools\test_mission.py"

Step "2b2. Book shape rules hold (path.yml, sidebar and sky data agree; broken copies are refused)"
Run "$live\.venv-docs\Scripts\python.exe" "$src\book\tools\test_shape.py"

Step "2c. Colour contrast still 7:1 or better (high-contrast rule)"
Run "$live\.venv-docs\Scripts\python.exe" "$src\book\tools\test_contrast.py"

Step "2d. Eyes mode logic: scoring, truth banner, saving after every answer, pass line (answers can never be changed)"
Run node "$src\book\tools\test_eyes.mjs"

Step "3. Strict build into $build"
Push-Location "$src\book"
Run $mkdocs build --strict -d $build
Pop-Location

Step "3b. Every link and anchor in the built site resolves; every chapter has the template"
Run "$live\.venv-docs\Scripts\python.exe" "$src\book\tools\check_site.py" $build

Step "4. Safety checks on the built site"
$html = Get-ChildItem $build -Recurse -Filter *.html
$missing = @($html | Where-Object { -not (Select-String -Path $_.FullName -Pattern 'noindex' -Quiet) })
if ($missing.Count) { throw "noindex missing in $($missing.Count) page(s), e.g. $($missing[0].FullName). Refusing to publish." }
$mb = [math]::Round((Get-ChildItem $build -Recurse -File | Measure-Object Length -Sum).Sum / 1MB, 1)
if ($mb -gt 50) { throw "built site is $mb MB (limit 50). Refusing to publish." }
$secret = Get-ChildItem $build -Recurse -File -Include *.html, *.js, *.json, *.css, *.xml, *.webmanifest |
    Select-String -Pattern 'ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|ntfy\.sh/[A-Za-z0-9_-]{8,}|BEGIN (RSA|OPENSSH) PRIVATE KEY' | Select-Object -First 1
if ($secret) { throw "possible secret in $($secret.Path): refusing to publish." }
if (-not (Test-Path "$build\sw.js")) { throw "sw.js missing: the hook did not run." }
Write-Host "ok: $($html.Count) pages, all noindex; $mb MB; no secret patterns"

if ($Test) {
    Step "4b. Browser tests on a spare port (8490)"
    $tools = "$live\research\burn-3-book\tools"
    $env:MSYS_NO_PATHCONV = "1"
    $srv = Start-Process node -ArgumentList "$tools\serve.mjs", "--dir=$build", "--port=8490" -PassThru -WindowStyle Hidden
    Start-Sleep -Seconds 2
    try { foreach ($m in "layout", "offline", "jsoff", "eyes") { Run node "$tools\site_check.mjs" $m "http://127.0.0.1:8490/" "--site=$build" | Out-Null; Write-Host "$m : pass" } }
    finally { Stop-Process -Id $srv.Id -Force -ErrorAction SilentlyContinue }
}

Step "4c. Same-day lesson rule: is the book behind the work? (reminder, never blocks)"
& "$live\.venv-docs\Scripts\python.exe" "$live\book\tools\teach_check.py"

if ($DryRun) { Write-Host "`nDry run: nothing pushed." -ForegroundColor Yellow; exit 0 }

Step "5. Publish to gh-pages"
if (-not (Test-Path "$pub\.git")) { Run git clone --quiet --branch gh-pages --single-branch $repoUrl $pub }
Run git -C $pub config user.name "M1Smacker"
Run git -C $pub config user.email "208063596+M1Smacker@users.noreply.github.com"
Run git -C $pub config core.autocrlf false      # keep LF; no line-ending warnings
Run git -C $pub pull --quiet --ff-only origin gh-pages
Get-ChildItem $pub -Force | Where-Object { $_.Name -ne ".git" } | Remove-Item -Recurse -Force
Copy-Item "$build\*" $pub -Recurse -Force
New-Item -ItemType File -Force "$pub\.nojekyll" | Out-Null
Run git -C $pub add -A
if (-not (git -C $pub status --porcelain)) { Write-Host "Nothing changed since the last publish." -ForegroundColor Green; Write-Host $url; exit 0 }
Run git -C $pub commit --quiet -m "Publish book (built from main $mainHash, strict build + checks passed)`n`nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
Run git -C $pub push origin gh-pages
Write-Host "`nPublished. GitHub takes 1 to 2 minutes to go live: $url" -ForegroundColor Green
