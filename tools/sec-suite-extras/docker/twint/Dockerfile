FROM python:3.11-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/twint
RUN git clone https://github.com/twintproject/twint.git .
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir twint
ENTRYPOINT ["python3","-c","print('twint image ready. Run twint --help inside the container.')"]
