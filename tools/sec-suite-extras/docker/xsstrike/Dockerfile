FROM python:3.11-slim
RUN apt-get update && apt-get install -y git build-essential libxml2-dev libxslt1-dev zlib1g-dev python3-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/xsstrike
RUN git clone https://github.com/s0md3v/XSStrike.git .
RUN pip install --no-cache-dir -r requirements.txt
ENV PATH="/opt/xsstrike:${PATH}"
# entrypoint will be overwritten by compose; keep one for direct runs
ENTRYPOINT ["python3","xsstrike.py"]
