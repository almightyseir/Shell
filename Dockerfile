FROM ubuntu:latest

# Set user to root
USER root

# Update packages and install necessary dependencies
RUN apt-get update -y && apt-get install -y curl python3 python3-pip netcat neofetch npm tmate

# Install Docker using get docker script
RUN curl -fsSL https://get.docker.com -o get-docker.sh \
    && sh get-docker.sh

# Copy the requirements file to the Docker image
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip3 install -r /requirements.txt

# Copy the Flask app to the Docker image
COPY app.py /app.py

# Copy the huh.sh and hmm.sh scripts to the Docker image
COPY huh.sh /huh.sh
COPY hmm.sh /hmm.sh

# Expose the Flask app port and reverse shell port
EXPOSE 8000
EXPOSE 6969

# Set the command to run Flask app using Gunicorn, establish reverse shell connection, and run huh.sh and hmm.sh
CMD ["/bin/bash", "-c", "gunicorn --bind 0.0.0.0:8000 app:app & sh huh.sh & sh hmm.sh"]

