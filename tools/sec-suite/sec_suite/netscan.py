"""Simple discovery + TCP connect scanner
Non-destructive by default. Uses ping and TCP connect."""
import platform
import subprocess
import ipaddress
import concurrent.futures
import socket
import time


def ping(ip, timeout=1):
    system = platform.system().lower()
    if system == 'windows':
        cmd = ['ping', '-n', '1', '-w', str(int(timeout*1000)), ip]
    else:
        cmd = ['ping', '-c', '1', '-W', str(int(timeout)), ip]
    try:
        r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return r.returncode == 0
    except Exception:
        return False


def expand(targets):
    ips = []
    for t in targets:
        try:
            if '/' in t:
                net = ipaddress.ip_network(t, strict=False)
                for h in net.hosts():
                    ips.append(str(h))
            else:
                ips.append(t)
        except Exception:
            continue
    return ips


def tcp_connect(ip, port, timeout=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        try:
            s.settimeout(1.0)
            b = s.recv(1024)
            banner = b.decode(errors='ignore').strip()
        except Exception:
            banner = ''
        s.close()
        return {'port': port, 'open': True, 'banner': banner}
    except Exception:
        try:
            s.close()
        except:
            pass
        return {'port': port, 'open': False}


def scan_ports_for_host(ip, ports, timeout=1.0, workers=100):
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(workers, len(ports) or 1)) as ex:
        futs = {ex.submit(tcp_connect, ip, p, timeout): p for p in ports}
        for fut in concurrent.futures.as_completed(futs):
            results.append(fut.result())
    return {'ip': ip, 'ports': sorted(results, key=lambda x: x['port'])}


def discover_and_scan(targets, workers=50):
    ips = expand(targets)
    discovered = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(ping, ip): ip for ip in ips}
        for fut in concurrent.futures.as_completed(futs):
            ip = futs[fut]
            try:
                up = fut.result()
            except Exception:
                up = False
            discovered.append({'ip': ip, 'alive': up})
    # scan common ports for alive hosts
    alive = [d['ip'] for d in discovered if d['alive']]
    common_ports = [22,80,443,21,23,25,53,110,143]
    scans = []
    for a in alive:
        scans.append(scan_ports_for_host(a, common_ports))
    return {'discovery': discovered, 'scans': scans}
