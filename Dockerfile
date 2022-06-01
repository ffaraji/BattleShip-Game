FROM python:3.7.3-alpine3.9 as base

WORKDIR /

COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN pip install requests

COPY . /

CMD [ "python3", "startServer.py" ]

