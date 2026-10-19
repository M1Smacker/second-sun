#!/usr/bin/env bash
# Wave 3: try installing each candidate tool on Windows + Python 3.12; record pass/fail + key error line.
# Safe tools go into the main venv; tools with risky pins are tested in throwaway venvs under .venv-tests\
cd /d/second-sun
export PIP_CACHE_DIR='D:\second-sun\.cache\pip'
OUT=research/wave-3-pipeline/install_results.txt
: > $OUT
try() {  # $1 = venv dir, $2.. = pip args
  local v=$1; shift
  local t0=$(date +%s)
  if "$v/Scripts/python" -m pip install -q "$@" > /tmp/pipout.txt 2>&1; then r=PASS; else r=FAIL; fi
  echo "$r | $(( $(date +%s)-t0 ))s | $v | $* | $(grep -iE 'error|requires|conflict' /tmp/pipout.txt | head -2 | tr '\n' ' ' | cut -c1-300)" >> $OUT
}
for pkg in wotan transitleastsquares batman-package rebound triceratops exovetter; do try .venv $pkg; done
mkdir -p .venv-tests
for pkg in stanley_cbp mono-cbp ellc phoebe "git+https://github.com/mkunimoto/LEO-Vetter.git"; do
  name=$(echo $pkg | sed 's#.*/##; s/\.git$//; s/[^A-Za-z0-9_-]/_/g')
  py -3.12 -m venv .venv-tests/$name && try .venv-tests/$name "$pkg"
done
.venv/Scripts/python -m pip list 2>/dev/null | grep -iE "^(wotan|transitleastsquares|batman|rebound|triceratops|exovetter|numpy|scipy|astropy|lightkurve) " >> $OUT
echo DONE >> $OUT
