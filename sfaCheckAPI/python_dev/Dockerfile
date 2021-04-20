# FROM node:latest
FROM python:alpine
LABEL maintaner='y-yoshimoto'

RUN apk --no-cache add gcc musl-dev python3-dev libffi-dev openssl-dev rust cargo

### pip
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && pip freeze > requirements.lock
COPY sfadxinfo.pem ./

WORKDIR /usr/src
VOLUME /usr/src


# COPY python_dev/src/* ./

ENTRYPOINT ["tail", "-f", "/dev/null"]