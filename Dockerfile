FROM python:3.7-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    python3-dev \
    && apk add --no-cache unixodbc-dev g++ \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY src/ .

CMD [ "python", "./server.py" ]