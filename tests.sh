#!/bin/sh

python ./app.py &
APP_PID=$!

sleep 2s

python ./tests.py

kill "$APP_PID"
