import requests
import time
from urllib.parse import urljoin

DEFAULT_WORDLIST = [
    'admin/','login/','robots.txt','.git/','backup/','config.php','uploads/','wp-admin/','index.php'
]


def run_direnum(base_url, wordlist=None, rps=5, timeout=6):
    wl = DEFAULT_WORDLIST
    if wordlist:
        try:
            with open(wordlist,'r') as f:
                wl = [l.strip() for l in f if l.strip()]
        except Exception:
            pass
    results = []
    delay = 1.0 / max(1, rps)
    for p in wl:
        url = urljoin(base_url.rstrip('/')+'/', p.lstrip('/'))
        try:
            r = requests.get(url, timeout=timeout)
            results.append({'path': p, 'status': r.status_code, 'len': len(r.content)})
        except Exception as e:
            results.append({'path': p, 'error': str(e)})
        time.sleep(delay)
    return results
