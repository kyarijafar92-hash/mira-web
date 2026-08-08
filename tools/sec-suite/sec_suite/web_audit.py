import requests
from urllib.parse import urlparse
import ssl
import socket


def fetch_headers(url, timeout=8):
    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)
        return {'status_code': r.status_code, 'headers': dict(r.headers), 'url': r.url}
    except Exception as e:
        return {'error': str(e)}


def get_cert(hostname, port=443, timeout=6):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                return ssock.getpeercert()
    except Exception as e:
        return {'error': str(e)}


def audit_url(url):
    out = {'url': url}
    h = fetch_headers(url)
    out['http'] = h
    parsed = urlparse(url)
    if parsed.scheme == 'https':
        out['cert'] = get_cert(parsed.hostname)
    try:
        base = f"{parsed.scheme}://{parsed.netloc}"
        r = requests.get(base + '/robots.txt', timeout=4)
        out['robots'] = r.text if r.status_code == 200 else None
    except Exception:
        out['robots'] = None
    return out
