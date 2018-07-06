#!/bin/bash

# Build and deploy on master branch
if [[ $CI_COMMIT_REF_SLUG == 'master' ]]; then
    echo "Connecting to docker hub"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

    echo "Building..."
    docker build -t pythondiscord/bot-verification:latest -f docker/Dockerfile .

    echo "Pushing image to Docker Hub..."
    docker push pythondiscord/bot-verification:latest
else
    echo "Skipping deploy"
fi
