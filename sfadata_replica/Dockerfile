# build
#FROM salesforce/salesforcedx:latest-slim
FROM node:current-buster-slim
# https://hub.docker.com/r/salesforce/salesforcedx
LABEL  maintainer "y.yoshimoto"
ENV APPNAME sfa_get_sodata

RUN npm install --global sfdx-cli
RUN apt-get -y update && apt-get -y install jq curl && apt-get clean

RUN sfdx force:project:create -n $APPNAME --template standard
WORKDIR /$APPNAME

COPY ./config/* /$APPNAME/
COPY ./script/* /$APPNAME/
RUN mkdir /uploadvolume/

#ENTRYPOINT [ "tail", "-f", "/dev/null" ]
ENTRYPOINT [ "/bin/bash", "./RequestAPICounts.sh" ]