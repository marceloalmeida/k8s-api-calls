FROM python:3

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN \
    pip3 install -r /app/requirements.txt && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /app

CMD ["python", "main.py"]
