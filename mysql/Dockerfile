FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=votary_db

COPY ./mysql/init /docker-entrypoint-initdb.d
