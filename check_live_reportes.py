import requests
for path in ['/reportes/', '/reportes/crear', '/reportes/nuevo']:
    try:
        r = requests.get('http://127.0.0.1:5000' + path, timeout=5)
        print(path, r.status_code)
        print(r.text[:200])
    except Exception as e:
        print(path, 'ERROR', e)
