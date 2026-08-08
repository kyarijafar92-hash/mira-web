#!/usr/bin/env bash
# run_tools.sh - safely start the lab and run benign/non-destructive commands for each tool
# WARNING: This script runs tools only against the local Docker lab (juice-shop, dvwa, httpbin)
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_DIR="$ROOT_DIR/docker"
OUT_DIR="$ROOT_DIR/outdir"
mkdir -p "$OUT_DIR"
cd "$DOCKER_DIR"

echo "Starting lab + tool containers (will build local images)..."
docker compose -f docker-compose.yml -f docker-compose.tools.yml up -d --build
sleep 5

# Run safe/non-destructive commands and save outputs to the outdir
# 1) Wapiti scan (non-aggressive) against Juice Shop
echo "Running wapiti against http://juice-shop:3000 (non-aggressive)"
docker run --rm --network="$(docker compose -f docker-compose.yml -f docker-compose.tools.yml ps -q | head -n1 >/dev/null 2>&1 || echo bridge)" \
  -v "$OUT_DIR/wapiti:/out" wapiti:latest wapiti -u http://juice-shop:3000 -f json -o /out/wapiti.json || true

# 2) XSStrike crawl-only against Juice Shop
echo "Running XSStrike crawl (discovery) against http://juice-shop:3000"
docker run --rm --network bridge -v "$OUT_DIR/xsstrike:/out" xsstrike:latest python3 xsstrike.py -u http://juice-shop:3000 --crawl > "$OUT_DIR/xsstrike/xsstrike.txt" || true

# 3) Pocsuite3 - show help to verify install
echo "Exporting pocsuite3 help output"
docker run --rm pocsuite3:latest --help > "$OUT_DIR/pocsuite3/help.txt" || true

# 4) Sublist3r - run against example.local (replace with in-scope domain if needed)
echo "Running Sublist3r (passive enumeration) against example.local"
docker run --rm --network bridge -v "$OUT_DIR/sublist3r:/out" sublist3r:latest -d example.local -o /out/subs.txt || true

# 5) SpiderFoot is web UI - create note
echo "SpiderFoot is available at http://localhost:5001 (web UI)."

# 6) GoPhish is available at http://localhost:3333 (admin) — use for training only

# 7) Print a summary of outputs
sleep 1
echo "Outputs saved to: $OUT_DIR"
ls -R "$OUT_DIR" || true

echo "Done. Tear down with: docker compose -f docker-compose.yml -f docker-compose.tools.yml down"
