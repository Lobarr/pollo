FROM python:3.6-alpine

COPY . /pollo

WORKDIR /pollo

ENV GOOGLE_APPLICATION_KEY ./apikey.json

RUN sudo apt update  && \
  sudo apt install ffmpeg && \
  make init

CMD python app.py

EXPOSE 3000