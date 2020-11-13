FROM python:3.8

RUN apt-get update
RUN apt-get install git

RUN mkdir -p /srv/project/commands
WORKDIR /srv/project

COPY ./src ./
COPY ./requirements.txt ./
COPY ./commands/ ./commands

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["bash"]
