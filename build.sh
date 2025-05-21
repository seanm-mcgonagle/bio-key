#!/bin/bash
# This script builds a Docker image for a flask/python application and runs it in a container.
# Ensure the script is executable
#docker build -t my-app .
#docker run -p 5001:5001 -v $PWD:/app my-app

docker compose up -d

