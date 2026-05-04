import urllib.request
url = 'http://127.0.0.1:5000/reportes/'
with urllib.request.urlopen(url, timeout=5) as r:
    html = r.read().decode('utf-8', errors='replace')
print(html.find('href'))
print(html[:1200])
