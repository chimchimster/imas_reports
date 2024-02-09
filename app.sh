#!/bin/sh

SERVER=false
APPLICATION=false
CURRENT_DIR=$(pwd)
SERVER_PID=""
APPLICATION_PID=""

cleanup() {
    echo "Cleaning up..."
    [ -n "$SERVER_PID" ] && kill "$SERVER_PID"
    [ -n "$APPLICATION_PID" ] && kill "$APPLICATION_PID"
    exit 0
}

trap cleanup EXIT

usage() {
    echo "Usage: $0 [-s] [-a]" >&2
    echo "  -s, --server      Use only if you want to use server as producer for broker." >&2
    echo "  -a, --application Use only if you want to use application as consumer for broker." >&2
    exit 1
}

while [ "$#" -gt 0 ]; do
    case "$1" in
        -s|--server)
            SERVER=true
            ;;
        -a|--application)
            APPLICATION=true
            ;;
        -h|--help)
            usage
            ;;
        *)
            usage
            ;;
    esac
    shift
done

if [ "$SERVER" = true ] && [ "$APPLICATION" = true ]; then
    echo "Server and application are running now."
    python3 "$CURRENT_DIR/server/server.py" &
    SERVER_PID=$!
    python3 "$CURRENT_DIR/modules/listener.py" &
    APPLICATION_PID=$!
elif [ "$SERVER" = true ]; then
    echo "Only server is running now."
    gunicorn -w 15 -k gevent -b 0.0.0.0:5007 "server.server:app" --timeout 5000 &
    SERVER_PID=$!
else
    echo "Only application is running now."
    python3 "$CURRENT_DIR/modules/listener.py" &
    APPLICATION_PID=$!
fi

wait "$SERVER_PID"
wait "$APPLICATION_PID"
