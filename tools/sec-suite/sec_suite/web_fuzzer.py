import requests
import time
from urllib.parse import urlencode

DEFAULT_PAYLOADS = ["' OR '1'='1", '" OR "1"="1', "' OR 'x'='x' -- ", '<script>alert(1)</script>', '../../../etc/passwd']


def fuzz(url, param_name=None, payload_file=None, max_requests=200, timeout=6):
    payloads = DEFAULT_PAYLOADS
    if payload_file:
        try:
            with open(payload_file,'r') as f:
                payloads = [l.strip() for l in f if l.strip()]
        except Exception:
            pass
    results = []
    count = 0
    for p in payloads:
        if count >= max_requests:
            break
        try:
            if param_name:
                q = {param_name: p}
                r = requests.get(url, params=q, timeout=timeout)
                results.append({'payload': p, 'status': r.status_code, 'url': r.url, 'len': len(r.content)})
            else:
                # try path-based fuzzing
                target = url.rstrip('/') + '/' + p
                r = requests.get(target, timeout=timeout)
                results.append({'payload': p, 'status': r.status_code, 'url': r.url, 'len': len(r.content)})
        except Exception as e:
            results.append({'payload': p, 'error': str(e)})
        count += 1
        time.sleep(0.05)
    return results
