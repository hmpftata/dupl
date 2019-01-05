#!/bin/bash

docker build . -t dupl-service:v1

docker save dupl-service:v1 > dupl-service.tar

gzip dupl-service.tar

scp dupl-service.tar.gz stefan@185.101.159.191:/home/stefan/Projects/dupl
scp dupl_service_container_load.sh stefan@185.101.159.191:/home/stefan/Projects/dupl


