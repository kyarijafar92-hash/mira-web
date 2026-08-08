# basic utility functions

def parse_ports(spec):
    parts = str(spec).split(',')
    out = set()
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if '-' in p:
            try:
                a,b = p.split('-',1)
                a=int(a); b=int(b)
                for x in range(a,b+1): out.add(x)
            except Exception:
                continue
        else:
            try:
                out.add(int(p))
            except Exception:
                continue
    return sorted(out)
