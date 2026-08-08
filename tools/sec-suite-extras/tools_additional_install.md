# Additional Tools: install & safe usage (lab-only)

This document adds safe installation and usage guidance for the additional tools you requested. These instructions are intended for educational, lab, and authorized penetration-testing use only.

LEGAL REMINDER (READ FIRST)
- Use these tools only on systems you own or where you have explicit written permission to test. Many of these tools can be intrusive or disruptive (wireless testing, MITM, poisoning, exploitation). Misuse is illegal and unethical.
- Whenever a tool can perform active or disruptive operations, the examples below use non-destructive or passive modes when possible, and emphasize lab-only deployment.

Tools and safe usage

1) Aircrack-ng (Python wrappers)
- Purpose: Wireless network auditing (capture and analysis, cracking protected networks in labs).
- Install (Linux) and basic usage (lab):
  - sudo apt update && sudo apt install aircrack-ng
  - For Python helpers: pip install aircrack-ng (third-party wrappers exist but prefer the CLI tools)
  - Use only on your own Wi‑Fi networks or an isolated lab AP. Examples:
    - Capture: sudo airodump-ng wlan0mon --write capture
    - Analyze: aircrack-ng capture-01.cap
- Notes: Many countries restrict wireless monitoring and deauth attacks; only run in a lab or on networks you own.

2) Impacket
- Purpose: Python library for low-level network protocols and authorized red-team exercises (SMB, NTLM relay, etc.).
- Install:
  pip install impacket
- Safe usage: use for reading/constructing packets in a lab. Do not run relay or credential-harvesting modules against production systems without permission.
- Example (list available scripts):
  python -c "import pkgutil, impacket; print([m.name for m in pkgutil.iter_modules(impacket.__path__)])"

3) Responder
- Purpose: LLMNR/NBT-NS poisoning and credential capture — highly intrusive.
- Safe usage: ONLY in a completely isolated lab network. Prefer to avoid unless you have explicit scope for active network attacks.
- Install and run in lab:
  git clone https://github.com/lgandx/Responder.git
  cd Responder
  # run in lab with monitor mode disabled until you verify environment
  sudo python Responder.py -I eth0
- Notes: Do NOT run on production or shared networks.

4) Mitmproxy
- Purpose: Interactive HTTPS-capable proxy for inspecting and modifying traffic (great for app testing).
- Install:
  pip install mitmproxy
- Lab-safe usage (intercept local app traffic):
  mitmproxy --mode regular -p 8080
  # Configure the test device to use http://<lab-host>:8080 as HTTP proxy and install mitmproxy CA cert
- Notes: Never intercept traffic from users without consent. Use on test devices or in lab.

5) Twint
- Purpose: Twitter OSINT without API (note: may break due to platform changes). Respect platform TOS.
- Install:
  pip install twint
- Basic usage (passive):
  twint -u someuser --json -o out.json
- Notes: Use responsibly and respect rate limits and terms of service.

6) Sherlock
- Purpose: Username enumeration across services.
- Install and run:
  git clone https://github.com/sherlock-project/sherlock.git
  pip install -r requirements.txt
  python3 sherlock/sherlock.py username --output out.csv
- Notes: Use only for your own accounts or accounts you have permission to investigate.

7) Knockpy
- Purpose: Subdomain discovery (dictionary-based).
- Install & run (passive dictionary; supply allowed wordlist):
  pip install knockpy
  knockpy example.local
- Notes: Keep rate low and only against domains you control.

8) Fierce (DNS recon)
- Purpose: DNS reconnaissance and discovery.
- Install & run:
  git clone https://github.com/davidpepper/fierce-domain-scanner.git
  perl fierce.pl -dns example.local
- Notes: Avoid brute-force sweeps without permission and monitor impact.

9) SpiderFoot
- Purpose: Automated OSINT collection across many sources.
- Install & run (Docker recommended):
  docker run -d -p 5001:5001 spiderfoot/spiderfoot
  # Access UI at http://localhost:5001
- Notes: Configure modules carefully to avoid abusive scraping and to respect API terms.

10) Shodan API (Python)
- Purpose: Search internet-connected devices via Shodan API.
- Install:
  pip install shodan
- Example usage (requires Shodan API key):
  python3 - <<'PY'
import shodan
api = shodan.Shodan('YOUR_API_KEY')
res = api.search('apache')
print(res['total'])
PY
- Notes: Use the API for discovery only; do not probe or attack devices found without permission.

Collecting outputs and reporting
- Use the existing report_merge.py in tools/sec-suite-extras to aggregate JSON outputs from these tools into merged_report.json and merged_report.html.
- Always include the legal & scope statements in any report you generate.

Would you like me to:
- append these entries into tools/sec-suite-extras/install_guides.md (yes/no)?
- create minimal Dockerfiles/containers for any of these tools so they run inside the local lab (recommend: mitmproxy, SpiderFoot, Shodan client, XSStrike already present)? Specify which tools if yes.

If you say “yes, append and add Dockerfiles for mitmproxy and spiderfoot”, I will append the docs and add Dockerfiles and compose entries and push them. Otherwise I will only append the docs.