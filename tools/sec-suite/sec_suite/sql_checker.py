import requests

# Conservative SQL checker: inject safe test payloads and look for common DB error strings
ERROR_SIGNS = ['sql syntax', 'mysql', 'syntax error', 'unclosed quotation mark', 'pq:', 'ORA-']
TEST_PAYLOADS = ["'", '"', "' OR '1'='1"]


def run_checks(url):
    findings = []
    for p in TEST_PAYLOADS:
        try:
            r = requests.get(url, params={'q': p}, timeout=8)
            body = r.text.lower()
            for sig in ERROR_SIGNS:
                if sig in body:
                    findings.append({'payload': p, 'evidence': sig, 'status': r.status_code, 'url': r.url})
        except Exception as e:
            findings.append({'payload': p, 'error': str(e)})
    return {'url': url, 'findings': findings}
