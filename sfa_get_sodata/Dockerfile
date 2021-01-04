# build
FROM salesforce/salesforcedx:latest-slim
# https://hub.docker.com/r/salesforce/salesforcedx
LABEL  maintainer "y.yoshimoto"

RUN apt-get -y update && apt-get -y install jq && apt-get clean

RUN sfdx force:project:create -n sfa_get_sodata --template standard
WORKDIR /sfa_get_sodata

COPY ./* /sfa_get_sodata/

#ENTRYPOINT [ "tail", "-f", "/dev/null" ]
ENTRYPOINT [ "/bin/bash", "./RequestAPICounts.sh" ]