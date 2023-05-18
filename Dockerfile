FROM ubuntu:latest

# Set user to root
USER root

# Update packages and install curl
RUN apt-get update -y && apt-get install -y curl

# Install teleconsole
RUN curl -sSL https://github.com/gravitational/teleconsole/releases/download/0.3.1/teleconsole-v0.3.1-linux-amd64.tar.gz | tar -xz -C /usr/local/bin teleconsole \
    && chmod +x /usr/local/bin/teleconsole

# Install tmate
RUN apt-get install -y tmate

# Start tmate in the background
CMD ["tmate", "-S", "/tmp/tmate.sock", "new-session", "-d"]
