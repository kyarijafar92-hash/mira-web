#!/usr/bin/env bash
# run_demo.sh - bring up the Docker lab and run a few safe scans against it
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
COMPOSE_DIR="$HERE/docker"

echo "Starting docker lab..."
cd "$COMPOSE_DIR"
docker compose up -d
sleep 4

echo "Lab running:"
echo " - Juice Shop: http://localhost:3000"
echo " - DVWA: http://localhost"
echo " - httpbin: http://localhost:8000"

echo "Running a safe web audit against Juice Shop (requires sec-suite installed locally)"
if command -v python3 >/dev/null 2>&1; then
  if [ -f "$HERE/../sec-suite/sec_suite/web_audit.py" ]; then
    python3 - <<'PY'
import json
from pathlib import Path
from sec_suite import web_audit
res = web_audit.audit_url('http://localhost:3000')
Path('demo_web_audit.json').write_text(json.dumps(res,indent=2))
print('Wrote demo_web_audit.json')
PY
  else
    echo "sec-suite web_audit module not found locally; skipping automated demo audit. You can run the web audit CLI manually."
  fi
else
  echo "python3 not found; skipping demo audit"
fi

echo "Demo complete. Tear down the lab with: docker compose down"
