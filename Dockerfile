FROM python:2.7-wheezy


RUN mkdir /code
WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 3000
ENTRYPOINT python ./bin/start_server.py

