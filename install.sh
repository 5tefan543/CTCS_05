#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define the container and image names
CONTAINER_NAME="ctcs05"
IMAGE_NAME="ctcs05"

# Delete the specific container by name if it exists
if [ $(docker ps -aq -f name="^${CONTAINER_NAME}$") ]; then
    echo "Stopping and removing container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
else
    echo "No container named $CONTAINER_NAME found. Skipping removal."
fi

# Delete the specific image if it exists
if [ $(docker images -q $IMAGE_NAME) ]; then
    echo "Removing image: $IMAGE_NAME"
    docker rmi -f $IMAGE_NAME
else
    echo "No image named $IMAGE_NAME found. Skipping removal."
fi

# Build the Dockerfile
echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Run the Docker container and open an interactive terminal
echo "Running Docker container: $CONTAINER_NAME"
docker run --name $CONTAINER_NAME -it $IMAGE_NAME