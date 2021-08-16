FROM mongo
LABEL  maintainer "y.yoshimoto"
EXPOSE 27017

COPY ./Sampledb.js  /docker-entrypoint-initdb.d/Sampledb.js
CMD ["--auth"]
# mongoimport -u root -p mongo --db mongo_example