FROM node:18-alpine

RUN apk update \
 && apk --no-cache add openjdk17-jre-headless \
 && rm -rf /var/cache/apk/*

WORKDIR /root/src
