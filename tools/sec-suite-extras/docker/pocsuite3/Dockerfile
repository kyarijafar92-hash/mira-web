FROM python:3.11-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/pocsuite3
RUN pip install --no-cache-dir pocsuite3
ENTRYPOINT ["pocsuite3"]
