FROM python:3.11-slim
RUN apt-get update && apt-get install -y mitmproxy && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/mitmproxy
# mitmproxy installed via apt; keep container ready for manual use
ENTRYPOINT ["mitmweb"]
