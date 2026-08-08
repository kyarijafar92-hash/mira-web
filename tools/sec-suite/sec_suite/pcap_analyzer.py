"""Passive pcap analyzer (read pcap files). Uses scapy if available or parses minimal info."""
import os


def analyze(pcap_path):
    # Try scapy if available for richer parsing
    try:
        from scapy.all import rdpcap
        pkts = rdpcap(pcap_path)
        summary = {'file': pcap_path, 'count': len(pkts)}
        # collect top protocols and IP pairs (simple)
        proto_count = {}
        pairs = {}
        for p in pkts[:1000]:
            proto = p.__class__.__name__
            proto_count[proto] = proto_count.get(proto, 0) + 1
            try:
                s = p.src; d = p.dst
                pairs[f"{s}->{d}"] = pairs.get(f"{s}->{d}", 0) + 1
            except Exception:
                pass
        summary['protocols'] = sorted(proto_count.items(), key=lambda x: -x[1])
        summary['pairs_sample'] = list(pairs.items())[:20]
        return summary
    except Exception:
        # fallback: simple file size and timestamp
        st = os.stat(pcap_path)
        return {'file': pcap_path, 'size': st.st_size}
