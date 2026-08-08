"""Simple OSINT harvester (crt.sh + DNS) — conservative and rate-limited"""
import requests
from urllib.parse import quote_plus

CRT_SH = 'https://crt.sh/?q='


def crtsh_lookup(domain):
    try:
        q = quote_plus('%.' + domain)
        url = CRT_SH + q + '&output=json'
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            try:
                return r.json()
            except Exception:
                return {'raw': r.text[:2000]}
        return {'error': r.status_code}
    except Exception as e:
        return {'error': str(e)}


def harvest(domain):
    data = {'domain': domain}
    data['crtsh'] = crtsh_lookup(domain)
    # basic DNS (A) lookup
    try:
        import socket
        data['resolve'] = socket.gethostbyname_ex(domain)
    except Exception as e:
        data['resolve_error'] = str(e)
    return data
