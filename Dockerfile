FROM python:alpine3.7

COPY . /pollo

WORKDIR /pollo

ENV GOOGLE_APPLICATION_CREDENTIALS ./apikey.json 

RUN apk update  && \
  apk add make && \
  apk add gcc && \
  apk add g++ && \
  apk add libffi-dev && \
  apk add openssl-dev && \
  apk add ffmpeg && \
  pip install --upgrade pip && \
  make init

CMD python app.py

EXPOSE 3000
