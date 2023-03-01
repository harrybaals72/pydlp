FROM python:3.10-slim-buster

EXPOSE 5353

RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /

COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# COPY app.py .
COPY *.py /app/
COPY binaries/ /usr/local/bin/

# CMD [ "python", "app.py" ]
CMD [ "python", "/app/main.py" ]