FROM python:3


RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./

RUN apt-get clean all && apt-get update && apt-get install ffmpeg --assume-yes && rm -rf /var/cache/apt/*

COPY shamean /usr/local/bin/

EXPOSE 5000
ENTRYPOINT python ./bin/start_server.py

