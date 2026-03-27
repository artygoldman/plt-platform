#!/usr/bin/env bash
set -e

HOST="$1"
PORT="$2"
shift 2
CMD="$@"

TIMEOUT=15
ELAPSED=0

until nc -z "$HOST" "$PORT" 2>/dev/null; do
  if [ $ELAPSED -ge $TIMEOUT ]; then
    echo "Timeout waiting for $HOST:$PORT"
    exit 1
  fi
  echo "Waiting for $HOST:$PORT... ($ELAPSED/$TIMEOUT)"
  sleep 1
  ELAPSED=$((ELAPSED + 1))
done

echo "$HOST:$PORT is available"
exec $CMD
