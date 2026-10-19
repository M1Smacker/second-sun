"""Run one ADQL query on VizieR TAP, print CSV. Usage: py -3.12 -I vizier_tap.py "<ADQL>" [max_chars]"""
import sys, urllib.parse, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
u = 'https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync?' + urllib.parse.urlencode(
    {'REQUEST': 'doQuery', 'LANG': 'ADQL', 'FORMAT': 'csv', 'QUERY': sys.argv[1]})
print(urllib.request.urlopen(u, timeout=180).read().decode()[:int(sys.argv[2]) if len(sys.argv) > 2 else 20000])
