FROM python:3.11-slim
RUN apt-get update && apt-get install -y git python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/responder
RUN git clone https://github.com/lgandx/Responder.git .
RUN pip install --no-cache-dir -r requirements.txt || true
ENTRYPOINT ["/bin/sh","-c","echo 'Responder image ready. Do NOT run Responder on shared networks. Start it manually in a lab.'; sleep infinity"]
