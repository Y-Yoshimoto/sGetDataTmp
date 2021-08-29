# FROM node:latest
#FROM python:alpine
FROM python:slim-bullseye
LABEL maintaner='y-yoshimoto'

#RUN apk --no-cache add gcc musl-dev python3-dev libffi-dev openssl-dev rust cargo

### pip
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip freeze > requirements.lock

# Salesforce認証情報
COPY ./.sfadxinfo.pem /
# Box認証情報
COPY ./.config.json /

RUN mkdir /uploadvolume
WORKDIR /usr/src
VOLUME /usr/src
# COPY duplicateapp/src/* ./

ENTRYPOINT ["tail", "-f", "/dev/null"]