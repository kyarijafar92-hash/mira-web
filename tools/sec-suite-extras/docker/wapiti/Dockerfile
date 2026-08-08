FROM python:3.11-slim
RUN apt-get update && apt-get install -y git gcc libxml2-dev libxslt1-dev zlib1g-dev python3-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/wapiti
RUN pip install --no-cache-dir wapiti
ENTRYPOINT ["wapiti"]
