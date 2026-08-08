# sec-suite: Authorized security toolkit

This folder provides sec-suite — a modular, authorized security toolkit for
approved penetration testing and reconnaissance. Use only on systems you own or
have explicit written permission to test.

Modules included (safe-by-default):
- netscan: host discovery (ICMP) and TCP connect port scanning + banner grabbing
- pcap_analyzer: passive pcap reader (pcap file analysis; no packet crafting)
- osint: safe OSINT collectors (crt.sh, DNS, basic WHOIS via public endpoints)
- web_audit: passive HTTP/TLS checks (headers, TLS cert, robots.txt)
- direnum: directory enumeration with configurable wordlist and rate-limit
- web_fuzzer: conservative fuzzing of a single parameter/path with max requests
- sql_checker: conservative SQL injection detector (intrusive; requires confirm)
- report: aggregate JSON + HTML report generator

Legal & ethical requirements (you must read):
- I confirm I will only use this toolkit on systems I own or have written permission to test.
- Do NOT use these modules against third-party systems without explicit scope.

If you want additional hardening, Docker, or a web UI, ask and I will add it.
