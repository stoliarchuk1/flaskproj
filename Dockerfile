FROM python:3.10

WORKDIR /flaskproj

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /flaskproj

CMD flask --app flaskproj run -h 0.0.0.0 -p $PORT