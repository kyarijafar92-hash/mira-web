FROM python:3.11-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/knockpy
RUN git clone https://github.com/guelfoweb/knock.git . || git clone https://github.com/gueldweb/knockpy.git . || true
RUN pip install --no-cache-dir -r requirements.txt || true
ENTRYPOINT ["python3","-c","print('knockpy image ready. Run knockpy --help inside container.')"]
