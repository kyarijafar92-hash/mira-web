FROM python:3.11-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/sublist3r
RUN git clone https://github.com/aboul3la/Sublist3r.git .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3","sublist3r.py"]
