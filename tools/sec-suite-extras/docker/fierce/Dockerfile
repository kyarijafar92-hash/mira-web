FROM perl:5.36-slim
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/fierce
RUN git clone https://github.com/davidpepper/fierce-domain-scanner.git .
ENTRYPOINT ["/bin/sh","-c","echo 'fierce image ready. Run perl fierce.pl --help inside container.'; sleep infinity"]
