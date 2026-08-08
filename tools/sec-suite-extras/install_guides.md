# Install & Usage Guides for common security tools (lab-only)

This guide gives step-by-step, safe installation and basic usage for several common security tools. Run these in a lab VM or container.

1) Metasploit Framework (recon modules)
- Debian/Ubuntu (Kali includes it already):
  sudo apt update && sudo apt install -y metasploit-framework
- Launch:
  msfconsole
- Safe usage (recon):
  use auxiliary/scanner/ssh/ssh_version
  set RHOSTS 127.0.0.1
  set THREADS 10
  run

2) Pocsuite3 (PoC runner) — review PoC code before use
- Install:
  pip3 install pocsuite3
- Verify installation:
  pocsuite3 --help
- Use in verify/non-destructive mode if the PoC supports it:
  pocsuite3 -r ./pocs/example_poc.py --target http://127.0.0.1 --verify

3) Social-Engineer Toolkit (SET) / GoPhish (phishing simulations)
- SET (Kali ships it). For structured phishing simulations prefer GoPhish:
  docker run -p 3333:3333 -p 8080:8080 gophish/gophish
- GoPhish web UI: http://localhost:3333 (admin console)
- Use only with authorized training targets and a test email domain.

4) XSStrike (XSS detection)
- Clone & install:
  git clone https://github.com/s0md3v/XSStrike.git
  cd XSStrike
  pip3 install -r requirements.txt
- Crawl/passive mode example:
  python3 xsstrike.py -u 'http://localhost:3000' --crawl

5) Wapiti (web vulnerability scanner)
- Install (Debian):
  sudo apt install wapiti
- Safe scan (non-aggressive):
  wapiti -u http://127.0.0.1:3000 -f html -o wapiti_report.html

6) Sublist3r (subdomain enumeration)
- Install & run:
  git clone https://github.com/aboul3la/Sublist3r.git
  cd Sublist3r
  pip3 install -r requirements.txt
  python3 sublist3r.py -d yourdomain.local -o subs.txt
- Use only on domains you own or have permission to test.

7) Locust (load testing) — safer alternative to DoS tools
- Install:
  pip3 install locust
- Example locustfile (create locustfile.py) and run:
  locust -f locustfile.py --host=http://localhost:3000
- Open web UI: http://localhost:8089 to start/stop load tests.

8) Nmap (port scanning)
- Install:
  sudo apt install nmap
- Safe TCP connect scan:
  nmap -sT -p 22,80,443 --min-rate 50 127.0.0.1
- Export XML for reports:
  nmap -sT -p 1-1024 -oX nmap.xml 127.0.0.1

9) Pyloris / DoS testing
- **Only for controlled lab resilience testing.** Prefer vegeta or locust for structured load tests.
- If using pyloris, run only against containers you control and monitor resource usage closely.

General safety checklist
- Always run offensive tools in isolated lab environments.
- Document the scope and obtain written permission before testing third-party targets.
- Monitor resource utilization and keep logs/artifacts for post-test analysis.
