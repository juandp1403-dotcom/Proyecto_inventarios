import urllib.request
import urllib.error
for path in ['/reportes/', '/reportes/crear', '/reportes/nuevo']:
    url = 'http://127.0.0.1:5000' + path
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            body = r.read(200).decode('utf-8', errors='replace')
            print(path, r.status, body[:200])
    except urllib.error.HTTPError as e:
        body = e.read(200).decode('utf-8', errors='replace')
        print(path, e.code, body[:200])
    except Exception as e:
        print(path, 'ERROR', e)
