#!/usr/bin/env python3
"""
report_merge.py

Collects JSON outputs from multiple security tools, normalizes them into a single
"findings" array with a minimal schema, and writes:
 - merged_report.json (machine-readable)
 - merged_report.html (human-friendly, color-coded by severity)

Usage:
  python3 report_merge.py --input-dir ./outdir --output-json merged.json --output-html merged.html

This script is intended for aggregating outputs from authorized, lab-based scans.
"""

import argparse
import json
import glob
import uuid
import datetime
from pathlib import Path

SEVERITY_ORDER = {'critical': 5, 'high':4, 'medium':3, 'low':2, 'info':1}

DEFAULT_SCHEMA_FIELDS = ['id','tool','target','title','severity','description','evidence','recommendation','references']


def normalize_item(item, source_file):
    """Attempt to normalize an arbitrary item into the findings schema."""
    out = {}
    out['id'] = item.get('id') if isinstance(item, dict) and item.get('id') else str(uuid.uuid4())
    out['tool'] = item.get('tool') or (item.get('source') if isinstance(item, dict) else None) or Path(source_file).name
    out['target'] = item.get('target') or item.get('url') or item.get('host') or item.get('ip') or ''
    out['title'] = item.get('title') or item.get('name') or f'Finding from {out["tool"]}'
    out['severity'] = (item.get('severity') or 'info').lower()
    out['description'] = item.get('description') or item.get('summary') or ''
    out['evidence'] = item.get('evidence') or item.get('body') or item
    out['recommendation'] = item.get('recommendation') or ''
    out['references'] = item.get('references') or []
    return out


def load_json_files(indir):
    p = Path(indir)
    found = []
    for fp in sorted(p.glob('*.json')):
        try:
            j = json.loads(fp.read_text())
            found.append((fp, j))
        except Exception:
            # skip unreadable
            continue
    return found


def extract_findings(json_obj, source_file):
    findings = []
    # many tools output lists or dicts; attempt heuristics
    if isinstance(json_obj, list):
        for item in json_obj:
            if isinstance(item, dict) and 'findings' in item:
                for f in item['findings']:
                    findings.append(normalize_item(f, source_file))
            else:
                findings.append(normalize_item(item, source_file))
    elif isinstance(json_obj, dict):
        if 'findings' in json_obj and isinstance(json_obj['findings'], list):
            for f in json_obj['findings']:
                findings.append(normalize_item(f, source_file))
        else:
            # treat top-level dict as a single finding or collection
            # if dict has keys like 'hosts' or 'discovery', convert to info-type finding
            if any(k in json_obj for k in ('hosts','discovery','scans','resolve','cert','http')):
                findings.append(normalize_item({'title': Path(source_file).name, 'description': json_obj}, source_file))
            else:
                findings.append(normalize_item(json_obj, source_file))
    return findings


def merge(indir):
    files = load_json_files(indir)
    merged = {
        'metadata': {
            'generated': datetime.datetime.utcnow().isoformat()+'Z',
            'source_files': [str(fp) for fp,_ in files]
        },
        'findings': []
    }
    for fp, j in files:
        items = extract_findings(j, fp)
        merged['findings'].extend(items)
    # sort by severity
    merged['findings'].sort(key=lambda x: -SEVERITY_ORDER.get(x.get('severity','info'),1))
    return merged


def render_html(merged):
    css = '''
    body{font-family:Arial,Helvetica,sans-serif;padding:18px;color:#111}
    .meta{color:#666;margin-bottom:12px}
    .finding{border-radius:8px;padding:12px;margin-bottom:10px;border:1px solid #e6e6e6}
    .sev-critical{border-left:6px solid #8b0000}
    .sev-high{border-left:6px solid #ff4500}
    .sev-medium{border-left:6px solid #ff8c00}
    .sev-low{border-left:6px solid #2e8b57}
    .sev-info{border-left:6px solid #1e90ff}
    pre{background:#f6f6f6;padding:10px;border-radius:6px;overflow:auto}
    '''
    parts = ['<html><head><meta charset="utf-8"><title>Merged Security Report</title><style>%s</style></head><body>'%css]
    parts.append('<h1>Merged Security Report</h1>')
    parts.append('<div class="meta"><strong>Generated:</strong> %s</div>'%merged['metadata']['generated'])
    for f in merged['findings']:
        sev = f.get('severity','info').lower()
        cls = 'sev-info'
        if sev == 'critical': cls = 'sev-critical'
        elif sev == 'high': cls = 'sev-high'
        elif sev == 'medium': cls = 'sev-medium'
        elif sev == 'low': cls = 'sev-low'
        parts.append('<div class="finding %s">' % cls)
        parts.append('<h3>%s <small style="color:#666">(%s)</small></h3>' % (f.get('title'), f.get('tool')))
        parts.append('<p><strong>Target:</strong> %s &nbsp; <strong>Severity:</strong> %s</p>' % (f.get('target') or '-', f.get('severity').upper()))
        if f.get('description'):
            parts.append('<p>%s</p>' % (f.get('description') if isinstance(f.get('description'), str) else '<pre>'+json.dumps(f.get('description'), indent=2)+'</pre>'))
        parts.append('<p><strong>Evidence:</strong></p>')
        parts.append('<pre>%s</pre>'% (f.get('evidence') if isinstance(f.get('evidence'), str) else json.dumps(f.get('evidence'), indent=2)))
        if f.get('recommendation'):
            parts.append('<p><strong>Recommendation:</strong> %s</p>'%f.get('recommendation'))
        parts.append('</div>')
    parts.append('</body></html>')
    return '\n'.join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir','-i', default='sec-suite-output')
    parser.add_argument('--output-json','-j', default='merged_report.json')
    parser.add_argument('--output-html','-o', default='merged_report.html')
    args = parser.parse_args()
    merged = merge(args.input_dir)
    Path(args.output_json).write_text(json.dumps(merged, indent=2))
    Path(args.output_html).write_text(render_html(merged))
    print('Wrote', args.output_json, 'and', args.output_html)

if __name__ == '__main__':
    main()
