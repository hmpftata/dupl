#!/bin/bash

docker ps
docker stop $(docker ps -q --filter "ancestor=dupl-service:v1")
docker ps

