FROM python:3.6.8-jessie

RUN  mkdir /opt/app && cd /opt/app

WORKDIR /opt/app

COPY Pipfile.lock .
COPY Pipfile .

RUN pip install --upgrade pip && pip install pipenv && pipenv sync



ENTRYPOINT ["pipenv", "run"]
