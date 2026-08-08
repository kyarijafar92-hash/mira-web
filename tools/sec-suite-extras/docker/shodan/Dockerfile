FROM python:3.11-slim
RUN pip install --no-cache-dir shodan
WORKDIR /opt/shodan
ENTRYPOINT ["python3","-c","print('shodan python client ready. Set SHODAN_API_KEY env and run a script inside container.')"]
