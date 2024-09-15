#! /usr/bin/env sh
set -e

HOST=${SERVER_HOST:-0.0.0.0}
PORT=${SERVER_PORT:-8000}

# echo "Starting Django server"
# exec python3 manage.py runserver
echo "Starting Uvicorn"
exec uvicorn admin.asgi:app --reload --host $HOST --port $PORT --log-level debug
