FROM ubuntu:latest

# Set user to root
USER root

# Update packages and install necessary dependencies
RUN apt-get update -y && \
    apt-get install -y curl python3 python3-pip tmate python3-venv

# Copy the requirements file to the Docker image
COPY requirements.txt /requirements.txt

# Create a virtual environment and install dependencies
RUN python3 -m venv /venv
RUN /venv/bin/python -m pip install --upgrade pip
RUN /venv/bin/pip install -r /requirements.txt

# Copy the Flask app to the Docker image
COPY app.py /app.py

# Copy other necessary scripts if needed

# Expose the Flask app port and reverse shell port
EXPOSE 8000

# Set the command to run Flask app using Gunicorn, establish reverse shell connection, and run other scripts
CMD ["/bin/bash", "-c", "source /venv/bin/activate && gunicorn --bind 0.0.0.0:8000 app:app"]
