# Use the official Ubuntu developer image as the base image
FROM mcr.microsoft.com/devcontainers/base:jammy

# Update the package repository and upgrade Ubuntu packages
RUN apt-get update && apt-get upgrade -y

# Install necessary dependencies for OpenCV which are present in OS but not in containers by default
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Set environment variables, if necessary

# Note: The DEBIAN_FRONTEND export avoids warnings when you go on to work with your container.
#       See more on https://code.visualstudio.com/docs/devcontainers/create-dev-container#_dockerfile
ENV DEBIAN_FRONTEND=noninteractive
