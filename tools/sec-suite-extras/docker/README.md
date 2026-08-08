Docker lab for local, safe testing

This docker-compose file runs two intentionally vulnerable web apps for training:
- Juice Shop (port 3000)
- DVWA (port 80)
- httpbin (port 8000) — optional target for benign HTTP tests

How to run (on a machine with Docker & docker-compose):

1. From this folder:
   docker compose up -d

2. Visit the apps:
   - Juice Shop: http://localhost:3000
   - DVWA: http://localhost/
   - httpbin: http://localhost:8000

3. When finished, bring down the lab:
   docker compose down

Security notes:
- Only run this on an isolated host (not a public server). These apps are intentionally vulnerable.
- Do not expose these ports to the public Internet.
