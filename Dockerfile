FROM python:3.10.6-slim

ENV FLASK_APP=flaskproj
ENV FLASK_DEBUG=$FLASK_DEBUG

COPY requirements.txt /opt

RUN python3 -m pip install -r /opt/requirements.txt

COPY flaskproj /opt/flaskproj

WORKDIR /opt

CMD flask run --host 0.0.0.0 -p $PORT