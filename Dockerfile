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

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - && \
    apt-get install -y nodejs

# Install the localhost npm package globally
RUN npm install -g localhost

# Expose port
EXPOSE 8080

# Start ttyd and tunnel using localhost npm package
CMD ttyd -p 8080 bash & \
    localhost run --port 8080 --subdomain hahaserver
