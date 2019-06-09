FROM python:alpine3.7

COPY . /pollo

WORKDIR /pollo

ENV GOOGLE_APPLICATION_CREDENTIALS ./apikey.json 

RUN apk update  && \
  apk add ffmpeg && \
  apk add make && \
  apk add gcc && \
  apk add g++ && \
  make init

CMD python app.py

EXPOSE 3000
