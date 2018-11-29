# dupl

# Build the docker container
docker build . -t dupl-service:v1

# Run the docker container
docker run --rm -p 5000:5000 dupl-service:v1

# Run the docker container as deamon
docker run -d -p 5000:5000 dupl-service:v1

# Run the docker container interactively
docker run -it -p 5000:5000 dupl-service:v1 /bin/bash

# Save local docker image to tar file
docker save dupl-service > dupl-service.tar

# Load image from tar file
docker load -i dupl-service.tar

# GET the regions
curl http://127.0.0.1:5000/dopl/api/v1.0/regions

# GET the clubs
curl http://127.0.0.1:5000/dopl/api/v1.0/WTV

# GET the teams
curl http://127.0.0.1:5000/dopl/api/v1.0/WTV/10002

# GET the players
curl http://127.0.0.1:5000/dopl/api/v1.0/WTV/10002/418954
