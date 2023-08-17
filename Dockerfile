FROM python:3.10-slim-buster

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /downloads

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# COPY app.py .
COPY *.py /app/
COPY binaries/ /usr/local/bin/

ENTRYPOINT [ "python", "/app/main.py" ]