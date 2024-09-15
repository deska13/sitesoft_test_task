#!/usr/bin/env sh

set -o errexit
set -o nounset

# Check that Postgres is up and running
postgres_ready () {
  dockerize -wait "tcp://${POSTGRES_HOST:-parser_db}:${POSTGRES_PORT:-5432}" -timeout 10s
}

# Check that RabbitMQ is up and running
rabbitmq_ready () {
  dockerize -wait "tcp://${RABBITMQ_HOST:-rabbit}:${RABBITMQ_PORT:-5672}" -timeout 10s
}

# Check that redis is up and running
redis_ready() {
  dockerize -wait "tcp://${REDIS_HOST:-redis}:${REDIS_PORT:-6379}" -timeout 10s
}

until postgres_ready; do
  >&2 echo 'Postgres is unavailable - sleeping'
done
>&2 echo 'Postgres is up - continuing...'

>&2 echo 'Running migrations'
(python manage.py migrate)

until redis_ready; do
  >&2 echo 'Redis is unavailable - sleeping'
done
>&2 echo 'Redis is up - continuing...'

until rabbitmq_ready; do
  >&2 echo 'RabbitMQ is unavailable - sleeping'
done
>&2 echo 'RabbitMQ is up - continuing...'
