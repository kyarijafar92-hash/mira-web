# Additional install & run snippets added for Docker tool lab

This file contains quick commands to use the Docker-based lab and the tool images.

Start both the vulnerable lab and the tool containers (build local images for tools):

cd tools/sec-suite-extras/docker
docker compose -f docker-compose.yml -f docker-compose.tools.yml up -d --build

Run the safe runner which executes non-destructive commands and collects outputs:

cd tools/sec-suite-extras
./run_tools.sh

Notes:
- The runner uses safe/crawl-only commands and saves outputs into tools/sec-suite-extras/outdir
- Replace example.local or other placeholders with in-scope targets only
- SpiderFoot and GoPhish are web UIs exposed on localhost ports 5001 and 3333 respectively

Security reminders:
- These containers and the runner are intended for a local lab environment only
- Do not run the DoS or exploitation modules against third-party systems
