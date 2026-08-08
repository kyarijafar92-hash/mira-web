#!/usr/bin/env bash
# run_tools_extended.sh - extended safe runner for additional tool containers
# WARNING: This script intentionally avoids running intrusive actions (no MITM, no poisoning, no external scraping).
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DOCKER_DIR="$ROOT_DIR/docker"
OUT_DIR="$ROOT_DIR/outdir"
mkdir -p "$OUT_DIR"
cd "$DOCKER_DIR"

echo "Starting additional tool containers (build images)..."
docker compose -f docker-compose.yml -f docker-compose.tools.yml -f docker-compose.tools.extra.yml up -d --build
sleep 5

echo "Collecting help/version outputs from containers (safe, no external targets)"

# Impacket version
docker run --rm --network bridge -v "$OUT_DIR/impacket:/out" impacket:latest python3 -c "import pkg_resources;print('impacket', pkg_resources.get_distribution('impacket').version)" > "$OUT_DIR/impacket/version.txt" || true

# Twint help
docker run --rm --network bridge -v "$OUT_DIR/twint:/out" twint:latest python3 -c "import sys; import twint; print('twint installed')" > "$OUT_DIR/twint/info.txt" || true

# Sherlock help (no external queries)
docker run --rm -v "$OUT_DIR/sherlock:/out" sherlock:latest python3 sherlock.py --help > "$OUT_DIR/sherlock/help.txt" || true

# Knockpy help
docker run --rm -v "$OUT_DIR/knockpy:/out" knockpy:latest python3 -c "print('knockpy container ready')" > "$OUT_DIR/knockpy/info.txt" || true

# Fierce help
docker run --rm -v "$OUT_DIR/fierce:/out" fierce:latest perl fierce.pl --help > "$OUT_DIR/fierce/help.txt" || true

# Shodan client check
docker run --rm -v "$OUT_DIR/shodan:/out" shodan:latest python3 - <<'PY' > "$OUT_DIR/shodan/info.txt" || true
import shodan, os
print('shodan client installed')
print('SHODAN_API_KEY present:', 'SHODAN_API_KEY' in os.environ)
PY

# Mitmproxy - note: do NOT auto-start interception
echo "NOTICE: mitmproxy container is available at http://localhost:8080 but we DO NOT start MITM flows automatically. Start mitmproxy manually and configure test clients in lab."

# Responder: DO NOT RUN; just note presence
echo "Responder image built. DO NOT run Responder on shared networks."

echo "Extended outputs saved to: $OUT_DIR"
ls -R "$OUT_DIR" || true

echo "Done. To tear down: docker compose -f docker-compose.yml -f docker-compose.tools.yml -f docker-compose.tools.extra.yml down"
