# Wireless Controller (authorized agent) — README

This folder contains a small authorized remote-management prototype.
It is intended for devices you own and manage. The system uses a server (Flask)
that agents register with and poll for commands. Agents execute only a small
whitelist of allowed commands and send results back to the server.

Components
- server/: Flask app (server) — run on a trusted host accessible by devices
- agent/: Termux-compatible Python agent — run on devices you manage (Android/Termux)

Quick start (server)
1. Copy tools/wireless-controller/.env.example to tools/wireless-controller/.env and set values.
2. Create a Python venv and install dependencies:
   cd tools/wireless-controller/server
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
3. Start the server (ensure the .env is in tools/wireless-controller/):
   python app.py
4. Visit the admin UI in a browser and login with ADMIN_USER/ADMIN_PASS from .env.

Agent (Termux / device)
1. On the Android device (Termux), install Python and requests:
   pkg install python
   pip install requests
2. Edit the agent script or export environment vars:
   export MIRA_SERVER=http://your-server:5000
   export MIRA_REGISTER_SECRET=register-secret
3. Run the agent:
   python3 termux_agent.py
4. After registration, the device should appear in the server UI. From the UI you can queue a command (whitelisted) and the agent will poll, execute, and return results.

Security & notes
- This is a proof-of-concept. Do NOT expose the server without TLS (use a reverse proxy like Caddy/Nginx with HTTPS).
- Use strong secrets for ADMIN_PASS and AGENT_REGISTER_SECRET.
- The agent only executes a small whitelist of harmless commands; expand with caution.
- You must have explicit permission to install and run agents on any device.

If you want, I can harden the setup (HTTPS, JWT auth, signed messages, WebSocket push, device grouping) and push updates.
