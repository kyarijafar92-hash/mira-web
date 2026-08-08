FROM python:3.11-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/sherlock
RUN git clone https://github.com/sherlock-project/sherlock.git .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3","-c","print('sherlock image ready. Run python3 sherlock.py --help inside container.')"]
