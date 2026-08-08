FROM python:3.11-slim
RUN apt-get update && apt-get install -y git build-essential libssl-dev libffi-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/impacket
RUN pip install --no-cache-dir impacket
ENTRYPOINT ["python3","-c","import impacket;print('impacket version:',__import__('pkg_resources').get_distribution('impacket').version)"]
