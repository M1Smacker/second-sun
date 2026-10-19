"""Query arXiv API, print id | date | first authors | title (+ abstract head).
Usage: py -3.12 -I arxiv_q.py "<search_query>" | "id:<id1,id2>" [max] [abs_chars]"""
import sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding="utf-8")

q, n = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 25
abs_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 0
url = 'http://export.arxiv.org/api/query?' + urllib.parse.urlencode(
    {'id_list': q[3:], 'max_results': n} if q.startswith('id:') else
    {'search_query': q, 'max_results': n, 'sortBy': 'submittedDate', 'sortOrder': 'descending'})
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.fromstring(urllib.request.urlopen(url, timeout=60).read())
for e in root.findall('a:entry', ns):
    aid = e.find('a:id', ns).text.rsplit('/', 1)[-1]
    authors = [a.find('a:name', ns).text for a in e.findall('a:author', ns)]
    au = ', '.join(authors[:3]) + (' et al.' if len(authors) > 3 else '')
    title = ' '.join(e.find('a:title', ns).text.split())
    print(f"{aid} | {e.find('a:published', ns).text[:10]} | {au} | {title}")
    if abs_chars:
        print('    ', ' '.join(e.find('a:summary', ns).text.split())[:abs_chars])
time.sleep(3)  # arXiv asks for >=3 s between calls
