FROM redis
LABEL  maintainer "y.yoshimoto"
EXPOSE 6379

COPY redis*.conf /usr/local/etc/redis/
CMD [ "redis-server", "/usr/local/etc/redis/redisStandard.conf" ]
# CMD ["redis-server"]
