FROM mongo
LABEL  maintainer "y.yoshimoto"
EXPOSE 27017

COPY ./sObjectData.js  /docker-entrypoint-initdb.d/sObjectData.js
CMD ["--auth"]
# mongoimport -u root -p mongo --db mongo_example