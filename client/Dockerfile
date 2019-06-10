FROM node:10.16-alpine

COPY . /client
WORKDIR /client
RUN yarn install

CMD yarn run serve -- --port=3001

EXPOSE 3001
