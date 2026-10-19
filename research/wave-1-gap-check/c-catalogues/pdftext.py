"""Crude stdlib PDF text grep: inflate FlateDecode streams, pull (..) strings from TJ/Tj ops.
Usage: py -3.12 -I pdftext.py file.pdf [regex]
ponytail: no font-encoding/CMap handling; fine for LaTeX-made NASA/arXiv PDFs, garbles others."""
import re, sys, zlib

data = sys.stdin.buffer.read() if sys.argv[1] == '-' else open(sys.argv[1], 'rb').read()
out = []
for m in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', data, re.S):
    try:
        s = zlib.decompress(m.group(1))
    except Exception:
        continue
    for arr, single in re.findall(rb'\[((?:\\.|[^\]\\])*)\]\s*TJ|\(((?:\\.|[^\\)])*)\)\s*Tj', s, re.S):
        line = ''
        if arr:
            for txt, num in re.findall(rb'\(((?:\\.|[^\\)])*)\)|(-?\d+\.?\d*)', arr):
                if txt:
                    line += re.sub(rb'\\(.)', rb'\1', txt).decode('latin-1')
                elif num and float(num) < -200:
                    line += ' '
        else:
            line = re.sub(rb'\\(.)', rb'\1', single).decode('latin-1')
        out.append(line)
text = ' '.join(out)
if len(sys.argv) > 2:
    for m in re.finditer(sys.argv[2], text, re.I):
        print('>>', text[max(0, m.start() - 250):m.end() + 250])
else:
    print(text[:5000])
