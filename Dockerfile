FROM ubuntu:latest

# Set user to root
USER root

# Update packages and install curl
RUN apt-get update -y && apt-get install -y curl

# Set environment variable for non-interactive installation
ENV DEBIAN_FRONTEND noninteractive

# Install build dependencies
RUN apt-get install -y build-essential cmake git libjson-c-dev libwebsockets-dev

# Clone and build ttyd
RUN git clone https://github.com/tsl0922/ttyd.git && \
    cd ttyd && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

# Expose port
EXPOSE 8080

# Start ttyd
CMD ttyd -p 8080 bash
