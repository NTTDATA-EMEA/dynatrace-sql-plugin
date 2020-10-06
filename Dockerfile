FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt-get update && \
    apt-get install -y unixodbc-dev && \
    pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD [ "python", "./server.py" ]