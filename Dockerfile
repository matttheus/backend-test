FROM python:3.9

ENV FLASK_APP=app

RUN groupadd flaskgroup 
RUN useradd -m -g flaskgroup -s /bin/bash flask

COPY . /home/code

WORKDIR /home/code

RUN chown -R flask:flaskgroup /home/code

RUN pip install -U pip && pip install -r requirements.txt

USER flask
