FROM python:3.8

RUN apt-get update
RUN apt-get install git

RUN mkdir /srv/project
WORKDIR /srv

COPY ./src ./project
COPY ./requirements.txt ./
COPY ./runserver.sh ./


RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0:8000"]
