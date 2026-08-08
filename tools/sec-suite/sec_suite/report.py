import json
from pathlib import Path

def collect_results(indir='sec-suite-output'):
    p = Path(indir)
    data = {}
    if not p.exists():
        return data
    for f in p.glob('*.json'):
        try:
            data[f.name] = json.loads(f.read_text())
        except Exception:
            data[f.name] = f.read_text()
    return data


def render_html(data):
    out = ['<html><head><meta charset="utf-8"><title>sec-suite report</title><style>body{font-family:Arial;padding:20px}pre{background:#f6f6f6;padding:8px;border-radius:6px}</style></head><body>']
    out.append('<h1>sec-suite Report</h1>')
    for k,v in data.items():
        out.append(f'<h2>{k}</h2>')
        out.append('<pre>')
        out.append(json.dumps(v, indent=2))
        out.append('</pre>')
    out.append('</body></html>')
    return '\n'.join(out)
