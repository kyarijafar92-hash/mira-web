FROM python:3.11-slim
RUN apt-get update && apt-get install -y git python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/cryptohack
RUN git clone https://github.com/cryptohack/cryptohack.git . || true
RUN pip install --no-cache-dir -r requirements.txt || true
ENTRYPOINT ["python3","-c","print('cryptohack image ready for offline crypto challenges.')"]
